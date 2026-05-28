# Advanced Form Patterns

Complex form patterns including multi-step forms, dynamic fields, and relationships.

## Multi-Step Forms

```php
public int $step = 1;

public function nextStep(): void
{
    // Validate current step
    match($this->step) {
        1 => $this->validate(['title' => 'required']),
        2 => $this->validate(['email' => 'required|email']),
    };

    $this->step++;
}

public function previousStep(): void
{
    $this->step--;
}

public function submit(): void
{
    $validated = $this->validate();
    Post::create($validated);
}
```

```blade
@if ($step === 1)
    <!-- Step 1 fields -->
    <flux:button wire:click="nextStep">Next</flux:button>
@elseif ($step === 2)
    <!-- Step 2 fields -->
    <flux:button wire:click="previousStep">Back</flux:button>
    <flux:button wire:click="nextStep">Next</flux:button>
@else
    <!-- Step 3 / Review -->
    <flux:button wire:click="previousStep">Back</flux:button>
    <flux:button wire:click="submit">Submit</flux:button>
@endif
```

## Dynamic Fields

```php
public array $items = [['name' => '', 'quantity' => 1]];

public function addItem(): void
{
    $this->items[] = ['name' => '', 'quantity' => 1];
}

public function removeItem(int $index): void
{
    array_splice($this->items, $index, 1);
}
```

```blade
@foreach ($items as $index => $item)
    <div wire:key="item-{{ $index }}" class="flex gap-4">
        <flux:input wire:model="items.{{ $index }}.name" />
        <flux:input type="number" wire:model="items.{{ $index }}.quantity" />
        <flux:button variant="ghost" wire:click="removeItem({{ $index }})">Remove</flux:button>
    </div>
@endforeach

<flux:button wire:click="addItem">Add Item</flux:button>
```

## Form with Relationships

```php
public string $title = '';
public ?int $categoryId = null;
public array $tagIds = [];

public function save(): void
{
    $validated = $this->validate([
        'title' => 'required|string|max:255',
        'categoryId' => 'required|exists:categories,id',
        'tagIds' => 'array',
        'tagIds.*' => 'exists:tags,id',
    ]);

    $post = Post::create([
        'title' => $validated['title'],
        'category_id' => $validated['categoryId'],
    ]);

    $post->tags()->sync($validated['tagIds']);
}
```

```blade
<flux:select wire:model="categoryId">
    @foreach ($categories as $category)
        <flux:option value="{{ $category->id }}">{{ $category->name }}</flux:option>
    @endforeach
</flux:select>

<!-- Multiple select -->
<flux:select wire:model="tagIds" multiple>
    @foreach ($tags as $tag)
        <flux:option value="{{ $tag->id }}">{{ $tag->name }}</flux:option>
    @endforeach
</flux:select>
```
