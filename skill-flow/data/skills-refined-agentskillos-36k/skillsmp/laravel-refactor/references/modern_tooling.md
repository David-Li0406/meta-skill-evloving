# Modern Laravel Tooling Stack: 2024-2025 Complete Guide

This reference provides comprehensive coverage of modern Laravel development tooling, quality automation, and CI/CD practices based on patterns proven at scale by Spatie (500+ packages, 1.9B downloads), Tighten, Beyond Code, and the Laravel core team.

## Table of Contents

1. [Core Tooling Overview](#core-tooling-overview)
2. [Laravel Pint - Code Formatting](#laravel-pint---code-formatting)
3. [PHPStan + Larastan - Static Analysis](#phpstan--larastan---static-analysis)
4. [Progressive Static Analysis Adoption](#progressive-static-analysis-adoption)
5. [Pest - Modern Testing Framework](#pest---modern-testing-framework)
6. [Architecture Testing](#architecture-testing)
7. [Mutation Testing](#mutation-testing)
8. [Rector - Automated Refactoring](#rector---automated-refactoring)
9. [IDE Integration](#ide-integration)
10. [CI/CD Pipeline Patterns](#cicd-pipeline-patterns)
11. [Quality Gates](#quality-gates)
12. [Pre-commit Hooks](#pre-commit-hooks)
13. [Laravel Shift - Automated Upgrades](#laravel-shift---automated-upgrades)
14. [Production-Proven Patterns](#production-proven-patterns)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Core Tooling Overview

**Laravel's top developers in 2024-2025 have converged on a powerful toolset**: Laravel Pint for code style, PHPStan/Larastan at level 5-6 for static analysis, Pest for testing with built-in mutation testing, and Laravel 11's native architecture tests for structural enforcement.

### The Modern Stack

```
Code Formatting:    Laravel Pint (official, zero-config)
Static Analysis:    PHPStan + Larastan (level 5-6 for apps, 8-9 for packages)
Testing:            Pest (mutation testing + architecture tests)
Refactoring:        Rector (automated AST transformations)
CI/CD:              GitHub Actions / GitLab CI (quality gates)
Pre-commit:         GrumPHP (PHP teams) or Husky (full-stack teams)
Upgrades:           Laravel Shift (automated framework migrations)
```

### Philosophy

Taylor Otwell's core principle: **"The Laravel apps that age best are the ones that don't get too clever, because the clever dev always moves on."**

Modern practices prioritize:

- Simplicity over cleverness
- Framework conventions over custom architecture
- Automated quality enforcement over manual review
- Standardized tooling over custom solutions

---

## Laravel Pint - Code Formatting

**Laravel Pint emerged as the official code formatter in 2022 and now ships with Laravel by default.**

### Key Features

- Zero-configuration formatting based on Laravel's opinionated preset
- Combines best of PHP CS Fixer with Laravel-native experience
- Executes in seconds across entire codebases
- Automatically fixes PSR-12 violations + Laravel-specific conventions

### Basic Usage

```bash
# Format entire codebase
./vendor/bin/pint

# Check without modifying (for CI)
./vendor/bin/pint --test

# Format specific directories
./vendor/bin/pint app/Http/Controllers

# Show which files would be changed
./vendor/bin/pint --test -v
```

### Configuration

Create `pint.json` in project root:

```json
{
  "preset": "laravel",
  "rules": {
    "simplified_null_return": true,
    "ordered_imports": {
      "sort_algorithm": "alpha"
    },
    "no_unused_imports": true,
    "concat_space": {
      "spacing": "one"
    }
  },
  "exclude": ["vendor", "storage", "bootstrap/cache"]
}
```

### CI Integration

**.github/workflows/pint.yml**:

```yaml
name: Code Style

on: [push, pull_request]

jobs:
  pint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
      - run: composer install --no-progress
      - run: ./vendor/bin/pint --test
```

### Pint vs PHP CS Fixer

**Use Pint when:**

- Working on Laravel projects exclusively
- Want zero-configuration defaults
- Prefer faster execution (static compilation)
- Need official Laravel support

**Use PHP CS Fixer when:**

- Managing multi-framework codebases
- Require granular rule control
- Need broader rule catalog
- Have complex custom requirements

**Verdict**: Pint optimizes for Laravel developer experience; PHP CS Fixer optimizes for flexibility.

---

## PHPStan + Larastan - Static Analysis

**PHPStan paired with Larastan (Laravel-specific extension) has become the undisputed static analysis standard.**

### Why Larastan

Larastan 2.0+ understands Laravel's magic:

- Facades resolve correctly (`Cache::get()` knows return type)
- Eloquent dynamic properties validate (`$user->posts` understood)
- Framework patterns recognized (`scopeActive()` methods don't trigger false positives)

### Installation

```bash
composer require --dev nunomaduro/larastan

# Create phpstan.neon configuration
cat > phpstan.neon << 'EOF'
includes:
    - vendor/nunomaduro/larastan/extension.neon

parameters:
    paths:
        - app
    level: 5
    ignoreErrors:
        - '#Unsafe usage of new static#'
    checkMissingIterableValueType: false
    checkOctaneCompatibility: true
    checkModelProperties: true
EOF
```

### Running Analysis

```bash
# Analyze with progress
./vendor/bin/phpstan analyse

# Analyze specific paths
./vendor/bin/phpstan analyse app/Http/Controllers

# Generate baseline for legacy code
./vendor/bin/phpstan analyse --generate-baseline

# Clear cache (if behavior unexpected)
./vendor/bin/phpstan clear-result-cache
```

### Level System (0-9)

- **Level 0**: Unknown classes, undefined functions, invalid $this method calls
- **Level 1**: Unknown properties, undefined variables
- **Level 2**: Unknown methods on all expressions, PHPDoc accuracy
- **Level 3**: Return types, property assignments
- **Level 4**: Dead code, always-true/false conditions
- **Level 5**: Argument types passed to methods ✅ **PRODUCTION SWEET SPOT**
- **Level 6**: Explicit type hints everywhere
- **Level 7-8**: Stricter nullability, mixed type handling
- **Level 9**: Exhaustive type coverage (packages, critical systems)

### Configuration Deep Dive

**For Laravel 11+ applications**:

```neon
includes:
    - vendor/nunomaduro/larastan/extension.neon

parameters:
    paths:
        - app
        - config
        - database
        - routes

    level: 5

    # Octane compatibility (if using Octane)
    checkOctaneCompatibility: true

    # Validate Eloquent model properties
    checkModelProperties: true

    # Exclude problematic paths
    excludePaths:
        - app/Console/Kernel.php
        - bootstrap/cache/*

    # Common Laravel ignores
    ignoreErrors:
        - '#Unsafe usage of new static#'
        - '#Call to an undefined method Illuminate\\Database\\Eloquent\\Builder#'

    # Performance optimization
    parallel:
        maximumNumberOfProcesses: 4
        processTimeout: 300.0
```

**For packages (stricter)**:

```neon
parameters:
    level: 8
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
    reportUnmatchedIgnoredErrors: false
```

---

## Progressive Static Analysis Adoption

**The baseline feature revolutionizes legacy code migration.**

### Baseline Strategy

The baseline allows teams to enforce higher standards on new code immediately while gradually fixing legacy issues.

```bash
# Generate baseline (captures all current errors)
./vendor/bin/phpstan analyse --generate-baseline

# Creates phpstan-baseline.neon with all existing errors
# Now all new code must pass current level
```

**phpstan.neon with baseline**:

```neon
includes:
    - vendor/nunomaduro/larastan/extension.neon
    - phpstan-baseline.neon

parameters:
    paths:
        - app
    level: 5
```

### Progressive Adoption Timeline

**Week 1**: Install Larastan, generate baseline

```bash
composer require --dev nunomaduro/larastan
./vendor/bin/phpstan analyse --generate-baseline
```

**Week 2**: Configure level 3, address obvious issues

```bash
# Set level: 3 in phpstan.neon
./vendor/bin/phpstan analyse
# Fix easy wins, regenerate baseline
./vendor/bin/phpstan analyse --generate-baseline
```

**Month 2**: Increase to level 4, fix baseline errors incrementally

- Allocate 1-2 hours per week to baseline reduction
- Track progress: `wc -l phpstan-baseline.neon`
- Celebrate when baseline shrinks

**Month 3**: Reach level 5 (production-ready analysis)

- Level 5 = minimum for professional Laravel applications
- Catches legitimate bugs without excessive strictness

**Month 6+**: Consider level 6-8 for critical components

- Level 6-8 for admin panels, payment processing, authentication
- Level 9 for packages and public APIs

### Real-World Example

**Spatie's approach** across 500+ packages:

- New packages start at level 8
- Legacy packages at level 5-6 with aggressive baseline reduction
- Critical packages (like laravel-permission) at level 9
- Monthly "baseline reduction" sprints

---

## Pest - Modern Testing Framework

**Pest provides elegant testing syntax with built-in support for mutation testing and architecture tests.**

### Installation

```bash
composer require --dev pestphp/pest pestphp/pest-plugin-laravel

# Initialize Pest
./vendor/bin/pest --init
```

### Basic Test Structure

**tests/Feature/UserControllerTest.php**:

```php
<?php

use App\Models\User;

test('users can view their profile', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
        ->get('/profile')
        ->assertOk()
        ->assertSee($user->name);
});

it('requires authentication to view profile', function () {
    $this->get('/profile')
        ->assertRedirect('/login');
});
```

### Pest vs PHPUnit

**Pest advantages**:

- More readable syntax (test/it functions)
- Built-in architecture testing
- Native mutation testing support
- Higher-order testing methods
- Less boilerplate

**PHPUnit advantages**:

- More established ecosystem
- Some package test suites require it
- Team familiarity

**Migration strategy**: Keep existing PHPUnit tests, write new tests in Pest. Both coexist in same project.

### Running Tests

```bash
# Run all tests
./vendor/bin/pest

# Run specific test file
./vendor/bin/pest tests/Feature/UserControllerTest.php

# Run tests with coverage
./vendor/bin/pest --coverage

# Run tests in parallel
./vendor/bin/pest --parallel

# Filter by name
./vendor/bin/pest --filter=profile
```

---

## Architecture Testing

**Laravel 11's built-in architecture testing via Pest transformed structural validation.**

### Core Architecture Test Patterns

**tests/Architecture/ArchitectureTest.php**:

```php
<?php

arch('no debugging statements in production code')
    ->expect(['dd', 'dump', 'ray'])
    ->not->toBeUsed()
    ->ignoring('tests');

arch('all models extend base model')
    ->expect('App\Models')
    ->toExtend('Illuminate\Database\Eloquent\Model');

arch('controllers follow naming conventions')
    ->expect('App\Http\Controllers')
    ->toHaveSuffix('Controller');

arch('services only depend on repositories')
    ->expect('App\Services')
    ->toOnlyUse([
        'App\Repositories',
        'Illuminate\Support',
        'Illuminate\Database',
    ]);

arch('strict types declared in all app files')
    ->expect('App')
    ->toUseStrictTypes();

arch('no facades in domain layer')
    ->expect('App\Domain')
    ->not->toUse('Illuminate\Support\Facades');

arch('value objects are readonly')
    ->expect('App\Domain\ValueObjects')
    ->classes()
    ->toBeReadonly();

arch('actions are invokable')
    ->expect('App\Actions')
    ->toHaveMethod('__invoke');

arch('final classes cannot be extended')
    ->expect('App\Domain\ValueObjects')
    ->classes()
    ->toBeFinal();
```

### Security-Focused Architecture Tests

```php
arch('no request all() method usage')
    ->expect('App\Http\Controllers')
    ->not->toUse('Illuminate\Http\Request::all');

arch('controllers use form requests')
    ->expect('App\Http\Controllers')
    ->classes()
    ->toHaveMethod('store')
    ->toHaveMethodWithParameter('request', 'App\Http\Requests');
```

### Benefits

- Prevents architectural drift automatically
- Enforces team standards without manual review
- Catches violations in CI before merge
- Self-documenting codebase structure

---

## Mutation Testing

**Mutation testing validates test quality by introducing bugs and checking if tests catch them.**

### Installation

```bash
composer require --dev pestphp/pest-plugin-mutate
```

### Running Mutation Tests

```bash
# Run mutation testing
./vendor/bin/pest --mutate

# Mutation testing on specific files
./vendor/bin/pest --mutate --parallel --path=app/Services
```

### Interpreting Results

```
Mutations: 45
Killed: 40 (88.9%)
Not Covered: 3 (6.7%)
Escaped: 2 (4.4%)
```

- **Killed**: Test caught the mutation ✅
- **Not Covered**: No test covers this code ⚠️
- **Escaped**: Test ran but didn't catch mutation ❌

**Target**: 80%+ mutation score for critical code paths

### Example Mutation Scenario

**Original code**:

```php
public function calculateDiscount(int $total): int
{
    if ($total > 100) {
        return $total * 0.1;
    }
    return 0;
}
```

**Mutation 1**: Change `>` to `>=`
**Mutation 2**: Change `0.1` to `0.2`
**Mutation 3**: Change `return 0` to `return 1`

If tests pass with these mutations, test coverage is insufficient.

---

## Rector - Automated Refactoring

**Rector automates complex refactoring tasks impossible with simple formatting tools.**

### Installation

```bash
composer require --dev rector/rector
```

### Configuration

**rector.php**:

```php
<?php

use Rector\Config\RectorConfig;
use Rector\Laravel\Set\LaravelSetList;
use Rector\Set\ValueObject\SetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/app',
        __DIR__ . '/config',
        __DIR__ . '/database',
        __DIR__ . '/routes',
        __DIR__ . '/tests',
    ])
    ->withSkip([
        __DIR__ . '/bootstrap/cache',
        __DIR__ . '/storage',
    ])
    ->withPhpSets(php83: true)
    ->withSets([
        LaravelSetList::LARAVEL_110,
        SetList::CODE_QUALITY,
        SetList::DEAD_CODE,
        SetList::TYPE_DECLARATION,
    ]);
```

### Common Use Cases

**1. Framework Upgrades**

```bash
# Migrate deprecated Laravel APIs
./vendor/bin/rector process --set laravel-110
```

**2. PHP Version Migrations**

```bash
# Adopt PHP 8.3 features
./vendor/bin/rector process --set php83
```

**3. Architecture Refactoring**

```bash
# Convert to constructor property promotion
./vendor/bin/rector process --rule \Rector\Php80\Rector\Class_\ClassPropertyAssignToConstructorPromotionRector
```

### Real-World Example: Spatie's Use

Spatie uses Rector rules to maintain consistency across 500+ repositories:

- Automated conversion to short array syntax
- Constructor property promotion across all packages
- Migration from older Laravel patterns to modern equivalents
- Consistent code style transformations

---

## IDE Integration

### PHPStorm with Laravel Idea

**Laravel Idea plugin** provides comprehensive Laravel support:

- Autocomplete for routes: `route('user.show')`
- View autocomplete: `view('users.index')`
- Config autocomplete: `config('app.name')`
- Translation keys: `__('auth.failed')`
- Eloquent relationship navigation
- Route parameter validation
- Blade syntax validation

**Installation**: Settings → Plugins → "Laravel Idea" → Install

### VS Code with Laravel Extension

**Official Laravel extension** (announced Laracon US 2024) reached feature parity:

- Autocomplete for Eloquent, routes, services
- Inline diagnostics and error detection
- Language server protocol integration
- Real-time feedback while typing

**Installation**: Extensions → Search "Laravel" → Install official extension

### Additional IDE Tools

**PHP Inspections (EA Extended)**: Additional inspections beyond base PHPStorm
**PHP Toolbox**: Enhanced autocomplete for Laravel magic methods
**Laravel Snippet**: Common Laravel code snippets

---

## CI/CD Pipeline Patterns

### GitHub Actions - Complete Example

**.github/workflows/tests.yml**:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        php: [8.2, 8.3]
        laravel: [10.*, 11.*]
        dependency-version: [prefer-lowest, prefer-stable]

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: laravel
          MYSQL_ROOT_PASSWORD: password
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: --health-cmd="redis-cli ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, sqlite, pdo_sqlite, bcmath, soap, intl, gd, exif, iconv
          coverage: xdebug

      - name: Get composer cache directory
        id: composer-cache
        run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: ${{ runner.os }}-composer-

      - name: Install dependencies
        run: composer update --${{ matrix.dependency-version }} --prefer-dist --no-interaction

      - name: Copy environment file
        run: cp .env.example .env

      - name: Generate application key
        run: php artisan key:generate

      - name: Run migrations
        run: php artisan migrate --force
        env:
          DB_CONNECTION: mysql
          DB_HOST: 127.0.0.1
          DB_PORT: 3306
          DB_DATABASE: laravel
          DB_USERNAME: root
          DB_PASSWORD: password

      - name: Execute tests with coverage
        run: ./vendor/bin/pest --coverage --min=70
```

**.github/workflows/quality.yml**:

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  pint:
    name: Code Style
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
      - run: composer install --no-progress
      - run: ./vendor/bin/pint --test

  phpstan:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
      - run: composer install --no-progress
      - run: ./vendor/bin/phpstan analyse --memory-limit=2G

  security:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
      - run: composer install --no-progress
      - run: composer audit
```

### GitLab CI - Elite Pattern

**.gitlab-ci.yml** (inspired by Oh Dear):

```yaml
stages:
  - prepare
  - build
  - test
  - security
  - deploy

variables:
  MYSQL_DATABASE: laravel
  MYSQL_ROOT_PASSWORD: password
  DB_HOST: mysql
  DB_USERNAME: root

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - vendor/
    - node_modules/

composer:
  stage: prepare
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  script:
    - composer install --prefer-dist --no-ansi --no-interaction --no-progress
  artifacts:
    paths:
      - vendor/
    expire_in: 1 day

yarn:
  stage: prepare
  image: node:20
  script:
    - yarn install
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 day

build:
  stage: build
  image: node:20
  dependencies:
    - yarn
  script:
    - yarn build
  artifacts:
    paths:
      - public/build/
    expire_in: 1 day

pint:
  stage: test
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  dependencies:
    - composer
  script:
    - ./vendor/bin/pint --test

phpstan:
  stage: test
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  dependencies:
    - composer
  script:
    - ./vendor/bin/phpstan analyse --memory-limit=2G

pest:
  stage: test
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  services:
    - mysql:8.0
    - redis:7-alpine
  dependencies:
    - composer
  script:
    - cp .env.example .env
    - php artisan key:generate
    - php artisan migrate --force
    - ./vendor/bin/pest --coverage --min=70
  coverage: '/^\s*Lines:\s*\d+.\d+\%/'

composer-audit:
  stage: security
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  dependencies:
    - composer
  script:
    - composer audit

deploy:
  stage: deploy
  image: edbizarro/gitlab-ci-pipeline-php:8.3
  only:
    - main
  when: manual
  script:
    - "which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )"
    - eval $(ssh-agent -s)
    - ssh-add <(echo "$SSH_PRIVATE_KEY")
    - mkdir -p ~/.ssh
    - '[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config'
    - vendor/bin/dep deploy production
```

### Pipeline Optimization Strategies

**1. Parallelization**

```yaml
# GitHub Actions
jobs:
  tests:
    strategy:
      matrix:
        php: [8.2, 8.3]
        test-suite: [Unit, Feature, Browser]
```

**2. Caching**

```yaml
# Cache Composer dependencies
- uses: actions/cache@v3
  with:
    path: vendor
    key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
```

**3. Conditional Execution**

```yaml
# Only run on specific branches
on:
  push:
    branches: [main, develop]
    paths:
      - "**.php"
      - "composer.json"
```

---

## Quality Gates

**Quality gates block pull request merging until all pass**, preventing quality decay.

### Common Quality Gate Configuration

```yaml
# GitHub branch protection rules
# Settings → Branches → Branch protection rules

Required status checks:
✓ Code Style (Pint)
✓ Static Analysis (PHPStan level 5+)
✓ Tests (Pest with 70%+ coverage)
✓ Security Audit (composer audit)

Optional checks:
□ Mutation Testing (80%+ score)
□ Architecture Tests
□ PHPMD (complexity checks)
```

### Quality Metrics Thresholds

**Professional Laravel application standards**:

- Code style: 100% compliance (Pint)
- Static analysis: PHPStan level 5-6 with 0 errors
- Test coverage: 70-80% minimum
- Mutation score: 80%+ for critical paths
- Security audit: 0 vulnerabilities in dependencies
- Complexity: PHPMD max complexity 10-15

### Enforcement Strategies

**1. Fail Fast**

```yaml
# Run syntax check first (fastest failure)
- name: Check syntax
  run: parallel-lint app tests

# Then style (fast)
- name: Code style
  run: ./vendor/bin/pint --test

# Then analysis (medium)
- name: Static analysis
  run: ./vendor/bin/phpstan analyse

# Finally tests (slowest)
- name: Tests
  run: ./vendor/bin/pest
```

**2. Parallel Execution**

```yaml
jobs:
  quality:
    strategy:
      matrix:
        check: [pint, phpstan, pest, security]
    steps:
      - name: Run ${{ matrix.check }}
        run: make ${{ matrix.check }}
```

**3. Progressive Enhancement**

```
Week 1: Add Pint (easy win, fast)
Week 2: Add PHPStan level 3 with baseline
Week 4: Increase to level 5
Week 6: Add test coverage requirement
Week 8: Add security audit
Month 3: Add mutation testing
```

---

## Pre-commit Hooks

**Pre-commit hooks provide immediate feedback before code reaches version control.**

### GrumPHP - PHP-Native Solution

**Advantages**:

- Native PHP integration
- Automatic Git hook installation
- 50+ built-in tasks
- Laravel-specific presets
- Zero Node.js dependency

**Installation**:

```bash
composer require --dev phpro/grumphp
```

**grumphp.yml**:

```yaml
grumphp:
  tasks:
    # Static analysis
    phpstan:
      level: 5
      configuration: phpstan.neon
      memory_limit: "-1"

    # Code style
    phpcsfixer:
      config: .php-cs-fixer.php
      allow_risky: true

    # Tests
    phpunit:
      config: phpunit.xml
      always_execute: false # Only on staged test files

    # Complexity
    phpmd:
      ruleset: ["cleancode", "codesize", "naming"]
      exclude:
        - vendor
        - storage

    # Security
    composer_audit:
      composer_file: composer.json
      locked: true

    # JSON/YAML validation
    jsonlint:
      detect_key_conflicts: true

    yamllint: ~

  testsuites:
    quick:
      tasks: [phpcsfixer, phpstan]
    full:
      tasks: [phpstan, phpcsfixer, phpunit, phpmd, composer_audit]
```

**Usage**:

```bash
# Hooks run automatically on git commit
git commit -m "Add feature"

# Skip hooks if needed (emergency)
git commit -m "Hotfix" --no-verify

# Run manually
./vendor/bin/grumphp run

# Run specific testsuite
./vendor/bin/grumphp run --testsuite=quick
```

### Husky with lint-staged - Node.js Solution

**Advantages**:

- Optimized for full-stack teams
- Processes only staged files (faster)
- Integrates with frontend tooling
- Automatic Git hook installation

**Installation**:

```bash
npm install --save-dev husky lint-staged
npx husky install
```

**package.json**:

```json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.php": [
      "./vendor/bin/pint",
      "./vendor/bin/phpstan analyse --memory-limit=2G"
    ],
    "*.{js,vue}": ["eslint --fix", "prettier --write"],
    "*.{css,scss}": ["stylelint --fix", "prettier --write"]
  }
}
```

**.husky/pre-commit**:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

### Comparison: GrumPHP vs Husky

**Use GrumPHP when**:

- Pure PHP team
- PHP-centric workflow
- Want comprehensive built-in tasks
- Prefer native PHP solution

**Use Husky when**:

- Full-stack team (PHP + JavaScript)
- Significant frontend work
- Need integration with ESLint/Prettier
- Team familiar with Node.js tooling

---

## Laravel Shift - Automated Upgrades

**Laravel Shift automates upgrade and modernization** as the premier tool for framework migrations.

### What Shift Does

**Single-use Shifts** ($9-29 per version jump):

- Handles Laravel 4.2 → latest incrementally
- Creates detailed PRs with atomic commits
- Completes in under 40 minutes
- Provides explanatory comments throughout

**Process**:

1. Connect via GitHub/GitLab/Bitbucket
2. Select source and target Laravel version
3. Shift creates new branch with changes
4. Opens PR with detailed migration notes
5. Review and merge (human verification required)

### Beyond Upgrades

**Laravel Fixer**: One-time code style modernization
**Laravel Linter**: Continuous code review
**Workbench Shifts**: Specialized refactors (Livewire 2→3, PHP 8.x adoption)
**Shifty Plans**: Subscription-based continuous linting

### Shifty Plan Features

```
Monthly subscription: $29-99 based on team size

Features:
- Automated code review on every PR
- Laravel Fixer execution on commits
- Custom task sets for team standards
- API access for advanced automation
- Priority support
```

### API Integration

```php
// Trigger Shift programmatically
$response = Http::withToken($token)
    ->post('https://laravelshift.com/api/shifts', [
        'repository' => 'username/repo',
        'from_version' => '10',
        'to_version' => '11',
    ]);

// Batch process across repositories
$repositories = Repository::where('framework', 'laravel')->get();

foreach ($repositories as $repo) {
    ShiftJob::dispatch($repo);
}
```

### Notable Endorsements

**Jeffrey Way (Laracasts)**: "Worth much more than the cost"
**Matt Stauffer (Tighten)**: "Essential tooling for any Laravel team"
**Freek Van der Herten (Spatie)**: "Saves us hours on every upgrade"

---

## Production-Proven Patterns

### Spatie's Quality Standards (500+ Packages, 1.9B Downloads)

**GitHub Actions Workflows**:

```
.github/workflows/
├── run-tests.yml         (Pest with PHP 8.2, 8.3, 8.4)
├── phpstan.yml           (Level 5-8, varies by package criticality)
├── pint.yml              (Laravel Pint enforcement)
└── dependabot-auto-merge.yml (Automated dependency updates)
```

**PHPStan Configuration**:

- Level 5-8 typical across packages
- Critical packages (laravel-permission, laravel-backup) reach level 9
- Matrix testing validates all supported PHP and Laravel versions

**Testing Strategy**:

- Pest framework exclusively for new packages
- Mutation testing on critical packages
- Architecture tests prevent regressions
- 80%+ coverage requirement

### Tighten's Comprehensive Approach

**TLint - Laravel-Specific Linting**:

```bash
./vendor/bin/tlint lint

# Checks:
- No request()->all() (mass assignment risk)
- Form Request validation required
- Route path conventions enforced
- Anonymous migrations mandated
- Mailable structure validated
```

**Duster - All-in-One Quality Tool**:

```bash
# Check everything
./vendor/bin/duster lint

# Fix violations automatically
./vendor/bin/duster fix

# Generate GitHub Actions workflow
./vendor/bin/duster github-actions
```

**Bundles**:

- Laravel Pint
- PHP_CodeSniffer
- PHP-CS-Fixer
- TLint

### Common Quality Gates Across Elite Teams

```yaml
# Quality gate checklist (must pass for merge)

✓ PHP syntax check (parallel-lint)
✓ Code style (Laravel Pint --test)
✓ Static analysis (Larastan level 5-6 minimum, 8-9 for packages)
✓ Tests (Pest with 70-80% coverage)
✓ Security audit (composer audit)

Optional but recommended:
□ PHPMD complexity check
□ Psalm additional analysis
□ Architecture tests
□ Mutation testing (80%+ score)
```

---

## Implementation Roadmap

**Progressive adoption strategy for maximum impact with minimum disruption.**

### Phase 1: Quick Wins (Week 1-2)

**Priority**: Automated formatting

```bash
# Install and configure Pint
composer require --dev laravel/pint
./vendor/bin/pint

# Commit formatted code
git add .
git commit -m "Apply Laravel Pint formatting"
```

**Impact**: Instant code consistency, eliminates style debates

### Phase 2: Static Analysis Foundation (Week 3-4)

**Priority**: PHPStan with baseline

```bash
# Install Larastan
composer require --dev nunomaduro/larastan

# Create configuration at level 5
cat > phpstan.neon << 'EOF'
includes:
    - vendor/nunomaduro/larastan/extension.neon
parameters:
    paths:
        - app
    level: 5
EOF

# Generate baseline for legacy code
./vendor/bin/phpstan analyse --generate-baseline

# Commit configuration
git add phpstan.neon phpstan-baseline.neon
git commit -m "Add PHPStan with baseline"
```

**Impact**: Catches type errors, provides IDE hints, prevents regressions

### Phase 3: Automated Testing (Month 2)

**Priority**: Pest with architecture tests

```bash
# Install Pest
composer require --dev pestphp/pest pestphp/pest-plugin-laravel
./vendor/bin/pest --init

# Create architecture tests
mkdir -p tests/Architecture
```

**tests/Architecture/ArchitectureTest.php**:

```php
<?php

arch('no debugging in production')
    ->expect(['dd', 'dump', 'ray'])
    ->not->toBeUsed()
    ->ignoring('tests');

arch('strict types everywhere')
    ->expect('App')
    ->toUseStrictTypes();
```

**Impact**: Structural validation, prevents architectural drift

### Phase 4: CI/CD Integration (Month 2-3)

**Priority**: Quality gates in pipeline

```bash
# Create GitHub Actions workflows
mkdir -p .github/workflows
```

**.github/workflows/quality.yml**: (See CI/CD section above)

**Impact**: Automated enforcement, blocks bad code from merging

### Phase 5: Pre-commit Hooks (Month 3)

**Priority**: Local feedback loop

```bash
# Install GrumPHP (PHP teams)
composer require --dev phpro/grumphp

# Or Husky (full-stack teams)
npm install --save-dev husky lint-staged
```

**Impact**: Catches issues before CI, faster feedback

### Phase 6: Advanced Quality (Month 4+)

**Priority**: Mutation testing and enhanced analysis

```bash
# Add mutation testing
composer require --dev pestphp/pest-plugin-mutate

# Run on critical paths
./vendor/bin/pest --mutate --path=app/Services
```

**Impact**: Validates test quality, ensures coverage effectiveness

### Rollout Timeline Summary

```
Week 1:  Laravel Pint (1 hour setup)
Week 2:  PHPStan level 5 with baseline (2-4 hours)
Week 3:  Architecture tests (2 hours)
Week 4:  GitHub Actions CI/CD (4 hours)
Month 2: Pest adoption for new tests (ongoing)
Month 3: Pre-commit hooks (2 hours)
Month 3: Baseline reduction sprints (1-2 hours/week)
Month 4: Mutation testing evaluation (2 hours)
Month 6: Consider level 6-8 for critical areas
```

### Success Metrics

**Track progress monthly**:

```bash
# PHPStan baseline size (goal: decrease)
wc -l phpstan-baseline.neon

# Test coverage (goal: 70-80%)
./vendor/bin/pest --coverage

# Mutation score (goal: 80%+)
./vendor/bin/pest --mutate

# Code style violations (goal: 0)
./vendor/bin/pint --test
```

---

## Conclusion

**The 2024-2025 Laravel quality toolchain has reached maturity.**

Modern Laravel development combines:

- **Automated formatting** via Pint (eliminates style debates)
- **Static analysis** via Larastan (catches type errors pre-runtime)
- **Mutation testing** via Pest (validates test quality)
- **Architecture tests** (prevents structural regressions)
- **Pre-commit hooks** (instant feedback)
- **CI/CD pipelines** (enforces gates automatically)
- **Laravel Shift** (handles framework upgrades professionally)

**Manual code review now focuses on business logic and architecture** rather than catching formatting issues or missing types—automation handles mechanical quality enforcement comprehensively.

**The path forward**: automate quality enforcement, trust the tooling, and focus human creativity on solving actual business problems rather than reinventing quality standards solved years ago.

**Implementation priority by impact**:

1. Laravel Pint (instant consistency)
2. Larastan level 5 with baseline (legacy code friendly)
3. Architecture tests (structural validation)
4. CI/CD quality gates (automated enforcement)
5. Pre-commit hooks (local feedback)
6. Mutation testing (test quality validation)

The tools exist, patterns prove themselves at scale, and community consensus has emerged. Elite Laravel development no longer requires custom quality infrastructure—the ecosystem provides comprehensive solutions ready for immediate adoption.
