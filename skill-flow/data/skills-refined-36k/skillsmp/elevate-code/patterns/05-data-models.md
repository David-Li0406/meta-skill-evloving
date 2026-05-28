# Pattern 5: Data Models

**Problem**: Data shapes are unclear. Functions accept `dict` or `any`, and bugs hide in mismatched expectations.

**Solution**: Define explicit data structures for all domain objects. Use dataclasses (Python), interfaces (TypeScript), or schemas (JSON Schema) with validation at boundaries.

---

## Concept

Data Models answer: **"What shape is this data?"**

Strong typing provides:
1. **IDE Support** — Autocomplete, refactoring, inline docs
2. **Compile-time Safety** — Catch errors before runtime
3. **Documentation** — Types are always up-to-date docs
4. **Validation** — Reject bad data at boundaries

---

## Decision Tree

```
Where is the data coming from?

Internal (your code creates it)?
├─ Yes → Dataclass/Interface (trust it)
└─ No ↓

External (user input, API, file)?
├─ Yes → Validate at boundary
│   ├─ Simple validation → Type guard function
│   └─ Complex validation → Pydantic/Zod
└─ No → You're overthinking it
```

---

## Implementation

### Python: Dataclasses

```python
from dataclasses import dataclass, field, asdict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Config:
    """Application configuration. Immutable by convention."""
    input_path: str
    output_path: str
    verbose: bool = False
    max_retries: int = 3
    timeout_seconds: float = 30.0

@dataclass
class Task:
    """A unit of work to process."""
    id: str
    name: str
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize for JSON/persistence."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "error_message": self.error_message
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize from JSON/persistence."""
        return cls(
            id=data["id"],
            name=data["name"],
            status=Status(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
            error_message=data.get("error_message")
        )

@dataclass
class ProcessingResult:
    """Result of processing a task."""
    task: Task
    success: bool
    output: Optional[str] = None
    duration_seconds: float = 0.0

# Usage
def process_task(task: Task, config: Config) -> ProcessingResult:
    """Type hints make expectations clear."""
    # IDE knows task.status is Status, config.timeout_seconds is float
    pass
```

### Python: Pydantic (External Data)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class UserInput(BaseModel):
    """Validates external input. Raises on invalid data."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)
    tags: List[str] = Field(default_factory=list)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip()

# Usage
try:
    user = UserInput(name="  John  ", email="john@example.com", age=30)
    print(user.name)  # "John" (stripped)
except ValidationError as e:
    print(f"Invalid input: {e}")
```

### TypeScript: Interfaces

```typescript
// types.ts

// Enums for fixed values
enum Status {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Interface for configuration
interface Config {
  readonly inputPath: string;
  readonly outputPath: string;
  readonly verbose?: boolean;
  readonly maxRetries?: number;
  readonly timeoutMs?: number;
}

// Interface for domain objects
interface Task {
  id: string;
  name: string;
  status: Status;
  createdAt: Date;
  metadata?: Record<string, unknown>;
  errorMessage?: string;
}

interface ProcessingResult {
  task: Task;
  success: boolean;
  output?: string;
  durationMs: number;
}

// Factory functions for creating objects
function createTask(name: string, id?: string): Task {
  return {
    id: id ?? crypto.randomUUID(),
    name,
    status: Status.PENDING,
    createdAt: new Date(),
  };
}

// Serialization
function taskToJson(task: Task): string {
  return JSON.stringify({
    ...task,
    createdAt: task.createdAt.toISOString(),
  });
}

function taskFromJson(json: string): Task {
  const data = JSON.parse(json);
  return {
    ...data,
    createdAt: new Date(data.createdAt),
    status: data.status as Status,
  };
}
```

### TypeScript: Type Guards

```typescript
// Type guards for runtime validation

function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isTask(obj: unknown): obj is Task {
  if (typeof obj !== 'object' || obj === null) return false;

  const candidate = obj as Record<string, unknown>;

  return (
    typeof candidate.id === 'string' &&
    typeof candidate.name === 'string' &&
    Object.values(Status).includes(candidate.status as Status) &&
    candidate.createdAt instanceof Date
  );
}

function isValidConfig(obj: unknown): obj is Config {
  if (typeof obj !== 'object' || obj === null) return false;

  const candidate = obj as Record<string, unknown>;

  return (
    typeof candidate.inputPath === 'string' &&
    typeof candidate.outputPath === 'string' &&
    (candidate.verbose === undefined || typeof candidate.verbose === 'boolean') &&
    (candidate.maxRetries === undefined || typeof candidate.maxRetries === 'number')
  );
}

// Usage at boundaries
function loadConfig(filePath: string): Config {
  const raw = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  if (!isValidConfig(raw)) {
    throw new Error(`Invalid config file: ${filePath}`);
  }

  return raw;
}
```

### TypeScript: Zod (External Data)

```typescript
import { z } from 'zod';

// Define schema
const UserInputSchema = z.object({
  name: z.string().min(1).max(100).transform(s => s.trim()),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
  tags: z.array(z.string()).default([]),
});

// Infer TypeScript type from schema
type UserInput = z.infer<typeof UserInputSchema>;

// Usage
function handleUserInput(raw: unknown): UserInput {
  const result = UserInputSchema.safeParse(raw);

  if (!result.success) {
    throw new Error(`Invalid input: ${result.error.message}`);
  }

  return result.data;
}
```

---

## Validation Boundaries

Validate data where it enters your system:

```
┌─────────────────────────────────────────────────────┐
│                    Your Code                        │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │  Internal: Trust the types (dataclass)      │   │
│   │                                             │   │
│   │  Task ──► process() ──► Result             │   │
│   │                                             │   │
│   └─────────────────────────────────────────────┘   │
│                                                     │
│   ▲                                           ▲     │
│   │ VALIDATE                           VALIDATE     │
│   │                                           │     │
└───┼───────────────────────────────────────────┼─────┘
    │                                           │
 User Input                                 API Response
 (CLI args, config)                         (JSON)
```

---

## Checklist

- [ ] All domain objects have explicit type definitions
- [ ] No `dict`, `any`, or `object` in function signatures
- [ ] External data is validated at boundaries
- [ ] Serialization/deserialization methods exist
- [ ] Enums used for fixed sets of values
- [ ] Optional fields have sensible defaults
- [ ] Type guards exist for runtime validation when needed

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `def process(data: dict)` | Shape is unclear | Use dataclass |
| `any` everywhere | No type safety | Define specific types |
| Validate everywhere | Repetitive, error-prone | Validate at boundaries only |
| Mutable shared state | Race conditions, bugs | Prefer immutability |

---

## Success Signals

- IDE autocomplete works throughout codebase
- Type errors caught at lint/compile time
- Function signatures are self-documenting
- Refactoring is safe (type checker catches issues)
