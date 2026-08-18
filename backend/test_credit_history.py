from app.core.database import SessionLocal

from app.repositories.applicant_repository import (
    ApplicantRepository
)


db = SessionLocal()

try:

    result = (
        ApplicantRepository
        .get_application_with_credit_history(
            db,
            1
        )
    )

    print()
    print("=" * 60)
    print("CREDIT HISTORY TEST")
    print("=" * 60)

    if result is None:

        print(
            "No application with complete "
            "credit history found."
        )

    else:

        application = result["application"]

        credit_profile = result[
            "credit_profile"
        ]

        credit_rating = result[
            "credit_rating"
        ]

        loan_request = result[
            "loan_request"
        ]

        debt_metrics = result[
            "debt_payment_metrics"
        ]

        print(
            "Application ID:",
            application.application_id
        )

        print(
            "Credit Profile ID:",
            credit_profile.profile_id
        )

        print(
            "Credit Rating ID:",
            credit_rating.rating_id
        )

        print(
            "Loan Request ID:",
            (
                loan_request.loan_request_id
                if loan_request
                else None
            )
        )

        print(
            "Debt Metrics ID:",
            debt_metrics.metrics_id
        )

    print("=" * 60)

finally:

    db.close()