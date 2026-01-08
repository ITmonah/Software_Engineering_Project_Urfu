from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.model import router as api_router
from helpers.logger import log
from redis_client.client import close_redis, get_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis(host="localhost", port=6379)
    redis = get_redis()
    await redis.set("test", "Hello Redis!")
    value = await redis.get("test")
    log("lifespan", f"Редис запустился, тестовой значение: {value}", "INFO")

    yield
    await close_redis()


app = FastAPI(title="YOLO Object Detection", lifespan=lifespan)

# Подключение роутов из API
app.include_router(api_router)
