# UnoCSS Onmax Skill

Claude Code skill for custom UnoCSS workflow using `unocss-preset-onmax`.

Covers:
- Attribute mode patterns (`flex="~ col gap-8"`)
- Fluid spacing/typography (`f-px-md`, `f-text-xl`)
- Scale-to-pixel (1px base, not 4x multiplier)
- Custom variants (`hocus`, `reka-*`, `data-state`)
- nimiq-css design system (`nq-*` utilities)

## Install

```bash
/plugin marketplace add onmax/unocss-skill
/plugin install unocss-onmax@unocss-skill
```

Or manual:

```bash
git clone https://github.com/onmax/unocss-skill.git /tmp/unocss-skill
cp -r /tmp/unocss-skill ~/.claude/skills/unocss-onmax
```

## Files

| File | Content |
|------|---------|
| `SKILL.md` | Entry point, quick reference |
| `preset-onmax.md` | Configuration & presets |
| `attributify.md` | Attribute mode patterns |
| `fluid-sizing.md` | f- prefix utilities |
| `variants.md` | Custom variants |
| `nimiq-css.md` | Design system utilities |
