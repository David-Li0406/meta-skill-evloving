# validation rules

## automated checks (`validate-skill.sh`)

| check | signal | fix |
|-------|--------|-----|
| SKILL.md exists | ERROR: Missing SKILL.md | create file |
| YAML frontmatter | ERROR: missing YAML frontmatter | add `---` block |
| name present | ERROR: Frontmatter missing name | add `name:` |
| description present | ERROR: Frontmatter missing description | add `description:` |
| third-person phrasing | ERROR: Description should use third-person trigger phrasing | start with "This skill should be used when..." |
| first-person pronouns | WARN: description may not be third-person | remove I/we/my/us |
| references linked | WARN: Reference not linked in SKILL.md | link in `## references` |
| duplicated lines | WARN: Duplicated lines between SKILL.md and references | move deep content to references |

## heuristic checks (`introspect-skill.sh`)

| signal | meaning | action |
|--------|---------|--------|
| SKILL.md > 200 lines | might be too long | keep only if full-featured tier |
| many code fences + no scripts | repeated commands likely | move to `scripts/` |
| missing triggers in description | weak activation | add explicit phrases |
| zero references | shallow depth | add references/ docs |

## manual gates (recommended)

| check | target | fix |
|-------|--------|-----|
| reference depth | >= 50 lines each | expand with examples and checklists |
| tool examples | 2+ commands | add a tool integration section |
| triggers | 3-6 phrases | list exact user language |
| anti-triggers | 2-4 phrases | add misuse cases |
| decision trees | cover ~80% scenarios | add thresholds and default branch |

## fix flow when validation fails

1. update frontmatter name/description
2. link missing references in `## references`
3. move duplicated content into references/
4. re-run `validate-skill.sh <skill-path>`
5. re-run `introspect-skill.sh <skill-path>` for suggestions

## example output (warnings)

```
Validation results for ~/.claude/skills/example
WARN: Reference not linked in SKILL.md: references/guide.md
WARN: Duplicated lines between SKILL.md and references/guide.md:
use these prompts to design a new skill before scaffolding.
```

## warning triage

| warning | likely cause | first fix |
|---------|--------------|-----------|
| reference not linked | missing entry in `## references` | add link |
| duplicated lines | same text in SKILL.md and reference | move detail to reference |
