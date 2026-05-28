---
title: v6 Tool Result Access Pattern
impact: CRITICAL
tags: result, toolCalls, toolResults, input, output, v6
---

## v6 Tool Result Access Pattern

**Impact: CRITICAL**

In AI SDK v6, tool calls use `input` (not `args`) and results are in a separate `toolResults` array with `output` property.

**Incorrect (v5 patterns):**

```typescript
// ❌ WRONG - args and toolResult don't exist in v6
const toolCalls = result.steps
  .flatMap(step => step.toolCalls || [])
  .map(call => ({
    name: call.toolName,
    args: call.args,           // ❌ Wrong property
    result: call.toolResult,   // ❌ Wrong property
  }))
```

**Correct (v6 pattern):**

```typescript
// ✅ CORRECT - use input and join with toolResults
const toolCalls = result.steps.flatMap((step) => {
  // Build map of toolCallId -> output
  const resultsMap = new Map(
    (step.toolResults || []).map((r) => [r.toolCallId, r.output])
  )

  return (step.toolCalls || []).map((tc) => ({
    name: tc.toolName,
    args: tc.input as Record<string, unknown>,  // ✅ input not args
    result: resultsMap.get(tc.toolCallId),       // ✅ from toolResults
  }))
})
```

**Key v6 changes:**
- `tc.args` → `tc.input`
- `tc.toolResult` → Look up in `step.toolResults` by `toolCallId`, access `.output`

Reference: [Result Object](https://sdk.vercel.ai/docs/ai-sdk-core/generating-text#result-object)
