from app.models.transcription import Transcript, TranscriptSegment
from app.services.pronunciation_highlight_service import PronunciationHighlightService


def make_transcript(segments: list[TranscriptSegment]) -> Transcript:
    return Transcript(
        text=" ".join(segment.text for segment in segments),
        language="en",
        duration_seconds=30.0,
        segments=segments,
    )


def test_highlights_return_empty_list_when_no_observations_exist() -> None:
    transcript = make_transcript(
        [
            TranscriptSegment(
                start_seconds=0.0,
                end_seconds=4.0,
                text="This segment has a steady natural speaking pace",
            ),
            TranscriptSegment(
                start_seconds=4.4,
                end_seconds=8.8,
                text="and continues with a balanced phrase length",
            ),
        ]
    )

    highlights = PronunciationHighlightService().build_highlights(transcript)

    assert highlights == []


def test_highlights_prioritize_high_value_observations_and_limit_to_three() -> None:
    transcript = make_transcript(
        [
            TranscriptSegment(
                start_seconds=0.0,
                end_seconds=1.0,
                text="one two three four five",
            ),
            TranscriptSegment(
                start_seconds=1.2,
                end_seconds=5.2,
                text="slow segment words",
            ),
            TranscriptSegment(
                start_seconds=7.0,
                end_seconds=10.5,
                text="pause before this segment is notable",
            ),
            TranscriptSegment(
                start_seconds=10.6,
                end_seconds=11.5,
                text="yes",
            ),
            TranscriptSegment(
                start_seconds=11.7,
                end_seconds=20.2,
                text=(
                    "this segment continues for a long duration today with enough "
                    "words to keep pacing steady"
                ),
            ),
            TranscriptSegment(
                start_seconds=20.4,
                end_seconds=23.4,
                text=(
                    "artificial intelligence backend architecture pipeline "
                    "deployment model integration"
                ),
            ),
        ]
    )

    highlights = PronunciationHighlightService().build_highlights(transcript)

    assert [highlight.issue for highlight in highlights] == [
        "This segment contains a long pause before it begins.",
        "This segment is spoken faster than recommended.",
        "This segment is spoken slower than recommended.",
    ]
    assert len(highlights) == 3
    assert [highlight.severity for highlight in highlights] == [
        "warning",
        "warning",
        "warning",
    ]


def test_highlights_do_not_flag_very_short_segments_by_themselves() -> None:
    transcript = make_transcript(
        [
            TranscriptSegment(
                start_seconds=0.0,
                end_seconds=0.8,
                text="yes",
            ),
            TranscriptSegment(
                start_seconds=1.0,
                end_seconds=1.7,
                text="okay",
            ),
        ]
    )

    highlights = PronunciationHighlightService().build_highlights(transcript)

    assert highlights == []


def test_highlights_detect_dense_technical_segment_spoken_quickly() -> None:
    transcript = make_transcript(
        [
            TranscriptSegment(
                start_seconds=0.0,
                end_seconds=4.0,
                text=(
                    "artificial intelligence backend architecture pipeline "
                    "deployment model integration improves production systems"
                ),
            )
        ]
    )

    highlights = PronunciationHighlightService().build_highlights(transcript)

    assert [highlight.model_dump() for highlight in highlights] == [
        {
            "start_seconds": 0.0,
            "end_seconds": 4.0,
            "text": (
                "artificial intelligence backend architecture pipeline "
                "deployment model integration improves production systems"
            ),
            "severity": "info",
            "issue": (
                "This dense technical segment may be easier to understand if "
                "spoken more slowly."
            ),
            "recommendation": "Pause briefly between technical terms.",
        }
    ]
