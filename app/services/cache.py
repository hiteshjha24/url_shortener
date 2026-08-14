from app.core.redis import redis_client

DEFAULT_CACHE_TTL = 3600

def get_cached_url(short_code: str) -> str | None:
    try:
        val = redis_client.get(f"url:{short_code}")
        if isinstance(val, bytes):
            return val.decode("utf-8")
        return val
    except Exception:
        return None


def set_cached_url(short_code: str, target_url: str, ttl: int = DEFAULT_CACHE_TTL) -> None:
    try:
        redis_client.setex(f"url:{short_code}", ttl, target_url)
    except Exception:
        pass


def delete_cached_url(short_code: str) -> None:
    try:
        redis_client.delete(f"url:{short_code}")
    except Exception:
        pass