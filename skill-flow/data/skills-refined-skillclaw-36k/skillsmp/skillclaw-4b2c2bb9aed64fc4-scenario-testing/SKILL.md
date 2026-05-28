---
name: scenario-testing
description: Use this skill when validating features end-to-end without mocks, testing integrations, or when "scenario test", "e2e test", or "no mocks" are mentioned.
---

# Scenario Testing

End-to-end validation using real dependencies, no mocks ever.

<when_to_use>

- End-to-end feature validation
- Integration testing across services
- Proof programs demonstrating behavior
- Real-world workflow testing
- API contract verification
- Authentication flow validation

NOT for: unit testing, mock testing, performance benchmarking, load testing

</when_to_use>

<iron_law>

NO MOCKS EVER.

Truth hierarchy:
1. **Scenarios** — real dependencies, actual behavior
2. **Unit tests** — isolated logic, synthetic inputs
3. **Mocks** — assumptions about how things work

Mocks test your assumptions, not reality. When mocks pass but production fails, the mock lied. When scenarios fail, reality spoke.

Test against real databases, real APIs, real services. Use test credentials, staging environments, local instances — but always real implementations.

</iron_law>

<directory_structure>

## .scratch/ (gitignored)

Throwaway test scripts for quick validation. Self-contained, runnable, disposable.

CRITICAL: Verify .scratch/ in .gitignore before first use.

## scenarios.jsonl (committed)

Successful scenario patterns documented as JSONL. One scenario per line, each a complete JSON object.

Purpose: capture proven patterns, regression indicators, reusable test cases.

Structure:

```jsonl
{"name":"auth-login-success","description":"User logs in with valid credentials","setup":"Create test user with known password","steps":["POST /auth/login with credentials","Receive JWT token","GET /auth/me with token"],"expected":"User profile returned with correct data","tags":["auth","jwt","happy-path"]}
{"name":"auth-login-invalid","description":"Login fails with wrong password","setup":"Test user exists","steps":["POST /auth/login with wrong password"],"expected":"401 Unauthorized, no token issued","tags":["auth","error-handling"]}
```

</directory_structure>

<scratch_directory>

## Purpose

Quick validation without ceremony. Write script, run against real deps, verify behavior, delete or document.

## Characteristics

- **Gitignored** — never committed, purely local
- **Disposable** — delete after validation or promote to permanent tests
- **Self-contained** — runnable with single command
- **Real dependencies** — actual DB, real APIs

</scratch_directory>