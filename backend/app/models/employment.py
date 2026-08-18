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


class Employment(Base):
    __tablename__ = "employment"

    employment_id = Column(
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

    employment_type = Column(
        String,
        nullable=True
    )

    employer_name = Column(
        String,
        nullable=True
    )

    annual_income = Column(
        Numeric,
        nullable=True
    )

    employment_duration = Column(
        Integer,
        nullable=True
    )

    applicant = relationship(
        "Applicant",
        back_populates="employments"
    )