---
name: laravel-refactor
description: Use this skill when you need to refactor Laravel or Livewire applications to modern best practices, improve code quality, and set up automated testing and CI/CD pipelines.
---

# Skill body

## When to Use This Skill

Use this skill when the user:

- Requests to refactor Laravel or Livewire code
- Asks to set up modern Laravel tooling (Pint, PHPStan, Pest, Rector)
- Wants to implement CI/CD pipelines with quality gates
- Needs to configure static analysis and automated testing
- Asks to fix code smells or anti-patterns
- Wants to optimize database queries or performance
- Needs to modernize legacy Laravel code
- Requests to improve code architecture or structure
- Wants to fix security vulnerabilities
- Asks to upgrade to Livewire 3 patterns
- Needs help extracting business logic from controllers
- Requests to implement Laravel best practices
- Wants to set up pre-commit hooks or automated code review
- Asks about mutation testing or architecture tests

## Modern Laravel Tooling Stack (2024-2025)

The Laravel ecosystem has matured around a standardized quality toolchain:

### Core Quality Tools

**Laravel Pint** - Official code formatter (ships with Laravel)
- Zero-configuration formatting for Laravel projects
- Automatically fixes PSR-12 violations and Laravel conventions
- Run: `./vendor/bin/pint` to format, `./vendor/bin/pint --test` for CI validation

**PHPStan + Larastan** - Static analysis standard
- Larastan 2.0+ understands Laravel magic (facades, Eloquent, scopes)
- Most production apps target level 5-6 (catches real bugs without excessive strictness)
- Use baseline feature for legacy code: `./vendor/bin/phpstan analyse --generate-baseline`
- Progressive adoption: start at level 3, increase by 1 level per month

**Pest** - Modern testing framework with mutation testing
- Built-in architecture tests via `arch()` helper
- Mutation testing capabilities