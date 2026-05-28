---
name: vercel-ai-sdk-5
description: Use this skill when building AI chat features with Vercel AI SDK v5, including handling breaking changes from v4.
---

# Skill body

## Breaking Changes from AI SDK 4

```typescript
// ❌ AI SDK 4 (OLD)
import { useChat } from "ai";
const { messages, handleSubmit, input, handleInputChange } = useChat({
  api: "/api/chat",
});

// ✅ AI SDK 5 (NEW)
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";

const { messages, sendMessage } = useChat({
  transport: new DefaultChatTransport({ api: "/api/chat" }),
});
```

## Client Setup

```typescript
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { useState } from "react";

export function Chat() {
  const [input, setInput] = useState("");

  const { messages, sendMessage, isLoading, error } = useChat({
    transport: new DefaultChatTransport({ api: "/api/chat" }),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input });
    setInput("");
  };

  return (
    <div>
      <div>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>

      {error && <div>Error: {error.message}</div>}
    </div>
  );
}
```

## UIMessage Structure (v5)

```typescript
// ❌ Old: message.content was a string
// ✅ New: message.parts is an array

interface UIMessage {
  id: string;
  role: "user" | "assistant" | "system";
  parts: MessagePart[];
}

type MessagePart =
  | { type: "text"; text: string }
  | { type: "image"; image: string }
  | { type: "tool-call"; toolCallId: string; toolName: string; args: unknown }
  | { type: "tool-result"; toolCallId: string; result: unknown };

// Extract text from parts
function getMessageText(message: UIMessage): string {
  return message.parts
    .filter((part): part is { type: "text"; text: string } => part.type === "text")
    .map((part) => part.text)
    .join("");
}

// Render message
function Message({ message }: { message: UIMessage }) {
  return (
    <div className={message.role === "user" ? "user-message" : "assistant-message"}>
      {getMessageText(message)}
    </div>
  );
}
```