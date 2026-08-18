from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Numeric,
    String
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class ExistingLoan(Base):
    __tablename__ = "existing_loan"

    existing_loan_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    loan_request_id = Column(
        BigInteger,
        ForeignKey(
            "loan_request.loan_request_id"
        ),
        nullable=False,
        index=True
    )

    applicant_id = Column(
        BigInteger,
        ForeignKey(
            "applicant.applicant_id"
        ),
        nullable=False,
        index=True
    )

    loan_type = Column(
        String,
        nullable=True
    )

    loan_amount = Column(
        Numeric,
        nullable=True
    )

    outstanding_amount = Column(
        Numeric,
        nullable=True
    )

    monthly_emi = Column(
        Numeric,
        nullable=True
    )

    applicant = relationship(
        "Applicant",
        back_populates="existing_loans"
    )

    loan_request = relationship(
        "LoanRequest",
        back_populates="existing_loans"
    )