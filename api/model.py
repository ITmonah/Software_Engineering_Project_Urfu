from fastapi import APIRouter, Request, Response

from api.endpoints.modelEnd import change_version, detect
from modelsPyd import ChangeModelResponse

router = APIRouter()


@router.get("/detect")
async def detect_image(image_url: str, request: Request, response: Response):
    return await detect(image_url, request, response)


@router.get("/change_version", response_model=ChangeModelResponse)
async def change(version: int, request: Request, response: Response):
    return await change_version(version, request, response)
