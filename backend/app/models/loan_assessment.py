from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    JSON
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class LoanAssessment(Base):

    __tablename__ = "loan_assessment"

    assessment_id = Column(
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

    prediction = Column(
        Integer,
        nullable=False
    )

    approval_probability = Column(
        Numeric(6, 5),
        nullable=False
    )

    risk_score = Column(
        Numeric(6, 2),
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False
    )

    decision = Column(
        String,
        nullable=False
    )

    risk_factors = Column(
        JSON,
        nullable=True
    )

    assessment_date = Column(
        Date,
        nullable=False
    )

    application = relationship(
        "Application",
        back_populates="loan_assessments"
    )