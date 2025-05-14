import redis
from config import Config

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)

def set_cache(key, value, ex=3600):
    redis_client.set(key, value, ex=ex)

def get_cache(key):
    return redis_client.get(key) 