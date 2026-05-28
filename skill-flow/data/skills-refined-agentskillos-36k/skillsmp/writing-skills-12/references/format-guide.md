# Skill Format Guide

## Directories

Use subdirectories like `references`, `scripts`, and `assets` if you have the corresponding file types. Supporting markdown documentation MUST go in `references/`. Executable scripts MUST go in `scripts/`. Static resources MUST go in `assets/`.

## File References

All file paths MUST be relative to the `SKILL.md` file, not absolute paths from the project root.

```markdown
<!-- GOOD: Relative to SKILL.md -->

See [Format Guide](references/format-guide.md)

Run the `scripts/example.ts` script.

<!-- BAD: Absolute from project root -->

See [Format Guide](skills/writing-skills/references/format-guide.md)

<!-- BAD: Missing subdirectory -->

Run the `example.ts` script.
```

## Description

Describe ONLY _when_ to use the skill, NOT what it does.

**Guidelines:**

- Start the description with "Use when" and include specific symptoms, situations, and contexts.
- Use concrete triggers and symptoms that signal when the skill applies.
- Describe the problem (e.g. race conditions), not language-specific symptoms (e.g. `setTimeout`).
- Keep it technology-agnostic unless the skill is technology-specific.
- Use a third-person perspective.
- Keep it under 500 characters.

```yaml
# BAD: Too much process detail
description: Use for TDD—write test first, watch it fail, write minimal code, refactor

# BAD: Too abstract, vague
description: For async testing

# BAD: First person
description: I can help you with async tests when they're flaky

# BAD: Mentions technology but skill isn't specific to it
description: Use when tests use setTimeout/sleep and are flaky

# GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code

# GOOD: Problem-focused description
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently

# GOOD: Technology-specific (when skill IS tech-specific)
description: Use when using React Router and handling authentication redirects
```

## Code Examples

**One excellent example beats many mediocre ones.** One great example is enough. Choose the most relevant language for the example—TypeScript/JavaScript are a good fallback if the language is not obvious.

Good examples are:

- Complete and runnable
- Well-commented explaining WHY
- From a real scenario
- Shows the pattern clearly
- Ready to adapt (not generic)

Avoid:

- Implementing in multiple languages
- Creating fill-in-the-blank templates
- Writing contrived examples

## Token Efficiency

Frequently-loaded skills appear in EVERY conversation. Every token counts, so keep them concise.

| Skill Type        | Target Word Count |
| ----------------- | ----------------- |
| Always loaded     | < 150             |
| Frequently loaded | < 200             |
| Circumstantial    | < 500             |

You can check the word count with this command:

```bash
wc -w skills/<skill-name>/SKILL.md
```

**Techniques to stay concise:**

- Move details to tool `--help` instead of documenting in skill
- Reference other skills instead of repeating instructions
- Compress examples to essentials
- Don't repeat what's in cross-referenced skills
- Don't explain what's obvious from the command

```markdown
<!-- BAD: Document all flags -->

`search-conversations` supports `--text`, `--both`, `--after <date>`, `--before <date`, `--limit <count>`

<!-- GOOD: Reference help -->

`search-conversations` supports multiple modes and filters. Run `--help` for details.

<!-- BAD: Repeat workflow from another skill -->

Before testing, commit your changes:

1. Run `git status` to check working directory
2. Run `git diff` to see what changed
3. Stage files with `git add`
4. Create commit with descriptive message
   [15 more lines of git workflow details]

<!-- GOOD: Reference other skill -->

Before testing, commit your changes. REQUIRED: Use the `git-workflow` skill for the commit process.
```

## Referencing Other Skills

When referencing other skills, wrap the skill name in backticks and use explicit requirement markers.

```markdown
<!-- GOOD: Explicit requirement marker -->

**REQUIRED:** Use the `test-driven-development` skill

<!-- GOOD: Clear requirement language -->

**REQUIRED:** You MUST use the `using-skills` skill

<!-- BAD: Unclear if required -->

See skills/testing/test-driven-development
```
