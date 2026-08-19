from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    String,
    Text,
    func
)

from app.core.database import Base


class LenderAccount(Base):
    __tablename__ = "lender_account"

    lender_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        Text,
        nullable=False
    )

    full_name = Column(
        String,
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
