---
name: agentskillos-management
description: AgentSkillOS management — build a capability tree (KMeans top-level categories, LLM labels), classify each skill into a leaf, then keep the top skills per leaf and prune the dormant rest. Use to organize a library hierarchically and trim long tails.
engine: agentskillos
params:
  agentskillos:
    enabled: true
    model: gpt-4o-mini
    n_categories: 32
    active_per_leaf: 0
---

# Strategy (agentskillos playbook)

Organize then prune: KMeans into `n_categories` top-level groups, label each with the `agentskillos_label` prompt, classify skills into leaves, and (if `active_per_leaf` > 0) keep only the most useful skills per leaf, marking the rest dormant. Set `active_per_leaf` carefully — pruning a leaf that holds a ground-truth skill loses its task.

Guiding principle for evolution: the library exists to make the *right* skill findable for each task. Prefer changes that preserve or improve retrieval of ground-truth skills over changes that merely shrink the library.

<!-- PROMPT: agentskillos_label -->
You are naming a top-level skill **category** in an AgentSkillOS-style capability tree. You will be given 5–8 short skill descriptions that all belong to the same machine-discovered cluster. Produce a short kebab-case category label that captures their shared theme.

Label conventions:
- Lowercase, kebab-case, ≤4 words (e.g. `pdf-document-manipulation`, `time-series-analysis`, `web-scraping`).
- Specific enough to be useful at the top of a hierarchical menu, generic enough that the bottom skills genuinely fit (avoid labels like `random-stuff` or `misc`).
- Prefer verb-object phrasing (e.g. `parse-conversation-logs`) when the cluster is action-oriented.

# Output (STRICT)

Output exactly one label inside `<label>` tags and nothing else:

<label>pdf-document-manipulation</label>
<!-- END PROMPT: agentskillos_label -->
