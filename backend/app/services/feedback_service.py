import json
from typing import Any, Protocol

import requests

from app.core.config import settings
from app.models.feedback import AssessmentFeedback
from app.models.pronunciation import PronunciationAnalysis
from app.models.transcription import Transcript

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_REQUEST_TIMEOUT_SECONDS = 30


class FeedbackGenerationError(RuntimeError):
    pass


class FeedbackProvider(Protocol):
    def generate(self, prompt: str) -> AssessmentFeedback:
        pass


class OpenAIFeedbackProvider:
    def __init__(
        self,
        api_key: str | None = settings.openai_api_key,
        model: str = settings.openai_model,
        timeout_seconds: int = OPENAI_REQUEST_TIMEOUT_SECONDS,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str) -> AssessmentFeedback:
        if not self.api_key:
            raise FeedbackGenerationError("OpenAI API key is not configured.")

        try:
            response = requests.post(
                OPENAI_CHAT_COMPLETIONS_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You generate concise English pronunciation "
                                "assessment feedback from supplied metrics only."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
            content = payload["choices"][0]["message"]["content"]
        except Exception as exc:
            raise FeedbackGenerationError("OpenAI feedback request failed.") from exc

        return self._parse_feedback(content)

    def _parse_feedback(self, content: str) -> AssessmentFeedback:
        try:
            parsed = json.loads(content)
            return AssessmentFeedback.model_validate(parsed)
        except Exception as exc:
            raise FeedbackGenerationError(
                "OpenAI feedback response was invalid."
            ) from exc


class FeedbackService:
    def __init__(self, provider: FeedbackProvider | None = None) -> None:
        self.provider = provider or OpenAIFeedbackProvider()

    def generate_feedback(
        self,
        analysis: PronunciationAnalysis,
        transcript: Transcript,
    ) -> AssessmentFeedback:
        prompt = self._build_prompt(analysis, transcript)
        return self.provider.generate(prompt)

    def _build_prompt(
        self,
        analysis: PronunciationAnalysis,
        transcript: Transcript,
    ) -> str:
        payload: dict[str, Any] = {
            "pronunciation_score": analysis.score,
            "metrics": analysis.metrics.model_dump(),
            "detected_issues": [issue.model_dump() for issue in analysis.issues],
            "transcript": {
                "text": transcript.text,
                "language": transcript.language,
                "duration_seconds": transcript.duration_seconds,
                "segments": [segment.model_dump() for segment in transcript.segments],
            },
            "required_json_shape": {
                "overall_summary": "string",
                "strengths": ["string"],
                "improvement_suggestions": ["string"],
                "practice_recommendations": ["string"],
            },
        }

        return (
            "Generate constructive learner feedback for an English pronunciation "
            "assessment.\n\n"
            "Rules:\n"
            "- Never invent pronunciation errors.\n"
            "- Use ONLY the supplied metrics and detected issues.\n"
            "- Generate constructive learner feedback.\n"
            "- Keep responses concise.\n"
            "- Avoid absolute claims.\n"
            "- Do not claim any specific word is mispronounced.\n"
            "- Do not add phoneme analysis or LLM-internal reasoning.\n"
            "- Return valid JSON only using the required JSON shape.\n\n"
            f"Assessment data:\n{json.dumps(payload, ensure_ascii=True)}"
        )
