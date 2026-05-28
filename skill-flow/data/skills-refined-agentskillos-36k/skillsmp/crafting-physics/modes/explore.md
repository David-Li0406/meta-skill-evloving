# Explore Mode — Research & Understanding

Explore mode provides thorough research for understanding code, systems, and architecture.

<when_to_use>
## When Explore Activates

**Keyword Triggers:**
- "how does", "what is", "why does", "explain"
- "explore", "understand", "investigate" (without error context)
- Question format ("?")

**Context Triggers:**
- User asking about architecture
- Request to understand a system
- No specific component target
</when_to_use>

<mode_confirmation>
## Mode Confirmation

```
┌─ Mode: EXPLORE ───────────────────────────────────────────┐
│                                                           │
│  Detected: {keywords found}                               │
│                                                           │
│  I'll research thoroughly:                                │
│  1. Map the relevant code/systems                         │
│  2. Understand the architecture                           │
│  3. Document findings                                     │
│  4. Provide recommendations                               │
│                                                           │
│  [Proceed] [Switch to Debug] [Switch to Chisel]           │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
</mode_confirmation>

<workflow>
## Explore Workflow

### Step E1: Frame the Question

1. **Parse the exploration request:**
   - What is the user trying to understand?
   - What scope? (specific file, system, architecture)
   - What's the end goal?

2. **Show exploration plan:**
   ```
   ┌─ Explore Analysis ─────────────────────────────────────────┐
   │                                                            │
   │  Question: [what user wants to understand]                 │
   │  Scope: [what will be explored]                            │
   │                                                            │
   │  Exploration plan:                                         │
   │  1. [first area to explore]                                │
   │  2. [second area to explore]                               │
   │  3. [third area to explore]                                │
   │                                                            │
   │  Proceed? (y/n)                                            │
   │                                                            │
   └────────────────────────────────────────────────────────────┘
   ```

### Step E2: Research

1. **Map the territory:**
   - Read relevant files
   - Trace dependencies
   - Identify patterns and relationships

2. **Document as you go:**
   - Key files and their purposes
   - Important functions/classes
   - Data flows and relationships

3. **Check for escalation triggers:**
   - If exploration reveals missing infrastructure → Show Scope Check
   - If 2+ domain boundaries crossed → Suggest escalation to Hammer
   - If findings require architectural changes → Checkpoint and escalate

4. **Use Explore agent if needed:**
   - For large codebases, spawn Explore subagent
   - Aggregate findings

### Step E3: Synthesize and Report

1. **Present findings:**
   ```
   ┌─ Exploration Complete ─────────────────────────────────────┐
   │                                                            │
   │  Question: [original question]                             │
   │                                                            │
   │  Summary:                                                  │
   │  [concise answer to the question]                          │
   │                                                            │
   │  Key findings:                                             │
   │  • [finding 1 with file:line reference]                    │
   │  • [finding 2 with file:line reference]                    │
   │  • [finding 3 with file:line reference]                    │
   │                                                            │
   │  Architecture notes:                                       │
   │  [relevant architectural context]                          │
   │                                                            │
   │  Recommendations:                                          │
   │  [if applicable, suggestions for next steps]               │
   │                                                            │
   └────────────────────────────────────────────────────────────┘
   ```

2. **Log to taste.md:**
   ```markdown
   ## [YYYY-MM-DD HH:MM] | EXPLORE_COMPLETE
   Question: [what was explored]
   Summary: [key insight]
   Files reviewed: [count]
   ---
   ```
</workflow>

<escalation>
## Escalation Protocol

During exploration, watch for these signals:

| Signal | Threshold | Indicates |
|--------|-----------|-----------|
| **Domain boundaries** | 2+ systems involved | Integration work needed |
| **Missing infrastructure** | API/indexer needed | Full-stack work |
| **Architectural gaps** | Design issues found | Needs planning |
| **Exploration depth** | 3+ layers deep | Systemic complexity |

When escalation triggers hit:

```
┌─ Scope Check ──────────────────────────────────────────────────┐
│                                                                │
│  Exploration scope has grown:                                  │
│  • Files examined: [count]                                     │
│  • Systems involved: [list]                                    │
│  • Finding type: [discovery | gap | issue]                     │
│                                                                │
│  This may require Hammer mode to address properly.             │
│                                                                │
│  Options:                                                      │
│  1. Continue exploring (more context)                          │
│  2. Escalate to Hammer (plan architecture)                     │
│  3. Document findings and stop                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```
</escalation>

<codebase_discovery>
## Codebase Discovery Protocol

When exploring a new codebase:

### Phase 1: Package Analysis
```
Reading package.json...

Dependencies found:
  ✓ framer-motion (animation)
  ✓ @tanstack/react-query (data fetching)
  ✓ tailwindcss (styling)
```

### Phase 2: Pattern Discovery
```
Scanning existing components...

Gold components (high import count):
  • Button.tsx (23 imports)
  • Modal.tsx (18 imports)

Component structure pattern:
  └─ imports
  └─ type definitions
  └─ hooks
  └─ handlers
  └─ render
```

### Phase 3: Physics Baseline
```
Analyzing existing physics...

Financial components:
  • ClaimButton.tsx - 800ms, pessimistic ✓

Standard components:
  • LikeButton.tsx - 200ms, optimistic ✓
```

### Context Caching

Cache results to `grimoires/sigil/context/codebase-discovery.yaml`:

```yaml
discovered_at: "2026-01-20T14:30:00Z"
expires_at: "2026-01-21T14:30:00Z"

libraries:
  animation: framer-motion
  data_fetching: "@tanstack/react-query"
  styling: tailwindcss

conventions:
  import_style: named
  export_style: default

gold_components:
  - path: src/components/Button.tsx
    imports: 23
```
</codebase_discovery>

<examples>
## Examples

### Example: Understanding Architecture

```
User: /craft "how does the auth flow work in this app?"

[Mode Detection: EXPLORE]

┌─ Explore Analysis ─────────────────────────────────────────┐
│                                                            │
│  Question: How does the auth flow work?                    │
│  Scope: Authentication system                              │
│                                                            │
│  Exploration plan:                                         │
│  1. Find auth-related files and entry points               │
│  2. Trace login/logout flow                                │
│  3. Identify session management approach                   │
│                                                            │
│  Proceed? (y/n)                                            │
│                                                            │
└────────────────────────────────────────────────────────────┘

User: y

[Spawning Explore agent...]
[Mapping auth system...]

┌─ Exploration Complete ─────────────────────────────────────┐
│                                                            │
│  Question: How does the auth flow work?                    │
│                                                            │
│  Summary:                                                  │
│  The app uses NextAuth.js with JWT tokens stored in        │
│  httpOnly cookies. Sessions are validated server-side.     │
│                                                            │
│  Key findings:                                             │
│  • src/lib/auth.ts:12 — NextAuth configuration             │
│  • src/middleware.ts:8 — Route protection logic            │
│  • src/hooks/useAuth.ts:3 — Client-side auth hook          │
│                                                            │
│  Architecture notes:                                       │
│  JWT + server validation provides good security.           │
│  Protected routes defined in middleware matcher.           │
│                                                            │
│  Recommendations:                                          │
│  Consider adding refresh token rotation for long sessions. │
│                                                            │
└────────────────────────────────────────────────────────────┘

[Logs EXPLORE_COMPLETE to taste.md]
```

### Example: First-Time Codebase

```
User: /craft "claim button" (first craft in new codebase)

[EXPLORE mode triggered: no existing discovery cache]

┌─ EXPLORE MODE ─────────────────────────────────────────┐
│  Codebase discovery active                             │
│                                                        │
│  Scanning for conventions...                           │
└────────────────────────────────────────────────────────┘

[Package analysis...]
[Pattern discovery...]
[Physics baseline...]

┌─ Codebase Discovery Report ────────────────────────────┐
│                                                        │
│  Libraries:                                            │
│  • Animation: framer-motion                            │
│  • Data: @tanstack/react-query                         │
│  • Styling: tailwindcss                                │
│                                                        │
│  Conventions:                                          │
│  • Import: named, no barrels                           │
│  • Export: default                                     │
│  • Props: Interface + Props suffix                     │
│                                                        │
│  Saved to: grimoires/sigil/context/codebase-discovery  │
│                                                        │
│  Now proceeding with craft...                          │
│                                                        │
└────────────────────────────────────────────────────────┘

[Switches to Chisel mode for the actual craft]
```
</examples>
