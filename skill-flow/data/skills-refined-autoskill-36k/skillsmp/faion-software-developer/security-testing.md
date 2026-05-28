---
id: security-testing
name: "Security Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Security Testing

## Overview

Security testing identifies vulnerabilities in applications before they can be exploited. This includes static analysis, dynamic testing, dependency scanning, and penetration testing to ensure applications handle data safely and resist attacks.

## When to Use

- Before deploying to production
- After adding authentication/authorization features
- When handling sensitive data (PII, payments)
- Regular security audits and compliance checks
- After dependency updates

## Key Principles

- **Defense in depth**: Multiple layers of security testing
- **Shift left**: Test security early in development
- **Automate**: Include security in CI/CD pipeline
- **Stay updated**: Track new vulnerabilities and patches
- **Assume breach**: Test detection and response capabilities

## Best Practices

### OWASP Top 10 Testing

```python
# Test for common vulnerabilities

import pytest
from fastapi.testclient import TestClient

class TestSecurityVulnerabilities:
    """Tests based on OWASP Top 10."""

    # A01: Broken Access Control
    def test_unauthorized_access_to_other_user_data(self, client, user_token, other_user):
        """Ensure users cannot access other users' data."""
        response = client.get(
            f"/api/users/{other_user.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 403

    def test_admin_endpoint_requires_admin_role(self, client, user_token):
        """Regular users cannot access admin endpoints."""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 403

    # A02: Cryptographic Failures
    def test_passwords_are_hashed(self, db_session):
        """Verify passwords are not stored in plain text."""
        user = create_user(password="mypassword123")
        db_session.add(user)
        db_session.commit()

        assert user.password_hash != "mypassword123"
        assert len(user.password_hash) > 50  # Proper hash length

    def test_sensitive_data_not_in_logs(self, caplog):
        """Ensure sensitive data is not logged."""
        with caplog.at_level(logging.DEBUG):
            process_payment(card_number="4111111111111111", cvv="123")

        log_text = caplog.text
        assert "4111111111111111" not in log_text
        assert "123" not in log_text

    # A03: Injection
    def test_sql_injection_prevented(self, client):
        """SQL injection attempts should not work."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1 OR 1=1",
            "admin'--",
            "1; SELECT * FROM users",
        ]
        for payload in malicious_inputs:
            response = client.get(f"/api/users?search={payload}")
            assert response.status_code in [200, 400]  # Not 500

    def test_xss_prevented(self, client, user_token):
        """XSS payloads should be escaped."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
        ]
        for payload in xss_payloads:
            response = client.post(
                "/api/comments",
                json={"content": payload},
                headers={"Authorization": f"Bearer {user_token}"}
            )
            # Content should be escaped or rejected
            if response.status_code == 201:
                assert payload not in response.json()["content"]

    # A05: Security Misconfiguration
    def test_debug_mode_disabled_in_production(self, app_config):
        """Debug mode should be off in production."""
        if app_config.get("ENV") == "production":
            assert app_config.get("DEBUG") is False

    def test_security_headers_present(self, client):
        """Verify security headers are set."""
        response = client.get("/")

        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert "X-Frame-Options" in response.headers
        assert "Strict-Transport-Security" in response.headers

    # A07: Identification and Authentication Failures
    def test_brute_force_protection(self, client):
        """Account lockout after failed attempts."""
        for i in range(10):
            response = client.post("/api/auth/login", json={
                "email": "user@example.com",
                "password": "wrongpassword"
            })

        # Should be rate limited or locked
        assert response.status_code in [429, 423]

    def test_session_invalidated_on_logout(self, client, user_token):
        """Old tokens should not work after logout."""
        # Logout
        client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        # Try to use old token
        response = client.get(
            "/api/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 401

    # A08: Software and Data Integrity Failures
    def test_csrf_protection(self, client, user_token):
        """State-changing operations require CSRF token."""
        response = client.post(
            "/api/settings",
            json={"theme": "dark"},
            headers={"Authorization": f"Bearer {user_token}"}
            # Missing CSRF token
        )
        # Should require CSRF token for cookie-based auth
        # (JWT APIs may not need CSRF)
```

### Static Application Security Testing (SAST)

```yaml
# .github/workflows/security.yml
name: Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Python - Bandit
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json || true

      # Python - Safety (dependency check)
      - name: Check dependencies for vulnerabilities
        run: |
          pip install safety
          safety check -r requirements.txt --json > safety-report.json || true

      # JavaScript - npm audit
      - name: npm audit
        run: npm audit --json > npm-audit.json || true

      # Semgrep - Multi-language SAST
      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json
            npm-audit.json
```

### Bandit Configuration

```yaml
# .bandit.yaml
skips: []

exclude_dirs:
  - tests
  - venv
  - .venv

tests:
  - B101  # assert_used
  - B102  # exec_used
  - B103  # set_bad_file_permissions
  - B104  # hardcoded_bind_all_interfaces
  - B105  # hardcoded_password_string
  - B106  # hardcoded_password_funcarg
  - B107  # hardcoded_password_default
  - B108  # hardcoded_tmp_directory
  - B110  # try_except_pass
  - B112  # try_except_continue
  - B201  # flask_debug_true
  - B301  # pickle
  - B302  # marshal
  - B303  # md5
  - B304  # des
  - B305  # cipher
  - B306  # mktemp_q
  - B307  # eval
  - B308  # mark_safe
  - B310  # urllib_urlopen
  - B311  # random
  - B312  # telnetlib
  - B313  # xml_bad_cElementTree
  - B314  # xml_bad_ElementTree
  - B315  # xml_bad_expatreader
  - B316  # xml_bad_expatbuilder
  - B317  # xml_bad_sax
  - B318  # xml_bad_minidom
  - B319  # xml_bad_pulldom
  - B320  # xml_bad_etree
  - B321  # ftplib
  - B323  # unverified_context
  - B324  # hashlib_insecure_functions
  - B501  # request_with_no_cert_validation
  - B502  # ssl_with_bad_version
  - B503  # ssl_with_bad_defaults
  - B504  # ssl_with_no_version
  - B505  # weak_cryptographic_key
  - B506  # yaml_load
  - B507  # ssh_no_host_key_verification
  - B601  # paramiko_calls
  - B602  # subprocess_popen_with_shell_equals_true
  - B603  # subprocess_without_shell_equals_true
  - B604  # any_other_function_with_shell_equals_true
  - B605  # start_process_with_a_shell
  - B606  # start_process_with_no_shell
  - B607  # start_process_with_partial_path
  - B608  # hardcoded_sql_expressions
  - B609  # linux_commands_wildcard_injection
  - B610  # django_extra_used
  - B611  # django_rawsql_used
  - B701  # jinja2_autoescape_false
  - B702  # use_of_mako_templates
  - B703  # django_mark_safe
```

### Dependency Scanning

```python
# requirements-security.txt
# Tools for security scanning

bandit>=1.7.0        # Python SAST
safety>=2.0.0        # Dependency vulnerability check
pip-audit>=2.0.0     # Python dependency audit

# Example: Custom dependency check script
# scripts/check_dependencies.py

import subprocess
import json
import sys

def run_safety_check():
    """Check dependencies with Safety."""
    result = subprocess.run(
        ["safety", "check", "--json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        vulnerabilities = json.loads(result.stdout)
        print(f"Found {len(vulnerabilities)} vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"  - {vuln['package_name']}: {vuln['vulnerability_id']}")
            print(f"    Severity: {vuln.get('severity', 'unknown')}")
            print(f"    Fix: upgrade to {vuln.get('fixed_in', 'unknown')}")
        return False
    return True

def run_pip_audit():
    """Check dependencies with pip-audit."""
    result = subprocess.run(
        ["pip-audit", "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        findings = json.loads(result.stdout)
        for finding in findings:
            print(f"  - {finding['name']} {finding['version']}")
            for vuln in finding['vulns']:
                print(f"    {vuln['id']}: {vuln['description'][:100]}...")
        return False
    return True

if __name__ == "__main__":
    safe = run_safety_check() and run_pip_audit()
    sys.exit(0 if safe else 1)
```

### Secrets Detection

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

```python
# Test for secrets in code
import pytest
import re
from pathlib import Path

SECRET_PATTERNS = [
    (r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "API key"),
    (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
    (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
    (r'aws_access_key_id\s*=\s*["\']AKIA[A-Z0-9]{16}["\']', "AWS key"),
    (r'-----BEGIN (RSA |EC )?PRIVATE KEY-----', "Private key"),
]

def test_no_secrets_in_source_code():
    """Ensure no secrets are hardcoded in source files."""
    source_dir = Path("src")
    violations = []

    for file_path in source_dir.rglob("*.py"):
        content = file_path.read_text()
        for pattern, secret_type in SECRET_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append(f"{file_path}: {secret_type}")

    assert not violations, f"Secrets found in code:\n" + "\n".join(violations)
```

### Input Validation Testing

```python
import pytest
from pydantic import ValidationError

class TestInputValidation:

    @pytest.mark.parametrize("email", [
        "not-an-email",
        "@nodomain.com",
        "spaces in@email.com",
        "a" * 256 + "@example.com",  # Too long
    ])
    def test_invalid_email_rejected(self, email):
        """Invalid emails should be rejected."""
        with pytest.raises(ValidationError):
            UserCreate(email=email, password="valid123")

    @pytest.mark.parametrize("password", [
        "short",           # Too short
        "nouppercase1",    # No uppercase
        "NOLOWERCASE1",    # No lowercase
        "NoDigitsHere",    # No digits
    ])
    def test_weak_password_rejected(self, password):
        """Weak passwords should be rejected."""
        with pytest.raises(ValidationError):
            UserCreate(email="valid@example.com", password=password)

    def test_file_upload_type_validation(self, client, auth_token):
        """Only allowed file types should be accepted."""
        # Try uploading executable
        response = client.post(
            "/api/upload",
            files={"file": ("malware.exe", b"MZ...", "application/x-msdownload")},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400

    def test_file_upload_size_limit(self, client, auth_token):
        """Large files should be rejected."""
        large_content = b"x" * (10 * 1024 * 1024 + 1)  # > 10MB
        response = client.post(
            "/api/upload",
            files={"file": ("large.txt", large_content, "text/plain")},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 413  # Request Entity Too Large

    def test_path_traversal_prevented(self, client, auth_token):
        """Path traversal attempts should be blocked."""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2fetc/passwd",
        ]
        for path in malicious_paths:
            response = client.get(
                f"/api/files/{path}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code in [400, 404]
```

### Rate Limiting Tests

```python
import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test that rate limiting is enforced."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        responses = []

        # Send requests rapidly
        for _ in range(100):
            response = await client.get("/api/public")
            responses.append(response.status_code)

        # Should see rate limiting kick in
        rate_limited = sum(1 for s in responses if s == 429)
        assert rate_limited > 0, "Rate limiting not enforced"

@pytest.mark.asyncio
async def test_rate_limiting_by_endpoint():
    """Different endpoints should have different rate limits."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Login endpoint should have stricter limits
        login_responses = []
        for _ in range(20):
            response = await client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "wrong"
            })
            login_responses.append(response.status_code)

        # Should be rate limited quickly
        assert 429 in login_responses
```

## Anti-patterns

- **Security as afterthought**: Not testing security from the start
- **Only testing happy paths**: Not testing attack scenarios
- **Ignoring dependency vulnerabilities**: Not scanning third-party code
- **Hardcoded test credentials**: Using real secrets in tests
- **No automation**: Manual-only security testing
- **Skipping low severity**: All vulnerabilities matter

## References

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Semgrep Rules](https://semgrep.dev/explore)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
