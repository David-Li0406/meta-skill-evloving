# REFERENCE.standard.md — API / Types / Configuration Reference Standard

## Purpose

Reference docs are **factual and exact**. They define interfaces, inputs/outputs, configuration keys, and behaviors precisely.

## Audience

* Engineers integrating or maintaining
* Tooling and automation authors

## Source of truth

* Code and schema definitions
* Public API surface / exported types / config schema

## Required properties

* Precise, unambiguous language
* Stable headings and anchors
* Examples that match reality

## Recommended structure (choose what applies)

1. **Scope**
2. **Versioning / Stability notes**
3. **API / Interface**

   * endpoints, functions, events, CLI commands
4. **Types / Schemas**
5. **Parameters / Fields**

   * name, type, required?, default, constraints
6. **Responses / Outputs**
7. **Errors**

   * codes, conditions, meanings
8. **Examples**

   * minimal, correct
9. **Compatibility**

   * breaking changes, deprecations

## Allowed content

* Tables, schema blocks, minimal examples

## Forbidden content

* Long narrative “why” (ADRs)
* Workflow instructions (Guides)
* Design proposals (SPEC)
* Incident procedures (Playbooks)

## Maintenance rules

* If Reference contradicts code, Reference must be updated immediately.
* Prefer deriving from a single source (schema/type definitions) rather than duplicating.
* Clearly mark deprecated fields and replacement paths.

## Quality checklist

* Everything is testable/implementable.
* No vague terms (“sometimes”, “usually”) without conditions.
* Errors are documented.

## Common failure modes

* Reference becomes a tutorial
* Missing constraints → integrations break
* Examples drift from reality
