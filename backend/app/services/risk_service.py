from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.applicant_service import (
    ApplicantService
)

from app.services.risk_explanation import (
    get_risk_factors
)

from app.repositories.applicant_repository import (
    ApplicantRepository
)

from app.repositories.loan_repository import (
    LoanRepository
)

from app.ml.feature_builder import (
    FeatureBuilder
)

from app.ml.predictor import (
    Predictor
)


class RiskService:

    # =========================================================
    # CALCULATE RISK & APPLY UNDERWRITING POLICY
    # =========================================================

    @staticmethod
    def calculate_risk(
        probability: float,
        features: dict
    ) -> dict:

        # Model class 1 = Approve
        # Model class 0 = Reject
        #
        # P(1) = approval probability
        # Base risk score from ML model
        raw_risk_score = (
            1.0 - probability
        ) * 100.0

        # Financial health metrics for underwriting policy validation
        lti = float(features.get("Loan_to_Income_Ratio", 0.0) or 0.0)
        dti = float(features.get("Debt_to_Income_Ratio", 0.0) or 0.0)
        credit_score = int(features.get("Credit_Score", 700) or 700)
        previous_defaults = int(features.get("Previous_Defaults", 0) or 0)
        missed_payments = int(features.get("Missed_Payments", 0) or 0)
        max_dpd = int(features.get("Maximum_Days_Past_Due", 0) or 0)

        # -----------------------------------------------------
        # 1. Critical High Risk / Reject (Auto-Reject):
        #    - Unrealistic loan amount: Loan > 2.5x annual income (LTI > 250%)
        #    - Severe debt burden: Total EMI > 70% of monthly income (DTI > 70%)
        #    - Previous loan defaults on record (> 0)
        #    - High payment delinquency (DPD > 60)
        #    - Severely low credit score (< 580)
        #    - Model risk score > 60 (approval probability < 40%)
        # -----------------------------------------------------
        if (
            raw_risk_score > 60.0
            or lti > 250.0
            or dti > 70.0
            or previous_defaults > 0
            or max_dpd > 60
            or credit_score < 580
        ):
            risk_level = "HIGH"
            decision = "REJECT"
            risk_score = max(raw_risk_score, 65.0)

        # -----------------------------------------------------
        # 2. Medium Risk / Manual Underwriter Review (Lender Queue):
        #    - Moderately high LTI (100% < LTI <= 250%)
        #    - Moderately high DTI (40% < DTI <= 70%)
        #    - Subprime credit score (580 <= credit_score < 700)
        #    - Multiple missed payments (> 1)
        #    - Model risk score between 30 and 60
        # -----------------------------------------------------
        elif (
            raw_risk_score > 30.0
            or lti > 100.0
            or dti > 40.0
            or credit_score < 700
            or missed_payments > 1
        ):
            risk_level = "MEDIUM"
            decision = "REVIEW"
            risk_score = max(raw_risk_score, 35.0)

        # -----------------------------------------------------
        # 3. Low Risk / Auto-Approve:
        #    - Clean credit history (score >= 700, 0 defaults, <= 1 missed payment)
        #    - Safe debt ratios (LTI <= 100%, DTI <= 40%)
        #    - High ML approval probability (risk score <= 30)
        # -----------------------------------------------------
        else:
            risk_level = "LOW"
            decision = "APPROVE"
            risk_score = raw_risk_score

        return {

            "decision":
                decision,

            "risk_level":
                risk_level,

            "risk_score":
                round(
                    risk_score,
                    2
                ),

            "approval_probability":
                round(
                    probability,
                    5
                ),

            "risk_factors":
                get_risk_factors(
                    features
                )
        }


    # =========================================================
    # COMPLETE LOAN ASSESSMENT
    # =========================================================

    @staticmethod
    def assess_loan(
        db: Session,
        applicant_id: int,
        loan_data
    ):

        try:

            # =================================================
            # 1. GET APPLICANT PROFILE
            # =================================================

            customer_data = (
                ApplicantService
                .get_applicant_profile(
                    db,
                    applicant_id
                )
            )

            if customer_data is None:

                return None


            # =================================================
            # 2. FIND HISTORICAL CREDIT DATA
            #
            # Do NOT use the latest application blindly.
            #
            # We need an older application containing:
            #
            # - credit_profile
            # - credit_rating
            # - loan_request
            # - debt_payment_metrics
            # =================================================

            credit_history = (
                ApplicantRepository
                .get_application_with_credit_history(
                    db,
                    applicant_id
                )
            )

            if credit_history is None:

                raise ValueError(
                    "No complete credit history found "
                    f"for applicant {applicant_id}"
                )

            historical_application = (
                credit_history["application"]
            )

            historical_credit_profile = (
                credit_history["credit_profile"]
            )

            historical_credit_rating = (
                credit_history["credit_rating"]
            )

            historical_loan_request = (
                credit_history["loan_request"]
            )

            historical_debt_metrics = (
                credit_history["debt_payment_metrics"]
            )


            # =================================================
            # 3. REPLACE CURRENT PROFILE WITH HISTORICAL DATA
            # =================================================

            customer_data["credit_profile"] = {

                "profile_id":
                    historical_credit_profile.profile_id,

                "application_id":
                    historical_credit_profile.application_id,

                "annual_income":
                    historical_credit_profile.annual_income,

                "employment_type":
                    historical_credit_profile.employment_type,

                "employment_duration":
                    historical_credit_profile.employment_duration,

                "number_of_dependents":
                    historical_credit_profile.number_of_dependents,

                "debt_to_income_ratio":
                    historical_credit_profile.debt_to_income_ratio,

                "credit_utilization":
                    historical_credit_profile.credit_utilization,

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
                    historical_credit_profile.payment_history,

                "loan_to_income_ratio":
                    historical_credit_profile.loan_to_income_ratio
            }


            # =================================================
            # 4. HISTORICAL CREDIT RATING
            # =================================================

            customer_data["credit_rating"] = {

                "rating_id":
                    historical_credit_rating.rating_id,

                "application_id":
                    historical_credit_rating.application_id,

                "credit_score":
                    historical_credit_rating.credit_score,

                "risk_grade":
                    historical_credit_rating.risk_grade,

                "rating_date":
                    historical_credit_rating.rating_date
            }


            # =================================================
            # 5. HISTORICAL LOAN REQUEST
            # =================================================

            customer_data["loan_request"] = {

                "loan_request_id":
                    historical_loan_request.loan_request_id,

                "application_id":
                    historical_loan_request.application_id,

                "loan_amount":
                    historical_loan_request.loan_amount,

                "loan_tenure":
                    historical_loan_request.loan_tenure
            }


            # =================================================
            # 6. HISTORICAL DEBT PAYMENT METRICS
            # =================================================

            customer_data["debt_payment_metrics"] = {

                "metrics_id":
                    historical_debt_metrics.metrics_id,

                "loan_request_id":
                    historical_debt_metrics.loan_request_id,

                "existing_loans_count":
                    historical_debt_metrics.existing_loans_count,

                "total_outstanding_debt":
                    historical_debt_metrics.total_outstanding_debt,

                "monthly_emi":
                    historical_debt_metrics.monthly_emi
            }


            # =================================================
            # 7. BUILD ML FEATURES
            #
            # Historical customer information
            # +
            # New loan request
            # =
            # 33 ML features
            # =================================================

            features = (
                FeatureBuilder
                .build_raw_features(
                    customer_data,
                    loan_data
                )
            )


            # =================================================
            # 8. RUN RANDOM FOREST
            # =================================================

            prediction_result = (
                Predictor.predict(
                    features
                )
            )

            prediction = (
                prediction_result["prediction"]
            )

            probabilities = (
                prediction_result["probabilities"]
            )


            # =================================================
            # 9. APPROVAL PROBABILITY
            #
            # 0 = Reject
            # 1 = Approve
            # =================================================

            approval_probability = (
                probabilities["1"]
            )


            # =================================================
            # 10. CALCULATE BUSINESS RISK
            # =================================================

            risk_assessment = (
                RiskService
                .calculate_risk(
                    approval_probability,
                    features
                )
            )


            # =================================================
            # 11. CREATE NEW APPLICATION
            #
            # This is the CURRENT loan application.
            # It must NOT become historical data for this
            # same assessment.
            # =================================================

            application = (
                LoanRepository
                .create_application(
                    db=db,

                    applicant_id=
                        applicant_id,

                    loan_amount=
                        loan_data.loan_amount,

                    loan_tenure=
                        loan_data.loan_tenure,

                    loan_purpose=
                        loan_data.loan_purpose
                )
            )

            application_id = (
                application.application_id
            )


            # =================================================
            # 12. SYNCHRONIZE APPLICATION STATUS
            #
            # The assessment decision is the ML/business decision:
            #
            # APPROVE -> application is APPROVED
            # REVIEW  -> application is UNDER_REVIEW
            # REJECT  -> application is REJECTED
            #
            # This keeps application.status aligned with the
            # assessment shown to the frontend.
            # =================================================

            decision = (
                risk_assessment["decision"]
            )

            if decision == "APPROVE":

                application.status = "Approved"
                application.rejection_reason = None

            elif decision == "REJECT":

                application.status = "Rejected"
                risk_factors = risk_assessment.get("risk_factors", [])
                if risk_factors:
                    application.rejection_reason = "; ".join(risk_factors)
                else:
                    application.rejection_reason = "Application exceeded maximum risk threshold based on financial profile."

            else:

                application.status = "Pending"
                application.rejection_reason = None


            # =================================================
            # 13. CREATE NEW LOAN REQUEST
            # =================================================

            loan_request = (
                LoanRepository
                .create_loan_request(
                    db=db,

                    application_id=
                        application_id,

                    loan_amount=
                        loan_data.loan_amount,

                    loan_tenure=
                        loan_data.loan_tenure
                )
            )


            # =================================================
            # 14. CREATE CREDIT RATING SNAPSHOT
            #
            # The ML model does NOT generate the credit score.
            #
            # We preserve the applicant's existing score and
            # risk grade for this application.
            # =================================================

            credit_rating = (
                LoanRepository
                .create_credit_rating(
                    db=db,

                    application_id=
                        application_id,

                    credit_score=
                        historical_credit_rating.credit_score,

                    risk_grade=
                        historical_credit_rating.risk_grade
                )
            )


            # =================================================
            # 14b. CREATE CREDIT PROFILE SNAPSHOT
            # =================================================

            lti_decimal = Decimal(
                str(
                    round(
                        features.get(
                            "Loan_to_Income_Ratio",
                            0.0
                        ) / 100.0,
                        4
                    )
                )
            )

            dti_decimal = Decimal(
                str(
                    round(
                        features.get(
                            "Debt_to_Income_Ratio",
                            0.0
                        ) / 100.0,
                        4
                    )
                )
            )

            util_decimal = Decimal(
                str(
                    round(
                        features.get(
                            "Credit_Utilization",
                            0.0
                        ) / 100.0,
                        4
                    )
                )
            )

            pay_hist_decimal = Decimal(
                str(
                    round(
                        features.get(
                            "Payment_History",
                            100.0
                        ) / 100.0,
                        4
                    )
                )
            )

            LoanRepository.create_credit_profile(
                db=db,
                application_id=application_id,
                annual_income=Decimal(
                    str(
                        features.get(
                            "Annual_Income",
                            0
                        )
                    )
                ),
                employment_type=features.get(
                    "Employment_Type"
                ),
                employment_duration=int(
                    features.get(
                        "Employment_Duration_Years",
                        0
                    )
                ),
                number_of_dependents=int(
                    features.get(
                        "Number_of_Dependents",
                        0
                    )
                ),
                debt_to_income_ratio=dti_decimal,
                credit_utilization=util_decimal,
                previous_defaults=int(
                    features.get(
                        "Previous_Defaults",
                        0
                    )
                ),
                missed_payments=int(
                    features.get(
                        "Missed_Payments",
                        0
                    )
                ),
                maximum_days_past_due=int(
                    features.get(
                        "Maximum_Days_Past_Due",
                        0
                    )
                ),
                recent_credit_enquiries=int(
                    features.get(
                        "Recent_Credit_Enquiries",
                        0
                    )
                ),
                number_of_credit_accounts=int(
                    features.get(
                        "Number_of_Credit_Accounts",
                        0
                    )
                ),
                credit_history_length=int(
                    features.get(
                        "Credit_History_Length",
                        0
                    )
                ),
                payment_history=pay_hist_decimal,
                loan_to_income_ratio=lti_decimal
            )


            # =================================================
            # 14c. CREATE DEBT PAYMENT METRICS SNAPSHOT
            # =================================================

            LoanRepository.create_debt_payment_metrics(
                db=db,
                loan_request_id=loan_request.loan_request_id,
                existing_loans_count=int(
                    features.get(
                        "Existing_Loans_Count",
                        0
                    )
                ),
                total_outstanding_debt=Decimal(
                    str(
                        round(
                            features.get(
                                "Total_Outstanding_Debt",
                                0.0
                            ),
                            2
                        )
                    )
                ),
                monthly_emi=Decimal(
                    str(
                        round(
                            features.get(
                                "Existing_Monthly_EMI",
                                0.0
                            ),
                            2
                        )
                    )
                )
            )


            # =================================================
            # 15. CREATE LOAN ASSESSMENT
            #
            # ML output belongs here:
            #
            # prediction
            # approval_probability
            # risk_score
            # risk_level
            # decision
            # risk_factors
            # =================================================

            loan_assessment = (
                LoanRepository
                .create_loan_assessment(

                    db=db,

                    application_id=
                        application_id,

                    prediction=
                        prediction,

                    approval_probability=
                        approval_probability,

                    risk_score=
                        risk_assessment[
                            "risk_score"
                        ],

                    risk_level=
                        risk_assessment[
                            "risk_level"
                        ],

                    decision=
                        risk_assessment[
                            "decision"
                        ],

                    risk_factors=
                        risk_assessment[
                            "risk_factors"
                        ]
                )
            )


            # =================================================
            # 16. COMMIT TRANSACTION
            # =================================================

            db.commit()


            # =================================================
            # 17. RETURN COMPLETE RESULT
            # =================================================

            return {

                "applicant_id":
                    applicant_id,

                "application_id":
                    application_id,

                "loan_request_id":
                    loan_request.loan_request_id,

                "assessment_id":
                    loan_assessment.assessment_id,

                "credit_rating": {

                    "credit_score":
                        credit_rating.credit_score,

                    "risk_grade":
                        credit_rating.risk_grade
                },

                "loan_request": {

                    "loan_amount":
                        float(
                            loan_data.loan_amount
                        ),

                    "loan_tenure":
                        loan_data.loan_tenure,

                    "loan_purpose":
                        loan_data.loan_purpose
                },

                "model": {

                    "prediction":
                        prediction,

                    "probabilities":
                        probabilities,

                    "feature_count":
                        prediction_result[
                            "feature_count"
                        ]
                },

                "risk_assessment":
                    risk_assessment
            }


        except Exception:

            # =================================================
            # ROLLBACK EVERYTHING
            # =================================================

            db.rollback()

            raise