from datetime import datetime, timezone
from enum import Enum



from pydantic import BaseModel, Field


class PreregistrationStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    LOCKED = "LOCKED"


class Prediction(BaseModel):
    metric: str
    baseline: str
    candidate: str
    predicted_difference: float
    direction: str
    acceptance_threshold: float


class ResearchQuestion(BaseModel):
    objective: str
    task_type: str
    dataset: str


class Evaluation(BaseModel):
    protocol: str
    primary_metric: str
    random_seed: int = 42


class Rationale(BaseModel):
    reason: str
    mechanism: str


class PreRegistration(BaseModel):
    preregistration_id: str
    research_question: ResearchQuestion
    hypothesis: str
    null_hypothesis: str
    prediction: Prediction
    evaluation: Evaluation
    rationale: Rationale
    falsifier: str
    status: PreregistrationStatus = PreregistrationStatus.DRAFT
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    content_hash: str | None = None