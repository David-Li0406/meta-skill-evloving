# Data Patterns

Best practices for data processing, pipelines, and data management in Python.

## Table of Contents
- [Data Models](#data-models)
- [Data Validation](#data-validation)
- [ETL Patterns](#etl-patterns)
- [Database Patterns](#database-patterns)
- [Streaming Data](#streaming-data)

## Data Models

### Dataclasses for Domain Objects
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

@dataclass(frozen=True, slots=True)
class Money:
    amount: int  # Store in cents to avoid float precision issues
    currency: str = "USD"
    
    def __add__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    @property
    def dollars(self) -> float:
        return self.amount / 100

@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def total(self) -> Money:
        return sum(
            (item.total for item in self.items),
            start=Money(0)
        )
```

### Pydantic for External Data
```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Self

class ImportedRecord(BaseModel):
    id: str
    name: str
    value: float
    tags: list[str] = []
    
    @field_validator("value")
    @classmethod
    def value_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Value must be positive")
        return v
    
    @model_validator(mode="after")
    def validate_record(self) -> Self:
        if self.name.startswith("_") and "internal" not in self.tags:
            self.tags.append("internal")
        return self
```

## Data Validation

### Schema Validation with Pandera
```python
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series

class SalesSchema(pa.DataFrameModel):
    order_id: Series[str] = pa.Field(unique=True)
    customer_id: Series[str]
    amount: Series[float] = pa.Field(ge=0)
    quantity: Series[int] = pa.Field(ge=1)
    created_at: Series[pd.Timestamp]
    
    @pa.check("amount")
    def amount_reasonable(cls, series: Series[float]) -> Series[bool]:
        return series < 1_000_000  # Flag unreasonable amounts

@pa.check_types
def process_sales(df: DataFrame[SalesSchema]) -> DataFrame[SalesSchema]:
    return df[df["quantity"] > 0]
```

### Runtime Validation Pipeline
```python
from typing import Callable, TypeVar
from dataclasses import dataclass

T = TypeVar("T")

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]

def validate_pipeline(
    data: T,
    validators: list[Callable[[T], ValidationResult]]
) -> ValidationResult:
    all_errors: list[str] = []
    
    for validator in validators:
        result = validator(data)
        if not result.is_valid:
            all_errors.extend(result.errors)
    
    return ValidationResult(
        is_valid=len(all_errors) == 0,
        errors=all_errors
    )
```

## ETL Patterns

### Pipeline Architecture
```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class Transformer(ABC, Generic[T, U]):
    @abstractmethod
    def transform(self, data: T) -> U:
        pass

class Pipeline:
    def __init__(self) -> None:
        self._steps: list[Transformer] = []
    
    def add_step(self, transformer: Transformer) -> "Pipeline":
        self._steps.append(transformer)
        return self
    
    def execute(self, data):
        result = data
        for step in self._steps:
            result = step.transform(result)
        return result

# Usage
pipeline = (
    Pipeline()
    .add_step(CleanDataTransformer())
    .add_step(EnrichDataTransformer())
    .add_step(AggregateTransformer())
)
result = pipeline.execute(raw_data)
```

### Chunked Processing
```python
from typing import Iterator, TypeVar
from collections.abc import Iterable

T = TypeVar("T")

def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive chunks from iterable."""
    chunk: list[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def process_large_file(filepath: str, chunk_size: int = 10000) -> None:
    with open(filepath) as f:
        for chunk in chunked(f, chunk_size):
            process_chunk(chunk)
```

### Parallel ETL
```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")

def parallel_transform(
    items: list[T],
    transform_fn: Callable[[T], U],
    max_workers: int = 4
) -> list[U]:
    results: list[U] = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(transform_fn, item): i for i, item in enumerate(items)}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Transform failed: {e}")
    
    return results
```

## Database Patterns

### Repository Pattern
```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):
    @abstractmethod
    async def find_by_id(self, id: ID) -> T | None:
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def delete(self, id: ID) -> bool:
        pass

class SQLAlchemyUserRepository(Repository[User, str]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def find_by_id(self, id: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        row = result.scalar_one_or_none()
        return User.from_orm(row) if row else None
```

### Unit of Work Pattern
```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
    
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator["UnitOfWork", None]:
        self._session = self._session_factory()
        self.users = UserRepository(self._session)
        self.orders = OrderRepository(self._session)
        
        try:
            yield self
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        finally:
            await self._session.close()

# Usage
async with uow.transaction() as tx:
    user = await tx.users.find_by_id(user_id)
    order = Order(user_id=user.id, items=items)
    await tx.orders.save(order)
```

## Streaming Data

### Generator-Based Streaming
```python
from typing import Iterator, Generator

def stream_csv(filepath: str) -> Generator[dict, None, None]:
    """Stream CSV rows as dictionaries."""
    import csv
    
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def transform_stream(
    source: Iterator[dict],
    transform: Callable[[dict], dict]
) -> Generator[dict, None, None]:
    """Apply transformation to each item in stream."""
    for item in source:
        yield transform(item)

# Usage - memory efficient for large files
stream = stream_csv("large_file.csv")
transformed = transform_stream(stream, clean_record)
for record in transformed:
    process(record)
```

### Async Streaming
```python
from typing import AsyncGenerator

async def stream_api_pages(
    client: httpx.AsyncClient,
    base_url: str
) -> AsyncGenerator[list[dict], None]:
    """Stream paginated API results."""
    page = 1
    while True:
        response = await client.get(f"{base_url}?page={page}")
        data = response.json()
        
        if not data["items"]:
            break
        
        yield data["items"]
        
        if not data.get("has_next"):
            break
        page += 1

async def process_all_pages(url: str) -> int:
    total = 0
    async with httpx.AsyncClient() as client:
        async for items in stream_api_pages(client, url):
            for item in items:
                await process_item(item)
                total += 1
    return total
```

### Backpressure Handling
```python
import asyncio
from typing import AsyncGenerator

async def bounded_producer(
    items: list[str],
    queue: asyncio.Queue[str],
    max_pending: int = 100
) -> None:
    """Producer with backpressure via bounded queue."""
    for item in items:
        await queue.put(item)  # Blocks if queue is full
    
    # Signal completion
    await queue.put(None)

async def consumer(queue: asyncio.Queue[str | None]) -> None:
    """Consumer that processes items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        await process(item)
        queue.task_done()
```
