# docs/README.md — Documentation Home (Template)

## Purpose

This is the documentation home for this repository. It helps contributors and stakeholders quickly find:

* **contracts** (Specs)
* **exact interfaces** (Reference)
* **how-to workflows** (Guides)
* **operations** (Playbooks)
* **decisions** (ADRs)
* **direction** (Roadmap)
* **constraints** (Principles)
* **worldview** (Manifestos)
* **norms** (Standards)

---

## How to navigate

* Need to understand the project and start fast? → **Repository README**
* Need to implement or review a change? → **Specs**
* Need exact API/type/config details? → **Reference**
* Need step-by-step “how to”? → **Guides**
* Need operational procedures / incident response? → **Playbooks**
* Need to know *why* a decision was made? → **ADRs**
* Need future direction and sequencing? → **Roadmap**
* Need the rules that constrain decisions? → **Principles**
* Need the philosophical stance in a domain? → **Manifestos**
* Need the rules for writing docs? → **Standards**

---

## Quick links

* Specs: `./spec/`
* Reference: `./reference/`
* Guides: `./guides/`
* Playbooks: `./playbooks/`
* ADRs: `./adr/`
* Roadmap: `./roadmap/roadmap.md`
* Principles: `./principles/principles.md`
* Manifestos: `./manifesto/`
* Standards: `./_standards/`
* Doc graph (blast radius map): `./graph.md`

---

## Documentation map

### Specs

* *Add specs in:* `docs/spec/`
* Suggested index: `docs/spec/README.md` (optional)
* Examples:

  * `docs/spec/<area>.spec.md`

### Reference

* *Add reference docs in:* `docs/reference/`
* Examples:

  * `docs/reference/<surface>.reference.md`

### Guides

* *Add guides in:* `docs/guides/`
* Examples:

  * `docs/guides/<topic>.guide.md`

### Playbooks

* *Add playbooks in:* `docs/playbooks/`
* Examples:

  * `docs/playbooks/<procedure>.playbook.md`

### ADRs

* *Add ADRs in:* `docs/adr/`
* ADR Index: `docs/adr/README.md` (recommended)
* Naming: `NNNN-short-title.md` (e.g., `0001-auth-provider.md`)

### Roadmap

* Roadmap: `docs/roadmap/roadmap.md`
* Optional changelog: `docs/roadmap/changelog.md`

### Principles

* Principles: `docs/principles/principles.md`

### Manifestos

* *Add manifestos in:* `docs/manifesto/`
* Examples:

  * `docs/manifesto/<domain>.manifesto.md`

### Generated docs (if any)

* If docs are generated, follow: `docs/_standards/GENERATED-DOCS.standard.md`
* Keep generated outputs separate from hand-authored narrative.

### Standards (internal)

* Standards live in: `docs/_standards/`
* Treat them as normative: they define what “good docs” mean in this repo.

---

## Start-here paths (recommended)

### New contributor

1. Repository README
2. `docs/README.md` (this page)
3. The most relevant spec(s) under `docs/spec/`
4. Setup guide under `docs/guides/` (if available)

### Integrator / API consumer

1. Relevant `docs/reference/*.reference.md`
2. Related spec(s) under `docs/spec/`
3. Related ADRs (decision context)

### Operator / on-call

1. Relevant playbook(s) under `docs/playbooks/`
2. Related reference (commands/config)
3. Related spec(s) for invariants and expected behavior

### Reviewer

1. Spec(s) for the change
2. Reference docs impacted
3. ADR(s) if decisions are involved
4. Roadmap alignment (if applicable)

---

## Doc graph (blast radius map)

For larger repos, see `docs/graph.md` to understand which docs must be updated together when something changes.

---

## Maintenance policy

* If content spans multiple intents, **split docs by type** and cross-link.
* Avoid duplication: link to the authoritative doc instead of re-explaining.
* If links break, fix immediately.
* If a doc is replaced, mark it **Superseded** and link to the replacement.
