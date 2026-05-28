# API Patterns

CRUD operations and router implementations for conversation state management.

---

## CRUD Operations

### Conversation CRUD

```python
# crud/conversation.py
from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import Session, select, func
from typing import Optional

from app.models import Conversation, Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate


def create_conversation(
    session: Session,
    user_id: str,
    data: ConversationCreate
) -> Conversation:
    """Create a new conversation for user."""
    conversation = Conversation(
        id=str(uuid4()),
        user_id=user_id,
        title=data.title,
        system_prompt=data.system_prompt,
        model_name=data.model_name,
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # If system prompt provided, add as first message
    if data.system_prompt:
        add_message(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="system",
            content=data.system_prompt,
            skip_validation=True  # System message at creation is allowed
        )

    return conversation


def get_conversation(
    session: Session,
    conversation_id: str,
    user_id: str
) -> Optional[Conversation]:
    """
    Get conversation by ID with ownership check.
    Returns None if not found OR not owned by user.
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
        Conversation.status != "deleted"
    )
    return session.exec(statement).first()


def list_conversations(
    session: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 20,
    status: str = "active"
) -> tuple[list[Conversation], int]:
    """List user's conversations with pagination."""
    base_query = select(Conversation).where(
        Conversation.user_id == user_id,
        Conversation.status == status
    )

    # Get total count
    count_stmt = select(func.count()).select_from(base_query.subquery())
    total = session.exec(count_stmt).one()

    # Get paginated results
    statement = base_query.order_by(
        Conversation.updated_at.desc()
    ).offset(skip).limit(limit)

    conversations = session.exec(statement).all()
    return list(conversations), total


def update_conversation(
    session: Session,
    conversation_id: str,
    user_id: str,
    data: ConversationUpdate
) -> Optional[Conversation]:
    """Update conversation metadata."""
    conversation = get_conversation(session, conversation_id, user_id)
    if not conversation:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(conversation, key, value)

    conversation.updated_at = datetime.now(timezone.utc)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def delete_conversation(
    session: Session,
    conversation_id: str,
    user_id: str,
    hard_delete: bool = False
) -> bool:
    """
    Delete conversation (soft delete by default).
    Returns True if deleted, False if not found.
    """
    conversation = get_conversation(session, conversation_id, user_id)
    if not conversation:
        return False

    if hard_delete:
        session.delete(conversation)  # Cascades to messages
    else:
        conversation.status = "deleted"
        conversation.updated_at = datetime.now(timezone.utc)
        session.add(conversation)

    session.commit()
    return True
```

### Message CRUD

```python
# crud/message.py
from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import Session, select
from typing import Optional

from app.models import Conversation, Message


class RoleOrderingError(Exception):
    """Raised when message role violates ordering rules."""
    pass


def validate_role_sequence(
    existing_messages: list[Message],
    new_role: str
) -> bool:
    """
    Validate that new_role follows ordering rules.

    Rules:
    - system: only at start (when no messages exist)
    - After system (if any): must be user
    - Then: strict user ↔ assistant alternation
    """
    if not existing_messages:
        return new_role in ("system", "user")

    last_role = existing_messages[-1].role

    if new_role == "system":
        return False  # System only allowed at start

    if last_role == "system":
        return new_role == "user"

    # Must alternate
    if last_role == "user":
        return new_role == "assistant"
    if last_role == "assistant":
        return new_role == "user"

    return False


def add_message(
    session: Session,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str,
    skip_validation: bool = False,
    metadata: Optional[dict] = None
) -> Message:
    """
    Add message to conversation with role validation.

    Raises:
        RoleOrderingError: If role violates sequence rules
        ValueError: If conversation not found or not owned
    """
    # Verify ownership
    conv_stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = session.exec(conv_stmt).first()
    if not conversation:
        raise ValueError("Conversation not found")

    # Get existing messages for validation
    if not skip_validation:
        existing = get_messages(session, conversation_id, user_id)
        if not validate_role_sequence(existing, role):
            last_role = existing[-1].role if existing else "none"
            raise RoleOrderingError(
                f"Invalid role sequence: cannot add '{role}' after '{last_role}'"
            )

    # Create message
    message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata=metadata
    )
    session.add(message)

    # Update conversation timestamp
    conversation.updated_at = datetime.now(timezone.utc)
    session.add(conversation)

    session.commit()
    session.refresh(message)
    return message


def get_messages(
    session: Session,
    conversation_id: str,
    user_id: str,
    limit: Optional[int] = None
) -> list[Message]:
    """
    Get messages for conversation, ordered by created_at.
    Verifies user ownership.
    """
    # Verify ownership first
    conv_stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = session.exec(conv_stmt).first()
    if not conversation:
        return []

    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc())

    if limit:
        statement = statement.limit(limit)

    return list(session.exec(statement).all())


def get_last_message(
    session: Session,
    conversation_id: str,
    user_id: str
) -> Optional[Message]:
    """Get the most recent message in conversation."""
    messages = get_messages(session, conversation_id, user_id)
    return messages[-1] if messages else None


def get_message_count(
    session: Session,
    conversation_id: str
) -> int:
    """Get total message count for conversation."""
    from sqlmodel import func
    statement = select(func.count(Message.id)).where(
        Message.conversation_id == conversation_id
    )
    return session.exec(statement).one()
```

---

## Router Implementation

```python
# routers/conversations.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.dependencies.auth import get_current_user, AuthenticatedUser
from app.crud import conversation as conv_crud
from app.crud.message import add_message, get_messages, RoleOrderingError
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages,
    ConversationList,
    MessageCreate,
    MessageResponse,
    UserMessageCreate,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


# ============== Conversation Endpoints ==============

@router.post("", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Create a new conversation."""
    conversation = conv_crud.create_conversation(
        session=session,
        user_id=user.user_id,
        data=data
    )
    return conversation


@router.get("", response_model=ConversationList)
async def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query("active"),
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List user's conversations with pagination."""
    conversations, total = conv_crud.list_conversations(
        session=session,
        user_id=user.user_id,
        skip=skip,
        limit=limit,
        status=status
    )
    return ConversationList(
        items=conversations,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get conversation with all messages."""
    conversation = conv_crud.get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user.user_id
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = get_messages(session, conversation_id, user.user_id)

    return ConversationWithMessages(
        **conversation.model_dump(),
        messages=messages,
        message_count=len(messages)
    )


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    data: ConversationUpdate,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Update conversation metadata."""
    conversation = conv_crud.update_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user.user_id,
        data=data
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Delete (archive) conversation."""
    deleted = conv_crud.delete_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user.user_id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")


# ============== Message Endpoints ==============

@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=201
)
async def create_message(
    conversation_id: str,
    data: MessageCreate,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Add a message to conversation with role validation."""
    try:
        message = add_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user.user_id,
            role=data.role,
            content=data.content
        )
        return message
    except ValueError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except RoleOrderingError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
async def list_messages(
    conversation_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get all messages in conversation, ordered by time."""
    # Verify conversation exists and is owned
    conversation = conv_crud.get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user.user_id
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return get_messages(session, conversation_id, user.user_id)
```

---

## Router Registration

```python
# main.py
from fastapi import FastAPI
from app.routers import conversations

app = FastAPI()

app.include_router(conversations.router, prefix="/api/v1")
```

---

## Error Responses

| Status | When | Response Body |
|--------|------|---------------|
| 400 | Role ordering violation | `{"detail": "Invalid role sequence: cannot add 'user' after 'user'}` |
| 404 | Conversation not found OR not owned | `{"detail": "Conversation not found"}` |
| 422 | Validation error | Pydantic validation errors |

**Security note**: Always return 404 (not 403) when resource exists but isn't owned by requester. This prevents enumeration attacks.

---

## Context Helper for LLM Integration

```python
# crud/context.py
from sqlmodel import Session
from app.crud.message import get_messages


def get_conversation_context(
    session: Session,
    conversation_id: str,
    user_id: str
) -> list[dict]:
    """
    Fetch conversation history formatted for LLM API.

    Returns list of {"role": str, "content": str} dicts.
    """
    messages = get_messages(session, conversation_id, user_id)
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def get_recent_context(
    session: Session,
    conversation_id: str,
    user_id: str,
    max_messages: int = 20
) -> list[dict]:
    """
    Fetch recent messages for context window management.
    Always includes system message if present.
    """
    messages = get_messages(session, conversation_id, user_id)

    if not messages:
        return []

    # Always include system message if exists
    result = []
    if messages[0].role == "system":
        result.append({"role": "system", "content": messages[0].content})
        messages = messages[1:]

    # Take last N messages
    recent = messages[-max_messages:] if len(messages) > max_messages else messages

    result.extend([
        {"role": msg.role, "content": msg.content}
        for msg in recent
    ])

    return result
```
