**Skill**: [semantic-release](../SKILL.md)

# Documentation Linking in Release Notes

Automatically include links to all documentation changes in release notes, with AI-friendly categorization.

## Overview

When semantic-release creates a release, the `generate-doc-notes.mjs` script detects all changed markdown files and appends categorized links to the release notes.

## Documentation Categories

The script organizes documentation into these categories:

| Category             | Pattern                                  | Grouping                        |
| -------------------- | ---------------------------------------- | ------------------------------- |
| **ADRs**             | `docs/adr/YYYY-MM-DD-slug.md`            | Status table                    |
| **Design Specs**     | `docs/design/YYYY-MM-DD-slug/spec.md`    | List with change type           |
| **Skills**           | `plugins/*/skills/*/SKILL.md`            | Grouped by plugin (collapsible) |
| **Plugin READMEs**   | `plugins/*/README.md`                    | Simple list                     |
| **Skill References** | `plugins/*/skills/*/references/*.md`     | Grouped by skill (collapsible)  |
| **Commands**         | `plugins/*/commands/*.md`                | Grouped by plugin (collapsible) |
| **Root Docs**        | `CLAUDE.md`, `README.md`, `CHANGELOG.md` | Simple list                     |
| **General Docs**     | `docs/*.md` (excluding adr/, design/)    | Simple list                     |
| **Other**            | Any other `*.md` files                   | Catch-all list                  |

## How It Works

The script uses a **union approach** to detect documentation:

1. **Git diff detection**: All `.md` files changed since the last release tag
2. **Change type tracking**: Marks files as `new`, `updated`, `deleted`, or `renamed`
3. **Line count delta**: Shows additions/deletions via `git diff --numstat` (e.g., `+152/-3`)
4. **Rename context**: Preserves old path for renamed files (e.g., `renamed from \`old/path\``)
5. **Commit message parsing**: References like `ADR: 2025-12-06-slug` in commit bodies
6. **ADR-Design Spec coupling**: If one is changed, the corresponding pair is included
7. **Full HTTPS URLs**: Required for GitHub release pages (relative links don't work)

## Configuration

### Simple Setup (Hardcoded Path)

Add to your `.releaserc.yml` **before** `@semantic-release/changelog`:

```yaml
# All documentation changes in release notes
# ADR: 2025-12-06-release-notes-adr-linking
- - "@semantic-release/exec"
  - generateNotesCmd: "node plugins/itp/skills/semantic-release/scripts/generate-doc-notes.mjs ${lastRelease.gitTag}"
    prepareCmd: "node scripts/sync-versions.mjs ${nextRelease.version}"
```

### Environment Variable Setup (Shareable)

For projects using the installed plugin:

```bash
/usr/bin/env bash << 'DOC_RELEASE_LINKING_SCRIPT_EOF'
export DOC_NOTES_SCRIPT="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}/skills/semantic-release/scripts/generate-doc-notes.mjs"
DOC_RELEASE_LINKING_SCRIPT_EOF
```

Then in `.releaserc.yml`:

```yaml
- - "@semantic-release/exec"
  - generateNotesCmd: 'node "$DOC_NOTES_SCRIPT" ${lastRelease.gitTag}'
```

### Why Environment Variable for Shareable Configs?

**Important**: `@semantic-release/exec` uses [lodash templates](https://lodash.com/docs/4.17.15#template) to process commands. Lodash interprets `${...}` as JavaScript expressions, not shell variables.

| Syntax                             | What Lodash Does        | Result                              |
| ---------------------------------- | ----------------------- | ----------------------------------- |
| `${lastRelease.gitTag}`            | Evaluates as JS         | Works (semantic-release context)    |
| `${CLAUDE_PLUGIN_ROOT:-$HOME/...}` | Tries to evaluate as JS | `SyntaxError: Unexpected token ':'` |
| `$DOC_NOTES_SCRIPT`                | Ignores (no braces)     | Passes through to bash              |

## Output Format

The script generates categorized markdown with line count deltas (example):

```markdown
---

## Documentation Changes

## Architecture Decisions

### ADRs

| Status   | ADR                                     | Change            |
| -------- | --------------------------------------- | ----------------- |
| accepted | [Ralph RSSI Architecture](blob-url)     | new (+152)        |
| accepted | [PostToolUse Hook Visibility](blob-url) | updated (+45/-12) |

### Design Specs

- [Ralph RSSI Spec](blob-url) - new (+89)
- [Auth Flow Spec](blob-url) - renamed from `docs/design/old-auth/spec.md` (+5/-3)

## Plugin Documentation

### Skills

<details>
<summary><strong>itp</strong> (2 changes)</summary>

- [semantic-release](blob-url) - updated (+67/-23)
- [mise-configuration](blob-url) - updated (+12)

</details>

### Plugin READMEs

- [ralph](blob-url) - updated (+8/-2)

## Repository Documentation

### Root Documentation

- [README.md](blob-url) - updated (+15/-5)
```

### Change Info Formats

| Scenario           | Format                              | Example                                |
| ------------------ | ----------------------------------- | -------------------------------------- |
| New file           | `new (+N)`                          | `new (+152)`                           |
| Updated (add only) | `updated (+N)`                      | `updated (+45)`                        |
| Updated (del only) | `updated (-N)`                      | `updated (-12)`                        |
| Updated (both)     | `updated (+N/-M)`                   | `updated (+45/-12)`                    |
| Renamed            | `renamed from \`old/path\` (+N/-M)` | `renamed from \`docs/old.md\` (+5/-3)` |
| Deleted            | `deleted`                           | `deleted`                              |
| No line stats      | `changeType` only                   | `updated` (fallback if numstat fails)  |

## ADR Reference in Commits

To explicitly link an ADR in release notes (even if the ADR file wasn't modified), include this in your commit message body:

```
feat: add new authentication flow

Implements OAuth2 PKCE flow for mobile clients.

ADR: 2025-12-06-oauth2-pkce-mobile
```

The script will detect this reference and include the ADR in release notes.

## Edge Cases

| Scenario        | Behavior                                                      |
| --------------- | ------------------------------------------------------------- |
| No docs changed | Script exits silently (no section added)                      |
| First release   | Uses `git ls-files` to find all tracked docs                  |
| File deleted    | Shows with `deleted` change type (no line stats)              |
| File renamed    | Shows old path: `renamed from \`old/path\`` with line delta   |
| No H1 in file   | Uses filename/slug as fallback title                          |
| Missing file    | Referenced commits are skipped if file doesn't exist          |
| Empty category  | Category section is omitted entirely                          |
| Binary file     | Line stats show as `0` (git numstat returns `-` for binaries) |
| No line changes | Line delta omitted, just shows change type                    |

## Requirements

- **Git remote**: Must have `origin` remote configured
- **Node.js**: ES modules support (Node 14+)
- **Markdown files**: Must have `.md` extension

## Related

- [ADR Code Traceability](../../adr-code-traceability/SKILL.md) - Reference ADRs in code comments
- [Local Release Workflow](./local-release-workflow.md) - Complete release process
