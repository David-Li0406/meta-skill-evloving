---
name: subagents-architect
description: "Project-scoped context: fork router for .claude/agents/ with isolation and parallelism patterns. Use for creating, auditing, or refining subagents in current project. Routes to subagents-knowledge for coordination implementation. Do not use for standalone plugin agent development."
disable-model-invocation: true
---

## 🚨 MANDATORY: Read BEFORE Routing

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Project Configuration**: https://code.claude.com/docs/en/plugins
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: .claude/ structure, component organization
  - **Cache**: 15 minutes minimum

- **[MUST READ] Subagents Documentation**: https://code.claude.com/docs/en/sub-agents
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: Context fork, isolation patterns
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
- **MUST validate** all URLs are accessible before routing
- **REQUIRED** to understand subagents architecture before routing

---

# Subagents Architect

Domain router for project-scoped subagent development with isolation and parallelism focus.

## Actions

### create
**Creates subagents** in `.claude/agents/<name>.md`

**Target Directory**: `${CLAUDE_PROJECT_DIR}/.claude/agents/`

**Router Logic**:
1. Load: subagents-knowledge
2. Determine pattern:
   - **Reusable Agent File** (`.claude/agents/<name>.md`)
   - **Forked Skill** (`context: fork` in skill)
3. Generate with:
   - Clear autonomy definition
   - Coordination pattern
   - Output contracts
4. Validate: Context fork usage, isolation benefits

**Output Contract**:
```
## Subagent Created: {agent_name}

### Location
- Path: .claude/agents/{agent_name}.md
- Pattern: {pattern}

### Context Fork Usage
- Isolation needed: ✅/❌
- High-volume output: ✅/❌
- Noise prevention: ✅/❌

### Output Contract
{contract_definition}
```

### audit
**Audits subagents** for appropriate usage and effectiveness

**Router Logic**:
1. Load: subagents-knowledge
2. Check:
   - Context fork appropriateness
   - Autonomy definition clarity
   - Coordination pattern fit
   - Isolation benefits
3. Generate audit with usage scoring

**Output Contract**:
```
## Subagent Audit: {agent_name}

### Context Fork Assessment
- Appropriate usage: ✅/❌
- Isolation justified: ✅/❌
- High-volume work: ✅/❌

### Autonomy
- Definition clarity: {score}/10
- Independence level: {level}
- Coordination needs: {needs}

### Pattern Fit
- Current: {pattern}
- Appropriateness: {score}/10
- Alternatives: {alternatives}

### Issues
- {issue_1}
- {issue_2}
```

### refine
**Improves subagents** based on audit findings

**Router Logic**:
1. Load: subagents-knowledge
2. Enhance:
   - Context fork optimization
   - Autonomy definition
   - Coordination patterns
   - Output contracts
3. Validate improvements

**Output Contract**:
```
## Subagent Refined: {agent_name}

### Context Fork Optimization
- {optimization_1}
- {optimization_2}

### Autonomy Improvements
- {improvement_1}
- {improvement_2}

### Pattern Enhancement
- {enhancement_1}
- {enhancement_2}

### Effectiveness Score: {old_score} → {new_score}/10
```

## Context Fork Criteria

**Use context: fork when**:
- High-volume output (extensive analysis)
- Noisy exploration (clutters conversation)
- Isolated execution needed
- Prevents context pollution

**Don't use context: fork when**:
- Simple task execution
- Direct tool usage
- Straightforward operations
- Low complexity work

## Coordination Patterns

**Pipeline Pattern**:
- Sequential processing stages
- Data flows through stages
- Each stage transforms data
- Use for: multi-step transformations

**Router + Worker Pattern**:
- Task distribution and execution
- Router delegates to workers
- Workers return results
- Use for: parallel task execution

**Handoff Pattern**:
- Coordination between specialized agents
- State transfer between contexts
- Seamless information flow
- Use for: specialized domain handoffs

## Implementation Guidance

For detailed implementation patterns, route to subagents-knowledge or refer to:
- Official Subagents documentation: https://code.claude.com/docs/en/sub-agents

## Routing Criteria

**Direct action** when:
- Standard coordination patterns
- Basic context fork decisions
- Simple isolation scenarios

**Route to external docs** when:
- Complex pattern selection
- Advanced coordination implementation
- State management edge cases
