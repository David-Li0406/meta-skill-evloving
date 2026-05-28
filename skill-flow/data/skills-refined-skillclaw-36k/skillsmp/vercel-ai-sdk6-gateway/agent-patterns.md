# Agent Patterns Reference

Comprehensive patterns for building production AI agents with AI SDK v6.

## ToolLoopAgent Architecture

### Core Structure
```typescript
import { ToolLoopAgent, tool, stepCountIs, hasToolCall } from 'ai';
import { z } from 'zod';

const agent = new ToolLoopAgent({
  model: 'anthropic/claude-sonnet-4',
  id: 'unique-agent-id',
  instructions: 'System prompt defining agent behavior',
  tools: { /* tool definitions */ },
  stopWhen: stopCondition,
  maxOutputTokens: 4096,
  providerOptions: { /* gateway options */ },
});
```

### Agent Interface
```typescript
interface Agent<TOOLS, OUTPUT> {
  version: 'agent-v1';
  id: string | undefined;
  tools: TOOLS;
  generate(options: AgentCallParameters): Promise<GenerateTextResult>;
  stream(options: AgentCallParameters): Promise<StreamTextResult>;
}
```

## Agent Patterns

### 1. Simple Augmented LLM
Agent with search and analysis tools:

```typescript
const researchAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: `Research assistant with search access.
  1. Always search for information first
  2. Cross-reference multiple sources
  3. Cite sources in responses`,
  tools: {
    search: tool({
      description: 'Search for information',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => searchAPI(query),
    }),
    analyzeDocument: tool({
      description: 'Analyze document content',
      parameters: z.object({ documentId: z.string() }),
      execute: async ({ documentId }) => analyzeDoc(documentId),
    }),
  },
  stopWhen: stepCountIs(10),
});
```

### 2. Evaluator Pattern
Self-improving content generation:

```typescript
const evaluatorAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: `Quality assurance agent.
  1. Generate initial content
  2. Evaluate against quality criteria
  3. Improve until standards met`,
  tools: {
    generateContent: tool({
      description: 'Generate content',
      parameters: z.object({
        prompt: z.string(),
        attempt: z.number().default(1),
      }),
      execute: async ({ prompt, attempt }) => generateContent(prompt, attempt),
    }),
    evaluateQuality: tool({
      description: 'Evaluate content quality (1-10)',
      parameters: z.object({
        content: z.string(),
        criteria: z.array(z.string()),
      }),
      execute: async ({ content, criteria }) => {
        const scores = evaluateContent(content, criteria);
        return {
          scores,
          meetsStandards: scores.average >= 8,
        };
      },
    }),
    improveContent: tool({
      description: 'Improve based on feedback',
      parameters: z.object({
        content: z.string(),
        feedback: z.string(),
      }),
      execute: async ({ content, feedback }) => improveContent(content, feedback),
    }),
  },
  stopWhen: stepCountIs(20),
});
```

### 3. Parallel Processing Agent
Concurrent task execution:

```typescript
const parallelAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: `Research assistant for parallel tasks.
  1. Break complex tasks into subtasks
  2. Execute research streams in parallel
  3. Synthesize results`,
  tools: {
    splitTask: tool({
      description: 'Split task into parallel subtasks',
      parameters: z.object({
        task: z.string(),
        numParts: z.number().default(3),
      }),
      execute: async ({ task, numParts }) => ({
        subtasks: Array.from({ length: numParts }, 
          (_, i) => `${task} - Part ${i + 1}`),
      }),
    }),
    researchTopic: tool({
      description: 'Research a topic',
      parameters: z.object({
        topic: z.string(),
        depth: z.enum(['shallow', 'medium', 'deep']).default('medium'),
      }),
      execute: async ({ topic, depth }) => researchTopic(topic, depth),
    }),
    synthesize: tool({
      description: 'Synthesize research results',
      parameters: z.object({
        results: z.array(z.string()),
      }),
      execute: async ({ results }) => synthesizeResults(results),
    }),
  },
  stopWhen: stepCountIs(15),
});
```

### 4. Router Agent (Multi-Agent Orchestration)
Delegate to specialized sub-agents:

```typescript
// Specialized agents
const refundAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: 'Refund specialist. Verify orders, check eligibility, process refunds.',
  tools: { verifyOrder, processRefund },
  stopWhen: stepCountIs(5),
});

const techSupportAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: 'Technical support. Diagnose issues, provide solutions.',
  tools: { diagnoseIssue, provideSolution },
  stopWhen: stepCountIs(5),
});

// Router agent
const routerAgent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  instructions: 'Classify customer intent and delegate to specialists.',
  tools: {
    classifyIntent: tool({
      description: 'Classify customer message',
      parameters: z.object({ message: z.string() }),
      execute: async ({ message }) => {
        if (message.includes('refund')) return { intent: 'refund' };
        if (message.includes('error')) return { intent: 'tech_support' };
        return { intent: 'general' };
      },
    }),
    delegateToRefund: tool({
      description: 'Delegate to refund agent',
      parameters: z.object({ message: z.string() }),
      execute: async ({ message }) => {
        const result = await refundAgent.generate({ prompt: message });
        return result.text;
      },
    }),
    delegateToTechSupport: tool({
      description: 'Delegate to tech support',
      parameters: z.object({ message: z.string() }),
      execute: async ({ message }) => {
        const result = await techSupportAgent.generate({ prompt: message });
        return result.text;
      },
    }),
  },
  stopWhen: stepCountIs(10),
});
```

### 5. Orchestrator-Worker Pattern
Complex project coordination:

```typescript
// Worker agents
const researchWorker = new ToolLoopAgent({ /* ... */ });
const analysisWorker = new ToolLoopAgent({ /* ... */ });
const synthesisWorker = new ToolLoopAgent({ /* ... */ });

// Orchestrator
const orchestrator = new ToolLoopAgent({
  model: 'anthropic/claude-opus-4',
  instructions: `Project orchestrator.
  1. Break down complex tasks
  2. Delegate to worker agents
  3. Coordinate results
  4. Ensure quality`,
  tools: {
    planProject: tool({
      description: 'Create project plan',
      parameters: z.object({ task: z.string() }),
      execute: async ({ task }) => createProjectPlan(task),
    }),
    assignToResearch: tool({
      description: 'Assign research task',
      parameters: z.object({ task: z.string() }),
      execute: async ({ task }) => researchWorker.generate({ prompt: task }),
    }),
    assignToAnalysis: tool({
      description: 'Assign analysis task',
      parameters: z.object({ data: z.string() }),
      execute: async ({ data }) => analysisWorker.generate({ prompt: data }),
    }),
    assignToSynthesis: tool({
      description: 'Synthesize results',
      parameters: z.object({ inputs: z.array(z.string()) }),
      execute: async ({ inputs }) => 
        synthesisWorker.generate({ prompt: inputs.join('\n') }),
    }),
  },
  stopWhen: stepCountIs(30),
});
```

## Stop Conditions

### Built-in Conditions
```typescript
import { stepCountIs, hasToolCall } from 'ai';

// Stop after N steps
stopWhen: stepCountIs(10)

// Stop when tool called
stopWhen: hasToolCall('finalAnswer')
```

### Custom Conditions
```typescript
stopWhen: async ({ steps, toolCalls }) => {
  // Stop if max steps reached
  if (steps.length >= 20) return true;
  
  // Stop if final answer provided
  const lastStep = steps.at(-1);
  if (lastStep?.finishReason === 'stop') return true;
  
  // Stop if specific tool called
  const hasAnswer = toolCalls?.some(tc => tc.toolName === 'finalAnswer');
  if (hasAnswer) return true;
  
  return false;
}
```

## Tool Design Patterns

### Production-Safe Tool
```typescript
const searchDocs = tool({
  description: 'Search product documentation',
  inputSchema: z.object({
    q: z.string().min(2).max(200),
    limit: z.number().int().min(1).max(10).default(5),
  }),
  execute: async ({ q, limit }, ctx) => {
    // Get user from context, not model
    const results = await docs.search(q, { 
      limit, 
      userId: ctx.user.id 
    });
    
    // Curate output
    return {
      hits: results.map(r => ({
        id: r.id,
        title: r.title,
        summary: r.snippet.slice(0, 200),
      })),
    };
  },
});
```

### Masked Tools (Dynamic Availability)
```typescript
const agent = new ToolLoopAgent({
  model: 'openai/gpt-5',
  tools: { search, analyze, report },
  prepareStep: async ({ stepNumber }) => {
    if (stepNumber < 2) {
      return { activeTools: ['search'], toolChoice: 'required' };
    }
    return { activeTools: ['analyze', 'report'] };
  },
});
```

## Manual Agent Loop
Full control over execution:

```typescript
import { generateText, ModelMessage } from 'ai';

const messages: ModelMessage[] = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'Complete this task.' },
];

let step = 0;
const maxSteps = 10;

while (step < maxSteps) {
  const result = await generateText({
    model: 'openai/gpt-5',
    messages,
    tools: { search, analyze },
  });

  messages.push(...result.response.messages);
  
  if (result.text) break; // Model produced final text
  
  // Handle tool calls manually
  for (const toolCall of result.toolCalls || []) {
    const output = await executeToolManually(toolCall);
    messages.push({
      role: 'tool',
      content: [{
        type: 'tool-result',
        toolName: toolCall.toolName,
        toolCallId: toolCall.toolCallId,
        output: { type: 'text', value: output },
      }],
    });
  }
  
  step++;
}
```

## Testing Agents

```typescript
import { strict as assert } from 'assert';

const result = await agent.generate({ prompt: 'Test query' });

// Assert tool sequence
const toolNames = result.steps.flatMap(
  s => s.toolCalls?.map(c => c.toolName) ?? []
);
assert.deepEqual(toolNames, ['search', 'analyze', 'report']);

// Assert output pattern
assert.match(result.text ?? '', /expected.*pattern/i);
```

## Agent API Routes

### Streaming Response
```typescript
import { createAgentUIStreamResponse } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  const abortController = new AbortController();
  
  return createAgentUIStreamResponse({
    agent: myAgent,
    uiMessages: messages,
    abortSignal: abortController.signal,
  });
}
```

### UI Message Stream
```typescript
import { createUIMessageStream, createUIMessageStreamResponse } from 'ai';

const stream = createUIMessageStream({
  originalMessages: messages,
  execute: async ({ writer }) => {
    const result = streamText({
      model: 'openai/gpt-5',
      messages: await convertToModelMessages(messages),
      tools: { /* ... */ },
    });
    
    writer.merge(result.toUIMessageStream({ originalMessages: messages }));
  },
});

return createUIMessageStreamResponse({ stream });
```
