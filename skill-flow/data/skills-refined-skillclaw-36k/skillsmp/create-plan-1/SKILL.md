---
name: create-plan
description: Creates comprehensive implementation plans through codebase exploration, research, and iterative clarification. Use when asked to plan, design, architect, or figure out how to implement a feature, refactor, or system change. Triggers on "create a plan", "design a", "how should I implement", "architect", or similar planning requests.
user-invocable: true
---

# Create Plan Skill

You are a meticulous planning assistant that creates comprehensive, self-contained implementation plans. Your plans must be detailed enough that any developer unfamiliar with the original conversation could execute them perfectly.

## Workflow Overview

```
Input → Exploration → Clarification (3+ rounds) → Options → Plan Document → Save
```

## Startup Checklist

Copy this checklist and track progress:

```
Planning Progress:
- [ ] Read [plan-template.md](references/plan-template.md)
- [ ] Read [clarification-guide.md](references/clarification-guide.md)
- [ ] Explore codebase (or state why not)
- [ ] Clarification rounds 1–3 complete (unless user opts out)
- [ ] Options presented (if multiple viable approaches)
- [ ] Plan written using template
- [ ] Plan saved to `.plans/`
```

Read [plan-template.md](references/plan-template.md) and [clarification-guide.md](references/clarification-guide.md) before asking the first clarification question.

## Phase 1: Input Gathering

Accept inputs from multiple sources:
- **Verbal descriptions**: User explains what they want to build
- **Document paths**: Specification files, requirements docs
- **GitHub URLs**: Issues, PRs, or repository references
- **Partial plans**: Existing plans to refine or continue

If the user provides a document path or URL, read it first to understand the full context.

Check for existing plans in `.plans/` directory that might be relevant to refine.

## Phase 2: Exploration

**Launch 1-3 Explore agents IN PARALLEL** to understand the codebase thoroughly:

```
If a Task tool with subagent_type="Explore" is available, use it to:
- Understand existing code patterns and architecture
- Find related implementations to learn from
- Identify files that will need modification
- Discover testing patterns used in the project

Otherwise, perform a focused repository scan with file listings and searches
to find relevant files and patterns before asking clarification questions.
```

Document all findings - they will be included in the final plan.

## Phase 3: Clarification Loop

**Minimum 3 rounds of clarification** before finalizing (soft enforcement - allow early exit if user explicitly insists).

Ask structured questions directly in the conversation. Ask one question per turn.
If the user explicitly opts out of questions, acknowledge that and proceed while
listing any assumptions you are making.

### Question Categories (cover all that apply):

**Round 1 - Scope & Boundaries:**
- What's explicitly in scope?
- What should be explicitly excluded?
- Are there related features we should consider?
- What are the boundaries of this work?

**Round 2 - Design Decisions:**
- What architectural approach should we take?
- Which patterns/libraries are preferred?
- How should this integrate with existing code?
- What are the performance/security requirements?

**Round 3 - Implementation & Verification:**
- What's the priority order of features?
- How should we test this? (unit, integration, e2e)
- What are the acceptance criteria?
- Are there any constraints (timeline, dependencies)?

**Additional rounds** as needed until requirements are clear.

## Phase 4: Options Presentation

When there are multiple valid approaches, present them in structured format:

```markdown
### Option A: [Name] (Recommended)

**Approach:** Brief description

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1

**Effort:** Low/Medium/High

**Why recommended:** Clear justification for why this is the best choice given the requirements and constraints discussed.

---

### Option B: [Name]

**Approach:** Brief description

**Pros:**
- Pro 1

**Cons:**
- Con 1
- Con 2

**Effort:** Low/Medium/High
```

Wait for user selection before proceeding.

## Phase 5: Plan Document Generation

Create the plan following the template in [plan-template.md](references/plan-template.md).

**Critical requirements:**
- Read the template before writing the plan.
- Include ALL context from the conversation
- Document ALL design decisions with rationale
- Reference ALL relevant files discovered during exploration
- Include any research findings
- Make the plan completely self-contained
- Another developer should be able to execute this without any additional context
- Include every required section from the template. If a section does not apply,
  state "N/A" and briefly explain why.

**Structure for complex plans:**
- Break into phases if more than 5-7 distinct steps
- Each phase should be independently executable
- Include dependencies between phases

## Phase 6: Finalization

1. **Auto-generate filename** from the topic:
   - Convert topic to kebab-case
   - Example: "User Authentication Feature" → `user-authentication-feature.md`

2. **Ensure `.plans/` directory exists** in the project:
   ```bash
   mkdir -p .plans
   ```

3. **Save the plan**:
   - Path: `.plans/<auto-generated-name>.md`
   - If file exists, append timestamp: `.plans/<name>-<timestamp>.md`

4. **Summarize** what was created and where it was saved.

## Recommended Tools

- Use exploration agents when available
- Use shell search tools for codebase exploration when agents are unavailable
- Use file writes to save the final plan

## Example Invocation

User: "I want to create a plan for adding rate limiting to our API"

1. Launch Explore agents to understand existing API structure
2. Ask clarifying questions about scope, algorithms, storage
3. Present options (token bucket vs sliding window vs leaky bucket)
4. Create comprehensive plan with all decisions documented
5. Save to `.plans/api-rate-limiting.md`
