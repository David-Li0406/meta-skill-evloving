---
name: tm-tests
description: Generate security test cases from the threat model. Creates test scenarios for each threat and control verification tests. Use when creating security tests, generating penetration test cases, building security regression tests, or validating threat mitigations.
allowed-tools: Read, Write, Glob
---

# Security Test Generation

## Purpose

Generate security test cases from your threat model to:

- Create attack scenario tests for each threat
- Generate control verification tests
- Build security regression test suites
- Map test coverage to threats and controls

## Usage

```
/tm-tests [--format markdown|jest|pytest|playwright] [--category <name>] [--control <id>] [--output <path>]
```

**Arguments**:
- `--format`: Test output format (default: markdown)
- `--category`: Filter by threat category
- `--control`: Generate tests for specific control
- `--output`: Output directory

## Test Categories

### Attack Tests (Negative Tests)
Tests that attempt to exploit vulnerabilities:
- Verify threat is blocked/detected
- Simulate attack scenarios
- Test security boundaries

### Control Tests (Positive Tests)
Tests that verify security controls work:
- Verify control is active
- Test expected behavior
- Validate configuration

### Regression Tests
Tests that prevent security regressions:
- Run on every commit/PR
- Verify fixes remain in place
- Detect control degradation

## Test Output Formats

### Markdown Documentation
```markdown
# Security Test Cases

## Authentication Tests

### TEST-001: Credential Stuffing Prevention

**Threat**: THREAT-001 - Credential Stuffing Attack
**Control**: CONTROL-001 - Rate Limiting

#### Test Scenario
1. Attempt 6 failed logins from same IP within 1 minute
2. Expected: 6th request should be blocked (429 Too Many Requests)

#### Steps
1. POST /api/auth/login with invalid credentials
2. Repeat 5 more times
3. Verify 6th request returns 429

#### Expected Results
- First 5 requests: 401 Unauthorized
- 6th request: 429 Too Many Requests
- Response includes retry-after header

#### Pass Criteria
- Rate limit enforced at configured threshold
- Appropriate error response returned
- Event logged for security monitoring
```

### Jest/TypeScript
```typescript
// security-tests/auth-security.test.ts

describe('Authentication Security', () => {
  describe('Credential Stuffing Prevention', () => {
    // THREAT-001: Credential Stuffing Attack
    // CONTROL-001: Rate Limiting

    it('should block after 5 failed attempts from same IP', async () => {
      const loginAttempt = () =>
        request(app)
          .post('/api/auth/login')
          .send({ email: 'test@example.com', password: 'wrong' });

      // Make 5 failed attempts
      for (let i = 0; i < 5; i++) {
        const response = await loginAttempt();
        expect(response.status).toBe(401);
      }

      // 6th attempt should be blocked
      const blocked = await loginAttempt();
      expect(blocked.status).toBe(429);
      expect(blocked.headers['retry-after']).toBeDefined();
    });

    it('should return consistent error messages', async () => {
      // Test with valid email, wrong password
      const validEmail = await request(app)
        .post('/api/auth/login')
        .send({ email: 'existing@example.com', password: 'wrong' });

      // Test with invalid email
      const invalidEmail = await request(app)
        .post('/api/auth/login')
        .send({ email: 'nonexistent@example.com', password: 'wrong' });

      // Messages should be identical to prevent enumeration
      expect(validEmail.body.message).toBe(invalidEmail.body.message);
    });

    it('should log failed authentication attempts', async () => {
      const spy = jest.spyOn(logger, 'warn');

      await request(app)
        .post('/api/auth/login')
        .send({ email: 'test@example.com', password: 'wrong' });

      expect(spy).toHaveBeenCalledWith(
        expect.objectContaining({
          event: 'authentication_failure',
          email: 'test@example.com',
        })
      );
    });
  });

  describe('Session Management', () => {
    // THREAT-003: Session Hijacking
    // CONTROL-003: Secure Session Configuration

    it('should invalidate session on password change', async () => {
      const { sessionId } = await login('user@example.com', 'password');

      await changePassword('user@example.com', 'newpassword');

      const response = await request(app)
        .get('/api/profile')
        .set('Cookie', `session=${sessionId}`);

      expect(response.status).toBe(401);
    });

    it('should enforce session timeout', async () => {
      const { sessionId } = await login('user@example.com', 'password');

      // Fast-forward time past session timeout
      jest.advanceTimersByTime(31 * 60 * 1000); // 31 minutes

      const response = await request(app)
        .get('/api/profile')
        .set('Cookie', `session=${sessionId}`);

      expect(response.status).toBe(401);
    });
  });
});
```

### Pytest
```python
# tests/security/test_auth_security.py

import pytest
from fastapi.testclient import TestClient

class TestAuthenticationSecurity:
    """
    Security tests for authentication threats.
    """

    class TestCredentialStuffingPrevention:
        """
        THREAT-001: Credential Stuffing Attack
        CONTROL-001: Rate Limiting
        """

        def test_blocks_after_failed_attempts(self, client: TestClient):
            """Should block after 5 failed login attempts from same IP."""
            for i in range(5):
                response = client.post(
                    "/api/auth/login",
                    json={"email": "test@example.com", "password": "wrong"}
                )
                assert response.status_code == 401

            # 6th attempt should be blocked
            response = client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "wrong"}
            )
            assert response.status_code == 429
            assert "retry-after" in response.headers

        def test_returns_consistent_error_messages(self, client: TestClient):
            """Should return identical messages for valid/invalid emails."""
            valid_email = client.post(
                "/api/auth/login",
                json={"email": "existing@example.com", "password": "wrong"}
            )
            invalid_email = client.post(
                "/api/auth/login",
                json={"email": "nonexistent@example.com", "password": "wrong"}
            )

            assert valid_email.json()["message"] == invalid_email.json()["message"]


    class TestInputValidation:
        """
        THREAT-002: SQL Injection
        CONTROL-002: Parameterized Queries
        """

        @pytest.mark.parametrize("payload", [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
        ])
        def test_sql_injection_blocked(self, client: TestClient, payload: str):
            """Should block SQL injection attempts."""
            response = client.get(f"/api/users?search={payload}")
            assert response.status_code in [400, 200]
            # If 200, verify no SQL error in response
            if response.status_code == 200:
                assert "sql" not in response.text.lower()
                assert "error" not in response.text.lower()
```

## Test Matrix

### test-matrix.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "coverage": {
    "threats_with_tests": 42,
    "threats_without_tests": 5,
    "controls_with_tests": 25,
    "controls_without_tests": 4
  },
  "matrix": [
    {
      "threat_id": "threat-001",
      "threat_title": "Credential Stuffing",
      "test_ids": ["test-001", "test-002", "test-003"],
      "controls_tested": ["control-001", "control-002"],
      "coverage": "full"
    }
  ],
  "untested": {
    "threats": ["threat-045", "threat-046"],
    "controls": ["control-028"]
  }
}
```

## Instructions for Claude

When executing this skill:

1. **Load threat model**:
   - Read `.threatmodel/state/threats.json`
   - Read `.threatmodel/state/controls.json`

2. **Group tests by category**:
   - Authentication tests
   - Authorization tests
   - Input validation tests
   - Cryptography tests
   - Session management tests
   - Error handling tests

3. **For each threat**:
   - Create attack scenario test
   - Describe test steps
   - Define expected results
   - Link to mitigating controls

4. **For each control**:
   - Create verification test
   - Test both positive and negative cases
   - Validate configuration

5. **Generate in requested format**:
   - Markdown for documentation
   - Jest/Pytest for automation
   - Include proper test structure

6. **Create coverage matrix**:
   - Map tests to threats
   - Map tests to controls
   - Identify gaps

7. **Report summary**:
   ```
   Test Generation Complete
   ========================

   Format: jest

   Tests Generated:
     Authentication: 12 tests
     Authorization: 8 tests
     Input Validation: 15 tests
     Session Management: 6 tests
     Error Handling: 4 tests
     Total: 45 tests

   Coverage:
     Threats with tests: 42/47 (89%)
     Controls with tests: 25/29 (86%)

   Untested:
     - THREAT-045: Complex attack scenario
     - THREAT-046: Requires manual testing
     - CONTROL-028: Infrastructure control

   Files Created:
     .threatmodel/tests/auth-security.test.ts
     .threatmodel/tests/authz-security.test.ts
     .threatmodel/tests/input-validation.test.ts
     .threatmodel/tests/test-matrix.json

   Next Steps:
     1. Review generated tests
     2. Add to CI/CD pipeline
     3. Create manual test procedures for untested items
   ```
