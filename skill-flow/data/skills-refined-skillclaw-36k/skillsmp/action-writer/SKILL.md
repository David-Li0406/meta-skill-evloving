---
name: action-writer
description: Create or update an Action in app/Actions following JournalOS conventions (validation, logging, queues, tests).
---

# Action Writer

This Skill helps you add or update an Action in `app/Actions` using the project conventions.

## When to use this Skill

Use this Skill when:
- Creating a new Action
- Updating an existing Action

## Instructions

## Quick start

- Pick the action name (verb-first) and its input/output types.
- Create the Action class and implement `execute()`.
- Add or update unit tests in `tests/Unit/Actions`.
- Run the smallest relevant test(s), then `composer journalos:unit`.

### Step 1: Choose the action name and scope

1. Actions represent a single user intent (example: `LogHealth`, `CreateBook`, `ResetWorkData`).
1. Keep inputs minimal and explicit. Use descriptive parameter names.
1. Decide whether the Action returns a model, a scalar, or nothing (`void`).

### Step 2: Create the Action class

1. Use Artisan to create the class:

```bash
php artisan make:class Actions/ActionName --no-interaction
```

1. Use `declare(strict_types=1);` and the `App\Actions` namespace.
1. Default to `final readonly class` with constructor property promotion.
1. If the Action must store a result (ex: `$this->book`), keep it `final` but not `readonly`, and declare a private property for the result.
1. Always include explicit return types.

### Step 3: Implement the action flow

1. Typical flow:
   - validate input
   - perform data changes
   - log user action
   - update last activity date
   - refresh content presence (when journal entry content changes)
1. Validate ownership with `ModelNotFoundException` when a user does not own a journal or entry.
1. Validate input with `ValidationException::withMessages([...])` when values are invalid.
1. Sanitize user-provided text with `TextSanitizer::plainText()`.
1. Use Eloquent models and relationships. Avoid `DB::`.
1. Queue background work on the `low` queue:

```php
LogUserAction::dispatch(...)->onQueue('low');
UpdateUserLastActivityDate::dispatch($user)->onQueue('low');
CheckPresenceOfContentInJournalEntry::dispatch($entry)->onQueue('low');
```

1. If the Action mutates a journal entry module, reload the relationship before returning:

```php
$this->entry->load('moduleHealth');
```

### Step 4: Add tests

1. Create `tests/Unit/Actions/ActionNameTest.php`.
1. Use `RefreshDatabase` and `Queue::fake()`.
1. Use factories with explicit foreign keys. Never use `for()` on factories.
1. Cover:
   - happy path
   - invalid input (throws `ValidationException`)
   - unauthorized access (throws `ModelNotFoundException`)
   - queued jobs on `low` queue

### Step 5: Run tests and lint

1. Run the smallest relevant test file:

```bash
php artisan test tests/Unit/Actions/ActionNameTest.php
```

1. Run `composer journalos:unit`.
1. Run Pint:

```bash
vendor/bin/pint --dirty
```
