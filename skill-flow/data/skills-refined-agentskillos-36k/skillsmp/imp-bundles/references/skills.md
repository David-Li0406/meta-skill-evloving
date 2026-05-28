# Skills Structure

Skills live in `nix/bundles/<bundle>/skills/`:

```
skills/
  my-skill/
    SKILL.md             # skill entry with YAML frontmatter
    references/          # detailed docs linked from SKILL.md
      topic1.md
      topic2.md
    scripts/             # nushell/shell scripts for the skill
      helper.nu
```

## SKILL.md Format

```markdown
---
name: my-skill
description: One-line description. Trigger when [triggers].
---

# My Skill

Brief intro and quick reference.

## References

- [Topic 1 details](references/topic1.md)
- [Topic 2 details](references/topic2.md)
```

## Symlinked Shared Scripts

When multiple skills share scripts, symlink from one to others:

```
skills/
  base-skill/scripts/shared.nu
  other-skill/scripts/shared.nu -> ../../base-skill/scripts/shared.nu
```

This avoids duplication while keeping each skill self-contained.
