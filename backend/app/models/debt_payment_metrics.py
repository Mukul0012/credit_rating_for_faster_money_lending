from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class DebtPaymentMetrics(Base):
    __tablename__ = "debt_payment_metrics"

    metrics_id = Column(
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

    existing_loans_count = Column(
        Integer,
        nullable=True
    )

    total_outstanding_debt = Column(
        Numeric,
        nullable=True
    )

    monthly_emi = Column(
        Numeric,
        nullable=True
    )

    loan_request = relationship(
        "LoanRequest",
        back_populates="debt_payment_metrics"
    )