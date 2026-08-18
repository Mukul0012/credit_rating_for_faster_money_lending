from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class CreditProfile(Base):
    __tablename__ = "credit_profile"

    profile_id = Column(
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

    annual_income = Column(
        Numeric,
        nullable=True
    )

    employment_type = Column(
        String,
        nullable=True
    )

    employment_duration = Column(
        Integer,
        nullable=True
    )

    number_of_dependents = Column(
        Integer,
        nullable=True
    )

    debt_to_income_ratio = Column(
        Numeric,
        nullable=True
    )

    credit_utilization = Column(
        Numeric,
        nullable=True
    )

    previous_defaults = Column(
        Integer,
        nullable=True
    )

    missed_payments = Column(
        Integer,
        nullable=True
    )

    maximum_days_past_due = Column(
        Integer,
        nullable=True
    )

    recent_credit_enquiries = Column(
        Integer,
        nullable=True
    )

    number_of_credit_accounts = Column(
        Integer,
        nullable=True
    )

    credit_history_length = Column(
        Integer,
        nullable=True
    )

    payment_history = Column(
        Numeric,
        nullable=True
    )

    loan_to_income_ratio = Column(
        Numeric,
        nullable=True
    )

    application = relationship(
        "Application",
        back_populates="credit_profiles"
    )