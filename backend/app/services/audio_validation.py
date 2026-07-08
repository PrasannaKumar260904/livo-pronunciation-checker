from fastapi import UploadFile, status

from app.utils.audio import (
    ALLOWED_AUDIO_EXTENSIONS,
    ALLOWED_AUDIO_MIME_TYPES,
    MAX_AUDIO_DURATION_SECONDS,
    MIN_AUDIO_DURATION_SECONDS,
    is_supported_audio_extension,
    is_supported_audio_type,
)
from app.utils.errors import raise_api_error


class AudioValidationService:
    def validate_upload_metadata(self, audio: UploadFile) -> None:
        if not is_supported_audio_type(audio.content_type):
            raise_api_error(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "unsupported_mime_type",
                "Unsupported audio MIME type. Upload WAV, MP3, M4A, or WebM audio.",
                {
                    "allowed_mime_types": sorted(ALLOWED_AUDIO_MIME_TYPES),
                    "received_content_type": audio.content_type,
                },
            )

        if not is_supported_audio_extension(audio.filename):
            raise_api_error(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "unsupported_file_extension",
                "Unsupported audio file extension. Upload .wav, .mp3, .m4a, or .webm.",
                {
                    "allowed_extensions": sorted(ALLOWED_AUDIO_EXTENSIONS),
                    "received_filename": audio.filename,
                },
            )

    def validate_duration(self, duration_seconds: float) -> None:
        if duration_seconds < MIN_AUDIO_DURATION_SECONDS:
            raise_api_error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "audio_too_short",
                "Audio must be at least 30 seconds long.",
                {
                    "duration_seconds": round(duration_seconds, 2),
                    "minimum_duration_seconds": MIN_AUDIO_DURATION_SECONDS,
                },
            )

        if duration_seconds > MAX_AUDIO_DURATION_SECONDS:
            raise_api_error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "audio_too_long",
                "Audio must be no longer than 45 seconds.",
                {
                    "duration_seconds": round(duration_seconds, 2),
                    "maximum_duration_seconds": MAX_AUDIO_DURATION_SECONDS,
                },
            )
