# SPEC-First DDD - Specification-Driven Development

Purpose: Specification-driven domain-driven development workflow ensuring clear requirements before implementation through EARS format and ANALYZE-PRESERVE-IMPROVE cycles.

Version: 3.0.0 (DDD Migration)
Last Updated: 2026-01-17

---

## Quick Reference (30 seconds)

SPEC-First DDD is JikiME-ADK's development methodology combining:

1. SPEC Generation - EARS format requirements (/jikime:1-plan)
2. Domain-Driven Development - ANALYZE-PRESERVE-IMPROVE (/jikime:2-run)
3. Documentation Sync - Auto-generated docs (/jikime:3-sync)

Three-Phase Workflow:
```
Phase 1: SPEC → manager-spec → .jikime/specs/SPEC-XXX/spec.md
Phase 2: DDD  → manager-ddd → Code + Tests (≥85% coverage)
Phase 3: Docs → manager-docs → API docs + diagrams
```

Token Budget: SPEC 30K | DDD 180K | Docs 40K | Total 250K

Key Practice: Execute `/clear` after Phase 1 to save 45-50K tokens.

EARS Patterns:
- Ubiquitous: System SHALL always...
- Event-driven: WHEN <event>, system SHALL...
- State-driven: WHILE <state>, system SHALL...
- Unwanted: System SHALL NOT...
- Optional: WHERE possible, system SHOULD...

Extended Documentation:
- [EARS Format Reference](spec-ears-format.md) - Detailed EARS patterns and examples
- [DDD Implementation](spec-ddd-implementation.md) - ANALYZE-PRESERVE-IMPROVE workflows

---

## Implementation Guide (5 minutes)

### Phase 1: SPEC Generation

Purpose: Define clear, testable requirements in EARS format before coding.

Workflow:
```bash
# 1. Generate SPEC
/jikime:1-plan "Implement user authentication with JWT tokens"

# 2. manager-spec creates:
.jikime/specs/SPEC-001/
    spec.md           # EARS format requirements
    acceptance.md     # Acceptance criteria
    complexity.yaml   # Complexity analysis

# 3. Execute /clear (mandatory)
/clear    # Saves 45-50K tokens, prepares clean context
```

EARS Format Structure:

```markdown
---
spec_id: SPEC-001
title: User Authentication System
version: 1.0.0
complexity: Medium
estimated_effort: 8-12 hours
---

## Requirements

### SPEC-001-REQ-01: User Registration (Ubiquitous)
Pattern: Ubiquitous
Statement: The system SHALL register users with email and password validation.

Acceptance Criteria:
- Email format validated (RFC 5322)
- Password strength: ≥8 chars, mixed case, numbers, symbols
- Duplicate email rejected with clear error
- Success returns user ID and confirmation email sent

Test Coverage Target: ≥90%
```

---

### Phase 2: Domain-Driven Development

ANALYZE-PRESERVE-IMPROVE Cycle:

```python
# ANALYZE: Understand existing code and behavior
def analyze_existing_registration():
    """Analyze current registration implementation.

    - Identify existing behavior patterns
    - Document current test coverage
    - Map dependencies and side effects
    """
    pass

# PRESERVE: Create characterization tests
def test_register_user_existing_behavior():
    """Characterization test for existing behavior."""
    result = register_user("user@example.com", "SecureP@ssw0rd")
    assert result.success is True  # Documents existing behavior

# IMPROVE: Refactor with behavior preservation
def register_user(email: str, password: str) -> RegistrationResult:
    """Register new user with email and password.

    Implements SPEC-001-REQ-01
    Behavior preserved from existing implementation.
    """
    # Improved validation, hashing, database operations
    return RegistrationResult(success=True, user=user)
```

Coverage Validation:
```bash
# Run tests with coverage
pytest tests/auth/test_registration.py --cov=src/auth/registration --cov-report=html
```

---

### Phase 3: Documentation Synchronization

Workflow:
```bash
# 1. Generate documentation
/jikime:3-sync SPEC-001

# 2. manager-docs creates:
.jikime/specs/SPEC-001/
    docs/
        api.md           # API reference
        architecture.md  # Architecture diagram
        testing.md       # Test report
        report.md        # Implementation summary
```

---

## Advanced Patterns

For comprehensive implementation patterns including MFA examples, iterative SPEC refinement, and CI/CD integration, see:

- [EARS Format Reference](spec-ears-format.md) - All EARS patterns with examples
- [DDD Implementation](spec-ddd-implementation.md) - Advanced DDD workflows

---

## Works Well With

Agents:
- manager-spec - EARS format SPEC generation
- manager-ddd - ANALYZE-PRESERVE-IMPROVE execution
- manager-quality - TRUST 5 validation
- manager-docs - Documentation generation

Skills:
- jikime-workflow-testing - Test frameworks

Commands:
- /jikime:1-plan - SPEC generation (Phase 1)
- /jikime:2-run - DDD implementation (Phase 2)
- /jikime:3-sync - Documentation sync (Phase 3)
- /clear - Token optimization between phases

---

Version: 3.0.0
Last Updated: 2026-01-17
Status: Production Ready
