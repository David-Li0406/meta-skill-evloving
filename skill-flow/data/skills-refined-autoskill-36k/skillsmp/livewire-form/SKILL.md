---
name: livewire-form
description: Create production-ready class-based Livewire v4 forms with validation, loading states, error handling, and Flux UI components (light mode only). Use this for data entry, user input, and CRUD operations.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Livewire v4 Form Builder

Build elegant, validated class-based Livewire v4 forms using Flux UI Pro components and Laravel best practices.

## Pre-Flight Checklist

1. **Check existing Livewire components** to determine:
   - Validation patterns (inline vs Form Request)
   - Flux UI component usage patterns
   - Common component structure

2. **Search Flux documentation** using Laravel Boost:
   ```text
   Use search-docs tool with queries like:
   ['flux input validation', 'flux select', 'flux button variants']
   ```

3. **Understand Flux UI styling rules:**
   - Flux components can ONLY be customized with spacing utilities (padding, margins)
   - NEVER add custom colors, typography, borders, or other styling to Flux components
   - Valid: `<flux:button class="mt-4 px-6">`
   - Invalid: `<flux:button class="text-blue-500 border-2 font-bold">`

4. **Plan with TodoWrite** for complex forms

## Form Creation Workflow

### 1. Create Livewire Component

```bash
php artisan make:livewire [Feature/FormName] --test --pest --no-interaction
```

### 2. Build Component Class (Livewire v4)

```php
namespace App\Livewire\Features;

use App\Models\Post;
use Livewire\Attributes\Computed;
use Livewire\Attributes\Locked;
use Livewire\Attributes\On;
use Livewire\Component;

class PostForm extends Component
{
    // Typed public properties (Livewire v4 best practice)
    public string $title = '';
    public string $content = '';
    public ?int $categoryId = null;
    public bool $published = false;

    // Use #[Locked] for properties that shouldn't be modified from frontend
    #[Locked]
    public ?int $postId = null;

    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'content' => 'required|string',
            'categoryId' => 'required|exists:categories,id',
            'published' => 'boolean',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'Please enter a title',
            'categoryId.required' => 'Please select a category',
        ];
    }

    // Use #[On('event')] instead of $listeners property
    #[On('category-selected')]
    public function setCategory(int $categoryId): void
    {
        $this->categoryId = $categoryId;
    }

    // Use #[Computed] for derived properties (cached until dependencies change)
    #[Computed]
    public function categories(): \Illuminate\Support\Collection
    {
        return Category::orderBy('name')->get();
    }

    public function save(): void
    {
        $validated = $this->validate();

        Post::create([
            'title' => $validated['title'],
            'content' => $validated['content'],
            'category_id' => $validated['categoryId'],
            'published' => $validated['published'],
        ]);

        $this->dispatch('post-created');
        session()->flash('success', 'Post created successfully!');
        $this->redirect(route('posts.index'));
    }

    public function render(): \Illuminate\Contracts\View\View
    {
        return view('livewire.features.post-form');
    }
}
```

### 3. Build Blade View

**Basic form structure:**
```blade
<flux:card>
    <flux:heading>Create Post</flux:heading>

    <form wire:submit="save" class="space-y-6">
        <!-- Text input -->
        <flux:field>
            <flux:label>Title</flux:label>
            <flux:input wire:model.blur="title" placeholder="Enter title" required />
            <flux:error name="title" />
        </flux:field>

        <!-- Select dropdown -->
        <flux:field>
            <flux:label>Category</flux:label>
            <flux:select wire:model="categoryId" placeholder="Choose...">
                @foreach($categories as $category)
                    <flux:option value="{{ $category->id }}">{{ $category->name }}</flux:option>
                @endforeach
            </flux:select>
            <flux:error name="categoryId" />
        </flux:field>

        <!-- Textarea -->
        <flux:field>
            <flux:label>Content</flux:label>
            <flux:textarea wire:model.blur="content" rows="4" />
            <flux:error name="content" />
        </flux:field>

        <!-- Checkbox -->
        <flux:field>
            <flux:checkbox wire:model.boolean="published">
                <flux:label>Published</flux:label>
            </flux:checkbox>
        </flux:field>

        <!-- Submit button with loading state -->
        <flux:button type="submit" variant="primary" wire:loading.attr="disabled">
            <span wire:loading.remove wire:target="save">Save</span>
            <span wire:loading wire:target="save">Saving...</span>
        </flux:button>
    </form>
</flux:card>
```

**For complete component examples, see:** `references/flux-components.md`

### 4. Wire Modifiers

Choose the right modifier for optimal UX:

| Modifier | Use Case | Update Timing |
|----------|----------|---------------|
| `wire:model.blur` | **Standard form fields (recommended)** | On blur |
| `wire:model.live` | Real-time updates | Every keystroke |
| `wire:model.live.debounce.300ms` | Search inputs | After 300ms delay |
| `wire:model` | Deferred updates | On form submit |

```blade
<!-- Standard form field (recommended) -->
<flux:input wire:model.blur="title" />

<!-- Real-time search -->
<flux:input wire:model.live.debounce.300ms="search" />
```

### 5. Validation

**Inline validation (simple forms):**
```php
public function rules(): array
{
    return [
        'title' => 'required|string|max:255',
        'email' => 'required|email|unique:users,email',
    ];
}

public function messages(): array
{
    return [
        'title.required' => 'Please enter a title',
    ];
}
```

**Real-time validation:**
```php
public function updated($propertyName): void
{
    $this->validateOnly($propertyName);
}

// Or validate specific field
public function updatedEmail(): void
{
    $this->validateOnly('email');
}
```

**Form Request (complex forms):**
```bash
php artisan make:request Store[Model]Request --no-interaction
```

```php
use App\Http\Requests\StorePostRequest;

public function save(StorePostRequest $request): void
{
    $validated = $request->validated();
    Post::create($validated);
}
```

### 6. Loading States

Always provide visual feedback:

```blade
<flux:button type="submit" wire:loading.attr="disabled" wire:click="save">
    <span wire:loading.remove wire:target="save">Save</span>
    <span wire:loading wire:target="save">Saving...</span>
</flux:button>

<!-- Disable field during submission -->
<flux:input
    wire:model.blur="title"
    wire:loading.attr="disabled"
    wire:target="save"
/>
```

### 7. Error Handling

**Individual field errors:**
```blade
<flux:error name="title" />
```

**All errors:**
```blade
@if ($errors->any())
    <flux:callout variant="danger">
        <ul class="list-disc list-inside">
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </flux:callout>
@endif
```

**Conditional error display:**
```blade
@error('email')
    <flux:badge variant="danger">{{ $message }}</flux:badge>
@enderror
```

### 8. Success Feedback

**Flash messages:**
```php
public function save(): void
{
    $validated = $this->validate();
    Post::create($validated);

    session()->flash('success', 'Post created successfully!');
    $this->redirect(route('posts.index'));
}
```

```blade
@if (session('success'))
    <flux:callout variant="success">
        {{ session('success') }}
    </flux:callout>
@endif
```

**Toast notifications (Flux Pro):**
```php
public function save(): void
{
    $validated = $this->validate();
    Post::create($validated);

    $this->dispatch('toast', message: 'Saved!', variant: 'success');
}
```

### 9. Testing Forms

```php
use Livewire\Livewire;
use App\Livewire\Features\PostForm;

test('creates post with valid data', function () {
    $category = Category::factory()->create();

    Livewire::test(PostForm::class)
        ->set('title', 'Test Post')
        ->set('content', 'Test content')
        ->set('categoryId', $category->id)
        ->call('save')
        ->assertHasNoErrors()
        ->assertDispatched('post-created');

    expect(Post::where('title', 'Test Post')->exists())->toBeTrue();
});

test('validates required fields', function () {
    Livewire::test(PostForm::class)
        ->set('title', '')
        ->call('save')
        ->assertHasErrors(['title']);
});
```

## Advanced Patterns

For complex form scenarios, see:
- **Multi-step forms** → `references/advanced-patterns.md`
- **Dynamic fields** → `references/advanced-patterns.md`
- **Form with relationships** → `references/advanced-patterns.md`
- **Complete working example** → `references/complete-example.md`

## Quick Reference

### Common Flux Components

| Component | Usage |
|-----------|-------|
| `<flux:input>` | Text, email, password, number inputs |
| `<flux:textarea>` | Multi-line text |
| `<flux:select>` | Dropdown selection |
| `<flux:checkbox>` | Boolean/toggle |
| `<flux:radio>` | Single choice from group |
| `<flux:date-picker>` | Date selection (Pro) |
| `<flux:file-upload>` | File uploads (Pro) |

See `references/flux-components.md` for detailed examples.

### Wire Directives

| Directive | Purpose |
|-----------|---------|
| `wire:model.blur="field"` | Update on blur (recommended) |
| `wire:loading` | Show during request |
| `wire:loading.attr="disabled"` | Disable during request |
| `wire:target="method"` | Scope loading to method |
| `wire:key="unique-id"` | Required in loops |

## Output Checklist

- ✅ Form validates all inputs
- ✅ Loading states on submit button
- ✅ Error messages display clearly
- ✅ Success feedback provided
- ✅ Accessibility (labels, required attributes)
- ✅ Tests written and passing
- ✅ Uses class-based Livewire components
- ✅ Uses Flux UI components consistently
- ✅ Light mode only (no dark mode support)
- ✅ Code formatted with Pint

## Livewire v4 Attributes

| Attribute | Purpose |
|-----------|---------|
| `#[On('event')]` | Listen for events (replaces `$listeners` property) |
| `#[Computed]` | Cache derived property until dependencies change |
| `#[Locked]` | Prevent property modification from frontend |
| `#[Renderless]` | Skip re-rendering after method call |
| `#[Validate]` | Inline validation on property |

### New v4 Directives

| Directive | Purpose |
|-----------|---------|
| `wire:sort` | Drag-and-drop sorting |
| `wire:intersect` | Trigger action when element enters viewport |
| `wire:ref` | Element reference for JavaScript interaction |
| `.renderless` modifier | Skip re-rendering for specific action |
| `.preserve-scroll` modifier | Maintain scroll position |

## Important Reminders

- **ALWAYS** use class-based Livewire components (NOT Volt)
- **ALWAYS** use `#[On('event')]` attribute for event listeners (NOT `$listeners` property)
- **ALWAYS** use typed properties with explicit return types on all methods
- **ALWAYS** use `wire:model.blur` for standard inputs (better UX than `.live`)
- **ALWAYS** add loading states to submit buttons
- **ALWAYS** use `wire:key` in dynamic field loops
- **ALWAYS** validate on the server (Livewire actions)
- **ALWAYS** provide error feedback for each field
- **NEVER** add dark mode support (light mode only)
- **NEVER** customize Flux UI component colors, typography, or borders (only padding/margins)
- **NEVER** trust client-side validation alone
- **NEVER** use Volt (use class-based Livewire)
- **NEVER** use `protected $listeners` (use `#[On]` attribute instead)
- **SEARCH** Flux documentation before creating custom components
