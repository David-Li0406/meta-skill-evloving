---
name: complete-process
description: Transform → Validate → Optimize pipeline (auto-chained)
allowed-tools: Skill
model: sonnet
---

# Complete Process Orchestrator

Auto-chain: Transform → Validate → Optimize

## Memory Integration (START - MANDATORY)

Before starting the orchestration pipeline, load session memory:

```
# Step 1: Create memory directory (permission-free)
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load memory files (permission-free)
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")
Read(file_path=".claude/pseudo-code-prompting/patterns.md")
Read(file_path=".claude/pseudo-code-prompting/progress.md")
```

**Memory is passed through pipeline**:
- Transform step receives memory context from patterns.md
- Validation step uses patterns.md + progress.md for learned validations
- Optimization step applies patterns.md + progress.md for effective optimizations
- Memory is updated at END of pipeline with complete results

## MUST FOLLOW THIS 3-STEP WORKFLOW

When user invokes `/complete-process` or says "use complete process", run these 3 skills in sequence:

## Welcome Message and Menu System

When users invoke the plugin using trigger phrases, you MUST display a welcome message with an interactive menu for skill selection.

**See:** [references/welcome-menu-system.md](references/welcome-menu-system.md) for complete menu behavior and routing logic.

## CRITICAL IMPLEMENTATION REQUIREMENTS

### 1. Always Use Skill Tool for Sub-Skills

**MANDATORY**: When executing transformation, validation, or optimization steps, you MUST use the Skill tool to invoke the respective skills. NEVER handle these directly or inline.

```text
Skill(pseudo-code-prompting:prompt-structurer, args=user_query)
Output: transformed_pseudo_code

Display: "✓ Step 1/3 complete | Tokens: [N]
         Transformed to pseudo-code"
```

### 2. Context Window Optimization (MANDATORY)

To minimize token usage, you MUST remove intermediate outputs from the conversation flow:

**Keep Only**:

- Original user query (input)
- Final optimized output

**Remove/Don't Store**:

- Transform step output (intermediate)
- Validate step input (redundant with transform output)
- Validate step output (intermediate)
- Optimize step input (redundant with validate output)

**Implementation**: After each step completes, extract only the essential result and pass it to the next step WITHOUT including full tool outputs in subsequent messages.

**Token Savings**: By removing intermediate outputs, you save approximately **60-80% of context window usage**.

### 3. Context-Aware Tree Injection (MANDATORY)

Before invoking the transform step, you MUST ensure the context-aware tree injection occurs:

**Process**:

1. Check if user query contains implementation keywords: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`
2. If keywords detected, the UserPromptSubmit hook should have already injected PROJECT_TREE context
3. When invoking prompt-structurer skill, include any PROJECT_TREE context that was injected
4. This enables context-aware transformation with actual file paths from the project

**Why This Matters**: Without PROJECT_TREE context, transformations will be generic instead of project-specific.

**See:** [references/context-aware-detection.md](references/context-aware-detection.md) for complete context injection details.

## Execution Workflow

### Quick Mode Execution

1. **Validate Input**: Check query length (10-5000 characters)
2. **Invoke Transform Agent**:
   - Use: `Task tool with subagent_type="pseudo-code-prompting:prompt-transformer"`
   - Extract ONLY the transformed output from agent result
3. **Return Result**: Output the transformed pseudo-code
4. **Clean Up**: Do NOT keep intermediate outputs in context

### Complete Mode Execution (Automated Chain)

**CRITICAL**: This is a FULLY AUTOMATED workflow. Do NOT stop between steps. Execute the chain continuously.

1. **Validate Input**: Check query length (10-5000 characters)

2. **Step 1/3: Transform**
   - Use: `Task tool with subagent_type="pseudo-code-prompting:prompt-transformer"`
   - Pass: User query + PROJECT_TREE context + memory context
   - Agent outputs: `WORKFLOW_CONTINUES: YES` + `NEXT_AGENT: requirement-validator`
   - Extract: `transformed_output` from agent
   - Track token usage per step following [token-tracking.md](references/token-tracking.md)

3. **Check Agent Output** for workflow continuation signal
   - Look for `NEXT_AGENT: requirement-validator` in agent output
   - Immediately invoke next agent (DO NOT STOP)

4. **Step 2/3: Validate**
   - Use: `Task tool with subagent_type="pseudo-code-prompting:requirement-validator"`
   - Pass: `transformed_output` + memory context
   - Agent outputs: `WORKFLOW_CONTINUES: YES` + `NEXT_AGENT: prompt-optimizer`
   - Extract: `validation_report` from agent
   - Track token usage per step following [token-tracking.md](references/token-tracking.md)

5. **Check Agent Output** for workflow continuation signal
   - Look for `NEXT_AGENT: prompt-optimizer` in agent output
   - Immediately invoke next agent (DO NOT STOP)

6. **Step 3/3: Optimize**
   - Use: `Task tool with subagent_type="pseudo-code-prompting:prompt-optimizer"`
   - Pass: `transformed_output` + `validation_report` + memory context
   - Agent outputs: `WORKFLOW_CONTINUES: NO` + `TODO_LIST` (implementation tasks)
   - Extract: `optimized_output` + `todo_list` from agent
   - Track token usage per step following [token-tracking.md](references/token-tracking.md)

7. **Chain Complete** - Check for `WORKFLOW_CONTINUES: NO`
   - Generate implementation todos using TodoWrite tool
   - Present final output: optimized pseudo-code + reports
   - Update memory with pipeline results

8. **Final Context**: Keep ONLY original query + final optimized pseudo-code

### Chain Enforcement Protocol

**NEVER stop after one agent.** The workflow is NOT complete until the chain finishes.

After EACH agent completes, check its output for:
- `NEXT_AGENT: X` → **Immediately invoke that agent**
- `WORKFLOW_CONTINUES: NO` → **Chain complete, generate todos**

**Chain Execution Loop:**
```
1. Invoke agent via Task tool
2. Read agent output
3. Check output for:
   a. NEXT_AGENT: X → Invoke agent X immediately
   b. WORKFLOW_CONTINUES: NO → Chain complete
4. Return to step 1 until chain complete
```

### Implementation Readiness

After optimization completes:
1. **Extract optimized function** from agent output
2. **Generate implementation todos** from optimized pseudo-code parameters
3. **Present clean output**: Only the optimized function, not intermediate steps
4. **Trigger next action**: User can say "start to implement" or todos auto-create tasks

## When to Use

Use this skill when:

- You want an end-to-end workflow from natural language to optimized pseudo-code
- You need production-ready pseudo-code with validation and optimization
- You want to leverage project-specific context for transformations
- You want automated menu-driven interaction for command selection

## Workflow Modes

### Quick Transform Only

- **Duration**: 5-15 seconds
- **Steps**: Transform only
- **Output**: Raw pseudo-code
- **Best for**: Simple queries, rapid iteration

### Complete Process (Recommended)

- **Duration**: 30-90 seconds
- **Steps**: Transform → Validate → Optimize
- **Output**: Fully optimized pseudo-code with validation report
- **Best for**: Production features, complex requirements

**See:** [templates/mode-selection.md](templates/mode-selection.md) for mode selection criteria and user preference persistence.

## How It Works

### Workflow Diagram

```
User Query
    ↓
Input Validation (10-5000 chars)
    ↓
Context Detection (implementation keywords?)
    ↓
Mode Selection (Quick or Complete)
    ↓
┌─────────────────────────────────────┐
│  Quick Mode        Complete Mode    │
│  Transform         Transform        │
│      ↓                 ↓            │
│   Return           Validate         │
│                        ↓            │
│                    Optimize         │
│                        ↓            │
│                     Return          │
└─────────────────────────────────────┘
    ↓
Result: Optimized Pseudo-Code + Reports
```

**See:** [references/workflow-patterns.md](references/workflow-patterns.md) for detailed execution patterns and step-by-step implementations.

This shows users:

- **Automated Pipeline**: Seamlessly chains transform → validate → optimize
- **Mode Selection**: Choose between quick or complete processing
- **Context-Aware**: Leverages project structure for relevant transformations
- **Token Optimization**: Reduces context usage by 60-80%
- **Menu System**: Interactive command selection
- **Progress Tracking**: Real-time feedback during multi-step execution
- **Error Recovery**: Graceful fallbacks and retry options
- **Preference Persistence**: Remembers user's mode choice

### Transform Fails

### Quick Mode Output

```
Transformed: function_name(
  param1="value1",
  param2="value2"
)
```

### Complete Mode Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Fully optimized pseudo-code with all parameters]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Validation Report:
✓ PASSED CHECKS
- [Check 1]
- [Check 2]

⚠ WARNINGS
- [Warning 1]

✗ CRITICAL ISSUES
- [Issue 1]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Improvements made:
• [Improvement 1]
• [Improvement 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration: 42s
Steps Completed: 3/3
Issues Found: 2 warnings (resolved)
```

## Error Handling

### Transform Failure

```
❌ Transformation failed: Query too ambiguous

Suggestions:
- Rephrase with more specific details
- Try breaking into smaller queries
- Switch to quick mode and iterate
```

### Validation Failure (Non-Critical)

```
⚠ Validation found issues

You can:
1. Continue to optimization (recommended - may fix issues)
2. Return validation report and revise query
3. Return transformed pseudo-code as-is
```

### Optimization Failure

```
❌ Optimization failed: Unable to enhance pseudo-code

Returning validated pseudo-code instead. You can:
- Use the validated output (still production-ready)
- Manually optimize using /optimize-prompt command
```

## Best Practices

### When to Choose Quick Mode

- Simple, well-defined queries
- Rapid prototyping and iteration
- Non-critical features
- Learning and experimentation

### When to Choose Complete Mode

- Production features
- Security-sensitive implementations
- Complex multi-parameter features
- Features requiring validation/testing
- Team environments with quality standards

### Query Writing Tips

- **Be specific**: "Add OAuth authentication" → "Implement OAuth 2.0 authentication with Google provider"
- **Include constraints**: Mention performance, security, or scale requirements
- **Specify integration points**: Name files, components, or services to integrate with
- **Provide context**: Reference existing patterns or architectures

## Integration with Other Skills

### Used By Complete Process Orchestrator

- **prompt-structurer**: Performs transformation step
- **requirement-validator**: Performs validation step
- **prompt-optimizer**: Performs optimization step

### Complements

- **compress-context**: Use before orchestrator for large requirements
- **feature-dev-enhancement**: Use orchestrator output with /feature-dev
- **context-aware-transform**: Orchestrator leverages project context automatically

## Reference Documentation

- **[Welcome Menu System](references/welcome-menu-system.md)** - Interactive menu behavior and routing logic
- **[Context-Aware Detection](references/context-aware-detection.md)** - Project tree injection and context optimization
- **[Workflow Patterns](references/workflow-patterns.md)** - Detailed execution patterns and implementations
- **[Mode Selection](templates/mode-selection.md)** - Mode selection criteria and preference persistence
- **[Token Tracking](references/token-tracking.md)** - Real-time token consumption tracking and cost visibility

## Configuration

### Preference Storage

Preferences are stored in `.claude/plugin_preferences.json`:

```json
{
  "complete-process-orchestrator": {
    "preferred_mode": "complete",
    "show_progress": true,
    "remember_preference": true,
    "last_updated": "2026-01-20T12:00:00Z"
  }
}
```

## Command Aliases

- `/complete-process`
- `/complete`
- `/full-transform`
- `/orchestrate`

## Version

**1.3.0** - Refactored to modular structure with external references (under 250 lines)

## Memory Update (END - MANDATORY)

After completing the full pipeline, update memory with results:

```
# Read current memory
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")
Read(file_path=".claude/pseudo-code-prompting/progress.md")

# Update Recent Transformations with pipeline results
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="## Recent Transformations",
     new_string="## Recent Transformations
- Pipeline: Transform → Validate → Optimize (compression: X%, validation: pass/warnings, optimizations: N)")

# Update Progress with pipeline metrics
Edit(file_path=".claude/pseudo-code-prompting/progress.md",
     old_string="## Transformation History",
     new_string="## Transformation History
- [x] [Input query] - Complete pipeline (duration: Xs, issues: Y, optimizations: Z)")
```

**Update when:**
- Complete pipeline finishes successfully
- Validation issues discovered and resolved
- Optimization patterns applied effectively

**Memory Benefits:**
- Each agent in pipeline uses learned patterns
- Validation failures inform future validations
- Optimization patterns compound over time
- User preferences applied consistently

## Related Commands

- `/transform-query` - Transform only (equivalent to quick mode)
- `/validate-requirements` - Validate pseudo-code
- `/optimize-prompt` - Optimize pseudo-code
- `/compress-context` - Compress verbose requirements
