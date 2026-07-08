from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.models.assessment import AssessmentResponse
from app.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessments", tags=["assessments"])


def get_assessment_service() -> AssessmentService:
    return AssessmentService()


@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment(
    audio: Annotated[UploadFile, File(...)],
    service: Annotated[AssessmentService, Depends(get_assessment_service)],
) -> AssessmentResponse:
    return await service.create_assessment(audio)
