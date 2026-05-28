# Prompt-Based Hooks Comprehensive Guide

Prompt-based hooks enable LLM-powered decision-making for hooks, replacing deterministic bash scripts with context-aware intelligence.

## Overview

**What Are Prompt-Based Hooks?**

Prompt-based hooks (`type: "prompt"`) send hook context to an LLM (Claude Haiku) for intelligent evaluation. Instead of writing complex bash/python logic, you write a natural language prompt that describes the decision criteria.

**Example Use Cases**:
- Decide if Claude should stop based on conversation analysis
- Validate user prompts with semantic understanding
- Make context-aware permission decisions
- Evaluate subagent task completion with full context

**Key Advantages Over Command Hooks**:
| Aspect | Command Hooks | Prompt Hooks |
|--------|---|---|
| **Decision Logic** | Deterministic (pattern matching) | Contextual (LLM evaluation) |
| **Implementation** | Requires scripting | Just write a prompt |
| **Flexibility** | Limited to programmed patterns | Adapts to context |
| **Complexity** | Simple rules work well | Better for nuanced decisions |
| **Speed** | Very fast (local) | Slower (API call) |

## Supported Hook Events

Prompt-based hooks work with these event types:

**Primary Use Cases** (recommended):
- **Stop**: Decide whether Claude should continue working
- **SubagentStop**: Evaluate if subagent completed its task
- **UserPromptSubmit**: Validate user input with semantic analysis
- **PreToolUse**: Make context-aware tool permission decisions
- **PermissionRequest**: Intelligently allow/deny permission dialogs

**Less Common**:
- Other events support prompt-based hooks but are less typical

## Configuration

### Basic Structure

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Your prompt here describing the decision to make",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Configuration Fields

- **type**: Must be `"prompt"`
- **prompt**: The prompt text sent to LLM
  - Can include `$ARGUMENTS` placeholder (replaced with hook input JSON)
  - If no `$ARGUMENTS`, hook input JSON appended to prompt
- **timeout**: Maximum seconds to wait for LLM response (default: 30, max recommended: 60)

### Prompt Writing

**Best Practices for Prompt-Based Hook Prompts**:

1. **Be Specific**: Clearly state what decision to make
   ```
   # Good
   Evaluate if Claude should continue. Check if: 1) all user-requested tasks are complete, 2) no errors need fixing, 3) no follow-up work is needed. Respond with JSON.

   # Bad
   Should we continue?
   ```

2. **List Decision Criteria**:
   ```
   Criteria to evaluate:
   1. Has the user requested task been completed?
   2. Are there any errors in the conversation?
   3. Is there work mentioned but not yet started?
   4. Did the user say they're done?
   ```

3. **Include Response Format**: Tell LLM exactly what JSON to return
   ```
   Respond with JSON: {"decision": "approve" or "block", "reason": "explanation"}
   ```

4. **Reference `$ARGUMENTS`**: Use placeholder for hook input
   ```
   Hook context: $ARGUMENTS
   Evaluate the above context and decide if...
   ```

## Response Schema

### Standard Response Fields

All prompt-based hooks expect JSON response with:

```json
{
  "decision": "approve" | "block",
  "reason": "explanation of the decision"
}
```

- **decision**: "approve" allows action, "block" prevents it
- **reason**: Explanation shown to Claude (when decision is "block")

### Advanced Response Fields (Optional)

```json
{
  "decision": "approve" | "block",
  "reason": "Explanation",

  "continue": false,              // Stop entire Claude execution
  "stopReason": "message",        // Reason shown to user (with continue: false)
  "systemMessage": "warning"      // Additional message shown to user
}
```

- **continue**: If `false`, stops Claude entirely after hook runs
- **stopReason**: User-facing message (shown when continue: false)
- **systemMessage**: Additional context shown to user

### Event-Specific Responses

Different hook events have different response structures:

**For Stop/SubagentStop**:
```json
{
  "decision": "block",
  "reason": "Tasks not complete: user asked for X but it hasn't been done yet"
}
```

**For PreToolUse/PermissionRequest**:
```json
{
  "decision": "block",
  "reason": "This tool not allowed in current context"
}
```

**For UserPromptSubmit**:
```json
{
  "decision": "approve",
  "reason": "Prompt contains valid analysis request"
}
```

## Common Decision Patterns

### Pattern 1: Task Completion Analysis

**Use For**: Stop hook - decide if Claude should continue

**Prompt**:
```
You are evaluating whether Claude should stop working. Analyze the conversation:

$ARGUMENTS

Questions to answer:
1. Did the user request specific tasks? What were they?
2. Have all requested tasks been completed?
3. Are there any errors or failures mentioned?
4. Did the user indicate they're done?
5. Is there work mentioned but not started?

Respond with JSON:
{"decision": "approve" (to stop) or "block" (to continue), "reason": "brief explanation"}
```

**Example Hook Input**:
```json
{
  "session_id": "abc123",
  "hook_event_name": "Stop"
}
```

### Pattern 2: Semantic Prompt Validation

**Use For**: UserPromptSubmit hook - validate user intent

**Prompt**:
```
Evaluate this user prompt for validity: $ARGUMENTS

Checks:
1. Is the request clear and actionable?
2. Does it violate any security policies? (no requests for secrets, credentials, or harmful actions)
3. Is it relevant to the current project context?
4. Should it be processed or blocked?

Respond: {"decision": "approve" or "block", "reason": "..."}
```

### Pattern 3: Context-Aware Permission

**Use For**: PreToolUse hook - intelligent tool decisions

**Prompt**:
```
Determine if this tool call is appropriate given the context: $ARGUMENTS

Consider:
1. What tool is being called?
2. What's the input to this tool?
3. Is it safe and appropriate for current conversation?
4. Any security concerns?

Respond: {"decision": "approve" or "block", "reason": "..."}
```

### Pattern 4: Subagent Task Verification

**Use For**: SubagentStop hook - evaluate subagent completion

**Prompt**:
```
Did the subagent complete its assigned task? Context: $ARGUMENTS

Evaluate:
1. What was the subagent asked to do?
2. What did the subagent produce?
3. Does the output satisfy the requirements?
4. Is there additional work needed?

Response: {"decision": "approve" (done) or "block" (needs more work), "reason": "..."}
```

## Step-by-Step Examples

### Example 1: Intelligent Stop Hook

Create `.claude/settings.json` with:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. The conversation context is below:\n\n$ARGUMENTS\n\nAnalyze and determine:\n1. Has the user's stated request been completed?\n2. Are there any reported errors or problems?\n3. Is there incomplete work mentioned?\n4. Did the user indicate they want to stop?\n\nRespond with JSON:\n{\"decision\": \"approve\" (stop) or \"block\" (continue), \"reason\": \"brief explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**How It Works**:
1. When Claude finishes responding, Stop hook triggers
2. Hook input JSON (session context) appended to prompt
3. Haiku LLM evaluates if work is complete
4. Returns: `{"decision": "approve", "reason": "User confirmed task is done"}`
5. Claude stops (or continues if decision is "block")

### Example 2: Secure Prompt Validation

`.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate this user prompt:\n\n$ARGUMENTS\n\nCheck for:\n1. Sensitive info (API keys, passwords, credentials) - BLOCK if found\n2. Malicious intent - BLOCK if suspicious\n3. Clarity and legitimacy - APPROVE if valid\n\nRespond: {\"decision\": \"approve\" or \"block\", \"reason\": \"...\"}",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

### Example 3: MCP Tool Permission

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*__.*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Should this MCP tool call be allowed?\n\n$ARGUMENTS\n\nEvaluate:\n1. Is the tool safe and appropriate?\n2. Does the input look reasonable?\n3. Any security concerns?\n\nRespond: {\"decision\": \"approve\" or \"block\", \"reason\": \"...\"}",
            "timeout": 25
          }
        ]
      }
    ]
  }
}
```

## Advanced Features

### Using `$ARGUMENTS` Placeholder

Instead of appending input, explicitly place it in prompt:

```json
{
  "type": "prompt",
  "prompt": "Context: $ARGUMENTS\n\nMake decision based on above context..."
}
```

**Benefits**:
- Control where input appears in prompt
- Prepend instructions before context
- Cleaner prompt formatting

### Multiple Criteria Decision Trees

Complex decisions with weighted criteria:

```json
{
  "type": "prompt",
  "prompt": "Evaluate task completion with weighted criteria:\n\n$ARGUMENTS\n\nCriteria (weight):\n- Primary objective completed (70%)\n- No critical errors (20%)\n- User satisfied (10%)\n\nDecision matrix:\n- All criteria met: approve\n- Primary + one secondary: block (continue)\n- Primary failing: block (continue)\n\nRespond: {\"decision\": \"approve\" or \"block\", \"reason\": \"...\"}"
}
```

### Combining with Command Hooks

Use both prompt and command hooks on same event:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "log_session_metrics.sh"  // Log first
          },
          {
            "type": "prompt",
            "prompt": "Should we continue?"    // Then decide
          }
        ]
      }
    ]
  }
}
```

Both hooks execute in parallel.

## Performance Considerations

### Timeout Tuning

- **Default**: 30 seconds
- **Recommended Range**: 20-45 seconds
- **Quick Decisions**: 15-20 seconds (simple criteria)
- **Complex Decisions**: 30-45 seconds (multi-step analysis)

**Example**:
```json
{
  "type": "prompt",
  "timeout": 25  // Reasonable for most decisions
}
```

### Cost Implications

Each prompt hook makes an API call to Claude Haiku. Consider:
- **Stop Hook**: Called every time Claude finishes (frequent)
- **UserPromptSubmit Hook**: Called for every user input (frequent)
- **PreToolUse Hook**: Called for every tool use (very frequent for Stop/UserPromptSubmit)

**Optimization**:
- Use command hooks for simple pattern matching
- Reserve prompt hooks for decisions requiring context
- Don't use prompt hooks on high-frequency events unless necessary

## Troubleshooting

### Hook Not Firing

**Symptoms**: Prompt hook configured but never executes

**Debug Steps**:
1. Check hook is in correct settings file (user/project/local)
2. Restart Claude Code to reload
3. Run `/hooks` command to verify hook is registered
4. Check event type is correct
5. Enable debug mode: `claude --debug`

### Invalid JSON Response

**Symptoms**: "Hook failed with invalid JSON" error

**Causes**:
- LLM returned invalid JSON
- Response missing required `decision` field
- Malformed JSON syntax

**Fix**:
- Be more explicit in prompt: "Return ONLY valid JSON, no explanation"
- Show exact format: `{"decision": "approve", "reason": "explanation"}`
- Add validation instruction: "Ensure JSON is valid and parseable"

### Timeout Exceeded

**Symptoms**: Prompt hook times out before LLM responds

**Solutions**:
- Increase timeout: `"timeout": 45`
- Simplify prompt (shorter = faster)
- Reduce decision criteria
- Check network connectivity

### LLM Making Wrong Decisions

**Symptoms**: Prompt hook approves/blocks incorrectly

**Debugging**:
1. Check prompt clarity - is it unambiguous?
2. Provide examples: "Example input: X → decision should be: Y"
3. Add explicit decision rules
4. Test prompt separately before deploying
5. Refine based on actual behavior

**Example Improvement**:

Before (ambiguous):
```
Should we stop? $ARGUMENTS
```

After (clear):
```
Based on: $ARGUMENTS

Rules:
1. If all tasks complete: approve (stop)
2. If errors present: block (continue)
3. If user said "done": approve (stop)
4. If work mentioned but not started: block (continue)

Respond: {"decision": "approve" or "block", "reason": "..."}
```

## Best Practices

### 1. Write Clear, Unambiguous Prompts

✅ **Good**:
```
Evaluate if the user's request has been completely fulfilled.
"Completely fulfilled" means:
- All specific tasks mentioned are done
- No errors remain
- User indicated satisfaction
```

❌ **Bad**:
```
Is the task done?
```

### 2. Include Context Analysis in Prompt

✅ **Good**: Analyze the conversation, identify requests, evaluate completion
❌ **Bad**: Just ask a yes/no question without context

### 3. Be Specific About Decision Criteria

✅ **Good**: List 3-5 specific criteria that determine the decision
❌ **Bad**: Leave decision criteria vague or implicit

### 4. Test Decisions Before Deploying

Test prompt hook decisions in isolation before using in production:
```
Mock hook input: {"key": "value"}
My prompt: "Make decision about X"
Expected: "approve" | "block"
Actual: [run and verify]
```

### 5. Use Timeouts Appropriately

- Simple decisions: 15-20 seconds
- Complex decisions: 30-45 seconds
- Don't set excessive timeouts (>60 seconds)

### 6. Consider Fallback Behavior

If prompt hook fails/times out, what happens?
- Default behavior depends on event type
- Document expected fallback in comments

### 7. Combine with Command Hooks Strategically

Use prompt hooks for decisions, command hooks for logging/side effects:

```json
{
  "hooks": [
    {"type": "command", "command": "log_event.sh"},    // Log first
    {"type": "prompt", "prompt": "Make decision"}       // Then decide
  ]
}
```

## Comparison with Command Hooks

### When to Use Prompt Hooks

- ✅ Decisions require understanding context
- ✅ Multiple criteria to evaluate
- ✅ Natural language understanding needed
- ✅ Conversation analysis required
- ✅ Complex conditionals would be messy in bash

### When to Use Command Hooks

- ✅ Simple pattern matching
- ✅ File operations or system commands
- ✅ Deterministic rules
- ✅ Performance-critical (Stop hook called frequently)
- ✅ No network/API calls desired

### Example Decision

**Scenario**: Decide if Claude should stop

**Command Hook Approach**:
```bash
#!/bin/bash
# Check if stop_hook_active is true (prevent loops)
STOP_ACTIVE=$(echo "$INPUT" | grep -o '"stop_hook_active":\s*\(true\|false\)' | grep -o '\(true\|false\)$')
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0  # Allow stop (prevent loop)
fi
exit 2    # Block stop (continue)
```

**Prompt Hook Approach**:
```json
{
  "type": "prompt",
  "prompt": "Should Claude stop? Check if stop_hook_active to prevent loops. $ARGUMENTS"
}
```

The prompt version is clearer and handles edge cases better through natural language reasoning.

## Limitations & Considerations

### Latency

Prompt hooks add API call latency:
- Network: ~500ms-1000ms
- LLM Processing: ~1000-2000ms
- Total: ~1.5-3 seconds per hook

This is acceptable for Stop/UserPromptSubmit but noticeable for PreToolUse (called frequently).

### Model Limitations

LLM responses are non-deterministic:
- Same input might produce different decisions sometimes
- Improve consistency with explicit decision rules in prompt
- Test across multiple scenarios

### Cost

Each prompt hook = one Claude API call:
- Stop Hook: Called once per agent response (~dozens per session)
- UserPromptSubmit: Called per user input (~tens per session)
- PreToolUse: Called per tool (~hundreds per session)

Plan accordingly for usage-based pricing.

### No File System Access

Unlike command hooks, prompt hooks cannot:
- Read/write files
- Execute commands
- Access environment variables
- Perform system operations

For those capabilities, use command hooks.

## Migration Guide: Command to Prompt

### Scenario: Complex bash rule → Simple prompt

**Before (Command Hook - Complex)**:
```bash
#!/bin/bash
INPUT=$(cat)
TASKS=$(echo "$INPUT" | grep -oP '"tasks":\K[^,}]*')
ERRORS=$(echo "$INPUT" | grep -oP '"errors":\K[^,}]*')

if [ -z "$TASKS" ] || [ "$TASKS" = "0" ]; then
  exit 0  # Approve
fi

if [ ! -z "$ERRORS" ]; then
  exit 2  # Block
fi

exit 0  # Approve
```

**After (Prompt Hook - Clearer)**:
```json
{
  "type": "prompt",
  "prompt": "Should Claude continue? Context: $ARGUMENTS\n\nDecide based on:\n1. Are there pending tasks?\n2. Are there errors to fix?\n\nRespond: {\"decision\": \"approve\" (stop) or \"block\" (continue), \"reason\": \"...\"}"
}
```

The prompt version:
- Is easier to understand
- Handles edge cases better
- More maintainable long-term
- Can evolve without code changes

## Full Example: End-to-End Setup

**Goal**: Stop hook that intelligently decides if Claude should continue

**Step 1**: Create `.claude/settings.json`

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are Claude's continuation evaluator. Analyze the conversation context below and decide if Claude should stop or continue working.\n\nContext: $ARGUMENTS\n\nEvaluation criteria:\n1. **Task Completion**: Has the user's stated task been completed?\n2. **Error Resolution**: Are there unresolved errors mentioned?\n3. **User Intent**: Did the user indicate they're done?\n4. **Follow-up Work**: Is there additional work mentioned but not started?\n\nDecision rules:\n- Approve (stop) if: Task is complete AND no errors AND user seems satisfied\n- Block (continue) if: Task incomplete OR errors present OR follow-up work exists\n\nRespond with JSON (no other text):\n{\"decision\": \"approve\" or \"block\", \"reason\": \"brief explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Step 2**: Restart Claude Code
```bash
claude  # Restart to load new hooks
```

**Step 3**: Verify hook loaded
```
/hooks  # Check that Stop hook appears
```

**Step 4**: Test in conversation
- Ask Claude to do a task
- When Claude finishes, Stop hook fires
- LLM decides if work is complete
- Claude either stops or continues

**Step 5**: Refine based on behavior
- If Claude stops too early: Update prompt to be more demanding
- If Claude continues too long: Update prompt to recognize completion better

## See Also

- **SKILL.md**: Main skill overview and other workflows
- **hook-types-reference.md**: Complete reference for all hook event types
- **hook-schemas-reference.md**: Detailed input/output schema for each event
- **security-checklist.md**: Security considerations for all hook types
- **script-examples.md**: Command hook implementation examples
