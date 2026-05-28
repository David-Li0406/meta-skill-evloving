---
name: code-quality
description: Non-negotiable code quality standards for structure, testing, naming, and documentation
user-invocable: false
---

# Code Quality Skill

**Version:** 1.0
**Source:** Code Quality Standards

> Non-negotiable code quality standards. These are not preferences—they are requirements.

---

## Overview

This skill provides comprehensive code quality standards covering:
- 3-tier architecture and structure
- Test-Driven Development (TDD)
- Naming conventions with directional clarity
- Docstring requirements

---

## 1. Structure

### 3-Tier Architecture

Always respect the layered architecture:

```
01-presentation/  ← UI layer (React components, pages, styles)
02-logic/         ← Business logic (services, use cases, API)
03-data/          ← Data persistence (repositories, models)
config/           ← Cross-cutting configuration
```

### Valid Dependency Flow

```
Presentation → Logic → Data ✅
Data → Logic ❌ (blocked)
Logic → Presentation ❌ (blocked)
```

### Directory Structure

**Components:**
```
/01-presentation/components/
  Button/
    ├── Button.tsx           # Component
    ├── Button.test.tsx      # Tests
    ├── Button.css           # Styles
    └── index.ts             # Re-export
```

**Services:**
```
/02-logic/services/
  ├── UserService.ts
  ├── UserService.test.ts
  └── types.ts               # Service-specific types
```

**Repositories:**
```
/03-data/repositories/
  ├── UserRepository.ts
  └── UserRepository.test.ts
```

### Before Creating Any File

1. Ask: "Which tier does this belong to?"
2. Verify: "Am I importing from a valid dependency direction?"
3. Check: "Is this business logic masquerading as a component?"

---

## 2. Testing Standards

### The Testing Pyramid

| Layer | What it Tests | Speed | Purpose |
|-------|---------------|-------|---------|
| **Unit Tests** | Individual functions/components | Fast | TDD lives here. Catches logic errors early. |
| **Integration Tests** | Components working together | Medium | Catches connection and data flow issues. |
| **E2E Tests** | Full user flows | Slowest | Confirms the system does the thing. |
| **Human Review** | Visual correctness, UX | Manual | Irreducible quality judgment. |

### Test-Driven Development (TDD)

**TDD is mandatory at the unit test level:**

1. **Tests are written BEFORE implementation** — Never implement without a failing test first
2. **Red → Green → Refactor is mandatory** — No exceptions
3. **Tests define behavior** — Implementation serves tests
4. **Small incremental steps** — Tiny, safe changes over large speculative edits
5. **Tests are the source of truth** — If it's not tested, it doesn't work

**When in doubt:** Slow down, write the test, make the smallest possible change.

### Unit Tests
- Foundation of testing
- Run in milliseconds
- Catch most bugs before they escape

### Integration Tests
- Verify modules work together
- Use test databases or containers, not mocks
- Reset state between tests

### E2E Tests
- Critical user paths only
- Keep the suite small and focused
- Accept some flakiness, build in retries

### Human Review
- Does it work correctly?
- Does it look right?
- Does it feel good?
- Is it accessible?

---

## 3. Naming Conventions

Names must clearly communicate:
1. **Who is acting** — The subject performing the action
2. **What action is occurring** — The verb describing the behavior
3. **Direction of data or ownership flow** — Where things are going to/from

### Directional Clarity

Use prepositions (`to`, `from`, `into`, `onto`) or named parameters.

**Bad — Ambiguous:**
```python
shop.buy_item(item_id, buyer)      # Who is buying?
transfer(amount, account)           # Transfer to or from?
```

**Good — Clear:**
```python
shop.sell_item_to(item_id, buyer)  # Shop sells TO buyer
shop.sell(item_id, to=buyer)       # Named parameter clarifies
transfer_from(account, amount)      # Direction explicit
account.transfer_to(other, amount)  # Direction in method name
```

### The Read-Aloud Test

If a method call doesn't read naturally when spoken aloud, the name is wrong.

```python
# "shop buy item buyer" — confusing
shop.buy_item(item_id, buyer)

# "shop sell item to buyer" — clear
shop.sell_item_to(item_id, buyer)
```

### Naming Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| `verb_noun_to(target)` | Action flows to target | `send_message_to(user)` |
| `verb_noun_from(source)` | Action flows from source | `receive_payment_from(customer)` |
| `noun.verb_to(target)` | Object performs action toward target | `cart.transfer_to(order)` |
| `verb(noun, to=target)` | Named parameter clarifies | `assign(task, to=developer)` |

### File Naming

| File Type | Convention | Example |
|-----------|------------|---------|
| **Components** | PascalCase | `Button.tsx`, `UserProfile.tsx` |
| **Pages** | PascalCase | `Dashboard.tsx`, `Login.tsx` |
| **Services** | PascalCase + "Service" | `EmailService.ts`, `AuthService.ts` |
| **Repositories** | PascalCase + "Repository" | `UserRepository.ts` |
| **Use Cases** | camelCase (verb-first) | `registerUser.ts`, `createOrder.ts` |
| **Utils** | camelCase | `formatDate.ts`, `validateEmail.ts` |
| **Types** | PascalCase | `User.ts`, `Order.ts` |
| **Tests** | Same as source + `.test` | `UserService.test.ts` |
| **Styles** | kebab-case | `button.css`, `user-profile.css` |
| **Config** | camelCase | `database.ts`, `email.ts` |

---

## 4. Docstrings

**Docstrings are living documentation.** Public APIs must be self-explanatory without reading implementation.

### Required Elements

Every public function, method, and class must include:

1. **Purpose** — What it does (one line)
2. **Parameters** — Each parameter with type and meaning
3. **Returns** — What is returned and when
4. **Side effects** — Any state changes, I/O, or mutations
5. **Errors** — What exceptions/errors can occur
6. **Examples** — Realistic usage showing common cases

### Example Docstring

```python
def sell_item_to(self, item_id: str, buyer: Customer) -> Receipt:
    """Sell an item from shop inventory to a customer.

    Transfers ownership of the item from the shop to the buyer,
    processes payment, and updates inventory.

    Args:
        item_id: Unique identifier of the item to sell.
        buyer: Customer purchasing the item. Must have sufficient balance.

    Returns:
        Receipt containing transaction details and timestamp.

    Raises:
        ItemNotFoundError: If item_id doesn't exist in inventory.
        InsufficientBalanceError: If buyer can't afford the item.
        ItemAlreadySoldError: If item was sold between check and purchase.

    Examples:
        Basic sale:
        >>> shop = Shop(inventory=[item])
        >>> buyer = Customer(balance=100)
        >>> receipt = shop.sell_item_to(item.id, buyer)
        >>> assert receipt.amount == item.price
        >>> assert item.id not in shop.inventory

        Handling insufficient balance:
        >>> poor_buyer = Customer(balance=0)
        >>> shop.sell_item_to(item.id, poor_buyer)
        Raises InsufficientBalanceError
    """
```

### Docstring Rules

- Examples should mirror actual test scenarios
- Update docstrings when behavior changes
- Treat docstrings as first-class code, not decoration

---

## Quick Reference

### Checklist

- [ ] Files in correct tier (01-presentation / 02-logic / 03-data)
- [ ] Valid dependency flow (Presentation → Logic → Data)
- [ ] No business logic in components
- [ ] Directory structure follows conventions
- [ ] Tests written BEFORE implementation
- [ ] Red → Green → Refactor followed
- [ ] All tests pass
- [ ] Edge cases tested
- [ ] File names follow convention
- [ ] Function names pass read-aloud test
- [ ] Directional clarity in method names
- [ ] No abbreviations in names
- [ ] All public APIs have docstrings
- [ ] Docstring examples mirror test cases

---

## References

- `references/testing-pyramid.md` — Detailed testing guidance
- `references/naming-patterns.md` — Complete naming conventions
- `references/directory-conventions.md` — File organization rules

## Assets

- `assets/tdd-checklist.md` — TDD workflow checklist
- `assets/docstring-template.md` — Copy-paste docstring templates

## Scripts

- `scripts/validate_structure.py` — Check 3-tier architecture compliance
- `scripts/check_naming.py` — Validate naming conventions
