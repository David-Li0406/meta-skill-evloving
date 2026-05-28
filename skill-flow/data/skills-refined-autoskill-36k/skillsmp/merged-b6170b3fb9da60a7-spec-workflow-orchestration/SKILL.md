---
name: spec-workflow-orchestration
description: Use this skill for comprehensive specification management and workflow orchestration using the EARS format, including requirement clarification and Plan-Run-Sync integration for development methodologies.
---

# SPEC Workflow Management

## Quick Reference (30 seconds)

SPEC Workflow Orchestration - Comprehensive specification management using EARS format for systematic requirement definition and Plan-Run-Sync workflow integration.

Core Capabilities:
- EARS Format Specifications: Five requirement patterns for clarity
- Requirement Clarification: Four-step systematic process
- SPEC Document Templates: Standardized structure for consistency
- Plan-Run-Sync Integration: Seamless workflow connection
- Parallel Development: Git Worktree-based SPEC isolation
- Quality Gates: TRUST 5 framework validation

EARS Five Patterns:
- Ubiquitous: The system shall always perform action - Always active
- Event-Driven: WHEN event occurs THEN action executes - Trigger-response
- State-Driven: IF condition is true THEN action executes - Conditional behavior
- Unwanted: The system shall not perform action - Prohibition
- Optional: Where possible, provide feature - Nice-to-have

When to Use:
- Feature planning and requirement definition
- SPEC document creation and maintenance
- Parallel feature development coordination
- Quality assurance and validation planning

Quick Commands:
- Create new SPEC: `/spec:1-plan "user authentication system"`
- Create SPEC with domain: `/spec:1-plan --domain AUTH "JWT login"`
- Create parallel SPECs with Worktrees: `/spec:1-plan "login feature" "signup feature" --worktree`
- Create SPEC with new branch: `/spec:1-plan "payment processing" --branch`
- Update existing SPEC: `/spec:1-plan SPEC-001 "add OAuth support"`

---

## Implementation Guide (5 minutes)

### Core Concepts

SPEC-First Development Philosophy:
- EARS format ensures unambiguous requirements
- Requirement clarification prevents scope creep
- Systematic validation through test scenarios
- Integration with DDD workflow for implementation
- Quality gates enforce completion criteria
- Constitution reference ensures project-wide consistency

### Constitution Reference (SDD 2025 Standard)

Constitution defines the project DNA that all SPECs must respect. Before creating any SPEC, verify alignment with project constitution defined in `.project/tech.md`.

Constitution Components:
- Technology Stack: Required versions and frameworks
- Naming Conventions: Variable, function, and file naming standards
- Forbidden Libraries: Libraries explicitly prohibited with alternatives
- Architectural Patterns: Layering rules and dependency directions
- Security Standards: Authentication patterns and encryption requirements
- Logging Standards: Log format and structured logging requirements

Constitution Verification:
- All SPEC technology choices must align with Constitution stack versions
- No SPEC may introduce forbidden libraries or patterns
- SPEC must follow naming conventions defined in Constitution
- SPEC must respect architectural boundaries and layering

### SPEC Workflow Stages

1. User Input Analysis: Parse natural language feature description
2. Requirement Clarification: Four-step systematic process
3. EARS Pattern Application: Structure requirements using five patterns
4. Success Criteria Definition: Establish completion metrics
5. Test Scenario Generation: Create verification test cases
6. SPEC Document Generation: Produce standardized markdown output

### EARS Format Deep Dive

- **Ubiquitous Requirements**: System-wide quality attributes (e.g., logging, input validation)
- **Event-Driven Requirements**: User interactions and inter-system communication (e.g., button clicks)
- **State-Driven Requirements**: Access control and conditional business logic (e.g., account status checks)
- **Unwanted Requirements**: Prohibited actions (e.g., no plaintext passwords)
- **Optional Requirements**: Enhancement features (e.g., OAuth login)

### Requirement Clarification Process

1. Assumption Analysis: Validate underlying assumptions
2. Root Cause Analysis: Apply Five Whys for feature requests
3. Scope Definition: Identify supported methods and constraints
4. Constraint Extraction: Define performance, security, and compatibility requirements
5. Success Criteria Definition: Establish measurable completion metrics
6. Test Scenario Creation: Document normal, error, edge, and security cases

### Plan-Run-Sync Workflow Integration

- **PLAN Phase**: Analyze user input, generate EARS requirements, create SPEC document
- **RUN Phase**: Load SPEC document, execute DDD cycle, validate quality
- **SYNC Phase**: Synchronize documentation, generate API docs, update CHANGELOG

### Parallel Development with Git Worktree

Worktree Concept:
- Independent working directories for multiple branches
- Each SPEC gets isolated development environment
- Reduced merge conflicts through feature isolation

Worktree Creation:
- Command `/spec:1-plan "login feature" "signup feature" --worktree` creates multiple SPECs

---

## Advanced Implementation (10+ minutes)

For advanced patterns including SPEC templates, validation automation, and workflow optimization, see:

- [Advanced Patterns](modules/advanced-patterns.md): Custom SPEC templates, validation automation
- [Reference Guide](reference.md): SPEC metadata schema, integration examples
- [Examples](examples.md): Real-world SPEC documents, workflow scenarios

## Resources

### SPEC File Organization

Directory Structure:
```
.specs/
├── README.md                    # Directory documentation
└── SPEC-{DOMAIN}-{NUMBER}/      # SPEC document directory
    ├── spec.md                  # EARS requirements
    ├── plan.md                  # Implementation plan
    └── acceptance.md            # Acceptance criteria
```

### SPEC Metadata Schema

Required Fields:
- SPEC ID: Format SPEC-{DOMAIN}-{NUMBER} (e.g., SPEC-AUTH-001)
- Title: Feature name in English
- Created: ISO 8601 timestamp
- Status: Planning, In Progress, Completed, Blocked
- Priority: High, Medium, Low
- Assigned: Agent responsible for implementation

Optional Fields:
- Related SPECs: Dependencies and related features
- Epic: Parent feature group
- Estimated Effort: Time estimate in hours or story points
- Labels: Tags for categorization

### SPEC Lifecycle Management (SDD 2025 Standard)

Lifecycle Levels:
- **Level 1**: SPEC written before implementation, discarded after completion
- **Level 2**: SPEC maintained alongside implementation for evolution
- **Level 3**: SPEC is the single source of truth; only SPEC is edited by humans

### Quality Metrics

SPEC Quality Indicators:
- Requirement Clarity: All EARS patterns used appropriately
- Test Coverage: All requirements have corresponding test scenarios
- Constraint Completeness: Technical and business constraints defined
- Success Criteria Measurability: Quantifiable completion metrics

Validation Checklist:
- All EARS requirements testable
- No ambiguous language
- All error cases documented
- Performance targets quantified
- Security requirements OWASP-compliant

### Works Well With

- SPEC-First DDD methodology and TRUST 5 framework
- DDD implementation and test automation
- Project initialization and configuration
- Git Worktree management for parallel development
- SPEC creation and requirement analysis agent

### Integration Examples

Sequential Workflow:
- Step 1 PLAN: `/spec:1-plan "user authentication system"`
- Step 2 RUN: `/spec:2-run SPEC-001`
- Step 3 SYNC: `/spec:3-sync SPEC-001`

Parallel Workflow:
- Create multiple SPECs: `/spec:1-plan "backend API" "frontend UI" "database schema" --worktree`
- Session 1: `/spec:2-run SPEC-001 (backend API)`
- Session 2: `/spec:2-run SPEC-002 (frontend UI)`
- Session 3: `/spec:2-run SPEC-003 (database schema)`

### Token Management

Session Strategy:
- PLAN phase uses approximately 30% of session tokens
- RUN phase uses approximately 60% of session tokens
- SYNC phase uses approximately 10% of session tokens

Context Optimization:
- SPEC document persists in `.specs/` directory
- Session memory in `.memory/` for cross-session context
- Minimal context transfer through SPEC ID reference

---

Version: 2.0.0 (3-File SPEC Structure)
Last Updated: 2026-01-22
Integration Status: Complete - Full Plan-Implement-Test-Sync workflow with 3-file SPEC structure