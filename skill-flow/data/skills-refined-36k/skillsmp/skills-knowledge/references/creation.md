# Build Workflow: Creating and Refining Customizations

## Table of Contents

- [Step 0: Choose Your Layer](#step-0-choose-your-layer)
- [Creating Skills Workflow](#creating-skills-workflow)
- [Refining Skills Workflow](#refining-skills-workflow)
- [Advanced Patterns](#advanced-patterns)
- [File References](#file-references)
- [Trust the Agent's Native Capacities](#trust-the-agents-native-capacities)
- [What Gets Ingested](#what-gets-ingested)
- [Core Workflow: The Golden Path Method](#core-workflow-the-golden-path-method)
- [Example](#example)
- [Ingesting Other Skills](#ingesting-other-skills)
- [Ingesting External References](#ingesting-external-references)
- [[Reference Name]](#reference-name)
- [Common Patterns](#common-patterns)
- [Modularization Strategy](#modularization-strategy)
- [Red Flags](#red-flags)
- [The Spirit of Ingestion](#the-spirit-of-ingestion)
- [Validation Checklist](#validation-checklist)
- [Tool vs Skill](#tool-vs-skill)
- [Three Types of Knowledge in Skills](#three-types-of-knowledge-in-skills)
- [Evaluation Framework (160 points total)](#evaluation-framework-160-points-total)
- [NEVER Do When Evaluating](#never-do-when-evaluating)
- [Evaluation Protocol](#evaluation-protocol)
- [Summary](#summary)
- [Dimension Scores](#dimension-scores)
- [Critical Issues](#critical-issues)
- [Top 5 Improvements](#top-5-improvements)
- [Detailed Analysis](#detailed-analysis)
- [Common Failure Patterns](#common-failure-patterns)
- [The Meta-Question](#the-meta-question)
- [Quick Reference Checklist](#quick-reference-checklist)
- [Writing Style Requirements](#writing-style-requirements)
- [Anti-Patterns to Avoid (Building-Specific)](#anti-patterns-to-avoid-building-specific)
- [Security Considerations](#security-considerations)
- [Validation Checklist](#validation-checklist)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Quality Validation](#quality-validation)

> This workflow guides you through building customizations from scratch and refining existing ones. For core principles and archetypes, see **Load: meta-architect-claudecode**.

---

## Step 0: Choose Your Layer

> **Before building any customization**, ensure you've chosen the appropriate layer.

**Quick Decision Tree**:
```
START: What do you need?
│
├─ "Persistent project norms" → CLAUDE.md rules
├─ "Domain expertise to discover" → Skill
├─ "Explicit workflow I trigger" → Slash Command
└─ "Isolation/parallelism" → Subagent
```

**Key Principle**: A complete customization pack can be just **CLAUDE.md + one Skill**. Commands and subagents are optional enhancements.

**For detailed layer selection**: See **Load: meta-architect-claudecode**

---

## Creating Skills Workflow

### Step 1: Feel the Purpose

**What problem are you solving?** Not the mechanism - the problem.

- Who benefits from this skill?
- What makes this unique?
- What would success look like?

**Define the Work Unit (Mandatory for Prompt Budget):**
- What is the explicit completion criteria?
- What does "done" look like in measurable terms?
- Can this be verified with binary pass/fail?

**Identify iteration patterns:**
- What corrections loops are common?
- What clarifications does Claude typically request?
- What decisions get re-worked multiple times?

> **Encode the answers**: Each identified pattern is a candidate for encoding in the Skill/Command to prevent future iteration cycles.

**Anti-2nd-Turn Checklist (complete before proceeding):**
- [ ] All required inputs identified or available
- [ ] Success criteria are measurable, not subjective
- [ ] Expected output format is specified
- [ ] Rollback strategy exists for destructive operations

> **If any checkbox is empty**: Gather information first. Do not proceed until all items are confirmed.

### Step 1.5: Design for Autonomy

> **Critical**: Skills should be self-sufficient by default.

**Autonomy Design Checklist**:
- [ ] What ambiguity can be resolved through exploration (read/grep)?
- [ ] What truly requires user input (cannot be inferred)?
- [ ] What are the explicit success/stop criteria?
- [ ] Which fork pattern matches the use case?
  - Router + Worker (flexible, auto-discovery + isolated noisy work)
  - Single Forked (simpler, all work is noisy)
  - Skill + Command (user controls noisy phase)

**Question Burst Test**: If questions are needed, verify ALL 3 conditions:
1. Information NOT inferrable from repo/tools
2. High impact if wrong choice
3. Small set (3-7 max) unlocks everything

If any condition fails → encode decision tree instead of asking.

**For detailed autonomy design**: See **Load: meta-architect-claudecode**

### Step 2: Name from Essence

The name should capture the **core value**, not the technical mechanism.

**Good names:**
- `document-whisperer` (not `pdf-extractor`)
- `architecture-navigator` (not `code-review-assistant`)
- `deployment-guardian` (not `kubectl-deploy`)

### Step 3: Identify Core Value

Review the Core Values Framework in **Load: meta-architect-claudecode** and identify which value your skill provides: reliability, wisdom, consistency, coordination, or simplicity.

Use the decision tree to determine the design approach that best fits your task.

### Step 4: Describe the Magic

Write in plain language: **"What this does + when to use it + when not to use it"**

Example:
> "Helps agents extract insights from conversations. Use when analyzing customer feedback, user interviews, or chat logs. Do not use for transcribing audio or real-time processing."

### Step 5: Show, Don't Tell

Give **one concrete example** of it in action. That's worth 100 explanations.

### Step 6: Organize the Content

**The "Rule of Three":**
- Mentioned once → Keep in SKILL.md
- Mentioned twice → Reference it
- Mentioned three times → Extract to dedicated file

**Content placement:**
- Core workflow → SKILL.md
- Deep domain knowledge → references/
- Reusable patterns → examples/
- Complex operations → scripts/

### Step 7: Apply the Delta Standard

Document secrets, not basics.

If any agent would know this → Don't write it

### Step 8: Test It

**Fresh Eyes Test:**
1. Start a new conversation
2. Describe the problem your skill solves
3. Does the skill activate and deliver?

### Step 9: Iteration Audit (Optional)

**After testing, track your prompt budget:**

**Prompt Efficiency Scorecard:**
- Number of top-level prompts used: ___
- Number of subagent runs: ___
- Number of correction cycles: ___
- Total budget: ___ (Target: ≤2, Max: ≤3)

**Audit questions:**
- Did Claude ask for clarifications that could have been encoded?
- Were there correction cycles that could have been prevented?
- Did the workflow require multiple prompts to complete?
- Did you hit any hard stop limits (3+ subagents, 2+ corrections)?

**For each "yes":**
1. Identify what was missing from the Skill/Command
2. Encode the missing constraint/decision tree
3. Re-test until the workflow completes deterministically

**Success metrics:**
- **Prompt Budget**: ≤2 top-level prompts per work unit
- **Subagent Fan-out**: ≤3 subagents per work unit
- **Correction Cycles**: ≤1 correction per file
- **Completion**: Work unit defined and achieved in single session

> **Redesign Trigger**: If consistently >3 prompts, the Skill/Command architecture needs fundamental redesign.

---

## Refining Skills Workflow

### When to Refine (Trust the Signs)

**Content Signals:**
- Readers get confused about what to do
- Examples don't match real use cases
- Content feels scattered
- It's trying to be everything for everyone

**Structural Signals:**
- Reading takes more than 2 minutes
- Users ask "when would I use this?"
- Activation feels random or inconsistent

### How to Refine

**Teaching basics?** → Remove (violates Delta Standard)

**Code that looks copy-pasteable?** → Move to examples/

**Complex setup instructions?** → Move to scripts/

**Deep domain knowledge?** → Extract to references/

**Simple, direct steps?** → Keep in SKILL.md

### Keyword Optimization

Match the user's language, not technical terms:

**Before:**
```yaml
description: "Processes files"
```

**After:**
```yaml
description: "Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF documents."
```

### Skill Evolution

Skills evolve as they mature based on usage patterns:
- **Simple workflows** → **Coordination** (adding orchestration)
- **Coordination** → **Wisdom** (knowledge accumulates)
- **Wisdom** → **Reliability** (processes become standardized)
- **Reliability** → **Consistency** (complex scaffolds emerge)

Don't force evolution. Let usage patterns guide the skill's natural development.

---

## Advanced Patterns

### State Anchoring Strategy

Context windows are temporary. Skills must anchor state for long-running workflows:

```markdown
# State
- [x] Step 1: Backup
- [ ] Step 2: Transform
**Last Checkpoint:** SUCCESS
```

**Requirements:**
- Atomic checkpoints
- Idempotent operations
- Progress visibility
- Failure isolation

### Pipeline Sequencing

Use dependency graphs to coordinate multi-step workflows:

**Design Rules:**
- Unidirectional dependencies
- Parallel execution for independent steps
- Define data contracts
- Stop on errors

```markdown
# Sequence
1. **Analyze**: Run xlsx tool, verify file exists
2. **Present**: Run pptx tool, charts MUST match Step 1 data
```

### Validation-First Architecture

Use three-phase validation for complex workflows:

1. **Plan**: Verify plan is well-formed
2. **Pre-execution**: Check prerequisites
3. **Post-execution**: Verify outputs

**Use for:** Batch operations, destructive operations, high-stakes tasks

---

## File References

When referencing files in your skill:

- Use relative paths from the skill root
- Keep file references one level deep from `SKILL.md`
- Avoid deeply nested chains (>1 level)

**Correct:**
```markdown
See [the guide](references/deployment.md)
Run `scripts/deploy.sh`
```

**Incorrect:**
```markdown
See [the guide](references/deployment.md)  # leading slash
See [guide](references/subdir/deployment.md)  # nested
```

---

## Trust the Agent's Native Capacities

The agent already knows how to read/write files, run bash commands, parse data structures, format output, organize directories.

**Question to ask:** "Can the agent do this with existing tools?"

If yes → Let the agent write it directly
If no → Provide a script (rare)

---

# Extracting Knowledge from Documentation

> This workflow guides you through distilling knowledge from documentation, references, other customizations, and external sources into actionable customization content. This applies to **any layer** — rules, skills, commands, or subagents. For core principles and archetypes, see **Load: meta-architect-claudecode**.

> **Before starting**: Ensure you've chosen the correct layer for your needs. See **Load: meta-architect-claudecode** for guidance.

## What Gets Ingested

| Source Type | Golden Path | Delta Focus |
|-------------|-------------|-------------|
| **README** | "Getting Started" section | Your specific configuration |
| **Tutorial** | Main tutorial steps | Shortcuts, tips, gotchas |
| **Process Docs** | Standard operating procedure | Specific decisions, quality gates |
| **Knowledge Base** | Most common workflow | Tribal knowledge, best practices |
| **Other Skills** | Core workflow patterns | Unique approaches, anti-patterns |
| **External Refs** | Primary use cases | Domain-specific insights |

## Core Workflow: The Golden Path Method

### Step 1: Find the Golden Path

Every document has a **golden path** - the main workflow that practitioners actually follow.

**How to find it:**
- What workflow do people actually use?
- What's the most common task?
- What sequence of steps delivers value?

**Ignore:**
- Edge cases
- Alternative approaches
- Theoretical discussions
- Background context

**Focus on:**
- The path that works
- The steps that matter
- The decisions that count

### Step 2: Extract the Delta

What makes this knowledge **unique**? What can't someone find in a tutorial?

**The Delta Question:**
- What specific insights does this document contain?
- What unique procedures are documented?
- What tribal knowledge is captured?
- What decisions are explained?

**The Delta Test:**
- "Any developer would know this" → Not the Delta
- "This is how I specifically handle this" → That's the Delta

### Step 3: Choose Your Archetype

Based on the golden path, what archetype fits?

Review the Five Archetypes in **Load: meta-architect-claudecode** and select:

| Content Type | Archetype |
|--------------|-----------|
| Single objective | Minimalist |
| Process with verification | Executor |
| Knowledge sharing | Consultant |
| Multiple workflows | Orchestrator |
| Standardized outputs | Generator |

### Step 4: Organize by Intention

**The "Rule of Three":**
- Mentioned once → Keep in SKILL.md
- Mentioned twice → Reference it
- Mentioned three times → Extract to dedicated file

**Content placement:**
- **Core workflow** → SKILL.md (the golden path steps)
- **Supporting knowledge** → references/
- **Concrete patterns** → examples/
- **Reusable code** → scripts/

### Step 5: Craft the Description

Write the description as a **beacon**:

**Format:** "What this does + when to use it + when not to use it"

**Example:**
> "Deploys containerized applications with health checks and rollback. Use when deploying production services that need reliability and monitoring. Do not use for development deployments or one-time tasks."

### Step 6: Extract Examples

Give **one concrete example** of the golden path in action.

**Before (theoretical):**
```markdown
This workflow shows how to deploy applications.
```

**After (concrete):**
```markdown
## Example

User: "Deploy my React app to production"

Agent:
1. Builds the application
2. Pushes to container registry
3. Deploys to production environment
4. Waits for health checks to pass
5. Confirms successful deployment
```

### Step 7: Apply Progressive Disclosure

Keep SKILL.md focused on the core workflow.

**Signs content wants to move:**
- **Detailed explanations** → references/
- **Code patterns** → examples/
- **Complex operations** → scripts/
- **Edge cases** → references/edge-cases.md

### Step 8: Test the Extraction

**The Golden Path Test:**
1. Start with the original documentation
2. Follow your extracted skill
3. Does it achieve the same outcome?
4. Is it simpler and clearer?

## Ingesting Other Skills

When analyzing existing skills to extract patterns:

### Pattern Extraction

1. **Identify the archetype** being used
2. **Extract the decision framework** (how choices are made)
3. **Note the anti-patterns** (what to avoid)
4. **Capture the verification approach** (how success is measured)

### Best Practice Synthesis

When combining patterns from multiple skills:

1. **Find common patterns** across sources
2. **Identify conflicts** and resolve with context
3. **Prefer simpler approaches** when effectiveness is equal
4. **Document the synthesis rationale**

## Ingesting External References

When integrating external documentation (URLs, APIs, libraries):

### Reference Integration Workflow

1. **Identify the primary use case** for your context
2. **Extract the minimal viable setup**
3. **Note environment-specific requirements**
4. **Create fallback strategies** for failures

### External Reference Format

```markdown
## [Reference Name]

**Source:** [URL or location]
**Purpose:** [Why this reference is needed]

**Key Procedures:**
1. [Specific step from reference]
2. [Specific step from reference]

**Caveats:**
- [Environment-specific consideration]
- [Known limitation]
```

## Common Patterns

### From README to Skill

**Golden Path:** Usually the "Getting Started" section
**Delta:** Your specific configuration and approach
**Archetype:** Often Minimalist or Executor
**Structure:** Single SKILL.md, minimal references

### From Tutorial to Skill

**Golden Path:** The main tutorial steps
**Delta:** Your shortcuts, tips, and gotchas
**Archetype:** Often Consultant (sharing knowledge)
**Structure:** SKILL.md + examples/

### From Process Docs to Skill

**Golden Path:** The standard operating procedure
**Delta:** Your specific decisions and quality gates
**Archetype:** Often Executor (reliable process)
**Structure:** SKILL.md + scripts/ for automation

### From Knowledge Base to Skill

**Golden Path:** The most common workflow
**Delta:** Tribal knowledge and best practices
**Archetype:** Often Consultant or Orchestrator
**Structure:** SKILL.md + references/ for deep dives

## Modularization Strategy

For large documents:

1. **Identify the main workflow** → SKILL.md
2. **Extract supporting knowledge** → references/
3. **Create reference files** for:
   - Deep dives
   - Edge cases
   - Decision matrices
   - Troubleshooting

**Target structure:**
```
skill-name/
├── SKILL.md (golden path only)
├── references/
│   ├── deep-dive.md
│   ├── edge-cases.md
│   └── troubleshooting.md
└── examples/
    ├── pattern-1.md
    └── pattern-2.md
```

## Red Flags

**You're doing it wrong if:**
- You're copying the entire document
- You're teaching basics
- You're including multiple approaches
- SKILL.md is 1000+ lines

**You're doing it right if:**
- You've extracted the golden path
- You've captured unique insights
- SKILL.md is focused and clear
- Users can succeed with it

## The Spirit of Ingestion

Ingestion is **synthesis**, not transcription.

You're not creating a copy - you're creating a **condensed, focused, actionable** version.

You're not teaching the technology - you're **sharing your specific approach**.

You're not including everything - you're **extracting the essence**.

**Remember:**
- Find the golden path
- Extract the Delta
- Organize by intention
- Trust the agent's native capabilities
- Keep it simple and focused

## Validation Checklist

**Content Quality:**
- [ ] Extracted the golden path (main workflow)
- [ ] Captured the Delta (unique insights)
- [ ] Applied Delta Standard (no basics)
- [ ] Selected appropriate archetype

**Structure:**
- [ ] SKILL.md focused on core workflow
- [ ] Supporting content in references/
- [ ] Examples in examples/
- [ ] Complex operations in scripts/

**Progressive Disclosure:**
- [ ] Core knowledge in SKILL.md
- [ ] Deep dives in references/
- [ ] Patterns in examples/
- [ ] SKILL.md references these resources

**Quality Indicators:**
- [ ] Description uses third person
- [ ] Includes trigger keywords
- [ ] States what NOT to use for
- [ ] Examples are concrete and working

---

# Evaluating Skill Quality

> This workflow provides a comprehensive evaluation framework for Agent Skills based on the Universal Engineering Standard. For core principles and archetypes, see **Load: meta-architect-claudecode**.

## Tool vs Skill

| Concept | Essence | Function | Example |
|---------|---------|----------|---------|
| **Tool** | What model CAN do | Execute actions | bash, read_file, write_file, WebSearch |
| **Skill** | What model KNOWS how to do | Guide decisions | PDF processing, MCP building, frontend design |

Tools define capability boundaries — without bash tool, model can't execute commands.
Skills inject knowledge — without frontend-design Skill, model produces generic UI.

**The equation**:
```
General Agent + Excellent Skill = Domain Expert Agent
```

Same Claude model, different Skills loaded, becomes different experts.

## Three Types of Knowledge in Skills

When evaluating, categorize each section:

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | Claude genuinely doesn't know this | Must keep — this is the Skill's value |
| **Activation** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant** | Claude definitely knows this | Should delete — wastes tokens |

The art of Skill design is maximizing Expert content, using Activation sparingly, and eliminating Redundant ruthlessly.

## Evaluation Framework (160 points total)

### D1: Knowledge Delta — The Delta Standard (20 points)

**Definition**: Only provide context Claude cannot infer. Focus on expert-only knowledge, not redundant information.

The most important dimension. Does the Skill add genuine expert knowledge?

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics Claude knows (what is X, how to write code, standard library tutorials) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

**Red flags** (instant score ≤5):
- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Explaining how to use common libraries
- Generic best practices ("write clean code", "handle errors")
- Definitions of industry-standard terms

**Green flags** (indicators of high knowledge delta):
- Decision trees for non-obvious choices ("when X fails, try Y because Z")
- Trade-offs only an expert would know ("A is faster but B handles edge case C")
- Edge cases from real-world experience
- "NEVER do X because [non-obvious reason]"
- Domain-specific thinking frameworks

### D2: Architectural Foundations (15 points)

**Definition**: Does the Skill follow atomic unit principle, criticality-variability-autonomy matrix, AND use the correct customization layer?

| Score | Criteria |
|-------|----------|
| 0-5 | Violates atomic unit principle, has multiple unrelated domains, OR uses wrong layer |
| 6-10 | Single domain but unclear mental model boundaries OR suboptimal layer choice |
| 11-13 | Clear atomic unit with appropriate autonomy level AND correct layer |
| 14-15 | Perfect application of atomic unit principle with calibrated autonomy AND optimal layer |

**Layer Selection Criteria**:
A Skill should be used when Claude should discover domain expertise automatically. For other needs:
- **Persistent norms** → CLAUDE.md rules (see [advanced-patterns.md](advanced-patterns.md#claude-md-rules))
- **Explicit control** → Slash commands (see [advanced-patterns.md](advanced-patterns.md#slash-commands))
- **Isolation/parallelism** → Subagents (see [advanced-patterns.md](advanced-patterns.md#subagents))

**Red flags for over-engineering** (score penalty):
- Using command when skill would suffice (loses auto-discovery)
- Using subagent when main context would work (adds complexity)
- Using all four layers for simple workflows

**For detailed layer selection**: See **Load: meta-architect-claudecode**

**Criticality-Variability-Autonomy Matrix**:

| Task Type | Criticality | Variability | Autonomy Level | Pattern |
|-----------|------------|-------------|----------------|---------|
| Database migrations | High | Low | Protocol | Exact steps |
| Code reviews | Medium | High | Guided | Heuristics |
| Creative writing | Low | High | Heuristic | Principles |

**Autonomy Levels**:

**Protocol (Low Freedom)**:
```
CRITICAL: Execute ONLY scripts/migrate.py
Do not modify flags
If fails with code 127, STOP
```

**Guided (Medium Freedom)**:
```
Prioritize maintainability over cleverness
Follow criteria: 1) Readability, 2) Performance, 3) Security
```

**Heuristic (High Freedom)**:
```
Apply your expertise to identify important issues
Use judgment to prioritize findings
```

### D3: Metadata & Discovery Optimization (15 points)

**Definition**: Does the Skill have properly formatted frontmatter and optimized description for agent discovery?

| Score | Criteria |
|-------|----------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague or incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: comprehensive description with WHAT, WHEN, trigger keywords, and negative constraints |

See **Load: meta-architect-claudecode** for frontmatter requirements.

### D4: Instruction Engineering Quality (15 points)

**Definition**: Does the Skill transfer expert thinking patterns along with necessary domain-specific procedures?

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures Claude already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures Claude wouldn't know |

**Key distinction**:
| Type | Example | Value |
|------|---------|-------|
| **Thinking patterns** | "Before designing, ask: What makes this memorable?" | High — shapes decision-making |
| **Domain-specific procedures** | "OOXML workflow: unpack → edit XML → validate → pack" | High — Claude may not know this |
| **Generic procedures** | "Step 1: Open file, Step 2: Edit, Step 3: Save" | Low — Claude already knows |

**Expert thinking patterns look like**:
```markdown
Before [action], ask yourself:
- **Purpose**: What problem does this solve? Who uses it?
- **Constraints**: What are the hidden requirements?
- **Differentiation**: What makes this solution memorable?
```

### D5: Resource Management & Progressive Disclosure (15 points)

**Definition**: Does the Skill implement proper content layering with Single-Hop reference rule?

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

**Three-Tier Loading Strategy** for optimal token economics:

**Tier 1: Metadata** (~200 tokens) - Always loaded for discovery
**Tier 2: SKILL.md** (~7,000 tokens) - Loaded when Skill is invoked
**Tier 3: Resources** (on-demand fragments) - Loaded on specific demand only

**Single-Hop Rule**: All references must be at one level of distance from SKILL.md

### D6: Validation & Quality Control (15 points)

**Definition**: Does the Skill implement Plan-Validate-Execute pattern for high-criticality operations?

| Score | Criteria |
|-------|----------|
| 0-5 | No validation for high-risk operations |
| 6-10 | Basic validation but not systematic |
| 11-13 | Good validation strategy for critical operations |
| 14-15 | Complete Plan-Validate-Execute with machine-verifiable gates |

See **Load: meta-architect-claudecode** for Plan-Validate-Execute Pattern details.

### D7: Error Handling & Resilience (10 points)

**Definition**: Does the Skill implement defensive programming and recovery patterns?

| Score | Criteria |
|-------|----------|
| 0-3 | No error handling strategy |
| 4-6 | Basic error handling without patterns |
| 7-8 | Good error handling with recovery patterns |
| 9-10 | Comprehensive defensive programming with machine-verifiable error states |

**Defensive Programming**:

**Fail-Safe by Design**:
- Always validate inputs before processing
- Check permissions before execution
- Verify environment readiness
- Use explicit checkpoints in workflows

**Machine-Verifiable Error States**:
- Scripts must return structured error codes
- Clear distinction between recoverable and fatal errors
- Provide actionable error messages
- Enable automatic retry for transient failures

### D8: Universal Skill Archetypes (15 points)

**Definition**: Does the Skill follow appropriate structural or execution archetype?

| Score | Criteria |
|-------|----------|
| 0-5 | No recognizable pattern, chaotic structure |
| 6-10 | Partially follows a pattern with significant deviations |
| 11-13 | Clear pattern with minor deviations |
| 14-15 | Masterful application of appropriate archetype |

See **Load: meta-architect-claudecode** for Structural Archetypes.

### D9: Anti-Pattern Quality & NEVER Lists (10 points)

**Definition**: Does the Skill have effective NEVER lists with expert-level anti-patterns?

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful", "consider edge cases") |
| 8-9 | Specific NEVER list with some reasoning |
| 10 | Expert-grade anti-patterns with WHY — things only experience teaches |

**Why this matters**: Half of expert knowledge is knowing what NOT to do. A senior designer sees purple gradient on white background and instinctively cringes — "too AI-generated." This intuition for "what absolutely not to do" comes from stepping on countless landmines.

**Expert anti-patterns** (specific + reason):
```markdown
NEVER use generic AI-generated aesthetics like:
- Overused font families (Inter, Roboto, Arial)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Default border-radius on everything
```

### D10: Testing & Validation Strategy (10 points)

**Definition**: Does the Skill incorporate model-specific testing and success metrics?

| Score | Criteria |
|-------|----------|
| 0-3 | No testing or validation strategy |
| 4-6 | Basic testing approach without metrics |
| 7-8 | Good testing strategy with clear success criteria |
| 9-10 | Comprehensive validation framework with theoretical grounding |

**Model-Specific Testing**:

**Test Across Model Types**:
- **Haiku** (fast, economical): Does the Skill provide enough guidance?
- **Sonnet** (balanced): Is the Skill clear and efficient?
- **Opus** (powerful reasoning): Does the Skill avoid over-explaining?

**Success Metrics**:
- **Activation Rate**: Percentage of appropriate activations
- **Success Rate**: Percentage of successful task completions
- **Context Efficiency**: Information density vs. capability ratio

### D11: Security & Safety Implementation (10 points)

**Definition**: Does the Skill implement least privilege and validation-first safety?

| Score | Criteria |
|-------|----------|
| 0-3 | No security or safety considerations |
| 4-6 | Basic safety measures without systematic approach |
| 7-8 | Good security practices with validation gates |
| 9-10 | Comprehensive security framework with machine-verifiable checks |

**Permission Management**:

**Least Privilege Principle**:
- Restrict tools to minimum required
- Use allowlists, not denylists
- Validate before execution

### D12: Autonomy & Question Bursting Discipline (10 points)

**Definition**: Does the Skill follow the autonomy contract — can it complete without questions in 80-95% of expected cases?

| Score | Criteria |
|-------|----------|
| 0-3 | Ask-first pattern, no exploration phase, vague stop criteria |
| 4-6 | Some autonomy but relies on questions for common cases |
| 7-8 | Good autonomy with "explore first" before "ask" |
| 9-10 | Excellent: 80-95% autonomous, explicit stop criteria, knows when to escalate |

**Autonomy Contract Checklist**:
- [ ] Can complete without questions in 80-95% of expected cases
- [ ] Has "explore first" path (read/grep/inspection) before "ask"
- [ ] Has explicit success/stop criteria
- [ ] Knows when to recommend a command (explicit control needed)
- [ ] Knows when to recommend fork (noise isolation needed)

**Question Burst Policy** (authorized ONLY when all 3 true):
- Information NOT inferrable from repo/tools
- High impact if wrong choice
- Small question set (3-7 max) unlocks everything

**Escalation Hygiene**:
- Too complex/risky for auto-discovery → recommend command
- Long/noisy work → recommend subagent or forked variant

**For detailed autonomy guidance**: See **Load: meta-architect-claudecode**

## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted
- **NEVER** ignore token waste — every redundant paragraph should result in deduction
- **NEVER** let length impress you — a 43-line Skill can outperform a 500-line Skill
- **NEVER** skip mentally testing the decision trees — do they actually lead to correct choices?
- **NEVER** forgive explaining basics with "but it provides helpful context"
- **NEVER** overlook missing anti-patterns — if there's no NEVER list, that's a significant gap
- **NEVER** assume all procedures are valuable — distinguish domain-specific from generic
- **NEVER** undervalue the description field — poor description = skill never gets used
- **NEVER** put "when to use" info only in the body — Agent only sees description before loading
- **NEVER** blindly enforce scripts for simple operations Claude natively handles
- **NEVER** accept generic best practices without domain-specific expertise

## Evaluation Protocol

### Step 1: First Pass — Knowledge Delta Scan

Read SKILL.md completely and for each section ask:
> "Does Claude already know this?"

Mark each section as:
- **[E] Expert**: Claude genuinely doesn't know this — value-add
- **[A] Activation**: Claude knows but brief reminder is useful — acceptable
- **[R] Redundant**: Claude definitely knows this — should be deleted

Calculate rough ratio: E:A:R
- Good Skill: >70% Expert, <20% Activation, <10% Redundant
- Mediocre Skill: 40-70% Expert, high Activation
- Bad Skill: <40% Expert, high Redundant

### Step 2: Structural Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and their sizes
[ ] Identify which archetype the Skill follows
[ ] Check for loading triggers (if references exist)
[ ] Verify autonomy level matches task characteristics
```

### Step 3: Score Each Dimension

For each of the 12 dimensions:
1. Find specific evidence (quote relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < max

### Step 4: Calculate Total & Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8 + D9 + D10 + D11 + D12
Max = 160 points
```

**Grade Scale** (percentage-based):
| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90%+ (144+) | Excellent — production-ready expert Skill |
| B | 80-89% (128-143) | Good — minor improvements needed |
| C | 70-79% (112-127) | Adequate — clear improvement path |
| D | 60-69% (96-111) | Below Average — significant issues |
| F | <60% (<96) | Poor — needs fundamental redesign |

### Step 5: Generate Report

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/160 (X%)
- **Grade**: [A/B/C/D/F]
- **Primary Archetype**: [Archetype from D8]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Autonomy Level**: [Protocol/Guided/Heuristic]
- **Verdict**: [One sentence assessment]

## Dimension Scores

| Dimension | Score | Max | Grade | Notes |
|-----------|-------|-----|-------|-------|
| D1: Knowledge Delta | X | 20 | | |
| D2: Architectural Foundations | X | 15 | | |
| D3: Metadata & Discovery | X | 15 | | |
| D4: Instruction Engineering | X | 15 | | |
| D5: Resource Management | X | 15 | | |
| D6: Validation & Quality Control | X | 15 | | |
| D7: Error Handling & Resilience | X | 10 | | |
| D8: Universal Skill Archetypes | X | 15 | | |
| D9: Anti-Pattern Quality | X | 10 | | |
| D10: Testing & Validation Strategy | X | 10 | | |
| D11: Security & Safety | X | 10 | | |
| D12: Autonomy & Question Bursting | X | 10 | | |

## Critical Issues
[List must-fix problems that significantly impact the Skill's effectiveness]

## Top 5 Improvements
1. [Highest impact improvement with specific guidance]
2. [Second priority improvement]
3. [Third priority improvement]
4. [Fourth priority improvement]
5. [Fifth priority improvement]

## Detailed Analysis
[For each dimension scoring below 80%, provide:
- What's missing or problematic
- Specific examples from the Skill
- Concrete suggestions for improvement]
```

## Common Failure Patterns

### Pattern 1: The Tutorial
```
Symptom: Explains what PDF is, how Python works, basic library usage
Root cause: Author assumes Skill should "teach" the model
Fix: Claude already knows this. Delete all basic explanations.
     Focus on expert decisions, trade-offs, and anti-patterns.
```

### Pattern 2: The Dump
```
Symptom: SKILL.md is 800+ lines with everything included
Root cause: No progressive disclosure design
Fix: Core routing and decision trees in SKILL.md (<300 lines ideal)
     Detailed content in references/, loaded on-demand
```

### Pattern 3: The Orphan References
```
Symptom: References directory exists but files are never loaded
Root cause: No explicit loading triggers
Fix: Add "MANDATORY - READ ENTIRE FILE" at workflow decision points
     Add "Do NOT Load" to prevent over-loading
```

### Pattern 4: The Checkbox Procedure
```
Symptom: Step 1, Step 2, Step 3... mechanical procedures
Root cause: Author thinks in procedures, not thinking frameworks
Fix: Transform into "Before doing X, ask yourself..."
     Focus on decision principles, not operation sequences
```

### Pattern 5: The Vague Warning
```
Symptom: "Be careful", "avoid errors", "consider edge cases"
Root cause: Author knows things can go wrong but hasn't articulated specifics
Fix: Specific NEVER list with concrete examples and non-obvious reasons
     "NEVER use X because [specific problem that takes experience to learn]"
```

### Pattern 6: The Invisible Skill
```
Symptom: Great content but skill rarely gets activated
Root cause: Description is vague, missing keywords, or lacks trigger scenarios
Fix: Description must answer WHAT, WHEN, and include KEYWORDS
     "Use when..." + specific scenarios + searchable terms
```

### Pattern 7: The Wrong Location
```
Symptom: "When to use this Skill" section in body, not in description
Root cause: Misunderstanding of three-layer loading
Fix: Move all triggering information to description field
     Body is only loaded AFTER triggering decision is made
```

### Pattern 8: The Over-Engineered
```
Symptom: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, CONTRIBUTING.md
Root cause: Treating Skill like a software project
Fix: Delete all auxiliary files. Only include what Agent needs for the task.
     No documentation about the Skill itself.
```

### Pattern 9: The Freedom Mismatch
```
Symptom: Rigid scripts for creative tasks, vague guidance for fragile operations
Root cause: Not considering task fragility
Fix: High freedom for creative (principles, not steps)
     Low freedom for fragile (exact scripts, no parameters)
```

### Pattern 10: The Script Envy
```
Symptom: Creating scripts for operations Claude natively handles
Root cause: Over-reliance on scripting
Fix: Use native tools for: read_file, write_file, bash, grep, etc.
     Use scripts ONLY for: API calls, data transformations, specialized tools
```

## The Meta-Question

When evaluating any Skill, always return to this fundamental question:

> **"Would an expert in this domain, looking at this Skill, say:**
> **'Yes, this captures knowledge that took me years to learn'?"**

If the answer is yes → the Skill has genuine value.
If the answer no → it's compressing what Claude already knows.

The best Skills are **compressed expert brains** — they take a designer's 10 years of aesthetic accumulation and compress it into 43 lines, or a document expert's operational experience into a 200-line decision tree.

What gets compressed must be things Claude doesn't have. Otherwise, it's garbage compression.

## Quick Reference Checklist

### Skill Evaluation Quick Check (12 Dimensions)

**D1: Knowledge Delta (Most Important):**
- [ ] No "What is X" explanations for basic concepts
- [ ] No step-by-step tutorials for standard operations
- [ ] Has decision trees for non-obvious choices
- [ ] Has trade-offs only experts would know
- [ ] Has edge cases from real-world experience

**D2: Architectural Foundations:**
- [ ] Follows atomic unit principle
- [ ] Autonomy level matches task characteristics
- [ ] Single domain, clear mental model

**D3: Metadata & Discovery:**
- [ ] Valid YAML frontmatter
- [ ] name: lowercase, ≤64 chars, gerund form
- [ ] description answers: WHAT does it do?
- [ ] description answers: WHEN should it be used?
- [ ] description contains trigger KEYWORDS
- [ ] description includes negative constraints (what NOT to use for)

**D4: Instruction Engineering:**
- [ ] Transfers thinking patterns (how to think about problems)
- [ ] Has "Before doing X, ask yourself..." frameworks
- [ ] Includes domain-specific procedures Claude wouldn't know
- [ ] Distinguishes valuable procedures from generic ones

**D5: Resource Management & Progressive Disclosure:**
- [ ] SKILL.md < 500 lines (ideal < 300)
- [ ] Heavy content in references/
- [ ] Loading triggers embedded in workflow
- [ ] Has "Do NOT Load" for preventing over-loading
- [ ] Single-Hop rule followed (no nested references)

**D6: Validation & Quality Control:**
- [ ] Plan-Validate-Execute for high-criticality operations
- [ ] Machine-verifiable validation gates
- [ ] Reversible planning for critical operations

**D7: Error Handling & Resilience:**
- [ ] Defensive programming implemented
- [ ] Machine-verifiable error states
- [ ] Recovery patterns (idempotent operations, graceful degradation)

**D8: Universal Skill Archetypes:**
- [ ] Follows appropriate structural archetype (A-D)
- [ ] Follows appropriate execution archetype (E-F) if applicable
- [ ] Avoids anti-patterns (Mega-Skill, Script Envy)

**D9: Anti-Pattern Quality:**
- [ ] Has explicit NEVER list
- [ ] Anti-patterns are specific, not vague
- [ ] Includes WHY (non-obvious reasons)

**D10: Testing & Validation Strategy:**
- [ ] Model-specific testing considerations (Haiku, Sonnet, Opus)
- [ ] Success metrics defined
- [ ] Theoretical validation framework

**D11: Security & Safety:**
- [ ] Least privilege principle implemented
- [ ] Validation-first safety
- [ ] Machine-verifiable checks

**D12: Autonomy & Question Bursting:**
- [ ] Can complete without questions in 80-95% of expected cases
- [ ] Has "explore first" path (read/grep) before "ask"
- [ ] Has explicit success/stop criteria
- [ ] Knows when to recommend command for explicit control
- [ ] Knows when to recommend fork for noise isolation


---

## Writing Style Requirements

### Imperative/Infinitive Form

Write using verb-first instructions, not second person:

**Correct (imperative):**
```
To create a hook, define the event type.
Configure the MCP server with authentication.
Validate settings before use.
```

**Incorrect (second person):**
```
You should create a hook by defining the event type.
You need to configure the MCP server.
You must validate settings before use.
```

### Third-Person in Description

The frontmatter description must use third person:

**Correct:**
```yaml
description: This skill should be used when the user asks to "create X", "configure Y"...
```

**Incorrect:**
```yaml
description: Use this skill when you want to create X...
description: Load this skill when user asks...
```

---

## Anti-Patterns to Avoid (Building-Specific)

### Weak Trigger Description

**Bad:** `description: Provides guidance for working with hooks.`
→ Vague, no specific trigger phrases, not third person

**Good:** `description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events.`
→ Third person, specific phrases, concrete scenarios

### Too Much in SKILL.md

**Bad:** 8,000 words in one file
→ Bloats context, detailed content always loaded

**Good:** 1,800 words in SKILL.md + references/patterns.md (2,500 words) + references/advanced.md (3,700 words)
→ Progressive disclosure, loaded only when needed

### Missing Resource References

**Bad:** SKILL.md with no mention of references/ or examples/
→ Claude doesn't know references exist

**Good:** Section at end listing all available resources
→ Claude knows where to find additional information

---

## Security Considerations

Script execution introduces security risks. Consider:

- **Sandboxing:** Run scripts in isolated environments
- **Allowlisting:** Only execute scripts from trusted skills
- **Confirmation:** Ask users before running potentially dangerous operations
- **Logging:** Record all script executions for auditing

---

## Validation Checklist

**Structure:**
- [ ] SKILL.md file exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description` fields
- [ ] Referenced files actually exist

**Description Quality:**
- [ ] Uses third person ("This skill should be used when...")
- [ ] Includes specific trigger phrases users would say
- [ ] Lists concrete scenarios ("create X", "configure Y")
- [ ] Not vague or generic

**Content Quality:**
- [ ] SKILL.md body uses imperative/infinitive form
- [ ] Body is focused and lean (1,500-2,000 words ideal)
- [ ] Detailed content moved to references/
- [ ] Examples are complete and working

**Progressive Disclosure:**
- [ ] Core concepts in SKILL.md
- [ ] Detailed docs in references/
- [ ] Working code in examples/
- [ ] Utilities in scripts/
- [ ] SKILL.md references these resources

**Autonomy Design:**
- [ ] 80-95% of expected cases can complete without questions
- [ ] "Explore first" path implemented before "ask"
- [ ] Explicit success/stop criteria defined
- [ ] Fork pattern documented (if applicable)

---

## Common Mistakes to Avoid

1. **Deep Nesting** - `references/v1/setup/config.md` → Flatten to `references/setup-config.md`
2. **Vague Description** - "Helps with coding." → Use clear capability + use case
3. **Over-Engineering** - Scripts for simple tasks → Use Native-First Principle
4. **Code Blocks in Body** - Large code blocks in SKILL.md → Move to examples/ or scripts/

---

## Quality Validation

**Quick sanity checks:**
- Does it follow the 3 Core Principles?
- Does it apply the Delta Standard?
- Would you recommend this to a friend?

**Signs of Readiness:**
- The name feels right (matches the essence)
- The description makes sense (clear value, when to use, when not)
- The structure feels natural (content where it belongs)
- Examples demonstrate the value (not just theory)

**Signs Something's Off:**
- Reading takes more than 2 minutes
- You're explaining what everyone knows
- Examples are theoretical, not practical
- Structure feels forced (content in wrong places)
- The skill tries to do too much

**The Real Test:**
1. Start a new conversation
2. Ask the skill to do its job
3. Does it work? That's validation
