# Function tools reference

Function tools let your agent call external functions during conversations.

## Basic function tool with zod

```typescript
import { voice, llm } from '@livekit/agents';
import { z } from 'zod';

const assistant = new voice.Agent({
  instructions: 'You are a helpful assistant.',
  tools: {
    getWeather: llm.tool({
      description: 'Get the current weather for a location',
      parameters: z.object({
        location: z.string().describe('The city name to get weather for'),
      }),
      execute: async ({ location }) => {
        return `The weather in ${location} is sunny and 72°F`;
      },
    }),
  },
});
```

## Tool with multiple parameters

```typescript
const bookAppointment = llm.tool({
  description: 'Book an appointment',
  parameters: z.object({
    date: z.string().describe('The date in YYYY-MM-DD format'),
    time: z.string().describe('The time in HH:MM format'),
    service: z.enum(['haircut', 'coloring', 'styling']).describe('Type of service'),
    notes: z.string().optional().describe('Optional additional notes'),
  }),
  execute: async ({ date, time, service, notes }) => {
    return `Booked ${service} for ${date} at ${time}`;
  },
});
```

## Tool with enum values

```typescript
const roomNameSchema = z.enum(['bedroom', 'living room', 'kitchen', 'bathroom', 'office']);

const toggleLight = llm.tool({
  description: 'Turn a light on or off in a room',
  parameters: z.object({
    room: roomNameSchema.describe('The room to control'),
    switchTo: z.enum(['on', 'off']).describe('The desired state'),
  }),
  execute: async ({ room, switchTo }) => {
    return `The light in the ${room} is now ${switchTo}`;
  },
});
```

## Raw parameter schema (without zod)

```typescript
const openGate = llm.tool({
  description: 'Opens a specified gate from a predefined set of access points',
  parameters: {
    type: 'object',
    properties: {
      gateId: {
        type: 'string',
        description: 'The ID of the gate to open',
        enum: ['main_entrance', 'north_parking', 'loading_dock'],
      },
    },
    required: ['gateId'],
    additionalProperties: false,
  },
  execute: async ({ gateId }) => {
    return `The gate ${gateId} is now open`;
  },
});
```

## Tools in Agent class

```typescript
class MyAgent extends voice.Agent {
  constructor() {
    super({
      instructions: 'You are a helpful assistant.',
      tools: {
        getWeather: llm.tool({
          description: 'Get weather for a location',
          parameters: z.object({
            location: z.string(),
          }),
          execute: async ({ location }) => {
            return `Weather in ${location}: Sunny`;
          },
        }),
        calculateTip: llm.tool({
          description: 'Calculate tip for a bill',
          parameters: z.object({
            amount: z.number(),
            percentage: z.number().default(18),
          }),
          execute: async ({ amount, percentage }) => {
            const tip = amount * (percentage / 100);
            return `Tip: $${tip.toFixed(2)}`;
          },
        }),
      },
    });
  }
}
```

## Agent handoff via tools

Tools can return a new Agent to transfer control using `llm.handoff()`:

```typescript
class TriageAgent extends voice.Agent {
  constructor() {
    super({
      instructions: 'You are a triage agent.',
      tools: {
        transferToSales: llm.tool({
          description: 'Transfer to the sales department',
          parameters: z.object({}),
          execute: async () => {
            // Return handoff with optional message for the LLM
            return llm.handoff({
              agent: new SalesAgent(),
              returns: 'Transferring the user to the sales department',
            });
          },
        }),
      },
    });
  }
}

class SalesAgent extends voice.Agent {
  constructor() {
    super({
      instructions: 'You are a sales representative.',
    });
  }
}
```

## Chaining tool calls

Enable multiple tool calls in sequence:

```typescript
const session = new voice.AgentSession({
  llm: "openai/gpt-4.1-mini",
  voiceOptions: {
    maxToolSteps: 5, // Allow up to 5 chained tool calls
  },
});
```

## Tool execution events

Listen for tool execution:

```typescript
session.on(voice.AgentSessionEventTypes.FunctionToolsExecuted, (ev) => {
  console.log('Tools executed:', ev);
});
```

## Error handling

Use `llm.ToolError` to return errors to the LLM:

```typescript
import { llm } from '@livekit/agents';
import { z } from 'zod';

const lookupWeather = llm.tool({
  description: 'Look up weather for a location',
  parameters: z.object({
    location: z.string(),
  }),
  execute: async ({ location }) => {
    if (location === 'mars') {
      throw new llm.ToolError('This location is not supported yet.');
    }
    return `Weather in ${location}: Sunny, 72°F`;
  },
});
```

## Best practices

1. **Write clear descriptions** - The LLM uses them to decide when to call the tool.
2. **Use zod for type safety** - Provides validation and better type inference.
3. **Keep parameters simple** - Prefer flat objects over deeply nested structures.
4. **Return strings** - Tool results are added to conversation context.
5. **Handle errors with ToolError** - Use `llm.ToolError` to return meaningful errors to the LLM.
6. **Use enums for fixed values** - Helps the LLM choose valid options.
7. **Use llm.handoff() for agent transfers** - Return a handoff object when transitioning to another agent.
