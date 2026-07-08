from pathlib import Path

from pydantic import BaseModel


class StoredUpload(BaseModel):
    path: Path
    filename: str
    content_type: str
    size_bytes: int
