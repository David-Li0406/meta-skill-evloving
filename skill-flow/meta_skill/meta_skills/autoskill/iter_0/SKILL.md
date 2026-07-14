---
name: autoskill-management
description: AutoSkill management — find near-duplicate skill PAIRS by embedding similarity, ask an LLM judge whether each pair is the same workflow, union-find the merges, then merge clusters and quality-filter. Use to dedupe a library conservatively (false-merge is costlier than false-keep).
engine: autoskill
params:
  autoskill:
    enabled: true
    model: gpt-4o-mini
    top_k: 10
    similarity_threshold: 0.85
  merger:
    model: gpt-4o-mini
  quality_filter:
    model: gpt-4o-mini
---

# Strategy (autoskill playbook)

Dedup by *pairwise* judgement rather than blind clustering: for each skill, take its top-k nearest neighbours above the similarity threshold, ask the `autoskill_judge` prompt whether the pair is truly the same workflow, union the merges, merge each resulting cluster, then quality-filter. Prefer `keep` when unsure — hiding a capability by over-merging directly loses tasks.

Guiding principle for evolution: the library exists to make the *right* skill findable for each task. Prefer changes that preserve or improve retrieval of ground-truth skills over changes that merely shrink the library.

<!-- PROMPT: autoskill_judge -->
You are deciding whether two SKILL.md skill bundles describe the **same reusable workflow** and should be merged into one canonical skill, or whether they describe **distinct** workflows and should stay separate.

This judgment drives AutoSkill-style library maintenance: redundant skill duplicates inflate retrieval candidate sets without adding signal, while collapsing genuinely different skills hides capability.

# Decision criteria (adapted from AutoSkill maintenance.py::_judge_merge_with_llm)

- Compare **what action the agent would actually take** when invoking the skill. If both skills push the agent through the same sequence of steps on the same kind of artifact, they are the SAME skill — verdict `merge`.
- Differences in **name only** (e.g. "edit-pdf" vs "pdf-editor"), or in surface example artifacts, are NOT enough to keep them separate.
- Differences in **scope** (one is "convert PDF to JSON", the other is "extract tables from PDF") ARE enough — verdict `keep`.
- Differences in **target framework or library** matter only if the workflow truly diverges (e.g. pandas-vs-polars dataframe analysis is `merge` if the workflow is identical; pytorch-vs-jax model training is `keep`).
- If you cannot tell from descriptions+bodies, prefer `keep` (false-merge is more costly than false-keep).

# Output (STRICT)

Reply with ONE verdict tag and nothing else:

<verdict>merge</verdict>

or

<verdict>keep</verdict>
<!-- END PROMPT: autoskill_judge -->

<!-- PROMPT: merge -->
You are a skill librarian. You are given a cluster of similar Anthropic-style "SKILL.md" skill bundles and must consolidate them into ONE merged SKILL.md.

# What is a SKILL.md?

A SKILL.md is a Markdown file describing a reusable workflow an AI coding agent can follow. It opens with YAML frontmatter containing at minimum `name` and `description`, followed by free-form Markdown instructions, optional code blocks, and references to companion files (scripts/, references/, assets/).

# Input

The user message contains {{ skills | length }} skill(s). Each is a complete SKILL.md (frontmatter + body), separated by `=== SKILL N: <key> ===` headers.

# Merge guidelines (adapted from SkillX FUNCTIONAL_MERGE_PROMPT)

1. **Generality** — produce one merged skill with a *generic* name that covers the union of what the inputs describe. Reuse the most common, broadly-applicable verb from the inputs (e.g. "PDF manipulation" rather than "PDF for invoices").
2. **Atomicity** — if the inputs describe truly different abstraction levels (one is "edit a PDF page"; another is "build a multi-step PDF pipeline"), prefer to keep the *narrower* concept and note the broader one in a sub-section rather than collapsing both into one vague skill. **Never** invent capabilities that aren't grounded in the inputs.
3. **Reusability** — strip hardcoded values from the merged body. Parameters should be described in terms of placeholders (e.g. `<input_path>`), not specific example filenames from one of the inputs.
4. **Self-contained** — the merged SKILL.md must stand alone. Do not reference companion files (scripts/, references/) that won't survive the merge — either inline the essential content or drop the reference. References that are common across multiple inputs can be kept if they're obviously generic.
5. **No verbosity** — consolidate redundant instructions across the inputs into a single canonical sentence. Drop near-duplicate notes.
6. **Frontmatter** — produce exactly two YAML keys: `name` (kebab-case slug, lowercase) and `description` (1–2 sentence summary of WHEN to use this skill, written from the agent's perspective).

# Output format (STRICT)

Return exactly one Markdown document wrapped in `<skill>` tags. The document must start with `---` frontmatter and contain valid YAML. Do NOT include any explanation or commentary outside the `<skill>` tags.

<skill>
---
name: example-merged-skill
description: Use this skill when ...
---

# Body of the merged SKILL.md

... markdown body here ...
</skill>
<!-- END PROMPT: merge -->

<!-- PROMPT: filter -->
You are a skill-library curator. Given ONE SKILL.md, decide whether to KEEP it in a reusable agent skill library or DROP it.

# What is a SKILL.md?

A SKILL.md is a Markdown file describing a reusable workflow for an AI coding agent. It has YAML frontmatter with `name` and `description`, followed by markdown instructions.

# Evaluation rubric (adapted from SkillX GENERAL_FILTER_FUNCTIONAL)

A skill is KEEP-worthy only if it meets ALL of the following:

1. **Clear frontmatter** — has both `name` (descriptive, not "unnamed" / "test" / "skill") and `description` (at least one sentence explaining when to use it).
2. **Self-contained** — the body actually instructs the agent. Skills that are *only* a description with no body, or that consist entirely of "see `references/foo.md`" without that file being inlinable, are DROP.
3. **Reusable across tasks** — the instructions are written generically (parameters, placeholders) rather than overfit to one specific input file, dataset, or company-specific scenario.
4. **Non-trivial** — the workflow involves multiple steps or a real domain concept. A skill whose entire body is one shell command (`run npm install`) or one obvious sentence (`use git`) is DROP.
5. **Coherent** — the body is comprehensible English/code, not corrupted, not a test stub (`TODO`, `lorem ipsum`, `example only`), not duplicated boilerplate.

If unsure, **err on KEEP** — false drops are worse than false keeps because the library still passes through downstream filtering (reranker, selector).

# Input

The user message will provide the SKILL.md text after `=== SKILL: <key> ===`.

# Output format (STRICT)

Provide ONE short reason (≤ 25 words) and then your verdict, wrapped in tags:

<reason>concise reason</reason>
<answer>keep</answer>

or

<reason>concise reason</reason>
<answer>drop</answer>

Do NOT output anything outside these tags.
<!-- END PROMPT: filter -->
