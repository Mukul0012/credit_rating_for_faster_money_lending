from typing import Optional

from sqlalchemy.orm import Session

from app.models.applicant import Applicant
from app.models.user_account import UserAccount


class AuthRepository:

    @staticmethod
    def get_applicant_by_email(
        db: Session,
        email: str
    ) -> Optional[Applicant]:

        return (
            db.query(Applicant)
            .filter(
                Applicant.email == email
            )
            .first()
        )

    @staticmethod
    def get_applicant(
        db: Session,
        applicant_id: int
    ) -> Optional[Applicant]:

        return (
            db.query(Applicant)
            .filter(
                Applicant.applicant_id
                == applicant_id
            )
            .first()
        )

    @staticmethod
    def get_user_account(
        db: Session,
        applicant_id: int
    ) -> Optional[UserAccount]:

        return (
            db.query(UserAccount)
            .filter(
                UserAccount.applicant_id
                == applicant_id
            )
            .first()
        )

    @staticmethod
    def create_user_account(
        db: Session,
        applicant_id: int,
        password_hash: str
    ) -> UserAccount:

        account = UserAccount(
            applicant_id=applicant_id,
            password_hash=password_hash
        )

        db.add(account)
        db.commit()
        db.refresh(account)

        return account