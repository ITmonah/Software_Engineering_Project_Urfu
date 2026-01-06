import redis.asyncio as redis
from typing import Optional
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

# Глобальная переменная для клиента
redis_client: Optional[redis.Redis] = None

async def init_redis(
    host: str = os.getenv("REDIS_HOST", "localhost"),
    port: int = int(os.getenv("REDIS_PORT", 6379)),
    db: int = int(os.getenv("REDIS_DB", 0)),
) -> redis.Redis:
    """Инициализация Redis и возврат клиента"""
    global redis_client
    
    try:
        redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_connect_timeout=5
        )
        
        # Проверка подключения
        await redis_client.ping()
        logger.info("Redis подключен")
        
        return redis_client
        
    except Exception as e:
        logger.error(f"Ошибка подключения к Redis: {e}")
        raise

def get_redis() -> redis.Redis:
    """Получение Redis клиента"""
    if redis_client is None:
        raise RuntimeError("Redis не инициализирован")
    return redis_client

async def close_redis():
    """Закрытие подключения"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        logger.info("Redis отключен")
