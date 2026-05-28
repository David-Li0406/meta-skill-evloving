# Rate Limiting 패턴

## 알고리즘 비교

| 알고리즘 | 특징 | 메모리 | 정확도 |
|----------|------|--------|--------|
| Fixed Window | 간단 | O(1) | 경계에서 2배 허용 |
| Sliding Window Log | 정확 | O(N) | 높음 |
| Sliding Window Counter | 균형 | O(1) | 중간 |
| Token Bucket | 버스트 허용 | O(1) | 중간 |

---

## Sliding Window Log (Eco² 사용)

```python
from redis.asyncio import Redis
import time

class SlidingWindowRateLimiter:
    """Sliding Window Log Rate Limiter"""

    def __init__(
        self,
        redis: Redis,
        prefix: str = "ratelimit",
    ):
        self._redis = redis
        self._prefix = prefix

    def _key(self, identifier: str) -> str:
        return f"{self._prefix}:{identifier}"

    async def is_allowed(
        self,
        identifier: str,
        limit: int,
        window_seconds: int,
    ) -> tuple[bool, int]:
        """요청 허용 여부 확인

        Returns:
            (allowed, remaining_requests)
        """
        key = self._key(identifier)
        now = time.time()
        window_start = now - window_seconds

        pipe = self._redis.pipeline()

        # 1. 윈도우 외 기록 제거
        pipe.zremrangebyscore(key, 0, window_start)

        # 2. 현재 요청 추가
        pipe.zadd(key, {f"{now}": now})

        # 3. 현재 카운트
        pipe.zcard(key)

        # 4. TTL 설정
        pipe.expire(key, window_seconds)

        results = await pipe.execute()
        count = results[2]

        allowed = count <= limit
        remaining = max(0, limit - count)

        return allowed, remaining

    async def get_retry_after(
        self,
        identifier: str,
        window_seconds: int,
    ) -> float:
        """재시도까지 대기 시간"""
        key = self._key(identifier)
        now = time.time()
        window_start = now - window_seconds

        # 가장 오래된 요청 조회
        oldest = await self._redis.zrangebyscore(
            key,
            window_start,
            now,
            start=0,
            num=1,
        )

        if oldest:
            oldest_time = float(oldest[0])
            retry_after = (oldest_time + window_seconds) - now
            return max(0, retry_after)

        return 0
```

---

## Token Bucket

```python
class TokenBucketRateLimiter:
    """Token Bucket Rate Limiter"""

    REFILL_SCRIPT = """
    local key = KEYS[1]
    local capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    local requested = tonumber(ARGV[4])

    local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
    local tokens = tonumber(bucket[1]) or capacity
    local last_refill = tonumber(bucket[2]) or now

    -- 토큰 리필
    local elapsed = now - last_refill
    local refill = elapsed * refill_rate
    tokens = math.min(capacity, tokens + refill)

    -- 토큰 소비
    if tokens >= requested then
        tokens = tokens - requested
        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, 3600)
        return {1, tokens}  -- allowed, remaining
    else
        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, 3600)
        return {0, tokens}  -- denied, remaining
    end
    """

    def __init__(
        self,
        redis: Redis,
        capacity: int = 100,
        refill_rate: float = 10,  # tokens per second
    ):
        self._redis = redis
        self._capacity = capacity
        self._refill_rate = refill_rate

    async def is_allowed(
        self,
        identifier: str,
        tokens: int = 1,
    ) -> tuple[bool, int]:
        """토큰 소비 시도"""
        key = f"bucket:{identifier}"
        now = time.time()

        result = await self._redis.eval(
            self.REFILL_SCRIPT,
            1,
            key,
            self._capacity,
            self._refill_rate,
            now,
            tokens,
        )

        allowed = result[0] == 1
        remaining = int(result[1])

        return allowed, remaining
```

---

## FastAPI 통합

```python
from fastapi import Request, HTTPException
from functools import wraps

def rate_limit(
    limit: int = 60,
    window: int = 60,
    key_func: Callable[[Request], str] | None = None,
):
    """Rate Limit 데코레이터"""

    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 식별자 추출
            if key_func:
                identifier = key_func(request)
            else:
                identifier = request.client.host

            # Rate Limit 확인
            limiter = request.app.state.rate_limiter
            allowed, remaining = await limiter.is_allowed(
                identifier, limit, window
            )

            # 헤더 설정
            request.state.ratelimit_remaining = remaining
            request.state.ratelimit_limit = limit

            if not allowed:
                retry_after = await limiter.get_retry_after(identifier, window)
                raise HTTPException(
                    status_code=429,
                    detail="Too Many Requests",
                    headers={"Retry-After": str(int(retry_after))},
                )

            return await func(request, *args, **kwargs)

        return wrapper
    return decorator

# 사용
@app.get("/api/chat")
@rate_limit(limit=10, window=60)  # 분당 10회
async def chat(request: Request, message: str):
    ...
```

---

## Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    """전역 Rate Limit Middleware"""

    def __init__(
        self,
        app,
        limiter: SlidingWindowRateLimiter,
        limit: int = 100,
        window: int = 60,
    ):
        super().__init__(app)
        self._limiter = limiter
        self._limit = limit
        self._window = window

    async def dispatch(self, request: Request, call_next):
        identifier = request.client.host

        allowed, remaining = await self._limiter.is_allowed(
            identifier, self._limit, self._window
        )

        if not allowed:
            retry_after = await self._limiter.get_retry_after(
                identifier, self._window
            )
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"},
                headers={
                    "Retry-After": str(int(retry_after)),
                    "X-RateLimit-Limit": str(self._limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        # 헤더 추가
        response.headers["X-RateLimit-Limit"] = str(self._limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response
```

---

## 분산 Rate Limiting

```python
# 여러 인스턴스에서 공유 Redis 사용
# Key: ratelimit:{service}:{identifier}

async def distributed_rate_limit(
    identifier: str,
    service: str = "chat-api",
    limit: int = 100,
    window: int = 60,
) -> bool:
    key = f"ratelimit:{service}:{identifier}"
    # ... 동일 로직
```
