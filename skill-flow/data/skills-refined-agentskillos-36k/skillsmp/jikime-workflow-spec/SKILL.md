---
name: jikime-workflow-spec
description: SPEC workflow orchestration with EARS format, requirement clarification, and Plan-Run-Sync integration for JikiME-ADK development methodology
version: 1.0.0
tags: ["workflow", "spec", "ears", "requirements", "planning"]
triggers:
  keywords: ["SPEC", "requirement", "EARS", "specification", "planning", "요구사항"]
  phases: ["plan"]
  agents: ["manager-spec", "manager-strategy"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~3607
user-invocable: false
context: fork
agent: Plan
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - mcp__context7__resolve-library-id
  - mcp__context7__get-library-docs
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
- Create new SPEC: /jikime:1-plan "user authentication system"
- Create SPEC with domain: /jikime:1-plan --domain AUTH "JWT login"
- Create parallel SPECs with Worktrees: /jikime:1-plan "login feature" "signup feature" --worktree
- Create SPEC with new branch: /jikime:1-plan "payment processing" --branch
- Use existing SPEC: /jikime:1-plan SPEC-AUTH-001

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

Constitution defines the project DNA that all SPECs must respect. Before creating any SPEC, verify alignment with project constitution defined in `.jikime/project/tech.md`.

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

WHY: Constitution prevents architectural drift and ensures maintainability
IMPACT: SPECs aligned with Constitution reduce integration conflicts significantly

### SPEC Workflow Stages

Stage 1 - User Input Analysis: Parse natural language feature description
Stage 2 - Requirement Clarification: Four-step systematic process
Stage 3 - EARS Pattern Application: Structure requirements using five patterns
Stage 4 - Success Criteria Definition: Establish completion metrics
Stage 5 - Test Scenario Generation: Create verification test cases
Stage 6 - SPEC Document Generation: Produce standardized markdown output

### EARS Format Deep Dive

Ubiquitous Requirements - Always Active:
- Use case: System-wide quality attributes
- Examples: Logging, input validation, error handling
- Test strategy: Include in all feature test suites as common verification

Event-Driven Requirements - Trigger-Response:
- Use case: User interactions and inter-system communication
- Examples: Button clicks, file uploads, payment completions
- Test strategy: Event simulation with expected response verification

State-Driven Requirements - Conditional Behavior:
- Use case: Access control, state machines, conditional business logic
- Examples: Account status checks, inventory verification, permission checks
- Test strategy: State setup with conditional behavior verification

Unwanted Requirements - Prohibited Actions:
- Use case: Security vulnerabilities, data integrity protection
- Examples: No plaintext passwords, no unauthorized access, no PII in logs
- Test strategy: Negative test cases with prohibited behavior verification

Optional Requirements - Enhancement Features:
- Use case: MVP scope definition, feature prioritization
- Examples: OAuth login, dark mode, offline mode
- Test strategy: Conditional test execution based on implementation status

### Requirement Clarification Process

Step 0 - Assumption Analysis (Philosopher Framework):

Before defining scope, surface and validate underlying assumptions using AskUserQuestion.

Assumption Categories:
- Technical Assumptions: Technology capabilities, API availability, performance characteristics
- Business Assumptions: User behavior, market requirements, timeline feasibility
- Team Assumptions: Skill availability, resource allocation, knowledge gaps
- Integration Assumptions: Third-party service reliability, compatibility expectations

Assumption Documentation:
- Assumption Statement: Clear description of what is assumed
- Confidence Level: High, Medium, or Low based on evidence
- Evidence Basis: What supports this assumption
- Risk if Wrong: Consequence if assumption proves false
- Validation Method: How to verify before committing significant effort

Step 0.5 - Root Cause Analysis:

For feature requests or problem-driven SPECs, apply Five Whys:
- Surface Problem: What is the user observing or requesting?
- First Why: What immediate need drives this request?
- Second Why: What underlying problem creates that need?
- Third Why: What systemic factor contributes?
- Root Cause: What fundamental issue must the solution adddess?

Step 1 - Scope Definition:
- Identify supported authentication methods
- Define validation rules and constraints
- Determine failure handling strategy
- Establish session management approach

Step 2 - Constraint Extraction:
- Performance Requirements: Response time targets
- Security Requirements: OWASP compliance, encryption standards
- Compatibility Requirements: Supported browsers and devices
- Scalability Requirements: Concurrent user targets

Step 3 - Success Criteria Definition:
- Test Coverage: Minimum percentage target
- Response Time: Percentile targets (P50, P95, P99)
- Functional Completion: All normal scenarios pass verification
- Quality Gates: Zero linter warnings, zero security vulnerabilities

Step 4 - Test Scenario Creation:
- Normal Cases: Valid inputs with expected outputs
- Error Cases: Invalid inputs with error handling
- Edge Cases: Boundary conditions and corner cases
- Security Cases: Injection attacks, privilege escalation attempts

### Plan-Implement-Test-Sync Workflow Integration

PLAN Phase (/jikime:1-plan):
- manager-spec agent analyzes user input
- EARS format requirements generation
- Requirement clarification with user interaction
- 3-file SPEC creation in .jikime/specs/SPEC-{DOMAIN}-{NUMBER}/ directory
- Git branch creation (optional --branch flag)
- Git Worktree setup (optional --worktree flag)

IMPLEMENT Phase (/jikime:2-run):
- manager-ddd agent loads SPEC document
- ANALYZE-PRESERVE-IMPROVE DDD cycle execution
- jikime-workflow-testing skill reference for test patterns
- Domain Expert agent delegation (backend, frontend, etc.)
- Quality validation through manager-quality agent

TEST Phase (/jikime:test):
- Test execution based on acceptance.md criteria
- Given-When-Then scenario verification
- Quality gate validation
- Coverage and performance checks

SYNC Phase (/jikime:3-sync):
- Documentation updates and synchronization
- CHANGELOG entry creation
- Version control commit with SPEC reference
- SPEC status update and closure

### Parallel Development with Git Worktree

Worktree Concept:
- Independent working directories for multiple branches
- Each SPEC gets isolated development environment
- No branch switching needed for parallel work
- Reduced merge conflicts through feature isolation

Worktree Creation:
- Command /jikime:1-plan "login feature" "signup feature" --worktree creates multiple SPECs
- Result creates project-worktrees directory with SPEC-specific subdirectories

Worktree Benefits:
- Parallel Development: Multiple features developed simultaneously
- Team Collaboration: Clear ownership boundaries per SPEC
- Dependency Isolation: Different library versions per feature
- Risk Reduction: Unstable code does not affect other features

---

## Advanced Implementation (10+ minutes)

For advanced patterns including SPEC templates, validation automation, and workflow optimization, see:

- [Advanced Patterns](modules/advanced-patterns.md): Custom SPEC templates, validation automation
- [Reference Guide](reference.md): SPEC metadata schema, integration examples
- [Examples](examples.md): Real-world SPEC documents, workflow scenarios

## Resources

### SPEC File Organization (3-File Structure)

Directory Structure:
```
.jikime/specs/
├── README.md                    # Directory documentation
└── SPEC-{DOMAIN}-{NUMBER}/      # SPEC document directory
    ├── spec.md                  # EARS requirements
    ├── plan.md                  # Implementation plan
    └── acceptance.md            # Acceptance criteria
```

SPEC ID Format:
- Pattern: `SPEC-{DOMAIN}-{NUMBER}`
- Domain: Uppercase letters (AUTH, USER, API, DB, UI, PERF, SEC)
- Number: 3-digit zero-padded (001, 002, etc.)
- Examples: `SPEC-AUTH-001`, `SPEC-API-002`, `SPEC-USER-003`

3-File Structure:
- spec.md: EARS format requirements (Ubiquitous, Event-driven, State-driven, Unwanted, Optional)
- plan.md: Implementation plan with milestones, phases, and risks
- acceptance.md: Given-When-Then acceptance criteria with quality gates

[HARD] Flat file creation is BLOCKED:
- `.jikime/specs/SPEC-*.md` single file is prohibited
- All SPECs MUST use directory structure with 3 files

### SPEC Metadata Schema

Required Fields (in spec.md):
- SPEC ID: Format SPEC-{DOMAIN}-{NUMBER} (e.g., SPEC-AUTH-001)
- Title: Feature name in English
- Created: ISO 8601 timestamp
- Status: Planning, In Progress, Completed, Blocked
- Priority: High, Medium, Low
- Assigned: Agent responsible for implementation

Optional Fields:
- Related SPECs: Dependencies and related features
- Epic: Parent feature group
- Estimated Effort: Priority-based (Primary/Secondary/Optional goals)
- Labels: Tags for categorization

### SPEC Lifecycle Management (SDD 2025 Standard)

Lifecycle Level Field:

Level 1 - spec-first:
- Description: SPEC written before implementation, discarded after completion
- Use Case: One-time features, prototypes, experiments
- Maintenance Policy: No maintenance required after implementation

Level 2 - spec-anchored:
- Description: SPEC maintained alongside implementation for evolution
- Use Case: Core features, API contracts, integration points
- Maintenance Policy: Quarterly review, update when implementation changes

Level 3 - spec-as-source:
- Description: SPEC is the single source of truth; only SPEC is edited by humans
- Use Case: Critical systems, regulated environments, code generation workflows
- Maintenance Policy: SPEC changes trigger implementation regeneration

Lifecycle Transition Rules:
- spec-first to spec-anchored: When feature becomes production-critical
- spec-anchored to spec-as-source: When compliance or regeneration workflow required
- Downgrade allowed but requires explicit justification in SPEC history

### Quality Metrics

SPEC Quality Indicators:
- Requirement Clarity: All EARS patterns used appropriately
- Test Coverage: All requirements have corresponding test scenarios
- Constraint Completeness: Technical and business constraints defined
- Success Criteria Measurability: Quantifiable completion metrics

Validation Checklist:
- All EARS requirements testable
- No ambiguous language (should, might, usually)
- All error cases documented
- Performance targets quantified
- Security requirements OWASP-compliant

### Works Well With

- jikime-foundation-core: SPEC-First DDD methodology and TRUST 5 framework
- jikime-workflow-testing: DDD implementation and test automation
- jikime-workflow-project: Project initialization and configuration
- jikime-workflow-worktree: Git Worktree management for parallel development
- manager-spec: SPEC creation and requirement analysis agent
- manager-ddd: DDD implementation based on SPEC requirements
- manager-quality: TRUST 5 quality validation and gate enforcement

### Integration Examples

Sequential Workflow:
- Step 1 PLAN: /jikime:1-plan "user authentication system"
- Step 2 IMPLEMENT: /jikime:2-run SPEC-AUTH-001
- Step 3 TEST: /jikime:test SPEC-AUTH-001
- Step 4 SYNC: /jikime:3-sync SPEC-AUTH-001

Parallel Workflow:
- Create multiple SPECs: /jikime:1-plan "backend API" "frontend UI" "database schema" --worktree
- Session 1: /jikime:2-run SPEC-API-001 (backend API)
- Session 2: /jikime:2-run SPEC-UI-001 (frontend UI)
- Session 3: /jikime:2-run SPEC-DB-001 (database schema)

### Token Management

Session Strategy:
- PLAN phase uses approximately 30% of session tokens
- RUN phase uses approximately 60% of session tokens
- SYNC phase uses approximately 10% of session tokens

Context Optimization:
- SPEC document persists in .jikime/specs/ directory
- Session memory in .jikime/memory/ for cross-session context
- Minimal context transfer through SPEC ID reference
- Agent delegation reduces token overhead

---

Version: 2.0.0 (3-File SPEC Structure)
Last Updated: 2026-01-22
Integration Status: Complete - Full Plan-Implement-Test-Sync workflow with 3-file SPEC structure
