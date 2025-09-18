import json, redis
from datetime import timedelta
from typing import Optional, Dict, Any
from .token_repo import TokenRepository

class RedisTokenRepository(TokenRepository):
    def __init__(self, url: str):
        self.r = redis.Redis.from_url(url, decode_responses=True)

    def save(self, token: str, data: Dict[str,Any], ttl: timedelta):
        self.r.set(name=f"session:{token}", value=json.dumps(data), ex=int(ttl.total_seconds()))

    def get(self, token: str) -> Optional[Dict[str,Any]]:
        raw = self.r.get(f"session:{token}")
        return json.loads(raw) if raw else None

    def delete(self, token: str) -> None:
        self.r.delete(f"session:{token}")
