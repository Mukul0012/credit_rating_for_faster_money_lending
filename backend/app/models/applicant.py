from sqlalchemy import BigInteger, Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Applicant(Base):
    __tablename__ = "applicant"

    applicant_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=True
    )

    gender = Column(
        String,
        nullable=True
    )

    pan = Column(
        String,
        nullable=False
    )

    aadhaar_number = Column(
        String,
        nullable=False
    )

    address = Column(
        Text,
        nullable=True
    )

    phone_number = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True,
        index=True
    )

    # Relationships

    applications = relationship(
        "Application",
        back_populates="applicant"
    )

    employments = relationship(
        "Employment",
        back_populates="applicant"
    )

    existing_loans = relationship(
        "ExistingLoan",
        back_populates="applicant"
    )

    user_account = relationship(
        "UserAccount",
        back_populates="applicant",
        uselist=False
    )