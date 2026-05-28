"""
Chat Router Template for ChatKit Backend

A FastAPI router that provides a chat endpoint compatible with ChatKit frontend.
Uses OpenAI Agents SDK with Gemini via LiteLLM and connects to MCP server for tools.

Requirements:
    pip install fastapi sse-starlette "openai-agents[litellm]"

Environment:
    GOOGLE_API_KEY=your-gemini-api-key
    MCP_SERVER_URL=http://localhost:8000/api/mcp (optional)

Usage:
    # In your main.py:
    from routes.chat import router as chat_router
    app.include_router(chat_router, prefix="/api")
"""

import os
import json
import uuid
from datetime import datetime
from typing import AsyncGenerator, List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from sqlmodel import Session, select

from agents import Agent, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from agents.extensions.models.litellm_model import LitellmModel
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

# Disable OpenAI tracing
set_tracing_disabled(disabled=True)

# Import from your app (adjust paths as needed)
# from database import engine, get_session
# from models import Conversation, Message
# from auth import get_current_user

router = APIRouter(tags=["chat"])


# ============================================================================
# Configuration
# ============================================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/api/mcp")
print(f"MCP_SERVER_URL: {MCP_SERVER_URL}")


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request from ChatKit frontend."""
    messages: List[ChatMessage]
    thread_id: Optional[str] = None
    user_id: Optional[str] = None
    model: Optional[str] = None  # Optional model selection


class ChatResponse(BaseModel):
    """Non-streaming chat response."""
    content: str
    thread_id: str
    message_id: str


# ============================================================================
# Agent Setup
# ============================================================================

AGENT_INSTRUCTIONS = prompt_with_handoff_instructions("""
You are a helpful task management assistant.

## Your Capabilities
Use MCP tools to help users manage tasks:
- **add_task**: Create new tasks (title, description, priority, due_date)
- **list_tasks**: View tasks (filter by status, priority)
- **complete_task**: Mark tasks as completed
- **delete_task**: Remove tasks
- **update_task**: Modify task details

## Guidelines
1. Always confirm actions after performing them
2. Format task lists nicely with bullet points
3. Include task IDs when relevant
4. Be concise but helpful
5. Ask for clarification if needed
""")


def create_agent(user_id: str, mcp_server=None) -> Agent:
    """Create an agent for the given user."""
    instructions = AGENT_INSTRUCTIONS + f"\n\nCurrent user ID: {user_id}"

    return Agent(
        name="Todo Assistant",
        instructions=instructions,
        model=LitellmModel(
            model="gemini/gemini-2.0-flash",
            api_key=GOOGLE_API_KEY,
        ),
        mcp_servers=[mcp_server] if mcp_server else [],
    )


# ============================================================================
# Streaming Response Generator
# ============================================================================

async def stream_chat_response(
    agent: Agent,
    user_message: str,
    thread_id: str,
) -> AsyncGenerator[str, None]:
    """
    Stream chat response as Server-Sent Events.

    Event format:
    - Content: data: {"content": "text"}
    - Done: data: {"done": true, "thread_id": "..."}
    - Error: data: {"error": "message"}
    """
    try:
        # Run agent with streaming
        result = Runner.run_streamed(agent, user_message)

        # Stream content as it arrives
        current_content = ""
        async for event in result.stream_events():
            if hasattr(event, 'item') and event.item:
                chunk = str(event.item)
                current_content += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"

        # If no streaming content, yield final output
        if not current_content and result.final_output:
            yield f"data: {json.dumps({'content': result.final_output})}\n\n"

        # Signal completion
        yield f"data: {json.dumps({'done': True, 'thread_id': thread_id})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


# ============================================================================
# Chat Endpoint (Streaming)
# ============================================================================

@router.post("/chat")
async def chat_streaming(
    request: ChatRequest,
    # user: dict = Depends(get_current_user),  # Uncomment for auth
):
    """
    Chat endpoint with SSE streaming response.

    Accepts messages from ChatKit frontend and returns streaming response.
    """
    if not GOOGLE_API_KEY:
        raise HTTPException(500, "GOOGLE_API_KEY not configured")

    if not request.messages:
        raise HTTPException(400, "No messages provided")

    # Get user ID from request or auth
    user_id = request.user_id or "anonymous"
    # user_id = user.get("id", "anonymous")  # Use with auth

    # Get or create thread ID
    thread_id = request.thread_id or str(uuid.uuid4())

    # Get the last user message
    user_message = request.messages[-1].content
    if request.messages[-1].role != "user":
        raise HTTPException(400, "Last message must be from user")

    # Connect to MCP server and create agent
    try:
        async with MCPServerStreamableHttp(
            name="Todo MCP",
            params={"url": MCP_SERVER_URL, "timeout": 30},
            cache_tools_list=True,
        ) as mcp_server:
            agent = create_agent(user_id, mcp_server)

            return EventSourceResponse(
                stream_chat_response(agent, user_message, thread_id),
                media_type="text/event-stream",
            )

    except ConnectionError:
        # Fallback: run without MCP if server unavailable
        agent = create_agent(user_id, None)
        return EventSourceResponse(
            stream_chat_response(agent, user_message, thread_id),
            media_type="text/event-stream",
        )


# ============================================================================
# Chat Endpoint (Non-Streaming)
# ============================================================================

@router.post("/chat/sync", response_model=ChatResponse)
async def chat_sync(
    request: ChatRequest,
    # user: dict = Depends(get_current_user),  # Uncomment for auth
):
    """
    Non-streaming chat endpoint.

    Returns complete response as JSON (for simple integrations).
    """
    if not GOOGLE_API_KEY:
        raise HTTPException(500, "GOOGLE_API_KEY not configured")

    if not request.messages:
        raise HTTPException(400, "No messages provided")

    user_id = request.user_id or "anonymous"
    thread_id = request.thread_id or str(uuid.uuid4())
    user_message = request.messages[-1].content

    try:
        async with MCPServerStreamableHttp(
            name="Todo MCP",
            params={"url": MCP_SERVER_URL, "timeout": 30},
            cache_tools_list=True,
        ) as mcp_server:
            agent = create_agent(user_id, mcp_server)
            result = await Runner.run(agent, user_message)

            return ChatResponse(
                content=result.final_output,
                thread_id=thread_id,
                message_id=str(uuid.uuid4()),
            )

    except Exception as e:
        raise HTTPException(500, f"Chat error: {e}")


# ============================================================================
# Health Check
# ============================================================================

@router.get("/chat/health")
async def chat_health():
    """Health check for chat service."""
    return {
        "status": "healthy",
        "google_api_configured": bool(GOOGLE_API_KEY),
        "mcp_server_url": MCP_SERVER_URL,
    }
