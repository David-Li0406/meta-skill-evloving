---
name: react-integration-quick
description: "React + Kailash SDK integration. Use when asking 'react integration', 'react kailash', or 'kailash frontend'."
---

# React + Kailash Integration

> **Skill Metadata**
> Category: `frontend`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Quick Setup

### 1. Backend API (Python)
```python
from kailash.api.workflow_api import WorkflowAPI
from kailash.workflow.builder import WorkflowBuilder

# Create workflow
workflow = WorkflowBuilder()
workflow.add_node("LLMNode", "chat", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "{{input.message}}"
})

# Deploy as API
api = WorkflowAPI(workflow.build())
api.run(port=8000)  # POST /execute
```

### 2. React Frontend
```typescript
// src/api/workflow.ts
export async function executeWorkflow(message: string) {
  const response = await fetch('http://localhost:8000/execute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({inputs: {message}})
  });
  return response.json();
}

// src/components/Chat.tsx
import { useState } from 'react';
import { executeWorkflow } from '../api/workflow';

export function Chat() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await executeWorkflow(message);
    setResponse(result.outputs.chat.response);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask a question..."
      />
      <button type="submit">Send</button>
      {response && <div>{response}</div>}
    </form>
  );
}
```

## Streaming Responses

```typescript
// Backend (Python)
api = WorkflowAPI(workflow.build(), streaming=True)

// Frontend (React)
async function streamWorkflow(message: string) {
  const response = await fetch('http://localhost:8000/stream', {
    method: 'POST',
    body: JSON.stringify({inputs: {message}})
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    console.log(chunk);  // Update UI incrementally
  }
}
```

<!-- Trigger Keywords: react integration, react kailash, kailash frontend, react workflows -->
