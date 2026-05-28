---
name: php-best-practices
description: PHP coding standards and best practices. This skill should be used when writing, reviewing, or refactoring PHP code. Triggers on tasks involving PHP applications, WordPress plugins, Laravel projects, or any PHP-based backend.
trigger_patterns:
  - php
  - composer
  - psr-4
  - namespace
  - wordpress plugin
  - laravel
auto_load_with:
  - wordpress-best-practices
  - laravel-best-practices
  - mysql-best-practices
---

# PHP Best Practices

Comprehensive coding standards for PHP development, optimized for AI agents and LLMs. Contains 24 rules across 8 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Writing PHP application code
- Developing WordPress plugins or themes
- Building Laravel applications
- Implementing security measures
- Optimizing PHP performance
- Following PSR standards

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Security | CRITICAL | `security-` |
| 2 | Error Handling | HIGH | `error-` |
| 3 | Performance | HIGH | `perf-` |
| 4 | Type Safety | MEDIUM-HIGH | `types-` |
| 5 | OOP Patterns | MEDIUM | `oop-` |
| 6 | PSR Standards | MEDIUM | `psr-` |
| 7 | Testing | MEDIUM | `test-` |
| 8 | Modern PHP | LOW-MEDIUM | `modern-` |

## Quick Reference

### 1. Security (CRITICAL)
- `security-input-validation` - Validate with filter_var()
- `security-output-escaping` - Escape based on context
- `security-password-hashing` - Use password_hash()
- `security-csrf-tokens` - Implement CSRF protection
- `security-no-eval` - Never use eval()

### 2. Error Handling (HIGH)
- `error-exception-handling` - Use try-catch properly
- `error-custom-exceptions` - Create domain exceptions
- `error-error-reporting` - Configure error levels
- `error-logging` - Use PSR-3 logging

### 3. Performance (HIGH)
- `perf-opcache-enabled` - Enable OPcache
- `perf-autoloading` - Use Composer autoloader
- `perf-string-interpolation` - Prefer interpolation
- `perf-generators-memory` - Use generators for large data

### 4. Type Safety (MEDIUM-HIGH)
- `types-strict-types` - Declare strict_types=1
- `types-return-types` - Always declare return types
- `types-nullable-types` - Use ?Type for nullable
- `types-union-types` - Use union types

### 5. OOP Patterns (MEDIUM)
- `oop-final-classes` - Prefer final classes
- `oop-interface-segregation` - Small interfaces
- `oop-dependency-injection` - Inject dependencies

### 6. PSR Standards (MEDIUM)
- `psr-coding-style` - Follow PSR-12
- `psr-autoloading` - Use PSR-4
- `psr-http-messages` - Use PSR-7

### 7. Modern PHP (LOW-MEDIUM)
- `modern-constructor-promotion` - Use property promotion

## How to Use

Read individual rule files for detailed explanations and code examples.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
