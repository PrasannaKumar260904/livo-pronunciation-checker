from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.services.assessment_service import AssessmentService
from app.utils.audio import is_supported_audio_type

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_assessment(audio: UploadFile = File(...)) -> None:
    if not is_supported_audio_type(audio.content_type):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported audio type. Upload WAV, MP3, M4A, or WebM audio.",
        )

    if audio.size and audio.size > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Audio file must be {settings.max_upload_size_mb} MB or smaller.",
        )

    service = AssessmentService()
    await service.create_assessment(audio)

