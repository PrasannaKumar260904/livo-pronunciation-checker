from pathlib import Path

ALLOWED_AUDIO_MIME_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/wav",
    "audio/wave",
    "audio/webm",
    "audio/x-m4a",
    "audio/x-wav",
}

ALLOWED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".webm"}
MIN_AUDIO_DURATION_SECONDS = 30.0
MAX_AUDIO_DURATION_SECONDS = 45.0


def is_supported_audio_type(content_type: str | None) -> bool:
    return content_type in ALLOWED_AUDIO_MIME_TYPES


def get_file_extension(filename: str | None) -> str:
    return Path(filename or "").suffix.lower()


def is_supported_audio_extension(filename: str | None) -> bool:
    return get_file_extension(filename) in ALLOWED_AUDIO_EXTENSIONS
