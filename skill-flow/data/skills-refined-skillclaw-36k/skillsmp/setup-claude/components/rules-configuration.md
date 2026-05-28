# Rules Configuration Component

This component guides the setup of modular rules for consistent Claude behavior.

## Concept: Rules vs CLAUDE.md

| Aspect | Rules (.claude/rules/) | CLAUDE.md |
|--------|------------------------|-----------|
| Purpose | Behavioral constraints | Project context |
| Loading | Always active | Read when relevant |
| Content | "Always do X" / "Never do Y" | "Here's how things work" |
| Format | Individual .md files | Single file |
| Scope | Specific concerns | General overview |

## Why Modular Rules?

1. **Focused**: Each rule file addresses one concern
2. **Reusable**: Copy rules between projects
3. **Maintainable**: Edit one concern without touching others
4. **Composable**: Enable/disable rules per project

## Available Rule Templates

| Rule | Purpose | Key Constraints |
|------|---------|-----------------|
| security.md | Security best practices | No secrets, validate inputs |
| coding-style.md | Code organization | Naming, file structure |
| testing.md | Test requirements | TDD, coverage |
| git-workflow.md | Git conventions | Commit format, branches |

## Setup Flow

### Step 1: Explain Rules

Present to user:
```
Rules are always-active behavioral constraints stored in .claude/rules/
Unlike CLAUDE.md (which provides context), rules are strict guidelines
that Claude will follow throughout the conversation.

Example rules:
- "Never hardcode secrets"
- "Always use async/await instead of .then()"
- "Run tests after each edit"
```

### Step 2: Interview User

```
AskUserQuestion: "Set up modular rules?"
(Multi-select)

├── security.md - Security best practices
│   - No hardcoded secrets or API keys
│   - Validate all inputs
│   - Escape outputs appropriately
│
├── coding-style.md - Code organization
│   - Naming conventions
│   - File structure patterns
│   - Import organization
│
├── testing.md - Testing requirements
│   - Test-first when appropriate
│   - Minimum coverage expectations
│   - Test naming conventions
│
├── git-workflow.md - Git conventions
│   - Commit message format
│   - Branch naming
│   - PR process
│
└── None - I'll add custom rules later
```

### Step 3: Create Rules Directory

```bash
mkdir -p .claude/rules
```

### Step 4: Copy Selected Templates

```bash
# For each selected rule
cp templates/rules/security.md .claude/rules/
cp templates/rules/coding-style.md .claude/rules/
cp templates/rules/testing.md .claude/rules/
cp templates/rules/git-workflow.md .claude/rules/
```

### Step 5: Customize Rules (Optional)

For each rule, ask if customization needed:

**Security:**
```
AskUserQuestion: "Customize security rules?"
├── Keep defaults
├── Add: Block commits with .env files
├── Add: Require security review for auth code
└── Custom
```

**Coding Style:**
```
AskUserQuestion: "Naming convention preference?"
├── camelCase (JavaScript/TypeScript default)
├── snake_case (Python default)
├── Keep language defaults
└── Custom convention
```

**Testing:**
```
AskUserQuestion: "Test requirements?"
├── TDD required for all features
├── Tests required but TDD optional
├── Tests optional (suggest only)
└── Custom
```

**Git:**
```
AskUserQuestion: "Commit message format?"
├── Conventional Commits (feat:, fix:, etc.)
├── Simple prefix (Add, Fix, Update)
├── No specific format
└── Custom format
```

### Step 6: Document in CLAUDE.md

Add rules summary to CLAUDE.md:

```markdown
## Active Rules

Rules in `.claude/rules/` are always enforced:

| Rule | Key Points |
|------|------------|
| security.md | No secrets in code, validate inputs |
| coding-style.md | camelCase, imports grouped |
| testing.md | Tests required for features |
| git-workflow.md | Conventional commits |

See individual rule files for full details.
```

## Rule File Format

Rules use a simple markdown format:

```markdown
# Rule Name

Brief description of what this rule covers.

## Always Do

- Point 1
- Point 2
- Point 3

## Never Do

- Anti-pattern 1
- Anti-pattern 2
- Anti-pattern 3

## Examples

### Good
```code
// Good example
```

### Bad
```code
// Bad example
```

## Exceptions

When it's okay to break this rule:
- Exception 1
- Exception 2
```

## Rule Categories

### Security Rules

**Focus**: Preventing security vulnerabilities

**Common rules**:
- No hardcoded secrets
- Input validation required
- Output escaping required
- Authentication checks
- SQL injection prevention
- XSS prevention

### Coding Style Rules

**Focus**: Consistent, readable code

**Common rules**:
- Naming conventions
- File organization
- Import ordering
- Function length limits
- Comment requirements
- Type annotation requirements

### Testing Rules

**Focus**: Quality assurance

**Common rules**:
- Test coverage requirements
- TDD workflow
- Test naming conventions
- Mock usage guidelines
- Integration test requirements

### Git Workflow Rules

**Focus**: Version control practices

**Common rules**:
- Commit message format
- Branch naming conventions
- PR requirements
- Review process
- Merge strategies

## Custom Rules

### Creating Custom Rules

1. Create a new .md file in `.claude/rules/`
2. Use the standard format
3. Be specific and actionable

### Example Custom Rule

```markdown
# API Design

Rules for designing consistent APIs in this project.

## Always Do

- Use RESTful conventions for HTTP endpoints
- Return consistent response shapes
- Include pagination for list endpoints
- Version APIs in URL (/v1/, /v2/)

## Never Do

- Mix REST and RPC styles
- Return different shapes for similar endpoints
- Use query params for mutations
- Break existing API contracts

## Examples

### Good
```typescript
// GET /api/v1/users
// Returns: { data: User[], pagination: {...} }

// POST /api/v1/users
// Returns: { data: User }
```

### Bad
```typescript
// GET /api/getUsers (RPC style)
// Returns: User[] (no wrapper)
```
```

## Integration with Workflows

### During Implementation

Claude checks rules before each action:
1. Read relevant rules
2. Verify action complies
3. Proceed or adjust

### During Review

Code reviewer subagent:
1. Loads all rules
2. Checks code against each
3. Reports violations

### During Commits

Git workflow rule enforced:
1. Check commit message format
2. Verify branch naming
3. Ensure PR process followed

## Troubleshooting

### Rule Not Being Followed

1. Check rule is in `.claude/rules/`
2. Verify file is readable
3. Check for conflicting rules
4. Make rule more specific

### Rules Conflicting

1. Identify which rules conflict
2. Add exception to one
3. Or merge into single rule

### Rules Too Restrictive

1. Add more exceptions
2. Relax specific constraints
3. Convert to suggestion instead of rule

## Output Format

Present rules configuration:

```
═══════════════════════════════════════════════════════════════════════════
Rules Configuration
═══════════════════════════════════════════════════════════════════════════

Active Rules:
├── security.md
│   - No hardcoded secrets
│   - Input validation required
│   - Secure output handling
│
├── coding-style.md
│   - camelCase naming
│   - Grouped imports
│   - Max 200 lines per file
│
├── testing.md
│   - Tests required for features
│   - TDD encouraged
│   - Min 80% coverage goal
│
└── git-workflow.md
    - Conventional commits
    - Feature branches
    - PR required for main

Location: .claude/rules/

Note: Rules are always active and enforced by Claude.
```
