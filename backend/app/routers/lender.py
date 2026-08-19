from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_lender
from app.repositories.lender_repository import LenderRepository
from app.schemas.lender import (
    LenderDecisionRequest,
    LenderDecisionResponse,
    LenderLoginRequest,
    LenderRegisterRequest,
    LenderTokenResponse,
    PendingApplicationsResponse
)
from app.services.lender_service import LenderService


router = APIRouter(
    prefix="/api/lender",
    tags=["Lender"]
)


# =========================================================
# LENDER REGISTER
# =========================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register_lender(
    data: LenderRegisterRequest,
    db: Session = Depends(get_db)
):
    return LenderService.register_lender(
        db=db,
        data=data
    )


# =========================================================
# LENDER LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=LenderTokenResponse
)
def login_lender(
    data: LenderLoginRequest,
    db: Session = Depends(get_db)
):
    return LenderService.login_lender(
        db=db,
        data=data
    )


# =========================================================
# CURRENT LENDER PROFILE
# =========================================================

@router.get(
    "/me"
)
def get_lender_profile(
    lender_id: int = Depends(get_current_lender),
    db: Session = Depends(get_db)
):
    lender = LenderRepository.get_lender_by_id(db, lender_id)
    if not lender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lender not found"
        )
    return {
        "lender_id": lender.lender_id,
        "email": lender.email,
        "full_name": lender.full_name,
        "is_active": lender.is_active
    }


# =========================================================
# PENDING APPLICATIONS
# =========================================================

@router.get(
    "/pending-applications",
    response_model=PendingApplicationsResponse
)
def get_pending_applications(
    lender_id: int = Depends(get_current_lender),
    db: Session = Depends(get_db)
):
    return LenderService.get_pending_applications(db=db)


# =========================================================
# ALL APPLICATIONS
# =========================================================

@router.get(
    "/all-applications",
    response_model=PendingApplicationsResponse
)
def get_all_applications(
    lender_id: int = Depends(get_current_lender),
    db: Session = Depends(get_db)
):
    return LenderService.get_all_applications(db=db)


# =========================================================
# APPLICATION FOR REVIEW
# =========================================================

@router.get(
    "/application/{application_id}"
)
def get_application_for_review(
    application_id: int,
    lender_id: int = Depends(get_current_lender),
    db: Session = Depends(get_db)
):
    result = LenderService.get_application_for_review(
        db=db,
        application_id=application_id
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return result


# =========================================================
# LENDER DECISION (APPROVE / REJECT)
# =========================================================

@router.post(
    "/application/{application_id}/decide",
    response_model=LenderDecisionResponse
)
def decide_application(
    application_id: int,
    data: LenderDecisionRequest,
    lender_id: int = Depends(get_current_lender),
    db: Session = Depends(get_db)
):
    return LenderService.update_application_decision(
        db=db,
        application_id=application_id,
        decision=data.decision,
        rejection_reason=data.rejection_reason,
        lender_id=lender_id
    )
