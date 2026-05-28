---
name: chatkit-server-integration
description: This skill provides functionality to properly expose a ChatKit server via FastAPI routes. It handles the integration between FastAPI request/response cycle and the ChatKit server, with proper request processing and response handling.
---

## ChatKit Server Integration Skill

## Description
This skill provides functionality to properly expose a ChatKit server via FastAPI routes. It handles the integration between FastAPI request/response cycle and the ChatKit server, with proper request processing and response handling.

## Parameters
- `route_path` (string): The path for the FastAPI route (default: "/chat")

## Precondition
- FastAPI application instance available
- ChatKit server instance properly configured

## Execution
1. Creates a FastAPI POST route at the specified path
2. Gets raw payload from request body
3. Processes the payload using the ChatKit server with proper context
4. Returns appropriate response based on result type (streaming or regular)

## Example Usage

```python
from fastapi import APIRouter
from chatkit.server import StreamingResult
from src.services.chatkit_server import chatkit_server

router = APIRouter()

@router.post("/chat", response_class=Response)
async def chat_endpoint(request: Request):
    # Get raw payload
    payload = await request.body()

    # Process with ChatKit server
    context = {"request": request}
    result = await chatkit_server.process(payload, context)

    # Return appropriate response
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

## Postcondition
- FastAPI route is properly registered with ChatKit server integration
- Request/response cycle is properly managed between FastAPI and ChatKit
- Both streaming and regular responses are supported
