# Retrofit Workflow

Most terminology work doesn't start from scratch. You inherit a system. The terminology is embedded in database schemas, API contracts, variable names, UI labels. It's inconsistent, undocumented, and load-bearing.

You can't throw it away because other things depend on it. You can't ignore it because it's causing problems. You have to work with it—understanding what exists, identifying what's wrong, and improving it without breaking what depends on it.

This document describes how.

## The Problem You're Facing

A legacy system's terminology wasn't designed. It accumulated. Different developers named things at different times with different mental models. The database uses `customer`. The API uses `client`. The UI uses `account`. Maybe they mean the same thing. Maybe they don't. The only way to know is to investigate.

The danger isn't that the terminology is inconsistent. The danger is that the inconsistency is invisible. Code works around it. People learn the quirks. New developers ask "why is this called X here and Y there?" and get the answer "it's always been that way." The cost is diffuse: longer onboarding, subtle bugs, meetings that go in circles because people are using the same words to mean different things.

Retrofit makes the inconsistency visible and then progressively fixes it.

## Phase 1: Inventory What Exists

Before you can fix anything, you need to know what's there.

### What to catalog

**Data layer:** Database tables and columns. Enum values. Foreign key names. Constraint names. Index names. Anything that encodes a concept in the schema.

**API layer:** Endpoint paths. Request field names. Response field names. Query parameters. Header names. Error codes. Anything a consumer sees.

**Code layer:** Class names. Variable names. Function names. Constants. Enum types. Module names. Comments that explain domain concepts.

**UI layer:** Labels. Button text. Error messages. Help text. Tooltips. Anything a user reads.

**Documentation layer:** Glossaries. Wiki pages. README files. Architecture docs. API documentation. Anything that attempts to explain what terms mean.

### How to do it

Start with the thing that's causing problems. If the problem is "we don't know what 'customer' means," search the codebase for `customer`, `client`, `user`, `account`, `buyer`—anything that might be related. Record where each term appears and how it's used.

Build a spreadsheet or structured file:

| Term | Location | Kind | Example usage |
|------|----------|------|---------------|
| customer | db: customers table | table name | stores purchasers |
| client_id | api: /orders response | field | references customers.id |
| user | ui: "Hello, {user}" | label | greeting in header |
| account | docs: glossary | definition | "an account is a customer or prospect" |

You're not analyzing yet. You're just recording what exists.

### Output

A terminology inventory: every place domain terms appear in the system, with enough context to understand each usage.

## Phase 2: Find the Conflations

A conflation is when one term or artifact tries to do two jobs.

### Types of conflation

**Axis conflation:** An enum that mixes different dimensions.

```
# Problem: mixes tracking mechanism and connection type
mouse_type: ['optical', 'mechanical', 'wireless', 'wired']
```

A wireless optical mouse can't be represented. The data model forces a false choice.

**Meaning conflation:** A field that means different things in different contexts.

```
# In the orders table, status means order lifecycle
orders.status: ['pending', 'shipped', 'delivered']

# In the users table, status means account state
users.status: ['active', 'suspended', 'deleted']
```

The same word points to different concepts. Code that handles "status" generically will break across contexts.

**Synonym collision:** Different terms that point to the same concept, used inconsistently.

```
# Database calls it customer_id
# API calls it client_id
# UI calls it account
# But they all mean the same thing
```

The inconsistency causes confusion. Which is canonical? What happens when they diverge?

**Implicit compound:** A single value that encodes multiple independent attributes.

```
# product_code: "WRL-OPT-ERG"
# encodes: wireless + optical + ergonomic
# can't query for "all wireless" without string parsing
```

The encoding is convenient until you need to query one dimension.

### How to find them

For each term in your inventory, ask:
- Is this term ever used to mean different things in different places?
- Does this field try to capture multiple independent attributes?
- Are there other terms that seem to mean the same thing?
- If I filter or group by this term, do the results make sense?

Flag anything suspicious. You don't need to resolve it yet—just identify it.

### Output

A conflation report: each problematic term or artifact, with a description of what's conflated and where the problem manifests.

## Phase 3: Build the Concept System as an Overlay

Now you know what exists and where it's broken. The next step is to build the correct structure—not by changing the system, but by describing what the system *should* represent.

### The overlay principle

The concept system exists alongside the implementation, not instead of it. You're not changing the database. You're documenting what the database should mean.

This separation is essential. The implementation is load-bearing. Changing it requires migration, testing, coordination with consumers. The concept system is documentation. You can revise it freely until it's right.

### How to build it

1. **Identify the parent concepts.** What is customer a kind of? What is order a kind of? Group your terms under their natural parents.

2. **Separate the axes.** Where your conflation report found axis mixing, create explicit axes. `mouse_type` becomes `tracking_mechanism` and `connection_type`.

3. **Define the siblings.** On each axis, what are the options? What distinguishes them?

4. **Write provisional definitions.** For each concept, state: what is its parent? What distinguishes it from siblings on its axis?

5. **Handle the compounds.** If your system has implicit compounds (like the product code encoding multiple attributes), make them explicit. A wireless optical mouse is the intersection of `wireless` on the connection axis and `optical` on the tracking axis.

### Output

A vocabulary package representing the target state—the concept system that the implementation *should* express, even though it currently doesn't.

## Phase 4: Build the Mapping Ledger

The concept system is correct. The implementation is what it is. The mapping ledger connects them.

### What mappings capture

For each concept, record every place it's implemented:

| Concept | Implementation | Mapping Type | What's Lost |
|---------|---------------|--------------|-------------|
| optical mouse | mouse_type='optical' | partial | conflated with connection axis |
| wireless mouse | mouse_type='wireless' | partial | conflated with tracking axis |
| active customer | is_active=true | exact | nothing |
| churned customer | is_active=false | lossy | conflated with paused |
| paused customer | is_active=false | lossy | conflated with churned |

### Mapping types

**exact:** The concept and the implementation represent the same thing. No information loss.

**partial:** The implementation contains this concept but also other things. The concept maps to part of the artifact.

**composite:** Multiple concepts combine into one implementation artifact. You lose the ability to query them independently.

**derived:** The implementation is computed from the concept rather than stored directly. The concept exists in logic, not storage.

**lossy:** Information is lost in the mapping. You can't recover the full concept from the implementation alone.

### Why this matters

The mapping ledger is your bug map. Every lossy or partial mapping is a place where code might do the wrong thing. Every composite mapping is a place where you can't answer a question without extra work.

When someone asks "why can't we filter orders by customer type?" the answer is in the ledger: customer type isn't stored separately, it's conflated with something else, and the mapping is lossy.

### Output

A complete mapping from every concept to every place it touches the implementation, with explicit notes on what's compromised.

## Phase 5: Introduce Semantic Accuracy at the Interface

You can't change the database without migration. But you can change the API. You can change the UI. You can change new code.

### The strategy

Let the storage stay broken. Make the interfaces correct. Use a translation layer to bridge them.

**New API versions:** Expose semantically correct fields. `tracking_mechanism` and `connection_type` instead of `mouse_type`. The new API speaks the concept system's language.

**Legacy API support:** Keep the old endpoints working. Map from new storage concepts to old response shapes. Consumers who don't upgrade keep working.

**Translation layer:** One place in the code that converts between semantic representation and storage representation. All the ugly mapping logic lives here, not scattered through the codebase.

```python
# Translation layer
def to_storage(tracking: str, connection: str) -> dict:
    # Semantic to legacy: combine into single field
    # This is where we acknowledge the lossy mapping
    if tracking in ['optical', 'mechanical', 'laser']:
        return {'mouse_type': tracking}
    elif connection in ['wireless', 'wired']:
        return {'mouse_type': connection}
    else:
        raise ValueError("Cannot map to legacy storage")

def from_storage(mouse_type: str) -> dict:
    # Legacy to semantic: derive what we can
    if mouse_type in ['optical', 'mechanical', 'laser']:
        return {'tracking_mechanism': mouse_type, 'connection_type': None}
    elif mouse_type in ['wireless', 'wired']:
        return {'tracking_mechanism': None, 'connection_type': mouse_type}
```

The translation layer makes the compromise explicit. The `None` values show where information is lost. Consumers of the semantic API see what's known and what isn't.

### Output

Semantic interfaces (APIs, UIs) that speak the concept system's language, plus a translation layer that maps to the legacy implementation.

## Phase 6: Detect Logic-Level Conflations

The hardest conflations aren't in the data model. They're in the code.

### What logic-level conflation looks like

The `mouse_type` field is checked in 47 places across the codebase. In 30 of them, the code correctly handles the tracking mechanism values. In 12 of them, the code correctly handles the connection values. In 5 of them, the code switches on all four values in ways that don't make sense—treating "optical" and "wireless" as if they're alternatives when they're actually orthogonal.

The data model conflation is visible in the schema. The logic conflation is hidden in code that no one has read in two years.

### How to find it

Build a usage index:

1. Find every place the problematic field is read.
2. For each read, determine what the code assumes about the values.
3. Classify each usage by which axis it actually cares about.

| Location | Operation | Assumed Axis | Problem? |
|----------|-----------|--------------|----------|
| MouseService.isOptical() | read | tracking | no |
| MouseService.isWireless() | read | connection | no |
| MouseService.getCategory() | read | both | yes—switches on all values |
| MouseReport.groupByType() | read | unclear | yes—groups mix axes |

The places marked "yes" are bugs waiting to happen. They work by accident—because no one has created a wireless optical mouse in production yet—but they encode incorrect assumptions.

### Output

A semantic trace matrix: every place the conflated field is used, with an assessment of what the code actually assumes.

## Phase 7: Migrate Storage Only When Stable

Now you have:
- A concept system describing correct meaning
- A mapping ledger showing where meaning is compromised
- Semantic interfaces that speak correct terminology
- A trace of logic-level conflations

You *could* fix the database. But should you?

### When to migrate

Migrate storage when:
- The concept system is stable (hasn't changed in two or more cycles)
- The mapping ledger is stable (not growing with new lossy entries)
- The translation layer is handling all cases (no bugs from the legacy representation)
- The cost of maintaining the translation layer exceeds the cost of migration

Don't migrate storage when:
- The concept system is still evolving
- You keep finding new conflations
- Consumers aren't ready for the change
- The legacy system is being replaced anyway

### How to migrate

1. **Add new columns.** Don't remove old ones yet. `tracking_mechanism VARCHAR, connection_type VARCHAR` alongside `mouse_type`.

2. **Backfill.** Derive new column values from old column. Use the same logic as your translation layer.

3. **Validate.** Check that round-trip works: old → new → old produces the same result.

4. **Switch reads.** Point application code at new columns.

5. **Switch writes.** Write to new columns as source of truth.

6. **Deprecate.** Mark old column as deprecated. Stop writing to it.

7. **Remove.** After all consumers have migrated, drop the old column.

Each step is reversible until step 7. If something goes wrong, you can fall back to the old column.

### Output

A migrated schema that directly represents the concept system, with the translation layer eliminated or simplified.

## What Success Looks Like

At the end of a retrofit:

- The concept system documents what each term means and how terms relate.
- The mapping ledger shows exactly where meaning and implementation diverge.
- Semantic interfaces let new code speak correct terminology.
- The translation layer contains all the legacy compromise in one place.
- Logic-level conflations are identified and queued for fix.
- Storage is either migrated or documented as technical debt with a clear cost.

The system isn't perfect. But the imperfection is visible. You know where the problems are, what they cost, and what it would take to fix them. That's the difference between inherited mess and managed technical debt.
