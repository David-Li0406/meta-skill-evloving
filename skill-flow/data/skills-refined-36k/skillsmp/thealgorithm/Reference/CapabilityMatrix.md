# Capability Matrix

**Source of Truth:** `Data/Capabilities.yaml`

This document describes what capabilities are unlocked at each effort level. Effort classification happens FIRST and determines which tools are available.

## The Matrix

| Effort Level | Models | Thinking | Analysis | Research | Execution | Verification | Parallel |
|--------------|--------|----------|----------|----------|-----------|--------------|----------|
| **TRIVIAL** | — | — | — | — | — | — | 0 |
| **QUICK** | haiku | — | — | — | general-purpose | — | 1 |
| **STANDARD** | haiku, sonnet | deep thinking | Science | WebSearch | general-purpose, Explore | Browser | 1-3 |
| **THOROUGH** | haiku, sonnet | All + Plan Mode | All | WebSearch | All + Plan | All | 3-5 |
| **DETERMINED** | all + opus | All | All | All | unlimited | All | 10 |

## Detailed Breakdown

### TRIVIAL (Skip Algorithm)
- **When:** Greetings, simple Q&A, acknowledgments
- **Capabilities:** None - direct response, no ISC
- **ISC Rows:** 0
- **Example:** "Hello", "Thanks", "What's 2+2?"

### QUICK
- **When:** Single-step tasks, simple lookups, quick fixes
- **Capabilities:**
  - `models.haiku` - Fast, cheap execution
  - `execution.general` - Parallel grunt work, simple tasks
- **ISC Rows:** Typically 1-3, but can be more if needed
- **Traits Added:** rapid, pragmatic
- **Max Parallel:** 1
- **Example:** "Fix the typo in README", "What does this function do?"

### STANDARD
- **When:** Multi-step tasks, bounded scope, most development work
- **Capabilities:**
  - `models.haiku` - For spotchecks, parallel work
  - `models.sonnet` - Main reasoning model
  - `thinking.deep thinking` - BeCreative for creative solutions
  - `analysis.science` - Hypothesis-driven exploration
  - `research.web_search` - WebSearch tool for research
  - `execution.general` - general-purpose agents
  - `execution.explore` - Explore agents for codebase
  - `verification.browser` - Web validation
  - `verification.skeptical_verifier` - Independent verification
- **ISC Rows:** As many as needed to capture ideal state
- **Traits Added:** analytical, systematic
- **Max Parallel:** 3
- **Example:** "Add dark mode to settings", "Create a new API endpoint"

### THOROUGH
- **When:** Complex work, multi-file changes, architectural decisions
- **Capabilities:**
  - All STANDARD capabilities
  - `thinking.tree_of_thought` - Branching exploration
  - `thinking.plan_mode` - EnterPlanMode for approval
  - `execution.plan` - Plan agents for architecture
- **ISC Rows:** Dozens typically, can be hundreds for complex projects
- **Traits Added:** thorough, meticulous
- **Max Parallel:** 5
- **Example:** "Refactor the authentication system", "Design a new microservice"

### DETERMINED
- **When:** Mission-critical, "until done", overnight tasks, unlimited iteration
- **Capabilities:**
  - All capabilities unlocked
  - `models.opus` - Maximum intelligence model
  - Unlimited agents
  - Unlimited iterations
- **ISC Rows:** Can be hundreds or thousands for major projects
- **Traits Added:** thorough, meticulous, adversarial
- **Max Parallel:** 10
- **Example:** "Build the entire feature from scratch", "Security audit everything"

## ISC Scale by Effort

**ISC size is NOT strictly bounded by effort level.** The effort level determines QUALITY expectations and available capabilities, not a hard limit on rows.

| Effort | Typical ISC Size | Quality Standard | Notes |
|--------|------------------|------------------|-------|
| QUICK | 1-5 rows | Good enough | Fast execution, minimal verification |
| STANDARD | 5-20 rows | High | Thorough verification, research via WebSearch |
| THOROUGH | 20-100 rows | Very high | Plan mode, multiple exploration passes |
| DETERMINED | 50-1000+ rows | Exceptional | Unlimited iteration until perfect |

**Key insight:** A complex problem at DETERMINED effort might have hundreds of ISC rows covering:
- Research findings (what to do)
- Anti-patterns (what to avoid)
- Best practices (how to do it well)
- Edge cases (what to handle)
- Verification criteria (how to confirm)
- Security considerations (what to protect)

## Capability Categories Explained

### Models
Compute resources for reasoning. Higher effort unlocks more powerful models.

| Model | Cost | Speed | Use For |
|-------|------|-------|---------|
| haiku | Low | Fast | Parallel grunt work, spotchecks, simple execution |
| sonnet | Medium | Medium | Analysis, planning, research, standard work |
| opus | High | Slower | Architecture, critical decisions, complex reasoning |

### Thinking Modes
Enhanced reasoning approaches.

| Mode | Skill | When |
|------|-------|------|
| deep thinking | BeCreative | Creative solutions, novel approaches |
| tree_of_thought | BeCreative (workflow) | Complex multi-factor decisions |
| plan_mode | EnterPlanMode tool | Multi-step implementations needing approval |

### Analysis Modes
Structured analytical approaches.

| Mode | Skill | When |
|------|-------|------|
| science | Science | Hypothesis-driven exploration, experiments |

### Research
Information gathering approaches.

| Method | Tool | When |
|--------|------|------|
| web_search | WebSearch | Web research, current events, citations |
| explore | Explore subagent | Codebase exploration, finding patterns |

### Execution Agents
Work performers using vanilla Claude Code subagent_types.

| Agent | Type | When |
|-------|------|------|
| general-purpose | general-purpose | Multi-step tasks, research, analysis |
| Explore | Explore | Codebase exploration |
| Plan | Plan | Architecture design, implementation planning |


### Verification
Validation approaches.

| Method | How | When |
|--------|-----|------|
| browser | Browser skill | Web application validation |
| skeptical_verifier | Independent agent | Independent verification, different from executor |

## Override Methods

### CLI Override
```bash
bun run EffortClassifier.ts --request "any request" --override DETERMINED
```

### Inline Override
```
algorithm effort THOROUGH: build this complex feature
```

The inline pattern is stripped from the request and effort is forced to the specified level.

## Commands

```bash
# Classify effort for a request
bun run ~/.claude/skills/THEALGORITHM/Tools/EffortClassifier.ts --request "your request"

# Load capabilities for an effort level
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilityLoader.ts --effort STANDARD

# List all capabilities
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilityLoader.ts --list-all

# Select capabilities for an ISC row
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilitySelector.ts --row "Research best practices" --effort STANDARD
```
