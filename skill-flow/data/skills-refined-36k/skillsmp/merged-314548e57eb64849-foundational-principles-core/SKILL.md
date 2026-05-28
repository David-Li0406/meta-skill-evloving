---
name: foundational-principles-core
description: Use this skill when building AI-powered development workflows based on foundational principles like TRUST 5, SPEC-First DDD, and modular architecture.
---

# Foundational Principles Core

Foundational principles and architectural patterns that power AI-driven development workflows.

Core Philosophy: Quality-first, test-driven, modular, and efficient AI development through proven patterns and automated workflows.

## Quick Reference

What is Foundational Principles Core?

Six essential principles that ensure quality, efficiency, and scalability in AI-powered development:

1. **TRUST 5 Framework** - Quality gate system (Test-first, Readable, Unified, Secured, Trackable)
2. **SPEC-First DDD** - Specification-driven domain-driven development workflow
3. **Delegation Patterns** - Task orchestration via specialized agents (never direct execution)
4. **Token Optimization** - 200K budget management and context efficiency
5. **Progressive Disclosure** - Three-tier knowledge delivery (Quick, Implementation, Advanced)
6. **Modular System** - File splitting and reference architecture for scalability

### Quick Access:

- Quality standards in `modules/trust-5-framework.md`
- Development workflow in `modules/spec-first-ddd.md`
- Agent coordination in `modules/delegation-patterns.md`
- Budget management in `modules/token-optimization.md`
- Content structure in `modules/progressive-disclosure.md`
- File organization in `modules/modular-system.md`
- Agent catalog in `modules/agents-reference.md`
- Command reference in `modules/commands-reference.md`
- Security and constraints in `modules/execution-rules.md`

### Use Cases:

- New agent creation with quality standards
- New skill development with structural guidelines
- Complex workflow orchestration
- Token budget planning and optimization
- Documentation architecture design
- Quality gate configuration

---

## Implementation Guide

### 1. TRUST 5 Framework - Quality Assurance System

Purpose: Automated quality gates ensuring code quality, security, and maintainability.

**Five Pillars:**

- **Test-first Pillar:** Maintain test coverage at or above 85 percent. Execute pytest with coverage reporting. Block merge and generate missing tests on failure.
- **Readable Pillar:** Use clear and descriptive naming conventions. Execute linter checks and suggest refactoring improvements on failure.
- **Unified Pillar:** Apply consistent formatting and import patterns. Execute formatter checks and auto-format code or issue warnings on failure.
- **Secured Pillar:** Comply with OWASP security standards. Execute security analysis and block merge on failure.
- **Trackable Pillar:** Write clear and structured commit messages. Match Git commit message regex patterns and suggest proper formats on failure.

Integration Points: Pre-commit hooks for automated validation, CI/CD pipelines for quality gate enforcement.

Detailed Reference: `modules/trust-5-framework.md`

---

### 2. SPEC-First DDD - Development Workflow

Purpose: Specification-driven development ensuring clear requirements before implementation.

**Three-Phase Workflow:**

- **Phase 1 SPEC:** Generates EARS format. Execute `/clear` to save tokens.
- **Phase 2 DDD:** Validate with at least 85% coverage.
- **Phase 3 Docs:** API documentation, architecture diagrams, project reports.

Token Budget: SPEC takes 30K, DDD takes 180K, Docs takes 40K, Total is 250K.

Key Practice: Execute `/clear` after Phase 1 to initialize context.

Detailed Reference: `modules/spec-first-ddd.md`

---

### 3. Delegation Patterns - Agent Orchestration

Purpose: Task delegation to specialized agents, avoiding direct execution.

Core Principle: Delegate all work through Task() to specialized agents. Proper delegation improves task success rate and enables parallel execution.

**Delegation Syntax:** Call Task with parameters for specialized agent, specific task, and relevant data dictionary.

**Three Patterns:**

- **Sequential for dependencies:** Call Task to one agent, then another with context.
- **Parallel for independent work:** Call multiple Tasks simultaneously.
- **Conditional for analysis-based:** Call Task for analysis, then based on results, call appropriate agent.

Detailed Reference: `modules/delegation-patterns.md`

---

### 4. Token Optimization - Budget Management

Purpose: Efficient 200K token budget through strategic context management.

**Budget Allocation:**

- SPEC Phase takes 30K tokens.
- DDD Phase takes 180K tokens.
- Docs Phase takes 40K tokens.

Total Budget is 250K tokens across all phases. Phase separation with context reset between phases provides clean context boundaries.

Token Saving Strategies:

- Execute `/clear` between phases.
- Load only necessary files.

Detailed Reference: `modules/token-optimization.md`

---

### 5. Progressive Disclosure - Content Architecture

Purpose: Three-tier knowledge delivery balancing value with depth.

**Three Levels:**

- **Quick Reference Level:** Core principles and essential concepts.
- **Implementation Level:** Workflows, practical examples, integration patterns.
- **Advanced Level:** Deep technical dives, edge cases, optimization techniques.

Detailed Reference: `modules/progressive-disclosure.md`

---

### 6. Modular System - File Organization

Purpose: Scalable file structure enabling unlimited content.

**Standard Structure:** Create a directory containing SKILL.md as core file under 500 lines, modules directory for extended content.

File Principles: SKILL.md stays under 500 lines with progressive disclosure and cross-references.

Detailed Reference: `modules/modular-system.md`

---

## Advanced Implementation

Advanced patterns including cross-module integration, quality validation, and error handling are available in the detailed module references.

Key Advanced Topics:

- Cross-Module Integration
- Token-Optimized Delegation
- Progressive Agent Workflows
- Quality Validation
- Error Handling

Detailed Reference: `examples.md` for working code samples.

---

## Works Well With

Agents: Various agents for creating agents, generating skills, and validating quality.

Skills: Skills with foundational patterns and configurations.

Tools: AskUserQuestion for direct user interaction.

Commands: Various commands for managing phases and token management.

Foundation Modules: Extended documentation for agents, commands, and execution rules.

---

## Quick Decision Guide

- **New Agent:** TRUST 5 and Delegation.
- **New Skill:** Progressive and Modular.
- **Workflow:** Delegation Patterns.
- **Quality:** TRUST 5 Framework.
- **Budget:** Token Optimization.
- **Docs:** Progressive and Modular.

Module Deep Dives: `modules/trust-5-framework.md`, `modules/spec-first-ddd.md`, `modules/delegation-patterns.md`, `modules/token-optimization.md`, `modules/progressive-disclosure.md`, `modules/modular-system.md`.

Full Examples: `examples.md`
External Resources: `reference.md`