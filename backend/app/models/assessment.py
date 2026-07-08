from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class AssessmentStatus(StrEnum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class AssessmentResponse(BaseModel):
    id: UUID
    status: AssessmentStatus

