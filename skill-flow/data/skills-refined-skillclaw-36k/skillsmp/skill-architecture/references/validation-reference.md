**Skill**: [Skill Architecture](../SKILL.md)

## Terminology: Audit vs Validate vs Verify

These terms have distinct meanings in the skill ecosystem:

| Term         | Definition                                  | Example Usage                                       |
| ------------ | ------------------------------------------- | --------------------------------------------------- |
| **audit**    | Detect violations, issues, or anti-patterns | `code-hardcode-audit` detects magic numbers         |
| **validate** | Check compliance with format/rules          | `link-tools:link-validator` checks link portability |
| **verify**   | Confirm existence or state                  | Preflight verifies ADR artifacts exist              |

**Guidelines**:

- Use **audit** for skills that scan for problems (static analysis, code smells)
- Use **validate** for skills that check format compliance (schemas, conventions)
- Use **verify** for workflow checkpoints that confirm prerequisites

---

## Part 9: Validation Checklist

Before finalizing:

- [ ] YAML frontmatter valid (name, description)
- [ ] `name` follows rules (lowercase, hyphens, \<64 chars)
- [ ] `description` includes WHAT + WHEN (\<1024 chars, specific triggers)
- [ ] `description` single-line, no colons in text (use `-` not `:`), unquoted
- [ ] Instructions use imperative mood
- [ ] Markdown formatting: No manual section numbering (use `--number-sections` for PDFs)
- [ ] At least one concrete example
- [ ] Security audit passed (no secrets, input validation)
- [ ] `allowed-tools` restricts dangerous operations
- [ ] Tested activation with trigger keywords
- [ ] File paths relative or documented
- [ ] No duplicate functionality
- [ ] Supporting files in scripts/, reference.md, examples.md

---

## Part 10: Quick Reference

**Minimal valid Agent Skill**:

```yaml
---
name: my-skill
description: Does X when user mentions Y (specific triggers)
---
# My Skill

1. Do this
2. Then this
3. Finally this
```

**Locations**:

- Personal: `~/.claude/skills/my-skill/SKILL.md`
- Project: `.claude/skills/my-skill/SKILL.md`

**Reload**: Agent Skills auto-reload. For manual: `/clear` or restart conversation.

**Token cost**: 30-50 tokens until activated (unlimited Agent Skills possible!)

**Security**: Sandbox, restrict tools, validate inputs, no secrets.

---

## Resources

- **Official Docs**: <https://docs.claude.com/en/docs/claude-code/skills>
- **Official Repo**: <https://github.com/anthropics/skills>
- **Template**: <https://github.com/anthropics/skills/tree/main/template>
- **Support**: <https://support.claude.com/en/articles/12512198-how-to-create-custom-skills>

---

## Plugin Manifest Validation

<!-- ADR: /docs/adr/2025-12-14-alpha-forge-worktree-management.md (lesson learned) -->

When creating **plugins** (not just skills), additional validation is required for marketplace discovery.

### Critical: Marketplace Registration

Plugins must be registered in `.claude-plugin/marketplace.json` to be discoverable by `/plugin install`. Creating a plugin directory without registration results in:

```
Plugin "plugin-name" not found in any marketplace
```

### Validation Script

Run before committing plugin changes:

```bash
node scripts/validate-plugins.mjs           # Validate only
node scripts/validate-plugins.mjs --fix     # Show fix instructions
node scripts/validate-plugins.mjs --strict  # Fail on warnings too
```

### What It Validates

| Check                  | Error Level | Description                                        |
| ---------------------- | ----------- | -------------------------------------------------- |
| Directory registration | ❌ Error    | Plugin dirs must have marketplace.json entry       |
| Required fields        | ❌ Error    | name, description, version, source, category       |
| Source path exists     | ❌ Error    | `source` field must point to real directory        |
| Hooks file exists      | ❌ Error    | `hooks` field (if present) must point to real file |
| Orphaned entries       | ⚠️ Warning  | Registered plugins must have directories           |
| Missing author         | ⚠️ Warning  | Recommended field                                  |
| Missing keywords       | ⚠️ Warning  | Recommended field                                  |

### Pre-Commit Hook

Install the validation hook to catch issues automatically:

```bash
./scripts/install-hooks.sh
```

The hook runs `validate-plugins.mjs` when `plugins/` or `marketplace.json` changes.

### Plugin Entry Template

When adding a new plugin, use this template:

```json
{
  "name": "my-plugin",
  "description": "Brief description of what the plugin does",
  "version": "1.0.0",
  "source": "./plugins/my-plugin/",
  "category": "productivity",
  "author": { "name": "Your Name", "url": "https://github.com/username" },
  "keywords": ["relevant", "keywords"],
  "strict": false
}
```

### Workflow Recommendation

Use `/plugin-dev:create` to create new plugins - it handles marketplace registration automatically (Phase 3.1).

---

## Meta-Example: This Agent Skill

This `agent-skill-builder` demonstrates its own principles:

1. ✅ **Clear name**: `agent-skill-builder` (lowercase, hyphenated, precise)
1. ✅ **Specific description**: Mentions "agent skill", "create", "build", "structure" as triggers
1. ✅ **Structured content**: Progressive disclosure with 10 parts
1. ✅ **Security included**: Dedicated section on threats and best practices
1. ✅ **Token efficient**: Core guidance here, could add reference.md for advanced topics
1. ✅ **CLI-specific**: Clarifies this is for Claude Code CLI, not API
1. ✅ **Examples**: Multiple concrete patterns
1. ✅ **Validation**: Includes checklist
1. ✅ **Official terminology**: Uses "Agent Skills" (formal) and `skills/` (file paths)

**Token usage**: ~50 tokens when inactive, ~2000 when fully loaded

---

## Summary

**Creating effective Claude Code CLI Agent Skills requires:**

1. **Specific naming/descriptions** for autonomous discovery (WHAT + WHEN + triggers)
1. **YAML frontmatter** with name, description, optional allowed-tools
1. **Security-first mindset** (sandbox, restrict tools, validate inputs, no secrets)
1. **Token optimization** (progressive disclosure, split large content)
1. **Structured content** (imperative instructions, concrete examples)
1. **Validation testing** (verify activation, security audit)
1. **Single focus** (one capability per Agent Skill)

This meta-Agent Skill teaches Agent Skill creation by being a canonical example itself.
