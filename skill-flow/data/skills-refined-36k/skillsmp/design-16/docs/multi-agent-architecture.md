# Multi-Agent Architecture for Design Ops

> Coordinated agent system for comprehensive spec validation and PRP generation.

---

## Overview

The multi-agent system decomposes the Design Ops workflow into specialized agents, each with a focused responsibility. This enables:

1. **Parallel execution** - Independent analyses run simultaneously
2. **Specialized reasoning** - Each agent optimized for its domain
3. **Composable workflows** - Agents can be combined for different scenarios
4. **Clear accountability** - Each agent produces a specific artifact

---

## Agent Roster

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **spec-analyst** | Analyze spec completeness and extract requirements | Spec file | Analysis report + extracted requirements |
| **validator** | Validate spec against invariants | Spec + domain modules | Violation report + confidence score |
| **prp-generator** | Generate PRP from validated spec | Spec + analysis + validation | Draft PRP |
| **reviewer** | Review PRP for completeness and quality | PRP draft | Review feedback + approval status |
| **retrospective** | Extract learnings and system improvements | Completed PRP + outcomes | Retrospective + invariant proposals |

---

## Workflow Phases

### Phase 1: Analysis (Parallel)
```
┌─────────────────┐     ┌─────────────────┐
│  spec-analyst   │     │    validator    │
│                 │     │                 │
│ • Completeness  │     │ • Invariants    │
│ • Requirements  │     │ • CONVENTIONS   │
│ • Complexity    │     │ • Confidence    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
              Combined Analysis
```

### Phase 2: Generation
```
              Combined Analysis
                     │
                     ▼
         ┌─────────────────────┐
         │   prp-generator     │
         │                     │
         │ • Structure PRP     │
         │ • Add validation    │
         │ • Set thinking lvl  │
         └──────────┬──────────┘
                    │
                    ▼
               Draft PRP
```

### Phase 3: Review
```
               Draft PRP
                    │
                    ▼
         ┌─────────────────────┐
         │     reviewer        │
         │                     │
         │ • Check structure   │
         │ • Verify commands   │
         │ • Quality gate      │
         └──────────┬──────────┘
                    │
              ┌─────┴─────┐
              ▼           ▼
          APPROVED    NEEDS WORK
              │           │
              ▼           └──► Back to Phase 2
         Final PRP
```

### Phase 4: Retrospective (Post-Implementation)
```
         Completed PRP + Outcomes
                    │
                    ▼
         ┌─────────────────────┐
         │   retrospective     │
         │                     │
         │ • Extract learnings │
         │ • Propose invariants│
         │ • System improvements│
         └──────────┬──────────┘
                    │
                    ▼
         Retrospective Report
         + Invariant Proposals
```

---

## Agent Specifications

### spec-analyst

**Purpose**: Analyze spec document for completeness, extract structured requirements, and assess complexity.

**Inputs**:
- `SPEC_FILE` - Path to spec document
- `DOMAIN` - Optional domain for context

**Outputs**:
- `analysis.json` containing:
  - `completeness_score` (0-100)
  - `missing_sections` (array)
  - `requirements` (structured list)
  - `complexity_factors` (array)
  - `thinking_level_recommendation`

**Key Checks**:
- Problem statement clarity
- Success criteria presence
- Scope boundaries defined
- Technical constraints listed
- Dependencies identified

---

### validator

**Purpose**: Validate spec against domain invariants and CONVENTIONS.md.

**Inputs**:
- `SPEC_FILE` - Path to spec document
- `DOMAIN` - Target domain (api, database, security, etc.)
- `CONVENTIONS_FILE` - Optional path to conventions

**Outputs**:
- `validation.json` containing:
  - `invariants_checked` (count)
  - `invariants_passed` (count)
  - `violations` (array with severity)
  - `warnings` (array)
  - `confidence_score` (0-100)

**Severity Levels**:
- `critical` - Blocks proceeding
- `major` - Must be addressed
- `minor` - Recommendations
- `info` - Informational

---

### prp-generator

**Purpose**: Generate a complete PRP from analysis and validation results.

**Inputs**:
- `SPEC_FILE` - Original spec
- `ANALYSIS_FILE` - Output from spec-analyst
- `VALIDATION_FILE` - Output from validator
- `TEMPLATE` - PRP template path

**Outputs**:
- `prp-draft.md` - Complete PRP following template
- `generation-log.json` - Decisions made during generation

**Generation Rules**:
1. All template sections must be filled
2. Validation commands must include actual bash
3. Thinking level must match analysis
4. Confidence score carried forward
5. Relevant patterns linked

---

### reviewer

**Purpose**: Quality gate for PRP completeness and correctness.

**Inputs**:
- `PRP_FILE` - Draft PRP to review
- `CHECKLIST` - prp-checker criteria

**Outputs**:
- `review.json` containing:
  - `status` (approved | needs_work | rejected)
  - `score` (0-100)
  - `issues` (array)
  - `suggestions` (array)

**Review Criteria**:
- All required sections present
- No placeholder text remaining
- Validation commands executable
- State transitions logical
- Confidence justification adequate

---

### retrospective

**Purpose**: Extract learnings and propose system improvements after implementation.

**Inputs**:
- `PRP_FILE` - Completed PRP
- `OUTCOME` - Implementation outcome summary
- `DOMAIN` - Target domain for invariant proposals

**Outputs**:
- `retrospective.md` - Completed retrospective template
- `invariant-proposals.json` - Suggested new invariants

**Key Questions**:
1. What process improvements are needed?
2. What invariants were missing?
3. What should update in CONVENTIONS.md?
4. What domain modules need enhancement?
5. What validation commands should be added?

---

## Orchestration

### Full Pipeline
```bash
# Run complete pipeline
./tools/multi-agent-orchestrator.sh \
  --spec path/to/spec.md \
  --domain api \
  --output output/

# Pipeline steps:
# 1. spec-analyst + validator (parallel)
# 2. prp-generator
# 3. reviewer
# 4. Output final PRP or iteration feedback
```

### Partial Runs
```bash
# Analysis only
./tools/multi-agent-orchestrator.sh --spec spec.md --phase analysis

# Generation only (requires prior analysis)
./tools/multi-agent-orchestrator.sh --spec spec.md --phase generate \
  --analysis analysis.json --validation validation.json

# Review only
./tools/multi-agent-orchestrator.sh --prp draft-prp.md --phase review
```

### Watch Mode Integration
```bash
# Continuous validation during development
./tools/watch-mode.sh --spec spec.md --domain api

# Triggers validator on spec changes
# Shows real-time confidence score
```

---

## Error Handling

### Agent Failures
- Each agent has timeout (default 30s)
- Failed agents produce error report
- Orchestrator continues with available results
- Final output notes incomplete analysis

### Validation Failures
- Critical violations block pipeline
- Major violations require confirmation
- Minor violations noted but proceed

### Recovery
```bash
# Resume from checkpoint
./tools/multi-agent-orchestrator.sh --resume checkpoint.json

# Skip failed agent
./tools/multi-agent-orchestrator.sh --skip validator

# Manual override
./tools/multi-agent-orchestrator.sh --force-proceed
```

---

## Configuration

### Agent Timeouts
```yaml
# config/agent-config.yaml
timeouts:
  spec-analyst: 30
  validator: 60
  prp-generator: 120
  reviewer: 30
  retrospective: 60
```

### Thinking Level Thresholds
```yaml
thinking_levels:
  normal:
    max_invariants: 10
    max_complexity: 2
  think:
    max_invariants: 20
    max_complexity: 4
  think_hard:
    max_invariants: 30
    max_complexity: 6
  ultrathink:
    # Above think_hard thresholds
```

---

## Integration Points

### With Claude Code
The multi-agent system is designed to work with Claude Code's Task tool:
- Each agent maps to a specialized subagent
- Orchestrator coordinates via Task invocations
- Results passed through structured JSON

### With Watch Mode
- Validator agent called on file changes
- Dashboard shows real-time status
- Notifications on critical issues

### With Retrospective Flow
- Retrospective agent called post-implementation
- Invariant proposals fed to domain modules
- Learning loop closes

---

## See Also

- [Thinking Levels](thinking-levels.md) - When to escalate thinking
- [Validation Commands Library](../templates/validation-commands-library.md) - Reusable commands
- [PRP Checker](../enforcement/prp-checker.sh) - Review criteria source
