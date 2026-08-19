from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.loan_request import LoanRequest
from app.models.credit_rating import CreditRating
from app.models.loan_assessment import LoanAssessment
from app.models.credit_profile import CreditProfile
from app.models.debt_payment_metrics import DebtPaymentMetrics


class LoanRepository:


    @staticmethod
    def get_application_history(
        db: Session,
        applicant_id: int
    ):
        """
        Get all loan applications and their assessments
        for a particular applicant.
        """

        return (
            db.query(
                Application,
                LoanAssessment
            )
            .outerjoin(
                LoanAssessment,
                LoanAssessment.application_id
                == Application.application_id
            )
            .filter(
                Application.applicant_id
                == applicant_id
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .all()
        )

    # =====================================================
    # CREATE APPLICATION
    # =====================================================

    @staticmethod
    def create_application(
        db: Session,
        applicant_id: int,
        loan_amount: Decimal,
        loan_tenure: int,
        loan_purpose: str
    ) -> Application:

        application = Application(

            applicant_id=applicant_id,

            application_date=date.today(),

            loan_purpose=loan_purpose,

            loan_amount=loan_amount,

            loan_tenure=loan_tenure,

            status="Pending"
        )

        db.add(application)

        # Forces INSERT so PostgreSQL generates
        # application_id immediately.
        db.flush()

        return application


    # =====================================================
    # CREATE LOAN REQUEST
    # =====================================================

    @staticmethod
    def create_loan_request(
        db: Session,
        application_id: int,
        loan_amount: Decimal,
        loan_tenure: int
    ) -> LoanRequest:

        loan_request = LoanRequest(

            application_id=application_id,

            loan_amount=loan_amount,

            loan_tenure=loan_tenure
        )

        db.add(loan_request)

        # PostgreSQL generates loan_request_id
        db.flush()

        return loan_request

    @staticmethod
    def create_credit_rating(
        db: Session,
        application_id: int,
        credit_score: int,
        risk_grade: str
    ) -> CreditRating:

        credit_rating = CreditRating(

            application_id=application_id,

            credit_score=credit_score,

            risk_grade=risk_grade,

            rating_date=date.today()
        )

        db.add(credit_rating)

        db.flush()

        return credit_rating

    @staticmethod
    def create_loan_assessment(
        db: Session,
        application_id: int,
        prediction: int,
        approval_probability: float,
        risk_score: float,
        risk_level: str,
        decision: str,
        risk_factors: list
    ) -> LoanAssessment:

        assessment = LoanAssessment(

            application_id=application_id,

            prediction=prediction,

            approval_probability=approval_probability,

            risk_score=risk_score,

            risk_level=risk_level,

            decision=decision,

            risk_factors=risk_factors,

            assessment_date=date.today()
        )

        db.add(assessment)

        db.flush()

        return assessment

    @staticmethod
    def create_credit_profile(
        db: Session,
        application_id: int,
        annual_income: Decimal | None = None,
        employment_type: str | None = None,
        employment_duration: int | None = None,
        number_of_dependents: int | None = None,
        debt_to_income_ratio: Decimal | None = None,
        credit_utilization: Decimal | None = None,
        previous_defaults: int | None = None,
        missed_payments: int | None = None,
        maximum_days_past_due: int | None = None,
        recent_credit_enquiries: int | None = None,
        number_of_credit_accounts: int | None = None,
        credit_history_length: int | None = None,
        payment_history: Decimal | None = None,
        loan_to_income_ratio: Decimal | None = None
    ) -> CreditProfile:

        profile = CreditProfile(
            application_id=application_id,
            annual_income=annual_income,
            employment_type=employment_type,
            employment_duration=employment_duration,
            number_of_dependents=number_of_dependents,
            debt_to_income_ratio=debt_to_income_ratio,
            credit_utilization=credit_utilization,
            previous_defaults=previous_defaults,
            missed_payments=missed_payments,
            maximum_days_past_due=maximum_days_past_due,
            recent_credit_enquiries=recent_credit_enquiries,
            number_of_credit_accounts=number_of_credit_accounts,
            credit_history_length=credit_history_length,
            payment_history=payment_history,
            loan_to_income_ratio=loan_to_income_ratio
        )

        db.add(profile)
        db.flush()

        return profile

    @staticmethod
    def create_debt_payment_metrics(
        db: Session,
        loan_request_id: int,
        existing_loans_count: int | None = None,
        total_outstanding_debt: Decimal | None = None,
        monthly_emi: Decimal | None = None
    ) -> DebtPaymentMetrics:

        metrics = DebtPaymentMetrics(
            loan_request_id=loan_request_id,
            existing_loans_count=existing_loans_count,
            total_outstanding_debt=total_outstanding_debt,
            monthly_emi=monthly_emi
        )

        db.add(metrics)
        db.flush()

        return metrics

    @staticmethod
    def get_application_details(
        db: Session,
        applicant_id: int,
        application_id: int
    ):
        """
        Get one application belonging to the specified applicant
        together with its assessment.
        """

        return (
            db.query(
                Application,
                LoanAssessment
            )
            .outerjoin(
                LoanAssessment,
                LoanAssessment.application_id
                == Application.application_id
            )
            .filter(
                Application.application_id
                == application_id,

                Application.applicant_id
                == applicant_id
            )
            .first()
        )