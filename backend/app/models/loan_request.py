from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class LoanRequest(Base):
    __tablename__ = "loan_request"

    loan_request_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    application_id = Column(
        BigInteger,
        ForeignKey(
            "application.application_id"
        ),
        nullable=False,
        index=True
    )

    loan_amount = Column(
        Numeric,
        nullable=False
    )

    loan_tenure = Column(
        Integer,
        nullable=False
    )

    application = relationship(
        "Application",
        back_populates="loan_requests"
    )

    debt_payment_metrics = relationship(
        "DebtPaymentMetrics",
        back_populates="loan_request"
    )

    existing_loans = relationship(
        "ExistingLoan",
        back_populates="loan_request"
    )