from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.applicant import Applicant
from app.models.application import Application
from app.models.credit_profile import CreditProfile
from app.models.credit_rating import CreditRating
from app.models.employment import Employment
from app.models.existing_loan import ExistingLoan
from app.models.lender_account import LenderAccount
from app.models.loan_assessment import LoanAssessment
from app.models.loan_request import LoanRequest
from app.models.debt_payment_metrics import DebtPaymentMetrics


class LenderRepository:

    @staticmethod
    def get_lender_by_email(
        db: Session,
        email: str
    ) -> Optional[LenderAccount]:
        return (
            db.query(LenderAccount)
            .filter(LenderAccount.email == email)
            .first()
        )

    @staticmethod
    def get_lender_by_id(
        db: Session,
        lender_id: int
    ) -> Optional[LenderAccount]:
        return (
            db.query(LenderAccount)
            .filter(LenderAccount.lender_id == lender_id)
            .first()
        )

    @staticmethod
    def create_lender_account(
        db: Session,
        email: str,
        password_hash: str,
        full_name: str
    ) -> LenderAccount:
        account = LenderAccount(
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_pending_applications(
        db: Session
    ):
        """
        Fetch all applications with status 'Pending' or 'Under Review',
        joined with applicant details and loan assessment.
        """
        return (
            db.query(
                Application,
                Applicant,
                CreditRating,
                LoanAssessment
            )
            .join(
                Applicant,
                Applicant.applicant_id == Application.applicant_id
            )
            .outerjoin(
                CreditRating,
                CreditRating.application_id == Application.application_id
            )
            .outerjoin(
                LoanAssessment,
                LoanAssessment.application_id == Application.application_id
            )
            .filter(
                Application.status.in_(["Pending", "Under Review"])
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .all()
        )

    @staticmethod
    def get_all_applications(
        db: Session
    ):
        """
        Fetch all applications with applicant and assessment details for overview.
        """
        return (
            db.query(
                Application,
                Applicant,
                CreditRating,
                LoanAssessment
            )
            .join(
                Applicant,
                Applicant.applicant_id == Application.applicant_id
            )
            .outerjoin(
                CreditRating,
                CreditRating.application_id == Application.application_id
            )
            .outerjoin(
                LoanAssessment,
                LoanAssessment.application_id == Application.application_id
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .all()
        )

    @staticmethod
    def get_daily_stats(
        db: Session
    ) -> dict:
        today = date.today()

        total_pending = (
            db.query(func.count(Application.application_id))
            .filter(Application.status.in_(["Pending", "Under Review"]))
            .scalar()
            or 0
        )

        approved_today = (
            db.query(func.count(Application.application_id))
            .filter(
                Application.status == "Approved",
                Application.application_date == today
            )
            .scalar()
            or 0
        )

        rejected_today = (
            db.query(func.count(Application.application_id))
            .filter(
                Application.status == "Rejected",
                Application.application_date == today
            )
            .scalar()
            or 0
        )

        return {
            "total_pending": total_pending,
            "approved_today": approved_today,
            "rejected_today": rejected_today
        }

    @staticmethod
    def get_application_by_id(
        db: Session,
        application_id: int
    ) -> Optional[Application]:
        return (
            db.query(Application)
            .filter(Application.application_id == application_id)
            .first()
        )

    @staticmethod
    def update_application_decision(
        db: Session,
        application: Application,
        status: str,
        rejection_reason: Optional[str],
        lender_id: int
    ) -> Application:
        application.status = status
        application.rejection_reason = rejection_reason
        application.reviewed_by = lender_id

        # Also update assessment decision if assessment exists
        assessment = (
            db.query(LoanAssessment)
            .filter(LoanAssessment.application_id == application.application_id)
            .first()
        )
        if assessment:
            if status == "Approved":
                assessment.decision = "APPROVE"
            elif status == "Rejected":
                assessment.decision = "REJECT"

        db.commit()
        db.refresh(application)
        return application
