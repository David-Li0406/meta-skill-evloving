# API Contract

Complete request/response schemas and examples for the chat API.

---

## Endpoint Definition

```
POST /api/{user_id}/chat
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID (must match JWT subject) |

---

## Request Schema

### ChatRequest

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ChatRequest(BaseModel):
    """
    Chat API request body.

    Required: message
    Optional: conversation_id, model, system_prompt, request_id
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="User message content"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Existing conversation to continue. Omit to start new."
    )
    model: Optional[str] = Field(
        "gpt-4",
        description="Model identifier"
    )
    system_prompt: Optional[str] = Field(
        None,
        description="System prompt (only used when creating new conversation)"
    )
    request_id: Optional[str] = Field(
        None,
        description="Client-generated UUID for idempotency"
    )
    stream: Optional[bool] = Field(
        False,
        description="Enable streaming response"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "message": "Hello, how can you help me today?",
                    "conversation_id": None,
                    "model": "gpt-4"
                },
                {
                    "message": "Can you explain that in more detail?",
                    "conversation_id": "conv_abc123",
                    "model": "gpt-4"
                }
            ]
        }
```

### Request Examples

**New conversation:**
```json
{
  "message": "Hello, I need help planning a project",
  "model": "gpt-4",
  "system_prompt": "You are a helpful project planning assistant."
}
```

**Continue existing conversation:**
```json
{
  "message": "What about the timeline?",
  "conversation_id": "conv_550e8400-e29b-41d4-a716-446655440000"
}
```

**With idempotency key:**
```json
{
  "message": "Process this important request",
  "conversation_id": "conv_abc123",
  "request_id": "req_xyz789"
}
```

---

## Response Schema

### ChatResponse

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class TokenUsage(BaseModel):
    """Token usage statistics."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """
    Chat API response body.

    Always includes: conversation_id, message, role, created_at
    Optional: usage, model, finish_reason
    """
    conversation_id: str = Field(
        ...,
        description="Conversation ID (use for continuation)"
    )
    message: str = Field(
        ...,
        description="Assistant response content"
    )
    role: Literal["assistant"] = Field(
        "assistant",
        description="Message role (always 'assistant' in response)"
    )
    created_at: datetime = Field(
        ...,
        description="Response timestamp"
    )
    model: Optional[str] = Field(
        None,
        description="Model used for generation"
    )
    usage: Optional[TokenUsage] = Field(
        None,
        description="Token usage statistics"
    )
    finish_reason: Optional[str] = Field(
        None,
        description="Why generation stopped: 'stop', 'length', 'tool_calls'"
    )

    model_config = ConfigDict(from_attributes=True)


class ChatResponseList(BaseModel):
    """Response for listing conversation messages."""
    conversation_id: str
    messages: list[MessageResponse]
    total: int
```

### Response Examples

**Successful response:**
```json
{
  "conversation_id": "conv_550e8400-e29b-41d4-a716-446655440000",
  "message": "I'd be happy to help you plan your project! Let's start by identifying the key objectives. What are the main goals you want to achieve?",
  "role": "assistant",
  "created_at": "2025-01-22T10:30:00Z",
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 45,
    "total_tokens": 195
  },
  "finish_reason": "stop"
}
```

**Minimal response:**
```json
{
  "conversation_id": "conv_abc123",
  "message": "Here's the information you requested...",
  "role": "assistant",
  "created_at": "2025-01-22T10:30:00Z"
}
```

---

## Error Response Schema

### ErrorResponse

```python
from pydantic import BaseModel
from typing import Optional


class ErrorDetail(BaseModel):
    """Structured error detail."""
    code: str
    message: str
    field: Optional[str] = None  # For validation errors


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: ErrorDetail
```

### Error Examples

**Validation error (400):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Message is required",
    "field": "message"
  }
}
```

**Authentication error (401):**
```json
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Valid authentication token required"
  }
}
```

**Authorization error (403):**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Cannot access another user's chat"
  }
}
```

**Not found (404):**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Conversation not found"
  }
}
```

**Agent error (503):**
```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Agent temporarily unavailable. Please retry."
  }
}
```

---

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: Chat API
  version: 1.0.0

paths:
  /api/{user_id}/chat:
    post:
      summary: Send chat message
      description: Send a message and receive AI response
      operationId: chat
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
          description: User ID (must match JWT subject)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatRequest'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChatResponse'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: Authentication required
        '403':
          description: Forbidden
        '404':
          description: Conversation not found
        '503':
          description: Agent unavailable
      security:
        - BearerAuth: []

components:
  schemas:
    ChatRequest:
      type: object
      required:
        - message
      properties:
        message:
          type: string
          minLength: 1
          maxLength: 100000
        conversation_id:
          type: string
          nullable: true
        model:
          type: string
          default: gpt-4
        system_prompt:
          type: string
          nullable: true
        request_id:
          type: string
          nullable: true

    ChatResponse:
      type: object
      required:
        - conversation_id
        - message
        - role
        - created_at
      properties:
        conversation_id:
          type: string
        message:
          type: string
        role:
          type: string
          enum: [assistant]
        created_at:
          type: string
          format: date-time
        model:
          type: string
        usage:
          $ref: '#/components/schemas/TokenUsage'

    TokenUsage:
      type: object
      properties:
        prompt_tokens:
          type: integer
        completion_tokens:
          type: integer
        total_tokens:
          type: integer

    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            field:
              type: string

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

## Streaming Response (Optional)

For streaming responses when `stream: true`:

```python
from fastapi.responses import StreamingResponse
import json


async def stream_chat_response(
    conversation_id: str,
    agent: AgentRunner,
    context: list[dict]
) -> AsyncGenerator[str, None]:
    """Stream chat response as Server-Sent Events."""
    async for chunk in agent.stream(messages=context):
        data = {
            "conversation_id": conversation_id,
            "delta": chunk.content,
            "role": "assistant"
        }
        yield f"data: {json.dumps(data)}\n\n"

    # Final message with usage
    yield f"data: {json.dumps({'done': True})}\n\n"


@router.post("/{user_id}/chat")
async def chat(...):
    if request.stream:
        return StreamingResponse(
            stream_chat_response(conversation_id, agent, context),
            media_type="text/event-stream"
        )
    # ... normal response
```

**Streaming event format:**
```
data: {"conversation_id": "conv_abc", "delta": "Hello", "role": "assistant"}

data: {"conversation_id": "conv_abc", "delta": ", how ", "role": "assistant"}

data: {"conversation_id": "conv_abc", "delta": "can I help?", "role": "assistant"}

data: {"done": true, "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
```

---

## Client Usage Examples

### Python (httpx)

```python
import httpx

async def chat(token: str, user_id: str, message: str, conversation_id: str = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.example.com/api/{user_id}/chat",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "message": message,
                "conversation_id": conversation_id
            }
        )
        response.raise_for_status()
        return response.json()
```

### TypeScript (fetch)

```typescript
interface ChatRequest {
  message: string;
  conversation_id?: string;
  model?: string;
}

interface ChatResponse {
  conversation_id: string;
  message: string;
  role: 'assistant';
  created_at: string;
}

async function chat(
  token: string,
  userId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error.message);
  }

  return response.json();
}
```
