---
name: laravel-feature
description: Build a complete Laravel feature following TDD principles with models, migrations, factories, tests, validation, and Livewire class-based components. Use this for new CRUD features or complex business logic.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Laravel Feature Builder

Build production-ready Laravel features using TDD, following this project's conventions and Laravel Boost guidelines.

## Workflow

### 1. Discovery & Planning

- **Search existing code** for similar patterns using Glob/Grep
- **Check sibling files** to understand naming conventions, structure, validation style
- **Use TodoWrite** to create a detailed task list with all steps
- **Ask clarifying questions** about:
  - Model relationships and attributes
  - Validation rules and business logic
  - Authorization requirements (gates/policies)
  - UI requirements (Livewire class-based components)
  - Whether queued jobs are needed

### 2. Test-Driven Development

Always write tests FIRST, then implementation:

1. **Create Feature Test** using Pest

   ```bash
   php artisan make:test Features/[Feature]Test --pest --no-interaction
   ```

2. **Write failing test cases** covering:
   - Happy paths (successful operations)
   - Failure paths (validation errors, unauthorized access)
   - Edge cases (null values, empty strings, boundary conditions)
   - N+1 query prevention (use eager loading)

3. **Run tests to confirm failure**

   ```bash
   php artisan test --filter=[TestName]
   ```

4. **Implement feature** to make tests pass

5. **Run tests again** to confirm success

### 3. Database Layer

#### Models

```bash
php artisan make:model [ModelName] --factory --migration --seed --policy --no-interaction
```

**Model Conventions:**

- Use PHP 8 constructor property promotion
- Define relationships with explicit return types
- Use `casts()` method (not `$casts` property) - check sibling models
- Add useful PHPDoc array shapes for complex attributes
- Follow TitleCase for Enum keys

#### Migrations

- Use `php artisan make:migration` with descriptive names
- **IMPORTANT:** When modifying columns, include ALL previous attributes or they'll be dropped
- Add indexes for foreign keys and frequently queried columns
- Use `after()` for logical column ordering

#### Factories & Seeders

- Create realistic test data using Faker
- Check existing factories for custom states before creating manual setups
- Use relationship methods: `->for($user)`, `->has(Post::factory()->count(3))`

### 4. Validation Layer

**Always use Form Requests** (not inline validation):

```bash
php artisan make:request [Feature/Store][Model]Request --no-interaction
```

**Check sibling Form Requests** to determine:

- Array-based vs string-based validation rules
- Custom error message patterns
- Authorization logic structure

**Include comprehensive validation:**

- Required/optional fields
- Type validation (string, integer, boolean, array)
- Format validation (email, url, uuid, date)
- Relationship existence (exists:table,column)
- Business rule validation (unique, min/max, regex)
- Custom error messages

### 5. Livewire Components

**Create class-based Livewire components:**

```bash
php artisan make:livewire [Feature/ComponentName] --test --pest --no-interaction
```

**Livewire Component Example:**

```php
namespace App\Livewire\Features;

use App\Models\Post;
use Livewire\Component;
use Livewire\Attributes\Computed;

class PostList extends Component
{
    public string $search = '';

    public ?int $editing = null;

    #[Computed]
    public function posts()
    {
        return Post::query()
            ->when($this->search, fn($q) => $q->where('title', 'like', "%{$this->search}%"))
            ->with('author') // Prevent N+1
            ->latest()
            ->get();
    }

    public function edit(int $postId): void
    {
        $this->editing = $postId;
    }

    public function save(): void
    {
        $this->validate([
            'form.title' => 'required|string|max:255',
        ]);

        Post::create($this->form);

        $this->dispatch('post-created');
        $this->reset('form');
    }

    public function render()
    {
        return view('livewire.features.post-list');
    }
}
```

**Livewire Best Practices:**

- Single root element required in Blade views
- Use `wire:key` in loops with unique identifiers
- Add `wire:loading` states for better UX
- Use `wire:model.live.debounce.300ms` for search inputs
- Prevent N+1 queries with eager loading
- Validate in Livewire actions (server-side)
- Use `#[Computed]` attribute for derived properties

### 6. Flux UI Components

**Use Flux UI Pro components** when available:

Common components: accordion, autocomplete, avatar, badge, button, calendar, card, chart, checkbox, command, composer, context, date-picker, dropdown, editor, field, file-upload, heading, icon, input, kanban, modal, navbar, pagination, select, separator, table, tabs, textarea, time-picker, toast, tooltip

**Search documentation first:**

```text
Use Laravel Boost's search-docs tool with queries like:
['flux button variants', 'flux table', 'flux modal']
```

**Patterns:**

- Use `gap-*` utilities for spacing (not margins)
- **LIGHT MODE ONLY** - Never add dark mode support with `dark:` classes
- **Flux UI styling restrictions:** Flux components can ONLY be customized with padding/margins (e.g., `class="p-4 mt-2"`). Never add custom colors, typography, or borders to Flux components.
- Follow existing Tailwind conventions in sibling files

### 7. Testing Livewire Components

```php
use Livewire\Livewire;
use App\Livewire\Features\PostList;

test('creates post successfully', function () {
    $user = User::factory()->create();

    Livewire::test(PostList::class)
        ->actingAs($user)
        ->set('form.title', 'Test Post')
        ->call('save')
        ->assertHasNoErrors()
        ->assertDispatched('post-created');

    expect(Post::where('title', 'Test Post')->exists())->toBeTrue();
});

test('validates required fields', function () {
    Livewire::test(PostList::class)
        ->set('form.title', '')
        ->call('save')
        ->assertHasErrors(['form.title' => 'required']);
});
```

### 8. Code Quality

Before finalizing:

1. **Run Pint** to format code:

   ```bash
   vendor/bin/pint --dirty
   ```

2. **Run tests** with appropriate filter:

   ```bash
   php artisan test --filter=[FeatureName]
   ```

3. **Ask user** if they want to run full test suite

### 9. URL Generation & Routes

- Use **named routes** with `route('items.show', $item)`
- Use Laravel Boost's `get-absolute-url` tool for sharing project URLs
- Define routes in `routes/web.php` or appropriate route file

### 10. Configuration

**Never use `env()` outside config files!**

✅ Correct: `config('app.name')`
❌ Wrong: `env('APP_NAME')`

### 11. Authorization

Use Laravel's built-in features:

- **Gates** for simple checks
- **Policies** for model-specific authorization (created with `--policy` flag)
- Check authorization in Livewire actions AND controllers

## Common Patterns

### Queued Jobs

For time-consuming operations:

```bash
php artisan make:job Process[Something] --no-interaction
```

Implement `ShouldQueue` interface and dispatch:

```php
Process[Something]::dispatch($data);
```

### Eloquent Relationships

Always use explicit return types:

```php
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}

public function user(): BelongsTo
{
    return $this->belongsTo(User::class);
}
```

### API Resources (if building API)

```bash
php artisan make:resource [Model]Resource --no-interaction
```

Follow existing API conventions in the codebase.

## Output

After completing the feature:

1. ✅ Show **file references** with line numbers: `[ModelName.php:42](app/Models/ModelName.php#L42)`
2. ✅ **Run tests** and show passing results
3. ✅ **Ask user** if they want full test suite run
4. ✅ **Mark all todos as completed**

## Important Reminders

- **ALWAYS** follow existing code conventions
- **ALWAYS** write tests FIRST (TDD)
- **ALWAYS** run Pint before finalizing
- **ALWAYS** prevent N+1 queries with eager loading
- **ALWAYS** use class-based Livewire components (NOT Volt)
- **NEVER** add dark mode support (light mode only)
- **NEVER** customize Flux UI component colors, typography, or borders (only padding/margins allowed)
- **NEVER** use `env()` outside config files
- **NEVER** commit without running tests
- **NEVER** skip Form Request validation
- **CHECK** sibling files before creating new patterns
