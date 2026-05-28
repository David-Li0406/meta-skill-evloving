---
name: c4-architecture
description: Use this skill when you need to generate architecture documentation using C4 model Mermaid diagrams, including context, container, component, and deployment diagrams.
---

# C4 Architecture Documentation

Generate software architecture documentation using C4 model diagrams in Mermaid syntax.

## Workflow

1. **Understand scope** - Determine which C4 level(s) are needed based on audience.
2. **Analyze codebase** - Explore the system to identify components, containers, and relationships.
3. **Generate diagrams** - Create Mermaid C4 diagrams at appropriate abstraction levels.
4. **Document** - Write diagrams to markdown files with explanatory context.

## C4 Diagram Levels

Select the appropriate level based on the documentation need:

| Level | Diagram Type | Audience | Shows | When to Create |
|-------|--------------|----------|-------|----------------|
| 1     | **C4Context** | Everyone | System + external actors | Always (required) |
| 2     | **C4Container** | Technical | Apps, databases, services | Always (required) |
| 3     | **C4Component** | Developers | Internal components | Only if adds value |
| 4     | **C4Deployment** | DevOps | Infrastructure nodes | For production systems |
| -     | **C4Dynamic** | Technical | Request flows (numbered) | For complex workflows |

**Key Insight:** "Context + Container diagrams are sufficient for most software development teams." Only create Component/Code diagrams when they genuinely add value.

## Quick Start Examples

### System Context (Level 1)
```mermaid
C4Context
  title System Context - Workout Tracker

  Person(user, "User", "Tracks workouts and exercises")
  System(app, "Workout Tracker", "Vue PWA for tracking strength and CrossFit workouts")
  System_Ext(browser, "Web Browser", "Stores data in IndexedDB")

  Rel(user, app, "Uses")
  Rel(app, browser, "Persists data to", "IndexedDB")
```

### Container Diagram (Level 2)
```mermaid
C4Container
  title Container Diagram - Workout Tracker

  Person(user, "User", "Tracks workouts")

  Container_Boundary(app, "Workout Tracker PWA") {
    Container(spa, "SPA", "Vue 3, TypeScript", "Single-page application")
    Container(pinia, "State Management", "Pinia", "Manages application state")
  }
```