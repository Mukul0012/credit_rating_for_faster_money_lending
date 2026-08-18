from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Application(Base):
    __tablename__ = "application"

    application_id = Column(
        BigInteger,
        primary_key=True,
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

    application_date = Column(
        Date,
        nullable=False
    )

    loan_purpose = Column(
        String,
        nullable=True
    )

    loan_amount = Column(
        Numeric,
        nullable=False
    )

    loan_tenure = Column(
        Integer,
        nullable=True
    )

    status = Column(
        String,
        nullable=True
    )

    # Relationships

    applicant = relationship(
        "Applicant",
        back_populates="applications"
    )

    credit_profiles = relationship(
        "CreditProfile",
        back_populates="application"
    )

    credit_ratings = relationship(
        "CreditRating",
        back_populates="application"
    )

    loan_requests = relationship(
        "LoanRequest",
        back_populates="application"
    )

    loan_assessments = relationship(
        "LoanAssessment",
        back_populates="application"
    )   