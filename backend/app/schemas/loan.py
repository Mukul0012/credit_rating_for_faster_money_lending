from decimal import Decimal

from pydantic import BaseModel, Field


# =========================================================
# LOAN ASSESSMENT REQUEST
# =========================================================

class LoanAssessmentRequest(BaseModel):

    loan_amount: Decimal = Field(
        gt=0,
        description="New loan amount requested by the applicant"
    )

    loan_tenure: int = Field(
        gt=0,
        description="Loan tenure in months"
    )

    loan_purpose: str = Field(
        min_length=1,
        description="Purpose of the new loan"
    )


# =========================================================
# LOAN HISTORY
# =========================================================

class LoanHistoryItem(BaseModel):

    application_id: int
    application_date: str | None

    loan_amount: float
    loan_tenure: int | None
    loan_purpose: str | None
    status: str | None

    assessment_id: int | None
    prediction: int | None
    approval_probability: float | None
    risk_score: float | None
    risk_level: str | None
    decision: str | None

    risk_factors: list[str]


class LoanHistoryResponse(BaseModel):

    applications: list[LoanHistoryItem]


# =========================================================
# PERSONAL
# =========================================================

class PersonalResponse(BaseModel):

    applicant_id: int
    full_name: str
    date_of_birth: str | None
    age: int | None
    gender: str | None
    email: str | None
    phone_number: str | None
    address: str | None


# =========================================================
# EMPLOYMENT
# =========================================================

class EmploymentResponse(BaseModel):

    employment_id: int
    employment_type: str | None
    employer_name: str | None
    annual_income: float | None
    employment_duration: float | None


# =========================================================
# APPLICATION
# =========================================================

class ApplicationResponse(BaseModel):

    application_id: int
    application_date: str | None
    loan_purpose: str | None
    loan_amount: float
    loan_tenure: int | None
    status: str | None


# =========================================================
# CREDIT PROFILE
# =========================================================

class CreditProfileResponse(BaseModel):

    profile_id: int
    number_of_dependents: int | None

    debt_to_income_ratio: float | None
    credit_utilization: float | None

    previous_defaults: int | None
    missed_payments: int | None
    maximum_days_past_due: int | None

    recent_credit_enquiries: int | None
    number_of_credit_accounts: int | None
    credit_history_length: float | None

    payment_history: float | None
    loan_to_income_ratio: float | None


# =========================================================
# CREDIT RATING
# =========================================================

class CreditRatingResponse(BaseModel):

    rating_id: int
    credit_score: int | None
    risk_grade: str | None
    rating_date: str | None


# =========================================================
# LOAN REQUEST
# =========================================================

class LoanRequestResponse(BaseModel):

    loan_request_id: int
    loan_amount: float
    loan_tenure: int


# =========================================================
# DEBT PAYMENT METRICS
# =========================================================

class DebtPaymentMetricsResponse(BaseModel):

    metrics_id: int

    existing_loans_count: int | None
    total_outstanding_debt: float | None
    monthly_emi: float | None


# =========================================================
# EXISTING LOAN
# =========================================================

class ExistingLoanResponse(BaseModel):

    existing_loan_id: int
    loan_request_id: int | None

    loan_type: str | None

    loan_amount: float | None
    outstanding_amount: float | None
    monthly_emi: float | None


# =========================================================
# ASSESSMENT
# =========================================================

class AssessmentResponse(BaseModel):

    assessment_id: int

    prediction: int

    approval_probability: float
    risk_score: float

    risk_level: str
    decision: str

    risk_factors: list[str]


# =========================================================
# COMPLETE APPLICATION DETAILS
# =========================================================

class LoanApplicationDetailsResponse(BaseModel):

    personal: PersonalResponse

    employment: EmploymentResponse | None

    application: ApplicationResponse

    credit_profile: CreditProfileResponse | None

    credit_rating: CreditRatingResponse | None

    loan_request: LoanRequestResponse | None

    debt_payment_metrics: DebtPaymentMetricsResponse | None

    existing_loans: list[ExistingLoanResponse]

    assessment: AssessmentResponse | None