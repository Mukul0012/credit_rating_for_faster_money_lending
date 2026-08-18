from typing import Any

from pydantic import BaseModel


class RiskAssessmentResponse(BaseModel):

    applicant_id: int

    prediction: Any

    risk_score: float | None = None

    risk_grade: str | None = None

    features_used: dict[str, Any]