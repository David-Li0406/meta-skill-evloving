---
name: kramme:structured-implementation-workflow
description: Use a structured workflow with three interconnected documents (main specification, open issues, and log) to plan, track, and document complex implementations, ensuring clarity and continuity. Use when you detect the presence of LOG.md and OPEN_ISSUES.md files.
---

# Structured Implementation Workflow

## Instructions

Provide clear, step-by-step guidance for Claude.

**When to use this skill:**

- You're implementing a complex feature or project requiring planning and decision tracking
- You're building comprehensive documentation or detailed technical content
- You need to track implementation decisions, open issues, and specifications
- You're working on multi-day projects with investigation and research phases
- You're creating technical designs, API documentation, or system architecture
- You're writing detailed guides, tutorials, or educational content
- You are asked to use the Structured Implementation Workflow

**When NOT to use this skill:**

- Small bug fixes or minor changes (< 1 day work)
- Trivial updates without architectural decisions
- Simple refactoring without functional changes
- Quick documentation fixes

**Context:** This is a structured approach using three interconnected working documents that serve different purposes:

1. **Main Specification** - The permanent deliverable (you'll choose an appropriate name like FEATURE_SPECIFICATION.md, DOCUMENTATION_SPEC.md, PROJECT_PLAN.md, etc.)
2. **OPEN_ISSUES.md** - Temporary working document for active blockers and investigations
3. **LOG.md** - Temporary log tracking session progress and decision rationale

The main specification is permanent and kept long-term. The other two are temporary scaffolding deleted after completion.

---

**🤖 For AI Agents - Critical Guidelines:**

**When starting/resuming work:**

1. **Read LOG.md FIRST** - Check "Current Progress" to see what was last done and what's next
2. **Then read [YOUR_SPEC].md** - Review relevant sections for context on the next task
3. **Check OPEN_ISSUES.md** - Review any active blockers (if file exists)

**Starting fresh?** If no files exist yet, proceed to Phase 1 to create them.

**After completing tasks/subtasks:** After finishing a task, subtask, or phase, **ALWAYS ask the user to review** unless they've explicitly stated they don't want reviews.

---

### Guideline Keywords

- **ALWAYS/NEVER** — Mandatory requirements/prohibitions (exceptions require explicit approval)
- **PREFER** — Strong recommendation (exceptions allowed with justification)
- **CAN** — Optional, developer's discretion
- **NOTE/EXAMPLE** — Context/illustration

Hierarchy: ALWAYS/NEVER > PREFER > CAN > NOTE/EXAMPLE

---

### CRITICAL: Document Permanence

⚠️ **[YOUR_SPEC].md** - **PERMANENT** - Choose name in Phase 1 Step 0 (FEATURE_SPECIFICATION.md, DOCUMENTATION_SPEC.md, API_DESIGN.md, TUTORIAL_PLAN.md, PROJECT_PLAN.md, SYSTEM_DESIGN.md, or custom)

⏳ **OPEN_ISSUES.md** + **LOG.md** - **TEMPORARY** - Deleted at project completion

**Critical rules:**

- [YOUR_SPEC].md is self-contained; NEVER reference OPEN_ISSUES.md or LOG.md from it
- NEVER reference temp docs in deliverables (code comments, docs, error messages, logs, published content)
- Only [YOUR_SPEC].md persists; keep it up-to-date as single source of truth

### Document Flow

```
┌──────────────────────┐
│   OPEN_ISSUES.md     │  ⏳ Temporary working document
│   (Active only)      │     Track blockers & investigations
└──────────┬───────────┘
           │ Investigation & resolution
           ↓
┌──────────────────────┐
│      LOG.md          │  ⏳ Temporary session log
│  (Progress + WHY)    │     Track what's done/next + decisions
└──────────┬───────────┘
           │ Final details incorporated
           ↓
┌──────────────────────┐
│ [YOUR_SPEC].md       │  ⚠️ PERMANENT living document
│ (Main specification  │     Single source of truth
│  - name you chose)   │     Must NEVER reference temp docs
└──────────────────────┘
```

**Flow**: Issues → LOG (progress + decisions) → [YOUR_SPEC].md (one-way flow, spec never references back)

---

### The Three Documents

#### [YOUR_SPEC].md - Main Specification

**Document name:** Choose in Phase 1 Step 0 (see [Document Permanence](#critical-document-permanence) for naming options)

**Purpose:** Comprehensive plan and specification - the permanent living document that will be kept long-term

**When to create:** At the start of your project, immediately after choosing its name (Phase 1, Step 0)

**When to update:** Throughout execution as tasks complete, requirements change, or new details emerge

**Typical sections:** Overview/objectives, scope, requirements, design decisions, implementation tasks (2-4 hour chunks), testing checklist, edge cases. Adapt to your context (code/docs/API/etc.)

**Key guidelines:**

- Keep up-to-date as single source of truth
- Include file references and specific acceptance criteria
- Be explicit about what's out of scope
- Update task descriptions with final implementation details

**Task example:**

```markdown
#### Task 1.1: Add Tracking Properties to Entity

**File**: `Connect/Connect.Api/Features/MyFeature/Entities/MyEntity.cs`

Add properties: `ActionNote` (string?, nullable, max 500 chars), `ActionByUserId` (string?, nullable)
Update `PerformAction()` method signature to accept these parameters
```

#### OPEN_ISSUES.md

**Purpose:** Track active blockers and investigations (temporary - deleted at completion)

**Create on demand** when first issue arises. **When resolved**, move to LOG.md and remove from here.

**Issue structure:**

- Status: 🔴 Blocked (waiting) | 🟡 Investigating (researching) | 🟢 Ready (needs decision/approval)
- Priority: High | Medium | Low
- Related Tasks, Problem Statement, Context, Options (pros/cons), Questions

**Key guidelines:**

- Keep succinct but complete; include all options with honest trade-offs
- Include status emoji and file references with line numbers
- Remove issue once resolved; document decision in LOG.md

**EXAMPLE - Active issue (succinct but complete):**

```markdown
### Issue #1: Data Tracking Strategy

**Status**: 🟡 Investigating | **Priority**: High | **Related**: Task 1.0, Task 1.1

**Problem**: Need tracking strategy for user actions on MyEntity.

**Context**: `MyEntity` doesn't implement `IAuditable` (`MyEntity.cs:9`)

**Options**:

1. **Add IAuditable** - Pros: Automatic, consistent; Cons: Redundant data
2. **Explicit ActionByUserId** - Pros: Clear intent, immutable; Cons: Manual

**Decision Needed**: Which aligns better with existing patterns?
```

#### LOG.md

**Purpose:** Session continuity + decision rationale (temporary - deleted at completion)

**Create on demand** when first decision made OR first task completed.

**Update:** After completing tasks, before ending sessions, when making decisions.

**Required sections (in order):**

1. **Current Progress** (MUST be first) - What was done, what's next
2. **Decision Log** - WHY decisions were made, with template
3. **Rejected Alternatives Summary** - Table of rejected options
4. **Guiding Principles** - Project principles
5. **References** - Links to materials

##### Current Progress Section

**Update after:** Completing numbered tasks/subtasks, before ending sessions (see Phase 0), after resolving blockers. NOT after every file edit.

**Structure:** Project Status (status, phase, progress) → Last Completed (task, what was done, files, status, notes) → Next Steps (immediate task, then what, blockers)

**Example:**

```markdown
## Current Progress

**Last Updated:** 2025-11-05 14:30

### 📍 Project Status

- **Status:** In Progress | **Current Phase:** Phase 3: Execution - Task 1.2 | **Overall Progress:** 3 of 12 tasks

### ✅ Last Completed

- **Task:** Task 1.1 - Add tracking properties
- **What was done:** Added ActionNote/ActionByUserId properties with nullability
- **Files:** `MyEntity.cs`, `MyEntityConfiguration.cs` | **Status:** Completed
- **Notes:** Made nullable after investigation (Decision #5)

### ⏭️ Next Steps

1. Task 1.2 - Update PerformAction() signature (~30 min)
2. Task 1.3 - Add validation (~20 min)
3. **Blockers:** None
```

##### Decision Log Section

**Structure:** Date | Category (Architecture/Data Model/UI/UX/etc.) | Status (✅ Implemented/🔄 Partial/📋 Planned) | Problem | Decision | Rationale | Alternatives | Impact

**Example:**

```markdown
### Decision #5: Make ActionByUserId Nullable

**Date**: 2025-11-05 | **Category**: Data Model | **Status**: ✅ Implemented

**Problem**: Not all entities undergo this action
**Decision**: Nullable at storage; required when calling PerformAction()
**Rationale**: Matches ActionAt pattern; semantically correct
**Alternatives**: Non-nullable - rejected (doesn't reflect reality)
**Impact**: Updated spec + `MyEntity.cs:23`, `MyEntityConfiguration.cs:74`
```

---

##### Complete LOG.md Example

```markdown
# LOG.md

## Current Progress

**Last Updated:** 2025-11-05 16:45

### 📍 Project Status

- **Status:** In Progress | **Phase:** Phase 3: Execution - Task 2.1 | **Progress:** 5 of 12 tasks

### ✅ Last Completed

- **Task:** Task 1.3 - Add validation | **Files:** `MyEntity.cs`, `MyEntityValidator.cs`, `MyEntityTests.cs`
- **Status:** Completed | **Notes:** Tests passing, ready for Task 2.1

### ⏭️ Next Steps

1. Task 2.1 - Create API endpoint (~45 min)
2. Task 2.2 - Add endpoint tests (~30 min)
3. **Blockers:** None

---

### Decision Log

#### Decision Template
```

### Decision #X: [Title]

**Date**: YYYY-MM-DD | **Category**: [type] | **Status**: [✅/🔄/📋]
**Problem**: [what] | **Decision**: [chosen] | **Rationale**: [why]
**Alternatives**: [rejected + why] | **Impact**: [changes]

```

### Planning Phase Decisions

#### Decision #1: Use Explicit Properties Over IAuditable
**Date**: 2025-11-04 | **Category**: Architecture | **Status**: ✅ Implemented
**Problem**: Need action tracking without redundant audit data
**Decision**: Explicit ActionByUserId/ActionNote properties vs IAuditable interface
**Rationale**: Clearer intent, avoids redundant fields, not all entities need full audit
**Alternatives**: IAuditable - rejected (redundant data) | **Impact**: Spec Task 1.1, MyEntity

#### Decision #5: Make ActionByUserId Nullable
**Date**: 2025-11-05 | **Category**: Data Model | **Status**: ✅ Implemented
**Problem**: Not all entities undergo action | **Decision**: Nullable at storage, required in PerformAction()
**Rationale**: Matches ActionAt pattern, semantically correct
**Alternatives**: Non-nullable - rejected (doesn't reflect reality)
**Impact**: Spec (lines 361,367,374,392), `MyEntity.cs:23`, `MyEntityConfiguration.cs:74`

---

## Rejected Alternatives Summary

| Alternative | For | Why Rejected | Decision # |
|------------|-----|--------------|------------|
| IAuditable interface | Action tracking | Redundant fields | #1 |
| Non-nullable ActionByUserId | Data model | Unrealistic | #5 |

---

## Guiding Principles
1. Explicit over implicit 2. Match existing patterns 3. Semantic correctness 4. Testability first

## References
- Spec: `FEATURE_SPECIFICATION.md` | Similar: ActionAt pattern | AGENTS.md: EF nullable guidelines
```

---

### Document Workflow

### Phase 0: Starting or Resuming Work

**This is where AI agents should ALWAYS begin.**

##### If files don't exist yet → You're starting fresh

Proceed directly to **Phase 1** to create your working documents.

##### If files already exist → You're resuming work

**Reading order:**

**1. LOG.md** → "Current Progress" section: Project Status, Last Completed, Next Steps, blockers

**2. OPEN_ISSUES.md** (if exists) → Active blockers (🔴), investigations (🟡), pending decisions (🟢)

**3. [YOUR_SPEC].md** → Section relevant to "Next Steps", task details, verification checklist, prerequisites

**4. Proceed to phase:** Phase 2 (investigation/blocked), Phase 3 (execution), or Phase 4 (review/completion)

**Session:** Continuous work period by one AI agent. Before ending: Update "Current Progress" in LOG.md.

---

#### Phase 1: Planning (Before Starting Work)

**Step 0: Choose [YOUR_SPEC].md Name**

Choose your permanent specification document name based on project type (see [Document Permanence](#critical-document-permanence) for options). This is the only document that persists.

1. **Create [YOUR_SPEC].md** (always required)

   - Use the name you chose in Step 0
   - Start with overview and objectives
   - Define scope, audience, and success criteria
   - Document guiding principles and constraints
   - Break down work into phases and tasks
   - Create verification/testing checklist
   - List explicitly what's out of scope
   - Make initial key decisions
   - Document current context (what exists already)
   - Suggest execution order
   - Estimate effort
   - **ALWAYS**: Ask user to review the plan unless they've explicitly opted out of reviews

2. **Create OPEN_ISSUES.md when first issue arises** (create on demand)

   - Add Issue Template at the top
   - Add your first issue using the template
   - **NOTE**: Only create this document when you encounter your first blocker or investigation need
   - **NOTE**: Resolved issues will be moved to LOG.md, not kept in this document

3. **Create LOG.md when first decision is made or first task is completed** (create on demand)
   - Add "Current Progress" section at the very top
   - Add Decision Template
   - Document your first decision with full rationale (if applicable)
   - Create Rejected Alternatives Summary table
   - List Design Principles Applied
   - Add References section
   - **NOTE**: Create this document when you make your first significant decision OR complete your first task

#### Phase 2: Investigation & Discovery

**Goal**: Document issue in OPEN_ISSUES → Investigate → Make decision → Record in LOG → Update [YOUR_SPEC].md → Remove issue from OPEN_ISSUES

**When you encounter blockers or need to make decisions:**

1. **Add to OPEN_ISSUES.md**

   - Create new issue using the template
   - Mark as 🔴 Blocked (cannot proceed) or 🟡 Investigating (actively researching)
   - Document problem statement and context
   - List options being considered
   - Note questions requiring answers

2. **Investigate and Research**

   - Search existing work for relevant patterns
   - Review existing implementations
   - Consider alternatives and trade-offs
   - Update the issue with findings
   - Mark as 🟢 Ready if decision requires team input or approval; otherwise proceed directly to step 3

3. **Make Decision**

   - Choose the best approach
   - Remove issue from OPEN_ISSUES.md
   - Prepare to document in LOG.md

4. **Record in LOG.md**

   - Create new decision entry in the Decision Log section
   - Document WHY the decision was made
   - Include the investigation from the issue
   - List alternatives considered and why rejected
   - Note impact on implementation
   - Add code/doc references
   - Reference the original issue number if helpful

5. **Update [YOUR_SPEC].md**
   - Modify affected tasks based on decision
   - Update implementation details with final approach chosen
   - Incorporate relevant context from the investigation
   - Adjust estimates if needed
   - **CRITICAL**: Keep spec self-contained (see [Document Permanence](#critical-document-permanence))
   - **ALWAYS**: Ask user to review decision and spec updates unless they've explicitly opted out of reviews

#### Phase 3: Execution

**As you work on each task:**

1. **Reference [YOUR_SPEC].md**

   - Follow the task breakdown
   - Check success criteria
   - Verify requirements and constraints
   - Follow suggested execution order

2. **Track Progress and Keep Spec Current**

   - Check off completed items in verification checklist
   - Update task descriptions if execution differs from plan
   - Update spec with actual details of what was done
   - **CRITICAL**: Update "Current Progress" in LOG.md after completing numbered tasks/subtasks, before ending sessions, or after resolving blockers
   - Update "Last Completed" and "Next Steps" sections
   - **CRITICAL**: Keep [YOUR_SPEC].md as the single source of truth
   - **ALWAYS**: Ask user to review completed work unless they've explicitly opted out of reviews

3. **Don't Reference Temporary Documents in Deliverables**

   - **NEVER** reference [YOUR_SPEC].md, OPEN_ISSUES.md, or LOG.md in final deliverables
   - **NEVER** add references like "See [YOUR_SPEC].md for details"
   - **For code**: No references in comments, XML docs, JSDoc, error messages, or logs
   - **For documentation**: No references in published content or final documents
   - **ALWAYS** make deliverables self-contained
   - **NOTE**: These temporary documents won't exist after project completion

4. **Handle New Issues**

   - Add to OPEN_ISSUES.md when blocked
   - Investigate using the template structure
   - Once resolved, remove from OPEN_ISSUES.md
   - Document resolution as a decision in LOG.md
   - Update "Current Progress" section with any blockers

5. **Document Execution Decisions**
   - Add to LOG.md's Decision Log section (Execution Phase)
   - Explain choices made during work
   - Document why certain approaches were taken
   - Note impact on final deliverable

#### Phase 4: Review & Completion

**Pre-completion checklist** (verify all items before finalizing):

- [ ] **[YOUR_SPEC].md is up-to-date**

  - All tasks marked complete
  - Verification checklist fully checked off
  - All success criteria met
  - Spec reflects actual execution (not original plan if it changed)
  - No references to OPEN_ISSUES.md or LOG.md

- [ ] **No deliverable references to temporary documents**

  - Searched deliverables for references to spec, OPEN_ISSUES, LOG
  - **For code**: No references in comments, documentation, error messages, logs
  - **For documentation**: No references in published content
  - **For any deliverable**: All content is self-contained

- [ ] **OPEN_ISSUES.md is empty or deleted**

  - No active issues remain (all resolved)
  - All resolved issues moved to LOG.md
  - Can be deleted if empty

- [ ] **LOG.md is complete** (will be deleted at completion, but should be complete for review)

  - "Project Status" shows status as "Complete" or "Ready for Review"
  - "Last Completed" reflects the final task
  - "Next Steps" indicates project completion or review
  - All decisions documented with rationale
  - Rejected Alternatives Summary is complete
  - All spec line number references are accurate

- [ ] **Requirements and edge cases verified**
  - All requirements from spec verified/tested
  - All edge cases addressed
  - Quality criteria met (appropriate to your context)

**After completing checklist:** **ALWAYS** ask user for final review of completed project before considering it done, unless they've explicitly opted out of reviews.

---

### Document Interconnections

**Information flow**: OPEN_ISSUES → LOG (progress + decisions) → [YOUR_SPEC].md (one-way only)

**Critical rule**: [YOUR_SPEC].md never references OPEN_ISSUES.md or LOG.md. It's self-contained and permanent. The other two are temporary scaffolding deleted at project completion.

**Reference rules**:

- **OPEN_ISSUES** can reference [YOUR_SPEC].md tasks and relevant files/content
- **LOG** can reference [YOUR_SPEC].md tasks, OPEN_ISSUES, and relevant files/content
- **[YOUR_SPEC].md** never references the other two (see [Document Permanence](#critical-document-permanence))

For visual flow diagram, see [Document Flow](#document-flow) above. For detailed examples, see "The Three Documents" section.

---

### Code Documentation Guidelines

- **NEVER** reference [YOUR_SPEC].md, OPEN_ISSUES.md, or LOG.md in code
- **NEVER** add comments like `// See [YOUR_SPEC].md for details`
- **NEVER** reference these documents in:
  - Code comments (inline, block, or doc comments)
  - XML documentation (C#) or JSDoc (TypeScript/JavaScript)
  - Error messages or exception messages
  - Log messages or debug output
  - README files or inline documentation
- **ALWAYS** write self-contained code documentation
- **NOTE**: These documents are deleted at project completion and won't exist in final deliverables

**EXAMPLE - Incorrect:**

```csharp
// See specification Task 1.1 for details on why this is nullable
public string? ActionByUserId { get; private set; }
```

**EXAMPLE - Correct:**

```csharp
// Nullable to allow entities that haven't undergone the action yet.
// Matches the pattern used by ActionAt property.
public string? ActionByUserId { get; private set; }
```

---

### Integration with AGENTS.md

If your project has an AGENTS.md file, check it for implementation best practices (coding patterns, git guidelines, review procedures, etc.).

**NOTE**: [YOUR_SPEC].md focuses on WHAT to build, AGENTS.md focuses on HOW to build it.

---

### File Locations

**ALWAYS** place these files in your project/work directory root:

```text
/
├── [YOUR_SPEC].md         ⚠️ PERMANENT (choose name based on project type:
│                             FEATURE_SPECIFICATION.md, DOCUMENTATION_SPEC.md,
│                             API_DESIGN.md, TUTORIAL_PLAN.md, PROJECT_PLAN.md, etc.)
├── OPEN_ISSUES.md         ⏳ Temporary (deleted after completion)
├── LOG.md                 ⏳ Temporary (session progress + decisions, deleted after completion)
├── AGENTS.md              (optional - project-wide guidelines)
└── CLAUDE.md              (optional - AI-specific instructions)
```

**See [Document Permanence](#critical-document-permanence) above for critical guidance on which documents persist.**

**For non-code projects**: Adapt the location to your context (e.g., documentation project root, content directory, design folder, etc.)

## Examples

Please see Instructions section.
