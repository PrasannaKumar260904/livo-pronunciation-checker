from pathlib import Path
from typing import Protocol

from app.core.config import settings
from app.models.transcription import Transcript, TranscriptSegment


class TranscriptionError(RuntimeError):
    pass


class TranscriptionProvider(Protocol):
    def transcribe(self, audio_path: Path) -> Transcript:
        pass


class FasterWhisperTranscriptionService:
    def __init__(
        self,
        model_size: str = settings.transcription_model_size,
        device: str = settings.transcription_device,
        compute_type: str = settings.transcription_compute_type,
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model = None

    def transcribe(self, audio_path: Path) -> Transcript:
        try:
            segments_iterable, metadata = self._get_model().transcribe(str(audio_path))
            segments = [
                TranscriptSegment(
                    start_seconds=round(float(segment.start), 2),
                    end_seconds=round(float(segment.end), 2),
                    text=segment.text.strip(),
                )
                for segment in segments_iterable
                if segment.text.strip()
            ]
        except TranscriptionError:
            raise
        except Exception as exc:
            raise TranscriptionError("Speech transcription failed.") from exc

        return Transcript(
            text=" ".join(segment.text for segment in segments).strip(),
            language=getattr(metadata, "language", None),
            duration_seconds=round(float(getattr(metadata, "duration", 0.0) or 0.0), 2),
            segments=segments,
        )

    def _get_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise TranscriptionError(
                    "Transcription dependency is not installed."
                ) from exc

            # faster-whisper uses CTranslate2/PyAV, which is a better fit here than
            # openai-whisper because it is faster on CPU and exposes segments cleanly.
            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )

        return self._model
