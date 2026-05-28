#!/usr/bin/env python3
"""
OpenMemory Client for AI Agent Long-term Memory Management.

This module provides a simple interface to store and retrieve memories
using OpenMemory's local-first approach.

Usage:
    from memory_client import MemoryClient

    memory = MemoryClient()
    memory.add("User prefers dark mode", tags=["preferences"])
    results = memory.query("What does the user like?")
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional


# Ensure project root is in path
def find_project_root():
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (
            (current / ".opencode").exists()
            or (current / "shared" / "context" / "config.yaml").exists()
            or (current / ".git").exists()
        ):
            return current
        if current.parent == current:
            break
        current = current.parent
    return Path(__file__).resolve().parents[4]


PROJECT_ROOT = find_project_root()
sys.path.insert(0, str(PROJECT_ROOT))

# Memory database directory
MEMORY_DIR = PROJECT_ROOT / "data" / "memory"

# Default user ID for the agent
DEFAULT_USER_ID = "opencode-agent"


def _run_async(coro):
    """Run an async coroutine synchronously."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If we're already in an async context, create a new thread
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return asyncio.run(coro)


class MemoryClient:
    """
    OpenMemory client for managing AI agent's long-term memory.

    Provides synchronous methods to add, query, list, and delete memories
    stored using OpenMemory's local-first approach.

    Attributes:
        mem: OpenMemory Memory instance
        user_id: User identifier for memory isolation
    """

    def __init__(
        self,
        user_id: Optional[str] = None,
        working_dir: Optional[str] = None,
    ):
        """
        Initialize the MemoryClient.

        Args:
            user_id: User identifier. Defaults to 'opencode-agent'
            working_dir: Working directory for OpenMemory data.
                        Defaults to data/memory/
        """
        try:
            from openmemory import Memory
        except ImportError as e:
            error_msg = str(e)
            if "dotenv" in error_msg:
                raise ImportError(
                    "python-dotenv is not installed (required by openmemory-py). "
                    "Please run: pip install python-dotenv"
                )
            elif "langchain" in error_msg.lower() or "BaseMessage" in error_msg:
                raise ImportError(
                    "langchain-core is not installed (required by openmemory-py). "
                    "Please run: pip install langchain-core"
                )
            else:
                raise ImportError(
                    f"openmemory-py failed to import: {error_msg}\n"
                    "Please run: pip install openmemory-py python-dotenv langchain-core"
                )

        self.user_id = user_id or DEFAULT_USER_ID

        # Set up working directory
        if working_dir:
            self.working_dir = Path(working_dir)
        else:
            self.working_dir = MEMORY_DIR

        # Ensure directory exists
        self.working_dir.mkdir(parents=True, exist_ok=True)

        # Change to working directory for OpenMemory
        self._original_cwd = os.getcwd()
        os.chdir(str(self.working_dir))

        # Initialize OpenMemory
        self.mem = Memory(user=self.user_id)

    def add(
        self,
        content: str,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Add a new memory.

        Args:
            content: The memory content to store
            tags: Optional list of tags for categorization
            metadata: Optional arbitrary metadata

        Returns:
            dict: Result with id, content, and metadata
        """

        async def _add():
            kwargs = {}
            if tags:
                kwargs["tags"] = tags
            if metadata:
                kwargs["metadata"] = metadata

            result = await self.mem.add(content, user_id=self.user_id, **kwargs)
            return result

        result = _run_async(_add())

        return {
            "status": "success",
            "id": result.get("id") or result.get("root_memory_id"),
            "content": content,
            "tags": tags,
            "result": result,
        }

    def query(self, question: str, limit: int = 5) -> list[dict]:
        """
        Query memories based on a question.

        Args:
            question: The query string
            limit: Maximum number of results to return

        Returns:
            list: List of relevant memories
        """

        async def _query():
            results = await self.mem.search(question, user_id=self.user_id, limit=limit)
            return results

        results = _run_async(_query())

        # Normalize results
        normalized = []
        for r in results:
            normalized.append(
                {
                    "id": r.get("id"),
                    "content": r.get("content"),
                    "score": r.get("score", 0),
                    "tags": r.get("tags", []),
                    "metadata": r.get("metadata", {}),
                    "salience": r.get("salience", 0.5),
                }
            )

        return normalized

    def get(self, memory_id: str) -> Optional[dict]:
        """
        Get a specific memory by ID.

        Args:
            memory_id: The ID of the memory

        Returns:
            dict: Memory data or None if not found
        """

        async def _get():
            result = await self.mem.get(memory_id)
            return result

        try:
            result = _run_async(_get())
            if result:
                return {
                    "id": result.get("id"),
                    "content": result.get("content"),
                    "tags": result.get("tags", []),
                    "metadata": result.get("metadata", {}),
                    "salience": result.get("salience", 0.5),
                }
        except Exception:
            pass

        return None

    def list_memories(
        self, limit: int = 20, tags: Optional[list[str]] = None
    ) -> list[dict]:
        """
        List stored memories.

        Args:
            limit: Maximum number of memories to return
            tags: Filter by specific tags (not directly supported, use query)

        Returns:
            list: List of memories
        """
        # Use query method with wildcard to list all memories
        return self.query("*", limit=limit)

    def delete(self, memory_id: str) -> dict:
        """
        Delete a specific memory by ID.

        Args:
            memory_id: The ID of the memory to delete

        Returns:
            dict: Result of the delete operation
        """

        async def _delete():
            result = await self.mem.delete(memory_id)
            return result

        try:
            result = _run_async(_delete())
            return {"status": "success", "deleted_id": memory_id, "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def clear(self) -> dict:
        """
        Clear all memories for the current user.

        Returns:
            dict: Result of the clear operation
        """

        async def _clear():
            if hasattr(self.mem, "delete_all"):
                await self.mem.delete_all(user_id=self.user_id)
                return True
            return False

        try:
            success = _run_async(_clear())
            if success:
                return {"status": "success", "message": "All memories cleared"}
            else:
                return {"status": "error", "message": "delete_all method not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def close(self):
        """Restore original working directory."""
        os.chdir(self._original_cwd)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Singleton instance for easy access
_client: Optional[MemoryClient] = None


def get_client() -> MemoryClient:
    """Get or create the singleton MemoryClient instance."""
    global _client
    if _client is None:
        _client = MemoryClient()
    return _client


def add(content: str, tags: Optional[list[str]] = None, **kwargs) -> dict:
    """Convenience function to add a memory."""
    return get_client().add(content, tags, **kwargs)


def query(question: str, limit: int = 5) -> list[dict]:
    """Convenience function to query memories."""
    return get_client().query(question, limit)


def list_memories(limit: int = 20, tags: Optional[list[str]] = None) -> list[dict]:
    """Convenience function to list memories."""
    return get_client().list_memories(limit, tags)


def delete(memory_id: str) -> dict:
    """Convenience function to delete a memory."""
    return get_client().delete(memory_id)


def clear() -> dict:
    """Convenience function to clear all memories."""
    return get_client().clear()
