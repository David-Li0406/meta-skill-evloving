# Validation Rules

Validation exists because structural problems in a concept system manifest as bugs downstream. A missing parent reference is not just a schema violation—it means a definition doesn't actually position the concept in the hierarchy. A cross-axis contamination isn't just a data error—it means a definition conflates dimensions that should be independent.

Each rule here catches a specific failure mode. Understanding the failure mode tells you whether the rule matters for your situation and what to do when it fails.

## The Rules

### R1: Identifiers Must Be Unique

**What it checks:** No two entities of the same type share an ID.

**Why it matters:** Identifiers are how everything else refers to things. If two concepts share an ID, you can't know which one a relation points to. Queries become ambiguous. Merges become impossible. The entire reference system breaks.

**What to do when it fails:** Find the duplicates. Decide which is canonical. Rename or merge the other.

### R2: Relation Targets Must Exist

**What it checks:** Every `sourceId` and `targetId` in a relation points to a concept that exists.

**Why it matters:** A relation to nothing is a broken link. If you try to traverse the concept system—find ancestors, find siblings, visualize the graph—you'll hit a dead end. Worse, you might not notice: the missing target just silently vanishes from results.

**What to do when it fails:** The relation references something that doesn't exist. Either the concept was deleted and the relation should be deleted too, or the concept was never created and should be. Trace back to find out which.

### R3: Axis and Characteristic References Must Exist

**What it checks:** Every `axisId` in a definition, relation, or characteristic points to an axis that exists. Every `delimitingCharacteristicId` points to a characteristic that exists.

**Why it matters:** Axes and characteristics are the vocabulary you use to describe the structure. Referencing a nonexistent axis is like using a word that has no definition—it looks meaningful but points to nothing. Code that tries to validate axis consistency will fail when it encounters the dangling reference.

**What to do when it fails:** Either the axis/characteristic was deleted and references should be cleaned up, or it was never defined and should be.

### R4: Axis-Scope Definitions Must Have Parents

**What it checks:** If a definition has `scope: 'axis'` or a non-null `axisId`, it must have a `parentId`.

**Why it matters:** A definition's job is to position a concept in the system. Axis-scope means "this concept is a kind of something, distinguished on this axis." Without a parent, the definition says "this is a kind of... nothing." It doesn't position anything.

The failure mode is subtle. The definition might read correctly as English: "optical mouse: a mouse that uses light sensors." But structurally, it's not connected to the hierarchy. You can't find siblings. You can't check that siblings are on the same axis. The concept floats free.

**What to do when it fails:** Add the parent. If you don't know what the parent is, that's the real problem—you haven't positioned the concept yet.

### R5: Parents Must Exist

**What it checks:** If a definition has a `parentId`, that ID must point to a concept in the package.

**Why it matters:** Same as R2, but for the most important relation: the parent-child link that defines the hierarchy.

**What to do when it fails:** Same as R2. Find out what happened to the parent.

### R6: Root Definitions Have No Parent

**What it checks:** If a definition has `scope: 'root'`, it must not have a `parentId`.

**Why it matters:** Root means "top of hierarchy." If a root concept claims a parent, it contradicts itself. The concept can't be both the top and a child of something.

**What to do when it fails:** Decide whether the concept is actually a root. If it has a real parent, change the scope to `axis`. If it's truly a root, remove the parentId.

### R7: No Cross-Axis Contamination

**What it checks:** If a definition has an `axisId`, all its `delimitingCharacteristicIds` must belong to that axis.

**Why it matters:** This is the structural rule that prevents the most common terminology bug.

A definition says "this concept differs from its siblings on this axis by these characteristics." If the characteristics belong to a different axis, the definition doesn't distinguish siblings—it mixes dimensions.

Example: If optical mouse is defined on the tracking axis, its delimiting characteristic should be about tracking (light sensors, ball, laser). If the definition includes "wireless" (a connection characteristic), you've contaminated the tracking-axis definition with connection-axis information.

This matters because the definition's job is to answer: "what makes this concept different from its siblings?" Siblings on the tracking axis are optical, mechanical, laser. Wireless isn't a sibling—it's on a different axis. Including it confuses the question the definition is supposed to answer.

**What to do when it fails:** You've mixed axes. Either the characteristic belongs to a different axis than the definition, or the characteristic is assigned to the wrong axis, or the definition is on the wrong axis. Trace back to figure out which.

### R8: Stable Concepts Need Definitions

**What it checks:** Every concept with `status: stable` has at least one definition.

**Why it matters:** Stable means "this concept is ready for downstream use." A concept without a definition is just a name. Downstream systems can't know what it means because you haven't said.

The failure mode: someone marks a concept stable because they're done working on it, not because it's actually defined. Consumers start depending on the concept. When someone finally writes the definition, it might not match how consumers interpreted the name. The stable status promised something the package didn't deliver.

**What to do when it fails:** Either write the definition or change the status to draft/provisional.

### R9: Stable Concepts Should Have Siblings

**What it checks:** Every stable concept with an axis-scope definition should have at least one sibling—another concept with the same parent on the same axis.

**This is a warning, not an error.** Single-child hierarchies are sometimes intentional.

**Why it matters:** A concept's meaning comes from what it's distinguished from. "Optical mouse" means something because it contrasts with "mechanical mouse" and "laser mouse." If optical mouse is the only child of "computer mouse" on the tracking axis, the axis isn't doing any work. The definition says "distinguished by light sensors"—distinguished from what?

Single-child hierarchies often indicate incomplete modeling. You identified one kind but not its siblings. Or you created an axis that only has one value, which means it's not really a subdivision.

**What to do when it warns:** Ask whether the concept really has no siblings. If it does, add them. If it genuinely doesn't—if this is the only kind—consider whether the axis is meaningful. A single-value axis might be overengineering.

### R10: Compound Concepts Need Multiple Components

**What it checks:** A concept with `kind: compound` has at least two components.

**Why it matters:** A compound is an intersection of axes. One component isn't an intersection—it's just a single-axis concept that's been mislabeled.

**What to do when it fails:** Either add the missing component or change the kind to atomic.

### R11: Compound Components Must Be on Distinct Axes

**What it checks:** A compound concept's components don't share the same axis.

**Why it matters:** A compound is "X on axis A *and* Y on axis B." If both components are on the same axis, you're saying "X on axis A and Y on axis A"—but a concept can only be one thing on each axis. You can't be both optical and mechanical on the tracking axis.

This usually means confusion about what a compound represents. A compound isn't "one of these two options." It's "this option on axis A combined with that option on axis B."

**What to do when it fails:** Figure out what you actually meant. If the components are alternatives, you don't have a compound—you have a concept with multiple possible values (which the schema doesn't model). If the components are genuinely on different dimensions, fix the axis assignments.

### R12: Compound Component References Must Exist

**What it checks:** Each component's `conceptId` and `axisId` point to things that exist.

**Why it matters:** Same as R2 and R3. Broken references break the structure.

### R13: Compound Definitions Should Use Multi Scope

**What it checks:** A compound concept has at least one definition with `scope: multi`.

**This is a warning, not an error.**

**Why it matters:** Compounds inherit from their components, but they may also need their own definitions—especially if the combination has emergent properties. A `multi` scope definition acknowledges that the concept spans multiple axes.

### R14: No Self-Referential Relations

**What it checks:** A relation's source and target are not the same concept.

**Why it matters:** A concept can't be a kind of itself, part of itself, or related to itself. Self-reference is always a data error.

### R15: Associative Relations Should Have Labels

**What it checks:** Relations with `type: associative` have a `label` explaining the relationship.

**This is a warning, not an error.**

**Why it matters:** Generic relations (kind-of) and partitive relations (part-of) are self-explanatory. Associative relations aren't—"related to" could mean anything. The label says what kind of relationship: controls, produces, causes, uses.

Without a label, the relation records that two concepts are connected but not how. That's usually not useful enough to be worth recording.

### R16: No Duplicate Relations

**What it checks:** No two relations have the same type, source, target, and axis.

**This is a warning, not an error.**

**Why it matters:** Duplicates don't break anything, but they indicate either a mistake (added twice by accident) or inconsistent tooling (merge didn't dedupe). They add noise to queries and visualizations.

### R17: Mapping Concepts Must Exist

**What it checks:** Every mapping's `conceptId` points to a concept that exists.

**Why it matters:** A mapping connects a concept to its implementation. If the concept doesn't exist, the mapping is orphaned—it documents how to implement something that isn't defined.

### R18: Lossy Mappings Should Document the Loss

**What it checks:** Mappings with `mappingType: lossy` have notes explaining what's lost.

**This is a warning, not an error.**

**Why it matters:** The whole point of recording a lossy mapping is to make the loss visible. If the notes are empty, the mapping says "something is lost" but not what. That's not useful for debugging or migration planning.

### R19: Concept Labels Must Exist

**What it checks:** Every concept has a non-empty `prefLabel`.

**Why it matters:** A concept without a label has no human-readable name. You can reference it by ID, but no one can talk about it. This is usually a data entry error—someone created the concept but forgot the label.

### R20: Orphan Concepts

**What it checks:** Every non-root concept has at least one incoming generic or partitive relation.

**This is a warning, not an error.**

**Why it matters:** A non-root concept should be a child of something. If nothing points to it as a child, it's floating free—not connected to the hierarchy.

This can be intentional (a concept awaiting positioning) or an error (the relation was deleted but the concept wasn't). The warning flags it for review.

## Severity Levels

**ERROR:** Structural violation that will cause downstream failures. Must fix before using the package.

**WARNING:** Potential issue that may be intentional. Review and either fix or document why it's acceptable.

## Running Validation

```bash
python scripts/validate_vocab.py vocab.json           # Errors fail, warnings print
python scripts/validate_vocab.py vocab.json --strict  # Errors and warnings both fail
python scripts/validate_vocab.py vocab.json --format json  # Machine-readable output
```

Validate on every change. Errors block release. Warnings require explicit acknowledgment.

## What Validation Can't Check

These rules check structure. They can't check meaning.

**Semantic correctness:** Is the definition actually true? Does "optical mouse" really mean what the definition says? Validation can check that the definition has a parent and uses the right-axis characteristics. It can't check that the definition reflects reality.

**Completeness:** Are all the concepts that should exist present? Validation can check that referenced concepts exist. It can't check that you've modeled the whole domain.

**Usage accuracy:** Does the code use these concepts correctly? Validation checks the package. It doesn't check the code that consumes it.

Structural validation catches a class of errors—the ones that can be detected from shape alone. Semantic validation requires human review.
