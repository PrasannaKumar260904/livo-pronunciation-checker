from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, status

from app.models.upload import StoredUpload
from app.utils.audio import get_file_extension
from app.utils.errors import raise_api_error

UPLOAD_CHUNK_SIZE_BYTES = 1024 * 1024


class UploadService:
    async def save_upload(
        self,
        upload: UploadFile,
        upload_dir: Path,
        max_size_bytes: int,
    ) -> StoredUpload:
        upload_dir.mkdir(parents=True, exist_ok=True)

        extension = get_file_extension(upload.filename)
        stored_filename = f"{uuid4().hex}{extension}"
        destination = upload_dir / stored_filename
        size_bytes = 0

        try:
            with destination.open("wb") as output_file:
                while chunk := await upload.read(UPLOAD_CHUNK_SIZE_BYTES):
                    size_bytes += len(chunk)

                    if size_bytes > max_size_bytes:
                        raise_api_error(
                            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            "file_too_large",
                            "Audio file exceeds the maximum allowed upload size.",
                            {"max_size_bytes": max_size_bytes},
                        )

                    output_file.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise

        return StoredUpload(
            path=destination,
            filename=stored_filename,
            content_type=upload.content_type or "application/octet-stream",
            size_bytes=size_bytes,
        )
