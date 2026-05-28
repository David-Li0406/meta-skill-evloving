---
name: github-cli-integration
description: Use GitHub CLI (gh) for authenticated API operations including repo access, file fetching, PR creation, and user management. Activate this skill when implementing GitHub integrations, working with gh CLI commands, creating PR workflows, handling GitHub authentication, or building testable GitHub clients using the Protocol pattern.
version: 1.0.0
tags:
  - github
  - cli
  - api
  - authentication
  - testing
---

# GitHub CLI Integration

Integrate with GitHub using the `gh` CLI tool following ContextHarness patterns for testability, error handling, and security.

## Core Concepts

### Protocol Pattern for Testability

Define a Protocol for GitHub operations to enable dependency injection and testing:

```python
from typing import Protocol, Optional
from pathlib import Path

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

    def fetch_directory(self, repo: str, path: str, dest: Path) -> bool:
        """Fetch a directory recursively from a repository."""
        ...
```

### Default Implementation

Implement the Protocol using `gh` CLI subprocess calls:

```python
import subprocess
import json
from pathlib import Path
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

    def get_username(self) -> str:
        """Get the current GitHub username."""
        try:
            result = subprocess.run(
                ["gh", "api", "/user", "--jq", ".login"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "github-user-unknown"
```

## Result Pattern for Error Handling

Use the Result pattern instead of exceptions for explicit error handling:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar, Union, Optional, Dict, Any

T = TypeVar("T")

class ErrorCode(Enum):
    """Standard error codes for operations."""
    NOT_FOUND = "not_found"
    ALREADY_EXISTS = "already_exists"
    PERMISSION_DENIED = "permission_denied"
    AUTH_REQUIRED = "auth_required"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class Success(Generic[T]):
    """Successful operation result."""
    value: T
    message: Optional[str] = None

@dataclass(frozen=True)
class Failure:
    """Failed operation result."""
    error: str
    code: ErrorCode
    details: Optional[Dict[str, Any]] = None

Result = Union[Success[T], Failure]
```

### Using Results with GitHub Operations

```python
def list_remote_skills(self) -> Result[List[Skill]]:
    """List available skills from remote registry."""
    if not self.github.check_auth():
        return Failure(
            error="GitHub CLI is not authenticated. Run 'gh auth login'.",
            code=ErrorCode.AUTH_REQUIRED,
        )

    if not self.github.check_repo_access(self.skills_repo):
        return Failure(
            error=f"Cannot access repository '{self.skills_repo}'",
            code=ErrorCode.PERMISSION_DENIED,
            details={"repo": self.skills_repo},
        )

    content = self.github.fetch_file(self.skills_repo, "skills.json")
    if content is None:
        return Failure(
            error="Skills registry not found",
            code=ErrorCode.NOT_FOUND,
        )

    try:
        registry = json.loads(content)
        skills = [parse_skill(s) for s in registry.get("skills", [])]
        return Success(value=skills)
    except json.JSONDecodeError as e:
        return Failure(
            error=f"Invalid registry: {e}",
            code=ErrorCode.VALIDATION_ERROR,
        )
```

## Testing with Mock Clients

Create mock implementations for testing without actual GitHub API calls:

```python
from typing import Optional
from pathlib import Path

class MockGitHubClient:
    """Mock GitHub client for testing."""

    def __init__(
        self,
        authenticated: bool = True,
        has_repo_access: bool = True,
        registry_content: Optional[str] = None,
        username: str = "test-user",
    ):
        self._authenticated = authenticated
        self._has_repo_access = has_repo_access
        self._registry_content = registry_content
        self._username = username
        self._files: dict[str, str] = {}
        self._fetch_directory_succeeds = True

    def check_auth(self) -> bool:
        return self._authenticated

    def check_repo_access(self, repo: str) -> bool:
        return self._has_repo_access

    def fetch_file(self, repo: str, path: str) -> Optional[str]:
        if path == "skills.json":
            return self._registry_content
        return self._files.get(path)

    def fetch_directory(self, repo: str, path: str, dest: Path) -> bool:
        if not self._fetch_directory_succeeds:
            return False
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SKILL.md").write_text("---\nname: test\n---\n# Test")
        return True

    def get_username(self) -> str:
        return self._username
```

### Test Examples

```python
import pytest
from your_module import SkillService, MockGitHubClient, Success, Failure, ErrorCode

class TestGitHubIntegration:
    """Tests using mock GitHub client."""

    def test_list_remote_not_authenticated(self) -> None:
        """Test failure when not authenticated."""
        client = MockGitHubClient(authenticated=False)
        service = SkillService(github_client=client)

        result = service.list_remote()

        assert isinstance(result, Failure)
        assert result.code == ErrorCode.AUTH_REQUIRED

    def test_list_remote_no_repo_access(self) -> None:
        """Test failure when no repo access."""
        client = MockGitHubClient(has_repo_access=False)
        service = SkillService(github_client=client)

        result = service.list_remote()

        assert isinstance(result, Failure)
        assert result.code == ErrorCode.PERMISSION_DENIED

    def test_list_remote_success(self) -> None:
        """Test successful listing."""
        registry = '{"skills": [{"name": "test", "version": "1.0.0"}]}'
        client = MockGitHubClient(registry_content=registry)
        service = SkillService(github_client=client)

        result = service.list_remote()

        assert isinstance(result, Success)
        assert len(result.value) == 1
```

## Common gh CLI Operations

### Authentication Commands

```bash
# Check authentication status
gh auth status

# Login interactively
gh auth login

# Login with token
gh auth login --with-token < token.txt

# Logout
gh auth logout
```

### API Operations

```bash
# Get repository info
gh api /repos/{owner}/{repo}

# Get file content (raw)
gh api /repos/{owner}/{repo}/contents/{path} \
  -H "Accept: application/vnd.github.raw+json"

# Get current user
gh api /user --jq ".login"

# Create a branch
gh api /repos/{owner}/{repo}/git/refs \
  -X POST \
  -f ref="refs/heads/{branch}" \
  -f sha="{commit_sha}"
```

### PR Operations

```bash
# Create pull request
gh pr create \
  --repo {owner}/{repo} \
  --title "feat: add feature" \
  --body "Description here" \
  --head {branch}

# List PRs
gh pr list --repo {owner}/{repo}

# Merge PR
gh pr merge {number} --repo {owner}/{repo} --squash
```

## Security Considerations

### Subprocess Safety

1. **Always use capture_output=True** to prevent output leakage
2. **Avoid shell=True** - use list arguments instead
3. **Handle FileNotFoundError** when gh CLI is not installed
4. **Use check=True carefully** - wrap in try/except for CalledProcessError

```python
# CORRECT: Safe subprocess call
try:
    result = subprocess.run(
        ["gh", "api", f"/repos/{repo}"],
        capture_output=True,
        text=True,
        check=True,
    )
except subprocess.CalledProcessError as e:
    return Failure(error=str(e.stderr), code=ErrorCode.UNKNOWN)
except FileNotFoundError:
    return Failure(error="gh CLI not installed", code=ErrorCode.NOT_FOUND)

# INCORRECT: Shell injection vulnerability
subprocess.run(f"gh api /repos/{repo}", shell=True)  # NEVER DO THIS
```

### Token Handling

- Never log or print authentication tokens
- Use `gh auth status` rather than checking token files directly
- Let `gh` CLI handle token storage and refresh
- Use environment variables for CI/CD tokens: `GH_TOKEN`

### Input Validation

Validate repository names and paths before use:

```python
import re

def validate_repo_name(repo: str) -> bool:
    """Validate repository name format (owner/repo)."""
    return bool(re.match(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$", repo))

def validate_skill_name(name: str) -> bool:
    """Validate skill name (alphanumeric, hyphens, underscores)."""
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))
```

## Rate Limiting

GitHub API has rate limits. Handle gracefully:

### Detection

```python
def check_rate_limit(self) -> dict:
    """Check current rate limit status."""
    try:
        result = subprocess.run(
            ["gh", "api", "/rate_limit", "--jq", ".rate"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return {"remaining": 0, "limit": 0}
```

### Handling

- Check `X-RateLimit-Remaining` header in responses
- Implement exponential backoff for 403 responses
- Cache API responses when appropriate
- Use conditional requests with `If-None-Match` header

## Troubleshooting Guide

### Authentication Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: command not found` | gh CLI not installed | Install: `brew install gh` or see [cli.github.com](https://cli.github.com) |
| `not logged in` | No authentication | Run `gh auth login` |
| `token expired` | OAuth token expired | Run `gh auth refresh` |
| `permission denied` | Insufficient scopes | Re-authenticate with required scopes |

### Repository Access Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `404 Not Found` | Repo doesn't exist or no access | Check repo name, verify access |
| `403 Forbidden` | Rate limited or blocked | Wait, check rate limits |
| `401 Unauthorized` | Token invalid | Re-authenticate |

### Common Fixes

```bash
# Verify authentication
gh auth status

# Re-authenticate
gh auth login --web

# Check rate limit
gh api /rate_limit --jq ".rate"

# Test repo access
gh api /repos/{owner}/{repo} --silent && echo "OK" || echo "FAIL"

# Debug API calls
gh api /repos/{owner}/{repo} --verbose
```

## Service Integration Pattern

Inject GitHub client into services for testability:

```python
class SkillService:
    """Service for managing skills."""

    def __init__(
        self,
        github_client: Optional[GitHubClient] = None,
        skills_repo: str = "org/skills-repo",
    ):
        """Initialize with optional GitHub client.
        
        Args:
            github_client: GitHub client for API operations.
                          Defaults to DefaultGitHubClient.
            skills_repo: Skills repository (owner/repo format)
        """
        self.github = github_client or DefaultGitHubClient()
        self.skills_repo = skills_repo
```

## Quick Reference

### Subprocess Template

```python
def gh_api_call(endpoint: str) -> Result[dict]:
    """Template for gh API calls with proper error handling."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            check=True,
        )
        return Success(value=json.loads(result.stdout))
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else "Unknown error"
        return Failure(error=error_msg, code=ErrorCode.UNKNOWN)
    except FileNotFoundError:
        return Failure(
            error="GitHub CLI not installed",
            code=ErrorCode.NOT_FOUND,
        )
    except json.JSONDecodeError as e:
        return Failure(
            error=f"Invalid JSON response: {e}",
            code=ErrorCode.VALIDATION_ERROR,
        )
```

### Checklist for New Operations

- [ ] Define method in Protocol
- [ ] Implement in DefaultGitHubClient
- [ ] Add mock behavior to MockGitHubClient
- [ ] Return Result type (Success/Failure)
- [ ] Handle FileNotFoundError for missing gh CLI
- [ ] Handle CalledProcessError for API failures
- [ ] Validate inputs before subprocess calls
- [ ] Write tests with mock client

---

_Skill: github-cli-integration v1.0.0 | Last updated: 2025-12-31_
