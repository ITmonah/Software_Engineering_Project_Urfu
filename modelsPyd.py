from pydantic import BaseModel


class DetectionResult(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    confidence: float
    class_: int
    name: str


class DetectionResponse(BaseModel):
    results: list[DetectionResult]


class ChangeModelResponse(BaseModel):
    result: str
