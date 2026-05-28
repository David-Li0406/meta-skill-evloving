---
# GitHub Issue Metadata (used by create-issue.ts)
issue:
  title: "chore(deps): integrate agent-browser {{VERSION}}"
  labels: [dependencies, chore, agent-browser]

# Version info (filled by agent)
version: "{{VERSION}}"
upstream_sha: "{{UPSTREAM_SHA}}"
fork_sha: "{{FORK_SHA}}"
date: "{{DATE}}"
---

# Agent-Browser {{VERSION}} Integration

Upstream [agent-browser](https://github.com/vercel-labs/agent-browser) has updates to integrate into our fork.

| | |
|---|---|
| **Upstream** | {{VERSION}} (`{{UPSTREAM_SHA}}`) |
| **Fork** | `{{FORK_SHA}}` |
| **Commits** | {{COMMIT_COUNT}} |
| **Breaking** | {{BREAKING_COUNT}} |

## Changes

### Breaking Changes

{{#if BREAKING_CHANGES}}
{{#each BREAKING_CHANGES}}
- [ ] `{{shortSha}}` {{message}}
{{/each}}
{{else}}
None
{{/if}}

### New Features

{{#if ADDITIVE_CHANGES}}
{{#each ADDITIVE_CHANGES}}
- `{{shortSha}}` {{message}}
{{/each}}
{{else}}
None
{{/if}}

### Bug Fixes

{{#if FIX_CHANGES}}
{{#each FIX_CHANGES}}
- `{{shortSha}}` {{message}}
{{/each}}
{{else}}
None
{{/if}}

## Navigator Impact

{{IMPACT_SUMMARY}}

### Files Affected

{{#each AFFECTED_FILES}}
- `{{path}}` — {{note}}
{{/each}}

### Required Changes

{{#if REQUIRED_CHANGES}}
{{#each REQUIRED_CHANGES}}
1. **{{title}}**
   - File: `{{file}}`
   - Change: {{description}}
{{/each}}
{{else}}
No code changes required.
{{/if}}

## Integration Checklist

- [ ] Review upstream changes
- [ ] Merge upstream into fork
- [ ] Push fork to GitHub
- [ ] Update navigator's `bun.lock`
- [ ] Apply required code changes
- [ ] Run `bun run typecheck`
- [ ] Run `bun test`
- [ ] Update CHANGELOG.md
- [ ] Create PR

## Links

- [Upstream diff](https://github.com/vercel-labs/agent-browser/compare/{{FORK_SHA}}...{{UPSTREAM_SHA}})
- [Fork repo](https://github.com/outfitter-dev/agent-browser)
