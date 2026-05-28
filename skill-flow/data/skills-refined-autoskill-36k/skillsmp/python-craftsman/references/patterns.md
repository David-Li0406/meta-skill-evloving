# Python Craftsman

## Patterns


---
  #### **Name**
Pydantic Model Design
  #### **Description**
Type-safe data models with validation
  #### **When**
Defining data structures, API schemas, config
  #### **Example**
    # Pydantic V2 Model Design for Memory System
    
    from datetime import datetime
    from enum import Enum
    from typing import Annotated
    
    from pydantic import (
        BaseModel,
        Field,
        ConfigDict,
        field_validator,
        model_validator,
    )
    
    class MemoryType(str, Enum):
        EPISODIC = "episodic"
        SEMANTIC = "semantic"
        PROCEDURAL = "procedural"
    
    class Memory(BaseModel):
        """A single memory unit in the memory system."""
    
        model_config = ConfigDict(
            # V2: Use this instead of class Config
            frozen=True,  # Immutable after creation
            extra="forbid",  # Reject unknown fields
            str_strip_whitespace=True,
        )
    
        id: str = Field(
            ...,
            min_length=1,
            max_length=64,
            pattern=r"^[a-zA-Z0-9_-]+$",
            description="Unique memory identifier"
        )
        content: str = Field(
            ...,
            min_length=1,
            max_length=10000,
        )
        memory_type: MemoryType
        created_at: datetime = Field(default_factory=datetime.utcnow)
        embedding: list[float] | None = None
        metadata: dict[str, str] = Field(default_factory=dict)
    
        @field_validator("embedding")
        @classmethod
        def validate_embedding(cls, v: list[float] | None) -> list[float] | None:
            if v is not None and len(v) != 384:
                raise ValueError("Embedding must be 384 dimensions")
            return v
    
        @model_validator(mode="after")
        def validate_memory(self) -> "Memory":
            """Cross-field validation."""
            if self.memory_type == MemoryType.SEMANTIC and not self.embedding:
                raise ValueError("Semantic memories require embeddings")
            return self
    
    # Usage with type safety
    def store_memory(memory: Memory) -> str:
        """Type hints make intent clear."""
        return memory.id
    

---
  #### **Name**
Async Context Manager Pattern
  #### **Description**
Resource management with async/await
  #### **When**
Managing connections, sessions, or any async resource
  #### **Example**
    # Async Context Manager for Database Connections
    
    from contextlib import asynccontextmanager
    from typing import AsyncGenerator
    import asyncpg
    
    class DatabasePool:
        """Connection pool with proper lifecycle management."""
    
        def __init__(self, dsn: str, min_size: int = 5, max_size: int = 20):
            self._dsn = dsn
            self._min_size = min_size
            self._max_size = max_size
            self._pool: asyncpg.Pool | None = None
    
        async def connect(self) -> None:
            """Initialize the connection pool."""
            if self._pool is not None:
                raise RuntimeError("Pool already connected")
    
            self._pool = await asyncpg.create_pool(
                self._dsn,
                min_size=self._min_size,
                max_size=self._max_size,
            )
    
        async def disconnect(self) -> None:
            """Close all connections."""
            if self._pool is not None:
                await self._pool.close()
                self._pool = None
    
        @asynccontextmanager
        async def acquire(self) -> AsyncGenerator[asyncpg.Connection, None]:
            """Acquire a connection from the pool."""
            if self._pool is None:
                raise RuntimeError("Pool not connected")
    
            async with self._pool.acquire() as conn:
                yield conn
    
        @asynccontextmanager
        async def transaction(self) -> AsyncGenerator[asyncpg.Connection, None]:
            """Acquire a connection with transaction."""
            async with self.acquire() as conn:
                async with conn.transaction():
                    yield conn
    
    # Application lifecycle
    @asynccontextmanager
    async def lifespan(app) -> AsyncGenerator[dict, None]:
        """FastAPI lifespan for resource management."""
        db = DatabasePool("postgres://...")
        await db.connect()
    
        try:
            yield {"db": db}
        finally:
            await db.disconnect()
    

---
  #### **Name**
Result Type Pattern
  #### **Description**
Explicit error handling without exceptions
  #### **When**
Functions that can fail in expected ways
  #### **Example**
    # Result Type for Explicit Error Handling
    
    from dataclasses import dataclass
    from typing import Generic, TypeVar, Callable
    
    T = TypeVar("T")
    E = TypeVar("E")
    
    @dataclass(frozen=True, slots=True)
    class Ok(Generic[T]):
        value: T
    
        def is_ok(self) -> bool:
            return True
    
        def is_err(self) -> bool:
            return False
    
        def unwrap(self) -> T:
            return self.value
    
        def map(self, fn: Callable[[T], "U"]) -> "Result[U, E]":
            return Ok(fn(self.value))
    
    @dataclass(frozen=True, slots=True)
    class Err(Generic[E]):
        error: E
    
        def is_ok(self) -> bool:
            return False
    
        def is_err(self) -> bool:
            return True
    
        def unwrap(self) -> T:
            raise ValueError(f"Called unwrap on Err: {self.error}")
    
        def map(self, fn: Callable) -> "Result[T, E]":
            return self
    
    Result = Ok[T] | Err[E]
    
    # Usage in memory service
    @dataclass(frozen=True)
    class MemoryError:
        code: str
        message: str
    
    async def retrieve_memory(
        id: str
    ) -> Result[Memory, MemoryError]:
        """Returns Result instead of raising exceptions."""
        try:
            memory = await db.fetchone("SELECT * FROM memories WHERE id = $1", id)
            if memory is None:
                return Err(MemoryError("NOT_FOUND", f"Memory {id} not found"))
            return Ok(Memory(**memory))
        except Exception as e:
            return Err(MemoryError("DB_ERROR", str(e)))
    
    # Caller handles explicitly
    async def process_memory(id: str) -> None:
        result = await retrieve_memory(id)
        match result:
            case Ok(memory):
                print(f"Found: {memory.content}")
            case Err(error):
                print(f"Error [{error.code}]: {error.message}")
    

---
  #### **Name**
Modern Python Project Structure
  #### **Description**
Project layout with proper packaging
  #### **When**
Starting new Python project or reorganizing existing
  #### **Example**
    # Modern Python Project Structure
    
    memory_service/
    ├── pyproject.toml          # Single source of truth
    ├── README.md
    ├── src/
    │   └── memory_service/            # Package in src/ layout
    │       ├── __init__.py
    │       ├── py.typed        # PEP 561 marker
    │       ├── core/
    │       │   ├── __init__.py
    │       │   ├── memory.py
    │       │   └── retrieval.py
    │       ├── models/
    │       │   ├── __init__.py
    │       │   └── schemas.py
    │       ├── db/
    │       │   ├── __init__.py
    │       │   └── postgres.py
    │       └── api/
    │           ├── __init__.py
    │           └── routes.py
    ├── tests/
    │   ├── conftest.py
    │   ├── unit/
    │   └── integration/
    └── scripts/
        └── migrate.py
    
    # pyproject.toml (using uv or poetry)
    [project]
    name = "memory-service"
    version = "0.1.0"
    requires-python = ">=3.11"
    dependencies = [
        "fastapi>=0.109.0",
        "pydantic>=2.5.0",
        "asyncpg>=0.29.0",
        "lancedb>=0.4.0",
    ]
    
    [project.optional-dependencies]
    dev = [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.23.0",
        "mypy>=1.8.0",
        "ruff>=0.1.0",
    ]
    
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    
    [tool.hatch.build.targets.wheel]
    packages = ["src/memory_service"]
    
    [tool.mypy]
    python_version = "3.11"
    strict = true
    warn_return_any = true
    warn_unused_configs = true
    
    [tool.ruff]
    target-version = "py311"
    line-length = 88
    
    [tool.ruff.lint]
    select = ["E", "F", "I", "N", "UP", "B", "C4", "SIM"]
    
    [tool.pytest.ini_options]
    asyncio_mode = "auto"
    testpaths = ["tests"]
    

## Anti-Patterns


---
  #### **Name**
Any Type Escape Hatch
  #### **Description**
Using Any to avoid proper typing
  #### **Why**
Any defeats the purpose of type hints. Every Any is a bug waiting.
  #### **Instead**
Use generics, TypeVar, or proper type narrowing

---
  #### **Name**
Bare Exception Handling
  #### **Description**
Using except Exception without specific handling
  #### **Why**
Hides bugs, catches things you didn't intend (KeyboardInterrupt, SystemExit)
  #### **Instead**
Catch specific exceptions, re-raise unexpected ones

---
  #### **Name**
Sync in Async
  #### **Description**
Calling blocking code in async functions
  #### **Why**
Blocks the entire event loop, defeats the purpose of async
  #### **Instead**
Use run_in_executor for blocking calls, or use async libraries

---
  #### **Name**
Global Mutable State
  #### **Description**
Module-level mutable variables
  #### **Why**
Hidden dependencies, race conditions in async, testing nightmares
  #### **Instead**
Dependency injection, explicit context passing

---
  #### **Name**
requirements.txt Without Pins
  #### **Description**
Unpinned or loosely pinned dependencies
  #### **Why**
Builds break randomly when dependencies update
  #### **Instead**
Use lock files (uv.lock, poetry.lock), pin all versions