import redis

class Cache:
    def __init__(self, host="localhost", port=6379):
        self.redis = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, expire=3600):
        self.redis.set(key, value, ex=expire)
