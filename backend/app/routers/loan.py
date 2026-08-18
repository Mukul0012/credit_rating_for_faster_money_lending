from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_applicant

from app.schemas.loan import (
    LoanAssessmentRequest,
    LoanHistoryResponse,
    LoanApplicationDetailsResponse
)

from app.services.risk_service import (
    RiskService
)

from app.services.loan_service import (
    LoanService
)


router = APIRouter(
    prefix="/api/loan",
    tags=["Loan"]
)


# =========================================================
# CREATE LOAN ASSESSMENT
# =========================================================

@router.post(
    "/assess"
)
def assess_loan(

    loan_data: LoanAssessmentRequest,

    applicant_id: int = Depends(
        get_current_applicant
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        result = (
            RiskService
            .assess_loan(
                db=db,
                applicant_id=applicant_id,
                loan_data=loan_data
            )
        )

        # -------------------------------------------------
        # APPLICANT NOT FOUND
        # -------------------------------------------------

        if result is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant not found"
            )

        return result

    # -----------------------------------------------------
    # PRESERVE HTTP EXCEPTIONS
    # -----------------------------------------------------

    except HTTPException:

        raise

    # -----------------------------------------------------
    # BUSINESS / DATA ERRORS
    # -----------------------------------------------------

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # -----------------------------------------------------
    # UNEXPECTED ERRORS
    # -----------------------------------------------------

    except Exception as e:

        print(
            "Loan assessment error:",
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Loan assessment failed"
        )


# =========================================================
# LOAN HISTORY
# =========================================================

@router.get(
    "/history",
    response_model=LoanHistoryResponse
)
def get_loan_history(

    applicant_id: int = Depends(
        get_current_applicant
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        history = (
            LoanService
            .get_loan_history(
                db=db,
                applicant_id=applicant_id
            )
        )

        return {
            "applications": history
        }

    except Exception as e:

        print(
            "Loan history error:",
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch loan history"
        )


# =========================================================
# INDIVIDUAL APPLICATION DETAILS
# =========================================================

@router.get(
    "/application/{application_id}",
    response_model=LoanApplicationDetailsResponse
)
def get_application_details(

    application_id: int,

    applicant_id: int = Depends(
        get_current_applicant
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        result = (
            LoanService
            .get_full_application_details(
                db=db,
                applicant_id=applicant_id,
                application_id=application_id
            )
        )

        # -------------------------------------------------
        # APPLICATION NOT FOUND
        # -------------------------------------------------

        if result is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        return result

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Application details error:",
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch application details"
        )