from pydantic import BaseModel


class PronunciationHighlight(BaseModel):
    start_seconds: float
    end_seconds: float
    text: str
    severity: str
    issue: str
    recommendation: str
