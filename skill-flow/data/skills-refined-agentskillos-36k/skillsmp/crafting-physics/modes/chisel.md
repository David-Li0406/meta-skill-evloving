# Chisel Mode — Single Component Physics

Default mode for single-component generation, refinement, and polish.

<when_to_use>
## When Chisel Activates

Chisel is the default when:
- Single component creation or modification
- No multi-file scope keywords detected
- No debug/explore signals present
- No existing Hammer session in progress
</when_to_use>

<workflow>
## Chisel Workflow

### Step 1: Discover Context

**1a. Read project context** (if exists):
```
Scan grimoires/sigil/context/
```
Look for:
- **Personas** (`context/personas/`) — User expertise, behavior, expectations
- **Brand** (`context/brand/`) — Voice, tone, visual guidelines
- **Domain** (`context/domain/`) — Best practices, domain-specific rules

**1b. Read taste log** (if exists):
```
Read grimoires/sigil/taste.md
```
Look for:
- Patterns with 3+ occurrences (apply automatically)
- `output_mode` preference (compact vs verbose)
- Timing/animation/material overrides

**1c. Discover codebase conventions** (single read):
```
Read package.json
```
Extract from dependencies:
- Animation: `framer-motion` | `react-spring` | CSS
- Data: `@tanstack/react-query` | `swr` | `fetch`
- Toast: `sonner` | `react-hot-toast` | native
- Styling: `tailwindcss` | `styled-components` | `@emotion`

**1d. Extract design patterns** (for Generate craft type):
Read ONE existing similar component to extract:
- Color tokens (`bg-muted`, not `bg-black`)
- Spacing tokens (`p-4`, `gap-2`)
- Border radius patterns
- State class patterns (hover, focus, disabled)

### Step 2: Detect Craft Type and Effect

**Craft Type Detection:**

| Input Signals | Craft Type | Output |
|---------------|------------|--------|
| Component name, no existing file | Generate | New file |
| "refine", "polish", existing file | Refine | Edit existing |
| "theme", "mode", config ref | Configure | Edit config |
| "loading", "data flow", "hook" | Pattern | Create hook/utility |
| Multi-file edits | Polish | Batch edits |

**Effect Detection:**

{{fragment:detection}}

### Step 3: Show Physics Analysis

```
┌─ Craft Analysis ───────────────────────────────────────┐
│  Target:       {component} ({new/existing})            │
│  Craft Type:   {generate/refine/configure/pattern}     │
│  Effect:       {detected effect}                       │
│  Iteration:    {n} ({new session/continuing})          │
│                                                        │
│  Behavioral    {sync} | {timing} | {confirmation}      │
│  Animation     {easing} | {timing} | {spring if used}  │
│  Material      {surface} | {shadow} | {radius}         │
│                                                        │
│  Output:       {target file path}                      │
│  Protected:    [✓] All capabilities included          │
└────────────────────────────────────────────────────────┘
```

**Quick Reference:**

{{fragment:physics-table}}

### Step 4: Get Confirmation

Wait for user response:
- **"yes", "y", "proceed"** → Apply immediately (Step 5)
- **Correction provided** → Update analysis, show again
- **Question asked** → Answer, then re-confirm

### Step 5: Apply Changes

IMMEDIATELY apply changes based on craft type:

**Generate:** Write complete new file with all three physics layers.

**Refine:** Use Edit tool to modify existing code, preserving what works.

**Configure:** Edit config file with physics-informed values.

**Pattern:** Write hook or utility with appropriate physics baked in.

**For all craft types:**
- Use discovered libraries only (never assume)
- Match existing code style exactly
- Apply physics from analysis
- Include protected capabilities where applicable

{{fragment:protected-caps}}

### Step 5.5: Validation Gate

When effect is Financial, Destructive, or SoftDelete:
- Run Anchor + Lens validation if CLIs available
- Run subagent validators if enabled in constitution.yaml
- Handle corrections and violations appropriately

### Step 6: Collect Feedback

{{fragment:feedback-loop}}

### Step 7: Log Taste Signal

Append to `grimoires/sigil/taste.md`:

**ACCEPT:**
```markdown
## [YYYY-MM-DD HH:MM] | ACCEPT
Target: [what was crafted]
Craft Type: [generate/refine/configure/pattern/polish]
Effect: [if applicable]
Physics: [key values applied]
---
```

**MODIFY:**
```markdown
## [YYYY-MM-DD HH:MM] | MODIFY
Target: [what was crafted]
Craft Type: [type]
Changed: [what user indicated was off]
Learning: [infer preference for future]
---
```

**REJECT:**
```markdown
## [YYYY-MM-DD HH:MM] | REJECT
Target: [what was crafted]
Craft Type: [type]
Reason: [user feedback]
---
```
</workflow>

<error_recovery>
## Error Recovery

**Craft type unclear:**
1. Ask ONE question: "Is this new, or refining something that exists?"
2. If still unclear: Infer from context (file reference = refine)

**Effect detection fails:**
1. Ask max 2 clarifying questions
2. If still unclear: Default to Standard, note: "⚠ Defaulted to Standard"

**Missing package.json:**
1. Check imports in existing files
2. Infer libraries from import statements
3. If no files exist: Ask user for preferences

**Protected capability violation:**
1. Stop generation
2. Explain which capability would be violated
3. Offer compliant alternative
</error_recovery>

<examples>
## Examples

### Example 1: New Component (Generate)

```
User: /craft "claim button for staking rewards"

┌─ Craft Analysis ───────────────────────────────────────┐
│  Target:       StakingClaimButton (new)                │
│  Craft Type:   Generate                                │
│  Effect:       Financial mutation                      │
│                                                        │
│  Behavioral    Pessimistic | 800ms | Confirmation      │
│  Animation     ease-out | 800ms | Non-interruptible   │
│  Material      Elevated | Soft shadow | 8px radius     │
│                                                        │
│  Output:       src/components/StakingClaimButton.tsx   │
│  Protected:    [✓] All capabilities included          │
└────────────────────────────────────────────────────────┘

Proceed? (y/n)

User: y

[Generates complete component]

Does this feel right? Think about your user in the moment of clicking.

User: feels a bit slow, our users claim multiple times a day

Adjusting to 600ms — still deliberate but respects high-frequency workflow.

[Applies adjustment, logs MODIFY with learning]
```

### Example 2: Theme Refinement (Configure)

```
User: /craft "improve light mode readability"

┌─ Craft Analysis ───────────────────────────────────────┐
│  Target:       Theme configuration                     │
│  Craft Type:   Configure                               │
│  Issue:        Lines hard to read in light mode        │
│                                                        │
│  Material      Readability focus                       │
│  Changes:      - Border colors: increase contrast      │
│                - Text secondary: darken for legibility │
│                                                        │
│  Output:       Edit vocs.config.ts                     │
└────────────────────────────────────────────────────────┘

Proceed? (y/n)

User: y

[Edits config with improved contrast values]
```

### Example 3: Compact Mode

After 5+ consecutive ACCEPT signals:

```
User: /craft "make the submit button snappier"

SubmitButton | Standard | Refine
Animation: 200ms → 150ms, spring(600,30) | Material: unchanged

Apply? (y/n)

User: y

[Applies change]
```
</examples>
