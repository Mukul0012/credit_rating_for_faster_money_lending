from datetime import date

from sqlalchemy.orm import Session

from app.repositories.applicant_repository import (
    ApplicantRepository
)


class ApplicantService:

    # =========================================================
    # CALCULATE AGE
    # =========================================================

    @staticmethod
    def calculate_age(
        date_of_birth: date
    ) -> int:

        today = date.today()

        age = (
            today.year
            - date_of_birth.year
            - (
                (today.month, today.day)
                <
                (
                    date_of_birth.month,
                    date_of_birth.day
                )
            )
        )

        return age


    # =========================================================
    # GET APPLICANT PROFILE
    # =========================================================

    @staticmethod
    def get_applicant_profile(
        db: Session,
        applicant_id: int
    ):

        # =====================================================
        # 1. APPLICANT
        # =====================================================

        applicant = (
            ApplicantRepository
            .get_applicant(
                db,
                applicant_id
            )
        )

        if not applicant:
            return None


        # =====================================================
        # 2. EMPLOYMENT
        # =====================================================

        employment = (
            ApplicantRepository
            .get_employment(
                db,
                applicant_id
            )
        )


        # =====================================================
        # 3. ALL APPLICATIONS
        # =====================================================

        applications = (
            ApplicantRepository
            .get_applications(
                db,
                applicant_id
            )
        )

        latest_application = (
            applications[0]
            if applications
            else None
        )


        # =====================================================
        # 4. FIND HISTORICAL CREDIT PROFILE
        #
        # IMPORTANT:
        #
        # Do NOT stop just because a credit_rating exists.
        #
        # Application 104 has a rating but no credit profile.
        #
        # Application 1 contains the actual historical
        # credit profile and debt metrics.
        # =====================================================

        historical_credit_profile = None
        historical_loan_request = None
        historical_debt_metrics = None
        historical_credit_rating = None

        for application in applications:

            profile = (
                ApplicantRepository
                .get_credit_profile(
                    db,
                    application.application_id
                )
            )

            request = (
                ApplicantRepository
                .get_loan_request(
                    db,
                    application.application_id
                )
            )

            metrics = None

            if request:

                metrics = (
                    ApplicantRepository
                    .get_debt_payment_metrics(
                        db,
                        request.loan_request_id
                    )
                )

            rating = (
                ApplicantRepository
                .get_credit_rating(
                    db,
                    application.application_id
                )
            )


            # -------------------------------------------------
            # We need the application that actually contains
            # the historical credit profile.
            #
            # Credit rating alone is NOT sufficient.
            # -------------------------------------------------

            if profile is not None:

                historical_credit_profile = profile

                historical_loan_request = request

                historical_debt_metrics = metrics

                historical_credit_rating = rating

                break


        # =====================================================
        # 5. FALLBACK FOR CREDIT RATING
        #
        # If the latest application has a rating, use the
        # latest rating because it is the most recent score.
        #
        # Otherwise use the historical rating.
        # =====================================================

        latest_credit_rating = None

        if latest_application:

            latest_credit_rating = (
                ApplicantRepository
                .get_credit_rating(
                    db,
                    latest_application.application_id
                )
            )


        credit_rating = (
            latest_credit_rating
            if latest_credit_rating is not None
            else historical_credit_rating
        )


        # =====================================================
        # 6. EXISTING LOANS
        # =====================================================

        existing_loans = (
            ApplicantRepository
            .get_existing_loans(
                db,
                applicant_id
            )
        )


        # =====================================================
        # 7. BUILD RESPONSE
        # =====================================================

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
                    applicant.date_of_birth,

                "age":
                    (
                        applicant.age
                        if applicant.age is not None
                        else ApplicantService.calculate_age(
                            applicant.date_of_birth
                        )
                    ),

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
                            if employment.annual_income is not None
                            else None
                        ),

                    "employment_duration":
                        employment.employment_duration
                }

                if employment

                else None
            ),


            # =================================================
            # LATEST APPLICATION
            #
            # Current/latest loan application.
            # =================================================

            "latest_application": (

                {

                    "application_id":
                        latest_application.application_id,

                    "application_date":
                        latest_application.application_date,

                    "loan_purpose":
                        latest_application.loan_purpose,

                    "loan_amount":
                        float(
                            latest_application.loan_amount
                        ),

                    "loan_tenure":
                        latest_application.loan_tenure,

                    "status":
                        latest_application.status
                }

                if latest_application

                else None
            ),


            # =================================================
            # HISTORICAL CREDIT PROFILE
            # =================================================

            "credit_profile": (

                {

                    "profile_id":
                        historical_credit_profile.profile_id,

                    "number_of_dependents":
                        historical_credit_profile.number_of_dependents,

                    "debt_to_income_ratio":
                        (
                            float(
                                historical_credit_profile
                                .debt_to_income_ratio
                            )
                            if historical_credit_profile
                            .debt_to_income_ratio is not None
                            else None
                        ),

                    "credit_utilization":
                        (
                            float(
                                historical_credit_profile
                                .credit_utilization
                            )
                            if historical_credit_profile
                            .credit_utilization is not None
                            else None
                        ),

                    "previous_defaults":
                        historical_credit_profile.previous_defaults,

                    "missed_payments":
                        historical_credit_profile.missed_payments,

                    "maximum_days_past_due":
                        historical_credit_profile.maximum_days_past_due,

                    "recent_credit_enquiries":
                        historical_credit_profile.recent_credit_enquiries,

                    "number_of_credit_accounts":
                        historical_credit_profile.number_of_credit_accounts,

                    "credit_history_length":
                        historical_credit_profile.credit_history_length,

                    "payment_history":
                        (
                            float(
                                historical_credit_profile
                                .payment_history
                            )
                            if historical_credit_profile
                            .payment_history is not None
                            else None
                        ),

                    "loan_to_income_ratio":
                        (
                            float(
                                historical_credit_profile
                                .loan_to_income_ratio
                            )
                            if historical_credit_profile
                            .loan_to_income_ratio is not None
                            else None
                        )
                }

                if historical_credit_profile

                else None
            ),


            # =================================================
            # CREDIT RATING
            #
            # Prefer latest rating.
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
                        credit_rating.rating_date
                }

                if credit_rating

                else None
            ),


            # =================================================
            # HISTORICAL LOAN REQUEST
            # =================================================

            "loan_request": (

                {

                    "loan_request_id":
                        historical_loan_request.loan_request_id,

                    "loan_amount":
                        float(
                            historical_loan_request.loan_amount
                        ),

                    "loan_tenure":
                        historical_loan_request.loan_tenure
                }

                if historical_loan_request

                else None
            ),


            # =================================================
            # HISTORICAL DEBT PAYMENT METRICS
            # =================================================

            "debt_payment_metrics": (

                {

                    "metrics_id":
                        historical_debt_metrics.metrics_id,

                    "existing_loans_count":
                        historical_debt_metrics.existing_loans_count,

                    "total_outstanding_debt":
                        (
                            float(
                                historical_debt_metrics
                                .total_outstanding_debt
                            )
                            if historical_debt_metrics
                            .total_outstanding_debt is not None
                            else None
                        ),

                    "monthly_emi":
                        (
                            float(
                                historical_debt_metrics
                                .monthly_emi
                            )
                            if historical_debt_metrics
                            .monthly_emi is not None
                            else None
                        )
                }

                if historical_debt_metrics

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
                            float(loan.loan_amount)
                            if loan.loan_amount is not None
                            else None
                        ),

                    "outstanding_amount":
                        (
                            float(
                                loan.outstanding_amount
                            )
                            if loan.outstanding_amount is not None
                            else None
                        ),

                    "monthly_emi":
                        (
                            float(loan.monthly_emi)
                            if loan.monthly_emi is not None
                            else None
                        )
                }

                for loan in existing_loans
            ]
        }