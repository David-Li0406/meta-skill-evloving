# ROADMAP.standard.md — Roadmap Standard

## Purpose

Roadmaps align expectations about **direction, scope, and sequencing**. They are not promises; they are communicated intent with constraints.

## Audience

* Stakeholders
* Contributors planning work
* Anyone assessing upcoming changes

## Source of truth

* Strategy + confirmed constraints (capacity, dependencies)
* SPECs/ADRs for committed technical direction

## Required sections

1. **Time horizon**

   * e.g., Now / Next / Later, or quarters
2. **Scope framing**

   * what is in, what is explicitly out
3. **Themes / Initiatives**

   * grouped outcomes, not a raw task list
4. **Milestones**

   * entry criteria + exit criteria
5. **Dependencies**

   * internal/external
6. **Risks**
7. **Status**

   * current truth: planned / in progress / blocked / shipped
8. **Links**

   * to Specs, epics, issues, ADRs

## Style rules

* Prefer outcome language over feature lists.
* Use clear status labels and keep them current.
* Avoid invented dates. If dates exist, mark confidence level.

## Allowed content

* Simple timeline, Now/Next/Later, confidence markers

## Forbidden content

* Detailed implementation steps (Guides/Playbooks)
* Undecided decisions presented as committed truth

## Maintenance rules

* Roadmap drift is a defect; update when reality changes.
* If an item is exploratory, label it.
* Do not let “Later” become a graveyard; prune and re-evaluate.

## Quality checklist

* Stakeholders can tell what’s truly planned vs aspirational.
* Dependencies and risks are visible.
* Milestones have criteria.

## Common failure modes

* Roadmap as wish list
* Fake certainty (dates without capacity)
* No explicit “out of scope”
