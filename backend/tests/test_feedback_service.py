import pytest

from app.models.feedback import AssessmentFeedback
from app.models.pronunciation import (
    AnalysisMetrics,
    PronunciationAnalysis,
    PronunciationIssue,
)
from app.models.transcription import Transcript, TranscriptSegment
from app.services.feedback_service import (
    FeedbackGenerationError,
    FeedbackService,
    OpenAIFeedbackProvider,
)


class CapturingFeedbackProvider:
    def __init__(self) -> None:
        self.prompt = ""

    def generate(self, prompt: str) -> AssessmentFeedback:
        self.prompt = prompt
        return AssessmentFeedback(
            overall_summary="The recording shows a generally understandable attempt.",
            strengths=["The speech sample contains enough content to review pacing."],
            improvement_suggestions=["The speech rate may need steadier pacing."],
            practice_recommendations=["Practice a similar passage with a timer."],
        )


def make_analysis() -> PronunciationAnalysis:
    return PronunciationAnalysis(
        score=82,
        metrics=AnalysisMetrics(
            total_word_count=64,
            speaking_rate_wpm=128.0,
            pause_count=1,
            average_segment_duration_seconds=8.5,
        ),
        issues=[
            PronunciationIssue(
                category="fluency",
                severity="medium",
                message="Long pauses detected.",
            )
        ],
    )


def make_transcript() -> Transcript:
    return Transcript(
        text="This is a concise test transcript for feedback generation.",
        language="en",
        duration_seconds=30.0,
        segments=[
            TranscriptSegment(
                start_seconds=0.0,
                end_seconds=3.0,
                text="This is a concise test transcript.",
            )
        ],
    )


def test_feedback_service_builds_guardrailed_prompt_and_returns_feedback() -> None:
    provider = CapturingFeedbackProvider()
    feedback = FeedbackService(provider=provider).generate_feedback(
        make_analysis(),
        make_transcript(),
    )

    assert feedback.overall_summary.startswith("The recording shows")
    assert "Never invent pronunciation errors." in provider.prompt
    assert "Use ONLY the supplied metrics and detected issues." in provider.prompt
    assert "Avoid absolute claims." in provider.prompt
    assert "Long pauses detected." in provider.prompt
    assert "pronunciation_score" in provider.prompt


def test_openai_provider_requires_api_key() -> None:
    provider = OpenAIFeedbackProvider(api_key=None)

    with pytest.raises(FeedbackGenerationError):
        provider.generate("Return feedback.")
