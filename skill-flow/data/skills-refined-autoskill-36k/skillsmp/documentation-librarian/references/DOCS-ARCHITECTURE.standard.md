# DOCS-ARCHITECTURE.standard.md — Documentation System Architecture Standard

## Purpose

Define a **stable, scalable documentation architecture** that supports:

* small repos (single README)
* large doc systems (many files, deep relationships)
* incremental evolution without churn
* consistent navigation, linking, and ownership

This standard exists to make documentation behave like a **maintainable system**, not a folder of text.

---

## 1) Core principles (non-negotiable)

* Documentation is a **graph**. Structure must make relationships discoverable.
* Prefer **stable paths** over “pretty” reorganizations.
* Prefer **linking** over duplication. Duplicate facts rot.
* One concept = one authoritative home (“single source of truth”), others link.
* All docs must have **clear role**, **clear audience**, and **clear source of truth**.

---

## 2) Canonical folder layout

Recommended baseline (adapt if repo conventions require it):

```text
/docs
  /_standards
    README.standard.md
    GUIDE.standard.md
    SPEC.standard.md
    ADR.standard.md
    REFERENCE.standard.md
    PLAYBOOK.standard.md
    ROADMAP.standard.md
    PRINCIPLES.standard.md
    MANIFESTO.standard.md
    GENERATED-DOCS.standard.md
    DOCS-ARCHITECTURE.standard.md

  /adr
    0001-<slug>.md
    0002-<slug>.md

  /spec
    <area-or-feature>.spec.md

  /reference
    <surface>.reference.md

  /guides
    <topic>.guide.md

  /playbooks
    <procedure>.playbook.md

  /roadmap
    roadmap.md
    changelog.md (optional)

  /principles
    principles.md (or multiple files if needed)

  /manifesto
    <domain>.manifesto.md
```

Notes:

* `_standards/` is **normative**. It defines what “good” means.
* `adr/` is chronological history (append-only behavior).
* Other folders are functional groupings by doc type.

---

## 3) Naming conventions

### File naming

* Use **kebab-case**.
* Use suffixes that encode type:

  * `*.spec.md`
  * `*.reference.md`
  * `*.guide.md`
  * `*.playbook.md`
  * `*.manifesto.md`
* ADR naming:

  * `docs/adr/NNNN-short-title.md`

### Slugs

* Keep slugs short and stable.
* Do not rename for aesthetics; rename only for correctness.

---

## 4) Document headers (required metadata)

Every doc (except short READMEs) must begin with a small header block:

* **Purpose**
* **Audience**
* **Source of truth**
* **Status** (Draft | Active | Deprecated | Superseded)
* **Last reviewed** (YYYY-MM-DD)

Example header (copy pattern, not necessarily exact fields):

* Purpose: …
* Audience: …
* Source of truth: …
* Status: …
* Last reviewed: …

---

## 5) Cross-linking rules (graph hygiene)

### Mandatory: local navigation links

Each doc must include:

* a **“Related”** section linking to:

  * upstream docs (what motivated it)
  * downstream docs (what depends on it)
  * adjacent docs (same area/type)

### Linking style

* Prefer relative links (repo-stable).
* Prefer stable anchors (avoid renaming headings casually).
* If a doc is superseded, add a top-level notice:

  * “Superseded by …” and link.

### Single source of truth policy

* If a fact belongs to Reference, **do not duplicate** it in README/Guides; link instead.
* If a rationale belongs to ADR, do not rewrite it in SPEC; link to ADR.

---

## 6) Indices (required for medium+ doc sets)

Once there are more than ~10 docs, add index files:

* `docs/README.md` (Documentation Home)

  * categorized links to all major sections
* `docs/adr/README.md` (ADR Index)
* optional per-folder index README

Index rules:

* Indices must be kept current.
* Indices are navigational, not exhaustive content dumps.

---

## 7) Relationship mapping (for complex systems)

For extensive doc graphs, maintain a lightweight map:

* `docs/graph.md` (or `docs/map.md`)

  * list key nodes (specs, major references)
  * list dependencies (what references what)
  * optional Mermaid diagram (if allowed by repo policy)

This enables Mode 2B (subtree repair) to operate reliably.

---

## 8) Ownership and review discipline

For mature repos, add ownership metadata:

Option A (lightweight):

* in each doc header: **Owner: @team-or-person**

Option B (central):

* `docs/OWNERS.md` mapping areas → owners

Review cadence:

* each doc must have “Last reviewed”.
* stale docs are a **known defect**; mark with **[RISK]** if not reviewed.

---

## 9) Drift management (how to prevent rot)

### Rules

* If docs contradict code:

  * Reference and Specs must be updated or marked stale.
  * README should link to accurate sources and avoid hard claims.
* When behavior changes:

  * update the minimal subtree of docs (Mode 2B).
* Prefer adding short “Notes” sections rather than rewriting.

### Deprecation protocol

When deprecating a doc:

* keep it, do not delete (unless explicitly requested)
* mark Status: Deprecated
* add “Replaced by …” link

---

## 10) Generated documentation integration

Generated docs must:

* live under `docs/reference/` or `docs/generated/` (choose one)
* include generation instructions per GENERATED-DOCS.standard.md
* never be mixed with hand-authored narrative

If hand narrative is needed:

* split into a separate hand-authored doc that links to the generated artifact.

---

## 11) Consistency rules (lint mindset)

The Documentation Librarian must treat these as invariants:

* Every doc has a type and follows its standard.
* Every doc is reachable from at least one index or README link.
* No orphan docs in `/docs` (unless explicitly marked “WIP / parking lot”).
* No duplicated authoritative facts across multiple docs.

---

## 12) Common failure modes

* “docs/” becomes a dumping ground without indices
* doc type boundaries blur (specs become guides, readmes become references)
* link rot due to aesthetic renames
* duplicated facts drift across files
* no ownership → no maintenance

---

## 13) Definition of done (for structural doc changes)

A structural doc update is done only when:

* indices are updated
* links are valid
* affected subtree is consistent (Mode 2B logic)
* no unrelated files were reformatted or moved
* deprecated/superseded docs are clearly marked and linked
