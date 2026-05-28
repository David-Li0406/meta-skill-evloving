---
name: chatkit-store-creator
description: This skill helps create ChatKit store implementations with database integration, following best practices and avoiding common errors we've solved in previous implementations.
---

# ChatKit Store Creator

This skill helps create ChatKit store implementations with database integration, following best practices and avoiding common errors we've solved in previous implementations.

## Usage Instructions

When a user needs to create a ChatKit store with database integration, use this skill to generate:

1. Store class extending the base ChatKit Store interface
2. Proper database connection and connection pooling
3. All required abstract methods implementation
4. Error handling for database operations
5. Type-safe implementations for ChatKit types

## Common Errors to Avoid (Based on Previous Solutions)

1. **Abstract Method Implementation Error**: "Cannot instantiate abstract class 'Store' - Abstract methods not implemented"
   - Solution: Implement ALL required abstract methods from the Store interface

2. **Configuration Access Error**: "AttributeError: 'Config' object has no attribute 'NEON_DATABASE_URL'"
   - Solution: Access settings correctly using the settings instance, not the Config class

3. **Content Part Type Error**: Using incorrect content types like MessageContentPart
   - Solution: Use correct ChatKit types like UserMessageContent and AssistantMessageContent

4. **Connection Pool Error**: "acquire" is not a known attribute of "None"
   - Solution: Ensure connection pool is initialized before use

5. **Type Mismatch Error**: "Argument of type 'int' cannot be assigned to parameter 'object' of type 'str'"
   - Solution: Cast parameters to correct types when appending to query parameters

6. **ThreadMetadata Error**: "No parameter named 'updated_at'"
   - Solution: Use metadata field instead: metadata={"updated_at": value}

7. **Type Annotation Error**: "Type of parameter 'context' is partially unknown" or "Parameter type is 'dict[Unknown, Unknown]'"
   - Solution: Use proper type annotations like `Dict[str, Any]` for the Store generic and context parameters instead of just `dict`

8. **UUID Generation Inconsistency**: Inconsistent ID generation patterns between `generate_thread_id` and `generate_item_id` methods
   - Solution: Use consistent UUID generation with `str(uuid.uuid4())` for both methods

9. **Append Method Type Error**: "Type of 'append' is partially unknown" or "Type of 'append' is '(object: Unknown, /) -> None'"
   - Solution: Always use proper type annotations for lists before using the append method, e.g., `items: List[ThreadItem] = []` or `thread_metadata_list: List[ThreadMetadata] = []`

10. **ThreadItem Content Access Error**: Issues when accessing content from ThreadItem without checking item type first
   - Solution: Use the type property to check item type before accessing content: `if (item.type == "user_message" or item.type == "assistant_message") and item.content:`

11. **Missing Abstract Method Error**: "Cannot instantiate abstract class 'Store' - Abstract method delete_thread_item not implemented"
   - Solution: Always implement ALL abstract methods from the Store interface, including `delete_thread_item(self, thread_id: str, item_id: str, context: TContext) -> None`

12. **Type Mismatch in Constructor Error**: Issues with required parameters like "thread_id", "inference_options", etc.
   - Solution: Ensure all required parameters are provided to constructors; for UserMessageItem and AssistantMessageItem, provide: thread_id, content (list of appropriate content types), created_at, and inference_options (InferenceOptions())

13. **Content Type Mismatch Error**: Using wrong content type literals like "text" instead of "input_text"/"output_text"
   - Solution: Use correct type literals: UserMessageTextContent(type="input_text", ...) and AssistantMessageContent(type="output_text", ...)

14. **Import Organization Error**: Local imports causing issues
   - Solution: Move all imports to the top level of the file, including datetime, uuid, and SQLModel functions like asc, desc

15. **SQLModel Order By Error**: Issues with order_by syntax
   - Solution: Use proper SQLModel syntax: `.order_by(asc(ColumnName))` and `.order_by(desc(ColumnName))` instead of `.order_by(ColumnName.asc())`

16. **Pre-Completion Error Checking**: Always verify your implementation before declaring it complete
   - Solution: Before marking the implementation as done, check for: missing abstract methods, type mismatches, incorrect content types, import issues, and proper SQL syntax

## Template Structure

### Complete Store Implementation Template:
```python
import asyncpg
from typing import Optional, List, Dict, Any
import uuid
import logging
from chatkit.store import Store, StoreItemType
from chatkit.types import ThreadMetadata, ThreadItem, Attachment, Page, UserMessageItem, AssistantMessageItem, InferenceOptions, AssistantMessageContent, UserMessageTextContent
from src.config import settings  # Import the settings instance, not the Config class

# Set up logging
logger = logging.getLogger(__name__)

class YourStoreName(Store[TContext]):
    """Store implementation using PostgreSQL database for message and attachment persistence."""

    def __init__(self):
        self.connection_string = settings.your_database_url  # Access settings correctly

    async def connect(self):
        """Establish connection to the database."""

    async def _initialize_tables(self):
        """Create required tables if they don't exist."""
        if not self.pool:
            await self.connect()

        # Verify the pool is not None after connecting
        if not self.pool:
            raise RuntimeError("Failed to establish database connection pool")


    # Implement ALL abstract methods from Store class
    async def load_thread(self, thread_id: str, context: TContext) -> ThreadMetadata:
        """Load a thread by its ID."""

    async def save_thread(self, thread: ThreadMetadata, context: TContext) -> None:
        """Save a thread."""

    async def load_thread_items(self, thread_id: str, after: str | None, limit: int, order: str, context: TContext) -> Page[ThreadItem]:
        """Load items for a specific thread."""


    async def save_attachment(self, attachment: Attachment, context: TContext) -> None:
        """Save an attachment."""

    async def load_attachment(self, attachment_id: str, context: TContext) -> Attachment:
        """Load an attachment by ID."""

    async def delete_attachment(self, attachment_id: str, context: TContext) -> None:
        """Delete an attachment by ID."""

    async def load_threads(self, limit: int, after: str | None, order: str, context: TContext) -> Page[ThreadMetadata]:
        """Load multiple threads."""

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: TContext) -> None:
        """Add an item to a thread."""

    async def save_item(self, thread_id: str, item: ThreadItem, context: TContext) -> None:
        """Save an item to a thread (alternative to add_thread_item)."""

    async def load_item(self, thread_id: str, item_id: str, context: TContext) -> ThreadItem:
        """Load a specific item from a thread."""

    def generate_thread_id(self, context: TContext) -> str:
        """Generate a new thread ID."""

    def generate_item_id(self, item_type: StoreItemType, thread: ThreadMetadata, context: TContext) -> str:
        """Generate a new item ID."""

    async def delete_thread(self, thread_id: str, context: TContext) -> None:
        """Delete a thread by its ID."""

    # Helper methods for compatibility with original implementation
    async def save_message(self, thread_id: str, content: str, sender_type: str) -> str:
        """Save a message to the database.

        Args:
            thread_id: The ID of the thread the message belongs to
            content: The content of the message
            sender_type: The type of sender ('user' or 'agent')

        Returns:
            The ID of the saved message
        """

    async def get_thread_messages(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a specific thread.

        Args:
            thread_id: The ID of the thread to retrieve messages for

        Returns:
            List of messages in the thread
        """

    async def create_thread(self, title: Optional[str] = None) -> str:
        """Create a new conversation thread.

        Args:
            title: Optional title for the thread

        Returns:
            The ID of the created thread
        """

    async def get_thread(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific thread by ID.

        Args:
            thread_id: The ID of the thread to retrieve

        Returns:
            Thread information or None if not found
        """
    async def close(self):
        """Close the database connection pool."""
```

## Key Implementation Points

- **All Abstract Methods**: Implements ALL required abstract methods from the Store interface
- **Configuration Access**: Uses the settings instance correctly, not the Config class
- **Type Safety**: Uses correct ChatKit types like UserMessageContent and AssistantMessageContent
- **Connection Handling**: Ensures connection pool is initialized before database operations
- **Type Casting**: Properly casts parameters to avoid type mismatch errors
- **ThreadMetadata**: Uses metadata field instead of direct updated_at parameter

## Common Store Categories

- PostgreSQL store (using asyncpg)
- MySQL store (using aiomysql)
- SQLite store (using aiosqlite)
- MongoDB store (using motor)
- In-memory store (for testing)

## Output Requirements

1. Generate complete, working ChatKit store implementations
2. Include ALL required abstract methods implementation
3. Add proper error handling for database operations
4. Use correct ChatKit types for content
5. Follow the exact patterns shown in the template to avoid common errors
