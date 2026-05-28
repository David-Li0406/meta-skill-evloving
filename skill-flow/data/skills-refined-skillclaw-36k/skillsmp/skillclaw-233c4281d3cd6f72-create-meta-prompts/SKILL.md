---
name: create-meta-prompts
description: Use this skill when building optimized prompts for Claude-to-Claude communication in multi-stage workflows, such as research, planning, and execution.
---

# Skill body

## Objective
Create prompts optimized for Claude-to-Claude communication in multi-stage workflows. Outputs are structured with XML and metadata for efficient parsing by subsequent prompts. Every execution produces a `SUMMARY.md` for quick human scanning without reading full outputs. Each prompt gets its own folder in `.prompts/` with its output artifacts, enabling clear provenance and chain detection.

## Quick Start

### Workflow
1. **Intake**: Determine purpose (Do/Plan/Research/Refine) and gather requirements.
2. **Chain Detection**: Check for existing research/plan files to reference.
3. **Generate**: Create prompt using purpose-specific patterns.
4. **Save**: Create folder in `.prompts/{number}-{topic}-{purpose}/`.
5. **Present**: Show decision tree for running.
6. **Execute**: Run prompt(s) with a dependency-aware execution engine.
7. **Summarize**: Create `SUMMARY.md` for human scanning.

### Folder Structure
```
.prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md    # Prompt (archived after run)
│   ├── auth-research.md            # Full output (XML for Claude)
│   └── SUMMARY.md                  # Executive summary (markdown for human)
├── 002-auth-plan/
│   ├── completed/
│   │   └── 002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
├── 003-auth-implement/
│   ├── completed/
│   │   └── 003-auth-implement.md
│   └── SUMMARY.md                  # Do prompts create code elsewhere
├── 004-auth-research-refine/
│   ├── completed/
│   │   └── 004-auth-research-refine.md
│   ├── archive/
│   │   └── auth-research-v1.md     # Previous version
│   └── SUMMARY.md
```

### Context
- Prompts directory: !`[ -d ./.prompts ] && echo "exists" || echo "missing"`
- Existing research/plans: !`find ./.prompts -name "*-research.md" -o -name "*-plan.md" 2>/dev/null | head -10`
- Next prompt number: !`ls -d ./.prompts/*/ 2>/dev/null | wc -l | xargs -I {} expr {} + 1`

### Automated Workflow
#### Step 0: Intake Gate
**Title**: Adaptive Requirements Gathering

**Critical First Action**: 
- **BEFORE analyzing anything**, check if context was provided.
- IF no context provided (skill invoked without description):
  - **IMMEDIATELY use AskUserQuestion** with:
    - header: "Purpose"
    - question: "What is the purpose of this prompt?"
    - options:
      - "Do" - Execute a task, produce an artifact.
      - "Plan" - Outline steps for a task.
      - "Research" - Gather information.
      - "Refine" - Improve existing outputs.