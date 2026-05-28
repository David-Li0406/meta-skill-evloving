---
name: tdd-workflow
description: Use TDD workflow (Red-Green-Refactor-Validate) when creating or modifying any business logic, use cases, or domain code. MANDATORY for all implementations. Apply when user requests new features, bug fixes, or refactoring that involves testable code.
---

# TDD Workflow

Test-Driven Development cycle: Red → Green → Refactor → Validate

**MANDATORY** for all business logic, use cases, and domain code implementations.

---

## Process

| Phase | Goal | Action | Expected | Template |
|-------|------|--------|----------|----------|
| **RED** | Define behavior | Write failing test | Test FAILS | `.claude/templates/test-unit.php.tpl` |
| **GREEN** | Pass test | Minimal implementation | Test PASSES | `.claude/templates/use-case.php.tpl`, `request.php.tpl` |
| **REFACTOR** | Clean code | Improve without breaking tests | Tests still pass | - |
| **VALIDATE** | Quality gates | `make qa` | All gates pass | - |

---

## 1. RED: Write Failing Test

**File**: `BC/Tests/UseCases/Entity/ActionEntity/ActionEntityTest.php`

**Steps**:
1. Use template: `.claude/templates/test-unit.php.tpl`
2. Write assertions (explicit expectations)
3. Use DataBuilder for test data (NOT Foundry)
4. Mock dependencies: `expects()->once()`
5. Run: `php bin/phpunit path/to/Test.php`

**Expected**: FAILURE (class not found or assertion fails)

**Critical**: Test MUST fail for the right reason

---

## 2. GREEN: Minimal Implementation

**Create Request** (`BC/UseCases/Entity/ActionEntity/ActionEntityRequest.php`):
- Template: `.claude/templates/request.php.tpl`
- `readonly` class, public fields only

**Create UseCase** (`BC/UseCases/Entity/ActionEntity/ActionEntity.php`):
- Template: `.claude/templates/use-case.php.tpl`
- `readonly` class, single `execute()` method
- Inject Repository (commands) OR Finder (queries)

**Run**: `php bin/phpunit path/to/Test.php`

**Expected**: OK (test passes)

**Critical**: Minimal code only, no premature optimization

---

## 3. REFACTOR: Clean Code

**Commands**:
```bash
make cs-fixer    # Auto-fix code style
make stan        # Static analysis (level 9)
make ta          # Verify tests still pass
```

**Improvements**:
- Better naming (domain language)
- Extract private methods if needed
- Add PHPDoc (`@param`, `@return`, `@throws`)
- Simplify logic

**Critical**: Tests MUST still pass after refactoring

---

## 4. VALIDATE: Full QA

**Command**:
```bash
make qa
```

**Gates** (all must pass):
- PHPStan level 9: 0 errors
- CS-Fixer: formatted
- PHPCS: compliant
- Rector: no suggestions
- Deptrac: architecture valid
- All tests: passing

**Critical**: NEVER commit without `make qa` passing

---

## Rules

**ALWAYS**:
- Start with test (Red phase)
- Test MUST fail before implementation
- Minimal implementation first (Green)
- Refactor only when tests pass
- `make qa` before commit

**NEVER**:
- Code before test
- Premature optimization (in Green)
- Refactor without passing tests
- Commit without `make qa`

---

## Repository vs Finder

| Aspect | Repository | Finder |
|--------|-----------|--------|
| **Use** | Commands (CUD) | Queries (R) |
| **Methods** | `get*()`, `save()`, `delete()` | `find*()`, `findAll()` |
| **Not found** | Throws exception | Returns null/[] |
| **Location** | `BC/Entities/Repository/` | `BC/UseCases/Gateway/Finder/` |

**See**: `docs/GLOSSARY.md#repository-vs-finder` for detailed comparison

---

## Templates

- `test-unit.php.tpl` - Unit test
- `request.php.tpl` - Request DTO
- `use-case.php.tpl` - UseCase

**Location**: `.claude/templates/`

---

## References

- Quick patterns: `docs/QUICK_REF.md#usecase-pattern`
- Testing strategy: `docs/testing.md`
- Commands: `docs/reference.md`
- Architecture: `docs/architecture.md`
