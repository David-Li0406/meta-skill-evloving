---
name: python-service-with-protocol
description: |
  Guide for implementing services with Protocol-based dependency injection in Python.
  Use when creating services that interact with external systems (APIs, databases, filesystems).
  Enables clean testing through mock injection while keeping production code simple.
version: 1.0.0
tags:
  - python
  - testing
  - dependency-injection
  - architecture
  - protocols
---

# Python Service with Protocol Dependency Injection

## Overview

This skill provides guidance for implementing Python services using the Protocol pattern for dependency injection. This pattern enables:

- **Testability**: Easy injection of mock implementations for unit testing
- **Flexibility**: Swap implementations without changing service code
- **Type Safety**: Full type checking support via `typing.Protocol`
- **Clean Architecture**: Clear separation between interfaces and implementations

## When to Use This Pattern

Use this pattern when:

1. **External Dependencies**: Your service calls external APIs, CLIs, or systems
2. **Unit Testing Required**: You need to test business logic in isolation
3. **Multiple Implementations**: Different backends (file vs memory, API vs mock)
4. **Side Effects**: Operations that shouldn't run during tests (network calls, file I/O)

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                       MyService                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ def __init__(                                        │    │
│  │     self,                                            │    │
│  │     client: Optional[ClientProtocol] = None          │    │
│  │ ):                                                   │    │
│  │     self.client = client or DefaultClient()          │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼───────┐       ┌───────▼───────┐
        │ DefaultClient │       │  MockClient   │
        │ (production)  │       │  (testing)    │
        └───────────────┘       └───────────────┘
```

## Step 1: Define the Protocol

Create a Protocol that defines the contract for your external dependency:

```python
from typing import Optional, Protocol


class GitHubClient(Protocol):
    """Protocol for GitHub API operations.

    Allows for dependency injection and testing.
    """

    def check_auth(self) -> bool:
        """Check if authenticated with GitHub."""
        ...

    def check_repo_access(self, repo: str) -> bool:
        """Check if user has access to a repository."""
        ...

    def fetch_file(self, repo: str, path: str) -> Optional[str]:
        """Fetch a file's content from a repository."""
        ...
```

### Protocol Best Practices

1. **Use `...` (Ellipsis)**: Protocol methods use `...` not `pass`
2. **Add Docstrings**: Document what each method should do
3. **Keep Focused**: One protocol per external system
4. **Return Types**: Always specify return types

## Step 2: Create the Default Implementation

Implement the protocol for production use:

```python
import subprocess
from typing import Optional


class DefaultGitHubClient:
    """Default GitHub client using gh CLI."""

    def check_auth(self) -> bool:
        """Check if GitHub CLI is authenticated."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def check_repo_access(self, repo: str) -> bool:
        """Check if user has access to the repository."""
        result = subprocess.run(
            ["gh", "api", f"/repos/{repo}", "--silent"],
            capture_output=True,
        )
        return result.returncode == 0

    def fetch_file(self, repo: str, path: str) -> Optional[str]:
        """Fetch a file's content from a repository."""
        try:
            result = subprocess.run(
                [
                    "gh", "api",
                    f"/repos/{repo}/contents/{path}",
                    "-H", "Accept: application/vnd.github.raw+json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return None
```

## Step 3: Create the Service with Optional DI

Design your service to accept an optional protocol implementation:

```python
from typing import List, Optional

from context_harness.primitives import (
    ErrorCode,
    Failure,
    Result,
    Skill,
    Success,
)


class SkillService:
    """Service for managing skills.

    Example:
        # Production usage (default client)
        service = SkillService()

        # Testing usage (mock client)
        mock_client = MockGitHubClient(authenticated=False)
        service = SkillService(github_client=mock_client)
    """

    def __init__(
        self,
        github_client: Optional[GitHubClient] = None,
        skills_repo: str = "org/skills-repo",
    ):
        """Initialize the skill service.

        Args:
            github_client: GitHub client for API operations
            skills_repo: Skills repository (owner/repo format)
        """
        self.github = github_client or DefaultGitHubClient()
        self.skills_repo = skills_repo

    def list_remote(self) -> Result[List[Skill]]:
        """List available skills from remote registry."""
        # Use self.github - works with either real or mock client
        if not self.github.check_auth():
            return Failure(
                error="GitHub CLI is not authenticated",
                code=ErrorCode.AUTH_REQUIRED,
            )

        # ... rest of implementation
```

### Service Pattern Best Practices

1. **Type Hint Protocol**: `github_client: Optional[GitHubClient]`
2. **Default to Real**: `self.github = github_client or DefaultGitHubClient()`
3. **Store as Attribute**: Assign to `self.github` for use in methods
4. **Document Both Uses**: Show production and testing usage in docstring

## Step 4: Create Mock for Testing

Create a mock implementation with controllable behavior:

```python
from typing import Optional


class MockGitHubClient:
    """Mock GitHub client for testing."""

    def __init__(
        self,
        authenticated: bool = True,
        has_repo_access: bool = True,
        registry_content: Optional[str] = None,
        username: str = "test-user",
    ):
        """Initialize mock with controllable behavior.

        Args:
            authenticated: Whether check_auth() returns True
            has_repo_access: Whether check_repo_access() returns True
            registry_content: Content to return from fetch_file
            username: Username to return from get_username
        """
        self._authenticated = authenticated
        self._has_repo_access = has_repo_access
        self._registry_content = registry_content
        self._username = username
        self._files: dict[str, str] = {}

    def check_auth(self) -> bool:
        return self._authenticated

    def check_repo_access(self, repo: str) -> bool:
        return self._has_repo_access

    def fetch_file(self, repo: str, path: str) -> Optional[str]:
        if path == "skills.json":
            return self._registry_content
        return self._files.get(path)
```

### Mock Best Practices

1. **Constructor Controls**: Set behavior via `__init__` parameters
2. **Sensible Defaults**: Default to "happy path" (authenticated, access granted)
3. **Stateful Mocks**: Use attributes like `_files` for complex scenarios
4. **Clear Names**: Parameter names should explain what they control

## Step 5: Write Tests with Mocks

```python
import pytest
from context_harness.primitives import ErrorCode, Failure, Success
from context_harness.services.skill_service import SkillService


class TestSkillServiceListRemote:
    """Tests for SkillService.list_remote()."""

    def test_list_remote_returns_skills(self) -> None:
        """Test listing remote skills returns skills from registry."""
        registry = '{"skills": [{"name": "skill-a"}]}'
        client = MockGitHubClient(registry_content=registry)
        service = SkillService(github_client=client)

        result = service.list_remote()

        assert isinstance(result, Success)
        assert len(result.value) == 1
        assert result.value[0].name == "skill-a"

    def test_list_remote_not_authenticated(self) -> None:
        """Test list_remote fails when not authenticated."""
        client = MockGitHubClient(authenticated=False)
        service = SkillService(github_client=client)

        result = service.list_remote()

        assert isinstance(result, Failure)
        assert result.code == ErrorCode.AUTH_REQUIRED
```

## Common Patterns in This Codebase

| Service | Protocol | Default | Mock/Memory |
|---------|----------|---------|-------------|
| SkillService | GitHubClient | DefaultGitHubClient | MockGitHubClient |
| OAuthService | TokenStorageProtocol | FileTokenStorage | MemoryTokenStorage |
| (various) | StorageProtocol | FileStorage | MemoryStorage |

## Anti-Patterns to Avoid

### ❌ Don't Hard-Code Dependencies

```python
# BAD: Can't test without calling GitHub
class SkillService:
    def __init__(self):
        self.github = DefaultGitHubClient()  # No way to override!
```

### ❌ Don't Require Protocol in Tests

```python
# BAD: Test depends on actual protocol
def test_list_remote():
    service = SkillService()  # Uses real GitHub client!
    result = service.list_remote()
```

## Files in This Pattern

- **Protocols**: `src/context_harness/storage/protocol.py`
- **Services**: `src/context_harness/services/`
  - `skill_service.py` - GitHubClient Protocol example
  - `oauth_service.py` - TokenStorageProtocol example
- **Storage**: `src/context_harness/storage/`
  - `file_storage.py` - Production implementation
  - `memory_storage.py` - Test implementation
- **Tests**: `tests/unit/services/`
  - `test_skill_service.py` - MockGitHubClient example
  - `test_oauth_service.py` - MemoryTokenStorage example

---

_Skill: python-service-with-protocol v1.0.0 | Last updated: 2025-12-30_
