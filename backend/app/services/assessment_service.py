from fastapi import UploadFile, status

from app.core.config import Settings, settings
from app.models.assessment import AssessmentResponse
from app.services.audio_duration import AudioDurationError, AudioDurationService
from app.services.audio_validation import AudioValidationService
from app.services.pronunciation_analysis_service import PronunciationAnalysisService
from app.services.transcription_service import (
    FasterWhisperTranscriptionService,
    TranscriptionError,
    TranscriptionProvider,
)
from app.services.upload_service import UploadService
from app.utils.errors import raise_api_error


class AssessmentService:
    def __init__(
        self,
        config: Settings = settings,
        upload_service: UploadService | None = None,
        duration_service: AudioDurationService | None = None,
        validation_service: AudioValidationService | None = None,
        transcription_service: TranscriptionProvider | None = None,
        pronunciation_analysis_service: PronunciationAnalysisService | None = None,
    ) -> None:
        self.config = config
        self.upload_service = upload_service or UploadService()
        self.duration_service = duration_service or AudioDurationService()
        self.validation_service = validation_service or AudioValidationService()
        self.transcription_service = (
            transcription_service or FasterWhisperTranscriptionService()
        )
        self.pronunciation_analysis_service = (
            pronunciation_analysis_service or PronunciationAnalysisService()
        )

    async def create_assessment(self, audio: UploadFile) -> AssessmentResponse:
        self.validation_service.validate_upload_metadata(audio)

        stored_upload = await self.upload_service.save_upload(
            audio,
            self.config.upload_dir,
            self.config.max_upload_size_bytes,
        )

        try:
            duration_seconds = self.duration_service.get_duration_seconds(
                stored_upload.path
            )
            self.validation_service.validate_duration(duration_seconds)
        except AudioDurationError:
            stored_upload.path.unlink(missing_ok=True)
            raise_api_error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "audio_duration_unreadable",
                "Unable to determine the uploaded audio duration.",
            )
        except Exception:
            stored_upload.path.unlink(missing_ok=True)
            raise

        try:
            transcript = self.transcription_service.transcribe(stored_upload.path)
        except TranscriptionError:
            stored_upload.path.unlink(missing_ok=True)
            raise_api_error(
                status.HTTP_502_BAD_GATEWAY,
                "transcription_failed",
                "Speech transcription failed.",
            )

        analysis = self.pronunciation_analysis_service.analyze(
            transcript,
            duration_seconds,
        )

        return AssessmentResponse(
            message="Audio uploaded, transcribed, and analyzed successfully.",
            status="analyzed",
            upload={
                "filename": stored_upload.filename,
                "duration_seconds": round(duration_seconds, 2),
                "content_type": stored_upload.content_type,
                "size_bytes": stored_upload.size_bytes,
            },
            transcription=transcript,
            analysis=analysis,
        )
