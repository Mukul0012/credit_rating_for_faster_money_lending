from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# =========================================================
# LENDER AUTH SCHEMAS
# =========================================================

class LenderLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LenderRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2)


class LenderTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    lender_id: int
    full_name: str
    email: str


# =========================================================
# PENDING APPLICATIONS SCHEMAS
# =========================================================

class PendingApplicationItem(BaseModel):
    application_id: int
    applicant_id: int
    applicant_name: str
    applicant_email: Optional[str] = None
    application_date: Optional[str] = None
    loan_amount: float
    loan_tenure: Optional[int] = None
    loan_purpose: Optional[str] = None
    status: Optional[str] = None
    credit_score: Optional[int] = None
    risk_grade: Optional[str] = None
    risk_level: Optional[str] = None
    approval_probability: Optional[float] = None
    risk_score: Optional[float] = None
    rejection_reason: Optional[str] = None


class PendingApplicationsResponse(BaseModel):
    applications: list[PendingApplicationItem]
    total_pending: int
    approved_today: int
    rejected_today: int


# =========================================================
# LENDER DECISION SCHEMAS
# =========================================================

class LenderDecisionRequest(BaseModel):
    decision: str = Field(
        ...,
        description="'APPROVE', 'REJECT', or 'REVIEW'"
    )
    rejection_reason: Optional[str] = Field(
        None,
        description="Reason for rejection if application is rejected"
    )


class LenderDecisionResponse(BaseModel):
    message: str
    application_id: int
    status: str
    rejection_reason: Optional[str] = None
