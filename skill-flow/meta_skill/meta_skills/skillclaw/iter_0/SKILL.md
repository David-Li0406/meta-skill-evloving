---
name: skillclaw-management
description: SkillClaw management — cluster the library, then for each cluster have an LLM decide improve / create / merge / skip, and verify each evolved skill against a quality bar before keeping it. Use to actively evolve skills, not just dedupe.
engine: skillclaw
params:
  eps: 0.10
  skillclaw:
    enabled: true
    model: gpt-4o-mini
    max_group_size: 5
    verify_enabled: true
    verify_min_score: 0.5
---

# Strategy (skillclaw playbook)

Per cluster, the `skillclaw_evolve` prompt chooses an action (improve one skill / create a better one / merge / skip); the `skillclaw_verify` prompt then scores the result and rejects it if below `verify_min_score`. Keep clusters small (`max_group_size`) so evolution stays grounded.

Guiding principle for evolution: the library exists to make the *right* skill findable for each task. Prefer changes that preserve or improve retrieval of ground-truth skills over changes that merely shrink the library.

<!-- PROMPT: skillclaw_evolve -->
You are a SkillClaw-style skill evolver. You receive a batch of {{ n }} pieces of **evidence** — each one is a real SKILL.md from the wild that someone wrote for a similar intent. Your job is to decide what *single canonical skill* (if any) should result from this evidence, and produce it.

Action vocabulary (mirrors SkillClaw/evolve_server/pipeline/execution.py `_EVOLVE_FROM_SESSIONS_SYSTEM`):

- **improve** — the evidence variants converge on a single skill that the library should hold. Synthesize the best version of it. Use this when the evidence is internally consistent and improving over the input variants is straightforward.
- **create** — the evidence reveals a *gap*: a useful skill exists in spirit but none of the variants is quite right. Write a fresh, better SKILL.md from scratch grounded in the evidence.
- **merge** — the evidence is multiple skills that *should* be one. Same as improve, but emphasize de-duplication and consolidation of the conflicting fields.
- **skip** — the evidence is too noisy / contradictory / low-quality to extract anything useful. The library should keep none of the variants. Do NOT emit a SKILL.md in this case.

# Output (STRICT)

First, name the action you chose:

<action>improve</action>   (or create / merge / skip)

If your action is NOT `skip`, follow it with exactly one Markdown skill wrapped in `<skill>` tags. Frontmatter MUST contain `name` (kebab-case slug) and `description` (1-2 sentence summary written from the agent's perspective about WHEN to use this skill).

<skill>
---
name: example-canonical-skill
description: Use this skill when ...
---

# Skill body

step-by-step instructions, code blocks, etc.
</skill>

If your action is `skip`, output only the `<action>skip</action>` tag.

# Guidelines for the produced skill

1. **Generality** — broad enough to be reusable, narrow enough to be invocable. Strip task-specific filenames; use placeholders.
2. **Self-contained** — don't reference companion files (scripts/, references/) that won't survive the merge.
3. **Concise** — consolidate redundant steps; drop near-duplicate sentences.
4. **Grounded** — never invent capabilities the evidence doesn't support.
<!-- END PROMPT: skillclaw_evolve -->

<!-- PROMPT: skillclaw_verify -->
You are a SkillClaw-style skill verifier. Score the given SKILL.md on a 0.0–1.0 scale based on whether it should be admitted to a curated agent skill library.

Scoring rubric (adapted from SkillClaw/evolve_server/pipeline/skill_verifier.py):

- **1.0** — clear, reusable, generalizable workflow with concrete actionable steps. Frontmatter `name` and `description` are present and informative. An agent could invoke this skill and follow it without external context.
- **0.7-0.9** — solid skill with minor weaknesses (vague description, some hardcoded examples, slightly verbose).
- **0.4-0.6** — useful in principle but flawed: missing frontmatter fields, ambiguous scope, mixes implementation details with workflow.
- **0.0-0.3** — unusable: broken markdown, contradictory instructions, trivial / boilerplate content, or duplicates obviously generic functionality with no added value.

# Output (STRICT)

Output exactly one numeric score in `<score>` tags, with one or two decimals, and nothing else outside.

<score>0.85</score>

Optional brief reason inside <reason> tags is allowed before the score:
<reason>clear steps, good description</reason>
<score>0.85</score>
<!-- END PROMPT: skillclaw_verify -->
