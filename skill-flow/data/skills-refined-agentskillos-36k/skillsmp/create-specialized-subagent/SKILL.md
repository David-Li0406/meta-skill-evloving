---
name: create-specialized-subagent
description: Create specialized subagents within the specialized-subagents extension. Use when asked to create a new subagent like scout, librarian, oracle, etc.
---

# Create Specialized Subagent

Create subagents within `extensions/specialized-subagents/subagents/`.

Subagents are autonomous agents with their own tools, system prompt, and model. They run as Pi tools, streaming progress and rendering results.

## Directory Structure

```
extensions/specialized-subagents/subagents/<name>/
├── index.ts          # Main tool definition (createXxxTool, executeXxx, XXX_GUIDANCE)
├── config.ts         # Model config, provider constants
├── system-prompt.ts  # System prompt string
├── types.ts          # XxxInput, XxxDetails interfaces
├── tool-formatter.ts # formatXxxToolCall() for display
└── tools/
    ├── index.ts      # createXxxTools() aggregator
    └── <tool>.ts     # Individual tool definitions
```

## Files Overview

### types.ts

- `XxxInput`: Parameters the parent agent provides
  - Include `skills?: string[]` for optional skill passthrough
- `XxxDetails`: State for UI rendering, must include:
  - `toolCalls: SubagentToolCall[]`
  - `spinnerFrame: number`
  - `response?: string`
  - `aborted?: boolean`
  - `error?: string`
  - `usage?: SubagentUsage`
  - `skills?: string[]` - Requested skill names (from input)
  - `skillsResolved?: number` - Number of skills successfully resolved
  - `skillsNotFound?: string[]` - Skill names that were not found

### config.ts

- `MODEL`: Provider and model ID
- Optional provider type aliases for external APIs

### system-prompt.ts

- Role definition
- Available tools list
- Behavior rules per input combination
- Response format guidelines
- Constraints and guardrails

### tool-formatter.ts

- `formatXxxToolCall(tc)`: Returns `{ label, detail }` for human-readable display
- `label`: Action name ("Search", "Fetch")
- `detail`: Context (hostname, query, repo path)

### tools/

- Individual tool definitions
- Must return `cost` in details for cost aggregation:
  ```typescript
  return {
    content: [...],
    details: { ..., cost: response.costDollars?.total },
  };
  ```

### index.ts

Exports:
- `createXxxTool()`: Tool definition with `execute`, `renderCall`, `renderResult`
- `executeXxx()`: Direct execution without tool wrapper
- `XXX_GUIDANCE`: Markdown guidance for parent agent's system prompt

## Execute Function

1. Resolve skills if provided:
   ```typescript
   const { skills: skillNames } = args;
   let resolvedSkills: Skill[] = [];
   let notFoundSkills: string[] = [];
   if (skillNames && skillNames.length > 0) {
     const result = resolveSkillsByName(skillNames, ctx.cwd);
     resolvedSkills = result.skills;
     notFoundSkills = result.notFound;
   }
   ```
2. Validate inputs, return error in details if invalid (include skill info)
3. Set up spinner interval (80ms), clear in `finally`
4. Build user message, append warning if skills not found:
   ```typescript
   if (notFoundSkills.length > 0) {
     userMessage += `\n\n**Note:** The following skills were not found and could not be loaded: ${notFoundSkills.join(", ")}`;
   }
   ```
5. Call `executeSubagent()` with:
   - `skills: resolvedSkills` in config
   - `onTextUpdate` and `onToolUpdate` callbacks that include skill info in details
6. Handle abort/error states (include skill info in all return paths)
7. Use final tool calls from `result.toolCalls` for failure checks
8. Check if all tool calls failed → return error
9. Return `usage` from result (include skill info)

## renderResult States

| State | Display |
|-------|---------|
| Aborted | Warning "Aborted" + optional completion count |
| Error | Error message |
| Running + collapsed | Spinner + current tool name |
| Running + expanded | Status line + all tool calls with indicators |
| Done + collapsed | `✓` or `✗` (if all failed) + stats |
| Done + expanded | Stats + tool summary + failed tool details + markdown response |

## Registration

In `extensions/specialized-subagents/index.ts`:

1. Import the tool and guidance
2. Add guidance to `SUBAGENT_GUIDANCES` array
3. Register tool with `pi.registerTool(createXxxTool())`
4. If the subagent requires API keys, add them to `checkApiKeys()`

See the existing registration pattern in the file.

## API Key Validation

If your subagent requires external API keys, validate them at extension load time. This prevents the extension from loading if required keys are missing.

Add your required keys to `checkApiKeys()` in `extensions/specialized-subagents/index.ts`. See the existing implementation for the pattern.

## Checklist

1. Create directory: `subagents/<name>/`
2. Create `types.ts` with Input and Details interfaces
   - Add `skills?: string[]` to Input interface
   - Add `skills?`, `skillsResolved?`, `skillsNotFound?` to Details interface
3. Create `config.ts` with model configuration
4. Create `system-prompt.ts` with subagent instructions
5. Create `tools/` directory with subagent's tools
6. Create `tool-formatter.ts` for display formatting
7. Create `index.ts` with createXxxTool, executeXxx, XXX_GUIDANCE
   - Import `resolveSkillsByName` and `Skill` type from lib
   - Add `skills` parameter to TypeBox schema
   - Update tool description to mention skill support
   - Resolve skills in execute function
   - Pass `skills: resolvedSkills` to executeSubagent
   - Include skill info in all details returns
   - Show skills in renderCall if provided
8. Register in `extensions/specialized-subagents/index.ts`
9. Run `pnpm typecheck`

## Key Points

- **Details interface**: Must include `toolCalls`, `spinnerFrame`, `response`, `aborted`, `error`, `usage`, and skill tracking fields
- **Skills support**: All subagents should support optional `skills` parameter for specialized context
- **Cost tracking**: Tools must return `cost` in details for aggregation
- **Spinner**: 80ms interval, clear in finally block
- **Extensions disabled**: Subagents don't run user extensions (`extensions: []`)
- **Failed tools**: Show individually in done+expanded state
- **All failed**: Show error indicator only when ALL tools failed (partial success = success indicator)
- **Final tool calls**: Use `result.toolCalls` if present to decide failure state
- **Mark tool as failed**: When all internal tools fail, return error so parent agent sees failure
- **Skill resolution**: Use `resolveSkillsByName()` from lib to convert skill names to Skill objects
- **Skill warnings**: Append warning to user message if skills not found (don't fail the request)

## Notifications

Subagents can emit notifications to alert users. This is useful for long-running subagent tasks or when user attention is needed.

### Emitting Notifications

```typescript
const NOTIFICATION_EVENT = "ad:notification";

interface NotificationEvent {
  message: string;
  sound?: string;
}

// In execute function, after completion
pi.events.emit(NOTIFICATION_EVENT, {
  message: "Research completed",
  sound: "/System/Library/Sounds/Blow.aiff",
});
```

### When to Notify

- Subagent completes a long-running task
- Subagent encounters errors that need user attention
- Subagent needs user input (though prefer interactive tools like `ask_user`)

## Reference

Refer to the scout subagent for complete implementation:
- [subagents/scout/](../../extensions/specialized-subagents/subagents/scout/)
