# DOCS-GRAPH.format.md — Documentation Graph (docs/graph.md) Format

## Purpose

`docs/graph.md` is a **lightweight dependency map** of the documentation system.
It exists to make Mode 2B (Relationship Repair) deterministic: when something changes, you can identify the **subtree** of docs that must be updated to keep global consistency.

This is not a glossary. This is not an index. This is a **relationship map**.

---

## Audience

* Documentation maintainers (human or agent)
* Reviewers assessing blast radius
* Contributors adding new specs/reference/playbooks

---

## Source of truth

* The docs themselves (links, references)
* The code base (for Reference/behavior grounding)

---

## Rules

* Keep it **small** and **current**.
* Map only key nodes and high-value relationships.
* Prefer stable IDs and stable links.
* If the repo is small (< ~10 docs), this file is optional.

---

## Format (required sections)

### 1) Nodes (authoritative list of key docs)

Each node must include:

* **ID** (stable short identifier)
* **Type** (README / SPEC / REFERENCE / GUIDE / PLAYBOOK / ADR / ROADMAP / PRINCIPLES / MANIFESTO / GENERATED)
* **Path** (relative link)
* **Owner** (optional)
* **Status** (Draft/Active/Deprecated/Superseded)
* **Primary responsibility** (one sentence)

Example:

* **ID:** spec-auth

  * Type: SPEC
  * Path: `docs/spec/auth.spec.md`
  * Status: Active
  * Responsibility: Defines authentication flows and invariants.

### 2) Edges (relationships)

Represent relationships as:

* `A -> B : <relationship-type> (optional note)`

Relationship types (use these exact labels):

* `depends-on` (B must be true/known for A to be correct)
* `references` (A links to B for detail)
* `supersedes` (A replaces B)
* `operationalizes` (A is the runbook for B’s behavior)
* `implements` (A is code/behavior contract implemented by B — use sparingly in doc graphs unless you map code artifacts too)
* `explains-why` (ADR relationship)

Example:

* `spec-auth -> ref-auth-api : references`
* `playbook-auth-incident -> spec-auth : operationalizes`
* `adr-0007-auth-provider -> spec-auth : explains-why`

### 3) Subtrees (blast radius groups)

Define 3–10 common “repair groups” that describe what usually must be updated together.

Format:

* **Group:** Auth Contract Subtree

  * Root: `spec-auth`
  * Includes: `ref-auth-api`, `guide-auth-setup`, `playbook-auth-incident`, `adr-0007-auth-provider`
  * Notes: “If login behavior changes, update all.”

### 4) Invariants (doc-graph constraints)

List the top invariants this repo wants:

* “Specs must not contradict Reference.”
* “Guides must link to Reference for exact interface details.”
* “Playbooks must link to the spec/reference they operationalize.”
* “Roadmap items must link to at least one tracking artifact (spec/issue/epic).”

---

## Optional: Mermaid diagram

If allowed, include a small Mermaid graph for major nodes only. Keep it stable and minimal.

---

## Maintenance triggers

Update `docs/graph.md` when:

* A new SPEC/REFERENCE/PLAYBOOK is added
* A doc is deprecated or superseded
* Major relationships change (new dependencies)
* The doc set crosses ~10 files and navigation becomes non-trivial

---

## Quality checklist

* You can identify the correct Mode 2B subtree in < 2 minutes.
* Relationships reflect real references (no fantasy edges).
* Groups match how changes actually propagate.
* Invariants are enforced by review (human/agent).

---

## Common failure modes

* Graph tries to model everything → becomes stale
* Missing subtrees → Mode 2B becomes guessy
* Edge labels inconsistent → no automation possible
