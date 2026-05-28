---
name: PHP Modern Best Practices & Laravel Helper
description: Enforces PSR-12, PHP 8.4+ idioms, security, Laravel/Symfony patterns, and clean code in PHP projects. Activates on .php files.
version: 1.1
triggers:
  - php
  - laravel
  - symfony
  - composer.json
---

# PHP Modern Best Practices & Laravel Helper Skill

## Overview
You are an expert PHP developer specializing in modern, secure, maintainable code (PHP 8.3/8.4+). Always follow these rules strictly when reading, writing, reviewing, refactoring, or suggesting PHP code.

## When to Activate
- Any file with .php extension
- composer.json present (especially with laravel/framework or symfony/* dependencies)
- User mentions PHP, Laravel, Symfony, PSR, PHPUnit, Pest, etc.
- Code review, generation, or debugging tasks involving backend logic, APIs, controllers, models, services.

## Core Rules & Guidelines

### 1. Coding Style (Strict PSR-12 + Modern Enhancements)
- Use 4 spaces for indentation (never tabs).
- Line length: max 120 chars (soft), 80 preferred.
- Always use strict_types=1 at the top of every file.
- Use short array syntax [] instead of array().
- Use named arguments where clarity helps (PHP 8+).
- Use match expressions over switch when possible.
- Use readonly properties/classes (PHP 8.1+), final classes/methods where appropriate.
- Attributes over annotations where possible (e.g., #[Route] in Symfony).
- Declare properties with types (public/private/protected Type $prop;).

### 2. Laravel-Specific (if laravel/framework in composer.json)
- Follow Laravel conventions: controllers in app/Http/Controllers, models in app/Models.
- Use dependency injection via constructor/type-hinting.
- Prefer Eloquent relationships, query builder over raw SQL.
- Use form requests for validation.
- Return responses with response()->json() or view().
- Use Laravel's env() / config() helpers, never getenv().
- Migrations: use Schema::create/table, foreignId(), etc.
- Testing: prefer Pest syntax if pestphp/pest present, else PHPUnit.

### 3. General PHP Best Practices
- SOLID principles: single responsibility, open/closed, etc.
- Use value objects/DTOs for complex data instead of arrays.
- Avoid global state; use services/DI containers.
- Error handling: throw specific exceptions, never die()/exit().
- Security:
  - Always validate/sanitize inputs (never trust $_GET/$_POST).
  - Use prepared statements/PDO (no mysql_query).
  - Hash passwords with password_hash().
  - CSRF/XSS protection (use Laravel's middleware or Symfony's CsrfTokenManager).
  - Avoid eval(), system(), etc.
- Performance: prefer generators/iterators for large data; cache where possible.

### 4. Code Review & Refactor Checklist
When reviewing:
- Flag any missing declare(strict_types=1);
- Suggest type hints everywhere possible.
- Point out potential SQL injection, XSS, insecure deserialization.
- Recommend PSR-4 autoloading compliance.
- Suggest unit/feature tests if missing.
- Enforce conventional commits if git-related.

## Examples

**Bad → Good refactor example:**
```php
// Bad
function process($data) {
    $db = new PDO(...);
    $db->query("INSERT INTO users VALUES ($data)");
}

// Good
function process(UserData $data): void {
    // Use repository/service + prepared statement
}

Laravel controller snippet you should aim for:

<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Http\Requests\StoreUserRequest;
use App\Services\UserService;

final class UserController extends Controller
{
    public function __construct(private readonly UserService $service)
    {
    }

    public function store(StoreUserRequest $request)
    {
        $this->service->create($request->validated());
        return response()->json(['message' => 'User created'], 201);
    }
}

Success Criteria
•  Code must be type-safe, PSR-12 compliant, secure, and idiomatic.
•  Prefer declarative/functional style over imperative when cleaner.
•  Always explain changes with “why” (e.g., “Using strict types prevents silent type coercion bugs”).
When user provides code or asks for generation/review: Apply these rules automatically. Ask clarifying questions only if project type (plain PHP vs Laravel vs Symfony) is unclear.

3. **Optional enhancements**:
   - Add a `/resources/` subfolder with example files (e.g., a sample Laravel controller.php, Pest test template).
   - Or `/scripts/` for a small Python helper if you want auto-formatting checks (but most agents handle Markdown instructions fine without).

4. **Install & Test**:
   - In Claude Code: Restart or reload workspace → mention "use PHP Modern Best Practices" or just edit a .php file.
   - In Antigravity: Same—drop into `~/.agent/skills/`, agent should detect on PHP context.
   - Test prompt: "Review this PHP controller for best practices" or "Generate a Laravel API resource controller for users".
