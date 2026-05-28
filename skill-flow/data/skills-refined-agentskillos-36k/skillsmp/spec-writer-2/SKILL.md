---
name: spec-writer
description: This skill should be used when the user asks to "create a spec", "write a specification", "create a feature specification", "build a requirements document", "gather requirements", "develop user stories", "start discovery process", or mentions needing help with requirements analysis or product specification. Guides users through a structured discovery process where stories emerge from problem understanding rather than being predefined.
version: 0.1.0
---

# Spec Writer

## Purpose

Guide users through creating complete, unambiguous feature specifications using a discovery-driven process. Unlike traditional requirements gathering that starts with predefined user stories, this skill helps stories emerge naturally from deep problem understanding. The resulting specification is comprehensive enough for implementation without further clarification.

## Core Philosophy

**Stories emerge from discovery, they don't precede it.**

Begin by understanding the problem space. Stories crystallize as understanding deepens through iterative exploration. Stories may split, merge, be added, or be revised as learning progresses—even after being written into the specification.

## When to Use This Skill

Use this skill when the user needs to:

- Transform a feature idea into a detailed specification
- Understand and document a problem before designing solutions
- Develop user stories through structured discovery
- Create implementation-ready requirements documentation
- Guide stakeholders through requirements clarification

## State Management Architecture

### The Compaction Mechanism

SPEC.md serves as the compaction mechanism. As user stories reach full clarity, they graduate from working state into the deliverable specification. STATE.md holds only in-flight work. SPEC.md is a living document—graduated stories can be revised when new information warrants it.

### Discovery Directory Structure

```
discovery/
├── SPEC.md            # Progressive deliverable (mutable)
├── STATE.md           # Working memory (current work)
├── OPEN_QUESTIONS.md  # Current blockers
└── archive/
    ├── DECISIONS.md   # Decision history
    ├── RESEARCH.md    # Research log
    ├── ITERATIONS.md  # Iteration summaries
    └── REVISIONS.md   # Changes to graduated stories
```

## Discovery Process Overview

### Phase 1: Problem Space Exploration

**Goal**: Understand the problem before proposing solutions.

**Activities**:
- Ask open-ended questions about the problem domain
- Research similar solutions and industry patterns
- Identify stakeholders and personas
- Map current state vs. desired state

**Outputs to STATE.md**:
- Problem statement (draft, iteratively refined)
- Identified personas
- Current vs. desired state comparison
- Emerging themes (proto-stories)

**Exit Criteria**:
- Core problem articulated in one paragraph
- Primary personas identified
- At least 2-3 proto-stories emerging from themes

### Phase 2: Story Crystallization

**Goal**: Transform themes into concrete, prioritized user stories.

Proto-stories become real stories when they have:
- A clear actor (persona)
- A clear goal
- A clear value proposition ("so that...")
- Sufficient shape to enable specific questions

**Activities**:
- Propose story candidates from emerged themes
- Collaborate with user to prioritize (P1, P2, P3...)
- Identify dependencies between stories
- Validate stories are independently valuable

**Outputs to STATE.md**:
- Story backlog with priorities
- Story dependency map
- Initial confidence assessment per story

**Exit Criteria**:
- User has agreed on initial story set and priorities
- Each story passes "independently testable" validation
- Ready to deep-dive on P1 story

### Phase 3: Story Development (Iterative)

**Goal**: Develop each story to graduation-ready clarity.

Work through stories by priority while remaining alert to:
- New stories emerging from questions
- Existing stories needing to split
- Stories that should merge
- Cross-cutting concerns affecting multiple stories

**Activities**:
- Deep-dive questions on focused story
- Story-specific research
- Draft acceptance scenarios
- Identify edge cases and requirements
- Validate with user

**Graduation Criteria** (per story):
- 100% confidence on story scope
- All blocking questions resolved
- Acceptance scenarios specific and testable
- Edge cases identified with defined handling
- Requirements extractable
- Success criteria measurable

**Graduation Protocol**:
1. Confirm with user: "Story [X] feels complete. Here's the summary: [brief]. Ready to graduate to SPEC.md?"
2. If yes: Write full story to SPEC.md, update STATE.md
3. Move to next priority story

### Phase 4: Continuous Refinement

**Reality**: Discovery doesn't end when a story graduates.

Later stories may reveal:
- Gaps in earlier stories
- Conflicting requirements
- Shared concerns not previously visible
- Edge cases spanning stories

**Process**:
- Flag when new information affects graduated stories
- Propose revisions to SPEC.md when warranted
- Log all revisions to archive/REVISIONS.md
- Re-confirm with user before modifying graduated work

**Revision Types**:
- **Additive**: New acceptance scenario, edge case, requirement
- **Modificative**: Changing existing scenario or requirement
- **Structural**: Story splits or merges

**All revisions require**:
- User confirmation before changing SPEC.md
- Entry in archive/REVISIONS.md
- Update to affected decision/research references

## Session Start Protocol

### Fresh Start (No existing discovery/)

1. Begin with opening question to understand the problem and identify a feature name:

"Let's build a feature specification together. I'm going to start by understanding the problem space - we'll figure out the user stories together as we go.

Tell me: What problem are you trying to solve? Who experiences this problem, and what does their life look like today without a solution?"

2. Once you understand the problem and have identified an appropriate feature name, use `scripts/init-spec.sh <feature-name> --base-path "${CLAUDE_WORKING_DIRECTORY}"` (Tier 1 Essential) to initialize the discovery/ directory with all required files at the project root. See `references/scripts-tier-1.md` for detailed usage.

3. Continue the discovery process from the project root (discovery/ directory will be created there)

### Resuming (Existing discovery/)

1. Read SPEC.md header + completed story count
2. Read STATE.md (in-flight work)
3. Read OPEN_QUESTIONS.md
4. Report current state:

"We're in Phase [X]. [N] stories completed, working on [Story Y]. [M] blocking questions. Any graduated stories at revision risk: [list]"

**Field Update Rules**: For exhaustive guidance on when to update each field and section, see `references/file-operations.md`.

## Question Management

### Question Categories

Track questions in OPEN_QUESTIONS.md by type using `add-question.py` (Tier 1 Essential):

- **🔴 Blocking**: Prevents progress on current story
- **🟡 Clarifying**: Needed for completeness, not blocking
- **🔵 Research Pending**: Requires investigation
- **🟠 Watching**: May affect graduated stories

Use `resolve-question.py` (Tier 2 Automation) to remove questions when answered.

See `references/scripts-tier-1.md` and `references/scripts-tier-2.md` for details.

### TodoWrite Integration

Use TodoWrite to track:
- Current phase
- Blocking questions for active story
- Emerging stories needing investigation
- Watching items (graduated story risks)
- Ready actions (stories ready to graduate)

## Rules of Engagement

- **Problem before solution** - Understand problem space before structuring stories
- **Stories emerge** - Let them crystallize from understanding, don't assign them
- **Stories are mutable** - Even graduated work can be revised with new information
- **Graduation is not forever** - Flag and revise when later discovery reveals gaps
- **Always confirm changes** - Never modify SPEC.md without user approval
- **Track everything** - Log decisions, research, revisions
- **Quantify everything** - Replace vague terms with specific numbers ("fast" → "under 200ms", "many" → "up to 10,000")
- **Challenge assumptions** - Question both your assumptions and the user's

## Completion Criteria

The specification is complete when:

- All identified stories graduated to SPEC.md
- No proto-stories remain in STATE.md
- OPEN_QUESTIONS.md is empty (including Watching list)
- All cross-cutting concerns addressed
- User confirms: "This spec captures everything"

### Final Deliverable Check

Before marking complete, verify:
- [ ] Every story independently testable
- [ ] Every acceptance scenario specific (no ambiguity)
- [ ] Every edge case has defined handling
- [ ] Every requirement is specific and measurable
- [ ] Every success criterion has numbers, not vibes
- [ ] Glossary captures all domain terms
- [ ] Run `validate-spec.py` (Tier 1) for final validation
- [ ] User has done final review and approved

## Context Recovery

### Standard Resume

1. Read SPEC.md header + story status markers
2. Read STATE.md
3. Read OPEN_QUESTIONS.md
4. Report current state and continue

### User Asks About Completed Story

1. Read that story section from SPEC.md
2. If context needed, search archive files

### User Wants to Restart or Revise

1. Confirm: "Do you want to revise specific stories, or restart discovery entirely?"
2. If restart: Archive current files, begin fresh
3. If revise: Identify what to reconsider, move back to appropriate phase

## Additional Resources

### Reference Files

For detailed templates and formats:

- **`references/file-templates.md`** - Manual operations reference showing what sections you must write manually vs what scripts handle. Focus on Problem Understanding, In-Progress Story Detail, and manual metadata updates.
- **`references/file-operations.md`** - Exhaustive field-level update rules, sync checkpoints, and cross-file consistency invariants. Reference when updating files to ensure all required fields are updated and cross-references maintained.
- **`references/phase-guide.md`** - Comprehensive phase-by-phase guidance with questioning strategies, research approaches, and transition criteria

### Example Files

Working examples in `examples/`:

- **`examples/sample-spec/`** - Complete example specification showing the discovery process from problem exploration through graduated stories

### Helper Scripts

The spec-writer skill includes 14 automation scripts in `scripts/` organized in four tiers by functionality.

**Script Organization**:

- **Tier 1: Essential Scripts** (6 scripts) - Initialization, question management, decision logging, validation
- **Tier 2: High-Value Automation** (4 scripts) - Story graduation, status updates, research search
- **Tier 3: Enhancement Scripts** (3 scripts) - Research logging, revisions, status monitoring
- **Tier 4: Specialized Tables** (3 scripts) - Edge cases, requirements, success criteria

**Quick Start**:
```bash
# Initialize new spec (creates discovery/ at project root)
scripts/init-spec.sh payment-flow-redesign --base-path "${CLAUDE_WORKING_DIRECTORY}"

# Add question
scripts/add-question.py \
  --question "Who are the primary users?" \
  --category clarifying

# Log decision
scripts/log-decision.py \
  --title "Use REST API" \
  --context "Need API protocol" \
  --decision "REST with JSON" \
  --stories "Story 1, Story 2"

# Find decisions
scripts/find-decisions.py --story 1

# Validate spec
scripts/validate-spec.py
```

**Smart Directory Discovery**: All scripts automatically locate `discovery/` directory using:
1. Explicit `--discovery-path` flag
2. Current directory if in `discovery/`
3. Auto-locate in parent directories

**Script Reference Documentation**:

Read the appropriate tier reference based on your current task:

- **`references/scripts-tier-1.md`** - Read when: starting new spec, adding questions, logging decisions, finding past decisions, validating spec integrity
  - init-spec.sh, next-id.py, add-question.py, find-decisions.py, log-decision.py, validate-spec.py

- **`references/scripts-tier-2.md`** - Read when: graduating stories to SPEC.md, changing story status, resolving questions, searching research log
  - graduate-story.py, update-story-status.py, resolve-question.py, find-research.py

- **`references/scripts-tier-3.md`** - Read when: logging research findings, recording revisions to graduated stories, getting quick status overview
  - log-research.py, add-revision.py, story-status.sh

- **`references/scripts-tier-4.md`** - Read when: adding edge cases, extracting functional requirements, defining success criteria
  - add-edge-case.py, add-functional-requirement.py, add-success-criteria.py

**Progressive Reading**: Start with Tier 1 for basic operations, read higher tiers only when needed for specific tasks.

## When to Use Scripts

The 16 automation scripts are organized into 4 tiers by functionality and use case. Use this quick reference to find the right script and its documentation.

### Quick Reference: Task → Tier

| Task | Tier | Key Scripts | Reference |
|------|------|-------------|-----------|
| Starting a new spec | 1 | init-spec.sh | scripts-tier-1.md |
| Adding questions | 1 | add-question.py | scripts-tier-1.md |
| Logging decisions | 1 | log-decision.py | scripts-tier-1.md |
| Finding decisions | 1 | find-decisions.py | scripts-tier-1.md |
| Validating spec | 1 | validate-spec.py | scripts-tier-1.md |
| Graduating stories | 2 | graduate-story.py | scripts-tier-2.md |
| Changing story status | 2 | update-story-status.py | scripts-tier-2.md |
| Resolving questions | 2 | resolve-question.py | scripts-tier-2.md |
| Finding research | 2 | find-research.py | scripts-tier-2.md |
| Logging research | 3 | log-research.py | scripts-tier-3.md |
| Recording revisions | 3 | add-revision.py | scripts-tier-3.md |
| Logging iterations | 3 | log-iteration.py | scripts-tier-3.md |
| Finding iterations | 3 | find-iterations.py | scripts-tier-3.md |
| Status overview | 3 | story-status.sh | scripts-tier-3.md |
| Adding edge cases | 4 | add-edge-case.py | scripts-tier-4.md |
| Adding requirements | 4 | add-functional-requirement.py | scripts-tier-4.md |
| Adding success criteria | 4 | add-success-criteria.py | scripts-tier-4.md |

### Tier Documentation

**Read the appropriate tier reference based on your current task:**

- **Tier 1: Essential Scripts** — `references/scripts-tier-1.md`

  Read when: starting new spec, adding questions, logging decisions, finding past decisions, validating spec integrity

  Core scripts for initialization and basic discovery operations.

- **Tier 2: High-Value Automation** — `references/scripts-tier-2.md`

  Read when: graduating stories to SPEC.md, changing story status, resolving questions, searching research log

  Advanced workflow automation for story lifecycle management.

- **Tier 3: Enhancement Scripts** — `references/scripts-tier-3.md`

  Read when: logging research findings, recording revisions to graduated stories, logging iteration summaries, getting quick status overview

  Support scripts for research, revisions, iteration tracking, and monitoring.

- **Tier 4: Specialized Tables** — `references/scripts-tier-4.md`

  Read when: adding edge cases, extracting functional requirements, defining success criteria

  Scripts for managing SPEC.md requirement tables.

**Progressive Reading Strategy:**
1. Start with Tier 1 for basic operations
2. Read higher tiers only when needed for specific tasks
3. Each tier reference includes complete usage examples and workflow patterns

## Implementation Approach

### Phase Transitions

Monitor for transition signals:

- **Phase 1 → 2**: Problem statement clear, personas identified, proto-stories emerging
- **Phase 2 → 3**: Story backlog confirmed, priorities agreed, ready to deep-dive
- **Phase 3 → 4**: First story graduates (automatic—always in refinement mode afterward)
- **Phase 4 → Complete**: All stories graduated, no open questions, user confirms completeness

### Story Development Workflow

For each story (in priority order):

1. **Update status** - Use `update-story-status.py` (Tier 2) to mark story as "In Progress"
2. **Deep-dive questions** - Track with `add-question.py` (Tier 1)
3. **Research** - Log findings with `log-research.py` (Tier 3)
4. **Draft and validate** - Extract requirements with Tier 4 scripts
5. **Check graduation criteria** - All blockers resolved? Testable? Complete?
6. **Graduate** - Use `graduate-story.py` (Tier 2) to move to SPEC.md
7. **Validate** - Run `validate-spec.py` (Tier 1) to check integrity
8. **Log iteration** - Use `log-iteration.py` (Tier 3) after completing story cycle

See appropriate tier references for detailed usage. For graduation field updates and sync rules, see `references/file-operations.md`.

Stay alert for:
- New stories emerging (add to backlog, discuss priority)
- Stories needing to split (too complex)
- Stories needing to merge (too coupled)
- Questions affecting graduated stories (add to Watching list)

### Revision Management

When new information affects graduated stories:

1. Flag immediately: "This answer suggests we may need to revise Story 1. Specifically: [what might change]"
2. Ask user: "Should I proceed with this revision, or do you want to discuss first?"
3. If approved:
   - Log revision with `add-revision.py` (Tier 3 Enhancement)
   - Update SPEC.md manually
   - Update affected requirements/edge cases with Tier 4 scripts if needed
4. Update cross-references and validate with `validate-spec.py` (Tier 1)

For revision field updates and sync rules, see `references/file-operations.md`. For revision logging script details, see `references/scripts-tier-3.md`.

## Best Practices

- Begin each session by checking for existing discovery/ directory
- Use STATE.md as working memory, SPEC.md as graduated deliverable
- Track all questions in OPEN_QUESTIONS.md for visibility
- Log decisions and research in archive files for traceability
- Update STATE.md frequently to reflect current understanding
- Graduate stories only when 100% confident
- Flag potential revisions to graduated stories proactively
- Quantify all vague terms in requirements and success criteria
- Challenge assumptions respectfully but firmly
- Maintain story independence for testability

Start by checking if `discovery/SPEC.md` exists, then follow the appropriate protocol (fresh start or resume). Guide the user through discovery with patience, using questions to deepen understanding rather than rushing to document preconceived stories.
