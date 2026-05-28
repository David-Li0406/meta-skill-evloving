# AI Elements (UI Components)

Anthropic's official UI components for building AI interfaces.

## Installation

```bash
npm install @anthropic-ai/ai-elements streamdown shiki
```

## Core Components

```tsx
// components/ai-chat.tsx
'use client'

import {
  Conversation,
  Message,
  PromptInput,
  Reasoning,
  Sources,
  Tool,
} from '@anthropic-ai/ai-elements'
import { useChat } from '@ai-sdk/react'

export function AIChat() {
  const { messages, input, setInput, sendMessage, isLoading } = useChat()

  return (
    <div className="flex flex-col h-screen">
      <Conversation className="flex-1 overflow-auto">
        {messages.map((m) => (
          <Message
            key={m.id}
            role={m.role}
            className={m.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'}
          >
            {m.parts.map((part, i) => {
              if (part.type === 'text') {
                return <span key={i}>{part.text}</span>
              }
              if (part.type === 'tool-call') {
                return (
                  <Tool key={i} name={part.toolName} status="running">
                    <pre>{JSON.stringify(part.args, null, 2)}</pre>
                  </Tool>
                )
              }
              if (part.type === 'tool-result') {
                return (
                  <Tool key={i} name={part.toolName} status="complete">
                    <pre>{JSON.stringify(part.result, null, 2)}</pre>
                  </Tool>
                )
              }
              if (part.type === 'reasoning') {
                return (
                  <Reasoning key={i} collapsed>
                    {part.text}
                  </Reasoning>
                )
              }
              return null
            })}
          </Message>
        ))}
      </Conversation>

      <PromptInput
        value={input}
        onChange={setInput}
        onSubmit={() => sendMessage({ text: input })}
        loading={isLoading}
        placeholder="Ask me anything..."
      />
    </div>
  )
}
```

## Sources Component

```tsx
import { Sources, Source } from '@anthropic-ai/ai-elements'

function SearchResults({ results }) {
  return (
    <Sources>
      {results.map((r, i) => (
        <Source
          key={i}
          title={r.title}
          url={r.url}
          snippet={r.snippet}
        />
      ))}
    </Sources>
  )
}
```

## Tool Status Component

```tsx
import { Tool } from '@anthropic-ai/ai-elements'

function ToolDisplay({ toolCall, result }) {
  return (
    <Tool
      name={toolCall.name}
      status={result ? 'complete' : 'running'}
      icon={<ToolIcon name={toolCall.name} />}
    >
      {result ? (
        <ToolResult data={result} />
      ) : (
        <ToolLoading args={toolCall.args} />
      )}
    </Tool>
  )
}
```

## Reasoning Component

```tsx
import { Reasoning } from '@anthropic-ai/ai-elements'

function ThinkingDisplay({ thinking }) {
  return (
    <Reasoning
      collapsed={true}
      title="Reasoning Process"
      className="my-4"
    >
      {thinking.map((step, i) => (
        <div key={i} className="mb-2">
          <strong>Step {i + 1}:</strong> {step}
        </div>
      ))}
    </Reasoning>
  )
}
```

## Custom Styling

```tsx
import { Message, Conversation } from '@anthropic-ai/ai-elements'

// With Tailwind classes
<Conversation className="bg-gray-50 rounded-lg p-4">
  <Message
    role="assistant"
    className="prose prose-sm max-w-none"
  >
    {content}
  </Message>
</Conversation>

// With CSS Modules
<Message
  role="user"
  className={styles.userMessage}
>
  {content}
</Message>
```

## Integration with shadcn/ui

```tsx
import { Card, CardContent } from '@/components/ui/card'
import { Message } from '@anthropic-ai/ai-elements'

function ChatMessage({ message }) {
  return (
    <Card className={message.role === 'user' ? 'ml-auto' : 'mr-auto'}>
      <CardContent className="p-3">
        <Message role={message.role}>
          {message.parts.map(renderPart)}
        </Message>
      </CardContent>
    </Card>
  )
}
```

---

Version: 1.0.0
Source: jikime-library-vercel-ai-sdk SKILL.md
