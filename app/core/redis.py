import redis
from app.core.config import settings

# Initialize redis client without connecting immediately
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)

def get_redis():
    """Helper to return the redis client instance."""
    return redis_client