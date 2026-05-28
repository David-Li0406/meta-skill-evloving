# Requirement Formats and Extraction Patterns

## User Story Format

### Standard Template

```
As a [actor/role]
I want [feature/capability]
So that [business benefit/value]
```

### Extraction Logic

```bash
# Detect "As a/an" → Actor
ACTOR=$(echo "$prompt" | grep -ioE "as an? [a-z ]+" | sed 's/as an? //')

# Detect "I want" → Feature
FEATURE=$(echo "$prompt" | grep -ioE "i want [^.]*" | sed 's/i want //')

# Detect "So that" → Benefit
BENEFIT=$(echo "$prompt" | grep -ioE "so that [^.]*" | sed 's/so that //')
```

### Example Output

**Input**: "As a developer I want JWT authentication so that users can securely log in"

```markdown
## User Story

**As a** developer
**I want** JWT authentication
**So that** users can securely log in

## Acceptance Criteria

- [ ] User can log in with email and password
- [ ] JWT access token is generated on successful login
- [ ] Refresh token is provided for token renewal
- [ ] Access token expires after 15 minutes
- [ ] Refresh token expires after 7 days
```

---

## Given/When/Then (BDD) Format

### Standard Template

```
Given [initial context/precondition]
When [action/event occurs]
Then [expected outcome/result]
```

### Extraction

```bash
# Extract Given/When/Then if present
if echo "$prompt" | grep -qiE "given|when|then"; then
  echo "$prompt" | grep -ioE "(given|when|then) [^.]*" >> requirements.md
fi
```

### Example

**Input**: "Given a user with a cart, when they checkout, then payment is processed"

```markdown
## Acceptance Criteria

**Given** a user with a cart
**When** they checkout
**Then** payment is processed and order is created

## Implied Tasks

1. Cart model and persistence
2. Checkout service
3. Payment processing integration
4. Order creation workflow
```

---

## Feature Request Parsing

### Action Verbs (Feature Type Detection)

| Verb | Feature Type | Example |
|------|--------------|---------|
| Implement/Build/Create | New Feature | "Implement user authentication" |
| Add/Include | Enhancement | "Add email notifications" |
| Fix/Debug | Bug Fix | "Fix login error" |
| Refactor/Cleanup | Refactoring | "Refactor payment service" |
| Optimize/Improve | Performance | "Optimize database queries" |

### Component Extraction

**Pattern**: "with X and Y"

```bash
COMPONENTS=$(echo "$prompt" | grep -ioE "with [a-z, and]+" | sed 's/with //' | tr ',' '\n')
```

**Example**: "Add JWT authentication with refresh tokens and email verification"
- Components: refresh tokens, email verification

### Technology Constraints

**Pattern**: "using Z"

```bash
TECH=$(echo "$prompt" | grep -ioE "using [a-z ]+" | sed 's/using //')
```

**Example**: "Build payment system using Stripe" → Technology: Stripe

### Target Audience

**Pattern**: "for A"

```bash
AUDIENCE=$(echo "$prompt" | grep -ioE "for [a-z ]+" | sed 's/for //')
```

---

## Intent Classification

### Level 1: Action Verb Detection

```bash
# Feature indicators
if echo "$prompt" | grep -qiE "add|implement|build|create"; then
  intent="feature"
fi

# Debug indicators
if echo "$prompt" | grep -qiE "fix|debug|troubleshoot|error"; then
  intent="debug"
fi

# Refactor indicators
if echo "$prompt" | grep -qiE "refactor|cleanup|optimize|restructure"; then
  intent="refactor"
fi
```

### Level 2: Context Analysis

```bash
# Rails-specific context
if echo "$prompt" | grep -qiE "model|controller|migration|activerecord"; then
  context="rails"
fi

# Technical domain
if echo "$prompt" | grep -qiE "jwt|oauth|api|rest"; then
  technical_context="authentication"
fi
```

### Level 3: Complexity Scoring

```bash
word_count=$(echo "$prompt" | wc -w)

if [ $word_count -gt 20 ]; then
  complexity="high"  # Complex feature request
elif [ $word_count -gt 10 ]; then
  complexity="medium"  # Standard feature
else
  complexity="low"  # Simple task
fi
```
