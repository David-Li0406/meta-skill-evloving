# Livewire Refactoring Patterns

## Common Livewire Anti-Patterns and Solutions

### 1. Business Logic in Components

**Problem:**

```php
// Bad: Business logic directly in Livewire component
class CreatePost extends Component
{
    public $title;
    public $content;

    public function save()
    {
        $this->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        $post = Post::create([
            'title' => $this->title,
            'content' => $this->content,
            'user_id' => auth()->id(),
            'slug' => Str::slug($this->title),
        ]);

        // Generate thumbnail
        $thumbnail = ImageProcessor::process($post->featured_image);
        $post->update(['thumbnail' => $thumbnail]);

        // Send notifications
        Notification::send(
            User::where('subscribed', true)->get(),
            new NewPostNotification($post)
        );

        session()->flash('message', 'Post created!');
        return redirect()->route('posts.index');
    }
}
```

**Solution: Delegate to Actions/Services**

```php
// Good: Thin component, business logic in action
class CreatePost extends Component
{
    public $title;
    public $content;

    public function save(CreatePostAction $action)
    {
        $validated = $this->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        $post = $action->execute($validated);

        session()->flash('message', 'Post created!');
        return redirect()->route('posts.index');
    }
}
```

### 2. Improper Property Binding

**Problem:**

```php
// Bad: Binding entire model (security risk)
class EditUser extends Component
{
    public User $user;

    public function mount(User $user)
    {
        $this->user = $user;
    }
}

<!-- Wire:model directly on model - exposes everything -->
<input wire:model="user.email">
<input wire:model="user.password"> <!-- DANGEROUS! -->
```

**Solution: Bind Specific Properties**

```php
// Good: Bind only necessary properties
class EditUser extends Component
{
    public $name;
    public $email;
    public $bio;

    private User $user;

    public function mount(User $user)
    {
        $this->user = $user;
        $this->name = $user->name;
        $this->email = $user->email;
        $this->bio = $user->bio;
    }

    public function save()
    {
        $validated = $this->validate([
            'name' => 'required',
            'email' => 'required|email',
            'bio' => 'nullable',
        ]);

        $this->user->update($validated);
    }
}
```

### 3. Missing Real-Time Validation

**Problem:**

```php
// Bad: Validation only on submit
class UserForm extends Component
{
    public $email;

    public function submit()
    {
        $this->validate(['email' => 'required|email|unique:users']);
    }
}
```

**Solution: Real-Time Validation**

```php
// Good: Validate as user types
class UserForm extends Component
{
    public $email;

    protected $rules = [
        'email' => 'required|email|unique:users',
    ];

    public function updated($propertyName)
    {
        $this->validateOnly($propertyName);
    }

    public function submit()
    {
        $this->validate();
        // ...
    }
}
```

### 4. Inefficient Computed Properties

**Problem:**

```php
// Bad: Query runs every render
class ShowPosts extends Component
{
    public function render()
    {
        return view('livewire.show-posts', [
            'posts' => Post::with('user')
                ->where('published', true)
                ->latest()
                ->get(),
        ]);
    }
}
```

**Solution: Use Computed Properties**

```php
// Good: Cache computed properties
class ShowPosts extends Component
{
    use WithCaching;

    #[Computed]
    public function posts()
    {
        return Post::with('user')
            ->where('published', true)
            ->latest()
            ->get();
    }

    public function render()
    {
        return view('livewire.show-posts');
    }
}

<!-- In view: access as property -->
@foreach($this->posts as $post)
    ...
@endforeach
```

### 5. Not Using Livewire Forms (Livewire 3)

**Problem:**

```php
// Bad: Manual property management
class ContactForm extends Component
{
    public $name;
    public $email;
    public $message;

    protected $rules = [
        'name' => 'required',
        'email' => 'required|email',
        'message' => 'required',
    ];

    public function submit()
    {
        $validated = $this->validate();
        // ...
        $this->reset();
    }
}
```

**Solution: Use Form Objects (Livewire 3)**

```php
// Good: Form objects
use Livewire\Form;

class ContactForm extends Form
{
    public $name = '';
    public $email = '';
    public $message = '';

    public function rules()
    {
        return [
            'name' => 'required',
            'email' => 'required|email',
            'message' => 'required',
        ];
    }

    public function submit()
    {
        $this->validate();
        // Handle submission
        $this->reset();
    }
}

class Contact extends Component
{
    public ContactForm $form;

    public function save()
    {
        $this->form->submit();
    }
}
```

### 6. Missing Loading States

**Problem:**

```php
<!-- Bad: No loading feedback -->
<button wire:click="save">
    Save
</button>
```

**Solution: Add Loading States**

```php
<!-- Good: Loading indicators -->
<button
    wire:click="save"
    wire:loading.attr="disabled"
    wire:loading.class="opacity-50"
>
    <span wire:loading.remove wire:target="save">Save</span>
    <span wire:loading wire:target="save">Saving...</span>
</button>

<!-- Better: Skeleton loaders for content -->
<div wire:loading.remove wire:target="loadMore">
    @foreach($posts as $post)
        <x-post-card :post="$post" />
    @endforeach
</div>

<div wire:loading wire:target="loadMore">
    <x-skeleton-loader />
</div>
```

### 7. Not Using Events for Component Communication

**Problem:**

```php
// Bad: Tight coupling between components
class ParentComponent extends Component
{
    public function refreshChild()
    {
        // Can't easily refresh child component
    }
}

class ChildComponent extends Component
{
    // No way to trigger refresh from parent
}
```

**Solution: Use Livewire Events**

```php
// Good: Event-driven communication
class ParentComponent extends Component
{
    public function refresh()
    {
        $this->dispatch('posts-updated');
    }
}

class ChildComponent extends Component
{
    #[On('posts-updated')]
    public function refreshPosts()
    {
        $this->posts = Post::latest()->get();
    }
}
```

### 8. Polling Without Conditionals

**Problem:**

```php
// Bad: Always polling, even when not needed
class Dashboard extends Component
{
    use WithPolling;

    public function render()
    {
        return view('livewire.dashboard', [
            'stats' => $this->getStats(),
        ]);
    }
}
```

**Solution: Conditional Polling**

```php
// Good: Poll only when necessary
class Dashboard extends Component
{
    public $isActive = false;

    public function render()
    {
        return view('livewire.dashboard', [
            'stats' => $this->getStats(),
        ]);
    }
}

<!-- View: Conditional polling -->
<div wire:poll.5s="$isActive">
    <!-- Content -->
</div>
```

### 9. File Upload Without Progress

**Problem:**

```php
// Bad: No upload feedback
class UploadDocument extends Component
{
    public $document;

    public function save()
    {
        $this->validate(['document' => 'required|file|max:10240']);
        $this->document->store('documents');
    }
}
```

**Solution: Upload with Progress**

```php
// Good: Progress indicators
class UploadDocument extends Component
{
    public $document;
    public $uploadProgress = 0;

    public function updatedDocument()
    {
        $this->validate(['document' => 'required|file|max:10240']);
    }

    public function save()
    {
        $path = $this->document->store('documents');
        $this->reset('document', 'uploadProgress');
    }
}

<!-- View -->
<input
    type="file"
    wire:model="document"
    x-on:livewire-upload-start="uploading = true"
    x-on:livewire-upload-finish="uploading = false"
    x-on:livewire-upload-progress="progress = $event.detail.progress"
>

<div x-show="uploading">
    <progress max="100" x-bind:value="progress"></progress>
</div>
```

### 10. Not Lazy Loading Components

**Problem:**

```php
<!-- Bad: Heavy component loads immediately -->
<livewire:analytics-dashboard />
<livewire:user-activity-chart />
<livewire:slow-data-table />
```

**Solution: Lazy Load Heavy Components**

```php
<!-- Good: Lazy loading with placeholders -->
<livewire:analytics-dashboard lazy />

<livewire:user-activity-chart
    lazy
    placeholder="<div class='animate-pulse bg-gray-200 h-64'></div>"
/>

<!-- Or using wire:init for manual control -->
<div wire:init="loadData">
    @if($dataLoaded)
        <x-data-table :data="$data" />
    @else
        <x-loading-spinner />
    @endif
</div>
```

## Livewire 3 Migration Patterns

### Property Declarations

```php
// Livewire 2
class Counter extends Component
{
    public $count = 0;
}

// Livewire 3: Type hints required for non-primitive types
class Counter extends Component
{
    public int $count = 0;
    public Collection $items;
    public ?User $user = null;
}
```

### Lifecycle Hooks

```php
// Livewire 2
public function mount() { }
public function hydrate() { }
public function dehydrate() { }

// Livewire 3: Attributes
#[On('mount')]
public function initialize() { }

#[On('hydrate')]
public function onHydrate() { }
```

### Computed Properties

```php
// Livewire 2
public function getPostsProperty()
{
    return Post::all();
}

// Livewire 3: Attribute
#[Computed]
public function posts()
{
    return Post::all();
}

// Access in view: $this->posts (same)
```

### Validation

```php
// Livewire 2
protected $rules = ['email' => 'required|email'];

// Livewire 3: Still works, but Forms are preferred
#[Rule('required|email')]
public string $email = '';

// Or use Form objects
public ContactForm $form;
```

## Performance Optimization Patterns

### 1. Reduce Component Nesting

```php
// Bad: Deep nesting causes many roundtrips
<livewire:parent>
    <livewire:child>
        <livewire:grandchild>
            <!-- Too many levels -->
        </livewire:grandchild>
    </livewire:child>
</livewire:parent>

// Good: Flatten when possible
<livewire:optimized-component :data="$consolidatedData" />
```

### 2. Use wire:model.lazy for Non-Critical Fields

```php
<!-- Bad: Updates on every keystroke -->
<textarea wire:model="description"></textarea>

<!-- Good: Updates on blur -->
<textarea wire:model.lazy="description"></textarea>

<!-- Also consider debouncing -->
<input wire:model.debounce.500ms="search">
```

### 3. Batch Related Operations

```php
// Bad: Multiple server roundtrips
public function updateQuantity($itemId, $quantity)
{
    $this->items[$itemId] = $quantity;
    $this->calculateTotal(); // Another roundtrip
}

// Good: Batch operations
public function updateQuantity($itemId, $quantity)
{
    $this->items[$itemId] = $quantity;
}

public function updated($property)
{
    if (Str::startsWith($property, 'items.')) {
        $this->calculateTotal();
    }
}
```

### 4. Defer Loading

```php
// Bad: Everything loads immediately
class Dashboard extends Component
{
    public $stats;
    public $charts;
    public $users;

    public function mount()
    {
        $this->stats = $this->getStats(); // Slow
        $this->charts = $this->getCharts(); // Slow
        $this->users = $this->getUsers(); // Slow
    }
}

// Good: Progressive loading
class Dashboard extends Component
{
    public $statsLoaded = false;
    public $chartsLoaded = false;

    public function loadStats()
    {
        $this->stats = $this->getStats();
        $this->statsLoaded = true;
    }

    public function loadCharts()
    {
        $this->charts = $this->getCharts();
        $this->chartsLoaded = true;
    }
}
```
