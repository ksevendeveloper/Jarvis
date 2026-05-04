from fastapi import HTTPException, Request
import time
from typing import Dict

# Simple in-memory rate limiter. For production replace with Redis-backed limiter.
_stores: Dict[str, Dict[str, float]] = {}

def rate_limit(key: str, limit: int = 10, period: int = 60):
    def _inner(request: Request):
        ip = request.client.host if request.client else 'unknown'
        store = _stores.setdefault(key, {})
        now = time.time()
        window_start = now - period
        # remove old
        keys = [k for k, t in store.items() if t < window_start]
        for k in keys:
            del store[k]
        count = len(store)
        if count >= limit:
            raise HTTPException(status_code=429, detail='Too many requests')
        store[f'{ip}:{now}'] = now
    return _inner
