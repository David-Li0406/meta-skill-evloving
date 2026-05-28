---
name: create-meta-prompts
description: Create optimized prompts for Claude-to-Claude pipelines with research, planning, and execution stages. Use when building prompts that produce outputs for other prompts to consume, or when running multi-stage workflows (research -> plan -> implement).
---

# Objective
Create prompts optimized for Claude-to-Claude communication in multi-stage workflows. Outputs are structured with XML and metadata for efficient parsing by subsequent prompts. Every execution produces a `SUMMARY.md` for quick human scanning without reading full outputs. Each prompt gets its own folder in `.prompts/` with its output artifacts, enabling clear provenance and chain detection.

# Quick Start
## Workflow
1. **Intake**: Determine purpose (Do/Plan/Research/Refine), gather requirements.
2. **Chain detection**: Check for existing research/plan files to reference.
3. **Generate**: Create prompt using purpose-specific patterns.
4. **Save**: Create folder in `.prompts/{number}-{topic}-{purpose}/`.
5. **Present**: Show decision tree for running.
6. **Execute**: Run prompt(s) with dependency-aware execution engine.
7. **Summarize**: Create SUMMARY.md for human scanning.

## Folder Structure
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

# Context
Prompts directory: !`[ -d ./.prompts ] && echo "exists" || echo "missing"`
Existing research/plans: !`find ./.prompts -name "*-research.md" -o -name "*-plan.md" 2>/dev/null | head -10`
Next prompt number: !`ls -d ./.prompts/*/ 2>/dev/null | wc -l | xargs -I {} expr {} + 1`

# Automated Workflow
## Step 0: Intake Gate
### Adaptive Requirements Gathering
**BEFORE analyzing anything**, check if context was provided.

IF no context provided (skill invoked without description):
→ **IMMEDIATELY use AskUserQuestion** with:
- header: "Purpose"
- question: "What is the purpose of this prompt?"
- options:
  - "Do" - Execute a task, produce an artifact
  - "Plan" - Create an approach, roadmap, or strategy
  - "Research" - Gather information or understand something
  - "Refine" - Improve an existing research or plan output

After selection, ask: "Describe what you want to accomplish" (they select "Other" to provide free text).

IF context was provided:
→ Check if purpose is inferable from keywords:
- `implement`, `build`, `create`, `fix`, `add`, `refactor` → Do
- `plan`, `roadmap`, `approach`, `strategy`, `decide`, `phases` → Plan
- `research`, `understand`, `learn`, `gather`, `analyze`, `explore` → Research
- `refine`, `improve`, `deepen`, `expand`, `iterate`, `update` → Refine

→ If unclear, ask the Purpose question above as first contextual question.
→ If clear, proceed to adaptive_analysis with inferred purpose.

## Step 1: Generate Prompt
### Generate Prompt
Load purpose-specific patterns:
- Do: [references/do-patterns.md](references/do-patterns.md)
- Plan: [references/plan-patterns.md](references/plan-patterns.md)
- Research: [references/research-patterns.md](references/research-patterns.md)
- Refine: [references/refine-patterns.md](references/refine-patterns.md)

Load intelligence rules: [references/intelligence-rules.md](references/intelligence-rules.md).

### Prompt Structure
All generated prompts include:
1. **Objective**: What to accomplish, why it matters.
2. **Context**: Referenced files (@), dynamic context (!).
3. **Requirements**: Specific instructions for the task.
4. **Output specification**: Where to save, what structure.
5. **Metadata requirements**: For research/plan outputs, specify XML metadata structure.
6. **SUMMARY.md requirement**: All prompts must create a SUMMARY.md file.
7. **Success criteria**: How to know it worked.

For Research and Plan prompts, output must include:
- `<confidence>` - How confident in findings.
- `<dependencies>` - What's needed to proceed.
- `<open_questions>` - What remains uncertain.
- `<assumptions>` - What was assumed.

All prompts must create `SUMMARY.md` with:
- **One-liner** - Substantive description of outcome.
- **Version** - v1 or iteration info.
- **Key Findings** - Actionable takeaways.
- **Files Created** - (Do prompts only).
- **Decisions Needed** - What requires user input.
- **Blockers** - External impediments.
- **Next Step** - Concrete forward action.

## Step 2: Present Decision Tree
After saving prompt(s), present inline (not AskUserQuestion):
### Single Prompt Presentation
```
Prompt created: .prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md

What's next?
1. Run prompt now
2. Review/edit prompt first
3. Save for later
4. Other

Choose (1-4): _
```

### Multi Prompt Presentation
```
Prompts created:
- .prompts/001-auth-research/001-auth-research.md
- .prompts/002-auth-plan/002-auth-plan.md
- .prompts/003-auth-implement/003-auth-implement.md

Detected execution order: Sequential (002 references 001 output, 003 references 002 output)

What's next?
1. Run all prompts (sequential)
2. Review/edit prompts first
3. Save for later
4. Other

Choose (1-4): _
```

## Step 3: Execution Engine
### Execution Modes
#### Single Prompt
Straightforward execution of one prompt.
1. Read prompt file contents.
2. Spawn Task agent with subagent_type="general-purpose".
3. Include in task prompt:
   - The complete prompt contents.
   - Output location: `.prompts/{number}-{topic}-{purpose}/{topic}-{purpose}.md`.
4. Wait for completion.
5. Validate output (see validation section).
6. Archive prompt to `completed/` subfolder.
7. Report results with next-step options.

#### Sequential Execution
For chained prompts where each depends on previous output.
1. Build execution queue from dependency order.
2. For each prompt in queue:
   a. Read prompt file.
   b. Spawn Task agent.
   c. Wait for completion.
   d. Validate output.
   e. If validation fails → stop, report failure, offer recovery options.
   f. If success → archive prompt, continue to next.
3. Report consolidated results.

#### Parallel Execution
For independent prompts with no dependencies.
1. Read all prompt files.
2. **CRITICAL**: Spawn ALL Task agents in a SINGLE message.
   - This is required for true parallel execution.
   - Each task includes its output location.
3. Wait for all to complete.
4. Validate all outputs.
5. Archive all prompts.
6. Report consolidated results (successes and failures).

### Validation
After each prompt completes, verify success:
1. **File exists**: Check output file was created.
2. **Not empty**: File has content (> 100 chars).
3. **Metadata present** (for research/plan): Check for required XML tags.
4. **SUMMARY.md exists**: Check SUMMARY.md was created.
5. **SUMMARY.md complete**: Has required sections (Key Findings, Decisions Needed, Blockers, Next Step).
6. **One-liner is substantive**: Not generic like "Research completed".

### Failure Handling
If validation fails:
- Report what's missing.
- Offer options:
  - Retry the prompt.
  - Continue anyway (for non-critical issues).
  - Stop and investigate.

### Archiving
- **Sequential**: Archive each prompt immediately after successful completion.
- **Parallel**: Archive all at end after collecting results.

## Reference Guides
**Prompt patterns by purpose:**
- [references/do-patterns.md](references/do-patterns.md) - Execution prompts + output structure.
- [references/plan-patterns.md](references/plan-patterns.md) - Planning prompts + plan.md structure.
- [references/research-patterns.md](references/research-patterns.md) - Research prompts + research.md structure.
- [references/refine-patterns.md](references/refine-patterns.md) - Iteration prompts + versioning.

**Shared templates:**
- [references/summary-template.md](references/summary-template.md) - SUMMARY.md structure and field requirements.
- [references/metadata-guidelines.md](references/metadata-guidelines.md) - Confidence, dependencies, open questions, assumptions.

**Supporting references:**
- [references/question-bank.md](references/question-bank.md) - Intake questions by purpose.
- [references/intelligence-rules.md](references/intelligence-rules.md) - Extended thinking, parallel tools, depth decisions.

## Success Criteria
**Prompt Creation:**
- Intake gate completed with purpose and topic identified.
- Chain detection performed, relevant files referenced.
- Prompt generated with correct structure for purpose.
- Folder created in `.prompts/` with correct naming.
- Output file location specified in prompt.
- SUMMARY.md requirement included in prompt.
- Metadata requirements included for Research/Plan outputs.
- Quality controls included for Research outputs (verification checklist, QA, pre-submission).
- Streaming write instructions included for Research outputs.
- Decision tree presented.

**Execution (if user chooses to run):**
- Dependencies correctly detected and ordered.
- Prompts executed in correct order (sequential/parallel/mixed).
- Output validated after each completion.
- SUMMARY.md created with all required sections.
- One-liner is substantive (not generic).
- Failed prompts handled gracefully with recovery options.
- Successful prompts archived to `completed/` subfolder.
- SUMMARY.md displayed inline in results.
- Results presented with decisions/blockers flagged.

**Research Quality (for Research prompts):**
- Verification checklist completed.
- Quality report distinguishes verified from assumed claims.
- Sources consulted listed with URLs.
- Confidence levels assigned to findings.
- Critical claims verified with official documentation.