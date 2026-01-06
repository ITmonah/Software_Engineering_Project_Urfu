from fastapi import FastAPI
from api.model import router as api_router

app = FastAPI(title="YOLOv5 Object Detection")

# Подключаем роуты из API
app.include_router(api_router)
