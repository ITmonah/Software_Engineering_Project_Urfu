from fastapi import APIRouter, Request

from api.endpoints.modelEnd import change_version, detect
from modelsPyd import ChangeModelResponse

router = APIRouter()


@router.get("/detect")
async def detect_image(image_url: str, request: Request):
    return await detect(image_url, request)


@router.get("/change_version", response_model=ChangeModelResponse)
async def change(version: int, request: Request):
    return await change_version(version, request)
