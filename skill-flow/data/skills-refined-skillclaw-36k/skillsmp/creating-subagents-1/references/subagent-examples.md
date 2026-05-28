---
title: Subagent Examples
description: Complete examples of well-designed subagents demonstrating concise prompts, skill integration patterns, and color coding across 6 design patterns
keywords: examples, patterns, skill integration, prompt-only, skill-augmented, color coding, best practices
skill: creating-subagents
---

# Subagent Examples

Examples of well-designed subagents demonstrating concise prompts, skill integration, and color coding.

## Color Coding

All subagents use color coding for visual identification. See `color-codes.md` for the complete color system.

**Quick reference**:
- **purple**: Review/audit agents
- **blue**: Implementation/development agents
- **green**: Testing/validation agents
- **yellow**: Documentation agents
- **orange**: Maintenance/refactoring agents
- **red**: Debugging/troubleshooting agents
- **cyan**: Research/analysis agents
- **magenta**: Deployment/operations agents
- **white**: General purpose agents

## Pattern 1: Prompt-Only (Simple Orchestration)

**When to use**: Task requires only tool orchestration without specialized knowledge.

### Example: Test Runner

```markdown
---
name: test-runner
description: Run tests and fix failures. Use proactively after code changes or when tests mentioned.
tools: Bash, Read, Edit, Grep
model: inherit
color: green
---

Run relevant tests after code changes and fix failures.

Workflow:
1. Identify test files matching changed code
2. Run tests using appropriate test command
3. If failures occur, analyze and fix root cause
4. Re-run to verify fixes

Always preserve original test intent when fixing.
```

**Why this works**:
- Clear, directive instructions (< 100 words)
- No specialized knowledge needed
- Tool orchestration only
- No skill needed
- Green color indicates testing purpose

## Pattern 2: Skill-Augmented (Domain Knowledge)

**When to use**: Task requires specialized knowledge or procedures.

### Example: Security Auditor with Skill

**First, create the skill**:

`.claude/skills/security-audit/SKILL.md`:
```markdown
---
name: security-audit
description: Security audit knowledge and procedures for code review.
---

# Security Audit

Audit code for common security vulnerabilities.

## Critical Checks

### Authentication & Authorization
- Verify authentication on protected endpoints
- Check authorization before data access
- Validate session management

### Input Validation
- All user input must be validated
- Use parameterized queries (no string interpolation)
- Sanitize output for XSS prevention

### Sensitive Data
- No secrets in code or logs
- Encrypted sensitive data at rest
- Secure credential storage

### Common Vulnerabilities
- SQL injection vectors
- XSS attack surfaces
- CSRF protection
- Path traversal risks
- Insecure deserialization
```

**Then, create concise subagent**:

`.claude/agents/security-auditor.md`:
```markdown
---
name: security-auditor
description: Security audit specialist. Use proactively after implementing authentication, data handling, or API endpoints.
tools: Read, Grep, Glob, Bash
model: sonnet
color: purple
---

Audit code for security vulnerabilities using @security-audit procedures.

Focus on recent changes via git diff. Report findings by severity (critical/high/medium/low).

Flag immediate blockers, suggest fixes.
```

**Why this works**:
- Subagent prompt: 35 words (ultra-concise)
- All domain knowledge in skill
- Skill reusable across agents
- Easy to maintain and update
- Purple color indicates review/audit purpose

## Pattern 3: Multi-Skill Integration

**When to use**: Task combines multiple domains of expertise.

### Example: API Developer

**Leverages existing skills**:
- `@crafting-agentic-prompts` for prompt quality
- `@api-design` (hypothetical) for REST patterns
- `@database-schema` (hypothetical) for data access

`.claude/agents/api-developer.md`:
```markdown
---
name: api-developer
description: Build RESTful APIs with best practices. Use when implementing new endpoints or API features.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
color: blue
---

Implement RESTful APIs following @api-design patterns.

Design:
1. Review @database-schema for data relationships
2. Define resource-oriented endpoints
3. Implement CRUD operations
4. Add input validation and error handling
5. Write integration tests

Use @security-audit for security review before completion.
```

**Why this works**:
- Subagent orchestrates multiple skills
- Prompt stays under 75 words
- Each skill maintains specialized knowledge
- Clear workflow with skill checkpoints
- Blue color indicates implementation/development purpose

## Pattern 4: Proactive Agent with Constraints

**When to use**: Agent should act automatically but with specific boundaries.

### Example: Code Formatter

```markdown
---
name: code-formatter
description: Format code automatically. MUST BE USED proactively after any code write or edit operations.
tools: Bash, Read
model: haiku
color: orange
---

Format code using project's formatter (prettier, black, rustfmt, etc.).

Run formatter on modified files only. Never modify formatting rules or configuration.

If formatter not found, skip silently—do not install or suggest changes.
```

**Why this works**:
- Strong proactive trigger in description
- Clear boundaries (never modify rules)
- Appropriate model (haiku for simple task)
- Handles edge cases gracefully
- Orange color indicates maintenance purpose

## Pattern 5: Research Agent with Minimal Tools

**When to use**: Agent needs to gather information without making changes.

### Example: Documentation Finder

```markdown
---
name: doc-finder
description: Locate and summarize relevant documentation. Use when users need info about APIs, libraries, or frameworks.
tools: Read, Grep, Glob, WebFetch
model: sonnet
color: yellow
---

Locate documentation for libraries, APIs, or frameworks.

Search order:
1. Local docs in `/docs`, `README.md`
2. Inline code documentation
3. Official documentation via WebFetch

Summarize findings with code examples and links. Prioritize official sources.
```

**Why this works**:
- Read-only tool access (appropriate for research)
- Clear search strategy
- No unnecessary write permissions
- Focused scope
- Yellow color indicates documentation purpose

## Pattern 6: Skill Creation Trigger

**When to use**: Subagent complexity suggests skill extraction.

### Example: Before and After

**❌ Before (bloated prompt)**:
```markdown
---
name: database-migrator
description: Handle database migrations
tools: Bash, Read, Write, Edit
---

Handle database migrations following these steps:

1. Schema Changes:
   - Always create reversible migrations
   - Use timestamp-based naming: YYYYMMDDHHMMSS_description.sql
   - Include both up and down migrations

2. Migration File Structure:
   - Start with transaction BEGIN
   - Add schema modifications
   - Include data migrations if needed
   - End with COMMIT

3. Safety Checks:
   - Verify migrations are idempotent
   - Test rollback before applying
   - Backup data for destructive changes

4. Application Changes:
   - Update models after schema changes
   - Modify queries if column names changed
   - Update indexes and constraints

[... continues for 300+ words]
```

**✅ After (skill extracted)**:

Create `@database-migrations` skill with all procedures, then:

```markdown
---
name: database-migrator
description: Handle database migrations. Use when schema changes needed or migrations mentioned.
tools: Bash, Read, Write, Edit
color: orange
---

Create and apply database migrations using @database-migrations procedures.

Verify migrations are reversible and tested before applying to production.
```

**Why this works**:
- Prompt reduced from 300+ to 25 words
- Procedural knowledge moved to reusable skill
- Easier to maintain and update
- Skill can be used by other agents
- Orange color indicates maintenance/migration purpose

## Decision Tree

Use this to decide between prompt-only vs skill-augmented:

```
Is the task > 100 words to explain?
├─ Yes → Create skill
└─ No → Prompt-only
    ├─ Does it need reference data (schemas, templates)?
    │   └─ Yes → Create skill
    └─ Does it need reusable scripts?
        └─ Yes → Create skill
```

## Best Practices Summary

1. **Start concise**: Default to < 100 words
2. **Extract early**: If prompt grows > 150 words, create skill
3. **Reference explicitly**: Use `@skill-name` syntax
4. **Minimize tools**: Only grant what's needed
5. **Test proactivity**: Verify description triggers correctly
6. **Iterate ruthlessly**: Remove anything non-essential
