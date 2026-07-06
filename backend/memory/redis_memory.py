import redis
import os

from dotenv import load_dotenv

load_dotenv()


class LazyRedis:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            redis_url = os.getenv("REDIS_URL")
            if redis_url:
                # Strip leading/trailing spaces in case of copy-paste issues
                redis_url = redis_url.strip()
                self._client = redis.Redis.from_url(redis_url, decode_responses=True)
            else:
                self._client = redis.Redis(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", 6379)),
                    db=0,
                    decode_responses=True
                )
        return self._client

    def __getattr__(self, name):
        return getattr(self._get_client(), name)

redis_client = LazyRedis()