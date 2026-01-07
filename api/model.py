from fastapi import APIRouter, Request
from modelsPyd import DetectionResponse, ChangeModelResponse
from api.endpoints.modelEnd import detect, change_version

router = APIRouter()


@router.get("/detect")
async def detect_image(image_url: str, request: Request):
    return await detect(image_url, request)

@router.get("/change_version", response_model=ChangeModelResponse)
async def change(version: int, request: Request):
    return await change_version(version, request)
