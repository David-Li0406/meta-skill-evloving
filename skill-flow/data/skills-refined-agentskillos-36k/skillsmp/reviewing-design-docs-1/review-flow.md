# Review Flow

Detailed walkthrough of the four-phase review process with example questions and decision points.

## Phase 1: Format Verification

### Initial Setup

1. **Read the full document** before creating tasks or asking questions
2. **Create the task list** for tracking review progress:

```
TaskCreate: subject="Verify design doc format", description="Check all expected sections are present", activeForm="Verifying format"
TaskCreate: subject="Review Summary section", description="Validate standalone clarity and completeness", activeForm="Reviewing Summary"
TaskCreate: subject="Review Background section", description="Validate context sufficiency for newcomers", activeForm="Reviewing Background"
TaskCreate: subject="Review Goals section", description="Validate SMART criteria", activeForm="Reviewing Goals"
TaskCreate: subject="Review Non-Goals section", description="Check for contradictions and missing exclusions", activeForm="Reviewing Non-Goals"
TaskCreate: subject="Review Plan section", description="Validate abstraction level and approach clarity", activeForm="Reviewing Plan"
TaskCreate: subject="Review Milestones section", description="Validate demo-ability and runnable artifacts", activeForm="Reviewing Milestones"
TaskCreate: subject="Review Measurable Impact section", description="Validate metrics map to goals", activeForm="Reviewing Measurable Impact"
TaskCreate: subject="Review Open Questions section", description="Categorize and assign questions", activeForm="Reviewing Open Questions"
TaskCreate: subject="Complete review handoff", description="Summarize and hand off to milestone planning", activeForm="Completing handoff"
```

3. **Check for expected sections** using the checklist in [section-checklist.md](section-checklist.md)

### Handling Missing Sections

When a section is missing or substantially different from expected:

**Example AskUserQuestion for missing section:**
```
Question: "The design doc is missing a 'Non-Goals' section. Non-Goals help prevent scope creep by explicitly excluding work readers might assume is included. How would you like to proceed?"

Options:
1. "Add Non-Goals section" - I'll help you draft explicit exclusions based on the Goals
2. "Proceed without" - Document the reason (e.g., "scope is narrowly defined in Goals")
```

**Example AskUserQuestion for deviant structure:**
```
Question: "The 'Technical Approach' section appears to combine what Lyft's template separates into 'Plan' and 'Milestones'. This can make it harder to track progress. How would you like to proceed?"

Options:
1. "Split into Plan + Milestones" - Separate the design approach from the delivery increments
2. "Keep combined" - Works if milestones are clearly marked within the section
3. "Rename to Plan, add Milestones" - Keep current content as Plan, add separate Milestones section
```

## Phase 2: Section-by-Section Review

Work through sections in order, updating task status as you go.

### Summary Section

**Mark task in_progress**, then check:
- Does it stand alone?
- Does it capture what, why, and outcome?
- Is it 2-4 sentences?

**Example issue and question:**

*Issue:* Summary starts with "This document describes the implementation of..."

```
Question: "The Summary starts with meta-language ('This document describes...') rather than describing the project itself. Summaries work better when they directly state what's being built. How would you like to revise?"

Options:
1. "Rewrite to lead with outcome" - e.g., "Users will be able to reset passwords via email link, reducing support tickets by 50%"
2. "Keep current phrasing" - The meta-framing works for this audience
```

### Goals Section

**Mark task in_progress**, then validate SMART criteria for each goal.

**Example issue and question:**

*Issue:* Goal states "Improve system performance"

```
Question: "The goal 'Improve system performance' isn't specific or measurable. SMART goals enable objective success evaluation. Which direction would you like to take?"

Options:
1. "Add specific metric" - e.g., "Reduce API p99 latency from 800ms to <200ms"
2. "Add specific capability" - e.g., "System handles 10x current load without degradation"
3. "Remove goal" - Performance isn't a primary objective for this project
4. "Move to Non-Goals" - Explicitly exclude performance work from scope
```

### Non-Goals Section

**Mark task in_progress**, then check for contradictions and missing exclusions.

**Example issue and question:**

*Issue:* Goal says "Support mobile users" but Non-Goal says "Native mobile app"

```
Question: "There's potential tension between the goal 'Support mobile users' and the non-goal 'Native mobile app'. This could confuse readers about mobile scope. How should we clarify?"

Options:
1. "Clarify Goal" - Change to "Support mobile users via responsive web"
2. "Clarify Non-Goal" - Change to "Native mobile app (mobile supported via responsive web)"
3. "Both" - Update both sections to be explicit about the mobile strategy
```

### Plan Section

**Mark task in_progress**, then validate abstraction level.

**Example issue and question:**

*Issue:* Plan includes Python code snippet showing class implementation

```
Question: "The Plan section includes a code snippet showing the PasswordResetService class implementation. Design docs work best at C4 Level 1-3 (System/Container/Component), with code-level detail deferred to milestone planning. How would you like to handle this?"

Options:
1. "Move to appendix" - Keep for reference but separate from main design
2. "Replace with component description" - Describe what PasswordResetService does, not how
3. "Remove entirely" - Defer to implementation planning phase
4. "Keep as-is" - The code example is essential for reviewer understanding
```

**Example issue and question:**

*Issue:* Plan has no diagrams for a multi-service system

```
Question: "The Plan describes interactions between 4 services but has no diagrams. A Container diagram would help reviewers understand the architecture quickly. Would you like to add one?"

Options:
1. "Add Container diagram" - I'll help draft a C4 Container diagram showing services and communication
2. "Add simpler box diagram" - Informal diagram showing key relationships
3. "Proceed without" - The text description is sufficient for this audience
```

### Milestones Section

**Mark task in_progress**, then validate demo-ability.

**Example issue and question:**

*Issue:* Milestone says "Set up database schema and migrations"

```
Question: "The milestone 'Set up database schema and migrations' is an implementation task rather than a demo-able increment. Milestones should end with something you can show to stakeholders. How would you like to revise?"

Options:
1. "Combine with next milestone" - Roll infrastructure into the first user-visible feature
2. "Reframe as foundation milestone" - "Backend infrastructure complete (internal demo: API returns test data)"
3. "Keep as-is" - Infrastructure setup is a meaningful checkpoint for this project
```

**Example issue and question:**

*Issue:* Milestone says "Users can manage their profiles" (vague)

```
Question: "The milestone 'Users can manage their profiles' is broad. What specific capabilities does 'manage' include? Breaking this down helps with estimation and demo planning."

Options:
1. "Split into specific milestones" - e.g., "Users can view profile", "Users can edit profile", "Users can upload avatar"
2. "Add detail to description" - Keep as one milestone but list specific capabilities included
3. "Keep vague" - Specific scope will be determined during implementation
```

### Measurable Impact Section

**Mark task in_progress**, then verify metrics map to goals.

**Example issue and question:**

*Issue:* Goal exists without corresponding metric

```
Question: "The goal 'Reduce customer support burden' has no corresponding metric in Measurable Impact. Without a metric, you can't verify success. What metric would indicate reduced support burden?"

Options:
1. "Add ticket reduction metric" - e.g., "Reduce password-related support tickets by 50%"
2. "Add time-to-resolution metric" - e.g., "Reduce average resolution time from 2 hours to 5 minutes"
3. "Goal is qualitative" - Remove from Goals or mark as secondary/non-measured objective
```

### Open Questions Section

**Mark task in_progress**, then categorize and assign.

**Example issue and question:**

*Issue:* Question has no owner or timeline

```
Question: "The open question 'How should we handle users with multiple email addresses?' has no owner or deadline. Unowned questions tend to stay unresolved. Who should own this decision?"

Options:
1. "Assign to author" - You'll decide before implementation starts
2. "Assign to specific person" - [Name/role] should decide this
3. "Mark as non-blocking" - Can be resolved during implementation
4. "Resolve now" - Let's decide this as part of the review
```

## Phase 3: Iterative Updates

After each AskUserQuestion response:

1. **Edit the document** to incorporate the agreed change
2. **Confirm the edit** - Show the user what changed
3. **Check for ripple effects** - Does this change affect other sections?
4. **Update task status** - Mark section complete if no more issues, otherwise continue

**Example ripple effect check:**

After updating a Goal:
> "I've updated the goal to 'Reduce API p99 latency from 800ms to <200ms'. Let me check if Measurable Impact needs a corresponding update... Yes, I'll add a metric for this goal."

## Phase 4: Handoff

When all section tasks are complete:

1. **Mark final task in_progress**
2. **Summarize the review:**
   - Sections reviewed
   - Changes made
   - Gaps accepted (with reasons)
   - Open questions status

3. **Present handoff instructions** (from SKILL.md Phase 4)

4. **Mark final task complete**

### Example Handoff Summary

> **Review Summary**
>
> Reviewed all 8 sections of `docs/design-plans/password-reset.md`.
>
> **Changes made:**
> - Summary: Rewritten to lead with outcome instead of meta-language
> - Goals: Made 2 goals SMART (added specific metrics)
> - Plan: Moved code snippet to appendix, added Container diagram
> - Milestones: Split "Profile management" into 3 specific milestones
> - Measurable Impact: Added metrics for 2 previously unmeasured goals
>
> **Accepted as-is:**
> - Non-Goals: User confirmed current list is sufficient
> - Open Questions: 2 blocking questions assigned, 1 deferred to implementation
>
> **Design review complete.**
>
> [... handoff instructions ...]
