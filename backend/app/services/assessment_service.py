from fastapi import HTTPException, UploadFile, status


class AssessmentService:
    async def create_assessment(self, audio: UploadFile) -> None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Pronunciation assessment is not implemented yet.",
        )

