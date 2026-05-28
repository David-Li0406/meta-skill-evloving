---
name: adr-backfill
description: Backfill missing ADR from git history and documentation
---

# Objective

Reconstruct Architecture Decision Records from a repository's git history and documentation. You're doing archaeology — finding the *decisions* buried in commits, specs, and docs, then surfacing them as ADRs.

An ADR is warranted when someone made a choice that shaped the system. Not every commit is a decision. Your job is to find the ones that were.

# Process

1. **Classify files** — Distinguish architectural files (where decisions manifest) from supportive files (tests, utils). Persist this classification.

2. **Identify candidate commits** — Find commits that touch architectural files with structural changes (not just edits).

3. **Cluster into decisions** — Group related commits that represent a single decision being implemented.

4. **Fill gaps** — Pull in minor commits (typo fixes, forgotten files) that belong to a cluster but were filtered out.

5. **For each cluster** — Analyze intent, ask the user for context, generate the ADR.

6. **Scan complementary sources** — Check `specs/` and `docs/` for decisions not captured by commits.

7. **Enrich ADRs** — Add cross-references, diagrams, and implementation notes from related documentation.

8. **Order chronologically** — Renumber ADRs to maintain chronological sequence.

Maintain state in files so work isn't lost if the conversation ends.

# 1. File Classification

Consider all files - present and deleted. Deletion may reveal an architectural decision.

## Architectural (decisions live here)

**Tier 0 — Dependency manifests** (highest signal)
- `requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`
- Every addition/removal is a technology choice

**Tier 1 — Infrastructure & deployment**
- `Dockerfile`, `docker-compose*.yml`, CI configs, terraform, k8s manifests
- How the system runs and deploys

**Tier 2 — Domain structure**
- Core modules, domain boundaries, entry points, service definitions
- The shape of the system

**Tier 3 — Interface contracts**
- OpenAPI specs, protobuf, GraphQL schemas, API route definitions
- Commitments to the outside world

## Supportive (usually not decisions)

- Tests, utils/helpers, generated files, migrations, dev tooling, config instances

## Decision artifacts (check separately)

- `specs/` — Design documents that may contain decisions preceding implementation
- `docs/` — Usage guides and criteria that may encode decisions-as-code

## Judgment calls

Some files blur the line. When uncertain, ask: "If this changed significantly, would a senior engineer want to know *why* before approving?" If yes, it's architectural.

# 2. Structural Change Signals

Not every change to an architectural file is a decision. Look for:

- New directory created
- File renamed or moved (especially across boundaries)
- Dependency added, removed, or major-version bumped
- New entry point (CLI command, API route, service)
- CI/CD pipeline added or significantly changed
- New base class or interface that others will inherit/implement
- Configuration schema change (not just values)

A 200-line refactor in a util is less ADR-worthy than a one-line addition of `celery` to requirements.txt.

# 3. Clustering

## What makes a good cluster

- Represents ONE decision, even if implemented across multiple commits
- Commits are related by intent, not just proximity
- Typically spans days to a couple weeks, not months
- Has a name you could say in a sentence: "the Celery migration", "switching to FastAPI"

## When to break clusters

- Large time gap (>1-2 weeks) with context switch
- Different author working on unrelated area
- Explicit markers: "BREAKING", "v2", "rewrite", "migrate to X"

## Anti-patterns

- **Over-clustering**: One giant cluster called "backend infrastructure" — too broad
- **Under-clustering**: Every commit is its own cluster — too granular
- **Mixing decisions**: Celery integration + unrelated API redesign in one cluster

When uncertain about boundaries, ask the user.

# 4. Gates (when to stop and ask)

**Classification ambiguity**
> "I'm unsure whether `src/lib/kafka_client.py` is architectural (core infrastructure) or supportive (utility). It's used by 12 services. How do you see it?"

**Cluster boundaries**
> "Commits abc123–def456 span 3 weeks and touch both the new auth system and the database migration. Should these be one decision or two?"

**Intent unclear**
> "This cluster adds Redis, but I can't tell if it's for caching, session storage, or as a Celery broker. What was the driver?"

**Low confidence**
> "I found 4 commits that add logging configuration. Is this ADR-worthy or just housekeeping?"

Always ask before generating an ADR. Present your analysis, let the user confirm or correct.

# 5. User Context to Gather

Before generating each ADR, ask for:

1. **Trigger** — What problem or constraint forced this decision?
2. **Alternatives** — What else was considered?
3. **Rationale** — Why this solution over the alternatives?
4. **Tradeoffs accepted** — Known limitations, risks, or debt?
5. **Related decisions** — Does this supersede or depend on other ADRs?

If PR descriptions or commit messages already contain this, confirm rather than re-ask.

# 6. Complementary Sources

Git commits are the primary source but not the only one. Some decisions are better documented in specs or docs than in commit messages.

## Specs as decision artifacts

Check `specs/` for:
- Design documents that preceded implementation
- Decision specs that explain *why* before *what*
- Technical specifications that represent architectural choices

A spec file often documents a decision that spans multiple commits or was made before coding began. When you find a spec that describes a decision:
1. Note it as a potential ADR source
2. Cross-reference with commits that implemented it
3. The spec becomes the "Considered Options" and "Rationale" section

**Example:** `specs/platform-detection.md` documented the three-module detection architecture before implementation — this warranted its own ADR even without a clear commit cluster.

## Docs as enrichment sources

Check `docs/` for:
- Usage guides that reveal workflow decisions
- Selection criteria that encode preferences-as-code
- Architecture overviews that contextualize other decisions

Docs may not warrant their own ADR but can enrich commit-based ADRs with:
- Pipeline diagrams and data flow
- Scoring systems and thresholds
- Integration points between components

**Example:** `docs/SELECTION-CRITERIA.md` documented the scoring system as a deliberate choice — this warranted an ADR capturing the "criteria as code" decision.

## Gap analysis workflow

After generating commit-based ADRs:

1. **Read all specs and docs** — Identify significant decisions not yet captured
2. **Present gaps to user** — "I found N decisions in specs/docs not covered by commit-based ADRs"
3. **Generate supplementary ADRs** — Mark source as spec/doc rather than commits

**Gate:**
> "I found these decisions in specs/docs that aren't captured by commit-based ADRs:
> 1. Platform detection architecture (specs/platform-detection.md)
> 2. Sector taxonomy resolution (specs/sector-taxonomy.md)
> Which should become ADRs?"

# 7. ADR Enrichment

After initial ADR generation, enrich with cross-references and context from related documentation.

## Cross-reference mapping

Build a reference graph:
- Which ADRs depend on prior decisions?
- Which ADRs supersede or extend others?
- Which ADRs are implemented together?

Use explicit references: "With the ATS extractor architecture established (ADR-0003, ADR-0008)..."

## Enrichment from related docs

For each ADR, check if related docs contain:
- **Diagrams** that clarify architecture (pipeline flows, module relationships)
- **Tables** that summarize implementation details (platform coverage, scoring weights)
- **Workflows** that show how components interact

Add these as inline content within relevant sections, not just as references.

**Example enrichment:**
```markdown
### Architecture

**6-Phase Pipeline Vision** (designed from day one):
\`\`\`
Phase 0: Company Discovery    → company-inventory.md
Phase 1: Job Discovery        → career_jobs/*.json
...
\`\`\`
```

## Implementation Notes section

When the user provides collaboration context, add an "Implementation Notes" section capturing:

- **Collaboration patterns** — How human and AI worked together
- **Technical decisions** — Choices made during implementation
- **Technical debt** — Issues identified post-implementation

**Example:**
```markdown
### Implementation Notes

**Collaboration model:** Paired with Claude on specs, implementation, and tests.
Human wrote ~20 LoC to demonstrate the `@register_extractor` decorator mechanism
and the base class pattern — faster than explaining. Every line reviewed with
many requested changes.

**Subsequent findings:** Architecture review identified technical debt:
- REQUEST_TIMEOUT duplication (10+ files, values 10-30s)
- Intra-module duplication in `extract_job_listings.py`
```

# 8. Chronological Ordering

ADRs should be numbered chronologically by decision date, not generation order.

## When supplementary ADRs are added

If spec-derived ADRs fall chronologically between commit-based ADRs:

1. **Build chronological mapping** — Order all ADRs by date (commit dates or spec creation dates)
2. **Propose renumbering** — Show old→new mapping to user for approval
3. **Execute with git mv** — Use `git mv` for rename tracking
4. **Update content**:
   - Title headers (`# 15 - ...` → `# 2 - ...`)
   - Cross-references (`ADR-0005` → `ADR-0008`)
   - State file with new paths

## Renaming strategy

To avoid conflicts when numbers swap:
1. Rename all changing files to temp names (`git mv 0002-*.md temp-0002-*.md`)
2. Rename from temp to final names (`git mv temp-0015-*.md 0002-*.md`)

## Ordering criteria

1. **Commit date range** — Earliest commit in cluster
2. **Spec creation date** — From `git log` of spec file
3. **Logical dependency** — If A depends on B, B comes first

# 9. ADR Output

Use MADR format unless the user specifies otherwise. Place in `specs/architecture/ADR/` or the project's existing ADR location.

## Footer for commit-based ADRs
```
---
*Reconstructed from commits {first_sha}..{last_sha} ({date_range})*
```

## Footer for spec/doc-derived ADRs
```
---
*Reconstructed from {source_file} ({date_range})*
```

---

# Quality Bar

A good backfilled ADR:
- Could have been written at the time of the decision
- Captures *why*, not just *what*
- Stands alone (reader doesn't need to grep the codebase)
- Is honest about what's reconstructed vs. confirmed by the user
- Cross-references related ADRs appropriately
- Includes enrichment from specs/docs where relevant

A bad backfilled ADR:
- Just describes the code changes
- Invents rationale that the user didn't confirm
- Combines multiple unrelated decisions
- Misses the actual decision (documents a symptom, not the choice)
- Ignores relevant context in specs/docs

# State Management

Persist your work so it survives conversation boundaries:

- `specs/architecture/ADR/adr-backfill-state.yml` — classification, clusters, processing progress
- `specs/architecture/ADR/adr-backfill-clusters/` — one file per cluster with analysis and user input

Check for existing state at the start. Offer to resume or restart.

# Anti-patterns to Avoid

- **Inventing rationale**: If you don't know why, ask. Don't fabricate.
- **Over-automation**: This is archaeology, not manufacturing. User judgment is essential.
- **Boiling the ocean**: Start with high-confidence clusters (tier 0-1 changes). Get feedback. Calibrate.
- **Treating all commits equally**: A dependency addition is almost always a decision. A whitespace fix never is.
- **Ignoring specs/docs**: Commits are primary but not exclusive. Decisions often exist in documentation first.
- **Skipping enrichment**: A bare ADR is less useful than one with diagrams, tables, and cross-references.

---

# Getting Started

When the user invokes this skill:

1. Check for existing state, offer to resume
2. If starting fresh, begin with file classification
3. Show the user your classification of tier 0-1 files for validation
4. Proceed through the process, asking at each gate
5. Process clusters in chronological order within confidence tiers (high-confidence first)
6. After commit-based ADRs, scan specs/docs for gaps
7. Enrich ADRs with cross-references and context
8. Propose chronological renumbering if needed

---

# Reference

## State schema

```yaml
# adr-backfill-state.yml
version: 1
repository: "git@github.com:org/repo.git"
started_at: "2024-01-15T10:30:00Z"
last_updated: "2024-01-15T14:22:00Z"

file_classification:
  # path → {tier: int | null, category: string, override: bool}
  "requirements.txt": {tier: 0, category: "dependency_manifest"}
  "src/core/domain.py": {tier: 2, category: "domain_structure"}
  "tests/test_domain.py": {tier: null, category: "test"}

commits:
  # sha → annotation
  "abc123":
    pruned: false
    highest_tier: 0
    signals:
      - {type: "dependency_added", weight: 1.0, details: {package: "celery"}}
    architectural_files: ["requirements.txt"]
    processed: true
  "def456":
    pruned: true
    processed: true

clusters:
  # Commit-based cluster
  - id: 17
    title: "Celery Integration"
    commit_shas: ["abc123", "abc124", "abc125"]
    gap_commits: ["abc123a"]
    date_range: "2024-01-10 to 2024-01-12"
    confidence: 0.85
    status: "adr_generated"  # pending | analyzed | user_enriched | adr_generated | skipped
    analysis:
      intent_hypothesis: "Introduce async task processing"
      solution_detected: "Celery with Redis broker"
    pr_metadata:
      number: 142
      title: "Add background job processing"
      description: "..."
    user_context:
      problem: "Synchronous email sending was blocking requests..."
      alternatives: "RQ, Dramatiq, custom threading"
      rationale: "Celery has best ecosystem support..."
      limitations: "Redis becomes SPOF..."
    adr_path: "specs/architecture/ADR/0017-celery-integration.md"

  # Spec/doc-derived cluster (supplementary ADR)
  - id: 18
    title: "Platform Detection Architecture"
    commit_shas: []  # Empty for spec-derived ADRs
    source: "specs/platform-detection.md"  # Source file instead of commits
    date_range: "2024-01-08 to 2024-01-15"
    confidence: 0.9
    status: "adr_generated"
    analysis:
      intent_hypothesis: "Design comprehensive ATS detection system"
      solution_detected: "Three-module architecture with fallback strategies"
    adr_path: "specs/architecture/ADR/0012-platform-detection-architecture.md"

processing_cursor:
  step: "cluster_analysis"  # classification | pruning | filtering | clustering | gap_filling | cluster_analysis | gap_analysis | enrichment | ordering
  cluster_index: 17
  substep: "user_enrichment"

configuration:
  max_time_gap_days: 7
  adr_output_dir: "specs/architecture/ADR"
  adr_format: "madr"  # madr | nygard | custom
  git_remote: "origin"
  pr_platform: "github"  # github | gitlab | bitbucket | none
```

## MADR template

```markdown
# [seq id] - [title]

## Context and Problem Statement

...

## Considered Options

1. [option name] - [description]
2. [option name] - [description]

## Decision Outcome

Chose **Option N**: ...

### Architecture

[diagrams, tables, module descriptions from enrichment]

### Rationale

...

### Implementation Notes

[collaboration patterns, technical decisions, debt identified — when provided by user]

### Consequences

**Positive:**
- ...

**Limitations accepted:**
- ...

---
*Reconstructed from commits {first_sha}..{last_sha} ({date_range})*
```
