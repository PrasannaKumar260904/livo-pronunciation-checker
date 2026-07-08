from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    start_seconds: float
    end_seconds: float
    text: str


class Transcript(BaseModel):
    text: str
    language: str | None = None
    duration_seconds: float
    segments: list[TranscriptSegment] = Field(default_factory=list)
