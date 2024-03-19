from redis import Redis


class RedisTools:

    redis = Redis(host='localhost', port=6379)

    @classmethod
    def set_data(cls, key: str, value) -> None:
        cls.redis.set(key, value)

    @classmethod
    def get_data(cls, key: str):
        return cls.redis.get(key)

    @classmethod
    def get_keys(cls):
        return cls.redis.keys()

    @classmethod
    def clear(cls):
        cls.redis.flushdb()
