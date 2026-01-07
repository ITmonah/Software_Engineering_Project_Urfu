from typing import Optional
import torch
import requests
from io import BytesIO
from PIL import Image
from fastapi import Request
from modelsPyd import DetectionResult, DetectionResponse
from redis_client.client import get_redis
from ultralytics import YOLO
from helpers.logger import log

modelYOLOV11s = YOLO('yolo11s.pt')
modelYOLOV11m = YOLO('yolo11m.pt')
available_version = ["11s","11m"]

def load_image_from_url(url: str) -> Image.Image:
    # Загружает изображение по URL и возвращает объект PIL.Image
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def get_client_ip(request: Request) -> Optional[str]:
    # Возвращает IP клиента из заголовков или объекта запроса
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    if request.client:
        return request.client.host
    
    return None

async def change_version(version: int, request: Request):
    # Меняет предпочитаемую версию модели для IP в Redis
    func_name = "change_version"
    try:        
        redis = get_redis()

        ip = get_client_ip(request)
        if not ip:
            log(func_name, "IP не найден", "ERROR")
            return {"result": "IP не найден"}

        await redis.set(str(ip), str(available_version[version]))

        return {"result": f"Версия модели изменена на {available_version[version]}"}

    except Exception as e:
        log(func_name, f"Ошибка смены версии: {e}", "ERROR")
        return {"result": f"Ошибка смены версии"}


async def detect(image_url: str, request: Request):
    # Выполняет детекцию объектов по URL изображения и возвращает структурированный ответ
    func_name = "detect"
    try:
        redis = get_redis()
        image = load_image_from_url(image_url)

        ip = get_client_ip(request)
        if not ip:
            log(func_name, "IP не найден", "ERROR")
            return {"result": "IP не найден"}
        
        version = await redis.get(str(ip))
        if version == "11s":
            results = modelYOLOV11s(image)
        elif version == "11m":
            results = modelYOLOV11m(image)
        else:
            results = modelYOLOV11s(image)
            version = "11s"

        result = results[0]
        
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        
        formatted_results = []
        for i in range(len(boxes)):
            box = boxes[i]
            confidence = confidences[i]
            class_id = int(class_ids[i])
            if version == "11s":
                class_name = modelYOLOV11s.names[class_id]
            else:
                class_name = modelYOLOV11m.names[class_id]
            
            formatted_results.append(DetectionResult(
                xmin = float(box[0]),
                ymin = float(box[1]),
                xmax = float(box[2]),
                ymax = float(box[3]),
                confidence = float(confidence),
                class_ = class_id,
                name = class_name
            ))

        return DetectionResponse(results=formatted_results)

    except Exception as e:
        log(func_name, f"Ошибка обработки изображения: {e}", "ERROR")
        return {"error": f"Ошибка обработки изображения"}