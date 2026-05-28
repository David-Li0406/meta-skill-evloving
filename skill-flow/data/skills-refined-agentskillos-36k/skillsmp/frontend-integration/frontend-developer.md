---
name: frontend-developer
description: "Frontend development patterns with Kailash. Use when asking 'frontend patterns', 'frontend development', or 'UI integration'."
---

# Frontend Development Patterns

> **Skill Metadata**
> Category: `frontend`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Architecture Pattern

```
┌─────────────┐
│   Frontend  │  (React/Flutter/Vue)
│   (Web/App) │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│ WorkflowAPI │  (Python/Kailash)
│   (FastAPI) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Workflows  │  (Business Logic)
│   (Kailash) │
└─────────────┘
```

## State Management

### Frontend State (React)
```typescript
// Use React Query for API calls
import { useQuery, useMutation } from 'react-query';

function useWorkflow() {
  return useMutation(async (message: string) => {
    const response = await fetch('/execute', {
      method: 'POST',
      body: JSON.stringify({inputs: {message}})
    });
    return response.json();
  });
}

// Component
function Chat() {
  const mutation = useWorkflow();

  const handleSubmit = () => {
    mutation.mutate(message);
  };

  return <div>{mutation.data?.outputs?.chat?.response}</div>;
}
```

## Error Handling

```typescript
// Frontend error handling
async function executeWorkflow(message: string) {
  try {
    const response = await fetch('/execute', {
      method: 'POST',
      body: JSON.stringify({inputs: {message}})
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Workflow failed');
    }

    return response.json();
  } catch (error) {
    console.error('Workflow error:', error);
    // Show user-friendly error message
    throw error;
  }
}
```

## Best Practices

1. **API layer** - Separate API calls from components
2. **Error handling** - User-friendly error messages
3. **Loading states** - Show loading indicators
4. **State management** - Use React Query/Redux
5. **Type safety** - TypeScript interfaces for API responses
6. **Environment configs** - API URL from env vars

<!-- Trigger Keywords: frontend patterns, frontend development, UI integration, frontend architecture -->
