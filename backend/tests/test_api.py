import wave
from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.api.routes.assessments import get_assessment_service
from app.core.config import settings
from app.main import app
from app.models.feedback import AssessmentFeedback
from app.models.transcription import Transcript, TranscriptSegment
from app.services.assessment_service import AssessmentService
from app.services.feedback_service import FeedbackGenerationError, FeedbackService
from app.services.transcription_service import TranscriptionError

client = TestClient(app)


@pytest.fixture(autouse=True)
def configure_uploads(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "upload_dir", tmp_path)
    monkeypatch.setattr(settings, "max_upload_size_mb", 25)
    app.dependency_overrides[get_assessment_service] = lambda: AssessmentService(
        transcription_service=SuccessfulTranscriptionService(),
        feedback_service=FeedbackService(provider=SuccessfulFeedbackProvider()),
    )
    yield
    app.dependency_overrides.clear()


class SuccessfulTranscriptionService:
    def transcribe(self, audio_path):
        return Transcript(
            text=(
                "This is a short English pronunciation sample with enough words "
                "for the deterministic analysis layer to evaluate speech rate."
            ),
            language="en",
            duration_seconds=34.6,
            segments=[
                TranscriptSegment(
                    start_seconds=0.0,
                    end_seconds=10.0,
                    text=(
                        "This is a short English pronunciation sample with enough words"
                    ),
                ),
                TranscriptSegment(
                    start_seconds=10.4,
                    end_seconds=20.0,
                    text=(
                        "for the deterministic analysis layer to evaluate speech rate."
                    ),
                ),
            ],
        )


class FailingTranscriptionService:
    def transcribe(self, audio_path):
        raise TranscriptionError("Transcription engine unavailable.")


class SuccessfulFeedbackProvider:
    def generate(self, prompt):
        return AssessmentFeedback(
            overall_summary="Your recording was processed with a cautious review.",
            strengths=["The transcript was long enough to inspect basic pacing."],
            improvement_suggestions=[
                "Speech rate appears slower than the recommended range."
            ],
            practice_recommendations=[
                "Practice reading a short paragraph at a steady pace."
            ],
        )


class FailingFeedbackProvider:
    def generate(self, prompt):
        raise FeedbackGenerationError("Provider unavailable.")


def make_wav_bytes(duration_seconds: float, sample_rate: int = 8_000) -> bytes:
    buffer = BytesIO()
    frame_count = int(duration_seconds * sample_rate)

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"\x00\x00" * frame_count)

    return buffer.getvalue()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "Livo Pronunciation Checker API",
        "status": "ok",
    }


def test_assessment_upload_accepts_valid_audio() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(34.6), "audio/wav")},
    )

    payload = response.json()

    assert response.status_code == 201
    assert (
        payload["message"]
        == "Audio uploaded, transcribed, analyzed, and reviewed successfully."
    )
    assert payload["status"] == "analyzed"
    assert payload["upload"]["filename"].endswith(".wav")
    assert payload["upload"]["duration_seconds"] == pytest.approx(34.6, abs=0.01)
    assert payload["upload"]["content_type"] == "audio/wav"
    assert payload["upload"]["size_bytes"] > 0
    assert payload["transcription"] == {
        "text": (
            "This is a short English pronunciation sample with enough words "
            "for the deterministic analysis layer to evaluate speech rate."
        ),
        "language": "en",
        "duration_seconds": 34.6,
        "segments": [
            {
                "start_seconds": 0.0,
                "end_seconds": 10.0,
                "text": (
                    "This is a short English pronunciation sample with enough words"
                ),
            },
            {
                "start_seconds": 10.4,
                "end_seconds": 20.0,
                "text": (
                    "for the deterministic analysis layer to evaluate speech rate."
                ),
            },
        ],
    }
    assert payload["analysis"]["score"] == 65
    assert payload["analysis"]["metrics"] == {
        "total_word_count": 19,
        "speaking_rate_wpm": pytest.approx(32.95, abs=0.01),
        "pause_count": 0,
        "average_segment_duration_seconds": 9.8,
    }
    assert payload["analysis"]["issues"] == [
        {
            "category": "speech_rate",
            "severity": "high",
            "message": "Speech rate is slower than recommended.",
        },
        {
            "category": "transcript_length",
            "severity": "medium",
            "message": "Transcript is very short for a pronunciation assessment.",
        },
    ]
    assert payload["feedback"] == {
        "overall_summary": "Your recording was processed with a cautious review.",
        "strengths": ["The transcript was long enough to inspect basic pacing."],
        "improvement_suggestions": [
            "Speech rate appears slower than the recommended range."
        ],
        "practice_recommendations": [
            "Practice reading a short paragraph at a steady pace."
        ],
    }
    assert not (settings.upload_dir / payload["upload"]["filename"]).exists()


def test_assessment_upload_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 415
    assert response.json()["detail"]["code"] == "unsupported_mime_type"


def test_assessment_upload_rejects_unsupported_file_extension() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.ogg", make_wav_bytes(34.6), "audio/wav")},
    )

    assert response.status_code == 415
    assert response.json()["detail"]["code"] == "unsupported_file_extension"


def test_assessment_upload_rejects_file_too_large(monkeypatch) -> None:
    monkeypatch.setattr(settings, "max_upload_size_mb", 0)

    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(34.6), "audio/wav")},
    )

    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "file_too_large"


def test_assessment_upload_rejects_audio_too_short() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(29.9), "audio/wav")},
    )

    payload = response.json()

    assert response.status_code == 422
    assert payload["detail"]["code"] == "audio_too_short"
    assert payload["detail"]["duration_seconds"] == pytest.approx(29.9, abs=0.01)


def test_assessment_upload_rejects_audio_too_long() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(45.1), "audio/wav")},
    )

    payload = response.json()

    assert response.status_code == 422
    assert payload["detail"]["code"] == "audio_too_long"
    assert payload["detail"]["duration_seconds"] == pytest.approx(45.1, abs=0.01)


def test_assessment_upload_handles_transcription_failure() -> None:
    app.dependency_overrides[get_assessment_service] = lambda: AssessmentService(
        transcription_service=FailingTranscriptionService()
    )

    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(34.6), "audio/wav")},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == {
        "code": "transcription_failed",
        "message": "Speech transcription failed.",
    }


def test_assessment_upload_returns_analysis_when_feedback_fails() -> None:
    app.dependency_overrides[get_assessment_service] = lambda: AssessmentService(
        transcription_service=SuccessfulTranscriptionService(),
        feedback_service=FeedbackService(provider=FailingFeedbackProvider()),
    )

    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", make_wav_bytes(34.6), "audio/wav")},
    )

    payload = response.json()

    assert response.status_code == 201
    assert payload["analysis"]["score"] == 65
    assert payload["feedback"] is None
