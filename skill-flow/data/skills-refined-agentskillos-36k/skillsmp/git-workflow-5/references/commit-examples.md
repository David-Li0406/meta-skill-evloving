# Commit Message Examples

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Real Examples from Eco² Project

### Feature Commits

```bash
# Simple feature
feat(chat): add full CRUD API for chats and messages

# Feature with details
feat(chat_worker): implement ADR P2 production features

- Add MAX_TRANSITION_BOOST (0.15) and MIN_CONFIDENCE_FOR_BOOST (0.7)
  constants for Chain-of-Intent boost control
- Refactor IntentClassifierService to use IntentSignals for
  transparent confidence calculation
- Add OpenTelemetry telemetry module with tracer setup

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

# Integration feature
feat(chat_worker): integrate KECO collection point API (폐전자제품 수거함)

# Subagent feature
feat(chat_worker): add image generation subagent with Responses API
```

### Fix Commits

```bash
# Simple fix
fix(chat_worker): add intent_history type declaration to ChatState

# Bug fix with details
fix(chat_worker): resolve race conditions and fallback execution bugs

- Circuit Breaker: Fix asyncio.Lock → threading.Lock for DCL pattern
- NodeExecutor: Actually execute fallback function in FAIL_FALLBACK mode
- Contracts: Add is_required derivation from INTENT_REQUIRED_FIELDS

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

# Timeout fix
fix(chat_worker): add timeout to gRPC clients and image generator
```

### Refactor Commits

```bash
# Architecture refactor
refactor(chat_worker): implement Single Source of Truth for node contracts

# Code review fixes
refactor(chat_worker): apply code review fixes for KECO collection point client

# Pattern migration
refactor(auth): migrate to Port/Adapter pattern
```

### Documentation Commits

```bash
# Simple docs
docs: add code review fixes report

# Architecture docs
docs: add Chat Worker Production Architecture implementation report

# API docs
docs(chat): update OpenAPI specification
```

### Test Commits

```bash
# Unit tests
test(chat_worker): add KECO collection point client unit tests

# Integration tests
test(auth): add OAuth2 integration tests

# Test coverage
test(chat_worker): increase intent classifier coverage to 85%
```

### Chore Commits

```bash
# Dependencies
chore: update dependencies

# CI/CD
chore(ci): add SonarCloud integration

# Cleanup
chore: remove unused imports
```

## Body Guidelines

### When to Include Body

- Complex changes affecting multiple files
- Breaking changes
- Implementation decisions worth documenting
- References to issues or ADRs

### Body Format

```bash
feat(chat_worker): add production resilience infrastructure (P1)

Implementation of ADR P2 requirements:
- Soft dependency timeout handling
- Chain-of-Intent boost limits
- IntentSignals confidence calculation
- OpenTelemetry span attributes

Breaking Changes:
- IntentClassificationResult now includes signals field

Refs: docs/plans/chat-worker-production-architecture-adr.md

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Footer Conventions

### Co-authorship

```bash
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Issue References

```bash
Closes #123
Fixes #456
Refs #789
```

### Breaking Changes

```bash
BREAKING CHANGE: API endpoint renamed from /v1/chat to /v2/conversations
```

## Anti-patterns

```bash
# Bad: No type
added new feature

# Bad: No scope for service changes
feat: add CRUD API

# Bad: Too vague
fix: bug fix

# Bad: Past tense
feat(chat): added new endpoint

# Bad: Capitalized
Feat(chat): Add new endpoint

# Bad: Period at end
feat(chat): add new endpoint.

# Good
feat(chat): add message persistence endpoint
```

## Quick Reference

| Type | When to Use |
|------|-------------|
| `feat` | New functionality for users |
| `fix` | Bug fix |
| `refactor` | Code restructure without behavior change |
| `docs` | Documentation only |
| `test` | Adding/updating tests |
| `chore` | Maintenance (deps, configs) |
| `style` | Formatting, no code change |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
