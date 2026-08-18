from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.applicant import Applicant


router = APIRouter(
    prefix="/api/debug",
    tags=["Debug"]
)


@router.get("/applicant/{applicant_id}/graph")
def get_applicant_graph(
    applicant_id: int,
    db: Session = Depends(get_db)
):

    applicant = (
        db.query(Applicant)
        .filter(
            Applicant.applicant_id == applicant_id
        )
        .first()
    )

    if not applicant:
        return {
            "found": False,
            "message": "Applicant not found"
        }

    return {
        "applicant": {
            "id": applicant.applicant_id,
            "name": applicant.full_name,
        },

        "applications": [
            {
                "application_id":
                    application.application_id,

                "application_date":
                    str(application.application_date),

                "loan_purpose":
                    application.loan_purpose,

                "loan_amount":
                    float(application.loan_amount),

                "loan_tenure":
                    application.loan_tenure,

                "status":
                    application.status,

                "credit_profiles": [
                    {
                        "profile_id":
                            profile.profile_id,

                        "annual_income":
                            float(profile.annual_income)
                            if profile.annual_income is not None
                            else None,

                        "number_of_dependents":
                            profile.number_of_dependents,

                        "credit_utilization":
                            float(profile.credit_utilization)
                            if profile.credit_utilization is not None
                            else None
                    }
                    for profile in application.credit_profiles
                ],

                "credit_ratings": [
                    {
                        "rating_id":
                            rating.rating_id,

                        "credit_score":
                            rating.credit_score,

                        "risk_grade":
                            rating.risk_grade
                    }
                    for rating in application.credit_ratings
                ],

                "loan_requests": [
                    {
                        "loan_request_id":
                            request.loan_request_id,

                        "loan_amount":
                            float(request.loan_amount),

                        "loan_tenure":
                            request.loan_tenure,

                        "debt_metrics": [
                            {
                                "metrics_id":
                                    metrics.metrics_id,

                                "existing_loans_count":
                                    metrics.existing_loans_count,

                                "total_outstanding_debt":
                                    float(
                                        metrics.total_outstanding_debt
                                    )
                                    if metrics.total_outstanding_debt is not None
                                    else None,

                                "monthly_emi":
                                    float(metrics.monthly_emi)
                                    if metrics.monthly_emi is not None
                                    else None
                            }
                            for metrics in request.debt_payment_metrics
                        ],

                        "existing_loans": [
                            {
                                "existing_loan_id":
                                    existing_loan.existing_loan_id,

                                "loan_type":
                                    existing_loan.loan_type,

                                "loan_amount":
                                    float(existing_loan.loan_amount)
                                    if existing_loan.loan_amount is not None
                                    else None,

                                "outstanding_amount":
                                    float(existing_loan.outstanding_amount)
                                    if existing_loan.outstanding_amount is not None
                                    else None,

                                "monthly_emi":
                                    float(existing_loan.monthly_emi)
                                    if existing_loan.monthly_emi is not None
                                    else None
                            }
                            for existing_loan in request.existing_loans
                        ]
                    }
                    for request in application.loan_requests
                ]
            }
            for application in applicant.applications
        ],

        "employment": [
            {
                "employment_id":
                    employment.employment_id,

                "employment_type":
                    employment.employment_type,

                "employer_name":
                    employment.employer_name,

                "annual_income":
                    float(employment.annual_income)
                    if employment.annual_income is not None
                    else None,

                "employment_duration":
                    employment.employment_duration
            }
            for employment in applicant.employments
        ],

        "existing_loans_direct": [
            {
                "existing_loan_id":
                    loan.existing_loan_id,

                "loan_request_id":
                    loan.loan_request_id,

                "loan_type":
                    loan.loan_type,

                "outstanding_amount":
                    float(loan.outstanding_amount)
                    if loan.outstanding_amount is not None
                    else None,

                "monthly_emi":
                    float(loan.monthly_emi)
                    if loan.monthly_emi is not None
                    else None
            }
            for loan in applicant.existing_loans
        ]
    }