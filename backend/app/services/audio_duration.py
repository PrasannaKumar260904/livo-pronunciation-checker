from pathlib import Path

from mutagen import File as MutagenFile


class AudioDurationError(ValueError):
    pass


class AudioDurationService:
    def get_duration_seconds(self, path: Path) -> float:
        try:
            audio = MutagenFile(path)
        except Exception as exc:
            raise AudioDurationError("Unable to read audio metadata.") from exc

        if audio is None or audio.info is None:
            raise AudioDurationError("Unable to read audio metadata.")

        duration = getattr(audio.info, "length", None)
        if duration is None or duration <= 0:
            raise AudioDurationError("Unable to determine audio duration.")

        return float(duration)
