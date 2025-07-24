import redis
from config import Config

# Fallback: caché en memoria
memory_cache = {}

try:
    redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)
    redis_client.ping()
    USE_REDIS = True
except Exception:
    USE_REDIS = False


def set_cache(key, value, ex=3600):
    if USE_REDIS:
        redis_client.set(key, value, ex=ex)
    else:
        memory_cache[key] = value


def get_cache(key):
    if USE_REDIS:
        return redis_client.get(key)
    else:
        return memory_cache.get(key) 