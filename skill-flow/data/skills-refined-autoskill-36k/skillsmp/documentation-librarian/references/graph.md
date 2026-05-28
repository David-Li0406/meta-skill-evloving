# docs/graph.md — Documentation Graph (Template)

## Purpose

This file is a **lightweight dependency map** of the documentation system.
It exists to make “Relationship Repair” (Mode 2B) deterministic: when something changes, identify the **subtree** of docs that must be updated to keep global consistency.

---

## Nodes (key documents)

> Add only key nodes and high-value docs. Keep it small and current.

* **ID:** readme-root

  * Type: README
  * Path: `../README.md`
  * Status: Active
  * Responsibility: Repository entry point and doc map.

* **ID:** docs-home

  * Type: README
  * Path: `README.md`
  * Status: Active
  * Responsibility: Documentation landing page and navigation.

* **ID:** roadmap

  * Type: ROADMAP
  * Path: `roadmap/roadmap.md`
  * Status: Draft
  * Responsibility: Direction, sequencing, and scope boundaries.

* **ID:** principles

  * Type: PRINCIPLES
  * Path: `principles/principles.md`
  * Status: Draft
  * Responsibility: Constraints and heuristics guiding decisions.

> Add your core specs/reference/playbooks below as they appear:

* **ID:** spec-\<area\>

  * Type: SPEC
  * Path: `spec/<area>.spec.md`
  * Status: Draft
  * Responsibility: \<one sentence\>

* **ID:** ref-\<surface\>

  * Type: REFERENCE
  * Path: `reference/<surface>.reference.md`
  * Status: Draft
  * Responsibility: \<one sentence\>

* **ID:** playbook-\<name\>

  * Type: PLAYBOOK
  * Path: `playbooks/<name>.playbook.md`
  * Status: Draft
  * Responsibility: \<one sentence\>

* **ID:** manifesto-\<domain\>

  * Type: MANIFESTO
  * Path: `manifesto/<domain>.manifesto.md`
  * Status: Draft
  * Responsibility: \<one sentence\>

---

## Edges (relationships)

Use: `A -> B : <relationship-type> (optional note)`

Relationship types (use these exact labels):

* `depends-on`
* `references`
* `supersedes`
* `operationalizes`
* `explains-why`

Examples (replace with real ones):

* `docs-home -> spec-<area> : references`
* `spec-<area> -> ref-<surface> : references`
* `playbook-<name> -> spec-<area> : operationalizes`
* `adr-0001-<slug> -> spec-<area> : explains-why`

---

## Subtrees (blast radius groups)

Define groups that usually must be updated together.

* **Group:** \<Area\> Contract Subtree

  * Root: `spec-<area>`
  * Includes: `ref-<surface>`, `playbook-<name>`, `docs-home`
  * Notes: “If \<behavior\> changes, update all.”

* **Group:** Operations Subtree

  * Root: `playbook-<name>`
  * Includes: `ref-<surface>`, `spec-<area>`
  * Notes: “If procedure changes, ensure invariants still hold.”

---

## Invariants (doc-graph constraints)

* Specs must not contradict Reference.
* Guides must link to Reference for exact interface details.
* Playbooks must link to the spec/reference they operationalize.
* Roadmap items should link to at least one tracking artifact (spec/issue/epic).
* Deprecated/superseded docs must link to replacements.

---

## Maintenance triggers

Update this file when:

* A new SPEC/REFERENCE/PLAYBOOK is added
* A doc is deprecated/superseded
* Major dependencies change
* The doc set grows beyond trivial navigation
