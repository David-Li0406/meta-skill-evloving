# Resume Patterns

Checkpoint and continuation strategies for resuming conversations after server restart.

---

## Core Principle

**Stateless Resume**: Since all state is in the database, "resuming" is simply loading the conversation again.

```
Server restart → User makes request → Load conversation from DB → Continue
```

No special recovery logic needed for basic resume.

---

## Basic Resume Pattern

### Load and Continue

```python
# crud/context.py
from sqlmodel import Session
from app.crud.conversation import get_conversation
from app.crud.message import get_messages, add_message


def resume_conversation(
    session: Session,
    conversation_id: str,
    user_id: str
) -> dict:
    """
    Resume a conversation - returns current state.
    """
    conversation = get_conversation(session, conversation_id, user_id)
    if not conversation:
        return None

    messages = get_messages(session, conversation_id, user_id)

    return {
        "conversation": conversation,
        "messages": messages,
        "message_count": len(messages),
        "last_role": messages[-1].role if messages else None,
        "can_add_user": not messages or messages[-1].role in ("system", "assistant"),
        "can_add_assistant": messages and messages[-1].role == "user"
    }


def continue_conversation(
    session: Session,
    conversation_id: str,
    user_id: str,
    user_message: str,
    llm_client  # Your LLM client
) -> dict:
    """
    Continue conversation with new user message.
    Handles the full cycle: load → add message → call LLM → persist response.
    """
    # Load existing context
    context = get_conversation_context(session, conversation_id, user_id)

    # Add user message
    add_message(session, conversation_id, user_id, "user", user_message)
    context.append({"role": "user", "content": user_message})

    # Call LLM
    response = llm_client.generate(messages=context)

    # Persist assistant response
    add_message(session, conversation_id, user_id, "assistant", response)

    return {
        "response": response,
        "conversation_id": conversation_id
    }
```

### API Endpoint

```python
# routers/conversations.py
from app.schemas.conversation import UserMessageCreate, ContinueResponse


@router.post("/{conversation_id}/continue", response_model=ContinueResponse)
async def continue_conversation_endpoint(
    conversation_id: str,
    data: UserMessageCreate,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
    llm: LLMClient = Depends(get_llm_client)
):
    """
    Continue conversation with a new user message.
    Loads history, calls LLM, persists response.
    """
    result = continue_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user.user_id,
        user_message=data.content,
        llm_client=llm
    )
    if not result:
        raise HTTPException(404, "Conversation not found")
    return result
```

---

## Checkpoint Pattern (For Long Conversations)

When conversations get very long, use checkpoints to manage context window.

### Checkpoint Model

```python
# models/checkpoint.py
from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import Field, SQLModel


class ConversationCheckpoint(SQLModel, table=True):
    """
    Snapshot of conversation state at a point in time.
    Used for efficient resume of long conversations.
    """
    __tablename__ = "conversation_checkpoint"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    message_count: int = Field(description="Messages at checkpoint time")
    summary: str = Field(description="Compressed summary of prior messages")
    checkpoint_message_id: str = Field(description="Message ID at checkpoint")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### Create Checkpoint

```python
# crud/checkpoint.py
from sqlmodel import Session, select
from app.models import ConversationCheckpoint, Message


def create_checkpoint(
    session: Session,
    conversation_id: str,
    user_id: str,
    summary: str,
    at_message_id: str
) -> ConversationCheckpoint:
    """
    Create a checkpoint summarizing conversation up to a message.
    """
    # Verify ownership
    messages = get_messages(session, conversation_id, user_id)
    if not messages:
        raise ValueError("Conversation not found or empty")

    # Find message index
    message_ids = [m.id for m in messages]
    if at_message_id not in message_ids:
        raise ValueError("Message not found in conversation")

    checkpoint = ConversationCheckpoint(
        conversation_id=conversation_id,
        message_count=message_ids.index(at_message_id) + 1,
        summary=summary,
        checkpoint_message_id=at_message_id
    )
    session.add(checkpoint)
    session.commit()
    session.refresh(checkpoint)
    return checkpoint


def get_latest_checkpoint(
    session: Session,
    conversation_id: str
) -> ConversationCheckpoint | None:
    """Get the most recent checkpoint for a conversation."""
    statement = select(ConversationCheckpoint).where(
        ConversationCheckpoint.conversation_id == conversation_id
    ).order_by(ConversationCheckpoint.created_at.desc()).limit(1)
    return session.exec(statement).first()
```

### Resume with Checkpoint

```python
def get_context_with_checkpoint(
    session: Session,
    conversation_id: str,
    user_id: str,
    max_recent_messages: int = 20
) -> list[dict]:
    """
    Get conversation context, using checkpoint summary for older messages.

    Returns:
        List of messages formatted for LLM, with summary prepended if needed.
    """
    messages = get_messages(session, conversation_id, user_id)

    if len(messages) <= max_recent_messages:
        # Short conversation, return all
        return [{"role": m.role, "content": m.content} for m in messages]

    # Long conversation, check for checkpoint
    checkpoint = get_latest_checkpoint(session, conversation_id)

    result = []

    # Include system message if present
    if messages[0].role == "system":
        result.append({"role": "system", "content": messages[0].content})
        messages = messages[1:]

    if checkpoint:
        # Add summary as system context
        result.append({
            "role": "system",
            "content": f"[Previous conversation summary: {checkpoint.summary}]"
        })
        # Get messages after checkpoint
        checkpoint_idx = next(
            (i for i, m in enumerate(messages) if m.id == checkpoint.checkpoint_message_id),
            0
        )
        messages = messages[checkpoint_idx + 1:]

    # Take recent messages
    recent = messages[-max_recent_messages:]
    result.extend([{"role": m.role, "content": m.content} for m in recent])

    return result
```

---

## Auto-Summarization

Automatically create checkpoints when conversation reaches threshold.

```python
# services/summarization.py
from app.crud.message import get_messages
from app.crud.checkpoint import create_checkpoint


CHECKPOINT_THRESHOLD = 50  # Messages before creating checkpoint


async def maybe_create_checkpoint(
    session: Session,
    conversation_id: str,
    user_id: str,
    llm_client
) -> ConversationCheckpoint | None:
    """
    Create checkpoint if conversation is long enough.
    Called after adding messages.
    """
    messages = get_messages(session, conversation_id, user_id)

    if len(messages) < CHECKPOINT_THRESHOLD:
        return None

    # Check if recent checkpoint exists
    latest = get_latest_checkpoint(session, conversation_id)
    if latest and len(messages) - latest.message_count < CHECKPOINT_THRESHOLD // 2:
        return None  # Too soon for new checkpoint

    # Determine messages to summarize (all except last 10)
    to_summarize = messages[:-10]
    summarize_until = to_summarize[-1]

    # Generate summary using LLM
    summary_prompt = [
        {"role": "system", "content": "Summarize this conversation concisely, preserving key information, decisions, and context needed for continuation."},
        *[{"role": m.role, "content": m.content} for m in to_summarize]
    ]
    summary = await llm_client.generate(messages=summary_prompt, max_tokens=500)

    return create_checkpoint(
        session=session,
        conversation_id=conversation_id,
        user_id=user_id,
        summary=summary,
        at_message_id=summarize_until.id
    )
```

---

## Recovery from Interruption

Handle cases where a request was interrupted mid-processing.

### Track Request State

```python
# models/conversation.py - add to Conversation model
class Conversation(SQLModel, table=True):
    # ... existing fields ...

    # Request tracking
    pending_request_id: str | None = Field(
        default=None,
        description="ID of in-flight request, if any"
    )
    pending_request_at: datetime | None = Field(
        default=None,
        description="When pending request started"
    )
```

### Idempotent Processing

```python
from uuid import uuid4
from datetime import datetime, timezone, timedelta


REQUEST_TIMEOUT = timedelta(minutes=5)


def start_request(
    session: Session,
    conversation_id: str,
    user_id: str
) -> str:
    """Mark conversation as having in-flight request."""
    conversation = get_conversation(session, conversation_id, user_id)
    if not conversation:
        raise ValueError("Conversation not found")

    # Check for stale pending request
    if conversation.pending_request_id:
        if conversation.pending_request_at:
            elapsed = datetime.now(timezone.utc) - conversation.pending_request_at
            if elapsed < REQUEST_TIMEOUT:
                raise ValueError("Request already in progress")
        # Stale request, clear it

    request_id = str(uuid4())
    conversation.pending_request_id = request_id
    conversation.pending_request_at = datetime.now(timezone.utc)
    session.add(conversation)
    session.commit()
    return request_id


def complete_request(
    session: Session,
    conversation_id: str,
    request_id: str
) -> None:
    """Clear pending request on completion."""
    conversation = session.get(Conversation, conversation_id)
    if conversation and conversation.pending_request_id == request_id:
        conversation.pending_request_id = None
        conversation.pending_request_at = None
        session.add(conversation)
        session.commit()


# Usage in endpoint
@router.post("/{conversation_id}/continue")
async def continue_endpoint(...):
    request_id = start_request(session, conversation_id, user.user_id)
    try:
        # Process request...
        result = await process_message(...)
        return result
    finally:
        complete_request(session, conversation_id, request_id)
```

---

## Resume Status Endpoint

Provide conversation state for client-side resume UI.

```python
# schemas/conversation.py
class ResumeStatus(BaseModel):
    conversation_id: str
    title: str | None
    message_count: int
    last_message_preview: str | None
    last_role: str | None
    last_activity: datetime
    can_continue: bool
    has_pending_request: bool


@router.get("/{conversation_id}/status", response_model=ResumeStatus)
async def get_resume_status(
    conversation_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get conversation status for resume UI."""
    conversation = get_conversation(session, conversation_id, user.user_id)
    if not conversation:
        raise HTTPException(404, "Conversation not found")

    messages = get_messages(session, conversation_id, user.user_id)
    last_message = messages[-1] if messages else None

    return ResumeStatus(
        conversation_id=conversation_id,
        title=conversation.title,
        message_count=len(messages),
        last_message_preview=last_message.content[:100] if last_message else None,
        last_role=last_message.role if last_message else None,
        last_activity=conversation.updated_at,
        can_continue=not last_message or last_message.role in ("system", "assistant"),
        has_pending_request=conversation.pending_request_id is not None
    )
```

---

## Session Switching (Multi-Device)

Since state is in DB, users can switch devices seamlessly.

```python
@router.get("/active", response_model=list[ConversationResponse])
async def get_active_conversations(
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Get user's active conversations.
    Useful for resume UI showing recent/ongoing conversations.
    """
    conversations, _ = list_conversations(
        session=session,
        user_id=user.user_id,
        limit=10,
        status="active"
    )
    return conversations
```

The user can:
1. Start conversation on desktop
2. Close browser
3. Open app on phone
4. Call `/conversations/active` to see ongoing conversations
5. Select one to continue
6. Load full history and continue seamlessly
