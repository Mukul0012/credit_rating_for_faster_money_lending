from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class CreditRating(Base):

    __tablename__ = "credit_rating"

    rating_id = Column(
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

    credit_score = Column(
        Integer,
        nullable=True
    )

    risk_grade = Column(
        String,
        nullable=True
    )

    rating_date = Column(
        Date,
        nullable=False
    )

    application = relationship(
        "Application",
        back_populates="credit_ratings"
    )