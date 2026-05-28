# Complete Form Example

Full working example of a Livewire form with Flux UI components.

## Component Class

```php
namespace App\Livewire\Features;

use App\Models\{Post, Category};
use Livewire\Component;

class CreatePost extends Component
{
    public string $title = '';
    public string $content = '';
    public ?int $categoryId = null;
    public bool $published = false;

    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'content' => 'required|string',
            'categoryId' => 'required|exists:categories,id',
            'published' => 'boolean',
        ];
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

        session()->flash('success', 'Post created!');
        $this->redirect(route('posts.index'));
    }

    public function render()
    {
        return view('livewire.features.create-post', [
            'categories' => Category::pluck('name', 'id'),
        ]);
    }
}
```

## Blade View

```blade
<div>
    <flux:card>
        <flux:heading>Create New Post</flux:heading>

        @if (session('success'))
            <flux:callout variant="success">{{ session('success') }}</flux:callout>
        @endif

        <form wire:submit="save" class="space-y-6">
            <flux:field>
                <flux:label>Title</flux:label>
                <flux:input wire:model.blur="title" placeholder="Enter post title" required />
                <flux:error name="title" />
            </flux:field>

            <flux:field>
                <flux:label>Category</flux:label>
                <flux:select wire:model="categoryId" placeholder="Choose category...">
                    @foreach ($categories as $id => $name)
                        <flux:option value="{{ $id }}">{{ $name }}</flux:option>
                    @endforeach
                </flux:select>
                <flux:error name="categoryId" />
            </flux:field>

            <flux:field>
                <flux:label>Content</flux:label>
                <flux:textarea wire:model.blur="content" rows="6" />
                <flux:error name="content" />
            </flux:field>

            <flux:field>
                <flux:checkbox wire:model.boolean="published">
                    <flux:label>Publish immediately</flux:label>
                </flux:checkbox>
            </flux:field>

            <div class="flex gap-4 justify-end">
                <flux:button variant="ghost" href="{{ route('posts.index') }}">Cancel</flux:button>
                <flux:button type="submit" variant="primary" wire:loading.attr="disabled">
                    <span wire:loading.remove wire:target="save">Create Post</span>
                    <span wire:loading wire:target="save">Creating...</span>
                </flux:button>
            </div>
        </form>
    </flux:card>
</div>
```

## Tests

```php
use Livewire\Livewire;
use App\Livewire\Features\CreatePost;

test('creates post with valid data', function () {
    $category = Category::factory()->create();

    Livewire::test(CreatePost::class)
        ->set('title', 'Test Post')
        ->set('content', 'Test content')
        ->set('categoryId', $category->id)
        ->call('save')
        ->assertHasNoErrors()
        ->assertRedirect(route('posts.index'));

    expect(Post::where('title', 'Test Post')->exists())->toBeTrue();
});

test('validates required fields', function () {
    Livewire::test(CreatePost::class)
        ->set('title', '')
        ->set('content', '')
        ->call('save')
        ->assertHasErrors(['title', 'content']);
});
```
