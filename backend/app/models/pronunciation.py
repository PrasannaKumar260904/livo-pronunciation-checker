from pydantic import BaseModel, Field


class AnalysisMetrics(BaseModel):
    total_word_count: int
    speaking_rate_wpm: float
    pause_count: int
    average_segment_duration_seconds: float


class PronunciationIssue(BaseModel):
    category: str
    severity: str
    message: str


class PronunciationAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    metrics: AnalysisMetrics
    issues: list[PronunciationIssue] = Field(default_factory=list)
