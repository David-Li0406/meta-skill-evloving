# Validation

Handle validation errors gracefully using the Result pattern.

## Basic Validation

```typescript
import { NonEmptyString100 } from "@/lib/evolu";

function TodoInput() {
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { create } = useEvolu();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const result = NonEmptyString100.from(title);

    if (!result.ok) {
      setError(formatValidationError(result.error));
      return;
    }

    setError(null);
    create("todo", { title: result.value, isCompleted: evolu.sqliteFalse });
    setTitle("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      {error && <span className="error">{error}</span>}
      <button type="submit">Add</button>
    </form>
  );
}
```

## Error Formatting

```typescript
function formatValidationError(error: unknown): string {
  // Evolu returns structured type errors
  if (typeof error === "object" && error !== null) {
    const err = error as { type?: string; min?: number; max?: number };

    if (err.type === "MinLength") {
      return `Minimum ${err.min} characters required`;
    }
    if (err.type === "MaxLength") {
      return `Maximum ${err.max} characters allowed`;
    }
  }
  return "Invalid input";
}
```

## Available Validation Types

| Type | Description |
|------|-------------|
| `NonEmptyString` | Non-empty string |
| `maxLength(n, type)` | Constrain max length |
| `minLength(n, type)` | Constrain min length |
| `SqliteBoolean` | Boolean stored as 0/1 |
| `id("TableName")` | Branded ID type |
| `nullOr(type)` | Make type nullable |

## Validation Pattern

Always validate before mutations:

```typescript
const result = BrandedType.from(input);
if (!result.ok) {
  // Handle error - don't proceed with mutation
  return;
}
// Safe to use result.value
```
