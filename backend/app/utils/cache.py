import time
from typing import Any, Optional, Dict

class TTLCache:
    def __init__(self, default_ttl_seconds: int = 30):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        self._store[key] = value
        self._expiry[key] = time.time() + ttl

    def get(self, key: str) -> Optional[Any]:
        exp = self._expiry.get(key)
        if exp is None:
            return None
        if time.time() > exp:
            self._store.pop(key, None)
            self._expiry.pop(key, None)
            return None
        return self._store.get(key)

    def clear(self):
        self._store.clear()
        self._expiry.clear()
