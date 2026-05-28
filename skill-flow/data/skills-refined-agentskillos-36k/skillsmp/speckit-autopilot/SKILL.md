---
name: speckit-autopilot
description: Automatically orchestrates spec-kit commands when detecting changes in conversation. Triggers when user pivots tech stack ("switch to React", "use Go instead"), modifies requirements ("add feature", "remove"), updates architecture principles, or when implementation hits ambiguities. Keeps spec-kit artifacts (spec.md, plan.md, tasks.md, constitution.md) synchronized without manual command invocation.
---

# Spec-Kit Autopilot

Intelligent assistant for Spec-Driven Development that watches conversations and automatically invokes the right spec-kit commands to keep your project specifications synchronized.

## When to Activate

Trigger this skill when detecting:

- **Tech stack changes**: "switch to [tech]", "use [X] instead of [Y]", "migrate to [tech]", "let's try [tech]"
- **Requirement changes**: "add feature", "also include", "remove [feature]", "additionally", "change requirement"
- **Architecture decisions**: "we should always [X]", "add principle", "establish [rule]"
- **Clarification needs**: Agent says "unclear", "ambiguous", "not specified" during implementation
- **User frustration with manual updates**: User mentions needing to update multiple spec-kit files

**Stay silent** for general questions, brainstorming, or casual conversation. Only activate when user makes a **decision** or **change** affecting spec-kit artifacts.

## How It Works

I monitor conversation passively until a trigger pattern appears, then:

1. **Confirm** what's changing
2. **Clarify** missing details (minimal questions or use `/speckit.clarify`)
3. **Invoke** the appropriate spec-kit command with full context
4. **Confirm** what was updated

## Trigger → Command Mappings

### 🔄 Tech Stack Pivots

**Patterns**: "switch to", "use [X] instead", "change from [X] to [Y]", "migrate to", "let's try"

**Action**:
```
1. Invoke /speckit.clarify for tech stack choices
2. After answers, invoke /speckit.plan with context:

/speckit.plan [Change description]. [Clarifications].
Keep all other requirements unchanged unless explicitly mentioned.
```

**Example**:
```
User: "Let's use React with TypeScript instead of Blazor"

Me: "Detected tech stack pivot. Quick questions:"
/speckit.clarify What React build tool? (Vite/Next.js/CRA)
State management? (Redux/Zustand/Context)
Styling approach? (Tailwind/CSS Modules/Styled)

User: "Vite, Zustand, Tailwind"

Me: "✅ Updating architecture..."
/speckit.plan Rewrite frontend to use React + TypeScript with Vite
build tool, Zustand for state management, and Tailwind for styling
instead of Blazor. Keep all existing features: real-time updates,
drag-and-drop boards, multi-user support. Maintain same backend API.
```

---

### ➕ Requirement Modifications

**Patterns**: "add feature", "also include", "remove [feature]", "additionally", "change requirement"

**Action**:
```
1. Ask specifics if vague
2. Invoke /speckit.specify with details:

/speckit.specify [Addition/removal with specific details]
```

**Example**:
```
User: "Add PDF export for task boards"

Me: "For which views? Formatting preferences?"

User: "Task boards and project summaries, standard format"

Me: "✅ Adding to requirements..."
/speckit.specify Add PDF export feature:
- Exportable views: Task boards, project summaries
- Format: Standard PDF with current filters applied
- Trigger: Export button in view toolbar
```

---

### 📋 Architecture & Principles

**Patterns**: "we should always", "add principle", "architectural decision", "establish [rule]", "convention"

**Action**:
```
/speckit.constitution [New principle with rationale]
```

**Example**:
```
User: "We should use TypeScript strict mode everywhere"

Me: "✅ Adding principle..."
/speckit.constitution Add development principle:
Always use TypeScript strict mode for all code to ensure
type safety and catch errors at compile time. No exceptions.
```

---

### ❓ Implementation Clarifications

**Patterns**: Agent says "unclear", "ambiguous", "not specified", "how should I"

**Action**:
```
1. Identify incomplete artifact (spec/plan/constitution)
2. Ask user for clarification
3. Update relevant artifact
```

**Example**:
```
Agent: "Spec mentions 'real-time' but no latency requirement"

Me: "What's acceptable latency?"
Options: <100ms (very responsive), <500ms (smooth), <1s (acceptable)

User: "<500ms"

Me: "✅ Updating spec..."
/speckit.specify Add to real-time requirements:
- Maximum latency: 500ms from data change to UI update
- Update trigger: Immediate on every change
- Fallback: Show stale data with indicator if connection fails
```

---

### 🔧 Task Reorganization

**Patterns**: "break down differently", "change task order", "split this", "combine these"

**Action**:
```
/speckit.tasks [Reorganization instructions]
```

---

## Critical Rules

### Context Preservation

When invoking commands, ALWAYS include:
- What's changing
- What stays the same
- User's clarifications
- Reference to existing artifacts

**Good**:
```
/speckit.plan Use Go with Gin framework instead of Node.js.
Keep PostgreSQL, REST API, and all existing features.
```

**Bad**:
```
/speckit.plan Switch to Go
```

### Minimal Interruption

- Batch clarifications when possible
- Use `/speckit.clarify` for structured discovery
- Only interrupt for CRITICAL missing info
- Let flow continue for nice-to-haves

### Transparent Actions

Always announce what command is being invoked:

```
✅ Detected tech stack change. Invoking /speckit.plan...
```

```
✅ Adding principle to constitution...
```

### No Assumptions

If ambiguous or vague, ask first. Better to clarify than guess wrong.

## Determining Current Phase

Check filesystem to know which command to use:

```
.specify/memory/constitution.md exists → Constitution phase
.specify/specs/*/spec.md exists → Specify phase
.specify/specs/*/plan.md exists → Plan phase
.specify/specs/*/tasks.md exists → Tasks phase
Implementation in progress → Implement phase
```

This helps choose the right command:
- Early phases: Focus on `/speckit.constitution` and `/speckit.specify`
- Planning: Use `/speckit.plan`
- Implementation: May need any command depending on gap

## Complete Workflow Example

```
User: "Building a task manager like Trello"

[Normal spec-kit flow - stay silent]

User: "Actually, let's use Go instead of Node.js"

Me: 🎯 Detected tech stack pivot.

/speckit.clarify Questions about Go architecture:
- Framework: Gin, Echo, Chi, or Fiber?
- Keep PostgreSQL or different DB?
- Keep REST or try gRPC?
- Real-time approach: WebSockets, SSE, or polling?

User: "Gin, keep Postgres and REST, WebSockets"

Me: ✅ Updating architecture...

/speckit.plan Rewrite backend to use Go with Gin framework
instead of Node.js. Keep PostgreSQL database, REST API design,
and WebSocket-based real-time updates. Maintain all features:
task management, boards, user auth, notifications. Update
implementation details, research, and tasks for Go ecosystem.

---

User: "Add a principle about error handling"

Me: What should the principle cover? (Retry logic, user messages, logging?)

User: "Always use exponential backoff for retries, show user-friendly errors"

Me: ✅ Adding to constitution...

/speckit.constitution Add error handling principle:
- Retry transient failures with exponential backoff (3 attempts)
- Show user-friendly error messages (no stack traces to users)
- Log detailed errors server-side for debugging
- Graceful degradation when services unavailable

---

Agent: "The drag-and-drop spec doesn't specify touch device support"

Me: Should drag-and-drop work on touch devices? Mobile priority?

User: "Yes, mobile-first approach"

Me: ✅ Updating spec...

/speckit.specify Update drag-and-drop requirements:
- Must support both mouse and touch interactions
- Mobile-first approach: optimize for touch, enhance for mouse
- Touch gestures: press-hold to initiate drag, visual feedback
- Responsive: adapt board layout for small screens
```

## When NOT to Trigger

❌ Don't activate for:
- General questions about features
- Asking preferences before specs exist
- Normal conversation flow
- "Just thinking out loud"
- Brainstorming without decisions

✅ Only activate when user makes **concrete decisions** or **changes** that should update spec-kit artifacts.

## Tips for Effective Use

1. **Be proactive but not intrusive** - Detect changes but don't over-clarify obvious things
2. **Batch questions** - Ask 3-5 related questions at once rather than one-by-one
3. **Use `/speckit.clarify`** - Let spec-kit's built-in clarification system do the work
4. **Reference existing context** - Before asking, check what's already in spec.md/plan.md
5. **Confirm actions** - Always tell user what command was invoked and why
6. **Preserve intent** - When formatting commands, maintain user's original goals

## Integration with Spec-Kit Workflow

This skill complements spec-kit's standard workflow:

```
Constitution → Specify → Clarify → Plan → Tasks → Implement
     ↓           ↓          ↓        ↓       ↓        ↓
  [Autopilot watches at every phase and invokes commands when changes detected]
```

The autopilot doesn't replace manual invocation—users can still call commands directly. It just catches changes that would otherwise require manual artifact updates.
