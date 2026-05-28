# Documentation Librarian

This skill defines a **Documentation Librarian** — a documentation maintainer whose job is to **preserve correctness, consistency, and continuity** across a repository’s documentation over time.

This is **not** a writing prompt.
It is a **governance and maintenance system** for documentation.

---

## What this skill is

The Documentation Librarian is designed to:

* Create documentation **when none exists**
* Update documentation **incrementally**, without rewrites
* Detect **inconsistencies and drift** across multiple documents
* Maintain documentation as a **connected system**, not isolated files
* Treat documentation as **versioned knowledge**, not prose

In short:
**it cares more about not breaking meaning than about improving wording.**

---

## What this skill is NOT

* ❌ Not a documentation generator
* ❌ Not a markdown formatter
* ❌ Not a “rewrite for clarity” assistant
* ❌ Not a creative or stylistic writer

If a task is “make this doc nicer”, this skill should **not** be used.

---

## Folder structure

```text
documentation-librarian/
  SKILL.md        # The skill definition (behavior, rules, operating modes)
  references/     # Normative documentation standards (contracts)
```

### `SKILL.md`

Defines:

* the mission of the skill
* the mental model (documentation as a graph)
* operating modes (bootstrap, incremental repair, controlled refactor)
* hard rules and stop conditions

This file answers:
**“How does the librarian think and act?”**

---

### `references/`

This folder contains **normative reference documents**.

They are:

* not templates
* not examples
* not suggestions

They define **what “correct documentation” means** for each document type.

This folder answers:
**“What are the technical standards this skill must obey?”**

Typical contents include:

* standards for README, SPEC, ADR, Reference, Guide, Playbook, Roadmap
* documentation architecture rules
* taxonomy / decision tables
* graph and linking conventions

---

## How this skill is meant to be used

The Documentation Librarian is meant to be used:

* **before** creating documentation
  → to choose the correct document type and structure
* **during** updates
  → to limit scope and prevent accidental rewrites
* **after** changes
  → to verify consistency across related documents

It works best when paired with:

* coding agents
* planning agents
* review workflows

Example mental flow:

1. Something changed (code, behavior, decision)
2. The librarian identifies affected docs
3. It updates the **necessary subtree**, not just one file
4. It flags risks or missing context instead of guessing

---

## Why this exists

Most documentation fails not because it is badly written, but because:

* it drifts away from reality
* it contradicts itself
* it is rewritten instead of maintained
* its structure collapses under growth

This skill exists to prevent that.

It treats documentation like infrastructure:

* boring when it works
* painful when it breaks
* expensive to rebuild if neglected

---

## Important note

This README is **for humans only**.

The skill itself:

* does not reference this file
* does not depend on it
* should remain fully operational without it

Think of this README as a **map for maintainers**, not part of the machine.

---

## Status

Stable.
Designed to evolve **slowly and deliberately**, alongside its standards.
