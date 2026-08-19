from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_lender_token,
    hash_password,
    verify_password
)
from app.models.application import Application
from app.repositories.applicant_repository import ApplicantRepository
from app.repositories.lender_repository import LenderRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.lender import (
    LenderLoginRequest,
    LenderRegisterRequest,
    PendingApplicationItem,
    PendingApplicationsResponse
)


class LenderService:

    # =========================================================
    # LENDER REGISTRATION
    # =========================================================

    @staticmethod
    def register_lender(
        db: Session,
        data: LenderRegisterRequest
    ):
        existing_lender = LenderRepository.get_lender_by_email(
            db,
            data.email
        )
        if existing_lender:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A lender with this email already exists"
            )

        password_hash = hash_password(data.password)
        account = LenderRepository.create_lender_account(
            db=db,
            email=data.email,
            password_hash=password_hash,
            full_name=data.full_name
        )

        token = create_lender_token(account.lender_id)

        return {
            "message": "Lender registered successfully",
            "access_token": token,
            "token_type": "bearer",
            "lender_id": account.lender_id,
            "full_name": account.full_name,
            "email": account.email
        }

    # =========================================================
    # LENDER LOGIN
    # =========================================================

    @staticmethod
    def login_lender(
        db: Session,
        data: LenderLoginRequest
    ):
        lender = LenderRepository.get_lender_by_email(
            db,
            data.email
        )
        if not lender:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not lender.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Lender account is deactivated"
            )

        if not verify_password(data.password, lender.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_lender_token(lender.lender_id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "lender_id": lender.lender_id,
            "full_name": lender.full_name,
            "email": lender.email
        }

    # =========================================================
    # PENDING APPLICATIONS
    # =========================================================

    @staticmethod
    def get_pending_applications(
        db: Session
    ) -> dict:
        rows = LenderRepository.get_pending_applications(db)
        stats = LenderRepository.get_daily_stats(db)

        items = []
        for application, applicant, credit_rating, assessment in rows:
            items.append(
                PendingApplicationItem(
                    application_id=application.application_id,
                    applicant_id=applicant.applicant_id,
                    applicant_name=applicant.full_name,
                    applicant_email=applicant.email,
                    application_date=(
                        application.application_date.isoformat()
                        if application.application_date
                        else None
                    ),
                    loan_amount=float(application.loan_amount),
                    loan_tenure=application.loan_tenure,
                    loan_purpose=application.loan_purpose,
                    status=application.status,
                    credit_score=(
                        credit_rating.credit_score
                        if credit_rating
                        else None
                    ),
                    risk_grade=(
                        credit_rating.risk_grade
                        if credit_rating
                        else None
                    ),
                    risk_level=(
                        assessment.risk_level
                        if assessment
                        else None
                    ),
                    approval_probability=(
                        float(assessment.approval_probability)
                        if assessment and assessment.approval_probability is not None
                        else None
                    ),
                    risk_score=(
                        float(assessment.risk_score)
                        if assessment and assessment.risk_score is not None
                        else None
                    ),
                    rejection_reason=application.rejection_reason
                )
            )

        return {
            "applications": items,
            "total_pending": stats["total_pending"],
            "approved_today": stats["approved_today"],
            "rejected_today": stats["rejected_today"]
        }

    # =========================================================
    # ALL APPLICATIONS
    # =========================================================

    @staticmethod
    def get_all_applications(
        db: Session
    ) -> dict:
        rows = LenderRepository.get_all_applications(db)
        stats = LenderRepository.get_daily_stats(db)

        items = []
        for application, applicant, credit_rating, assessment in rows:
            items.append(
                PendingApplicationItem(
                    application_id=application.application_id,
                    applicant_id=applicant.applicant_id,
                    applicant_name=applicant.full_name,
                    applicant_email=applicant.email,
                    application_date=(
                        application.application_date.isoformat()
                        if application.application_date
                        else None
                    ),
                    loan_amount=float(application.loan_amount),
                    loan_tenure=application.loan_tenure,
                    loan_purpose=application.loan_purpose,
                    status=application.status,
                    credit_score=(
                        credit_rating.credit_score
                        if credit_rating
                        else None
                    ),
                    risk_grade=(
                        credit_rating.risk_grade
                        if credit_rating
                        else None
                    ),
                    risk_level=(
                        assessment.risk_level
                        if assessment
                        else None
                    ),
                    approval_probability=(
                        float(assessment.approval_probability)
                        if assessment and assessment.approval_probability is not None
                        else None
                    ),
                    risk_score=(
                        float(assessment.risk_score)
                        if assessment and assessment.risk_score is not None
                        else None
                    ),
                    rejection_reason=application.rejection_reason
                )
            )

        return {
            "applications": items,
            "total_pending": stats["total_pending"],
            "approved_today": stats["approved_today"],
            "rejected_today": stats["rejected_today"]
        }

    # =========================================================
    # APPLICATION REVIEW DETAILS FOR LENDER
    # =========================================================

    @staticmethod
    def get_application_for_review(
        db: Session,
        application_id: int
    ):
        application = LenderRepository.get_application_by_id(
            db,
            application_id
        )
        if not application:
            return None

        applicant_id = application.applicant_id

        applicant = ApplicantRepository.get_applicant(
            db,
            applicant_id
        )
        if not applicant:
            return None

        employment = ApplicantRepository.get_employment(
            db,
            applicant_id
        )

        credit_profile = ApplicantRepository.get_credit_profile(
            db,
            application_id
        )
        credit_rating = ApplicantRepository.get_credit_rating(
            db,
            application_id
        )

        # Fallback to historical credit profile / rating if not in current
        if credit_profile is None or credit_rating is None:
            applications = ApplicantRepository.get_applications(
                db,
                applicant_id
            )
            for hist_app in applications:
                if hist_app.application_id == application_id:
                    continue
                hist_profile = ApplicantRepository.get_credit_profile(
                    db,
                    hist_app.application_id
                )
                hist_rating = ApplicantRepository.get_credit_rating(
                    db,
                    hist_app.application_id
                )
                if hist_profile is not None and hist_rating is not None:
                    if credit_profile is None:
                        credit_profile = hist_profile
                    if credit_rating is None:
                        credit_rating = hist_rating
                    break

        loan_request = ApplicantRepository.get_loan_request(
            db,
            application_id
        )

        debt_metrics = None
        if loan_request:
            debt_metrics = ApplicantRepository.get_debt_payment_metrics(
                db,
                loan_request.loan_request_id
            )

        if debt_metrics is None:
            applications = ApplicantRepository.get_applications(
                db,
                applicant_id
            )
            for hist_app in applications:
                if hist_app.application_id == application_id:
                    continue
                hist_req = ApplicantRepository.get_loan_request(
                    db,
                    hist_app.application_id
                )
                if hist_req:
                    hist_metrics = ApplicantRepository.get_debt_payment_metrics(
                        db,
                        hist_req.loan_request_id
                    )
                    if hist_metrics:
                        debt_metrics = hist_metrics
                        break

        existing_loans = ApplicantRepository.get_existing_loans(
            db,
            applicant_id
        )

        assessment_result = LoanRepository.get_application_details(
            db=db,
            applicant_id=applicant_id,
            application_id=application_id
        )
        assessment = assessment_result[1] if assessment_result else None

        return {
            "personal": {
                "applicant_id": applicant.applicant_id,
                "full_name": applicant.full_name,
                "date_of_birth": (
                    applicant.date_of_birth.isoformat()
                    if applicant.date_of_birth
                    else None
                ),
                "age": applicant.age,
                "gender": applicant.gender,
                "email": applicant.email,
                "phone_number": applicant.phone_number,
                "address": applicant.address
            },
            "employment": (
                {
                    "employment_id": employment.employment_id,
                    "employment_type": employment.employment_type,
                    "employer_name": employment.employer_name,
                    "annual_income": (
                        float(employment.annual_income)
                        if employment.annual_income is not None
                        else None
                    ),
                    "employment_duration": employment.employment_duration
                }
                if employment
                else None
            ),
            "application": {
                "application_id": application.application_id,
                "application_date": (
                    application.application_date.isoformat()
                    if application.application_date
                    else None
                ),
                "loan_purpose": application.loan_purpose,
                "loan_amount": float(application.loan_amount),
                "loan_tenure": application.loan_tenure,
                "status": application.status,
                "rejection_reason": application.rejection_reason,
                "reviewed_by": application.reviewed_by
            },
            "credit_profile": (
                {
                    "profile_id": credit_profile.profile_id,
                    "number_of_dependents": credit_profile.number_of_dependents,
                    "debt_to_income_ratio": (
                        float(credit_profile.debt_to_income_ratio)
                        if credit_profile.debt_to_income_ratio is not None
                        else None
                    ),
                    "credit_utilization": (
                        float(credit_profile.credit_utilization)
                        if credit_profile.credit_utilization is not None
                        else None
                    ),
                    "previous_defaults": credit_profile.previous_defaults,
                    "missed_payments": credit_profile.missed_payments,
                    "maximum_days_past_due": credit_profile.maximum_days_past_due,
                    "recent_credit_enquiries": credit_profile.recent_credit_enquiries,
                    "number_of_credit_accounts": credit_profile.number_of_credit_accounts,
                    "credit_history_length": credit_profile.credit_history_length,
                    "payment_history": (
                        float(credit_profile.payment_history)
                        if credit_profile.payment_history is not None
                        else None
                    ),
                    "loan_to_income_ratio": (
                        float(credit_profile.loan_to_income_ratio)
                        if credit_profile.loan_to_income_ratio is not None
                        else None
                    )
                }
                if credit_profile
                else None
            ),
            "credit_rating": (
                {
                    "rating_id": credit_rating.rating_id,
                    "credit_score": credit_rating.credit_score,
                    "risk_grade": credit_rating.risk_grade,
                    "rating_date": (
                        credit_rating.rating_date.isoformat()
                        if credit_rating.rating_date
                        else None
                    )
                }
                if credit_rating
                else None
            ),
            "loan_request": (
                {
                    "loan_request_id": loan_request.loan_request_id,
                    "loan_amount": float(loan_request.loan_amount),
                    "loan_tenure": loan_request.loan_tenure
                }
                if loan_request
                else None
            ),
            "debt_payment_metrics": (
                {
                    "metrics_id": debt_metrics.metrics_id,
                    "existing_loans_count": debt_metrics.existing_loans_count,
                    "total_outstanding_debt": (
                        float(debt_metrics.total_outstanding_debt)
                        if debt_metrics.total_outstanding_debt is not None
                        else None
                    ),
                    "monthly_emi": (
                        float(debt_metrics.monthly_emi)
                        if debt_metrics.monthly_emi is not None
                        else None
                    )
                }
                if debt_metrics
                else None
            ),
            "existing_loans": [
                {
                    "existing_loan_id": loan.existing_loan_id,
                    "loan_request_id": loan.loan_request_id,
                    "loan_type": loan.loan_type,
                    "loan_amount": (
                        float(loan.loan_amount)
                        if loan.loan_amount is not None
                        else None
                    ),
                    "outstanding_amount": (
                        float(loan.outstanding_amount)
                        if loan.outstanding_amount is not None
                        else None
                    ),
                    "monthly_emi": (
                        float(loan.monthly_emi)
                        if loan.monthly_emi is not None
                        else None
                    )
                }
                for loan in existing_loans
            ],
            "assessment": (
                {
                    "assessment_id": assessment.assessment_id,
                    "prediction": assessment.prediction,
                    "approval_probability": (
                        float(assessment.approval_probability)
                        if assessment.approval_probability is not None
                        else None
                    ),
                    "risk_score": (
                        float(assessment.risk_score)
                        if assessment.risk_score is not None
                        else None
                    ),
                    "risk_level": assessment.risk_level,
                    "decision": assessment.decision,
                    "risk_factors": (
                        assessment.risk_factors
                        if assessment.risk_factors
                        else []
                    )
                }
                if assessment
                else None
            )
        }

    # =========================================================
    # LENDER DECISION (APPROVE / REJECT)
    # =========================================================

    @staticmethod
    def update_application_decision(
        db: Session,
        application_id: int,
        decision: str,
        rejection_reason: Optional[str],
        lender_id: int
    ):
        application = LenderRepository.get_application_by_id(
            db,
            application_id
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        decision_upper = decision.strip().upper()
        if decision_upper in ["APPROVE", "APPROVED"]:
            new_status = "Approved"
            final_rejection_reason = None
        elif decision_upper in ["REJECT", "REJECTED"]:
            new_status = "Rejected"
            final_rejection_reason = (
                rejection_reason.strip()
                if rejection_reason
                else "Application does not meet the lender criteria."
            )
        elif decision_upper in ["REVIEW", "UNDER_REVIEW", "UNDER REVIEW"]:
            new_status = "Under Review"
            final_rejection_reason = None
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid decision: '{decision}'. Must be APPROVE, REJECT, or REVIEW."
            )

        updated_app = LenderRepository.update_application_decision(
            db=db,
            application=application,
            status=new_status,
            rejection_reason=final_rejection_reason,
            lender_id=lender_id
        )

        return {
            "message": f"Application #{application_id} has been marked as {new_status}",
            "application_id": updated_app.application_id,
            "status": updated_app.status,
            "rejection_reason": updated_app.rejection_reason
        }
