---
name: toolkit-architect
description: "Project scaffolding router for .claude/ configuration and local-first customization. Use when enhancing current project with skills, MCP, hooks, or subagents. Routes to specialized domain architects and toolkit-worker for analysis. Do not use for standalone plugin publishing."
disable-model-invocation: true
---

## 🚨 MANDATORY: Read BEFORE Routing

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Project Customization Guide**: https://code.claude.com/docs/en/skills
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: Project-scoped skills, .claude/ directory structure
  - **Cache**: 15 minutes minimum

- **[MUST READ] Local-First Configuration**: https://code.claude.com/docs/en/plugins
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: .claude/ configuration patterns
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
- **MUST validate** all URLs are accessible before routing
- **REQUIRED** to understand project-scoped configuration before routing

---

# Toolkit Architect

Project scaffolding router for .claude/ configuration using skills-first architecture.

## Actions

### create
**Creates project-scoped components** in .claude/

**Target Directory**: `${CLAUDE_PROJECT_DIR}/.claude/`

**Router Logic**:
1. Validate: User's project has .claude/ directory
2. Determine component type:
   - "I need a skill" → Route to skills-architect
   - "I want web search" → Route to mcp-architect
   - "I need a PR reviewer" → Route to skills-architect or subagents-architect
   - "I want automation" → Route to hooks-architect
3. Load: appropriate knowledge skill
4. Generate in .claude/ (not standalone plugin)
5. Validate: toolkit-quality-validator

**Output Contract**:
```
## Component Created: {component_type}

### Location
- Path: .claude/{component_path}/

### Quality Score: {score}/10
Continue only if score ≥ 8/10
```

### audit
**Audits .claude/ configuration** for quality and compliance

**Target**: `${CLAUDE_PROJECT_DIR}/.claude/`

**Router Logic**:
1. Load: toolkit-quality-validator
2. **Assess output volume**:
   - Large .claude/ or full audit? → Delegate to toolkit-worker (context: fork)
   - Simple validation? → Load directly
3. **Parse explicit output**:
   - Look for "## Audit Results:"
   - Check "Quality Score: {score}/10"
4. **Handle failures explicitly**:
   - On ERROR: Log issue and report to user
   - On FAIL (< 8/10): Continue with recommendations
   - On PASS (≥ 8/10): Report compliance status
5. Generate recommendations

**Fork Decision Matrix**:
| .claude/ Size | Component Count | Use Fork? | Worker |
|---------------|-----------------|-----------|--------|
| Small (<5 skills) | <10 components | No | Direct load |
| Medium (5-20 skills) | 10-50 components | Yes | toolkit-worker |
| Large (>20 skills) | >50 components | Yes | toolkit-worker |

**Worker Output Parsing**:
```markdown
# Parse toolkit-worker output for:
Completion marker: "## .claude/ Analysis Report"
Quality score: Extract from "Quality Score: {score}/10"
Status classification:
  - score ≥ 8 → Continue with recommendations
  - score 5-7 → Report issues, suggest refinement
  - score < 5 → Major rework required

# If worker returns ERROR:
1. Parse error context
2. Log and report error to user with recovery options
3. Do NOT continue or retry without explicit direction
```

**Output Contract**:
```
## .claude/ Audit Results

### Quality Score: {score}/10

### Structural Compliance
- ✅/❌ Skills-first architecture
- ✅/❌ .claude/ directory structure
- ✅/❌ Progressive disclosure

### Component Quality
- Skills: {score}/15
- Subagents: {score}/10
- Hooks: {score}/10
- MCP: {score}/5

### Standards Adherence
- URL currency: {score}/10
- Best practices: {score}/10

### Priority Actions
- High: {high_priority}
- Medium: {medium_priority}
- Low: {low_priority}
```

### refine
**Improves .claude/ configuration** based on audit findings

**Target**: `${CLAUDE_PROJECT_DIR}/.claude/`

**Router Logic**:
1. Load: toolkit-quality-validator, relevant knowledge skills
2. Review current .claude/ structure
3. Identify improvements by domain:
   - Skills issues → Route to skills-architect
   - Hook issues → Route to hooks-architect
   - MCP issues → Route to mcp-architect
   - Subagent issues → Route to subagents-architect
4. Apply improvements to .claude/
5. Validate: toolkit-quality-validator

**Output Contract**:
```
## .claude/ Refinement Complete

### Changes Applied
- {change_1}
- {change_2}
- {change_3}

### Quality Improvement: {old_score} → {new_score}/10

### Next Steps
- {recommendation_1}
- {recommendation_2}
```

## When to Use Context: Fork

**Use toolkit-worker (context: fork)** when:
- High-volume output (extensive grep, repo traversal)
- Noisy exploration that clutters conversation
- Full .claude/ directory audits
- Pattern discovery across multiple files

**Don't use context: fork** when:
- Simple task creation
- Direct skill instantiation
- Straightforward routing decisions

## Knowledge Skills

Delegates to:
- **toolkit-architect** - Project scaffolding guidance
- **skills-knowledge** - Skill development best practices
- **meta-architect-claudecode** - Layer selection decisions
- **toolkit-quality-validator** - Standards enforcement
- **toolkit-worker** - Noisy/high-volume analysis

## Integration Points

- **skills-architect** - Skills domain expertise
- **hooks-architect** - Hooks domain expertise
- **mcp-architect** - MCP domain expertise
- **subagents-architect** - Subagents domain expertise
- **toolkit-worker** - Isolated analysis worker
