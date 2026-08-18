from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.loan_request import LoanRequest
from app.models.credit_rating import CreditRating
from app.models.loan_assessment import LoanAssessment


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