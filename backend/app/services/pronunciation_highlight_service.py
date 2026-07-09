import re
from dataclasses import dataclass

from app.models.pronunciation_highlight import PronunciationHighlight
from app.models.transcription import Transcript, TranscriptSegment
from app.services.pronunciation_analysis_service import WORD_PATTERN

FAST_SEGMENT_RATE_WPM = 170.0
SLOW_SEGMENT_RATE_WPM = 90.0
LONG_PAUSE_BEFORE_SECONDS = 1.2
LONG_SEGMENT_SECONDS = 8.0
DENSE_SEGMENT_WORDS = 10
DENSE_SEGMENT_TECHNICAL_WORDS = 3
DENSE_SEGMENT_RATE_WPM = 140.0
LONG_SEGMENT_MIN_WORDS = 8
MAX_HIGHLIGHTS = 3

TECHNICAL_WORD_PATTERN = re.compile(
    r"\b(?:"
    r"algorithm|application|architecture|artificial|automation|backend|cloud|"
    r"database|deployment|deterministic|frontend|infrastructure|intelligence|"
    r"integration|javascript|kubernetes|language|machine|microservice|model|"
    r"neural|pipeline|production|python|software|technical|typescript|web"
    r")\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SegmentMetrics:
    duration_seconds: float
    word_count: int
    speaking_rate_wpm: float
    pause_before_seconds: float
    text_length: int
    technical_word_count: int


@dataclass(frozen=True)
class HighlightCandidate:
    priority: int
    highlight: PronunciationHighlight


class PronunciationHighlightService:
    def build_highlights(self, transcript: Transcript) -> list[PronunciationHighlight]:
        ordered_segments = sorted(
            transcript.segments, key=lambda segment: segment.start_seconds
        )
        candidates: list[HighlightCandidate] = []
        previous_segment: TranscriptSegment | None = None

        for segment in ordered_segments:
            metrics = self._compute_segment_metrics(segment, previous_segment)
            candidate = self._classify_segment(segment, metrics)

            if candidate:
                candidates.append(candidate)

            previous_segment = segment

        return [
            candidate.highlight
            for candidate in sorted(
                candidates,
                key=lambda item: (item.priority, item.highlight.start_seconds),
            )[:MAX_HIGHLIGHTS]
        ]

    def _compute_segment_metrics(
        self,
        segment: TranscriptSegment,
        previous_segment: TranscriptSegment | None,
    ) -> SegmentMetrics:
        duration_seconds = max(0.0, segment.end_seconds - segment.start_seconds)
        words = WORD_PATTERN.findall(segment.text)
        word_count = len(words)
        speaking_rate_wpm = (
            word_count / (duration_seconds / 60) if duration_seconds > 0 else 0.0
        )
        pause_before_seconds = (
            max(0.0, segment.start_seconds - previous_segment.end_seconds)
            if previous_segment
            else 0.0
        )
        technical_word_count = len(TECHNICAL_WORD_PATTERN.findall(segment.text))

        return SegmentMetrics(
            duration_seconds=duration_seconds,
            word_count=word_count,
            speaking_rate_wpm=speaking_rate_wpm,
            pause_before_seconds=pause_before_seconds,
            text_length=len(segment.text),
            technical_word_count=technical_word_count,
        )

    def _classify_segment(
        self,
        segment: TranscriptSegment,
        metrics: SegmentMetrics,
    ) -> HighlightCandidate | None:
        if metrics.pause_before_seconds > LONG_PAUSE_BEFORE_SECONDS:
            return HighlightCandidate(
                0,
                self._build_highlight(
                    segment,
                    "warning",
                    "This segment contains a long pause before it begins.",
                    "Use shorter pauses to keep the response flowing naturally.",
                ),
            )

        if (
            metrics.word_count >= 3
            and metrics.speaking_rate_wpm > FAST_SEGMENT_RATE_WPM
        ):
            return HighlightCandidate(
                1,
                self._build_highlight(
                    segment,
                    "warning",
                    "This segment is spoken faster than recommended.",
                    "Slow down slightly and articulate each word more clearly.",
                ),
            )

        if (
            metrics.word_count >= 3
            and metrics.speaking_rate_wpm < SLOW_SEGMENT_RATE_WPM
        ):
            return HighlightCandidate(
                2,
                self._build_highlight(
                    segment,
                    "warning",
                    "This segment is spoken slower than recommended.",
                    "Keep a steady pace while maintaining clear articulation.",
                ),
            )

        if self._is_dense_segment_spoken_quickly(metrics):
            return HighlightCandidate(
                3,
                self._build_highlight(
                    segment,
                    "info",
                    (
                        "This dense technical segment may be easier to understand if "
                        "spoken more slowly."
                    ),
                    "Pause briefly between technical terms.",
                ),
            )

        if self._is_long_segment_without_natural_pause(metrics):
            return HighlightCandidate(
                4,
                self._build_highlight(
                    segment,
                    "info",
                    "This long segment may benefit from clearer articulation.",
                    "Break long ideas into shorter phrases with natural pauses.",
                ),
            )

        return None

    def _is_dense_segment_spoken_quickly(self, metrics: SegmentMetrics) -> bool:
        return (
            metrics.word_count >= DENSE_SEGMENT_WORDS
            and metrics.technical_word_count >= DENSE_SEGMENT_TECHNICAL_WORDS
            and metrics.speaking_rate_wpm > DENSE_SEGMENT_RATE_WPM
        )

    def _is_long_segment_without_natural_pause(self, metrics: SegmentMetrics) -> bool:
        return (
            metrics.duration_seconds > LONG_SEGMENT_SECONDS
            and metrics.word_count >= LONG_SEGMENT_MIN_WORDS
        )

    def _build_highlight(
        self,
        segment: TranscriptSegment,
        severity: str,
        issue: str,
        recommendation: str,
    ) -> PronunciationHighlight:
        return PronunciationHighlight(
            start_seconds=round(segment.start_seconds, 2),
            end_seconds=round(segment.end_seconds, 2),
            text=segment.text,
            severity=severity,
            issue=issue,
            recommendation=recommendation,
        )
