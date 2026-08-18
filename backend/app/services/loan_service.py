from sqlalchemy.orm import Session

from app.models.applicant import Applicant
from app.models.application import Application

from app.repositories.applicant_repository import (
    ApplicantRepository
)

from app.repositories.loan_repository import (
    LoanRepository
)


class LoanService:

    # =========================================================
    # LOAN HISTORY
    # =========================================================

    @staticmethod
    def get_loan_history(
        db: Session,
        applicant_id: int
    ):

        rows = (
            LoanRepository
            .get_application_history(
                db,
                applicant_id
            )
        )

        history = []

        for application, assessment in rows:

            item = {

                "application_id":
                    application.application_id,

                "application_date":
                    (
                        application.application_date.isoformat()
                        if application.application_date
                        else None
                    ),

                "loan_amount":
                    float(
                        application.loan_amount
                    ),

                "loan_tenure":
                    application.loan_tenure,

                "loan_purpose":
                    application.loan_purpose,

                "status":
                    application.status,

                "assessment_id":
                    (
                        assessment.assessment_id
                        if assessment
                        else None
                    ),

                "prediction":
                    (
                        assessment.prediction
                        if assessment
                        else None
                    ),

                "approval_probability":
                    (
                        float(
                            assessment.approval_probability
                        )
                        if assessment
                        and assessment.approval_probability
                        is not None
                        else None
                    ),

                "risk_score":
                    (
                        float(
                            assessment.risk_score
                        )
                        if assessment
                        and assessment.risk_score
                        is not None
                        else None
                    ),

                "risk_level":
                    (
                        assessment.risk_level
                        if assessment
                        else None
                    ),

                "decision":
                    (
                        assessment.decision
                        if assessment
                        else None
                    ),

                "risk_factors":
                    (
                        assessment.risk_factors
                        if assessment
                        and assessment.risk_factors
                        else []
                    )
            }

            history.append(item)

        return history


    # =========================================================
    # FULL APPLICATION DETAILS
    # =========================================================

    @staticmethod
    def get_full_application_details(
        db: Session,
        applicant_id: int,
        application_id: int
    ):

        # -----------------------------------------------------
        # 1. Verify application belongs to applicant
        # -----------------------------------------------------

        application = (
            db.query(Application)
            .filter(
                Application.application_id
                == application_id,

                Application.applicant_id
                == applicant_id
            )
            .first()
        )

        if application is None:
            return None


        # -----------------------------------------------------
        # 2. Applicant
        # -----------------------------------------------------

        applicant = (
            ApplicantRepository
            .get_applicant(
                db,
                applicant_id
            )
        )

        if applicant is None:
            return None


        # -----------------------------------------------------
        # 3. Employment
        # -----------------------------------------------------

        employment = (
            ApplicantRepository
            .get_employment(
                db,
                applicant_id
            )
        )


        # -----------------------------------------------------
        # 4. Historical credit profile
        # -----------------------------------------------------
        #
        # IMPORTANT:
        #
        # The NEW application may not have a credit profile.
        #
        # The ML model uses the applicant's historical
        # credit information.
        #
        # Therefore:
        #
        # First try current application.
        #
        # If unavailable, find the latest application
        # containing historical credit data.
        # -----------------------------------------------------

        credit_profile = (
            ApplicantRepository
            .get_credit_profile(
                db,
                application_id
            )
        )

        credit_rating = (
            ApplicantRepository
            .get_credit_rating(
                db,
                application_id
            )
        )


        # -----------------------------------------------------
        # 5. Loan request
        # -----------------------------------------------------

        loan_request = (
            ApplicantRepository
            .get_loan_request(
                db,
                application_id
            )
        )


        # -----------------------------------------------------
        # 6. Historical fallback
        # -----------------------------------------------------

        historical_application = None

        if (
            credit_profile is None
            or credit_rating is None
        ):

            applications = (
                ApplicantRepository
                .get_applications(
                    db,
                    applicant_id
                )
            )

            for historical_app in applications:

                if (
                    historical_app.application_id
                    == application_id
                ):
                    continue

                historical_profile = (
                    ApplicantRepository
                    .get_credit_profile(
                        db,
                        historical_app.application_id
                    )
                )

                historical_rating = (
                    ApplicantRepository
                    .get_credit_rating(
                        db,
                        historical_app.application_id
                    )
                )

                if (
                    historical_profile is not None
                    and historical_rating is not None
                ):

                    historical_application = (
                        historical_app
                    )

                    if credit_profile is None:
                        credit_profile = (
                            historical_profile
                        )

                    if credit_rating is None:
                        credit_rating = (
                            historical_rating
                        )

                    break


        # -----------------------------------------------------
        # 7. Debt payment metrics
        # -----------------------------------------------------

        debt_metrics = None

        if loan_request:

            debt_metrics = (
                ApplicantRepository
                .get_debt_payment_metrics(
                    db,
                    loan_request.loan_request_id
                )
            )


        # -----------------------------------------------------
        # 8. Historical debt metrics fallback
        # -----------------------------------------------------

        if debt_metrics is None:

            applications = (
                ApplicantRepository
                .get_applications(
                    db,
                    applicant_id
                )
            )

            for historical_app in applications:

                if (
                    historical_app.application_id
                    == application_id
                ):
                    continue

                historical_loan_request = (
                    ApplicantRepository
                    .get_loan_request(
                        db,
                        historical_app.application_id
                    )
                )

                if historical_loan_request:

                    historical_metrics = (
                        ApplicantRepository
                        .get_debt_payment_metrics(
                            db,
                            historical_loan_request.loan_request_id
                        )
                    )

                    if historical_metrics:

                        debt_metrics = (
                            historical_metrics
                        )

                        break


        # -----------------------------------------------------
        # 9. Existing loans
        # -----------------------------------------------------

        existing_loans = (
            ApplicantRepository
            .get_existing_loans(
                db,
                applicant_id
            )
        )


        # -----------------------------------------------------
        # 10. Assessment
        # -----------------------------------------------------

        assessment_result = (
            LoanRepository
            .get_application_details(
                db=db,
                applicant_id=applicant_id,
                application_id=application_id
            )
        )

        assessment = None

        if assessment_result:

            _, assessment = assessment_result


        # -----------------------------------------------------
        # 11. Return complete response
        # -----------------------------------------------------

        return {

            # =================================================
            # PERSONAL
            # =================================================

            "personal": {

                "applicant_id":
                    applicant.applicant_id,

                "full_name":
                    applicant.full_name,

                "date_of_birth":
                    (
                        applicant.date_of_birth.isoformat()
                        if applicant.date_of_birth
                        else None
                    ),

                "age":
                    applicant.age,

                "gender":
                    applicant.gender,

                "email":
                    applicant.email,

                "phone_number":
                    applicant.phone_number,

                "address":
                    applicant.address
            },


            # =================================================
            # EMPLOYMENT
            # =================================================

            "employment": (

                {

                    "employment_id":
                        employment.employment_id,

                    "employment_type":
                        employment.employment_type,

                    "employer_name":
                        employment.employer_name,

                    "annual_income":
                        (
                            float(
                                employment.annual_income
                            )
                            if employment.annual_income
                            is not None
                            else None
                        ),

                    "employment_duration":
                        employment.employment_duration
                }

                if employment

                else None
            ),


            # =================================================
            # CURRENT APPLICATION
            # =================================================

            "application": {

                "application_id":
                    application.application_id,

                "application_date":
                    (
                        application.application_date.isoformat()
                        if application.application_date
                        else None
                    ),

                "loan_purpose":
                    application.loan_purpose,

                "loan_amount":
                    float(
                        application.loan_amount
                    ),

                "loan_tenure":
                    application.loan_tenure,

                "status":
                    application.status
            },


            # =================================================
            # CREDIT PROFILE
            # =================================================

            "credit_profile": (

                {

                    "profile_id":
                        credit_profile.profile_id,

                    "number_of_dependents":
                        credit_profile.number_of_dependents,

                    "debt_to_income_ratio":
                        (
                            float(
                                credit_profile.debt_to_income_ratio
                            )
                            if credit_profile.debt_to_income_ratio
                            is not None
                            else None
                        ),

                    "credit_utilization":
                        (
                            float(
                                credit_profile.credit_utilization
                            )
                            if credit_profile.credit_utilization
                            is not None
                            else None
                        ),

                    "previous_defaults":
                        credit_profile.previous_defaults,

                    "missed_payments":
                        credit_profile.missed_payments,

                    "maximum_days_past_due":
                        credit_profile.maximum_days_past_due,

                    "recent_credit_enquiries":
                        credit_profile.recent_credit_enquiries,

                    "number_of_credit_accounts":
                        credit_profile.number_of_credit_accounts,

                    "credit_history_length":
                        credit_profile.credit_history_length,

                    "payment_history":
                        (
                            float(
                                credit_profile.payment_history
                            )
                            if credit_profile.payment_history
                            is not None
                            else None
                        ),

                    "loan_to_income_ratio":
                        (
                            float(
                                credit_profile.loan_to_income_ratio
                            )
                            if credit_profile.loan_to_income_ratio
                            is not None
                            else None
                        )
                }

                if credit_profile

                else None
            ),


            # =================================================
            # CREDIT RATING
            # =================================================

            "credit_rating": (

                {

                    "rating_id":
                        credit_rating.rating_id,

                    "credit_score":
                        credit_rating.credit_score,

                    "risk_grade":
                        credit_rating.risk_grade,

                    "rating_date":
                        (
                            credit_rating.rating_date.isoformat()
                            if credit_rating.rating_date
                            else None
                        )
                }

                if credit_rating

                else None
            ),


            # =================================================
            # LOAN REQUEST
            # =================================================

            "loan_request": (

                {

                    "loan_request_id":
                        loan_request.loan_request_id,

                    "loan_amount":
                        float(
                            loan_request.loan_amount
                        ),

                    "loan_tenure":
                        loan_request.loan_tenure
                }

                if loan_request

                else None
            ),


            # =================================================
            # DEBT PAYMENT METRICS
            # =================================================

            "debt_payment_metrics": (

                {

                    "metrics_id":
                        debt_metrics.metrics_id,

                    "existing_loans_count":
                        debt_metrics.existing_loans_count,

                    "total_outstanding_debt":
                        (
                            float(
                                debt_metrics.total_outstanding_debt
                            )
                            if debt_metrics.total_outstanding_debt
                            is not None
                            else None
                        ),

                    "monthly_emi":
                        (
                            float(
                                debt_metrics.monthly_emi
                            )
                            if debt_metrics.monthly_emi
                            is not None
                            else None
                        )
                }

                if debt_metrics

                else None
            ),


            # =================================================
            # EXISTING LOANS
            # =================================================

            "existing_loans": [

                {

                    "existing_loan_id":
                        loan.existing_loan_id,

                    "loan_request_id":
                        loan.loan_request_id,

                    "loan_type":
                        loan.loan_type,

                    "loan_amount":
                        (
                            float(
                                loan.loan_amount
                            )
                            if loan.loan_amount is not None
                            else None
                        ),

                    "outstanding_amount":
                        (
                            float(
                                loan.outstanding_amount
                            )
                            if loan.outstanding_amount
                            is not None
                            else None
                        ),

                    "monthly_emi":
                        (
                            float(
                                loan.monthly_emi
                            )
                            if loan.monthly_emi is not None
                            else None
                        )
                }

                for loan in existing_loans
            ],


            # =================================================
            # ASSESSMENT
            # =================================================

            "assessment": (

                {

                    "assessment_id":
                        assessment.assessment_id,

                    "prediction":
                        assessment.prediction,

                    "approval_probability":
                        (
                            float(
                                assessment.approval_probability
                            )
                            if assessment.approval_probability
                            is not None
                            else None
                        ),

                    "risk_score":
                        (
                            float(
                                assessment.risk_score
                            )
                            if assessment.risk_score
                            is not None
                            else None
                        ),

                    "risk_level":
                        assessment.risk_level,

                    "decision":
                        assessment.decision,

                    "risk_factors":
                        (
                            assessment.risk_factors
                            if assessment.risk_factors
                            else []
                        )
                }

                if assessment

                else None
            )
        }