---
name: ensuring-laravel-quality
description: Run Laravel quality checks including Rector, Pint, PHPStan, code coverage, and type coverage. Use when ensuring code quality, before committing, running quality checks, or when user mentions quality, checks, Rector, Pint, PHPStan, coverage, or composer checks.
---

# Ensure Laravel Quality

Run comprehensive quality checks to ensure code meets project standards before committing. Execute `composer run checks` to run Rector, Pint, PHPStan level 8, tests with 90% coverage, and 100% type coverage in sequence.

## Quality Tools

This project uses a comprehensive quality toolchain:

1. **Rector** - Automated refactoring and code modernization
2. **Pint** - Laravel code style fixer (built on PHP-CS-Fixer)
3. **PHPStan/Larastan** - Static analysis for type safety
4. **Pest** - Testing framework with coverage
5. **Type Coverage** - Ensures 100% type coverage

## Running All Checks

```bash
composer run checks
```

This runs all quality checks in sequence:

1. Rector refactoring
2. Pint formatting
3. PHPStan analysis
4. Code coverage (90% minimum)
5. Type coverage (100% required)
6. All tests

## Individual Tools

### Rector - Automated Refactoring

**Run Rector:**

```bash
composer run rector
# or
./vendor/bin/rector process --ansi
```

**What it does:**

- Upgrades code to modern PHP syntax
- Applies Laravel best practices
- Refactors deprecated patterns
- Ensures consistency

**Configuration:** `rector.php`

**Example fixes:**

- Converts array syntax to typed properties
- Updates deprecated Laravel methods
- Modernizes PHP syntax
- Applies coding standards

### Pint - Code Formatting

**Run Pint:**

```bash
composer run pint
# or
./vendor/bin/pint
```

**What it does:**

- Formats PHP code to Laravel style
- Fixes indentation, spacing
- Ensures consistent code style
- Auto-fixes most style issues

**Configuration:** `pint.json`

**Example fixes:**

- Line length limits
- Indentation (4 spaces)
- Blank line rules
- Import ordering
- Brace placement

### PHPStan - Static Analysis

**Run PHPStan:**

```bash
composer run stan
# or
./vendor/bin/phpstan analyse --memory-limit=3G
```

**What it does:**

- Finds type errors before runtime
- Detects dead code
- Validates method calls
- Checks property access
- Ensures type safety

**Configuration:** `phpstan.neon`

**Level:** 9 (strictest)

**Common issues caught:**

- Undefined methods/properties
- Wrong parameter types
- Missing return types
- Nullable type issues
- Array access on non-arrays

### Code Coverage

**Run with coverage:**

```bash
composer run coverage
# or
./vendor/bin/pest --coverage --parallel --compact --min=90
```

**Requirements:**

- Minimum 90% code coverage
- All critical paths tested
- Feature and unit tests

**What it measures:**

- Line coverage
- Branch coverage
- Function coverage

### Type Coverage

**Run type coverage:**

```bash
composer run type-coverage
# or
./vendor/bin/pest --type-coverage --parallel --compact --min=100
```

**Requirements:**

- 100% type coverage required
- All parameters typed
- All return types declared
- All properties typed

## Quality Standards

### Required for All Code

1. **Type Safety:**
   - `declare(strict_types=1);` on every file
   - Full type hints on parameters
   - Full return type declarations
   - Typed properties

2. **Code Style:**
   - Passes Pint formatting
   - Laravel style guide
   - PSR-12 compliant

3. **Static Analysis:**
   - Passes PHPStan level 8
   - No ignored errors
   - Proper PHPDoc blocks

4. **Test Coverage:**
   - 90% minimum code coverage
   - 100% type coverage
   - All features tested

## Common Issues and Fixes

### Issue: PHPStan Errors

```
❌ Parameter #1 $user of method expects User, User|null given
```

**Fix:**

```php
// Before
public function handle($user): void
{
    $this->notify($user);
}

// After
public function handle(User $user): void
{
    $this->notify($user);
}
```

### Issue: Missing Return Types

```
❌ Method handle() has no return type specified
```

**Fix:**

```php
// Before
public function handle(RegisterData $data)
{
    return User::create([...]);
}

// After
public function handle(RegisterData $data): User
{
    return User::create([...]);
}
```

### Issue: Low Coverage

```
❌ Code coverage below 90%
```

**Fix:**

- Write feature tests for new controllers
- Write unit tests for Actions
- Test edge cases and error paths

## Integration with Workflow

### Pre-commit Checks

Run before committing:

```bash
composer run checks
```

### CI/CD Pipeline

All checks run automatically:

```yaml
- name: Run Quality Checks
  run: composer run checks
```

### IDE Integration

**PHPStorm/VS Code:**

- Configure Pint as formatter
- Enable PHPStan for real-time errors
- Run tests with coverage in IDE

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip type declarations
public function handle($data) // ❌

// Don't ignore PHPStan errors
/** @phpstan-ignore-next-line */ // ❌

// Don't commit without running checks
git commit -m "Quick fix" // ❌ Run checks first

// Don't disable strict types
// Missing declare(strict_types=1); ❌
```

### ✅ Do This Instead

```php
// Full type declarations
public function handle(RegisterData $data): User

// Fix PHPStan errors properly
public function handle(?User $user): void {
    if ($user === null) {
        throw new InvalidArgumentException();
    }
}

// Always run checks before commit
composer run checks
git commit -m "Add user registration"

// Always use strict types
<?php

declare(strict_types=1);
```

## Quality Checklist

Before committing code:

- [ ] Rector passes (no refactoring needed)
- [ ] Pint passes (code formatted)
- [ ] PHPStan passes level 9 (no type errors)
- [ ] Coverage ≥ 90% (features tested)
- [ ] Type coverage = 100% (all types declared)
- [ ] All tests pass (functionality works)
- [ ] No ignored errors or @phpstan-ignore comments

## Fixing Failed Checks

### Rector Failed

```bash
# View what Rector wants to change
./vendor/bin/rector process --dry-run

# Apply Rector changes
composer run rector
```

### Pint Failed

```bash
# Pint auto-fixes most issues
composer run pint
```

### PHPStan Failed

```bash
# See detailed errors
composer run stan

# Fix errors manually (no auto-fix)
# Add types, fix method calls, etc.
```

### Coverage Failed

```bash
# See coverage report
composer run coverage

# Write missing tests
```

### Type Coverage Failed

```bash
# See missing types
composer run type-coverage

# Add missing type declarations
```

## Quality Commands Reference

```bash
# Run all checks
composer run checks

# Individual tools
composer run rector      # Refactoring
composer run pint       # Formatting
composer run stan       # Static analysis
composer run coverage   # Code coverage
composer run type-coverage  # Type coverage
composer run test       # Just tests

# With options
./vendor/bin/pint --test  # Check without fixing
./vendor/bin/phpstan --memory-limit=4G  # More memory
./vendor/bin/pest --filter=UserTest  # Specific test
```

## Maintaining High Quality

1. Run checks frequently during development
2. Fix issues immediately (don't accumulate debt)
3. Write tests alongside features
4. Review PHPStan errors carefully
5. Keep type coverage at 100%
6. Run full checks before pushing
