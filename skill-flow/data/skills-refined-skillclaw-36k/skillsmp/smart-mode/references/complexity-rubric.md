# Complexity Scoring Rubric

Detailed criteria for scoring task complexity 1-5 and selecting execution mode.

## Scoring Matrix

| Score | Files | LOC | Scope | Mode |
|-------|-------|-----|-------|------|
| **1** | 1 | <50 | Trivial fix | DIRECT |
| **2** | 2-3 | <200 | Single feature | DIRECT |
| **3** | 4-7 | <500 | Multi-component | ORCHESTRATED |
| **4** | 8-15 | <1500 | Architecture change | ORCHESTRATED |
| **5** | 15+ | 1500+ | Full application | ORCHESTRATED |

## Score 1: Trivial

**Characteristics:**
- Single file modification
- Less than 50 lines of code
- Obvious, mechanical change
- No design decisions

**Examples:**
- Fix a typo in README
- Update a version number
- Add a missing import
- Rename a variable
- Fix a simple syntax error

**Heuristics:**
- Keywords: "fix", "typo", "rename", "update version"
- No component/feature names mentioned
- Single file path mentioned or implied

## Score 2: Simple Feature

**Characteristics:**
- 2-3 files affected
- Less than 200 lines of code
- Clear, single-purpose change
- Minimal design decisions

**Examples:**
- Add a button component
- Create a simple API endpoint
- Add form validation
- Implement a utility function
- Add a simple test

**Heuristics:**
- Single feature/component mentioned
- Keywords: "add", "create", "simple"
- No mentions of "system", "complete", "full"

## Score 3: Multi-Component

**Characteristics:**
- 4-7 files affected
- 200-500 lines of code
- Multiple related components
- Some design decisions required

**Examples:**
- Auth system (login + register)
- CRUD for a resource
- Form with validation + API
- Feature with frontend + backend
- Component library addition

**Heuristics:**
- Multiple related features mentioned
- Keywords: "system", "with", combining features
- Mentions database OR authentication
- Requires both UI and logic

## Score 4: Architectural

**Characteristics:**
- 8-15 files affected
- 500-1500 lines of code
- Significant structural changes
- Multiple design decisions
- Cross-cutting concerns

**Examples:**
- Complete auth with password reset + email
- New module/domain addition
- API redesign
- State management overhaul
- Database schema changes with migrations

**Heuristics:**
- Keywords: "complete", "full", "redesign", "overhaul"
- Mentions multiple systems (auth + email + db)
- Architectural terms used
- Migration or schema changes implied

## Score 5: Full Application

**Characteristics:**
- 15+ files affected
- 1500+ lines of code
- New application or major feature set
- Many design decisions
- Multi-phase implementation required

**Examples:**
- Build complete SaaS
- Create entire dashboard
- Full e-commerce checkout
- Complete CMS implementation
- Multi-tenant architecture

**Heuristics:**
- Keywords: "build", "create", "entire", "complete application"
- Multiple major features combined
- Would take a human developer days/weeks
- Requires infrastructure setup

## Heuristic Signals

### Positive Signals (increase score)

| Signal | Score Modifier |
|--------|---------------|
| "full" or "complete" | +1 |
| "entire" or "whole" | +1 |
| "system" | +1 |
| Multiple features (comma-separated) | +1 per feature |
| "database" or "schema" | +1 |
| "authentication" or "auth" | +1 |
| "payment" or "billing" | +1 |
| "email" or "notification" | +0.5 |
| "dashboard" | +1 |
| "admin" | +0.5 |

### Negative Signals (decrease score)

| Signal | Score Modifier |
|--------|---------------|
| "simple" or "quick" | -1 |
| "just" or "only" | -1 |
| "small" or "minor" | -1 |
| "fix" or "typo" | -1 |
| "rename" | -1 |
| Single file path mentioned | -1 |
| "button" or "component" (single) | -0.5 |

## Calculation Algorithm

```
base_score = 2  # Default assumption

# Add positive signals
for signal in positive_signals:
    if signal in prompt:
        base_score += signal.modifier

# Subtract negative signals
for signal in negative_signals:
    if signal in prompt:
        base_score += signal.modifier  # (negative values)

# Clamp to 1-5
final_score = max(1, min(5, round(base_score)))

# Determine mode
mode = "DIRECT" if final_score <= 2 else "ORCHESTRATED"
```

## Examples with Scoring

### Example 1: Score 1
```
Prompt: "fix the typo in README.md - 'recieve' should be 'receive'"

Signals:
- "fix" → -1
- "typo" → -1
- Single file → -1

Calculation: 2 + (-1) + (-1) + (-1) = -1 → clamped to 1
Mode: DIRECT
```

### Example 2: Score 2
```
Prompt: "add a logout button to the header"

Signals:
- "button" (single) → -0.5
- Simple component implied

Calculation: 2 + (-0.5) = 1.5 → rounded to 2
Mode: DIRECT
```

### Example 3: Score 3
```
Prompt: "implement user login with form validation"

Signals:
- "authentication" implied → +1
- Form + validation = 2 things → +0.5

Calculation: 2 + 1 + 0.5 = 3.5 → rounded to 4, but...
Adjustment: Single auth feature, not full system → 3
Mode: ORCHESTRATED
```

### Example 4: Score 4
```
Prompt: "build complete authentication with login, register, and password reset"

Signals:
- "complete" → +1
- "authentication" → +1
- Multiple features (3) → +1.5

Calculation: 2 + 1 + 1 + 1.5 = 5.5 → clamped to 5, but...
Adjustment: Auth only, not full app → 4
Mode: ORCHESTRATED
```

### Example 5: Score 5
```
Prompt: "create a full dashboard with user management, analytics, settings, and billing"

Signals:
- "full" → +1
- "dashboard" → +1
- Multiple features (4) → +2
- "billing" → +1

Calculation: 2 + 1 + 1 + 2 + 1 = 7 → clamped to 5
Mode: ORCHESTRATED
```

## LLM Self-Assessment Override

After heuristic calculation, LLM should self-assess:

1. Does the calculated score feel right?
2. Are there nuances the heuristics missed?
3. Is the project context relevant (e.g., small project = lower scores)?

If LLM assessment differs by more than 1 from heuristic:
- Use LLM assessment
- Document reasoning in state.yaml
