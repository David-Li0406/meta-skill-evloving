# FastAPI Middleware & Events Reference

## Middleware

### Custom Middleware

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Function-based middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Class-based middleware
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Before request
        response = await call_next(request)
        # After request
        return response

app.add_middleware(CustomMiddleware)
```

### Built-in Middleware

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Custom-Header"],
    max_age=600
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])

# HTTPS redirect
app.add_middleware(HTTPSRedirectMiddleware)
```

## Startup & Shutdown Events

### Lifespan Context Manager (Recommended)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: runs before accepting requests
    db_pool = await create_db_pool()
    app.state.db = db_pool
    yield
    # Shutdown: runs after finishing requests
    await db_pool.close()

app = FastAPI(lifespan=lifespan)
```

### Event Decorators (Legacy)

```python
@app.on_event("startup")
async def startup_event():
    await database.connect()
    app.state.config = load_config()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

async def send_email(email: str, message: str):
    # Async email sending
    await email_client.send(email, message)

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification sent in the background"}

# In dependencies
def write_notification(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"Query: {q}")
    return q

@app.post("/items/")
async def create_item(query: str = Depends(write_notification)):
    return {"query": query}
```

## Request Object

```python
from fastapi import Request

@app.get("/items/")
async def read_items(request: Request):
    # Request properties
    request.method          # "GET"
    request.url             # URL object
    request.url.path        # "/items/"
    request.url.query       # "q=foo&limit=10"
    request.headers         # Headers dict-like
    request.query_params    # QueryParams object
    request.path_params     # Dict of path params
    request.cookies         # Dict of cookies
    request.client          # Client info (host, port)
    request.state           # Custom state object

    # Body methods
    body = await request.body()      # Raw bytes
    json = await request.json()      # Parsed JSON
    form = await request.form()      # Form data

    return {"path": request.url.path}
```
