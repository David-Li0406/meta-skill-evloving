---
name: analyze-ticket
description: Skill for analyzing ticket complexity and determining required workflow phases. Uses scoring system to classify tickets as SIMPLE, MEDIUM, or COMPLEX, which determines exploration depth and planning approach.
---

# Analyze Ticket Skill

This skill analyzes a ticket's content to determine its complexity and decide which workflow phases are required.

## Complexity Levels

| Level | Score | Exploration | Planning | AEP | Architect |
|-------|-------|-------------|----------|-----|-----------|
| SIMPLE | 0-2 | Skip | Basic | No | No |
| MEDIUM | 3-5 | Light | Standard | Partial | Optional |
| COMPLEX | 6+ | Full AEP | Detailed | Full | Yes |

## Scoring Factors

Analyze the ticket content and assign points for each applicable factor:

### Technical Complexity

| Factor | Points | Detection Signals |
|--------|--------|-------------------|
| Multi-component changes | +2 | Mentions multiple services, modules, or layers |
| Database schema changes | +2 | Keywords: migration, schema, table, column, index |
| API breaking changes | +3 | Keywords: breaking, deprecate, remove endpoint, change contract |
| New external dependency | +2 | Keywords: integrate, new library, third-party, SDK |
| Performance requirements | +2 | Keywords: optimize, performance, latency, throughput |
| Security implications | +2 | Keywords: auth, permission, encryption, sensitive data |

### Scope Indicators

| Factor | Points | Detection Signals |
|--------|--------|-------------------|
| Cross-team coordination | +2 | Mentions other teams, external dependencies |
| Multiple file types | +1 | Backend + frontend, or multiple languages |
| Test infrastructure changes | +1 | Keywords: test framework, CI/CD, pipeline |
| Documentation required | +1 | Explicit doc requirements or public API changes |

### Uncertainty Factors

| Factor | Points | Detection Signals |
|--------|--------|-------------------|
| Vague requirements | +2 | Ambiguous language, missing acceptance criteria |
| Research needed | +2 | Keywords: investigate, explore, POC, spike |
| Unknown impact | +2 | Cannot determine affected components |
| No clear success criteria | +1 | Missing "done when" or validation steps |

### Negative Factors (Reduce Complexity)

| Factor | Points | Detection Signals |
|--------|--------|-------------------|
| Well-defined scope | -1 | Clear, specific requirements |
| Single file change | -1 | Obvious single-file fix |
| Existing pattern | -1 | Similar to existing code/feature |
| Has acceptance criteria | -1 | Clear validation steps provided |

## Label-Based Override

Certain labels can force complexity level:

### Simple Labels (force SIMPLE)
- `quick-fix`, `typo`, `documentation`, `trivial`, `minor`
- Config: `complexity.simple_labels`

### Complex Labels (force COMPLEX)
- `needs-analysis`, `architecture`, `breaking-change`, `migration`, `epic`
- Config: `complexity.complex_labels`

## Analysis Process

### Step 1: Extract Keywords
Parse ticket content for complexity signals:
- Title
- Description
- Labels/Tags
- Comments (if available)

### Step 2: Calculate Base Score
Sum points from all applicable factors.

### Step 3: Apply Label Override
Check for forcing labels that override calculated score.

### Step 4: Determine Level
```
if has_simple_label:
    level = SIMPLE
elif has_complex_label:
    level = COMPLEX
elif score <= simple_threshold (default: 2):
    level = SIMPLE
elif score >= complex_threshold (default: 6):
    level = COMPLEX
else:
    level = MEDIUM
```

### Step 5: Recommend Actions

Based on complexity level, recommend workflow phases:

#### SIMPLE
- Skip exploration phase
- Create direct implementation plan
- No AEP methodology
- Basic validation only

#### MEDIUM
- Light exploration (1 agent, focused search)
- Standard implementation plan
- Partial AEP (Analyse + Plan, skip deep Explore)
- Standard validation

#### COMPLEX
- Full AEP workflow (3 parallel explore agents)
- Invoke Architect skill for planning
- Detailed implementation plan with phases
- Comprehensive validation strategy

## Output Format

```markdown
## Complexity Analysis

### Score Breakdown

| Factor | Points | Reason |
|--------|--------|--------|
| Multi-component changes | +2 | Affects API and frontend |
| Database changes | +2 | Requires migration |
| Well-defined scope | -1 | Clear acceptance criteria |
| **Total** | **3** | |

### Classification

**Complexity Level**: MEDIUM (score: 3)

### Label Analysis
- Labels found: `feature`, `backend`
- No complexity-forcing labels detected

### Recommended Workflow

1. **Exploration**: Light (1 focused agent)
2. **Planning**: Standard approach
3. **AEP**: Partial (Analyse + Plan)
4. **Architect Skill**: Optional

### Key Concerns

- Database migration requires careful ordering
- Consider rollback strategy for schema changes

### Suggested Focus Areas

1. Existing migration patterns in codebase
2. Related API endpoints
3. Test coverage for affected components
```

## Integration with Workflow

This skill is invoked by:
1. `/resolve` command - after fetch, before workspace setup
2. `/analyze-ticket` standalone command
3. Planning phase to determine approach

## Configuration

Reads from `.claude/ticket-config.json`:
```json
{
  "complexity": {
    "auto_detect": true,
    "simple_labels": ["quick-fix", "typo"],
    "complex_labels": ["architecture", "migration"],
    "simple_threshold": 2,
    "complex_threshold": 6
  }
}
```

## Exploration Guidelines by Level

### SIMPLE - No Exploration
Proceed directly to implementation planning.

### MEDIUM - Light Exploration
Launch 1 explore agent to:
- Find similar existing code
- Identify files to modify
- Check test patterns

### COMPLEX - Full AEP Exploration
Launch up to 3 parallel explore agents:

**Agent 1: Implementation Patterns**
- Search for similar features
- Find reusable code patterns
- Identify coding conventions

**Agent 2: Impact Analysis**
- Trace dependencies
- Find all affected components
- Check for breaking changes

**Agent 3: Test Coverage**
- Find related tests
- Check testing patterns
- Identify test utilities

## Language

Analysis output in French for user communication.
Technical terms and factor names in English.
