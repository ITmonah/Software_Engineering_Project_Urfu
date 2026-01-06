from fastapi import APIRouter
from modelsPyd import DetectionResponse
from api.endpoints.modelEnd import detect as detect_handler

router = APIRouter()


@router.get("/detect", response_model=DetectionResponse)
async def detect(image_url: str):
    return await detect_handler(image_url)
