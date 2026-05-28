---
name: orchestrate
description: Main orchestration workflow that analyzes complexity, recommends patterns, and executes multi-agent coordination
auto_discover: false
---

# Multi-Agent Orchestration Skill

This skill intelligently routes user requests to single or multiple agents based on complexity analysis, with transparent cost-benefit estimates and user approval gates.

## Overview

**Problem**: Simple tasks waste tokens with multi-agent execution. Complex tasks fail with single agents.

**Solution**: Analyze complexity (0-100 score) → Recommend pattern (single/sequential/parallel/hierarchical) → Show cost (1× vs 15×) → Execute with user approval.

**Research Foundation**: Multi-agent achieves 90% better results but uses 15× more tokens. Optimal at 30K+ token contexts.

## Workflow

### Step 1: Load Configuration

Load user preferences from `~/.claude/multi-agent.local.md` if it exists:

```bash
CONFIG_FILE="$HOME/.claude/multi-agent.local.md"
DEFAULT_CONFIG="${CLAUDE_PLUGIN_ROOT}/config/default-config.json"

if [ -f "$CONFIG_FILE" ]; then
  # Extract YAML frontmatter configuration
  TOKEN_BUDGET=$(grep "^token_budget:" "$CONFIG_FILE" | awk '{print $2}')
  AUTO_APPROVE_SINGLE=$(grep "^auto_approve_single:" "$CONFIG_FILE" | awk '{print $2}')
  AUTO_APPROVE_PARALLEL=$(grep "^auto_approve_parallel:" "$CONFIG_FILE" | awk '{print $2}')
else
  # Use defaults
  TOKEN_BUDGET=$(jq -r '.token_budget' "$DEFAULT_CONFIG")
  AUTO_APPROVE_SINGLE=$(jq -r '.auto_approve.single_agent' "$DEFAULT_CONFIG")
  AUTO_APPROVE_PARALLEL=$(jq -r '.auto_approve.parallel' "$DEFAULT_CONFIG")
fi

# Fallback to safe defaults
TOKEN_BUDGET=${TOKEN_BUDGET:-200000}
AUTO_APPROVE_SINGLE=${AUTO_APPROVE_SINGLE:-true}
AUTO_APPROVE_PARALLEL=${AUTO_APPROVE_PARALLEL:-false}
```

### Step 2: Analyze Request Complexity

Invoke the task-analyzer agent to get complexity analysis:

```bash
# Use Task tool to analyze request
echo "Analyzing request complexity..."

# The task-analyzer agent will use the complexity-analyzer.js script
# and return structured JSON with recommendations
```

Use the Task tool with:
- `subagent_type`: "multi-agent:task-analyzer"
- `description`: "Analyze request complexity"
- `prompt`: "Analyze this request with token budget ${TOKEN_BUDGET}: ${USER_REQUEST}"

The analyzer returns JSON with:
- `complexity_score`: 0-100
- `pattern`: single | sequential | parallel | hierarchical
- `recommended_agents`: ["agent-id-1", "agent-id-2"]
- `cost`: {single: N, multi: M, multiplier: "Xx"}
- `reasoning`: Why this pattern is recommended
- `warnings`: Budget or complexity concerns
- `alternatives`: Other viable approaches

### Step 3: Present Analysis and Get Approval

Based on complexity score and pattern, present analysis to user:

#### For Simple Tasks (score < 30)

```markdown
## Complexity Analysis

**Score**: <score>/100 (Simple task)
**Pattern**: Single agent
**Cost**: ~<single_cost> tokens

This is a straightforward task that doesn't require multi-agent coordination.

<if AUTO_APPROVE_SINGLE is true>
Proceeding with single agent execution...
<else>
Proceed? (y/N)
</if>
```

#### For Moderate Tasks (score 30-69)

```markdown
## Complexity Analysis

**Score**: <score>/100 (<Moderate/Complex>)
**Detected Domains**: <domain1>, <domain2>, ...
**Recommended Pattern**: <sequential/parallel>

**Cost Comparison**:
- Single agent:  ~<single_cost> tokens
- Multi-agent:   ~<multi_cost> tokens (<multiplier>)

**Expected Improvement**: 90% better results with multi-agent coordination

**Recommended Agents**:
- <agent-1>: <role/domain>
- <agent-2>: <role/domain>

**Reasoning**: <why this pattern is recommended>

<if warnings exist>
⚠️  **Warnings**:
- <warning-1>
- <warning-2>
</if>

<if alternatives exist>
**Alternatives**:
1. <alternative pattern> (<cost>) - <trade-offs>
</if>

Proceed with <pattern> execution? (y/N)
```

#### For Complex Tasks (score >= 70)

```markdown
## Complexity Analysis

**Score**: <score>/100 (High complexity)
**Detected Domains**: <domain1>, <domain2>, <domain3>, ...
**Recommended Pattern**: Hierarchical coordination

**Cost Comparison**:
- Single agent:  ~<single_cost> tokens
- Multi-agent:   ~<multi_cost> tokens (<multiplier>)

**Expected Improvement**: 90% better results with coordinated specialist review

**Workflow**:
<high-level workflow description from coordinator pattern>

**Reasoning**: <why hierarchical coordination is needed>

⚠️  **Note**: This will use significant tokens but provides comprehensive multi-specialist coverage.

Proceed with hierarchical coordination? (y/N)
```

Use AskUserQuestion tool to get approval unless auto-approve is configured for the pattern.

### Step 4: Execute Selected Pattern

Based on approved pattern, execute the appropriate workflow:

#### Pattern: Single

```bash
# Simple execution with general-purpose or domain-specific agent
AGENT_ID="<recommended_agent>"

# Invoke agent
echo "Executing with ${AGENT_ID}..."
```

Use Task tool:
- `subagent_type`: "${AGENT_ID}"
- `description`: "Execute user request"
- `prompt`: "${USER_REQUEST}"

#### Pattern: Sequential

```bash
# Sequential execution with dependency chain
AGENTS=("<agent-1>" "<agent-2>")

# Phase 1
echo "Phase 1: ${AGENTS[0]}"
RESULT_1=$(invoke_agent "${AGENTS[0]}" "$USER_REQUEST")

# Phase 2 (with context from Phase 1)
echo "Phase 2: ${AGENTS[1]}"
RESULT_2=$(invoke_agent "${AGENTS[1]}" "$USER_REQUEST with context: $RESULT_1")

# Present combined results
echo "Sequential workflow completed."
echo "Results from ${AGENTS[@]}"
```

Use Task tool sequentially, passing context forward:
1. Invoke agent 1 with original request
2. Wait for completion
3. Invoke agent 2 with original request + agent 1 results as context

#### Pattern: Parallel

```bash
# Parallel execution with independent agents
AGENTS=("<agent-1>" "<agent-2>" "<agent-3>")

echo "Launching parallel analysis with ${#AGENTS[@]} agents..."
```

Use Task tool with **multiple invocations in same message** for parallel execution:
- Invoke agent-1, agent-2, agent-3 simultaneously
- All agents receive the same original request
- Wait for all to complete
- Collect results

Then invoke aggregator agent:
- `subagent_type`: "multi-agent:aggregator"
- `description`: "Synthesize parallel results"
- `prompt`: "Synthesize results from: <agent-outputs>"

#### Pattern: Hierarchical

```bash
# Hierarchical coordination
echo "Initiating hierarchical coordination..."
```

Use Task tool:
- `subagent_type`: "multi-agent:coordinator"
- `description`: "Coordinate complex multi-agent workflow"
- `prompt`: "${USER_REQUEST} with specialists: <recommended_agents>"

The coordinator agent will handle decomposition, delegation, and synthesis internally.

### Step 5: Track Metrics (Optional)

Log execution for learning and improvement:

```bash
METRICS_FILE="$HOME/.claude/multi-agent-metrics.jsonl"

echo "{
  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"complexity_score\": ${SCORE},
  \"pattern\": \"${PATTERN}\",
  \"agents\": [${AGENTS[@]}],
  \"cost_estimate\": ${COST},
  \"user_approved\": true
}" >> "$METRICS_FILE"
```

## Helper Functions

### invoke_agent()

Wrapper for Task tool invocation:

```bash
invoke_agent() {
  local agent_id="$1"
  local prompt="$2"
  local description="${3:-Execute task}"

  # Use Task tool (this is pseudocode - actual implementation uses Task tool)
  # Task(subagent_type: "$agent_id", description: "$description", prompt: "$prompt")
}
```

### check_budget()

Validate token budget before execution:

```bash
check_budget() {
  local estimated_cost="$1"
  local budget="$2"

  if [ "$estimated_cost" -gt "$budget" ]; then
    echo "⚠️  Warning: Estimated cost ($estimated_cost) exceeds budget ($budget)"
    echo "This may result in incomplete execution or hitting token limits."
    return 1
  fi
  return 0
}
```

### present_alternatives()

Show alternative patterns when budget is tight:

```bash
present_alternatives() {
  local alternatives="$1"  # JSON array from analyzer

  echo "Alternative approaches:"
  echo "$alternatives" | jq -r '.[] | "- \(.pattern): \(.cost) tokens - \(.trade_offs)"'
}
```

## Configuration

### Default Configuration (`config/default-config.json`)

```json
{
  "token_budget": 200000,
  "complexity_thresholds": {
    "simple": 30,
    "moderate": 50,
    "complex": 70
  },
  "auto_approve": {
    "single_agent": true,
    "sequential": false,
    "parallel": false,
    "hierarchical": false
  },
  "cost_awareness": {
    "show_estimates": true,
    "warn_on_high_multiplier": true,
    "warn_threshold": 10
  }
}
```

### User Configuration (`~/.claude/multi-agent.local.md`)

```markdown
---
token_budget: 150000
auto_approve_single: true
auto_approve_parallel: false
auto_approve_sequential: false
preferred_agents:
  security: "security-auditor"
  testing: "test-automator"
---

# My Multi-Agent Preferences

I prefer conservative token usage and want approval before multi-agent execution.
Always involve security-auditor for authentication code.
```

## Error Handling

### Agent Failures

If an agent invocation fails:

```bash
if [ $? -ne 0 ]; then
  echo "❌ Agent ${AGENT_ID} failed"
  echo "Attempting fallback to general-purpose agent..."
  invoke_agent "general-purpose" "$USER_REQUEST"
fi
```

### Budget Exceeded

If estimated cost exceeds budget:

```bash
if ! check_budget "$ESTIMATED_COST" "$TOKEN_BUDGET"; then
  echo "Options:"
  echo "1. Use simpler pattern (reduce agents)"
  echo "2. Focus on highest priority domain only"
  echo "3. Proceed anyway (may hit limits)"

  # Use AskUserQuestion to get choice
fi
```

### Invalid Analysis

If task-analyzer returns invalid JSON or unexpected format:

```bash
if ! echo "$ANALYSIS" | jq empty 2>/dev/null; then
  echo "⚠️  Analysis parsing failed. Defaulting to single agent."
  PATTERN="single"
  AGENTS=("general-purpose")
fi
```

## Success Criteria

✅ Complexity scoring accurate (>85% match with manual assessment)
✅ Token estimates within ±20% of actual usage
✅ User approval rate >70% for multi-agent suggestions
✅ Clear cost-benefit communication
✅ Graceful degradation on failures
✅ Respects token budget constraints

## Examples

### Example 1: Simple Task Auto-Routed

**Input**: "Fix typo in README.md"

**Analysis**:
- Score: 12 (simple)
- Pattern: single
- Agent: general-purpose
- Cost: 7,000 tokens

**Output**: Auto-executes with general-purpose agent (no approval needed if configured)

### Example 2: Moderate Task with Approval

**Input**: "Review authentication module for security issues"

**Analysis**:
- Score: 48 (moderate)
- Pattern: sequential
- Agents: security-auditor → code-reviewer
- Cost: 50,000 tokens (4× multiplier)

**Output**: Shows cost comparison, asks approval, executes sequentially if approved

### Example 3: Complex Task with Hierarchical Coordination

**Input**: "Comprehensive code review including security audit, performance analysis, and test coverage validation"

**Analysis**:
- Score: 78 (complex)
- Pattern: hierarchical
- Coordinator orchestrates: security-auditor, performance-engineer, test-automator
- Cost: 180,000 tokens (9× multiplier)

**Output**: Explains workflow, shows cost, requires user approval, coordinator handles orchestration

---

This skill is the intelligent routing layer that ensures optimal agent utilization based on task complexity and user preferences, with full cost transparency.
