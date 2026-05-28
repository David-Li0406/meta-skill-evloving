# MANIFESTO.standard.md — Manifesto Standard

## Purpose

A manifesto is a **strongly opinionated declaration** of intent and worldview for a domain (e.g., “Color Manifesto”). It is motivational, but must remain coherent, constrained, and non-contradictory.

## Audience

* Internal team (alignment)
* External readers (positioning)
* Future maintainers (why this approach exists)

## Source of truth

* The philosophy and constraints the project commits to
* Must not contradict SPEC/ADR/Reference; if it does, the manifesto must be revised or scoped.

## Required sections

1. **Title + one-line thesis**
2. **Context**

   * what problem space this manifesto addresses
3. **Core claims**

   * 5–12 claims max, each:

     * Claim (bold)
     * Why it matters (short)
     * What it implies in practice (concrete)
4. **Boundaries**

   * what this manifesto is NOT claiming
5. **Tradeoffs**

   * what we accept losing by choosing this worldview
6. **Operational commitments**

   * how this manifesto shows up in day-to-day decisions
7. **Glossary**

   * only if required for precision
8. **References**

   * links to specs/ADRs/papers/docs that underpin claims (optional but recommended)

## Style rules

* Clear, crisp, slightly forceful language.
* Claims must be defensible. Avoid mystical wording.
* Prefer “we choose X because Y” over vague inspiration.

## Allowed content

* Narrative framing
* Domain arguments and persuasion
* Examples and illustrations

## Forbidden content

* Detailed implementation steps (Guides/Playbooks)
* API specifics (Reference)
* Hidden assumptions presented as facts

## Maintenance rules

* Manifestos can evolve, but changes must be intentional.
* When a claim changes meaningfully, add a brief changelog entry or link an ADR.

## Quality checklist

* Readers can summarize the thesis in one sentence.
* Claims lead to concrete implications.
* Boundaries and tradeoffs are explicit.

## Common failure modes

* Manifesto becomes marketing copy
* Too many claims → dilution
* Contradicting specs or reference docs
