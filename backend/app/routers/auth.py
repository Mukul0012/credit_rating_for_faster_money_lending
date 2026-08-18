from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse
)

from app.services.auth_service import (
    AuthService
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register"
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    return (
        AuthService
        .register(
            db=db,
            applicant_id=data.applicant_id,
            password=data.password
        )
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    return (
        AuthService
        .login(
            db=db,
            email=data.email,
            password=data.password
        )
    )