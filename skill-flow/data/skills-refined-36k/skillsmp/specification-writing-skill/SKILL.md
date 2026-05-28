---
name: specification-writing-skill
description: This skill provides guidance for creating feature specifications in the Spec-Driven Development process.
---

# Specification Writing Skill

## Purpose
This skill provides guidance for creating feature specifications in the Spec-Driven Development process.

## Project Phases Structure
The project is organized into 5 distinct phases:

- **Phase 01**: Todo In-Memory Python Console App 
- **Phase 02**: Todo Full-Stack Web Application
- **Phase 03**: Todo AI Chatbot
- **Phase 04**: Local Kubernetes Deployment
- **Phase 05**: Advanced Cloud Deployment

## Specifications Folder Structure
```
specs/
├── phase-01/
│   ├── 001-<feature-name>/
│   │   └── spec.md
│   └── 002-<feature-name>/
│       └── spec.md
├── phase-02/
│   └── 001-<feature-name>/
│       └── spec.md
├── phase-03/
│   └── 001-<feature-name>/
│       └── spec.md
├── phase-04/
│   └── 001-<feature-name>/
│       └── spec.md
└── phase-05/
    └── 001-<feature-name>/
        └── spec.md
```

## Feature Specification Format
Each feature specification includes:
- Feature title and metadata
- User scenarios & testing (with priorities P1-P4)
- Functional requirements (FR-001 to FR-nn)
- Key entities
- Success criteria

## PHR Structure
Prompt History Records are stored in:
```
history/prompts/
├── phase-01/
│   ├── 001-todo-app/
│   │   └── <ID>-<slug>.<stage>.prompt.md
│   └── 002-<feature-name>/
│       └── <ID>-<slug>.<stage>.prompt.md
├── phase-02/
│   ├── 001-<feature-name>/
│   │   └── <ID>-<slug>.<stage>.prompt.md
│   └── 002-<feature-name>/
│       └── <ID>-<slug>.<stage>.prompt.md
└── general/
    └── <ID>-<slug>.general.prompt.md
```

## Naming Convention
- Feature branches: `{###}-{feature-name}` (e.g., `001-todo-app`)
- Spec directories: `phase-{nn}/{###}-{feature-name}` (e.g., `phase-01/001-todo-app`)
- PHR files: `{ID}-{slug}.{stage}.prompt.md` (e.g., `1-todo-app-created.spec.prompt.md`)

## Best Practices
1. Prioritize user stories with clear P1-P4 priorities
2. Define clear acceptance scenarios with Given/When/Then format
3. Document functional requirements with specific capabilities
4. Consider edge cases and error handling
5. Define measurable success criteria
