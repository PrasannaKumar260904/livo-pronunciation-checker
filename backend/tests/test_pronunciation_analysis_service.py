import pytest

from app.models.transcription import Transcript, TranscriptSegment
from app.services.pronunciation_analysis_service import PronunciationAnalysisService


def make_transcript(
    text: str,
    segments: list[TranscriptSegment],
    duration_seconds: float = 34.0,
) -> Transcript:
    return Transcript(
        text=text,
        language="en",
        duration_seconds=duration_seconds,
        segments=segments,
    )


def test_analysis_computes_metrics_for_clear_sample() -> None:
    transcript = make_transcript(
        text=" ".join(["word"] * 68),
        segments=[
            TranscriptSegment(start_seconds=0.0, end_seconds=10.0, text="word " * 20),
            TranscriptSegment(start_seconds=10.4, end_seconds=20.0, text="word " * 20),
            TranscriptSegment(start_seconds=20.3, end_seconds=34.0, text="word " * 28),
        ],
    )

    analysis = PronunciationAnalysisService().analyze(transcript, 34.0)

    assert analysis.score == 100
    assert analysis.metrics.total_word_count == 68
    assert analysis.metrics.speaking_rate_wpm == pytest.approx(120.0, abs=0.01)
    assert analysis.metrics.pause_count == 0
    assert analysis.metrics.average_segment_duration_seconds == pytest.approx(
        11.1,
        abs=0.01,
    )
    assert analysis.issues == []


def test_analysis_flags_fast_speech_rate() -> None:
    transcript = make_transcript(
        text=" ".join(["word"] * 130),
        segments=[
            TranscriptSegment(start_seconds=0.0, end_seconds=15.0, text="word " * 65),
            TranscriptSegment(start_seconds=15.2, end_seconds=30.0, text="word " * 65),
        ],
    )

    analysis = PronunciationAnalysisService().analyze(transcript, 30.0)

    assert analysis.score == 80
    assert analysis.metrics.speaking_rate_wpm == pytest.approx(260.0, abs=0.01)
    assert [issue.model_dump() for issue in analysis.issues] == [
        {
            "category": "speech_rate",
            "severity": "high",
            "message": "Speech rate is faster than recommended.",
        }
    ]


def test_analysis_flags_slow_speech_rate_and_short_transcript() -> None:
    transcript = make_transcript(
        text="one two three four five",
        segments=[
            TranscriptSegment(start_seconds=0.0, end_seconds=6.0, text="one two"),
            TranscriptSegment(
                start_seconds=6.2, end_seconds=15.0, text="three four five"
            ),
        ],
    )

    analysis = PronunciationAnalysisService().analyze(transcript, 30.0)

    assert analysis.score == 65
    assert analysis.metrics.total_word_count == 5
    assert analysis.metrics.speaking_rate_wpm == pytest.approx(10.0, abs=0.01)
    assert [issue.category for issue in analysis.issues] == [
        "speech_rate",
        "transcript_length",
    ]


def test_analysis_counts_pauses_from_segment_gaps() -> None:
    transcript = make_transcript(
        text=" ".join(["word"] * 60),
        segments=[
            TranscriptSegment(start_seconds=0.0, end_seconds=3.0, text="word"),
            TranscriptSegment(start_seconds=3.7, end_seconds=6.0, text="word"),
            TranscriptSegment(start_seconds=6.8, end_seconds=9.0, text="word"),
            TranscriptSegment(start_seconds=9.7, end_seconds=12.0, text="word"),
            TranscriptSegment(start_seconds=12.8, end_seconds=18.0, text="word"),
            TranscriptSegment(start_seconds=18.9, end_seconds=30.0, text="word"),
        ],
    )

    analysis = PronunciationAnalysisService().analyze(transcript, 30.0)

    assert analysis.metrics.pause_count == 5
    assert analysis.score == 90
    assert {
        "category": "fluency",
        "severity": "medium",
        "message": "Long pauses detected.",
    } in [issue.model_dump() for issue in analysis.issues]


def test_analysis_flags_short_segments_as_possible_unclear_audio() -> None:
    transcript = make_transcript(
        text=" ".join(["word"] * 50),
        segments=[
            TranscriptSegment(start_seconds=0.0, end_seconds=0.5, text="word"),
            TranscriptSegment(start_seconds=0.6, end_seconds=1.0, text="word"),
        ],
    )

    analysis = PronunciationAnalysisService().analyze(transcript, 30.0)

    assert analysis.metrics.average_segment_duration_seconds == pytest.approx(
        0.45,
        abs=0.01,
    )
    assert {
        "category": "clarity",
        "severity": "low",
        "message": "Some segments may be unclear.",
    } in [issue.model_dump() for issue in analysis.issues]
