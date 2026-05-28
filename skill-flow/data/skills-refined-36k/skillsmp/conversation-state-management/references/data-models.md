# Data Models

Complete SQLModel and Pydantic definitions for conversation state management.

---

## SQLModel Database Models

### Conversation Model

```python
# models/conversation.py
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Conversation(SQLModel, table=True):
    """
    Represents a chat session/thread owned by a user.
    """
    __tablename__ = "conversation"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique conversation identifier"
    )
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        nullable=False,
        description="Owner of this conversation"
    )
    title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional display title"
    )
    system_prompt: Optional[str] = Field(
        default=None,
        description="System message for this conversation"
    )
    model_name: str = Field(
        default="gpt-4",
        max_length=100,
        description="LLM model to use"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Last activity timestamp"
    )
    status: str = Field(
        default="active",
        description="active | archived | deleted"
    )

    # Relationship (optional, for eager loading)
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
# models/message.py
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional, Literal
from sqlmodel import Field, SQLModel, Relationship


class Message(SQLModel, table=True):
    """
    Individual message within a conversation.
    """
    __tablename__ = "message"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique message identifier"
    )
    conversation_id: str = Field(
        foreign_key="conversation.id",
        index=True,
        nullable=False,
        description="Parent conversation"
    )
    role: str = Field(
        nullable=False,
        description="Message role: system, user, or assistant"
    )
    content: str = Field(
        nullable=False,
        description="Message text content"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
        description="Message timestamp for ordering"
    )
    metadata: Optional[dict] = Field(
        default=None,
        sa_type=JSON,
        description="Optional: token_count, model, temperature"
    )

    # Relationship
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
```

### Role Enum (Optional Type Safety)

```python
# models/enums.py
from enum import Enum


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
```

---

## Pydantic Schemas (API Layer)

### Request Schemas

```python
# schemas/conversation.py
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ConversationCreate(BaseModel):
    """Create a new conversation."""
    title: Optional[str] = Field(None, max_length=255)
    system_prompt: Optional[str] = None
    model_name: str = Field(default="gpt-4", max_length=100)


class ConversationUpdate(BaseModel):
    """Update conversation metadata."""
    title: Optional[str] = Field(None, max_length=255)
    status: Optional[Literal["active", "archived"]] = None


class MessageCreate(BaseModel):
    """Add a message to conversation."""
    role: Literal["system", "user", "assistant"] = Field(
        ...,
        description="Message role"
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="Message content"
    )


class UserMessageCreate(BaseModel):
    """Simplified: add user message only."""
    content: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )
```

### Response Schemas

```python
# schemas/conversation.py (continued)
from datetime import datetime
from pydantic import ConfigDict


class MessageResponse(BaseModel):
    """Message in API response."""
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime
    metadata: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(BaseModel):
    """Conversation in API response."""
    id: str
    user_id: str
    title: Optional[str]
    system_prompt: Optional[str]
    model_name: str
    created_at: datetime
    updated_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


class ConversationWithMessages(ConversationResponse):
    """Conversation with full message history."""
    messages: list[MessageResponse] = []
    message_count: int = 0


class ConversationList(BaseModel):
    """Paginated conversation list."""
    items: list[ConversationResponse]
    total: int
    skip: int
    limit: int
```

---

## Database Schema (SQL)

For Neon PostgreSQL:

```sql
-- Conversations table
CREATE TABLE conversation (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(255),
    system_prompt TEXT,
    model_name VARCHAR(100) DEFAULT 'gpt-4',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted'))
);

CREATE INDEX idx_conversation_user_id ON conversation(user_id);
CREATE INDEX idx_conversation_status ON conversation(status);
CREATE INDEX idx_conversation_updated_at ON conversation(updated_at DESC);

-- Messages table
CREATE TABLE message (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('system', 'user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB
);

CREATE INDEX idx_message_conversation_id ON message(conversation_id);
CREATE INDEX idx_message_created_at ON message(created_at);

-- Composite index for fetching messages in order
CREATE INDEX idx_message_conversation_created
    ON message(conversation_id, created_at ASC);
```

---

## Alembic Migration Example

```python
# alembic/versions/xxx_add_conversation_tables.py
"""Add conversation and message tables."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision = 'xxx'
down_revision = 'yyy'


def upgrade():
    op.create_table(
        'conversation',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255)),
        sa.Column('system_prompt', sa.Text),
        sa.Column('model_name', sa.String(100), server_default='gpt-4'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(20), server_default='active'),
    )
    op.create_index('idx_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('idx_conversation_updated_at', 'conversation', ['updated_at'])

    op.create_table(
        'message',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('conversation_id', sa.String(36), sa.ForeignKey('conversation.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('metadata', JSONB),
    )
    op.create_index('idx_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('idx_message_conversation_created', 'message', ['conversation_id', 'created_at'])


def downgrade():
    op.drop_table('message')
    op.drop_table('conversation')
```

---

## Model Registration

```python
# models/__init__.py
from .conversation import Conversation
from .message import Message

__all__ = ["Conversation", "Message"]
```

Ensure models are imported before `SQLModel.metadata.create_all()` is called.
