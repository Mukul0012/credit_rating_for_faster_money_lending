from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)

from app.repositories.auth_repository import (
    AuthRepository
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        applicant_id: int,
        password: str
    ):

        # ---------------------------------------------
        # 1. Check applicant exists
        # ---------------------------------------------

        applicant = (
            AuthRepository
            .get_applicant(
                db,
                applicant_id
            )
        )

        if not applicant:

            raise HTTPException(
                status_code=404,
                detail="Applicant not found"
            )

        # ---------------------------------------------
        # 2. Check whether account already exists
        # ---------------------------------------------

        existing_account = (
            AuthRepository
            .get_user_account(
                db,
                applicant_id
            )
        )

        if existing_account:

            raise HTTPException(
                status_code=409,
                detail="Account already exists"
            )

        # ---------------------------------------------
        # 3. Hash password
        # ---------------------------------------------

        password_hash = hash_password(
            password
        )

        # ---------------------------------------------
        # 4. Create account
        # ---------------------------------------------

        account = (
            AuthRepository
            .create_user_account(
                db,
                applicant_id,
                password_hash
            )
        )

        return {
            "message":
                "Account created successfully",

            "applicant_id":
                account.applicant_id
        }

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        # ---------------------------------------------
        # 1. Find applicant
        # ---------------------------------------------

        applicant = (
            AuthRepository
            .get_applicant_by_email(
                db,
                email
            )
        )

        if not applicant:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # ---------------------------------------------
        # 2. Find account
        # ---------------------------------------------

        account = (
            AuthRepository
            .get_user_account(
                db,
                applicant.applicant_id
            )
        )

        if not account:

            raise HTTPException(
                status_code=401,
                detail="Account not found"
            )

        # ---------------------------------------------
        # 3. Check account status
        # ---------------------------------------------

        if not account.is_active:

            raise HTTPException(
                status_code=403,
                detail="Account is inactive"
            )

        # ---------------------------------------------
        # 4. Verify password
        # ---------------------------------------------

        valid_password = (
            verify_password(
                password,
                account.password_hash
            )
        )

        if not valid_password:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # ---------------------------------------------
        # 5. Generate JWT
        # ---------------------------------------------

        token = (
            create_access_token(
                applicant.applicant_id
            )
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }