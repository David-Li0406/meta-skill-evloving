
## Part 9: Validation Checklist

Before finalizing:

- [ ] YAML frontmatter valid (name, description)
- [ ] `name` follows rules (lowercase, hyphens, \<64 chars)
- [ ] `description` includes WHAT + WHEN (\<1024 chars, specific triggers)
- [ ] Instructions use imperative mood
- [ ] Markdown formatting: No manual section numbering (use `--number-sections` for PDFs)
- [ ] At least one concrete example
- [ ] Security audit passed (no secrets, input validation)
- [ ] `allowed-tools` restricts dangerous operations
- [ ] Tested activation with trigger keywords
- [ ] File paths relative or documented
- [ ] No duplicate functionality
- [ ] Supporting files in scripts/, reference.md, examples.md

______________________________________________________________________

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

______________________________________________________________________

## Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code/skills
- **Official Repo**: https://github.com/anthropics/skills
- **Template**: https://github.com/anthropics/skills/tree/main/template-skill
- **Support**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

______________________________________________________________________

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

______________________________________________________________________

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
