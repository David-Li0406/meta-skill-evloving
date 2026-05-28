# Test Scenarios Reference

Complete test scenario definitions for all components with expected outputs and validation criteria.

## code-with-codex Test Scenarios

### Scenario 1: Simple Function

**Prompt**:
```
Create a Python function named 'calculate_fibonacci' that returns the nth Fibonacci number using recursion. Include docstring and type hints.
```

**Expected Files**:
- `fibonacci.py`

**Expected Content Structure**:
```python
def calculate_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using recursion.

    Args:
        n: The position in Fibonacci sequence

    Returns:
        The Fibonacci number at position n
    """
    # Implementation...
```

**Validation Rules**:
- Contains `def calculate_fibonacci`
- Contains docstring (triple quotes)
- Contains type hints (`: int`, `-> int`)
- Implementation uses recursion
- Handles base cases (n=0, n=1)

**Success Criteria**:
- Syntactically valid Python
- Executable without errors
- Passes basic test: `calculate_fibonacci(10) == 55`

---

### Scenario 2: Class Implementation

**Prompt**:
```
Create a Python class 'UserManager' with methods to add_user, remove_user, and get_user_by_id. Use a dictionary for storage. Include docstrings.
```

**Expected Files**:
- `user_manager.py`

**Expected Content Structure**:
```python
class UserManager:
    """Manages user data with CRUD operations."""

    def __init__(self):
        self.users = {}

    def add_user(self, user_id: str, user_data: dict) -> None:
        """Add a new user."""
        pass

    def remove_user(self, user_id: str) -> bool:
        """Remove a user by ID."""
        pass

    def get_user_by_id(self, user_id: str) -> dict:
        """Retrieve user by ID."""
        pass
```

**Validation Rules**:
- Contains `class UserManager`
- Contains all three methods: `add_user`, `remove_user`, `get_user_by_id`
- Uses dictionary for storage
- Each method has docstring

**Success Criteria**:
- Class instantiable without errors
- Methods callable with correct signatures
- Basic CRUD operations work correctly

---

### Scenario 3: Bug Fixing

**Prompt**:
```
Fix this buggy code: 'def divide(a, b): return a / b'. Handle division by zero and add error handling.
```

**Expected Files**:
- `divide_fixed.py`

**Expected Content Structure**:
```python
def divide(a: float, b: float) -> float:
    """
    Safely divide two numbers with error handling.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Result of division

    Raises:
        ValueError: If denominator is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Validation Rules**:
- Contains error handling for division by zero
- Uses try/except or if-check
- Includes proper error messages
- Has type hints and docstring

**Success Criteria**:
- Handles zero division gracefully
- Raises appropriate exception
- Works correctly for valid inputs

---

### Scenario 4: Test Generation

**Prompt**:
```
Generate pytest unit tests for a function 'def add(a, b): return a + b'. Include edge cases.
```

**Expected Files**:
- `test_add.py`

**Expected Content Structure**:
```python
import pytest

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_floats():
    assert add(1.5, 2.5) == 4.0
```

**Validation Rules**:
- Contains `import pytest` or `import unittest`
- Contains multiple test functions (at least 3)
- Tests cover edge cases (zero, negative, float)
- Uses assertions

**Success Criteria**:
- All tests are runnable
- Tests pass when add() function is correct
- Coverage includes edge cases

---

### Scenario 5: Multi-File Project

**Prompt**:
```
Create a simple FastAPI project structure with: main.py (app entry), routes/users.py (user routes), models/user.py (User model). Basic skeleton only.
```

**Expected Files**:
- `main.py`
- `routes/users.py`
- `models/user.py`

**Expected Content Structure**:

`main.py`:
```python
from fastapi import FastAPI
from routes import users

app = FastAPI()

app.include_router(users.router)
```

`routes/users.py`:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    return []
```

`models/user.py`:
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
```

**Validation Rules**:
- `main.py` contains FastAPI app initialization
- `routes/users.py` contains APIRouter or route definitions
- `models/user.py` contains User class with BaseModel
- Files are in correct directory structure

**Success Criteria**:
- Project structure is correct
- FastAPI app is importable
- No syntax errors
- Basic routes are defined

---

## ux-design-gemini Test Scenarios

### Scenario 1: Component Wireframe

**Prompt**:
```
Design a user profile card component. Include: avatar, name, bio, action buttons. Provide wireframe description and CSS specifications.
```

**Expected Sections**:
- Wireframe Description
- Layout Structure
- Component Elements
- Styling/CSS Specifications

**Expected Content Elements**:
- Avatar/image placement description
- Name and bio text layout
- Button positioning and styling
- Spacing/padding specifications
- Color scheme
- CSS code or design tokens

**Validation Rules**:
- Mentions avatar/image/photo
- Mentions buttons or actions
- Contains CSS specifications or design tokens
- Includes layout description

**Success Criteria**:
- Complete wireframe description (> 300 words)
- Specific CSS values provided
- All required elements covered
- Structured in Markdown format

---

### Scenario 2: User Flow Diagram

**Prompt**:
```
Create user flow for login process: landing page → login form → authentication → dashboard. Document each step and decision points.
```

**Expected Sections**:
- Flow Overview
- Step-by-Step Process
- User Actions
- Decision Points
- Error Handling

**Expected Content Elements**:
- Each step clearly described
- Decision branches (success/failure)
- User inputs at each stage
- Navigation between screens
- Error states

**Validation Rules**:
- Mentions login/authentication
- Contains step-by-step flow
- Mentions dashboard or success state
- Includes decision points

**Success Criteria**:
- Complete flow documented
- All decision points identified
- Error paths included
- Clear navigation logic

---

### Scenario 3: Design System

**Prompt**:
```
Generate a design system foundation: color palette (primary, secondary, accent), typography scale, spacing units. Provide CSS custom properties.
```

**Expected Sections**:
- Color Palette
- Typography Scale
- Spacing System
- CSS Custom Properties

**Expected Content Elements**:
- Primary/secondary/accent color definitions
- Color values in hex/rgb/hsl
- Font sizes (h1-h6, body, small)
- Font families
- Line heights
- Spacing scale (4px, 8px, 16px, etc.)
- CSS variable declarations

**Validation Rules**:
- Contains color values (hex, rgb, or hsl)
- Mentions typography/font sizes
- Contains CSS variables or tokens
- Includes spacing units

**Success Criteria**:
- Complete color palette (minimum 3 colors)
- Full typography scale
- Spacing system defined
- CSS custom properties provided

---

### Scenario 4: Responsive Layout

**Prompt**:
```
Design responsive layout for e-commerce product grid. Define breakpoints (mobile, tablet, desktop) and grid specifications.
```

**Expected Sections**:
- Breakpoint Definitions
- Grid Layout Specifications
- Responsive Behavior
- Mobile/Tablet/Desktop Views

**Expected Content Elements**:
- Breakpoint values (px)
- Grid columns per breakpoint
- Spacing/gutters
- Product card dimensions
- Layout transitions

**Validation Rules**:
- Mentions mobile/tablet/desktop
- Contains breakpoint values
- Describes grid layout
- Specifies column counts

**Success Criteria**:
- All three breakpoints defined
- Grid specifications complete
- Responsive behavior documented
- Specific pixel values provided

---

### Scenario 5: Interaction Pattern

**Prompt**:
```
Document interaction pattern for dropdown menu: hover states, click behavior, keyboard navigation, accessibility considerations.
```

**Expected Sections**:
- Interaction States
- Mouse/Touch Behavior
- Keyboard Navigation
- Accessibility Features

**Expected Content Elements**:
- Hover/focus/active states
- Click/tap behaviors
- Keyboard shortcuts (Tab, Enter, Escape, Arrow keys)
- ARIA labels
- Screen reader support

**Validation Rules**:
- Mentions hover/focus states
- Mentions keyboard navigation
- Contains accessibility considerations
- Includes ARIA or a11y terms

**Success Criteria**:
- All interaction states defined
- Keyboard navigation complete
- Accessibility guidelines followed
- Clear behavioral specifications

---

## /multcode Workflow Test Scenarios

*(Note: /multcode testing is complex and requires end-to-end workflow validation)*

### Scenario 1: Simple Feature Development

**Input**:
```
Feature: User registration form
- Email and password fields
- Validation
- Submit button
- Success/error messaging
```

**Expected Workflow Stages**:

1. **Requirements Analysis (Claude)**
   - Output: `requirements.md`
   - Contains: functional requirements, user stories, acceptance criteria

2. **UX Design (Gemini)**
   - Output: `design-specs.md`
   - Contains: wireframes, form layout, interaction patterns

3. **Implementation Planning (Codex)**
   - Output: `implementation-plan.md`
   - Contains: file structure, component breakdown, technical approach

4. **Code Development (Codex)**
   - Output: Source files (`components/RegistrationForm.jsx`, `validators.js`, etc.)
   - Contains: Working implementation

5. **Quality Assurance (Claude)**
   - Output: `test-results.md`, test files
   - Contains: Test coverage report, validation results

**Validation Rules**:
- All 5 stages complete without errors
- Each stage produces expected output files
- Files are valid and non-empty
- Context flows correctly between stages
- Final code is executable

**Success Criteria**:
- Complete workflow execution (< 10 minutes)
- All output files present
- No critical errors
- Code passes basic validation
- Documentation is complete

---

## Performance Baselines

### Expected Execution Times

| Component | Scenario | Expected Time | Timeout |
|-----------|----------|---------------|---------|
| code-with-codex | Simple Function | 15-30s | 60s |
| code-with-codex | Class Implementation | 20-40s | 60s |
| code-with-codex | Multi-File Project | 40-60s | 90s |
| ux-design-gemini | Component Wireframe | 30-60s | 90s |
| ux-design-gemini | Design System | 45-75s | 90s |
| /multcode | Simple Feature | 5-8 min | 10 min |

### Resource Usage

**Memory**:
- memex-cli process: < 200MB
- Test orchestrator: < 100MB
- Total test suite: < 500MB

**Disk Space**:
- Test artifacts per run: < 50MB
- Complete test history (10 runs): < 500MB

**Network**:
- API calls per test run: ~20-30 requests
- Data transfer: < 10MB

---

## Troubleshooting Common Scenarios

### Scenario: Code Generation Timeout

**Symptoms**:
- Test exceeds 60s timeout
- No output file created
- memex-cli process hangs

**Diagnosis**:
1. Check network connectivity
2. Verify API key is valid
3. Check memex-cli logs for errors
4. Test with simpler prompt

**Resolution**:
- Increase timeout in test config
- Simplify prompt complexity
- Check API rate limits
- Retry with different backend

---

### Scenario: Invalid Output Format

**Symptoms**:
- Files created but content invalid
- Missing expected sections
- Syntax errors in generated code

**Diagnosis**:
1. Review generated file contents
2. Check if prompt was too complex
3. Verify backend model version
4. Check for API response errors

**Resolution**:
- Refine prompt clarity
- Add explicit format instructions
- Use different model/backend
- Add post-processing validation

---

### Scenario: Workflow State Corruption

**Symptoms**:
- /multcode stage transitions fail
- Context not passed between stages
- Duplicate outputs or missing files

**Diagnosis**:
1. Check `.bmad/state.yaml` for corruption
2. Verify stage completion markers
3. Review orchestrator logs

**Resolution**:
- Reset workflow state: `rm -rf .bmad/`
- Restart workflow from beginning
- Check for file permission issues
- Verify disk space availability

---

## Custom Scenario Template

Use this template to define custom test scenarios:

```yaml
scenario:
  name: "Your Scenario Name"
  component: "code-with-codex | ux-design-gemini | multcode"

  prompt: |
    Your detailed prompt here
    Can be multi-line

  expected_files:
    - "path/to/file1.ext"
    - "path/to/file2.ext"

  expected_sections:  # For design/doc outputs
    - "Section Name 1"
    - "Section Name 2"

  validation_rules:
    - "contains 'keyword'"
    - "mentions topic or concept"
    - "includes specific_function_name"

  timeout: 90  # seconds

  success_criteria:
    - "Criterion 1"
    - "Criterion 2"
```

**Usage**:
```python
# Load custom scenario from YAML
import yaml

with open('custom_scenarios.yaml') as f:
    scenario_def = yaml.safe_load(f)

# Create scenario object
scenario = TestScenario(
    name=scenario_def['name'],
    prompt=scenario_def['prompt'],
    expected_files=scenario_def['expected_files'],
    validation_rules=scenario_def['validation_rules']
)

# Run test
result = run_scenario(scenario)
```

---

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Maintained By**: coding-workflow plugin team
