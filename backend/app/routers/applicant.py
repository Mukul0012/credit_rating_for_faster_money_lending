from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_applicant

from app.services.applicant_service import (
    ApplicantService
)


router = APIRouter(
    prefix="/api/applicant",
    tags=["Applicant"]
)


# =========================================================
# CURRENT LOGGED-IN APPLICANT
# =========================================================

@router.get("/me")
def get_my_profile(
    applicant_id: int = Depends(
        get_current_applicant
    ),
    db: Session = Depends(
        get_db
    )
):

    profile = (
        ApplicantService
        .get_applicant_profile(
            db,
            applicant_id
        )
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Applicant not found"
        )

    return profile


# =========================================================
# DEBUG / ADMIN ENDPOINT
# =========================================================

@router.get("/{applicant_id}")
def get_applicant(
    applicant_id: int,
    db: Session = Depends(
        get_db
    )
):

    profile = (
        ApplicantService
        .get_applicant_profile(
            db,
            applicant_id
        )
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Applicant not found"
        )

    return profile