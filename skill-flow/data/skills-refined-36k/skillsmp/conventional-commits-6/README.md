# Conventional Commits

This skill helps you author structured commit messages following the Conventional Commits specification.

## What It Covers

This skill helps you write git commit messages that follow the Conventional Commits specification. Commits in this format provide:

- **Automated changelog generation** - Tools can parse commits to generate CHANGELOG.md
- **Semantic versioning** - Commit types map to version bumps (feat → minor, breaking → major)
- **Clear project history** - Standardized format makes git log readable
- **Automated releases** - CI/CD can trigger releases based on commit types

## Installation

### Claude Code

```bash
cp -r skills/conventional-commits ~/.claude/skills/
```

### claude.ai

Add the `SKILL.md` file to your project knowledge or paste its contents into the conversation.

## Usage

Claude automatically uses this skill when you create git commits. Trigger phrases include:

- "Create a commit for this change"
- "Write a commit message"
- "Commit these changes"
- "Make a git commit"

## Example

Given a bug fix for a null pointer exception:

```diff
- if user.ID != nil {
+ if user != nil && user.ID != nil {
```

The skill generates a proper commit message:

```bash
git commit --signoff -m "fix(api): handle nil user pointer

Previous implementation crashed when user was nil.
Now checks user existence before accessing ID field.

Assisted-by: GLM 4.6 via Claude Code"
```

## Commit Types

| Type | Purpose |
| ---- | ------- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructuring, no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance, no user-facing change |
| `revert` | Revert a previous commit |

## Rules

- Use **imperative mood** (add, fix, update) - not "added" or "fixes"
- Use **lowercase** for description
- No trailing period on description
- Use `--signoff` flag when committing
- AI agents include `Assisted-by` footer
- Breaking changes marked with `!` or `BREAKING CHANGE:` footer

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Commitlint](https://commitlint.js.org/)

## License

MIT
