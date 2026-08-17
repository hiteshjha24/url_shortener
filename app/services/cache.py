from app.core.redis import redis_client
import logging

DEFAULT_CACHE_TTL = 3600
logger = logging.getLogger(__name__)

def get_cached_url(short_code: str) -> str | None:
    try:
        val = redis_client.get(f"url:{short_code}")
        if isinstance(val, bytes):
            return val.decode("utf-8")
        return val
    except Exception as e:
        logger.debug(f"Redis cache miss or error: {e}")
        return None


def set_cached_url(short_code: str, target_url: str, ttl: int = DEFAULT_CACHE_TTL) -> None:
    try:
        redis_client.set(f"url:{short_code}", str(target_url), ex=ttl)
    except Exception as e:
        logger.debug(f"Redis set error (cache disabled): {e}")


def delete_cached_url(short_code: str) -> None:
    try:
        redis_client.delete(f"url:{short_code}")
    except Exception as e:
        logger.debug(f"Redis delete error: {e}")