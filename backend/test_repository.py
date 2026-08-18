from app.core.database import SessionLocal
from app.repositories.applicant_repository import (
    ApplicantRepository
)


db = SessionLocal()

try:

    data = (
        ApplicantRepository
        .get_full_applicant_profile(
            db,
            1
        )
    )

    if data is None:

        print("Applicant not found")

    else:

        (
            applicant,
            employment,
            application,
            credit_profile,
            credit_rating,
            loan_request,
            debt_payment_metrics,
            existing_loans
        ) = data

        print()
        print("=" * 60)
        print("REPOSITORY TEST")
        print("=" * 60)

        print(
            "Applicant:",
            applicant.applicant_id
        )

        print(
            "Employment:",
            employment
        )

        print(
            "Application:",
            application
        )

        print(
            "Credit Profile:",
            credit_profile
        )

        print(
            "Credit Rating:",
            credit_rating
        )

        print(
            "Loan Request:",
            loan_request
        )

        print(
            "Debt Metrics:",
            debt_payment_metrics
        )

        print(
            "Existing Loans:",
            existing_loans
        )

        print("=" * 60)

finally:

    db.close()