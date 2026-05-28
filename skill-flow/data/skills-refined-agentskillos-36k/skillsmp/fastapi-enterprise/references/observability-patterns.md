# Observability Patterns

OpenTelemetry tracing, Prometheus metrics, and conversation ID tracking.

## Conversation ID Tracking

Track requests end-to-end with UUIDs.

### middleware/conversation.py

```python
import uuid
from contextvars import ContextVar
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

_conversation_id: ContextVar[Optional[str]] = ContextVar("conversation_id", default=None)

CONVERSATION_HEADER = "X-Conversation-ID"
CONVERSATION_COOKIE = "conversation_id"

def get_conversation_id() -> Optional[str]:
    return _conversation_id.get()

def set_conversation_id(conversation_id: str) -> None:
    _conversation_id.set(conversation_id)

class ConversationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get or generate conversation ID
        conversation_id = request.headers.get(CONVERSATION_HEADER)
        if not conversation_id:
            conversation_id = request.cookies.get(CONVERSATION_COOKIE)
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        set_conversation_id(conversation_id)
        
        response: Response = await call_next(request)
        
        response.headers[CONVERSATION_HEADER] = conversation_id
        response.set_cookie(
            key=CONVERSATION_COOKIE,
            value=conversation_id,
            httponly=True,
            samesite="lax",
        )
        
        return response
```

## Prometheus Metrics

### Install

```bash
pip install prometheus-client
```

### Setup (core/metrics.py)

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# HTTP requests
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)

# Database
db_connections_active = Gauge(
    "db_connections_active",
    "Active database connections"
)

# Business metrics
user_registrations_total = Counter(
    "user_registrations_total",
    "Total user registrations"
)
```

### Middleware (middleware/metrics.py)

```python
from starlette.middleware.base import BaseHTTPMiddleware
from core.metrics import http_requests_total, http_request_duration_seconds
import time

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
```

### Metrics Endpoint

```python
# api/routes/metrics.py
from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

router = APIRouter(tags=["Metrics"])

@router.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

## OpenTelemetry (Optional)

### Install

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi
```

### Setup (core/tracing.py)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_tracing(app):
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
    
    FastAPIInstrumentor.instrument_app(app)
```

### Usage in app.py

```python
from core.tracing import setup_tracing

app = FastAPI()
setup_tracing(app)
```

## Custom Business Metrics

```python
# services/user/profile.py
from core.metrics import user_registrations_total

async def create_user(db, data):
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    
    # Track metric
    user_registrations_total.inc()
    
    return user
```

## Health Checks

```python
# api/routes/health.py
from fastapi import APIRouter
from core.db import engine

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "components": {
            "database": db_status,
            "api": "healthy"
        }
    }
```

## Conversation ID Usage

All logs include conversation_id automatically:

```python
logger.info("User created", user_id=user.id)
# Output: {"event": "User created", "conversation_id": "abc-123", "user_id": 456}
```

External API calls propagate conversation_id:

```python
response = await external_client.get("/users")
# Request includes header: X-Conversation-ID: abc-123
```

## Next Steps

- [Logging Patterns](logging-patterns.md) - Structured logs with conversation ID
- [HTTPX Client Patterns](httpx-patterns.md) - Propagating conversation ID
- [Error Handling Workflow](error-handling-workflow.md) - Debugging with traces
