import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.model import router as api_router
from helpers.logger import log
from redis_client.client import close_redis, get_redis, init_redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis(host=REDIS_HOST, port=REDIS_PORT)
    redis = get_redis()
    await redis.set("test", "Hello Redis!")
    value = await redis.get("test")
    log("lifespan", f"Редис запустился, тестовой значение: {value}", "INFO")

    yield
    await close_redis()


app = FastAPI(title="YOLO Object Detection", lifespan=lifespan)

# Подключение роутов из API
app.include_router(api_router)
