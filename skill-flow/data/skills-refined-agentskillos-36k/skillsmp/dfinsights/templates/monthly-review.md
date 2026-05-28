# Monthly Review Prompt

Generate a significance-based monthly review focusing on impact and effort.

## Input Data

**Period:** {{MONTH}} ({{MONTH_START}} to {{MONTH_END}})

### Pull Requests

{{PRS_DATA}}

### Commits

{{COMMITS_DATA}}

### Work Items

{{WORKITEMS_DATA}}

## Task

Create a monthly review that answers: **What got done, why did it matter, and how much effort did it take?**

Focus on:

1. **High-Impact Initiatives** - Group work by theme, not just list items
2. **Effort Assessment** - Estimate HIGH/MEDIUM/LOW based on PR count, reverts, iterations
3. **Status Tracking** - Shipped, In Progress, In Review, Troubled
4. **Top Contributors** - Who drove what areas
5. **Key Observations** - Patterns, bottlenecks, concerns

## Theme Classification

Classify PRs/commits into themes:

| Theme                 | Patterns                                        |
| --------------------- | ----------------------------------------------- |
| Framework / Migration | nuxt, vue, layer, config refactor, upgrade      |
| Performance           | inp, cls, ttfb, lcp, performance, speed         |
| Registration / Auth   | registration, login, auth, customer, my-account |
| Checkout / Delivery   | checkout, delivery, cart, shipping, payment     |
| Catalog / PDP         | catalog, pdp, product, filter, category, search |
| CMS / Content         | cms, banner, pagebuilder, content               |
| Reviews / Ratings     | review, rating                                  |
| Infrastructure        | hotfix, deploy, ci, pipeline, docker            |
| Other                 | Everything else                                 |

## Effort Estimation

- **HIGH**: 5+ PRs, or multiple reverts/revisions, or abandoned attempts
- **MEDIUM**: 2-4 PRs
- **LOW**: 1 PR

## Status Categories

- **Shipped**: All PRs merged
- **In Progress**: Mix of merged and active
- **In Review**: More active than merged
- **Troubled**: Abandoned > Merged, or multiple reverts

## Output Format

```markdown
# {{MONTH}} Monthly Review

**Period:** {{MONTH_START}} to {{MONTH_END}}
**PRs:** X created (Y merged)
**Commits:** Z
**Work Items:** N active

---

## High-Impact Initiatives

### 1. [Theme Name]

**Effort: HIGH | Status: In Progress**

Why it matters: [1-2 sentences on business/technical value]

Key PRs:

- ✅ PR title (Author) - context
- 🔄 PR title (Author) - context
- ❌ PR title (Author) - why abandoned

### 2. [Theme Name]

...

---

## Feature Completions

| Feature | Ticket | Merged | Impact            |
| ------- | ------ | ------ | ----------------- |
| Name    | #123   | Date   | Brief description |

---

## Top Contributors

| Contributor | PRs | Focus Area   |
| ----------- | --- | ------------ |
| Name        | N   | Theme, Theme |

---

## Themes Summary

| Theme | PRs | Merged | Status |
| ----- | --- | ------ | ------ |
| Name  | N   | M      | Status |

---

## Key Observations

- **[Category]:** Observation with data
- **Merge rate:** X%
- **Primary focus:** Theme name
- **Concerns:** Any red flags

---

_Generated from Azure DevOps and git data_
```

## Guidelines

- **Group by significance** not chronology
- **Lead with impact** - why does this work matter?
- **Quantify effort** - how hard was it?
- **Track turbulence** - reverts, abandoned PRs, multiple attempts indicate complexity
- **Name names** - credit contributors for their focus areas
- **Flag concerns** - review bottlenecks, stalled work, high abandon rates
- **Be honest** - if something failed, say so
