"""
Database Models for Chat Conversations

SQLModel models for persisting chat conversations and messages.
Enables stateless server architecture with conversation continuity.

Requirements:
    pip install sqlmodel

Usage:
    from models import Conversation, Message
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation (thread).

    Each conversation has a unique thread_id and belongs to a user.
    Metadata can store arbitrary JSON data like conversation settings.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default=None)  # Auto-generated from first message

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Metadata (JSON string)
    metadata: Optional[str] = Field(default=None)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.

    Messages can be from "user" or "assistant" roles.
    Tool calls and their results are also stored.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str = Field(index=True, unique=True)  # UUID
    thread_id: str = Field(foreign_key="conversations.thread_id", index=True)

    # Message content
    role: str = Field(index=True)  # "user", "assistant", "system", "tool"
    content: str

    # Tool call info (optional)
    tool_name: Optional[str] = Field(default=None)
    tool_input: Optional[str] = Field(default=None)  # JSON string
    tool_output: Optional[str] = Field(default=None)  # JSON string

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


# ============================================================================
# Helper Functions
# ============================================================================

from sqlmodel import Session, select
import uuid
import json


def create_conversation(
    session: Session,
    user_id: str,
    thread_id: Optional[str] = None,
    title: Optional[str] = None,
) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(
        thread_id=thread_id or str(uuid.uuid4()),
        user_id=user_id,
        title=title,
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(
    session: Session,
    thread_id: str,
    user_id: Optional[str] = None,
) -> Optional[Conversation]:
    """Get a conversation by thread_id, optionally filtering by user."""
    statement = select(Conversation).where(Conversation.thread_id == thread_id)
    if user_id:
        statement = statement.where(Conversation.user_id == user_id)
    return session.exec(statement).first()


def get_or_create_conversation(
    session: Session,
    thread_id: str,
    user_id: str,
) -> Conversation:
    """Get existing conversation or create new one."""
    conversation = get_conversation(session, thread_id, user_id)
    if not conversation:
        conversation = create_conversation(session, user_id, thread_id)
    return conversation


def add_message(
    session: Session,
    thread_id: str,
    role: str,
    content: str,
    tool_name: Optional[str] = None,
    tool_input: Optional[dict] = None,
    tool_output: Optional[dict] = None,
) -> Message:
    """Add a message to a conversation."""
    message = Message(
        message_id=str(uuid.uuid4()),
        thread_id=thread_id,
        role=role,
        content=content,
        tool_name=tool_name,
        tool_input=json.dumps(tool_input) if tool_input else None,
        tool_output=json.dumps(tool_output) if tool_output else None,
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    # Update conversation timestamp
    conversation = get_conversation(session, thread_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        # Auto-generate title from first user message
        if not conversation.title and role == "user":
            conversation.title = content[:50] + ("..." if len(content) > 50 else "")
        session.add(conversation)
        session.commit()

    return message


def get_messages(
    session: Session,
    thread_id: str,
    limit: int = 100,
    order: str = "asc",
) -> List[Message]:
    """Get messages for a conversation."""
    statement = select(Message).where(Message.thread_id == thread_id)
    if order == "asc":
        statement = statement.order_by(Message.created_at.asc())
    else:
        statement = statement.order_by(Message.created_at.desc())
    statement = statement.limit(limit)
    return session.exec(statement).all()


def get_conversation_history(
    session: Session,
    thread_id: str,
    limit: int = 50,
) -> List[dict]:
    """Get conversation history in chat format."""
    messages = get_messages(session, thread_id, limit=limit)
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def delete_conversation(session: Session, thread_id: str) -> bool:
    """Delete a conversation and all its messages."""
    conversation = get_conversation(session, thread_id)
    if not conversation:
        return False

    # Delete messages first
    messages = get_messages(session, thread_id)
    for msg in messages:
        session.delete(msg)

    # Delete conversation
    session.delete(conversation)
    session.commit()
    return True


def list_conversations(
    session: Session,
    user_id: str,
    limit: int = 20,
    offset: int = 0,
) -> List[Conversation]:
    """List conversations for a user."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


# ============================================================================
# Database Initialization
# ============================================================================

def init_chat_tables(engine):
    """Initialize chat tables in database."""
    SQLModel.metadata.create_all(engine)
