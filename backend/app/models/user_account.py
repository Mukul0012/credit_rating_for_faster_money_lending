from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Text,
    func
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class UserAccount(Base):

    __tablename__ = "user_account"

    user_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    applicant_id = Column(
        BigInteger,
        ForeignKey(
            "applicant.applicant_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True,
        index=True
    )

    password_hash = Column(
        Text,
        nullable=False
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    applicant = relationship(
        "Applicant",
        back_populates="user_account"
    )