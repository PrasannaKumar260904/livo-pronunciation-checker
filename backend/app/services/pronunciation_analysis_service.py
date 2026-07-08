import re

from app.models.pronunciation import (
    AnalysisMetrics,
    PronunciationAnalysis,
    PronunciationIssue,
)
from app.models.transcription import Transcript

FAST_SPEAKING_RATE_WPM = 180.0
VERY_FAST_SPEAKING_RATE_WPM = 210.0
SLOW_SPEAKING_RATE_WPM = 90.0
VERY_SLOW_SPEAKING_RATE_WPM = 70.0
EXCESSIVE_PAUSE_COUNT = 3
VERY_SHORT_TRANSCRIPT_WORDS = 20
SHORT_SEGMENT_DURATION_SECONDS = 1.0
PAUSE_GAP_SECONDS = 0.6
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


class PronunciationAnalysisService:
    def analyze(
        self,
        transcript: Transcript,
        audio_duration_seconds: float,
    ) -> PronunciationAnalysis:
        metrics = self._compute_metrics(transcript, audio_duration_seconds)
        issues = self._build_issues(metrics, transcript)
        score = self._compute_score(metrics)

        return PronunciationAnalysis(
            score=score,
            metrics=metrics,
            issues=issues,
        )

    def _compute_metrics(
        self,
        transcript: Transcript,
        audio_duration_seconds: float,
    ) -> AnalysisMetrics:
        word_count = len(WORD_PATTERN.findall(transcript.text))
        speaking_rate = self._compute_speaking_rate(word_count, audio_duration_seconds)
        pause_count = self._count_pauses(transcript)
        average_segment_duration = self._compute_average_segment_duration(transcript)

        return AnalysisMetrics(
            total_word_count=word_count,
            speaking_rate_wpm=round(speaking_rate, 2),
            pause_count=pause_count,
            average_segment_duration_seconds=round(average_segment_duration, 2),
        )

    def _compute_score(self, metrics: AnalysisMetrics) -> int:
        # Deterministic heuristic:
        # start at 100, deduct for rate outside a clear-conversational band,
        # excessive pauses, very short transcripts, and unusually short segments.
        score = 100

        if metrics.speaking_rate_wpm > VERY_FAST_SPEAKING_RATE_WPM:
            score -= 20
        elif metrics.speaking_rate_wpm > FAST_SPEAKING_RATE_WPM:
            score -= 10

        if metrics.speaking_rate_wpm < VERY_SLOW_SPEAKING_RATE_WPM:
            score -= 20
        elif metrics.speaking_rate_wpm < SLOW_SPEAKING_RATE_WPM:
            score -= 10

        if metrics.pause_count > EXCESSIVE_PAUSE_COUNT:
            score -= min(25, (metrics.pause_count - EXCESSIVE_PAUSE_COUNT) * 5)

        if metrics.total_word_count < VERY_SHORT_TRANSCRIPT_WORDS:
            score -= 15

        if (
            metrics.average_segment_duration_seconds > 0
            and metrics.average_segment_duration_seconds
            < SHORT_SEGMENT_DURATION_SECONDS
        ):
            score -= 10

        return max(0, min(100, score))

    def _build_issues(
        self,
        metrics: AnalysisMetrics,
        transcript: Transcript,
    ) -> list[PronunciationIssue]:
        issues: list[PronunciationIssue] = []

        if metrics.speaking_rate_wpm > FAST_SPEAKING_RATE_WPM:
            issues.append(
                PronunciationIssue(
                    category="speech_rate",
                    severity=(
                        "high"
                        if metrics.speaking_rate_wpm > VERY_FAST_SPEAKING_RATE_WPM
                        else "medium"
                    ),
                    message="Speech rate is faster than recommended.",
                )
            )

        if metrics.speaking_rate_wpm < SLOW_SPEAKING_RATE_WPM:
            issues.append(
                PronunciationIssue(
                    category="speech_rate",
                    severity=(
                        "high"
                        if metrics.speaking_rate_wpm < VERY_SLOW_SPEAKING_RATE_WPM
                        else "medium"
                    ),
                    message="Speech rate is slower than recommended.",
                )
            )

        if metrics.pause_count > EXCESSIVE_PAUSE_COUNT:
            issues.append(
                PronunciationIssue(
                    category="fluency",
                    severity="medium",
                    message="Long pauses detected.",
                )
            )

        if metrics.total_word_count < VERY_SHORT_TRANSCRIPT_WORDS:
            issues.append(
                PronunciationIssue(
                    category="transcript_length",
                    severity="medium",
                    message="Transcript is very short for a pronunciation assessment.",
                )
            )

        if self._has_short_segments(metrics, transcript):
            issues.append(
                PronunciationIssue(
                    category="clarity",
                    severity="low",
                    message="Some segments may be unclear.",
                )
            )

        return issues

    def _compute_speaking_rate(
        self,
        word_count: int,
        audio_duration_seconds: float,
    ) -> float:
        if audio_duration_seconds <= 0:
            return 0.0

        return word_count / (audio_duration_seconds / 60)

    def _count_pauses(self, transcript: Transcript) -> int:
        ordered_segments = sorted(
            transcript.segments, key=lambda segment: segment.start_seconds
        )
        pause_count = 0

        for previous_segment, current_segment in zip(
            ordered_segments,
            ordered_segments[1:],
            strict=False,
        ):
            gap_seconds = current_segment.start_seconds - previous_segment.end_seconds
            if gap_seconds > PAUSE_GAP_SECONDS:
                pause_count += 1

        return pause_count

    def _compute_average_segment_duration(self, transcript: Transcript) -> float:
        durations = [
            max(0.0, segment.end_seconds - segment.start_seconds)
            for segment in transcript.segments
        ]

        if not durations:
            return 0.0

        return sum(durations) / len(durations)

    def _has_short_segments(
        self,
        metrics: AnalysisMetrics,
        transcript: Transcript,
    ) -> bool:
        return bool(transcript.segments) and (
            metrics.average_segment_duration_seconds < SHORT_SEGMENT_DURATION_SECONDS
        )
