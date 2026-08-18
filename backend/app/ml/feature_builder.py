from decimal import Decimal


class FeatureBuilder:

    # =========================================================
    # NUMERIC CONVERSION
    # =========================================================

    @staticmethod
    def _number(value, default=0):

        if value is None:
            return default

        if isinstance(value, Decimal):
            return float(value)

        return value

    # =========================================================
    # PERCENTAGE CONVERSION
    # =========================================================

    @staticmethod
    def _percentage(value):

        if value is None:
            return 0

        if isinstance(value, Decimal):
            value = float(value)

        value = float(value)

        # Database representation:
        # 0.16 -> 16.0
        # 0.11 -> 11.0
        # 0.91 -> 91.0

        if 0 <= value <= 1:
            return value * 100

        return value

    # =========================================================
    # BUILD FEATURES
    # =========================================================

    @staticmethod
    def build_raw_features(
        customer_data: dict,
        loan_data
    ) -> dict:

        if not customer_data:
            raise ValueError(
                "Applicant data is empty"
            )

        # =====================================================
        # EXTRACT SECTIONS
        # =====================================================

        personal = customer_data.get(
            "personal"
        )

        employment = customer_data.get(
            "employment"
        )

        credit_profile = customer_data.get(
            "credit_profile"
        )

        credit_rating = customer_data.get(
            "credit_rating"
        )

        debt_metrics = customer_data.get(
            "debt_payment_metrics"
        )

        # =====================================================
        # VALIDATE REQUIRED DATA
        # =====================================================

        missing_sections = []

        if personal is None:
            missing_sections.append(
                "personal"
            )

        if employment is None:
            missing_sections.append(
                "employment"
            )

        if credit_profile is None:
            missing_sections.append(
                "credit_profile"
            )

        if credit_rating is None:
            missing_sections.append(
                "credit_rating"
            )

        if debt_metrics is None:
            missing_sections.append(
                "debt_payment_metrics"
            )

        if missing_sections:

            raise ValueError(
                "Missing applicant database sections: "
                + ", ".join(
                    missing_sections
                )
            )

        # =====================================================
        # BUILD FLAT ML FEATURES
        # =====================================================

        features = {

            # -------------------------------------------------
            # PERSONAL
            # -------------------------------------------------

            "Age":
                FeatureBuilder._number(
                    personal.get(
                        "age"
                    )
                ),

            # -------------------------------------------------
            # EMPLOYMENT
            # -------------------------------------------------

            "Annual_Income":
                FeatureBuilder._number(
                    employment.get(
                        "annual_income"
                    )
                ),

            "Employment_Duration_Years":
                FeatureBuilder._number(
                    employment.get(
                        "employment_duration"
                    )
                ),

            "Employment_Type":
                employment.get(
                    "employment_type"
                ),

            # -------------------------------------------------
            # CREDIT PROFILE
            # -------------------------------------------------

            "Number_of_Dependents":
                FeatureBuilder._number(
                    credit_profile.get(
                        "number_of_dependents"
                    )
                ),

            "Debt_to_Income_Ratio":
                FeatureBuilder._percentage(
                    credit_profile.get(
                        "debt_to_income_ratio"
                    )
                ),

            "Loan_to_Income_Ratio":
                FeatureBuilder._percentage(
                    credit_profile.get(
                        "loan_to_income_ratio"
                    )
                ),

            "Credit_Utilization":
                FeatureBuilder._percentage(
                    credit_profile.get(
                        "credit_utilization"
                    )
                ),

            "Previous_Defaults":
                FeatureBuilder._number(
                    credit_profile.get(
                        "previous_defaults"
                    )
                ),

            "Missed_Payments":
                FeatureBuilder._number(
                    credit_profile.get(
                        "missed_payments"
                    )
                ),

            "Maximum_Days_Past_Due":
                FeatureBuilder._number(
                    credit_profile.get(
                        "maximum_days_past_due"
                    )
                ),

            "Recent_Credit_Enquiries":
                FeatureBuilder._number(
                    credit_profile.get(
                        "recent_credit_enquiries"
                    )
                ),

            "Credit_History_Length":
                FeatureBuilder._number(
                    credit_profile.get(
                        "credit_history_length"
                    )
                ),

            "Number_of_Credit_Accounts":
                FeatureBuilder._number(
                    credit_profile.get(
                        "number_of_credit_accounts"
                    )
                ),

            "Payment_History":
                FeatureBuilder._percentage(
                    credit_profile.get(
                        "payment_history"
                    )
                ),

            # -------------------------------------------------
            # CREDIT RATING
            # -------------------------------------------------

            "Credit_Score":
                FeatureBuilder._number(
                    credit_rating.get(
                        "credit_score"
                    )
                ),

            # -------------------------------------------------
            # EXISTING DEBT
            # -------------------------------------------------

            "Existing_Loans_Count":
                FeatureBuilder._number(
                    debt_metrics.get(
                        "existing_loans_count"
                    )
                ),

            "Total_Outstanding_Debt":
                FeatureBuilder._number(
                    debt_metrics.get(
                        "total_outstanding_debt"
                    )
                ),

            "Existing_Monthly_EMI":
                FeatureBuilder._number(
                    debt_metrics.get(
                        "monthly_emi"
                    )
                ),

            # -------------------------------------------------
            # NEW LOAN
            # -------------------------------------------------

            "Loan_Amount":
                FeatureBuilder._number(
                    loan_data.loan_amount
                ),

            "Loan_Tenure_Months":
                FeatureBuilder._number(
                    loan_data.loan_tenure
                ),

            "Loan_Purpose":
                loan_data.loan_purpose
        }

        # =====================================================
        # DEBUG
        # =====================================================

        print()
        print("=" * 60)
        print("FEATURE BUILDER OUTPUT")
        print("=" * 60)

        for key, value in features.items():

            print(
                f"{key:35}: {value}"
            )

        print("=" * 60)

        return features