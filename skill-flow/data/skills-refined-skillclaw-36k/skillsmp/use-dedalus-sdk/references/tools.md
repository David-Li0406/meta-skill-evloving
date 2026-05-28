# Tools Reference

Advanced tool patterns for the Dedalus SDK.

## Tool Definition Patterns

### With Docstrings (Python)

Docstrings become tool descriptions:

```python
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for matching records.
    
    Args:
        query: Search query string
        limit: Maximum results to return
    
    Returns:
        List of matching records
    """
    return db.search(query, limit=limit)
```

### With JSDoc (TypeScript)

```typescript
/**
 * Search the database for matching records
 * @param query - Search query string  
 * @param limit - Maximum results to return
 */
function searchDatabase(query: string, limit: number = 10): object[] {
  return db.search(query, limit);
}
```

## Tool Execution Control

### autoExecuteTools

Control whether tools run automatically:

```typescript
const runner = new DedalusRunner(client, true);  // Auto-execute enabled

const result = await runner.run({
  model: 'openai/gpt-4o-mini',
  input: 'What time is it?',
  tools: [getCurrentTime],
  autoExecuteTools: true,  // Default when runner initialized with true
});
```

### maxSteps

Limit tool execution iterations:

```typescript
const result = await runner.run({
  input: 'Complex multi-step task',
  model: 'openai/gpt-4o-mini',
  tools: [step1, step2, step3],
  maxSteps: 5,
});
```

## Complex Tool Types

### Pydantic Models (Python)

```python
from pydantic import BaseModel

class SearchParams(BaseModel):
    query: str
    filters: dict[str, str] = {}
    limit: int = 10

def search(params: SearchParams) -> list[dict]:
    """Search with structured parameters."""
    return db.search(params.query, params.filters, params.limit)
```

### Zod Schemas (TypeScript)

```typescript
import { zodFunction } from 'dedalus-labs/helpers/zod';
import { z } from 'zod';

const searchTool = zodFunction({
  name: 'search',
  description: 'Search the database',
  parameters: z.object({
    query: z.string(),
    filters: z.record(z.string()).optional(),
    limit: z.number().default(10),
  }),
  function: async ({ query, filters, limit }) => {
    return await db.search(query, filters, limit);
  },
});
```

## Model Selection for Tools

Tool calling quality varies by model:

| Model | Multi-step Reasoning | Tool Chaining |
|-------|---------------------|---------------|
| `openai/gpt-4o-mini` | ✓ Good | ✓ Good |
| `openai/gpt-4.1` | ✓ Excellent | ✓ Excellent |
| `anthropic/claude-sonnet-4-20250514` | ✓ Good | ✓ Good |
| Older/smaller models | Limited | Limited |

## Error Handling

Tools can return errors that the model will see:

```python
def risky_operation(params: dict) -> dict:
    try:
        result = perform_operation(params)
        return {"success": True, "data": result}
    except ValidationError as e:
        return {"success": False, "error": str(e)}
```

## Tool Results in RunResult

Access tool execution details:

```python
result = await runner.run(...)

# Final text output
print(result.final_output)

# All tool executions
for tool_result in result.tool_results:
    print(f"Tool: {tool_result.name}")
    print(f"Step: {tool_result.step}")
    print(f"Result: {tool_result.result}")
    if tool_result.error:
        print(f"Error: {tool_result.error}")
```
