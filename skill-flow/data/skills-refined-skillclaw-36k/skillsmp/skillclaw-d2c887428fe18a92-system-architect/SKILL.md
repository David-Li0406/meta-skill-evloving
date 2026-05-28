---
name: system-architect
description: Use this skill when you need expert guidance on software architecture, system design, and technical planning, especially regarding scalability, refactoring, and code organization.
---

# Skill body

This skill provides AI-powered architectural guidance for designing, planning, and improving software systems with a focus on maintainability, scalability, and clean code principles.

## Key Capabilities:
- **System Design**: Create architecture diagrams, component designs, and API plans.
- **Code Organization**: Structure modules, ensure separation of concerns, and implement layered architectures.
- **Pattern Selection**: Identify and apply design patterns, architectural patterns, and detect anti-patterns.
- **Dependency Management**: Analyze coupling, design interfaces, and implement dependency injection.
- **Tech Debt Assessment**: Evaluate code health, prioritize refactoring, and develop migration strategies.
- **Scalability Planning**: Consider performance, caching strategies, and design for distributed systems.

## Core Principles

### The SOLID Foundation
- **S**ingle Responsibility: Each module/class should have one reason to change.
- **O**pen/Closed: Open for extension, closed for modification.
- **L**iskov Substitution: Subtypes must be substitutable for base types.
- **I**nterface Segregation: Prefer many specific interfaces over one general interface.
- **D**ependency Inversion: Depend on abstractions, not concretions.

### Architectural Qualities
1. **Maintainability**: Code should be easy to understand and modify.
2. **Testability**: Components should be testable in isolation.
3. **Scalability**: Systems should grow gracefully under load.
4. **Resilience**: Systems should degrade gracefully under failure.
5. **Evolvability**: Systems should adapt to changing requirements.

## Architecture Assessment Workflow

### 1. Initial Analysis
```
Analyze the current system:
├── Structure (directories, modules, packages)
├── Dependencies (internal and external)
├── Data Flow (how information moves)
├── Integration Points (APIs, databases, services)
└── Pain Points (what causes friction)
```

### 2. Architecture Metrics
- **Coupling Score**: Measure how tightly connected components are.
- **Cohesion Score**: Assess how focused individual components are.
```
```