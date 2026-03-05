from fastapi import APIRouter

from app.api.v1 import video

router = APIRouter()
router.include_router(video.router, prefix="/v1/video", tags=["Video Analysis"])
