from typing import Optional

from sqlalchemy.orm import Session

from app.models.applicant import Applicant
from app.models.application import Application
from app.models.employment import Employment
from app.models.credit_profile import CreditProfile
from app.models.credit_rating import CreditRating
from app.models.loan_request import LoanRequest
from app.models.debt_payment_metrics import DebtPaymentMetrics
from app.models.existing_loan import ExistingLoan


class ApplicantRepository:

    # =========================================================
    # APPLICANT
    # =========================================================

    @staticmethod
    def get_applicant(
        db: Session,
        applicant_id: int
    ) -> Optional[Applicant]:

        return (
            db.query(Applicant)
            .filter(
                Applicant.applicant_id == applicant_id
            )
            .first()
        )

    # =========================================================
    # EMPLOYMENT
    # =========================================================

    @staticmethod
    def get_employment(
        db: Session,
        applicant_id: int
    ) -> Optional[Employment]:

        return (
            db.query(Employment)
            .filter(
                Employment.applicant_id == applicant_id
            )
            .order_by(
                Employment.employment_id.desc()
            )
            .first()
        )

    # =========================================================
    # ALL APPLICATIONS
    # =========================================================

    @staticmethod
    def get_applications(
        db: Session,
        applicant_id: int
    ) -> list[Application]:

        return (
            db.query(Application)
            .filter(
                Application.applicant_id == applicant_id
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .all()
        )

    # =========================================================
    # LATEST APPLICATION
    #
    # Used when we want to display the applicant's
    # most recent application.
    # =========================================================

    @staticmethod
    def get_latest_application(
        db: Session,
        applicant_id: int
    ) -> Optional[Application]:

        return (
            db.query(Application)
            .filter(
                Application.applicant_id == applicant_id
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .first()
        )

    # =========================================================
    # CREDIT PROFILE
    # =========================================================

    @staticmethod
    def get_credit_profile(
        db: Session,
        application_id: int
    ) -> Optional[CreditProfile]:

        return (
            db.query(CreditProfile)
            .filter(
                CreditProfile.application_id == application_id
            )
            .order_by(
                CreditProfile.profile_id.desc()
            )
            .first()
        )

    # =========================================================
    # CREDIT RATING
    # =========================================================

    @staticmethod
    def get_credit_rating(
        db: Session,
        application_id: int
    ) -> Optional[CreditRating]:

        return (
            db.query(CreditRating)
            .filter(
                CreditRating.application_id == application_id
            )
            .order_by(
                CreditRating.rating_date.desc(),
                CreditRating.rating_id.desc()
            )
            .first()
        )

    # =========================================================
    # LOAN REQUEST
    # =========================================================

    @staticmethod
    def get_loan_request(
        db: Session,
        application_id: int
    ) -> Optional[LoanRequest]:

        return (
            db.query(LoanRequest)
            .filter(
                LoanRequest.application_id == application_id
            )
            .order_by(
                LoanRequest.loan_request_id.desc()
            )
            .first()
        )

    # =========================================================
    # DEBT PAYMENT METRICS
    # =========================================================

    @staticmethod
    def get_debt_payment_metrics(
        db: Session,
        loan_request_id: int
    ) -> Optional[DebtPaymentMetrics]:

        return (
            db.query(DebtPaymentMetrics)
            .filter(
                DebtPaymentMetrics.loan_request_id
                == loan_request_id
            )
            .order_by(
                DebtPaymentMetrics.metrics_id.desc()
            )
            .first()
        )

    # =========================================================
    # EXISTING LOANS
    # =========================================================

    @staticmethod
    def get_existing_loans(
        db: Session,
        applicant_id: int
    ) -> list[ExistingLoan]:

        return (
            db.query(ExistingLoan)
            .filter(
                ExistingLoan.applicant_id == applicant_id
            )
            .order_by(
                ExistingLoan.existing_loan_id.desc()
            )
            .all()
        )

    # =========================================================
    # APPLICATION WITH COMPLETE CREDIT HISTORY
    #
    # IMPORTANT:
    #
    # The latest application may be a newly-created application
    # that does not yet have credit_profile / credit_rating /
    # debt_payment_metrics.
    #
    # Therefore, for ML assessment we search for an application
    # that actually has the required historical credit data.
    # =========================================================

    @staticmethod
    def get_application_with_credit_history(
        db: Session,
        applicant_id: int
    ):

        applications = (
            db.query(Application)
            .filter(
                Application.applicant_id == applicant_id
            )
            .order_by(
                Application.application_date.desc(),
                Application.application_id.desc()
            )
            .all()
        )

        for application in applications:

            application_id = (
                application.application_id
            )

            # -------------------------------------------------
            # Credit Profile
            # -------------------------------------------------

            credit_profile = (
                ApplicantRepository
                .get_credit_profile(
                    db,
                    application_id
                )
            )

            # -------------------------------------------------
            # Credit Rating
            # -------------------------------------------------

            credit_rating = (
                ApplicantRepository
                .get_credit_rating(
                    db,
                    application_id
                )
            )

            # -------------------------------------------------
            # Loan Request
            # -------------------------------------------------

            loan_request = (
                ApplicantRepository
                .get_loan_request(
                    db,
                    application_id
                )
            )

            # -------------------------------------------------
            # Debt Payment Metrics
            # -------------------------------------------------

            debt_payment_metrics = None

            if loan_request is not None:

                debt_payment_metrics = (
                    ApplicantRepository
                    .get_debt_payment_metrics(
                        db,
                        loan_request.loan_request_id
                    )
                )

            # -------------------------------------------------
            # We need all required historical data.
            # -------------------------------------------------

            if (
                credit_profile is not None
                and credit_rating is not None
                and debt_payment_metrics is not None
            ):

                return {
                    "application": application,

                    "credit_profile":
                        credit_profile,

                    "credit_rating":
                        credit_rating,

                    "loan_request":
                        loan_request,

                    "debt_payment_metrics":
                        debt_payment_metrics
                }

        # No application has complete credit history

        return None

    # =========================================================
    # FULL APPLICANT PROFILE
    #
    # Used by GET /api/applicant/me
    #
    # This returns the latest application for display.
    # It does NOT necessarily represent the application whose
    # credit history should be used for ML.
    # =========================================================

    @staticmethod
    def get_full_applicant_profile(
        db: Session,
        applicant_id: int
    ):

        # -----------------------------------------------------
        # Applicant
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
        # Employment
        # -----------------------------------------------------

        employment = (
            ApplicantRepository
            .get_employment(
                db,
                applicant_id
            )
        )

        # -----------------------------------------------------
        # Latest application
        # -----------------------------------------------------

        application = (
            ApplicantRepository
            .get_latest_application(
                db,
                applicant_id
            )
        )

        # -----------------------------------------------------
        # Related records
        # -----------------------------------------------------

        credit_profile = None
        credit_rating = None
        loan_request = None
        debt_payment_metrics = None

        if application is not None:

            application_id = (
                application.application_id
            )

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

            loan_request = (
                ApplicantRepository
                .get_loan_request(
                    db,
                    application_id
                )
            )

            if loan_request is not None:

                debt_payment_metrics = (
                    ApplicantRepository
                    .get_debt_payment_metrics(
                        db,
                        loan_request.loan_request_id
                    )
                )

        # -----------------------------------------------------
        # Existing loans
        # -----------------------------------------------------

        existing_loans = (
            ApplicantRepository
            .get_existing_loans(
                db,
                applicant_id
            )
        )

        # -----------------------------------------------------
        # Return
        # -----------------------------------------------------

        return (
            applicant,
            employment,
            application,
            credit_profile,
            credit_rating,
            loan_request,
            debt_payment_metrics,
            existing_loans
        )