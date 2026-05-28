# GUIDE.standard.md — How-To & Tutorial Standard

## Purpose

Guides teach someone **how to accomplish a task**. They are procedural, user-oriented, and practical.

## Audience

* Users and contributors executing tasks (setup, workflows, usage patterns)

## Source of truth

* Working behavior of the system
* Playbooks for operational tasks (when relevant)
* Reference for exact API/config details

## Required sections

1. **Goal**

   * what the reader will achieve
2. **Prerequisites**

   * required tools, access, prior knowledge
3. **Steps**

   * numbered, explicit, reproducible
4. **Verification**

   * how to confirm it worked
5. **Troubleshooting**

   * common failure points + fixes
6. **Next steps**

   * links to deeper docs / related guides

## Style rules

* Use imperative voice: “Run…”, “Create…”, “Verify…”
* Prefer small steps with explicit expected outputs.
* Include examples, but keep them minimal and correct.

## Allowed content

* Screenshots / snippets (if stable)
* “Why this matters” (short, optional)

## Forbidden content

* Normative contracts (belongs in SPEC)
* Exhaustive API listing (belongs in Reference)
* Operational incident response (belongs in Playbooks)

## Maintenance rules

* If steps diverge from reality, update immediately.
* Split guides when they exceed ~15 minutes to follow.
* Link to reference instead of duplicating definitions.

## Quality checklist

* A reader can follow without guessing.
* Verification steps exist.
* Troubleshooting covers the top 3 breakpoints.
* No contradictions with SPEC/Reference.

## Common failure modes

* Mixing tutorial with specification
* Too much narrative, too few steps
* Missing verification (reader can’t tell if it worked)
