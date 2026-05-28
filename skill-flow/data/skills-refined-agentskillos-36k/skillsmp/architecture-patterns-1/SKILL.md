---
name: architecture-patterns
description: A specialist skill that recognises and applies common software architecture patterns within a codebase. This skill should be used during the design and development phases of a project.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Architecture Patterns Skill

## Tooling Notes

This skill should only use read-only commands and avoid modifying files.

## Workflow

Copy this checklist and use it to track your progress through the performance optimisation process:

```markdown
Architecture Patterns Checklist

- [ ] Understand Requirements
  - [ ] Gather and analyse the functional and non-functional requirements of the project.
- [ ] Identify Suitable Patterns
  - [ ] Review common architecture patterns (e.g., MVC, Microservices, Layered, Event-Driven).
  - [ ] Select patterns that align with project requirements and constraints.
- [ ] Design Architecture
  - [ ] Create high-level diagrams illustrating the chosen architecture patterns.
  - [ ] Define components, their interactions, and data flow.
- [ ] Document trade-offs
  - [ ] Document the advantages and disadvantages of the selected patterns.
  - [ ] Justify the choice of patterns based on project needs.
- [ ] Review and Validate
```

## Appropriate Patterns

Here are some common software architecture patterns and their typical use cases:

- **Model-View-Controller (MVC)**: Suitable for web applications with a clear separation between data (Model), user interface (View), and business logic (Controller).
- **Layered Architecture**: Useful for applications that benefit from separation of concerns, with distinct layers for presentation, business logic, and data access.
- **Event-Driven Architecture**: Best for applications that need to respond to events asynchronously, such as real-time systems.

### MVC Pattern Diagram

```plaintext
┌───────────────┐
│     View      │  ← User Interface
└──────┬────────┘
       │
┌──────▼────────┐
│   Controller  │  ← Business Logic
└──────┬────────┘
       │
┌──────▼────────┐
│     Model     │  ← Data Management
└───────────────┘
```

### Layered Architecture Diagram

```plaintext
┌─────────────────────────────┐
│       Presentation          │  ← UI, API Controllers
├─────────────────────────────┤
│       Application           │  ← Use Cases, Services
├─────────────────────────────┤
│         Domain              │  ← Business Logic, Entities
├─────────────────────────────┤
│      Infrastructure         │  ← Database, External APIs
└─────────────────────────────┘
```

### Event Driven Architecture Diagram

```plaintext
┌───────────────┐      ┌───────────────┐
│   Event       │─────▶│   Event       │
│   Producer    │      │   Consumer    │
└───────────────┘      └───────────────┘
       │                      │
       │                      │
       ▼                      ▼
┌────────────────────────────────┐
│        Event Bus / Queue       │  ← Message Broker
└────────────────────────────────┘
```

## Decision Framework

When selecting architecture patterns, consider the following framework:

- **Scalability**: Will the pattern support future growth in users and data?
- **Maintainability**: Does the pattern facilitate easy updates and modifications?
- **Performance**: Will the pattern meet the performance requirements of the application?
- **Complexity**: Is the pattern appropriate for the complexity of the project, or does it introduce unnecessary overhead?
- **Team Expertise**: Does the development team have experience with the chosen patterns?

## Output Template

When documenting the architecture patterns applied, use the following template:

```markdown
# Decision Record: [What was decided]

## Project Overview

A brief summary of the project, its purpose, and main features.

## Options Considered

A list of architecture patterns considered for the project.

## Trade-offs

A detailed analysis of the advantages and disadvantages of each considered pattern.

## Decision

The chosen architecture.

## Consequences

A summary of the expected outcomes and any potential challenges associated with the chosen architecture.
```
