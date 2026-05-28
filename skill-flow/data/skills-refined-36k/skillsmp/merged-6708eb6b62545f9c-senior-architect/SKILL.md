---
name: senior-architect
description: Use this skill when designing scalable and maintainable software architectures, making technical decisions, or creating architecture diagrams.
---

# Senior Architect

Comprehensive toolkit for designing scalable and maintainable systems using modern technologies.

## Quick Start

### Main Capabilities

This skill provides several core capabilities through automated scripts:

```bash
# Script 1: Architecture Diagram Generator
python scripts/architecture_diagram_generator.py [options]

# Script 2: Project Architect
python scripts/project_architect.py [options]

# Script 3: Dependency Analyzer
python scripts/dependency_analyzer.py [options]
```

## Core Capabilities

### 1. Architecture Diagram Generator

Automated tool for generating architecture diagrams.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/architecture_diagram_generator.py <project-path> [options]
```

### 2. Project Architect

Comprehensive analysis and optimization tool for project architecture.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/project_architect.py <target-path> [--verbose]
```

### 3. Dependency Analyzer

Advanced tooling for analyzing project dependencies.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/dependency_analyzer.py [arguments] [options]
```

## System Design Considerations

### Core Competencies
- **Microservices vs. Monolith**: Evaluate trade-offs based on team size and domain complexity.
- **Event-Driven Architecture**: Use Pub/Sub for decoupling services.
- **Data Modeling**: Design schemas for relational and NoSQL databases.

### Code Organization
- **Monorepo Structure**: Organize shared packages and feature modules effectively.
- **Dependency Rules**: Enforce strict boundaries between layers.

### Cross-Cutting Concerns
- **Observability**: Implement consistent logging and tracing.
- **Security**: Centralize authentication and secret management.
- **Scalability**: Utilize caching strategies and database read replicas.

## Decision Framework

When evaluating a new technology or pattern:
1. **Problem Fit**: Does it solve a real problem?
2. **Cost**: What is the maintenance overhead?
3. **Team**: Does the team have the necessary skills?
4. **Lock-in**: How hard is it to replace later?

## Best Practices Summary

### Code Quality
- Follow established patterns and write comprehensive tests.
- Document decisions and review regularly.

### Performance
- Measure before optimizing and use appropriate caching.
- Optimize critical paths and monitor in production.

### Security
- Validate all inputs and use parameterized queries.
- Implement proper authentication and keep dependencies updated.

### Maintainability
- Write clear code with consistent naming and helpful comments.

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/project_architect.py .
python scripts/dependency_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues
Refer to the troubleshooting section in the technical documentation.

### Getting Help
- Review reference documentation and script output messages.
- Consult tech stack documentation and review error logs.

## Resources
- Architecture Patterns
- System Design Workflows
- Tech Decision Guide
- Tool Scripts