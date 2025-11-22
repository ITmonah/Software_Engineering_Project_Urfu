from pydantic import BaseModel
from typing import List, Optional

class DetectionResult(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    confidence: float
    class_: int
    name: str

class DetectionResponse(BaseModel):
    results: List[DetectionResult]


