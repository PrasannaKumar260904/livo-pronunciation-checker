from pydantic import BaseModel, Field


class Feedback(BaseModel):
    overall_summary: str
    strengths: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    practice_recommendations: list[str] = Field(default_factory=list)


class AssessmentFeedback(Feedback):
    pass
