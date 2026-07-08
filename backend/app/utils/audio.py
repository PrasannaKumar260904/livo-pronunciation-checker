SUPPORTED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/mp4",
    "audio/wav",
    "audio/webm",
    "audio/x-m4a",
    "audio/x-wav",
}


def is_supported_audio_type(content_type: str | None) -> bool:
    return content_type in SUPPORTED_AUDIO_TYPES

