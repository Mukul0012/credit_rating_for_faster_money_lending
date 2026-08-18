from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError, jwt

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings


# =========================================================
# Password Hashing
# =========================================================

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str
) -> bool:

    try:

        return password_hasher.verify(
            password_hash,
            plain_password
        )

    except VerifyMismatchError:

        return False


# =========================================================
# JWT
# =========================================================

def create_access_token(
    applicant_id: int
) -> str:

    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(applicant_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


# =========================================================
# HTTP Bearer Authentication
# =========================================================

bearer_scheme = HTTPBearer()


def get_current_applicant(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
) -> int:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )

        applicant_id = payload.get("sub")

        if applicant_id is None:

            raise credentials_exception

        return int(applicant_id)

    except (
        JWTError,
        ValueError
    ):

        raise credentials_exception