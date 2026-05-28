---
name: git-commit
description: Guide for creating git commit messages following Conventional Commits 1.0.0 specification. Use whenever making commits to ensure consistent, semantic version-aware commit history with proper types, scopes, and breaking change indicators.
---

# Git Commit Messages

Create semantic, version-aware commit messages following Conventional Commits 1.0.0 specification.

## Quick Reference

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Example:**
```
feat(api): add pagination support

Support limit and offset parameters for list endpoints.
Enables clients to fetch large datasets incrementally.

BREAKING CHANGE: Default result limit changed from 100 to 20
```

## Type Selection

| Type | When to Use | SemVer | Example |
|------|-------------|--------|---------|
| `feat` | New feature added | MINOR | `feat(ui): add theme switching` |
| `fix` | Bug patched | PATCH | `fix(auth): correct session validation` |
| `docs` | Documentation only | - | `docs: add API authentication guide` |
| `style` | Code formatting (no logic change) | - | `style: fix indentation in router` |
| `refactor` | Code restructure (no behavior change) | - | `refactor: extract validation logic` |
| `perf` | Performance improvement | PATCH | `perf(api): parallelize database queries` |
| `test` | Adding tests | - | `test: add input validation tests` |
| `build` | Build system changes | - | `build: update build configuration` |
| `ci` | CI configuration | - | `ci: add automated deployment` |
| `chore` | Other changes (tooling, deps) | - | `chore: update dependencies` |
| `revert` | Revert previous commit | - | `revert: feat(api): add endpoint` |

## Common Project Scopes

Choose scopes that match your project architecture. Here are examples across different project types:

### Web Application Projects

| Scope | Component |
|-------|-----------|
| `api` | REST/GraphQL endpoints |
| `frontend` | Client-side UI |
| `backend` | Server-side logic |
| `auth` | Authentication/authorization |
| `database` | Database schemas/migrations |
| `ui` | User interface components |
| `routing` | Application routing |

### CLI/Library Projects

| Scope | Component |
|-------|-----------|
| `cli` | Command-line interface |
| `parser` | Input parsing logic |
| `config` | Configuration system |
| `core` | Core library functionality |
| `utils` | Utility functions |

### Infrastructure/Common

| Scope | Component |
|-------|-----------|
| `docs` | Documentation files |
| `build` | Build system |
| `ci` | Continuous integration |
| `deps` | Dependencies management |
| `cache` | Caching system |

**Scope format:**
- Use singular: `feat(api):` not `feat(apis):`
- Keep short and clear
- Optional but **recommended** for clarity

**Define your own:** These are examples. Choose scopes that match your project's architecture and components.

## Breaking Changes

Indicate breaking changes in **two ways**:

### Pattern 1: With `!` before `:`
```
feat(api)!: change response format

The API now returns JSON instead of XML
```

### Pattern 2: With `BREAKING CHANGE:` footer (uppercase required)
```
feat(compiler): update expression syntax

BREAKING CHANGE: Removed support for bare entity references.
All references must now use @ prefix: @character[id].endAt
```

### Pattern 3: Both (most explicit)
```
feat(renderer)!: remove deprecated components

BREAKING CHANGE: Removed LegacyTimeline and OldCharacter components.
Migrate to Timeline and Character components.
```

**When to use:**
- API changes that break existing code
- Removed features or options
- Changed behavior that affects users
- Configuration format changes
- Renamed functions, components, or files that are public API

## Full Specification

### Rules (MUST/MAY)

1. **Type** (REQUIRED): Commits MUST be prefixed with a type
2. **Scope** (OPTIONAL): MAY be provided after type in parentheses
3. **Description** (REQUIRED): MUST immediately follow colon and space
4. **Body** (OPTIONAL): MAY be provided after blank line
5. **Footer** (OPTIONAL): MAY be provided after blank line
6. **Breaking Changes**: MUST be indicated with `!` or `BREAKING CHANGE:` footer
7. **Case**: Type and scope are case-insensitive, but `BREAKING CHANGE` MUST be uppercase

### Description Guidelines

- **Imperative mood**: "add" not "added", "fix" not "fixed"
- **Lowercase** after colon: `feat: add feature` not `feat: Add feature`
- **No period** at end
- **Under 50 characters** (hard limit: 72)
- **Clear and concise**: what changed, not how or why

**Good:**
```
feat(compiler): add narrator:speak action type
fix(renderer): prevent video freeze with Sequence offset
docs: update XML grammar reference
```

**Bad:**
```
feat(compiler): Added narrator speak action type.  # Past tense, period
Fix(renderer): Prevent Video Freeze  # Wrong case
docs: I updated the xml grammar docs because they were outdated  # Too verbose
```

### Body Guidelines

Use body to explain:
- **WHAT** changed (if not obvious from description)
- **WHY** the change was needed (motivation)
- **Context** or background
- **Consequences** or side effects

**Do NOT explain HOW** - the code diff shows that.

**Format:**
- Blank line between description and body
- Free-form text, multiple paragraphs allowed
- Wrap at 72 characters (optional but recommended)

**Example:**
```
fix(compiler): resolve circular dependency in timeline builder

The timeline builder was importing StateManager, which imported
TimelineBuilder, causing a circular dependency that broke the
module loading in certain edge cases.

Resolved by extracting shared types to a separate module and
using dependency injection for StateManager.
```

### Footer Guidelines

**Format:** `<token>: <value>` or `<token> #<value>`

**Common tokens:**
- `BREAKING CHANGE:` - Breaking change description (uppercase required)
- `Refs:` or `Closes:` - Issue references
- `Reviewed-by:` - Code reviewers
- `Co-authored-by:` - Multiple authors

**Example:**
```
fix: prevent racing of requests

Introduce request ID and reference to latest request. Dismiss
incoming responses other than from latest request.

Reviewed-by: Z
Refs: #123
```

**Multiple footers:**
```
feat(analyzer): add Gemini video analysis

BREAKING CHANGE: GEMINI_API_KEY now required in .env
Closes: #45
Reviewed-by: User
```

## Commit Workflow

### 1. Analyze Changes
```bash
git status        # What files changed?
git diff --staged # What are the actual changes?
```

### 2. Determine Type

Ask yourself:
- **New feature?** → `feat`
- **Bug fix?** → `fix`
- **Documentation only?** → `docs`
- **Code cleanup/reorganization?** → `refactor`
- **Performance improvement?** → `perf`
- **Tests only?** → `test`
- **Build/tooling/dependencies?** → `chore`, `build`, or `ci`

### 3. Identify Scope

Which component is affected?
- Compiler? → `(compiler)`
- Renderer? → `(renderer)`
- Multiple components? → Omit scope or use general scope like `(core)`
- Documentation? → `(docs)` or no scope

### 4. Check Breaking Changes

Does this change:
- Break existing API?
- Remove features?
- Change configuration format?
- Require migration?

If YES → Add `!` or `BREAKING CHANGE:` footer

### 5. Write Description

- Start with type and optional scope
- Use imperative mood
- Keep under 50 characters
- Lowercase after colon
- No period at end

### 6. Add Body (if needed)

Add body if:
- Changes are complex
- Need to explain motivation
- Multiple related changes
- Context is important

### 7. Add Footers

Always add:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Add if applicable:
- `BREAKING CHANGE:` with migration guide
- `Closes:` or `Refs:` with issue numbers
- `Reviewed-by:` with reviewer names

### 8. Validate Format

Check:
- [ ] Type is valid (feat/fix/docs/refactor/perf/test/chore/build/ci)
- [ ] Scope uses recommended project scopes (if present)
- [ ] Description is imperative mood, lowercase, no period
- [ ] Description is under 50 characters
- [ ] Blank line before body (if body present)
- [ ] Blank line before footers (if footers present)
- [ ] `BREAKING CHANGE` is uppercase (if present)
- [ ] Claude Code footer included

## Examples

### Basic (No Scope)

```
feat: add shape:show action type
fix: prevent crash on empty timeline
docs: add troubleshooting guide
refactor: simplify expression parser
perf: optimize keyframe interpolation
test: add validator test suite
chore: update dependencies
```

### With Scope

```
feat(compiler): add word reference expressions
fix(renderer): correct caption z-index layering
docs(xml): document J-cut pattern
refactor(timeline): split state manager into modules
perf(tts): parallelize ElevenLabs requests
test(parser): add edge case coverage
chore(deps): bump remotion to 4.0.294
```

### With Body

```
feat(compiler): add multi-provider TTS support

Support both OpenAI and ElevenLabs TTS in the same project.
Each voice explicitly declares its provider in project-config.yaml.

This enables cost optimization (OpenAI for testing, ElevenLabs for
production) and provider redundancy.
```

```
fix(renderer): prevent video freeze with Sequence offset

The Sequence component was incorrectly calculating frame offsets
when action startAt was non-zero. This caused frames to be skipped
or repeated, resulting in frozen video.

Now properly accounts for action.startAt when determining which
frame of the sequence to display.
```

### Breaking Changes

**Pattern 1: With !**
```
feat(compiler)!: remove voice attribute from narrator:speak

Voice must now be defined in narrator definition, not on each action.
This enforces DRY principle and prevents inconsistent voice usage.

BREAKING CHANGE: Move voice="..." from <narrator:speak> actions to
<narrator id="..." voice="..."> definitions.
```

**Pattern 2: Multiple breaking changes**
```
feat(config)!: restructure project configuration

BREAKING CHANGE: Renamed character_voices to voices
BREAKING CHANGE: Added required provider field for each voice
BREAKING CHANGE: Removed model_id field, use model instead

Migration guide available in docs/config/migration.md
```

### Real-World Software Examples

Examples from diverse project types:

**Web Application:**
```
feat(auth): add social login providers

Integration with multiple identity providers including automatic
user profile creation and avatar fetching.

docs(api): add rate limiting documentation

fix(frontend): resolve memory leak in infinite scroll

The scroll observer was not being properly cleaned up on
component unmount, causing observers to accumulate during navigation.

refactor(backend): extract user service to separate module

perf(database): add indexes for user lookup queries

Optimizes authentication queries by indexing email and username fields.
Reduces average login time from 250ms to 45ms.

test(auth): add token refresh flow test cases
```

**CLI Tool:**
```
feat(cli): add interactive configuration wizard

Guides users through initial setup with prompts for credentials,
environment settings, and default preferences.

fix(parser): handle malformed configuration gracefully

chore(deps): update command framework to latest version
```

**Infrastructure:**
```
feat(ci): add automated changelog generation

build(container): optimize production image size

Reduces container image from 1.2GB to 340MB using multi-stage builds
and minimal base image. Removes development dependencies.
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Multiple Footers

```
fix(renderer): prevent memory leak in character components

Components were not cleaning up event listeners on unmount,
causing memory accumulation during long preview sessions.

Closes: #234
Reviewed-by: Lead Dev
Refs: #230, #231

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Integration with Project Guidelines

This skill **reinforces** existing project conventions from CLAUDE.md or similar documentation:

✅ **Already following:**
- Subject ≤50 chars
- Imperative mood ("add" not "added")
- Optional scope with component/module names
- Body explains WHAT and WHY, not HOW
- Claude Code attribution footer

✅ **New standardization:**
- Explicit type taxonomy (feat/fix/docs/refactor/perf/test/chore)
- Breaking change indicators (! or BREAKING CHANGE:)
- SemVer correlation (feat→MINOR, fix→PATCH)
- Consistent scope names for your project's components

## When to Use This Skill

Use this skill **every time** you make a git commit:
- Creating new commits (git commit)
- Amending commits (git commit --amend)
- Writing commit messages
- Reviewing commit history
- Planning feature branches

**Workflow integration:**
1. Stage changes: `git add`
2. **Reference this skill** before writing commit message
3. Select type, scope, description
4. Write commit: `git commit`
5. Validate format matches specification

## Benefits

1. **Semantic Versioning**: Commits correlate to version bumps (feat→MINOR, fix→PATCH)
2. **Consistency**: All commits follow same format
3. **Searchable**: Easy to find commits by type: `git log --grep="^feat"`
4. **Automation**: Changelogs can be auto-generated from commit history
5. **Clarity**: Type and scope make purpose immediately clear
6. **Breaking Changes**: Clearly marked for major version bumps

## Reference

**Specification:** https://www.conventionalcommits.org/en/v1.0.0/

**Project Guidelines:** Check your project's CLAUDE.md, CONTRIBUTING.md, or README.md for project-specific commit conventions.

---

*Always include Claude Code attribution footer in commits made by Claude*
