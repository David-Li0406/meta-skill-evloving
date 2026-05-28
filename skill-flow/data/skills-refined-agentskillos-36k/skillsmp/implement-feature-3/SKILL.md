---
name: implement-feature
description: Implement feature code to make BDD scenarios pass. Write production code that satisfies Given/When/Then scenarios. Use after implement-step-definitions when step definitions exist but scenarios are failing.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# implement-feature

**Skill Type**: Actuator (BDD Workflow)
**Purpose**: Implement feature code to make scenarios pass
**Prerequisites**:
- Feature file exists with Gherkin scenarios
- Step definitions exist
- Scenarios are FAILING (implementation missing)

---

## Agent Instructions

You are in the **IMPLEMENT** phase of BDD (SCENARIO → STEP DEFINITIONS → IMPLEMENT → REFACTOR).

Your goal is to **implement production code** that makes the scenarios pass.

---

## Workflow

### Step 1: Review Scenarios and Step Definitions

**Understand what needs to be implemented**:
- What functionality is being tested?
- What are the expected inputs and outputs?
- What business rules must be enforced?

**Example**:
```gherkin
# features/authentication.feature shows we need:

Scenario: Successful login
  When I click the "Login" button
  Then I should see "Welcome back"

# Step definition shows:
@when('I click the "Login" button')
def step_impl(context, button):
    email = _ui_state['email_input']
    password = _ui_state['password_input']
    _login_result = login(email, password)  # Calls login() - doesn't exist yet

# We need to implement: login(email, password) -> LoginResult
```

---

### Step 2: Determine Implementation File Location

**Follow project conventions**:

**Python**:
```
features/authentication.feature → src/auth/authentication.py
features/payments/checkout.feature → src/payments/checkout.py
```

**JavaScript/TypeScript**:
```
features/authentication.feature → src/auth/authentication.ts
features/payments/checkout.feature → src/payments/checkout.ts
```

**Java**:
```
features/authentication.feature → src/main/java/auth/Authentication.java
```

---

### Step 3: Implement Feature Code

**Write production code that makes scenarios pass**:

```python
# src/auth/authentication.py

# Implements: <REQ-ID>
# Business Rules: BR-001, BR-002, BR-003

import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

@dataclass
class LoginResult:
    """Result of login attempt"""
    success: bool
    user: Optional['User'] = None
    error: Optional[str] = None

class User:
    """User model"""
    def __init__(self, email: str):
        self.email = email
        self.password_hash: Optional[str] = None
        self.failed_attempts = 0
        self.locked_until: Optional[datetime] = None

    def set_password(self, password: str) -> None:
        """Set user password (hashed)"""
        self.password_hash = self._hash_password(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches"""
        return self.password_hash == self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password (simplified for demo)"""
        # In production: use bcrypt
        return str(hash(password))


# Implements: <REQ-ID>
def login(email: str, password: str) -> LoginResult:
    """
    Authenticate user with email and password.

    Implements: <REQ-ID> (User login)

    Business Rules:
    - BR-001: Email must be valid format
    - BR-002: Password minimum 12 characters
    - BR-003: Account locks after 3 failed attempts (15min)

    Args:
        email: User email address
        password: User password

    Returns:
        LoginResult with success status, user object, or error message
    """
    # Implements: BR-001 (email validation)
    if not _validate_email(email):
        return LoginResult(success=False, error="Invalid email format")

    # Implements: BR-002 (password minimum length)
    if len(password) < 12:
        return LoginResult(success=False, error="Password must be at least 12 characters")

    # Get user from database
    user = _get_user_by_email(email)
    if not user:
        return LoginResult(success=False, error="User not found")

    # Implements: BR-003 (check if account locked)
    if user.locked_until and datetime.now() < user.locked_until:
        remaining = (user.locked_until - datetime.now()).seconds // 60
        return LoginResult(
            success=False,
            error=f"Account locked. Try again in {remaining} minutes"
        )

    # Check password
    if not user.check_password(password):
        user.failed_attempts += 1

        # Implements: BR-003 (lock after 3 failed attempts)
        if user.failed_attempts >= 3:
            user.locked_until = datetime.now() + timedelta(minutes=15)
            return LoginResult(
                success=False,
                error="Account locked. Try again in 15 minutes"
            )

        return LoginResult(success=False, error="Invalid password")

    # Success - reset failed attempts
    user.failed_attempts = 0
    user.locked_until = None

    return LoginResult(success=True, user=user)


def _validate_email(email: str) -> bool:
    """Validate email format (BR-001)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _get_user_by_email(email: str) -> Optional[User]:
    """Get user from database (simplified for testing)"""
    # In production: query database
    # For testing: use in-memory store or mock
    return _test_user_store.get(email)


# Test user storage (for BDD testing)
_test_user_store = {}

def create_test_user(email: str, password: str = "DefaultPass123!") -> User:
    """Create a test user (helper for step definitions)"""
    user = User(email=email)
    user.set_password(password)
    _test_user_store[email] = user
    return user
```

**Key implementation principles**:
- ✅ Tag code with REQ-* and BR-* keys
- ✅ Implement exactly what scenarios require (no more)
- ✅ Use clear, descriptive names
- ✅ Add docstrings explaining business rules
- ✅ Keep functions focused (single responsibility)

---

### Step 4: Run Scenarios (Expect SUCCESS)

**Run BDD framework**:

```bash
# Behave (Python)
behave features/authentication.feature -v

# Cucumber (JavaScript)
npm run cucumber

# Cucumber (Java)
mvn test -Dcucumber.options="features/authentication.feature"
```

**Expected output**:
```
Feature: User Login

  Background:
    Given the application is running           PASSED
    And I am on the login page                PASSED

  Scenario: Successful login with valid credentials
    Given I am a registered user              PASSED
    And my password is "SecurePassword123!"   PASSED
    When I enter email "user@example.com"     PASSED
    And I enter password "SecurePassword123!" PASSED
    And I click the "Login" button            PASSED
    Then I should see "Welcome back"          PASSED
    And I should be redirected to dashboard   PASSED

  Scenario: Login fails with invalid email
    When I enter email "invalid-email"        PASSED
    And I enter password "SecurePassword123!" PASSED
    And I click the "Login" button            PASSED
    Then I should see "Invalid email format"  PASSED

5 scenarios (5 passed)
27 steps (27 passed)
```

**✅ All scenarios PASSING!** This is what we want in IMPLEMENT phase.

---

### Step 5: Commit Implementation

**Create commit**:

```bash
git add src/auth/authentication.py
git commit -m "IMPLEMENT: Implement <REQ-ID>

Implement user login functionality to satisfy BDD scenarios.

Implements:
- <REQ-ID>: User login
- BR-001: Email validation
- BR-002: Password minimum 12 characters
- BR-003: Account lockout after 3 failed attempts

Implementation:
- Created LoginResult dataclass
- Implemented login() function
- Added email validation helper
- Added user model with password hashing
- Added test user helpers for BDD testing

Scenarios: 5 scenarios passing ✓
Steps: 27 steps passing ✓
"
```

---

## Output Format

When you complete the IMPLEMENT phase, show:

```
[IMPLEMENT Phase - <REQ-ID>]

Implementation: src/auth/authentication.py

Code Created:
  ✓ LoginResult dataclass
  ✓ User class with password handling
  ✓ login() function (<REQ-ID>)
  ✓ _validate_email() helper (BR-001)
  ✓ _get_user_by_email() helper
  ✓ create_test_user() helper (for BDD)

Business Rules Implemented:
  ✓ BR-001: Email validation (regex)
  ✓ BR-002: Password minimum 12 characters
  ✓ BR-003: Account lockout after 3 attempts

Running scenarios...
  Scenario: Successful login              PASSED ✓
  Scenario: Login fails invalid email     PASSED ✓
  Scenario: Login fails short password    PASSED ✓
  Scenario: Account locks after 3 fails   PASSED ✓
  Scenario: Login after lockout expires   PASSED ✓

Result: 5/5 scenarios PASSING ✓ (IMPLEMENT phase)

Commit: IMPLEMENT: Implement <REQ-ID>

✅ IMPLEMENT Phase Complete!
   Next: Invoke refactor-bdd skill to improve code quality
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Feature file exists (from write-scenario)
2. Step definitions exist (from implement-step-definitions)
3. Scenarios are FAILING (implementation missing)

If prerequisites not met:
- No feature file → Invoke `write-scenario` skill first
- No step definitions → Invoke `implement-step-definitions` skill first
- Scenarios already passing → Already implemented, skip to refactor-bdd

---

## Next Steps

After IMPLEMENT phase completes:
1. **Do NOT refactor yet** (scenarios must pass first)
2. Invoke `refactor-bdd` skill to improve code quality and eliminate tech debt
3. Scenarios should STILL PASS after refactoring

---

## Implementation Strategies

### Strategy 1: Scenario-by-Scenario

Implement code to pass **one scenario at a time**:
1. Make "Successful login" scenario pass
2. Make "Login fails with invalid email" scenario pass
3. Make "Login fails with short password" scenario pass
4. Make "Account locks after 3 failed attempts" scenario pass

### Strategy 2: Step-by-Step

Implement helpers for **each step type**:
1. Implement Given steps (setup, fixtures)
2. Implement When steps (actions)
3. Implement Then steps (assertions)

### Strategy 3: Business Rule by Business Rule

Implement **one business rule at a time**:
1. Implement BR-001 (email validation)
2. Implement BR-002 (password minimum length)
3. Implement BR-003 (account lockout)

---

## Common Pitfalls to Avoid

❌ **Implementing more than scenarios require**: Only implement what's tested
❌ **Technical coupling**: Don't tightly couple to step definitions
❌ **Skipping business rules**: Every BR-* must be implemented
❌ **Not running scenarios**: Must verify scenarios pass

✅ **Do this instead**:
- Implement exactly what scenarios require
- Keep production code separate from test code
- Verify all scenarios pass
- Tag code with REQ-* and BR-* keys

---

## Notes

**Why implement after step definitions?**
- Step definitions = executable specification
- Clear contract between tests and implementation
- Easier to implement when you know exactly what's needed

**BDD implementation mantra**: "Make scenarios green"
- Scenarios define behavior
- Implementation satisfies behavior
- Refactoring improves quality

**Homeostasis Goal**:
```yaml
desired_state:
  scenarios_passing: true
  all_business_rules_implemented: true
  production_code_clean: true
```

**"Excellence or nothing"** 🔥
