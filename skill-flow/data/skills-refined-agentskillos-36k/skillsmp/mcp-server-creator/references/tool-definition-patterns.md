# MCP Tool Definition Patterns

This document provides patterns and best practices for defining MCP tools in production servers.

## Basic Tool Patterns

### Simple Synchronous Tool
```python
@mcp.tool()
def greet_user(name: str) -> str:
    """Simple tool that returns a greeting."""
    return f"Hello, {name}!"
```

### Tool with Multiple Parameters
```python
@mcp.tool()
def calculate_area(width: float, height: float, unit: str = "meters") -> dict:
    """Calculate area with units."""
    area = width * height
    return {
        "area": area,
        "unit": unit,
        "width": width,
        "height": height
    }
```

### Tool with Complex Return Types
```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    title: str
    score: float
    metadata: Dict[str, any]

@mcp.tool()
def search_documents(query: str, limit: int = 10) -> List[SearchResult]:
    """Search for documents and return structured results."""
    results = perform_search(query, limit)
    return [
        SearchResult(id=r["id"], title=r["title"], score=r["score"], metadata=r["meta"])
        for r in results
    ]
```

## Advanced Tool Patterns

### Async Tool with Context
```python
from mcp_use.server import Context

@mcp.tool()
async def intelligent_search(query: str, ctx: Context) -> str:
    """Search tool that leverages context for LLM assistance."""
    # Use context to get LLM assistance
    refined_result = await ctx.sample(
        messages=f"Refine this search query: {query}",
        max_tokens=100,
        temperature=0.7
    )

    refined_query = refined_result.content.text

    # Log progress
    await ctx.log('info', f'Searching with refined query: {refined_query}')

    # Perform search
    results = await async_search(refined_query)

    return format_results(results)
```

### Tool with Progress Updates
```python
@mcp.tool()
async def process_large_dataset(dataset_id: str, ctx: Context) -> str:
    """Process large dataset with progress updates."""
    total_items = get_dataset_size(dataset_id)

    await ctx.log('info', f'Starting to process {total_items} items')

    processed = 0
    for item in get_dataset_items(dataset_id):
        result = process_item(item)
        processed += 1

        # Update progress every 100 items
        if processed % 100 == 0:
            progress = (processed / total_items) * 100
            await ctx.log('info', f'Progress: {progress:.1f}% ({processed}/{total_items})')

    await ctx.log('info', 'Dataset processing completed')
    return f'Processed {processed} items successfully'
```

## Error Handling Patterns

### Comprehensive Error Handling
```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def robust_data_processor(data: str) -> dict:
    """Tool with comprehensive error handling."""
    try:
        # Input validation
        if not data:
            raise ValueError("Data cannot be empty")

        if len(data) > 10000:  # 10KB limit
            raise ValueError("Data too large, maximum 10KB allowed")

        # Process data
        result = process_data(data)

        return {"status": "success", "result": result}

    except ValueError as e:
        # Log validation errors
        logger.warning(f"Validation error in data processor: {e}")
        raise  # Re-raise to send to client

    except ExternalServiceError as e:
        # Log external service errors
        logger.error(f"External service error: {e}")
        raise RuntimeError("External service temporarily unavailable")

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in data processor: {e}", exc_info=True)
        raise RuntimeError("An error occurred processing your request")
```

### Conditional Error Handling
```python
@mcp.tool()
def conditional_tool(operation: str, data: str) -> str:
    """Tool with conditional error handling based on operation type."""

    if operation == "read":
        if not data_exists(data):
            raise FileNotFoundError(f"Data '{data}' not found")
        return read_data(data)

    elif operation == "write":
        if not is_valid_write_target(data):
            raise PermissionError(f"Cannot write to '{data}', access denied")
        return write_data(data)

    elif operation == "delete":
        if is_protected_resource(data):
            raise PermissionError(f"Cannot delete protected resource '{data}'")
        return delete_data(data)

    else:
        raise ValueError(f"Unsupported operation: {operation}")
```

## Validation Patterns

### Custom Validator Class
```python
class DataValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        import re
        pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s\.-]?(\d{3})[\s\.-]?(\d{4})$'
        return re.match(pattern, phone) is not None

@mcp.tool()
def contact_validator(email: str, phone: str) -> dict:
    """Validate contact information."""
    email_valid = DataValidator.validate_email(email)
    phone_valid = DataValidator.validate_phone(phone)

    return {
        "email": {"value": email, "valid": email_valid},
        "phone": {"value": phone, "valid": phone_valid},
        "overall_valid": email_valid and phone_valid
    }
```

### Pydantic Integration
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class UserData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: str
    phone: Optional[str] = None

    @validator('email')
    def validate_email_format(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v

@mcp.tool()
def process_user_data(raw_data: dict) -> dict:
    """Process user data with Pydantic validation."""
    try:
        validated_data = UserData(**raw_data)
        result = save_user(validated_data.dict())
        return {"status": "success", "user_id": result.id}
    except Exception as e:
        raise ValueError(f"Invalid user data: {str(e)}")
```

## State Management Patterns

### Tool with Internal State
```python
from threading import Lock
from collections import defaultdict

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = Lock()

    def create_session(self, user_id: str) -> str:
        import uuid
        session_id = str(uuid.uuid4())
        with self.lock:
            self.sessions[session_id] = {
                "user_id": user_id,
                "created_at": __import__('datetime').datetime.now(),
                "active": True
            }
        return session_id

    def get_session(self, session_id: str):
        with self.lock:
            return self.sessions.get(session_id)

session_manager = SessionManager()

@mcp.tool()
def create_user_session(user_id: str) -> str:
    """Create a new user session."""
    return session_manager.create_session(user_id)

@mcp.tool()
def get_session_info(session_id: str) -> dict:
    """Get information about a session."""
    session = session_manager.get_session(session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    return session
```

## Resource Management Patterns

### Tool with Resource Cleanup
```python
from contextlib import contextmanager
import tempfile
import os

@contextmanager
def temporary_file(suffix: str = ""):
    """Context manager for temporary files that ensures cleanup."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
    try:
        os.close(temp_fd)  # Close the file descriptor
        yield temp_path
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@mcp.tool()
def process_document_content(content: str) -> str:
    """Process document content using temporary file."""
    with temporary_file(suffix=".txt") as temp_path:
        # Write content to temporary file
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Process the file
        result = process_document_file(temp_path)

        # File is automatically cleaned up
        return result
```

### Tool with Connection Pooling
```python
import asyncio
from asyncio import Semaphore

class ConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.semaphore = Semaphore(max_connections)
        self.active_connections = 0

    async def get_connection(self):
        """Get a connection from the pool."""
        await self.semaphore.acquire()
        self.active_connections += 1
        return self._create_connection()

    def release_connection(self):
        """Release a connection back to the pool."""
        self.active_connections -= 1
        self.semaphore.release()

    def _create_connection(self):
        """Create a new connection (implementation depends on your use case)."""
        # This is a placeholder - implement based on your needs
        return "connection_object"

pool = ConnectionPool(max_connections=5)

@mcp.tool()
async def database_operation(query: str) -> dict:
    """Perform database operation with connection pooling."""
    conn = await pool.get_connection()
    try:
        result = await execute_query(conn, query)
        return result
    finally:
        pool.release_connection()
```

## Async Patterns

### Tool with Concurrent Operations
```python
import asyncio

@mcp.tool()
async def fetch_multiple_sources(urls: list[str]) -> list[dict]:
    """Fetch data from multiple sources concurrently."""
    async def fetch_single(url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return {
                        "url": url,
                        "status": response.status,
                        "data": await response.text()
                    }
        except Exception as e:
            return {
                "url": url,
                "error": str(e)
            }

    # Execute all requests concurrently
    results = await asyncio.gather(*[fetch_single(url) for url in urls])
    return results
```

### Tool with Timeouts
```python
import asyncio

@mcp.tool()
async def timed_operation(data: str, timeout_seconds: int = 30) -> str:
    """Perform operation with timeout."""
    try:
        result = await asyncio.wait_for(
            perform_long_operation(data),
            timeout=timeout_seconds
        )
        return result
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")
```

These patterns provide a solid foundation for implementing robust, production-ready MCP tools.
