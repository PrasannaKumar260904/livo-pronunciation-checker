import logging

from fastapi import UploadFile, status

from app.core.config import Settings, settings
from app.models.assessment import AssessmentResponse
from app.services.audio_duration import AudioDurationError, AudioDurationService
from app.services.audio_validation import AudioValidationService
from app.services.feedback_service import FeedbackGenerationError, FeedbackService
from app.services.pronunciation_analysis_service import PronunciationAnalysisService
from app.services.transcription_service import (
    FasterWhisperTranscriptionService,
    TranscriptionError,
    TranscriptionProvider,
)
from app.services.upload_service import UploadService
from app.utils.errors import raise_api_error

logger = logging.getLogger(__name__)


class AssessmentService:
    def __init__(
        self,
        config: Settings = settings,
        upload_service: UploadService | None = None,
        duration_service: AudioDurationService | None = None,
        validation_service: AudioValidationService | None = None,
        transcription_service: TranscriptionProvider | None = None,
        pronunciation_analysis_service: PronunciationAnalysisService | None = None,
        feedback_service: FeedbackService | None = None,
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
        self.feedback_service = feedback_service or FeedbackService()

    async def create_assessment(self, audio: UploadFile) -> AssessmentResponse:
        self.validation_service.validate_upload_metadata(audio)

        stored_upload = await self.upload_service.save_upload(
            audio,
            self.config.upload_dir,
            self.config.max_upload_size_bytes,
        )

        try:
            try:
                duration_seconds = self.duration_service.get_duration_seconds(
                    stored_upload.path
                )
                self.validation_service.validate_duration(duration_seconds)
            except AudioDurationError:
                raise_api_error(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "audio_duration_unreadable",
                    "Unable to determine the uploaded audio duration.",
                )

            try:
                transcript = self.transcription_service.transcribe(stored_upload.path)
            except TranscriptionError:
                logger.exception("Speech transcription failed")
                raise_api_error(
                    status.HTTP_502_BAD_GATEWAY,
                    "transcription_failed",
                    "Speech transcription failed.",
                )

            analysis = self.pronunciation_analysis_service.analyze(
                transcript,
                duration_seconds,
            )

            try:
                feedback = self.feedback_service.generate_feedback(analysis, transcript)
            except FeedbackGenerationError:
                logger.warning("Feedback generation failed", exc_info=True)
                feedback = None

            return AssessmentResponse(
                message=(
                    "Audio uploaded, transcribed, analyzed, and reviewed successfully."
                ),
                status="analyzed",
                upload={
                    "filename": stored_upload.filename,
                    "duration_seconds": round(duration_seconds, 2),
                    "content_type": stored_upload.content_type,
                    "size_bytes": stored_upload.size_bytes,
                },
                transcription=transcript,
                analysis=analysis,
                feedback=feedback,
            )
        finally:
            try:
                stored_upload.path.unlink(missing_ok=True)
            except OSError:
                logger.warning(
                    "Failed to delete temporary upload",
                    extra={"path": str(stored_upload.path)},
                    exc_info=True,
                )
