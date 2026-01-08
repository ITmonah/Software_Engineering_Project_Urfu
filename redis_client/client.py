import asyncio
import os

import redis.asyncio as redis
from dotenv import load_dotenv

from helpers.logger import log

load_dotenv()

# Глобальная переменная для клиента
redis_client: redis.Redis | None = None


async def init_redis(
    host: str = os.getenv("REDIS_HOST", "127.0.0.1"),
    port: int = int(os.getenv("REDIS_PORT", 6379)),
    db: int = int(os.getenv("REDIS_DB", 0)),
) -> redis.Redis:
    func_name = "init_redis"
    global redis_client

    try:
        redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True, socket_connect_timeout=5
        )

        last_exc = None
        for attempt in range(3):
            try:
                await redis_client.ping()
                log(func_name, "Redis подключение успешно установлено", "INFO")
                return redis_client
            except Exception as e:
                last_exc = e
                log(
                    func_name,
                    f"Попытка {attempt+1}: не удалось подключиться к Redis: {e}",
                    "WARNING",
                )
                await asyncio.sleep(1)

        log(
            func_name,
            f"Ошибка подключения к Redis после 3 попыток: {last_exc}",
            "ERROR",
        )
        raise last_exc

    except Exception as e:
        log(func_name, f"Ошибка подключения к Redis: {e}", "ERROR")
        raise


def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        host = os.getenv("REDIS_HOST", "127.0.0.1")
        port = int(os.getenv("REDIS_PORT", 6379))
        db = int(os.getenv("REDIS_DB", 0))

        redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True, socket_connect_timeout=5
        )
        log(
            "get_redis",
            "Ленивая инициализация Redis без проверки подключения",
            "WARNING",
        )

    return redis_client


async def close_redis():
    global redis_client
    func_name = "close_redis"
    if redis_client:
        await redis_client.close()
        redis_client = None
        log(func_name, "Redis соединение закрыто", "INFO")
