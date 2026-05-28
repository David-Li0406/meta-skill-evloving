# Output Contracts Standard

**Version**: 2026.01
**Purpose**: Explicit output contracts prevent orchestrator deadlock and enable reliable skill-to-skill communication.

## Why Output Contracts Matter

Without explicit output contracts:
- ❌ Orchestrators cannot detect completion vs. failure
- ❌ No error recovery when workers fail
- ❌ Risk of infinite loops in skill chains
- ❌ Cannot validate worker output programmatically

With explicit output contracts:
- ✅ Orchestrators parse explicit success/failure
- ✅ Clear error conditions and recovery paths
- ✅ Guaranteed stop conditions
- ✅ Programmatic output validation

## Where to Document Output Contracts

**IMPORTANT**: Output contracts are documented in the **SKILL.md body**, NOT in frontmatter. The frontmatter only supports:
- `name`
- `description`
- `disable-model-invocation` (optional)
- `user-invocable` (optional, default: true)
- `context` (optional, for worker skills)
- `agent` (optional, when context: fork)

### For Orchestrator Skills (Router)

Document output contract in the SKILL.md body:

```markdown
## Output Format

This router produces one of the following outputs:

**Routing Decision**:
```
## Routing Decision
**Action**: Route to {skill_name}
**Reason**: {justification}
```

**Blocking Issue**:
```
## Error: Cannot Proceed
**Issue**: {blocking_reason}
**Recommendation**: {next_steps}
```
```

### For Worker Skills (Forked)

Document output contract in the SKILL.md body:

```markdown
---
name: validation-worker
description: "..."
context: fork
agent: Explore
---

# Validation Worker

## Output Format

This worker MUST return output in exactly this format:

```markdown
## Validation Complete

### Quality Score: {score}/10

### Status: PASS|FAIL|ERROR

### Component Scores
- Skills: {score}/15
- Subagents: {score}/10
- Hooks: {score}/10
- MCP: {score}/5

### Critical Issues
- {issue_1}
- {issue_2}
```

## STOP WHEN

Complete this workflow when ALL of:
- [ ] Quality score calculated and formatted
- [ ] All components validated
- [ ] Report formatted exactly as specified above

## If Validation Fails

1. Return "Status: ERROR" in the output format
2. Include error context in the report
3. NEVER loop, retry, or continue without explicit instruction
```

### For Knowledge Skills (Reference)

Document informational output format:

```markdown
## Output Format

This skill provides informational content about {domain}.

**Expected Use**: Reference for orchestrator routing decisions

**If information not found**: State clearly "Information not available" and suggest alternative sources
```

## Output Contract Templates by Use Case

### Template 1: Quality Validation Output

```markdown
## Validation Complete

### Quality Score: {score}/10

### Status: PASS|FAIL|ERROR

### Component Scores
- Skills: {score}/15
- Subagents: {score}/10
- Hooks: {score}/10
- MCP: {score}/5

### Critical Issues
- {issue_1}
- {issue_2}

### Next Steps
- {recommendation_1}
- {recommendation_2}
```

### Template 2: Audit Report Output

```markdown
## Audit Results: {plugin_name}

### Structural Compliance
- ✅/❌ Skills-first architecture
- ✅/❌ Directory structure
- ✅/❌ Progressive disclosure

### Component Quality
- Skills: {score}/15
- Subagents: {score}/10
- Hooks: {score}/10
- MCP: {score}/5

### Priority Actions
- High: {high_priority}
- Medium: {medium_priority}
- Low: {low_priority}
```

### Template 3: Routing Decision Output

```markdown
## Routing Decision

**Action**: Route to {skill_name}

**Reason**: {justification}

**Context**:
- Input: {user_request}
- Analysis: {brief_analysis}
- Expected Output: {what_to_expect}
```

### Template 4: Worker Delegation Output

```markdown
## Worker Delegation

**Worker**: {worker_name}

**Context**:
- Task: {task_description}
- Input: {input_data}
- Timeout: {duration}

**Expected Output Contract**:
{output_contract}
```

### Template 5: Error Report Output

```markdown
## Error: {error_type}

**Context**: {what_was_attempted}

**Issue**: {what_failed}

**Recovery Options**:
- Option 1: {recovery_strategy_1}
- Option 2: {recovery_strategy_2}

**Recommendation**: {recommended_action}
```

## STOP WHEN Sections

Every worker skill MUST include a `## STOP WHEN` section:

```markdown
## STOP WHEN

Complete this workflow when ALL of:
- [ ] Quality score calculated and formatted
- [ ] All components validated
- [ ] Report formatted exactly as specified in output contract

If ANY step fails:
1. Log failure with context
2. Return error in output format (never loop)
3. Allow orchestrator to handle recovery
```

## Orchestrator Parsing Requirements

Orchestrators MUST parse worker output for:

### 1. Completion Detection
```markdown
Look for explicit completion marker:
- "## Validation Complete"
- "## Audit Results"
- "## Routing Decision"
```

### 2. Status Parsing
```markdown
Extract status from output:
- "Status: PASS" → Continue workflow
- "Status: FAIL" → Log and continue with recommendations
- "Status: ERROR" → Handle error explicitly
```

### 3. Error Handling
```markdown
On ERROR status:
1. Parse error context
2. Log to orchestrator state
3. Execute recovery strategy or abort with message
4. NEVER continue blindly or retry without explicit logic
```

## Anti-Patterns to Avoid

### ❌ Missing Output Contract in Body
```markdown
# BAD: No way to detect completion
# validation-worker/SKILL.md

---
name: validation-worker
context: fork
agent: Explore
---

# Instructions
Validate the plugin thoroughly.
# Missing: What output format? When is it done?
```

### ✅ Correct Pattern
```markdown
# GOOD: Explicit output contract and stop conditions
# validation-worker/SKILL.md

---
name: validation-worker
context: fork
agent: Explore
---

# Validation Worker

## Output Format

This worker MUST return output in exactly this format:

```markdown
## Validation Complete
Quality Score: {score}/10
Status: PASS|FAIL|ERROR
```

## STOP WHEN
- [ ] Quality score calculated
- [ ] Report formatted exactly as specified above

## If Validation Fails
1. Return "Status: ERROR" in output
2. Include error context
3. Never loop or retry
```

## Validation Checklist

Before considering a skill production-ready:

**Orchestrator Skills**:
- [ ] Output format documented in body (## Output Format section)
- [ ] Routing decision logic explicit
- [ ] Error handling documented (blocking issues)

**Worker Skills** (context: fork):
- [ ] Output format MUST be in exact template form
- [ ] STOP WHEN section present with explicit conditions
- [ ] Error handling specified (never loop/retry)
- [ ] Status field present (PASS/FAIL/ERROR) for parseable results
- [ ] Test cases cover success, failure, and error paths

**Knowledge Skills** (user-invocable: true):
- [ ] Informational output format documented
- [ ] Clear guidance on expected use
- [ ] Fallback behavior specified ("Information not available")

## Integration with Existing Skills

### Updating Orchestrator Skills

Add fork decision logic to router skills:

```markdown
### {action_name}
**Router Logic**:
1. Load: {knowledge_skill}
2. **Assess output volume**:
   - Large/complex task? → Delegate to {worker_name} (context: fork)
   - Simple task? → Load directly
3. **Parse explicit output**:
   - Look for "{completion_marker}"
   - Check "Status: {PASS|FAIL|ERROR}"
4. **Handle failures explicitly**:
   - On ERROR: Log and abort with message
   - On FAIL: Continue with recommendations
   - On PASS: Proceed with next step

**Output Contract**:
```
{routing_output_template}
```
```

### Updating Knowledge Skills

Add informational output contract:

```markdown
## Output Format

This skill provides informational content about {domain}.

**Expected Use**: Reference for orchestrator routing

**If information not found**: State clearly "Information not available"
```

## Examples

See these skills for complete examples:
- `meta-plugin-manager/skills/workers/validation-worker/SKILL.md` - Forked validation worker
- `meta-plugin-manager/skills/toolkit-architect/SKILL.md` - Orchestrator with fork delegation
- `meta-plugin-manager/skills/validation/toolkit-quality-validator/SKILL.md` - Knowledge skill with output contract
