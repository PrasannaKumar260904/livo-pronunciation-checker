from fastapi import APIRouter

from app.api.routes import assessments, health

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(assessments.router)

root_router = APIRouter()
root_router.include_router(health.router)
