# Coding Standards

## Purpose

Consistent code style reduces cognitive load, speeds reviews, and prevents bikeshedding.

**Rule:** Standards are enforced by tools (linters, formatters), not by memory or code review comments.

## Python Standards

### Style Guide: PEP 8 + Black

**Formatter:** Black (line length: 100)

```python
# File: pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.flake8]
max-line-length = 100
extend-ignore = E203, W503  # Black compatibility
```

### Naming Conventions

```python
# Modules: lowercase_with_underscores
# file: user_service.py

# Classes: PascalCase
class UserService:
    pass

# Functions/methods: lowercase_with_underscores
def create_user(email: str) -> User:
    pass

# Constants: UPPERCASE_WITH_UNDERSCORES
MAX_LOGIN_ATTEMPTS = 3

# Private: _leading_underscore
def _internal_helper() -> None:
    pass

# Type variables: PascalCase
T = TypeVar('T')
```

### Type Annotations

**Always use type hints:**

```python
# ✅ Good - explicit types
def get_user(user_id: UUID) -> Optional[User]:
    ...

async def create_user(request: CreateUserRequest, db: Session) -> User:
    ...

# ❌ Bad - no types
def get_user(user_id):
    ...
```

### Docstrings

**Use for public functions/classes:**

```python
def create_user(request: CreateUserRequest, db: Session) -> User:
    """
    Create a new user with validation.

    Args:
        request: User creation data (validated DTO)
        db: Database session

    Returns:
        Created user entity

    Raises:
        DuplicateEntityError: If email already exists
        ValidationError: If request data invalid
    """
    ...
```

### Imports

**Order:**
1. Standard library
2. Third-party packages
3. Local application imports

```python
# Standard library
import os
from typing import Optional, List
from uuid import UUID

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Local
from app.models.user import User
from app.schemas.user_schema import CreateUserRequest
from app.services.user_service import UserService
```

**Use `isort` to enforce:**
```bash
uv run isort app/ tests/
```

## TypeScript/JavaScript Standards

### Style Guide: ESLint + Prettier

**Configuration:**

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:vue/vue3-recommended",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}

// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

### Naming Conventions

```typescript
// Files: camelCase or kebab-case
// user-service.ts or userService.ts

// Interfaces: PascalCase
interface UserResponse {
  id: string;
  email: string;
}

// Types: PascalCase
type UserStatus = 'active' | 'inactive';

// Functions: camelCase
function createUser(request: CreateUserRequest): Promise<User> {
  ...
}

// Constants: UPPERCASE_WITH_UNDERSCORES
const MAX_LOGIN_ATTEMPTS = 3;

// Components: PascalCase
const CreateUserForm = () => { ... };
```

### Type Annotations

**Always explicit, never `any`:**

```typescript
// ✅ Good - explicit types
function getUser(userId: string): Promise<UserResponse> {
  ...
}

const users: UserResponse[] = [];

// ❌ Bad - any or implicit
function getUser(userId: string): Promise<any> {
  ...
}

const users = [];  // Implicit any[]
```

### Vue 3 Composition API

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';
import type { CreateUserRequest } from '@/types/api/users';

// Props with types
interface Props {
  initialData?: Partial<CreateUserRequest>;
}
const props = defineProps<Props>();

// Emits with types
const emit = defineEmits<{
  submit: [payload: CreateUserRequest];
  cancel: [];
}>();

// Reactive state with types
const formData = ref<CreateUserRequest>({
  email: '',
  first_name: '',
  last_name: '',
});

// Computed with explicit return type
const isValid = computed((): boolean => {
  return formData.value.email !== '' && formData.value.first_name !== '';
});
</script>
```

## General Standards

### File Organization

```
app/
├── api/              # API routes/endpoints
│   └── v1/
├── services/         # Business logic
├── repositories/     # Data access
├── models/           # Database models
├── schemas/          # DTOs (Pydantic)
└── core/             # Config, security, utils

frontend/src/
├── components/       # Vue components
├── views/            # Page views
├── stores/           # Pinia stores
├── api/              # API clients
├── types/            # TypeScript interfaces
└── utils/            # Helper functions
```

### Function Length

**Target:** < 50 lines per function

**If longer:** Extract helper functions

```python
# ✅ Good - small focused functions
def create_user(request: CreateUserRequest, db: Session) -> User:
    _validate_email_unique(request.email, db)
    user = _build_user_entity(request)
    return _persist_user(user, db)

def _validate_email_unique(email: str, db: Session) -> None:
    if db.query(User).filter(User.email == email).first():
        raise DuplicateEntityError("User", "email", email)

# ❌ Bad - monolithic function
def create_user(request: CreateUserRequest, db: Session) -> User:
    # 200 lines of validation, entity creation, persistence...
```

### Comments

**Good comments explain WHY, not WHAT:**

```python
# ✅ Good - explains business rule
# Hash password with bcrypt (12 rounds) per security policy SEC-001
password_hash = bcrypt.hashpw(password, bcrypt.gensalt(12))

# ❌ Bad - explains obvious code
# Hash the password
password_hash = bcrypt.hashpw(password, bcrypt.gensalt(12))
```

### Magic Numbers

**Extract to named constants:**

```python
# ✅ Good
MAX_LOGIN_ATTEMPTS = 3
BCRYPT_ROUNDS = 12

if login_attempts > MAX_LOGIN_ATTEMPTS:
    lock_account()

# ❌ Bad
if login_attempts > 3:
    lock_account()
```

### Error Messages

**User-facing:**
- Clear and actionable
- No technical jargon
- Suggest next steps

```python
# ✅ Good
"Email address is already registered. Please sign in or use a different email."

# ❌ Bad
"DuplicateEntityError: User with email=john@example.com already exists in table users"
```

**Developer-facing (logs):**
- Include context
- Include identifiers
- Include stack traces

```python
logger.error(
    f"Failed to create user: email={request.email}, error={e}",
    exc_info=True,
    extra={"user_email": request.email}
)
```

## Code Review Standards

### Before Requesting Review

- [ ] All validation gates pass
- [ ] Code follows style guide (automated)
- [ ] Functions are small and focused
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No TODO comments without issue number

### Review Checklist

**Automated (caught by gates):**
- Style violations
- Type errors
- Test failures
- Linting issues

**Manual (reviewer focuses on):**
- Business logic correctness
- Security vulnerabilities
- Performance concerns
- API design
- Error handling completeness

## Standards Enforcement

### Automated Tools

```bash
# Python
uv run black app/ tests/           # Format
uv run isort app/ tests/           # Sort imports
uv run flake8 app/ tests/          # Lint
uv run mypy app/                   # Type check

# TypeScript
npm run format -- --write          # Format
npm run lint -- --fix              # Lint
npm run type-check                 # Type check
```

### Pre-commit Hook

```bash
# File: .git/hooks/pre-commit
#!/bin/sh
uv run black --check app/ tests/ || exit 1
uv run flake8 app/ tests/ || exit 1
uv run mypy app/ || exit 1
```

### CI/CD

```yaml
# .github/workflows/ci.yml
- name: Check Style
  run: |
    uv run black --check app/
    uv run flake8 app/
    npm run lint
```

## Anti-Patterns

**Don't:**
- Debate style in code review (use automated tools)
- Mix formatting changes with logic changes
- Ignore linter warnings
- Use `# noqa` or `// eslint-disable` without justification
- Commit code with `any` or `dict` types

**Do:**
- Configure tools once, enforce automatically
- Run formatters before commit
- Fix all linting violations
- Document exceptions to rules
- Use strict type checking

---

**Remember:** Standards exist to reduce cognitive load, not to be a burden. Configure tools to enforce automatically, focus code review on logic and design.
