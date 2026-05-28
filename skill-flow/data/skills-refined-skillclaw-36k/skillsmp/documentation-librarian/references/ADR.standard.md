# ADR.standard.md — Architecture Decision Record Standard

## Purpose

An ADR captures **why** a decision was made: context, options, the chosen path, and its consequences. ADRs preserve organizational memory.

## Audience

* Current and future engineers
* Reviewers assessing design tradeoffs

## Source of truth

* The ADR itself for rationale
* SPEC/Reference for current implementation contracts

## Core rule

**ADRs are append-only history.**
Do not rewrite old ADRs to match current taste. If a decision changes, create a new ADR that supersedes the old one.

## Naming + location

* `docs/adr/NNNN-short-title.md`
* NNNN is sequential (0001, 0002, …)

## Required sections

1. **Title**
2. **Status**

   * Proposed | Accepted | Deprecated | Superseded
3. **Context**
4. **Decision**
5. **Alternatives considered**

   * with brief pros/cons
6. **Consequences**

   * positive, negative, neutral
7. **Links**

   * SPEC, PRs, issues, related ADRs

## Allowed content

* Small code snippets illustrating the decision
* Decision constraints and explicit assumptions

## Forbidden content

* Full technical design (SPEC)
* How-to instructions (Guides)
* Operational response instructions (Playbooks)

## Quality checklist

* The decision is unambiguous.
* Alternatives are real (not strawmen).
* Consequences include downsides.
* Links connect the decision to artifacts.

## Common failure modes

* ADR becomes a design doc
* “Status” missing → no one knows if it’s real
* Rewriting history instead of superseding
