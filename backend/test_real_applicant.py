from app.ml.feature_builder import (
    FeatureBuilder
)

from app.ml.predictor import (
    Predictor
)

from app.schemas.loan import (
    LoanAssessmentRequest
)


# =========================================================
# Data returned by GET /api/applicant/me
# =========================================================

customer_data = {

    "personal": {

        "applicant_id": 1,

        "full_name": "Applicant 1",

        "date_of_birth": "1985-03-15",

        "age": 41,

        "gender": "Male",

        "email":
            "applicant1@example.com",

        "phone_number":
            "9810000001",

        "address":
            "Address 1, Pune, Maharashtra"
    },

    "employment": {

        "employment_id": 1,

        "employment_type":
            "Salaried",

        "employer_name":
            "TCS",

        "annual_income":
            317500,

        "employment_duration":
            2
    },

    "credit_profile": {

        "profile_id": 1,

        "number_of_dependents":
            1,

        "debt_to_income_ratio":
            0.16,

        "credit_utilization":
            0.11,

        "previous_defaults":
            1,

        "missed_payments":
            1,

        "maximum_days_past_due":
            1,

        "recent_credit_enquiries":
            1,

        "number_of_credit_accounts":
            3,

        "credit_history_length":
            3,

        "payment_history":
            0.91,

        "loan_to_income_ratio":
            0.21
    },

    "credit_rating": {

        "rating_id":
            1,

        "credit_score":
            617,

        "risk_grade":
            "D",

        "rating_date":
            "2026-08-13"
    },

    "debt_payment_metrics": {

        "metrics_id":
            84,

        "existing_loans_count":
            1,

        "total_outstanding_debt":
            82000,

        "monthly_emi":
            7150
    }
}


# =========================================================
# NEW LOAN ENTERED BY USER
# =========================================================

loan_data = LoanAssessmentRequest(

    loan_amount=300000,

    loan_tenure=36,

    loan_purpose="Personal"
)


# =========================================================
# BUILD FEATURES
# =========================================================

features = (
    FeatureBuilder
    .build_raw_features(
        customer_data,
        loan_data
    )
)


print("\nRAW FEATURES")
print("=" * 60)

for key, value in features.items():

    print(
        f"{key:35} : {value}"
    )


# =========================================================
# RUN MODEL
# =========================================================

result = Predictor.predict(
    features
)


print("\nMODEL RESULT")
print("=" * 60)

print(result)