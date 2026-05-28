---
name: terminology-work
description: This skill should be used when the user asks to "standardize terminology", "define terms", "clean up naming", "create a glossary", "fix inconsistent naming", "build a concept system", "document domain terms", "create a vocabulary", "map concepts to code", or when naming inconsistencies are causing bugs, confusion, or communication failures in a codebase, API, database, or documentation.
---

# Terminology Work

## What This Skill Is For

Words fail silently. When two engineers say "user" and mean different things, they don't notice the disagreement. They build systems that encode their different assumptions. The systems work until they meet at an interface—an API call, a database join, a shared service—and then they fail in ways that are hard to diagnose because the failure looks like a bug but is actually a misunderstanding fossilized in code.

This skill provides a method for making the meanings of words explicit, consistent, and traceable from human understanding to machine representation.

## The Core Problem

A word like "customer" seems simple. But probe it and the simplicity dissolves:

- Is a customer someone who has purchased, or someone who might purchase?
- Is a business that buys through a reseller your customer, or is the reseller your customer?
- If someone's trial expired, are they still a customer?
- Is the person who pays the same as the person who uses the product?

These aren't edge cases. They're the normal state of terminology in any domain of sufficient complexity. The word exists; the shared understanding does not.

The failure mode is not that people disagree. Disagreement surfaces and gets resolved. The failure mode is that people *don't know they disagree*. They use the same word, assume shared meaning, and build systems that encode incompatible assumptions.

## Why Definitions Alone Don't Work

The instinct is to write definitions. But definitions written in isolation drift, contradict, and fail to distinguish.

A definition like "customer: a person or entity that purchases goods or services" seems clear until you need to decide: does it include someone who purchased once, three years ago, and never returned? Does it include someone whose purchase was refunded? The definition doesn't say, because the definition was written without reference to what "customer" needs to be distinguished from.

**The insight that makes terminology work tractable: a word's meaning is determined by what it excludes, not just what it includes.** "Customer" means something only in contrast to "prospect," "lead," "user," "subscriber," "account." The boundaries between these terms—where one ends and another begins—are where meaning lives.

This is why you must build the system of related terms before you write definitions. The system tells you what distinctions matter. The definitions record those distinctions.

## The Method

### 1. Name the problem you're solving

Terminology work can expand forever. Scope it by stating what's broken.

Bad: "We need to standardize our terminology."
Good: "The `customer` table, the `user` table, and the `account` table overlap in ways that cause bugs when services join across them. We need to know what each term means and how they relate."

The problem statement determines what's in scope. If the problem is about three tables, you work on the concepts those tables represent and their immediate neighbors. You don't boil the ocean.

**Output:** A sentence or two stating what confusion or failure you're trying to eliminate.

### 2. Collect the neighborhood, not just the term

A term that's causing problems is usually the surface sign of a confused neighborhood. The term "customer" is confusing because its relationship to "user," "account," "subscriber," "lead," "prospect," and "contact" is unclear.

Map the neighborhood:
- Terms that seem like synonyms (might be the same concept, might not)
- Terms that seem like siblings (different kinds of the same parent)
- Terms that seem like parts (components of a larger whole)
- Terms that seem related by process (one becomes another, one creates another)

At this stage, you're not defining. You're inventorying. Pull terms from code (table names, field names, enum values, class names), from documentation, from how people talk in meetings.

**Output:** A list of 5-20 terms that form the neighborhood around the problem.

### 3. Find the parent

Most confusion resolves when you identify what the confusing terms are *kinds of*.

If "customer," "prospect," and "lead" are all kinds of "party" (a general term for any person or organization you track), then the question becomes: what distinguishes a customer-party from a prospect-party from a lead-party?

If you can't find a parent, you may be looking at terms from different domains that accidentally share a word. "Account" in the authentication sense (a login credential) and "account" in the sales sense (a company you're selling to) have no shared parent—they're homonyms, not siblings.

**Output:** For each cluster of related terms, identify the parent concept they're all kinds of.

### 4. Find the axis of distinction

Here is where the hard thinking happens.

Siblings under a parent differ along some dimension. The dimension is called an axis. The axis is a type of characteristic you're using to divide the parent into kinds.

Example: "Computer mouse" can be divided into kinds along multiple axes:
- Tracking mechanism axis: optical, mechanical, laser
- Connection axis: wired, wireless
- Form factor axis: standard, ergonomic, trackball

Each axis produces a different set of siblings. On the tracking axis, optical and mechanical are siblings. On the connection axis, wired and wireless are siblings. These are independent dimensions—an optical mouse can be wired or wireless.

**The most common terminology bug is conflating axes.** An enum with values `{optical, mechanical, wireless, wired}` mixes two independent dimensions. You can't answer "what type is a wireless optical mouse?" because the enum can only hold one value. The data model encodes a false assumption: that tracking mechanism and connection type are the same dimension.

When you find your terms, ask: are these terms all varying along the same dimension, or am I accidentally mixing dimensions?

**Output:** For each set of siblings, name the axis that distinguishes them. If siblings are on different axes, separate them.

### 5. Write definitions that encode position in the system

A definition has a job: to tell you what this concept is and what it's not.

The form that does this job:

> [term]: [immediate parent] + [what distinguishes it from siblings on this axis]

Example:
> optical mouse: computer mouse (parent) whose movement is detected by light sensors (distinction from mechanical, which uses a ball)

The parent places the term in the hierarchy. The distinguishing characteristic separates it from its siblings. Together, they encode the term's position in the system.

**Do not include characteristics from other axes.** "Optical mouse" should not mention wired vs. wireless, because that's a different axis. An optical mouse can be either. Including connection information in the optical mouse definition conflates axes at the definition level, even if you kept them separate in the data model.

**Output:** One definition per term per axis. If a term appears on multiple axes (rare), it needs a definition for each position.

### 6. Handle compound concepts explicitly

Sometimes a term refers to an intersection of axes: "wireless optical mouse" is both wireless (connection axis) and optical (tracking axis).

Compounds are derived, not primary. They inherit from their components. A wireless optical mouse is a kind of optical mouse (on the tracking axis) and a kind of wireless mouse (on the connection axis).

Only materialize a compound as a first-class term when:
- The compound has a stable name in actual usage
- Systems need to store or transmit it as a single value
- The compound has properties beyond what you'd predict from its components

Most intersections don't need to be named. "Wired mechanical mouse" is a valid description, but if no one uses that phrase and no system stores it, you don't need a term for it.

**Output:** A list of compounds that are named in actual usage, with explicit links to their component terms.

### 7. Record mappings between meaning and implementation

The concept system describes meaning. But meaning must be implemented: stored in databases, transmitted through APIs, displayed in UIs.

Implementation has constraints that meaning doesn't. A database field has one type. An enum has a flat list of values. An API response has a fixed schema. These constraints often force you to lose information.

Example: Your concept system distinguishes "active customer" from "churned customer" from "paused customer." But your legacy database has a boolean `is_active` field. You can map active→true and churned→false, but where does paused go? You have to choose, and the choice loses information.

Record these mappings explicitly:

| Concept | Implementation | Mapping Type | What's Lost |
|---------|---------------|--------------|-------------|
| active customer | is_active=true | exact | nothing |
| churned customer | is_active=false | lossy | conflated with paused |
| paused customer | is_active=false | lossy | conflated with churned |

The mapping ledger is your record of where meaning is compromised by implementation. It tells you where bugs can hide, where migrations are needed, and what you're losing by not fixing it yet.

**Output:** A mapping from each concept to each place it's implemented, with notes on what's lost.

### 8. Validate the system, not just the definitions

A single definition can be well-formed but still wrong in context. Validation must check the system.

Structural checks (automatable):
- Every non-root term has a parent
- Every parent with children has at least two children (if you only have one child, you don't have a real distinction)
- No definition includes characteristics from a different axis
- All relation targets exist

Semantic checks (require human judgment):
- Does the parent actually generalize all its children?
- Do siblings actually contrast on the stated axis?
- Does the distinguishing characteristic actually distinguish, or is it true of siblings too?
- Does the definition match how the term is used in code and documentation?

The validation script in `scripts/validate_vocab.py` handles structural checks. Semantic checks require review.

**Output:** Validation passing, or a list of structural problems to fix.

### 9. Plan what happens when meanings change

Terminology is not static. Products evolve. Markets shift. The meaning of "customer" this year may not be the meaning next year.

When meaning changes, you need to know:
- What changed (which concept, what about it)
- What depends on the old meaning (which systems, which consumers)
- What they need to do (update their code, migrate their data, do nothing)

Major changes:
- Splitting a concept into multiple concepts
- Merging multiple concepts into one
- Moving a concept to a different parent
- Changing what distinguishes a concept from its siblings

These require migration support. See `references/migration-templates.md` for the manifest format.

Minor changes:
- Fixing a typo in a label
- Adding a synonym
- Adding examples or notes

These don't require migration.

**Output:** Versioned releases with migration manifests for breaking changes.

## When You're Working With a Legacy System

Most terminology work doesn't start from scratch. You inherit a database, an API, a codebase. The terminology is already embedded. It's inconsistent, undocumented, and load-bearing.

The retrofit workflow in `references/retrofit.md` addresses this:

1. **Inventory what exists.** Every table, field, enum, variable name, UI label, documentation term. This is your inherited terminology, even if no one designed it.

2. **Find the conflations.** Look for enums that mix axes, fields that mean different things in different contexts, names that are used inconsistently.

3. **Build the concept system as an overlay.** Don't change the implementation yet. Build Layer 1 (meaning) and Layer 2 (vocabulary package) as parallel structures. Map them to the existing implementation via the ledger.

4. **Introduce semantic accuracy at the interface layer.** New APIs can use correct terminology. New UI can use correct labels. A translation layer maps between the clean interface and the messy storage.

5. **Migrate storage only when stable.** When the concept system has stabilized and the mappings are well-understood, then consider schema changes. Not before.

The key insight: you can have semantic clarity in your head and in your documentation long before you have it in your database. The mapping ledger is what makes the gap between meaning and implementation visible and manageable.

## What This Skill Provides

### Core File

**SKILL.md** (this file): The method. When to use it, what problem it solves, how to do it.

### Reference Files

**`references/schema.md`**: The data model for vocabulary packages. How to represent concepts, axes, characteristics, definitions, relations, and mappings in JSON.

**`references/retrofit.md`**: The workflow for legacy systems. How to impose semantic structure without breaking production.

**`references/validation-rules.md`**: The 25 structural checks the validation script runs. What each checks, why it matters, what to do when it fails.

**`references/migration-templates.md`**: Templates for communicating breaking changes. Human-readable migration notes. Machine-readable migration manifests.

### Scripts

**`scripts/validate_vocab.py`**: Validates a vocabulary package against structural rules. Run it on every change.

### Examples

**`examples/pointing-devices.json`**: A complete vocabulary package for the "computer mouse" domain. Demonstrates axes, compounds, definitions, relations, and mappings.

## What This Skill Does Not Provide

**Social process for getting agreement.** Terminology work requires people to agree on what words mean. This skill gives you a structure for recording agreements. It does not give you a method for reaching them. That's facilitation, negotiation, and sometimes authority.

**Domain expertise.** The skill tells you how to structure terminology. It does not tell you what your terms should mean. You need people who understand the domain to decide that "customer" means X and not Y.

**Automated semantic validation.** The script checks structure. It cannot check whether your definitions actually match reality. A definition can be structurally valid and semantically wrong. Humans must review.

**Certainty.** Terminology work is iterative. You will discover that your initial concept system was wrong. That's not failure—it's the process working. The system is designed to be revised.
