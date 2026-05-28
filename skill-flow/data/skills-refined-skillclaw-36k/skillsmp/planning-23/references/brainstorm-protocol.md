# Brainstorm Protocol (Interactive Mode)

## Core Principle

Turn ambiguous ideas into clear, validated designs through dialogue.

## The Flow

```
For each batch of related decision points (max 4 per call):
  1. Present brief context (what you found)
  2. Ask questions with options (batch related)
  3. Wait for response
  4. Record decisions
  5. Move to next batch
```

---

## Question Rules

| Rule | Description |
|------|-------------|
| **Batch related** | Group related questions (max 4 per AskUserQuestion call) |
| **Multiple choice** | Prefer options over open-ended when possible |
| **Recommend** | Add "(Recommended)" to your suggested option |
| **Max 4 options per question** | Keep choices manageable for each question |
| **Lead with why** | Briefly explain why you're asking |

---

## Question Template

```python
# Before asking, provide brief context
"""
Based on exploration, the project uses Next.js App Router
and has no existing auth implementation.
"""

AskUserQuestion(questions=[{
  "question": "Which authentication method should we implement?",
  "header": "Auth",  # Short label (max 12 chars)
  "options": [
    {"label": "OAuth + Email (Recommended)", "description": "Most flexible, supports both"},
    {"label": "OAuth only", "description": "Simpler, relies on social providers"},
    {"label": "Email only", "description": "Traditional, no third-party deps"}
  ],
  "multiSelect": False
}])
```

---

## Question Priority Order

Ask in this order (skip if already clear):

1. **Purpose/Goal** - What problem does this solve? Core objective?
2. **Scope** - MVP / Full / Prototype?
3. **Constraints** - Performance, security, compatibility requirements?
4. **Architecture** - Follow existing patterns / New patterns / Hybrid?
5. **Libraries** - Which packages to use?

---

## Exploring Approaches (Critical)

**Before settling on a design, ALWAYS propose 2-3 approaches:**

```markdown
## Approach Options

### Option A: NextAuth.js (Recommended)
- **Pros**: Next.js standard, built-in OAuth, active community
- **Cons**: Limited customization, learning curve
- **Best for**: Quick implementation, standard auth flows

### Option B: Passport.js
- **Pros**: Flexible strategy pattern, many providers
- **Cons**: Complex setup, separate Next.js integration needed
- **Best for**: Complex custom requirements

### Option C: Custom Implementation
- **Pros**: Full control, minimal dependencies
- **Cons**: Security risks, development time
- **Best for**: Very specialized requirements

**Recommendation**: Option A - Project is Next.js based, standard auth flow is sufficient
```

Then ask:
```python
AskUserQuestion(questions=[{
  "question": "Which approach should we use?",
  "header": "Approach",
  "options": [
    {"label": "Option A (Recommended)", "description": "NextAuth.js - fast, standard"},
    {"label": "Option B", "description": "Passport.js - flexible customization"},
    {"label": "Option C", "description": "Custom - full control"}
  ],
  "multiSelect": False
}])
```

---

## Red Flags (Ask More Questions)

Stop and ask if you notice:

| Signal | Example | Action |
|--------|---------|--------|
| Vague scope | "Add login feature" | Ask about OAuth/email/both |
| Multiple approaches | REST vs GraphQL | Ask preference |
| Missing constraints | No perf requirements | Ask about scale |
| Ambiguous terms | "quickly", "simple" | Clarify meaning |

---

## Incremental Design Presentation

After decisions are made, present design in small sections:

```
Section 1: Overview (200-300 words)
  → Ask: "Does the overview look correct?"

Section 2: Architecture (200-300 words)
  → Ask: "Is the architecture appropriate?"

Section 3: Scope (200-300 words)
  → Ask: "Is the scope correct?"
```

**After each section:**
```python
AskUserQuestion(questions=[{
  "question": "Does this section look correct?",
  "header": "Review",
  "options": [
    {"label": "Yes, continue", "description": "Move to next section"},
    {"label": "Needs changes", "description": "I have feedback"}
  ],
  "multiSelect": False
}])
```

If "Needs changes" → get feedback, adjust, re-present that section.

---

## Auto Mode (Planner Agent)

Make decisions automatically (no user interaction available):

```
For each decision:
  1. Analyze context for signals
  2. Choose based on:
     - Existing patterns in codebase
     - Dependencies already present
     - Common best practices
  3. Record choice with rationale
  4. Mark asked_user: false
```

**Auto Decision Heuristics:**
- If existing pattern exists → follow it
- If dependency present → use it
- If multiple valid options → choose most common/standard
- When unsure → prefer simpler, reversible choices
