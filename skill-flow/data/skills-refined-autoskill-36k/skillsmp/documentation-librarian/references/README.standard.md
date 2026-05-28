# README.standard.md — Repository Entry Standard

## Purpose

The README is the **front door**. It explains what the project is, who it’s for, what it does (and does not), and where to go next.

## Audience

* New contributors
* Evaluators (someone deciding whether to use or contribute)
* Returning contributors who need quick orientation

## Source of truth

* The repository itself (current behavior, current scope)
* Links to **Specs / Reference** for authoritative details

## Required sections (in this order)

1. **Title + one-line summary**
2. **What this is**

   * problem solved, target users, key outcomes
3. **What this is not**

   * explicit non-goals and boundaries
4. **Status**

   * stability level (MVP/Beta/Stable), active development signals
5. **Quick start**

   * minimal commands/steps to run
   * environment assumptions (Node version, required tooling)
6. **Key concepts (brief)**

   * 3–8 bullets max; link deeper docs
7. **Documentation map**

   * links to Guides, Specs, Reference, Playbooks, Roadmap, ADR index
8. **Contributing (short)**

   * link to CONTRIBUTING.md or section
9. **License**
10. **Support / Contact**

    * where issues/discussions live

## Allowed content

* High-level architecture diagram (optional)
* Minimal examples (only if stable)
* Links to authoritative docs

## Forbidden content

* Deep business rules (belongs in SPEC)
* Full API docs (belongs in Reference)
* Long tutorials (belongs in Guides)
* Historical rationale (belongs in ADRs)

## Maintenance rules

* Keep “Quick start” in sync with reality.
* If README contradicts SPEC/Reference, **README is wrong**.
* Prefer linking to deeper docs over expanding README.

## Quality checklist

* A new dev can run it in < 10 minutes.
* Scope and non-goals are explicit.
* Next docs to read are obvious.
* No contradictory claims.

## Common failure modes

* README becomes a dumping ground
* “Quick start” rots
* Vague scope and hidden assumptions
