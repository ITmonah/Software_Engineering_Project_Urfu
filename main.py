from fastapi import FastAPI
from modelsPyd import DetectionResult, DetectionResponse
import torch
import requests
from io import BytesIO
from PIL import Image

# Загружаем модель при старте приложения
modelYOLOV5 = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

app = FastAPI(title="YOLOv5 Object Detection")

def load_image_from_url(url: str) -> Image.Image:
    """Загружает изображение из URL"""
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

@app.get("/detect", response_model=DetectionResponse)
async def detect(image_url: str):
    """
    Выполняет детекцию объектов на изображении по URL
    """
    try:
        image = load_image_from_url(image_url)
        
        results = modelYOLOV5(image)
        
        detections = results.pandas().xyxy[0]
        
        formatted_results = []
        for _, detection in detections.iterrows():
            formatted_results.append(DetectionResult(
                xmin=detection['xmin'],
                ymin=detection['ymin'],
                xmax=detection['xmax'],
                ymax=detection['ymax'],
                confidence=detection['confidence'],
                class_=detection['class'],
                name=detection['name']
            ))
        
        return DetectionResponse(results=formatted_results)
    
    except Exception as e:
        return {"error": f"Ошибка обработки изображения: {str(e)}"}