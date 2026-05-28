# DOCS-HOME.standard.md — Documentation Home (docs/README.md) Standard

## Purpose

`docs/README.md` is the **documentation landing page**: the fastest way to navigate the documentation system without hunting through folders.

This file is **navigation-first**. It should never become a dumping ground.

---

## Audience

* Contributors looking for the right doc quickly
* Reviewers trying to understand scope and contracts
* Operators looking for playbooks
* Stakeholders scanning direction (roadmap)

---

## Source of truth

* Links to the authoritative docs by type:

  * Specs define contracts
  * Reference defines exact interfaces
  * ADRs define “why”
  * Playbooks define operational procedures
  * Roadmaps define intended direction
  * Principles/Manifestos define worldview and constraints

If this page conflicts with a referenced doc, **this page is wrong**.

---

## Required structure (recommended order)

### 1) Title + one-line purpose

* `# Documentation`
* A single sentence: “How this repository documents decisions, contracts, operations, and usage.”

### 2) How to navigate (very short)

* 3–6 bullets explaining what each doc type is *in this repo* and where to find it.

### 3) Quick links (top-level)

A compact set of links to:

* Specs index
* Reference index
* Guides index
* Playbooks index
* ADR index
* Roadmap
* Principles
* Manifestos
* Standards (internal)

### 4) Documentation map (by type)

Provide headings with curated links under each:

* **Specs**
* **Reference**
* **Guides**
* **Playbooks**
* **ADRs**
* **Roadmap**
* **Principles**
* **Manifestos**
* **Generated docs** (if any)
* **Standards** (internal)

Rules:

* Keep lists curated. If a section becomes long, link to a per-folder index instead of listing everything here.

### 5) “Start here” paths (optional but recommended)

Provide 2–4 role-based paths:

* “New contributor”
* “Integrator”
* “Operator / on-call”
* “Reviewer”

Each path is 3–6 links, max.

### 6) Doc graph (optional but recommended for complex repos)

Link to `docs/graph.md` and say what it’s for.

### 7) Maintenance policy (short)

* “If a doc changes type, split it rather than blending.”
* “If links break, fix immediately.”
* “Last reviewed” policy (if used)

---

## Allowed content

* Navigation
* Lightweight context that prevents wrong turns
* Explicit “where to put new docs” guidance

## Forbidden content

* Deep technical design (belongs in SPEC)
* Exact API listings (belongs in Reference)
* Operational step sequences (belongs in Playbooks)
* Long onboarding tutorials (belongs in Guides)

---

## Quality checklist

* A contributor can find the right doc in < 30 seconds.
* Every doc category has a clear home.
* No contradictions with linked authoritative docs.
* No section grows uncontrolled (use indices).

---

## Common failure modes

* This file becomes a mini-spec
* Endless lists with no hierarchy
* “Start here” paths missing → newcomers flail
