from datetime import datetime, timedelta
from backend.logger.logger import logger

class CacheService:
    def __init__(self):
        self._cache = {}
        self.TTL_SECONDS = 3600

    def get(self, key: str):
        entry = self._cache.get(key)
        if not entry: return None
        
        if datetime.now() > entry["expires"]:
            del self._cache[key]
            return None
            
        logger.info(f"Cache HIT for key: {key}")
        return entry["data"]

    def set(self, key: str, data: dict):
        self._cache[key] = {
            "data": data,
            "expires": datetime.now() + timedelta(seconds=self.TTL_SECONDS)
        }
        logger.info(f"Cache SET for key: {key}")

cache_service = CacheService()