---
name: pr-workflow
description: Use this skill when generating standardized pull request titles and descriptions for GitHub PRs, ensuring adherence to project conventions.
---

# Pull Request Workflow

This skill encompasses the generation of both pull request titles and descriptions, following established project conventions.

## Pull Request Title Format

Follow these conventions when creating pull request titles.

### Rules

1. Use Conventional Commit format: `<type>[optional scope]: <description>`
2. Types: feat, fix, refactor, docs, test, chore, style, perf, ci
3. An optional scope MAY be provided to a commit's type.
4. A scope MUST consist of a noun describing a section of the codebase surrounded by parentheses.
5. Keep under 72 characters including type and scope.
6. Be specific and descriptive.
7. Use imperative mood (e.g., 'add' not 'added').
8. No period at the end.
9. Respond with ONLY the title, no explanations or markdown formatting.

### Examples

**Good examples:**

- chore: cleanup workspace config and refactor agent names
- feat: implement PR title generation using Claude API
- feat(auth): add OAuth2 login support
- fix(api): resolve null pointer exception in user endpoint
- docs(readme): update installation instructions for clarity

**Bad examples:**

- Added OAuth2 login support. (not imperative, has period)
- Fix issue with user endpoint (not specific)
- Update docs (not descriptive)
- feat: implement PR title generation using Claude API to enhance automation and improve workflow efficiency in CI/CD processes (too long)

## Pull Request Description Format

Follow these conventions when creating a pull request description.

### PR Description Structure

Use the project template with three required sections. See [PR Template](./assets/pull_request_template.md).

#### Section 1: Scope & Context

```markdown
### 🎯 Scope & Context

**Type:** [Feat | Fix | Refactor | Chore | Perf]

**Intent:** [1-2 sentences explaining the business or technical goal]

**Related Issues:** [#123 - Remove if none]
```

#### Section 2: Reviewer Guide

```markdown
### 🧭 Reviewer Guide

**Complexity:** [Low | Medium | High]

#### Entry Point

[Most critical file where reviewer should start + why]

#### Sensitive Areas

- `path/to/file`: [Why this needs extra scrutiny]
```

#### Section 3: Risk Assessment

```markdown
### ⚠️ Risk Assessment

- **Breaking Changes:** [Yes + details | No breaking changes]
- **Migrations/State:** [Required steps | No migrations or state changes]
```

### Formatting Constraints

| Rule                      | Requirement                                               |
| ------------------------- | --------------------------------------------------------- |
| **Emojis**                | Only in section headers (🎯, 🧭, ⚠️) as shown in template |
| **No fluff**              | Avoid generic intros like "This PR updates..."            |
| **All sections required** | Include all 3 sections from template                      |
| **Dynamic sub-sections**  | Only show sub-sections if relevant data exists            |
| **No top-level headers**  | Start directly with first section                         |
| **Dashes**                | Use single hyphen with spaces: " - " not "—"              |
| **Filenames**             | Wrap in backticks: \`lib/services/AutoPayService.ts\`     |

### Complexity Assessment

| Level      | Criteria                                                                         |
| ---------- | -------------------------------------------------------------------------------- |
| **Low**    | Single file or config changes, documentation, simple fixes                       |
| **Medium** | Multiple related files, new features with tests, refactoring                     |
| **High**   | Cross-cutting changes, database migrations, breaking changes, security-sensitive |

### Anti-Patterns

| Pattern                     | Problem                  | Correct Form                        |
| --------------------------- | ------------------------ | ----------------------------------- |
| `This PR adds...`           | Fluff intro              | Start with Type and Intent directly |
| Using "—"                   | Em-dash causes issues    | Use " - " (hyphen with spaces)      |
| Missing Entry Point         | Reviewer lacks direction | Always specify where to start       |
| `file.ts` without backticks | Poor formatting          | Use \`file.ts\`                     |

### Language

ALWAYS write PR titles and descriptions in **English** regardless of conversation language.