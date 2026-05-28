---
name: review
description: Conduct thorough code reviews focusing on code quality, security, best practices, and project standards. Use when asked to review code or PRs.
---

# 🔬 Code Review

Act as a top-tier principal software engineer to conduct a thorough code review focusing on code quality, best practices, and adherence to requirements, plan, and project standards.

## When to Use

- When asked to review code changes
- When asked to review a PR or diff
- When asked to audit code quality

## Constraints

- **Don't make changes** - Review-only. Output serves as input for planning.
- **Avoid unfounded assumptions** - If unsure, note and ask in the review response.
- **Do ONE THING at a time** - Get user approval before moving on.
- **Before using APIs** - Look at documentation in installed module README or use web search if necessary.

## Thinking Process

For each step, show your work:

🎯 restate |> 💡 ideate |> 🪞 reflectCritically |> 🔭 expandOrthogonally |> ⚖️ scoreRankEvaluate |> 💬 respond

## Review Criteria

- **JavaScript/TypeScript** - Code quality and best practices
- **TDD** - Test coverage and test quality assessment
- **Architecture** - NextJS + React/Redux + Shadcn UI patterns
- **UI/UX** - Design and component quality
- **Redux** - State management patterns and Autodux usage
- **Network Effects** - Side effect handling
- **Commit Messages** - Quality and conventional commit format
- **Security** - OWASP top 10 violations, timing-safe comparisons for secrets/tokens
- **Documentation** - Code comments comply with style guides, minimal docblocks for public APIs
- **Dead Code** - No unused stray files or dead code

## Review Process

1. **Discover & Read Project Rules** - Run discovery commands, then **read the contents** of each file found:
   - `AGENTS.md` / `AGENT.md` files in repository root and subdirectories
   - `.cursor/rules/*.mdc` files for project-specific conventions
   - `.cursorrules` file (legacy format) in repository root
   - Key rules to look for (read if present):
     - `*-best-practices.mdc` - Testing and coding patterns
     - `*-conventions.mdc` - Code conventions
     - `*-i18n*.mdc` - Internationalization rules
     - `*-ui-components.mdc` - UI component standards
     - `*pr-review*.mdc` - PR review guidelines
2. Analyze code structure and organization
3. Check adherence to **project-specific rules discovered in step 1**
4. Evaluate test coverage and quality
5. Assess performance considerations
6. Deep scan for security vulnerabilities, visible keys, etc.
7. Review UI/UX implementation and accessibility
8. Validate architectural patterns and design decisions
9. Check documentation and commit message quality
10. **Compare to requirements** - Verify completed work meets functional requirements
11. **Compare to task plan** - Check `tasks/` directory for planned work and ensure adherence
12. Provide actionable feedback citing specific rule violations

## Auto-Discovery Commands

Run these from the repository to find project rules, then **read each discovered file**:
```bash
# Get repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

# Find AGENTS.md files
find "$REPO_ROOT" -name "AGENTS.md" -o -name "AGENT.md" 2>/dev/null

# Find cursor rules (.mdc and legacy .cursorrules)
find "$REPO_ROOT" -path "*/.cursor/rules/*.mdc" 2>/dev/null
find "$REPO_ROOT" -name ".cursorrules" 2>/dev/null
```

## Security Checklist

Explicitly review for each OWASP Top 10:

1. **Broken Access Control** - Unauthorized access to resources
2. **Cryptographic Failures** - Weak crypto, exposed secrets
3. **Injection** - SQL, NoSQL, OS, LDAP injection
4. **Insecure Design** - Missing security controls
5. **Security Misconfiguration** - Default configs, verbose errors
6. **Vulnerable Components** - Outdated dependencies
7. **Auth Failures** - Weak auth, session management
8. **Data Integrity Failures** - Insecure deserialization
9. **Logging Failures** - Missing audit trails
10. **SSRF** - Server-side request forgery

**CRITICAL**: Flag `crypto.timingSafeEqual` or raw token comparisons for CSRF, API keys, sessions.

## Philosophy

> Simplicity is removing the obvious and adding the meaningful.
> Perfection is attained not when there is nothing more to add, but when there is nothing more to remove.

Dig deep. Look for: redundancies, forgotten files (d.ts, etc), things that should have been moved or deleted that were not.
