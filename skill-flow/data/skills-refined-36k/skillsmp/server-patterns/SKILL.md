---
name: server-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Django, FastAPI, and Flask API routes.
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications.

## API Design Patterns

### RESTful API Structure

```python
# ✅ Resource-based URLs
GET    /api/markets/                # List resources
GET    /api/markets/{id}/           # Get single resource
POST   /api/markets/                # Create resource
PUT    /api/markets/{id}/           # Replace resource
PATCH  /api/markets/{id}/           # Update resource
DELETE /api/markets/{id}/           # Delete resource

# ✅ Query parameters for filtering, sorting, pagination
GET /api/markets/?status=active&ordering=-volume&limit=20&offset=0
```

### Repository Pattern

**Django:**
```python
# models.py
from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

# repositories.py
from typing import Optional, List
from django.db.models import QuerySet

class MarketRepository:
    def find_all(self, filters: Optional[dict] = None) -> QuerySet:
        queryset = Market.objects.all()

        if filters:
            if status := filters.get('status'):
                queryset = queryset.filter(status=status)
            if limit := filters.get('limit'):
                queryset = queryset[:limit]

        return queryset

    def find_by_id(self, market_id: int) -> Optional[Market]:
        try:
            return Market.objects.get(id=market_id)
        except Market.DoesNotExist:
            return None

    def create(self, data: dict) -> Market:
        return Market.objects.create(**data)

    def update(self, market_id: int, data: dict) -> Market:
        market = Market.objects.get(id=market_id)
        for key, value in data.items():
            setattr(market, key, value)
        market.save()
        return market

    def delete(self, market_id: int) -> None:
        Market.objects.filter(id=market_id).delete()
```


### Service Layer Pattern

**Django:**
```python
# services.py
from typing import List
from repositories import MarketRepository

class MarketService:
    def __init__(self, market_repo: MarketRepository):
        self.market_repo = market_repo

    def search_markets(self, query: str, limit: int = 10) -> List[Market]:
        embedding = self._generate_embedding(query)
        results = self._vector_search(embedding, limit)
        market_ids = [r['id'] for r in results]
        markets = list(self.market_repo.find_all({'id__in': market_ids}))
        score_map = {r['id']: r['score'] for r in results}
        markets.sort(key=lambda m: score_map.get(m.id, 0), reverse=True)
        return markets

    def _generate_embedding(self, query: str) -> List[float]:
        pass

    def _vector_search(self, embedding: List[float], limit: int) -> List[dict]:
        pass
```


### Middleware Pattern

**Django:**
```python
# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import jwt

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/auth/'):
            return None

        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = payload  # Attach user to request
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return None

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'myapp.middleware.AuthMiddleware',
    # ... other middleware
]
```


## Database Patterns

### Query Optimization

**Django:**
```python
# ✅ GOOD: Select only needed columns
markets = Market.objects.filter(
    status='active'
).only('id', 'name', 'status', 'volume').order_by('-volume')[:10]

# ❌ BAD: Select everything
markets = Market.objects.filter(status='active').order_by('-volume')[:10]

# ✅ GOOD: Use select_related for foreign keys
markets = Market.objects.select_related('creator').all()

# ✅ GOOD: Use prefetch_related for many-to-many
markets = Market.objects.prefetch_related('tags').all()
```


### N+1 Query Prevention

**Django:**
```python
# ❌ BAD: N+1 query problem
markets = Market.objects.all()
for market in markets:
    market.creator = User.objects.get(id=market.creator_id)  # N queries

# ✅ GOOD: Use select_related (foreign key)
markets = Market.objects.select_related('creator').all()
# Single query with JOIN

# ✅ GOOD: Use prefetch_related (many-to-many, reverse FK)
markets = Market.objects.prefetch_related('tags', 'positions').all()

# ✅ GOOD: Manual prefetch for complex cases
markets = Market.objects.all()
creator_ids = [m.creator_id for m in markets]
creators = {c.id: c for c in User.objects.filter(id__in=creator_ids)}
for market in markets:
    market.creator = creators.get(market.creator_id)
```

### Transaction Pattern

**Django:**
```python
from django.db import transaction

@transaction.atomic
def create_market_with_position(market_data: dict, position_data: dict):
    market = Market.objects.create(**market_data)
    position = Position.objects.create(
        market=market,
        **position_data
    )
    return market, position

def create_market_with_position(market_data: dict, position_data: dict):
    with transaction.atomic():
        market = Market.objects.create(**market_data)
        position = Position.objects.create(
            market=market,
            **position_data
        )
        return market, position
```


## Caching Strategies

### Redis Caching Layer

**Django:**
```python
# repositories.py
import json
from django.core.cache import cache
from typing import Optional
from .models import Market

class CachedMarketRepository:
    def __init__(self, base_repo):
        self.base_repo = base_repo
        self.cache_timeout = 300  # 5 minutes

    def find_by_id(self, market_id: int) -> Optional[Market]:
        cache_key = f'market:{market_id}'
        cached = cache.get(cache_key)
        if cached:
            return Market(**json.loads(cached))

        market = self.base_repo.find_by_id(market_id)

        if market:
            cache.set(
                cache_key,
                json.dumps({
                    'id': market.id,
                    'name': market.name,
                    'status': market.status,
                    # ... other fields
                }),
                self.cache_timeout
            )

        return market

    def invalidate_cache(self, market_id: int) -> None:
        cache.delete(f'market:{market_id}')
```


### Cache-Aside Pattern

**Django:**
```python
from django.core.cache import cache
import json

def get_market_with_cache(market_id: int) -> Market:
    cache_key = f'market:{market_id}'
    cached = cache.get(cache_key)
    if cached:
        return Market(**json.loads(cached))

    try:
        market = Market.objects.get(id=market_id)
    except Market.DoesNotExist:
        raise ValueError('Market not found')

    cache.set(
        cache_key,
        json.dumps({
            'id': market.id,
            'name': market.name,
            # ... other fields
        }),
        300
    )
    return market
```


## Error Handling Patterns

### Centralized Error Handler

**Django:**
```python
# exceptions.py
class ApiError(Exception):
    def __init__(self, status_code: int, message: str, is_operational: bool = True):
        self.status_code = status_code
        self.message = message
        self.is_operational = is_operational
        super().__init__(self.message)

from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            return JsonResponse({
                'success': False,
                'error': 'Validation failed',
                'details': exc.detail
            }, status=400)

        return JsonResponse({
            'success': False,
            'error': str(exc)
        }, status=response.status_code)

    if isinstance(exc, ApiError):
        return JsonResponse({
            'success': False,
            'error': exc.message
        }, status=exc.status_code)

    logger.error('Unexpected error:', exc_info=True)

    return JsonResponse({
        'success': False,
        'error': 'Internal server error'
    }, status=500)

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_markets(request):
    try:
        data = fetch_data()
        return Response({'success': True, 'data': data})
    except ApiError as e:
        raise
    except Exception as e:
        raise ApiError(500, 'Internal server error')
```


### Retry with Exponential Backoff

**Django:**
```python
import time
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

def fetch_with_retry(
    fn: Callable[[], T],
    max_retries: int = 3
) -> T:
    last_error = None

    for i in range(max_retries):
        try:
            return fn()
        except Exception as error:
            last_error = error

            if i < max_retries - 1:
                delay = (2 ** i) * 1.0
                time.sleep(delay)

    raise last_error

# Async version
async def fetch_with_retry_async(
    fn: Callable[[], T],
    max_retries: int = 3
) -> T:
    last_error = None

    for i in range(max_retries):
        try:
            return await fn()
        except Exception as error:
            last_error = error

            if i < max_retries - 1:
                delay = (2 ** i) * 1.0
                await asyncio.sleep(delay)

    raise last_error

# Usage
data = fetch_with_retry(lambda: fetch_from_api())
```


## Authentication & Authorization

### JWT Token Validation

**Django:**
```python
# auth.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.InvalidTokenError:
        raise ApiError(401, 'Invalid token')

def require_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None

        if not token:
            return JsonResponse(
                {'error': 'Missing authorization token'},
                status=401
            )

        try:
            user = verify_token(token)
            request.user = user  # Attach user to request
            return view_func(request, *args, **kwargs)
        except ApiError as e:
            return JsonResponse({'error': e.message}, status=e.status_code)

    return wrapper

# Usage in view
@require_auth
def get_markets(request):
    user_id = request.user['userId']
    data = get_data_for_user(user_id)
    return JsonResponse({'success': True, 'data': data})
```


### Role-Based Access Control

**Django:**
```python
# auth.py
from typing import Literal

Permission = Literal['read', 'write', 'delete', 'admin']
UserRole = Literal['admin', 'moderator', 'user']

ROLE_PERMISSIONS: dict[UserRole, list[Permission]] = {
    'admin': ['read', 'write', 'delete', 'admin'],
    'moderator': ['read', 'write', 'delete'],
    'user': ['read', 'write']
}

def has_permission(user: dict, permission: Permission) -> bool:
    role = user.get('role', 'user')
    return permission in ROLE_PERMISSIONS.get(role, [])

def require_permission(permission: Permission):
    def decorator(view_func):
        @wraps(view_func)
        @require_auth
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                return JsonResponse(
                    {'error': 'Insufficient permissions'},
                    status=403
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@require_permission('delete')
def delete_market(request, market_id):
    pass
```


## Rate Limiting

### Simple In-Memory Rate Limiter

**Django:**
```python
# rate_limiter.py
from collections import defaultdict
from time import time
from threading import Lock

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = Lock()

    def check_limit(
        self,
        identifier: str,
        max_requests: int,
        window_ms: int
    ) -> bool:
        now = time() * 1000
        window_seconds = window_ms / 1000

        with self.lock:
            requests = self.requests[identifier]
            recent_requests = [
                req_time for req_time in requests
                if now - req_time < window_ms
            ]
            if len(recent_requests) >= max_requests:
                return False
            recent_requests.append(now)
            self.requests[identifier] = recent_requests
            return True

limiter = RateLimiter()

# Usage in view
from django.http import JsonResponse

def get_markets(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
    allowed = limiter.check_limit(ip, 100, 60000)  # 100 req/min
    if not allowed:
        return JsonResponse({
            'error': 'Rate limit exceeded'
        }, status=429)
    return JsonResponse({'data': 'markets'})
```


**Note:** For production, use Redis-based rate limiting with libraries like:
- Django: `django-ratelimit` or `django-ratelimit2`

## Background Jobs & Queues

### Simple Queue Pattern

**Django:**
```python
# queue.py
import queue
import threading
from typing import TypeVar, Generic, Callable
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class IndexJob:
    market_id: int

class JobQueue(Generic[T]):
    def __init__(self, executor: Callable[[T], None]):
        self.queue: queue.Queue = queue.Queue()
        self.processing = False
        self.executor = executor
        self.lock = threading.Lock()

    def add(self, job: T) -> None:
        self.queue.put(job)
        with self.lock:
            if not self.processing:
                self.processing = True
                threading.Thread(target=self._process, daemon=True).start()

    def _process(self) -> None:
        while True:
            try:
                job = self.queue.get(timeout=1)
                try:
                    self.executor(job)
                except Exception as error:
                    print(f'Job failed: {error}')
                finally:
                    self.queue.task_done()
            except queue.Empty:
                with self.lock:
                    if self.queue.empty():
                        self.processing = False
                        break

def index_market(job: IndexJob):
    print(f"Indexing market {job.market_id}")

index_queue = JobQueue[IndexJob](index_market)

# Usage in view
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def create_market(request):
    data = json.loads(request.body)
    market_id = data.get('marketId')
    index_queue.add(IndexJob(market_id=market_id))
    return JsonResponse({'success': True, 'message': 'Job queued'})
```


**Note:** For production, use proper task queues:
- Django: `Celery` with Redis/RabbitMQ
- FastAPI: `Celery` or `ARQ` (Redis-based)
- Flask: `Celery` or `RQ` (Redis Queue)

## Logging & Monitoring

### Structured Logging

**Django:**
```python
# logger.py
import logging
import json
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _log(
        self,
        level: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **(context or {})
        }
        self.logger.log(getattr(logging, level.upper()), json.dumps(entry))

    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self._log('info', message, context)

    def warn(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self._log('warning', message, context)

    def error(
        self,
        message: str,
        error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        error_context = {
            **(context or {}),
            'error': str(error) if error else None,
            'error_type': type(error).__name__ if error else None
        }
        if error and hasattr(error, '__traceback__'):
            import traceback
            error_context['traceback'] = traceback.format_exc()
        self._log('error', message, error_context)

logger = StructuredLogger(__name__)

# Usage in view
from django.http import JsonResponse
import uuid

def get_markets(request):
    request_id = str(uuid.uuid4())
    logger.info('Fetching markets', {
        'request_id': request_id,
        'method': request.method,
        'path': request.path
    })
    try:
        markets = fetch_markets()
        return JsonResponse({'success': True, 'data': markets})
    except Exception as error:
        logger.error('Failed to fetch markets', error, {'request_id': request_id})
        return JsonResponse({'error': 'Internal error'}, status=500)
```


**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.
