---
name: domain-driven-design
description: Use this skill when asked to make changes to or reason about a domain capability, handler, query, command, action, model, or service.
---

# Skill body

## Meaning of "Domain"

A domain is a conceptual boundary -- a slice of the system that represents a stable idea, not a specific instance or a collection of instances. Domains are named with **singular nouns** because they model concepts, not lists.

A **domain**...

- contains unversioned logic and entities
- evolves independently from API surfaces (which are versioned)
- provides action pathways for users to interact with domain objects

Think of a domain path like `organization.building.device.io` as a chain of nested concepts, each narrowing the scope of meaning. It's not describing "many organizations" or "many buildings" -- it's describing the conceptual space where each capability lives.

## Meaning of "Capability"

A **capability**...

- is a domain subsystem
- is a cohesive set of domain behaviors centered around a single domain concept
- comprises a set of operations (commands, queries)
- contains services that encapsulate domain logic
- evolves with the domain concept
- applies the Single Responsibility Principle
- should not exist without at least one action
- is created automatically when the first action within it is created

**Example:**

```text
cyberdyne/           <- domain
  skynet/            <- domain
    defense/         <- capability
      fire_nukes/    <- action
        command.py   <- action shape
        handler.py   <- execution logic
```

### General rule for extracting capabilities from paths

Given a domain path like: `internal.network.devices.execute`

Use this rule:

> Find the last noun before the verb

That noun (`devices`) is the capability.

Everything before the verb is the capability path.

Verbs tend to be like:

```text
audit
configure
create
delete
execute
export
get
import
list
monitor
provision
render
reporting
sync
update
```

## Meaning of "Stable Entity"

A **stable** entity...

- is a *simple* entity
- exists in a domain and has no exposed actions
- is not *capable*

In REST terms, it is a **resource**.

**Example:**

```text
cyberdyne/           <- domain
  skynet/            <- domain
    weapon/          <- capability
      nuke/          <- entity
        entity.py    <- entity shape
        rules.py     <- validation logic
```

## Meaning of "Capable Entity"

A **capable** entity...

- is a *complex* entity
- exists in a domain and exposes actions
- is capable of performing operations defined by its domain