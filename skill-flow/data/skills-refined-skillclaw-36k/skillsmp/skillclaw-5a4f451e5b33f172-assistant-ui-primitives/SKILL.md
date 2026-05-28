---
name: assistant-ui-primitives
description: Use this skill when customizing chat UI components with assistant-ui's unstyled primitives.
---

# Skill body

**Always consult [assistant-ui.com/llms.txt](https://assistant-ui.com/llms.txt) for the latest API.**

This skill provides guidance on using composable, unstyled components that follow Radix UI patterns.

## Import

```tsx
import {
  ThreadPrimitive,
  ComposerPrimitive,
  MessagePrimitive,
  ActionBarPrimitive,
  BranchPickerPrimitive,
  AttachmentPrimitive,
  ThreadListPrimitive,
  ThreadListItemPrimitive,
} from "@assistant-ui/react";
```

## Primitive Parts

| Primitive | Key Parts |
|-----------|-----------|
| `ThreadPrimitive` | `.Root`, `.Viewport`, `.Messages`, `.Empty`, `.ScrollToBottom` |
| `ComposerPrimitive` | `.Root`, `.Input`, `.Send`, `.Cancel`, `.Attachments` |
| `MessagePrimitive` | `.Root`, `.Content`, `.Avatar`, `.If` |
| `ActionBarPrimitive` | `.Copy`, `.Edit`, `.Reload`, `.Speak` |
| `BranchPickerPrimitive` | `.Previous`, `.Next`, `.Number`, `.Count` |

## Custom Thread Example

```tsx
function CustomThread() {
  return (
    <ThreadPrimitive.Root className="flex flex-col h-full">
      <ThreadPrimitive.Empty>
        <div className="flex-1 flex items-center justify-center">
          Start a conversation
        </div>
      </ThreadPrimitive.Empty>

      <ThreadPrimitive.Viewport className="flex-1 overflow-y-auto p-4">
        <ThreadPrimitive.Messages components={{
          UserMessage: CustomUserMessage,
          AssistantMessage: CustomAssistantMessage,
        }} />
      </ThreadPrimitive.Viewport>

      <ComposerPrimitive.Root className="border-t p-4 flex gap-2">
        <ComposerPrimitive.Input className="flex-1 rounded-lg border px-4 py-2" />
        <ComposerPrimitive.Send className="bg-blue-500 text-white px-4 py-2 rounded-lg">
          Send
        </ComposerPrimitive.Send>
      </ComposerPrimitive.Root>
    </ThreadPrimitive.Root>
  );
}
```

## Conditional Rendering

```tsx
<MessagePrimitive.If user>User only</MessagePrimitive.If>
<MessagePrimitive.If assistant>Assistant only</MessagePrimitive.If>
```