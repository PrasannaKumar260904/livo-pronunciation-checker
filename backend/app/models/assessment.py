from pydantic import BaseModel

from app.models.feedback import AssessmentFeedback
from app.models.pronunciation import PronunciationAnalysis
from app.models.transcription import Transcript


class UploadSummary(BaseModel):
    filename: str
    duration_seconds: float
    content_type: str
    size_bytes: int


class AssessmentResponse(BaseModel):
    message: str
    status: str
    upload: UploadSummary
    transcription: Transcript
    analysis: PronunciationAnalysis
    feedback: AssessmentFeedback | None = None
