# Request Flow

Detailed implementation of each step in the deterministic chat request flow.

---

## Flow Overview

```
Request → Validate → Authenticate → Resolve → Execute → Respond
            │            │             │          │         │
           400          401           404        503       200
                        403
```

Each step has exactly one responsibility. If a step fails, the request stops immediately with the appropriate error.

---

## Step 1: Validate Request

**Responsibility**: Ensure request body is well-formed and constraints are met.

**Handled by**: Pydantic + FastAPI automatic validation

```python
# schemas/chat.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=100000)
    conversation_id: Optional[str] = None
    model: Optional[str] = "gpt-4"
    system_prompt: Optional[str] = None
    request_id: Optional[str] = None

    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # UUID format validation
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(uuid_pattern, v, re.IGNORECASE):
                raise ValueError('Invalid conversation_id format')
        return v

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        allowed_models = {'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus', 'claude-3-sonnet'}
        if v not in allowed_models:
            raise ValueError(f'Model must be one of: {allowed_models}')
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        # Strip whitespace but ensure not empty after stripping
        v = v.strip()
        if not v:
            raise ValueError('Message cannot be empty or whitespace only')
        return v
```

**Validation errors return 422 (FastAPI default) or 400:**

```python
# Custom validation error handler (optional)
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0] if errors else {}

    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": first_error.get("msg", "Validation failed"),
                "field": ".".join(str(loc) for loc in first_error.get("loc", []))
            }
        }
    )
```

---

## Step 2: Authenticate User

**Responsibility**: Verify JWT and ensure path user_id matches token subject.

```python
# dependencies/auth.py
from dataclasses import dataclass
from typing import Annotated
import jwt
from fastapi import Header, HTTPException, status, Path

from app.config import get_settings


@dataclass
class AuthenticatedUser:
    user_id: str
    email: str


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> AuthenticatedUser:
    """Extract and verify user from JWT."""
    settings = get_settings()

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = parts[1]

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required claims"
            )

        return AuthenticatedUser(user_id=user_id, email=email or "")

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def verify_user_id_matches(
    path_user_id: str,
    current_user: AuthenticatedUser
) -> None:
    """Verify path user_id matches authenticated user."""
    if path_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's chat"
        )
```

**In the router:**

```python
@router.post("/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    # Explicit user_id verification
    verify_user_id_matches(user_id, current_user)
    # ... rest of flow
```

---

## Step 3: Resolve Conversation

**Responsibility**: Load existing conversation or create new one.

```python
# services/conversation_resolver.py
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException, status

from app.crud.conversation import get_conversation, create_conversation
from app.schemas.chat import ChatRequest


async def resolve_conversation(
    session: Session,
    user_id: str,
    request: ChatRequest
) -> str:
    """
    Resolve conversation_id from request.

    If conversation_id provided:
        - Load conversation
        - Verify ownership
        - Return conversation_id

    If conversation_id not provided:
        - Create new conversation
        - Apply system_prompt if provided
        - Return new conversation_id
    """
    if request.conversation_id:
        # Load existing
        conversation = get_conversation(
            session,
            conversation_id=request.conversation_id,
            user_id=user_id
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return conversation.id

    else:
        # Create new
        conversation = create_conversation(
            session,
            user_id=user_id,
            system_prompt=request.system_prompt,
            model_name=request.model
        )

        return conversation.id
```

**Conversation resolution decision tree:**

```
conversation_id provided?
    │
    ├─ YES ─→ Load from DB
    │              │
    │         Found & owned by user?
    │              │
    │              ├─ YES ─→ Return conversation_id
    │              │
    │              └─ NO ──→ 404 Not Found
    │
    └─ NO ──→ Create new conversation
                   │
              Return new conversation_id
```

---

## Step 4: Execute Agent

**Responsibility**: Build context, call agent, persist messages.

```python
# services/agent_executor.py
from datetime import datetime, timezone
from typing import Protocol
from sqlmodel import Session

from app.crud.message import get_messages, add_message
from app.schemas.chat import ChatResponse


class AgentRunner(Protocol):
    """Protocol for agent runner implementations."""

    async def run(
        self,
        messages: list[dict],
        model: str
    ) -> 'AgentResult':
        ...


@dataclass
class AgentResult:
    content: str
    usage: dict | None = None
    finish_reason: str | None = None


async def execute_agent(
    session: Session,
    agent: AgentRunner,
    conversation_id: str,
    user_id: str,
    message: str,
    model: str
) -> ChatResponse:
    """
    Execute agent with full conversation context.

    1. Load conversation history from DB
    2. Format as message list for agent
    3. Append user message
    4. Call agent runner
    5. Persist both messages (user + assistant)
    6. Return structured response
    """
    # 1. Load history
    history = get_messages(session, conversation_id, user_id)

    # 2. Format context
    context = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]

    # 3. Add user message to context (not yet persisted)
    context.append({"role": "user", "content": message})

    # 4. Call agent
    try:
        result = await agent.run(messages=context, model=model)
    except Exception as e:
        # Log error for debugging
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent temporarily unavailable"
        )

    # 5. Persist messages (in transaction)
    now = datetime.now(timezone.utc)

    # Persist user message
    add_message(
        session,
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=message
    )

    # Persist assistant message
    add_message(
        session,
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=result.content,
        metadata={"usage": result.usage} if result.usage else None
    )

    # 6. Return response
    return ChatResponse(
        conversation_id=conversation_id,
        message=result.content,
        role="assistant",
        created_at=now,
        model=model,
        usage=result.usage,
        finish_reason=result.finish_reason
    )
```

**Agent execution sequence:**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTE AGENT                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Load      │    │   Format    │    │   Add User  │     │
│  │   History   │───►│   Context   │───►│   Message   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                               │              │
│                                               ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Return    │    │   Persist   │    │   Call      │     │
│  │   Response  │◄───│   Messages  │◄───│   Agent     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 5: Return Response

**Responsibility**: Format and return the structured response.

```python
# Already handled in execute_agent, but can be separated:

def format_response(
    conversation_id: str,
    agent_result: AgentResult,
    model: str
) -> ChatResponse:
    """Format agent result as API response."""
    return ChatResponse(
        conversation_id=conversation_id,
        message=agent_result.content,
        role="assistant",
        created_at=datetime.now(timezone.utc),
        model=model,
        usage=agent_result.usage,
        finish_reason=agent_result.finish_reason
    )
```

---

## Complete Router Implementation

```python
# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.dependencies.auth import get_current_user, verify_user_id_matches, AuthenticatedUser
from app.services.conversation_resolver import resolve_conversation
from app.services.agent_executor import execute_agent
from app.dependencies.agent import get_agent_runner, AgentRunner
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        403: {"description": "Cannot access another user's chat"},
        404: {"description": "Conversation not found"},
        503: {"description": "Agent unavailable"}
    }
)
async def chat(
    user_id: str,
    request: ChatRequest,  # Step 1: Validated by Pydantic
    current_user: AuthenticatedUser = Depends(get_current_user),  # Step 2a: Auth
    session: Session = Depends(get_session),
    agent: AgentRunner = Depends(get_agent_runner)
):
    """
    Send a chat message and receive AI response.

    Deterministic 5-step flow:
    1. Validate request (Pydantic)
    2. Authenticate user (JWT dependency)
    3. Resolve conversation (create or load)
    4. Execute agent (with context)
    5. Return response
    """
    # Step 2b: Verify user_id matches token
    verify_user_id_matches(user_id, current_user)

    # Step 3: Resolve conversation
    conversation_id = await resolve_conversation(
        session=session,
        user_id=user_id,
        request=request
    )

    # Step 4: Execute agent
    response = await execute_agent(
        session=session,
        agent=agent,
        conversation_id=conversation_id,
        user_id=user_id,
        message=request.message,
        model=request.model or "gpt-4"
    )

    # Step 5: Return response (already formatted)
    return response
```

---

## Idempotency Implementation (Optional)

For safe retries with `request_id`:

```python
from functools import lru_cache
from datetime import datetime, timedelta
import asyncio


class IdempotencyCache:
    """Simple in-memory cache for request deduplication."""

    def __init__(self, ttl_seconds: int = 300):
        self._cache: dict[str, tuple[ChatResponse, datetime]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)
        self._lock = asyncio.Lock()

    async def get(self, request_id: str) -> ChatResponse | None:
        async with self._lock:
            if request_id in self._cache:
                response, created_at = self._cache[request_id]
                if datetime.now() - created_at < self._ttl:
                    return response
                del self._cache[request_id]
        return None

    async def set(self, request_id: str, response: ChatResponse) -> None:
        async with self._lock:
            self._cache[request_id] = (response, datetime.now())


# In router:
idempotency_cache = IdempotencyCache()


@router.post("/{user_id}/chat")
async def chat(...):
    # Check idempotency cache
    if request.request_id:
        cached = await idempotency_cache.get(request.request_id)
        if cached:
            return cached

    # ... normal flow ...

    # Cache response
    if request.request_id:
        await idempotency_cache.set(request.request_id, response)

    return response
```

---

## Testing the Flow

```python
# tests/test_chat_flow.py
import pytest
from fastapi.testclient import TestClient


class TestChatFlow:
    """Test the deterministic chat flow."""

    def test_step1_validates_empty_message(self, client: TestClient, auth_headers):
        response = client.post(
            "/api/user123/chat",
            json={"message": ""},
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_step2_requires_auth(self, client: TestClient):
        response = client.post(
            "/api/user123/chat",
            json={"message": "Hello"}
        )
        assert response.status_code == 401

    def test_step2_forbids_wrong_user(self, client: TestClient, auth_headers_user456):
        response = client.post(
            "/api/user123/chat",  # Different user
            json={"message": "Hello"},
            headers=auth_headers_user456
        )
        assert response.status_code == 403

    def test_step3_creates_new_conversation(self, client: TestClient, auth_headers):
        response = client.post(
            "/api/user123/chat",
            json={"message": "Hello"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "conversation_id" in response.json()

    def test_step3_continues_existing(self, client: TestClient, auth_headers, conversation_id):
        response = client.post(
            "/api/user123/chat",
            json={"message": "Follow up", "conversation_id": conversation_id},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["conversation_id"] == conversation_id

    def test_step3_rejects_unknown_conversation(self, client: TestClient, auth_headers):
        response = client.post(
            "/api/user123/chat",
            json={"message": "Hello", "conversation_id": "nonexistent"},
            headers=auth_headers
        )
        assert response.status_code == 404
```
