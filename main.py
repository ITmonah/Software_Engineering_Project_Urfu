from fastapi import FastAPI
from api.model import router as api_router
from contextlib import asynccontextmanager
from redis_client.client import init_redis, close_redis, get_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis(host="localhost", port=6379)
    redis = get_redis()
    await redis.set("test", "Hello Redis!")
    value = await redis.get("test")
    print("Redis работает!", "value: ", value)

    yield
    await close_redis()

app = FastAPI(title="YOLO Object Detection", lifespan=lifespan)

# Подключаем роуты из API
app.include_router(api_router)
