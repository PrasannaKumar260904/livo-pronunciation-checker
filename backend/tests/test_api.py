from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "Livo Pronunciation Checker API",
        "status": "ok",
    }


def test_assessment_upload_returns_not_implemented() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.wav", b"RIFF", "audio/wav")},
    )

    assert response.status_code == 501
    assert response.json() == {
        "detail": "Pronunciation assessment is not implemented yet."
    }


def test_assessment_upload_rejects_unsupported_audio_type() -> None:
    response = client.post(
        "/api/v1/assessments",
        files={"audio": ("sample.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 415

