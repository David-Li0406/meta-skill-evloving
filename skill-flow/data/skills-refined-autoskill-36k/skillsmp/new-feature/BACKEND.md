# Backend Implementation Guide

Step-by-step instructions for implementing backend components of a new feature.

## 1. Database Migration

**Create migration:**

```bash
php artisan make:migration create_[table]_table --no-interaction
# or
php artisan make:migration add_[field]_to_[table] --no-interaction
```

**Migration template:**

```php
public function up(): void
{
    Schema::create('feature_items', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('title');
        $table->text('description')->nullable();
        $table->enum('status', ['draft', 'active', 'archived'])->default('draft');
        $table->timestamps();

        $table->index(['user_id', 'status']);
    });
}

public function down(): void
{
    Schema::dropIfExists('feature_items');
}
```

**Run migration:**

```bash
php artisan migrate
```

## 2. Model

**Create model:**

```bash
php artisan make:model FeatureItem --no-interaction
```

**Model template:**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class FeatureItem extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'title',
        'description',
        'status',
    ];

    protected function casts(): array
    {
        return [
            'status' => 'string',
        ];
    }

    // Relationships
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('status', 'active');
    }

    public function scopeForUser($query, User $user)
    {
        return $query->where('user_id', $user->id);
    }
}
```

## 3. Factory

**Create factory:**

```bash
php artisan make:factory FeatureItemFactory --no-interaction
```

**Factory template:**

```php
<?php

namespace Database\Factories;

use App\Models\FeatureItem;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class FeatureItemFactory extends Factory
{
    protected $model = FeatureItem::class;

    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(3),
            'description' => fake()->paragraph(),
            'status' => 'draft',
        ];
    }

    public function active(): static
    {
        return $this->state(fn (array $attributes) => [
            'status' => 'active',
        ]);
    }

    public function archived(): static
    {
        return $this->state(fn (array $attributes) => [
            'status' => 'archived',
        ]);
    }
}
```

## 4. Form Request

**Create form request:**

```bash
php artisan make:request StoreFeatureItemRequest --no-interaction
```

**Form request template:**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreFeatureItemRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Or check policy
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:1000'],
            'status' => ['required', Rule::in(['draft', 'active', 'archived'])],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'Title is required',
            'title.max' => 'Title must be less than 255 characters',
            'description.max' => 'Description must be less than 1000 characters',
            'status.in' => 'Please select a valid status',
        ];
    }
}
```

## 5. Controller

**Create controller:**

```bash
php artisan make:controller FeatureItemController --no-interaction
```

**Controller template:**

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreFeatureItemRequest;
use App\Http\Requests\UpdateFeatureItemRequest;
use App\Models\FeatureItem;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

class FeatureItemController extends Controller
{
    public function index(): Response
    {
        $items = FeatureItem::query()
            ->forUser(auth()->user())
            ->latest()
            ->paginate(10);

        return Inertia::render('feature-items/index', [
            'items' => $items,
        ]);
    }

    public function create(): Response
    {
        return Inertia::render('feature-items/create');
    }

    public function store(StoreFeatureItemRequest $request): RedirectResponse
    {
        $item = FeatureItem::create([
            'user_id' => auth()->id(),
            ...$request->validated(),
        ]);

        return redirect()
            ->route('feature-items.show', $item)
            ->with('success', __('Item created successfully'));
    }

    public function show(FeatureItem $featureItem): Response
    {
        $this->authorize('view', $featureItem);

        return Inertia::render('feature-items/show', [
            'item' => $featureItem,
        ]);
    }

    public function edit(FeatureItem $featureItem): Response
    {
        $this->authorize('update', $featureItem);

        return Inertia::render('feature-items/edit', [
            'item' => $featureItem,
        ]);
    }

    public function update(UpdateFeatureItemRequest $request, FeatureItem $featureItem): RedirectResponse
    {
        $this->authorize('update', $featureItem);

        $featureItem->update($request->validated());

        return redirect()
            ->route('feature-items.show', $featureItem)
            ->with('success', __('Item updated successfully'));
    }

    public function destroy(FeatureItem $featureItem): RedirectResponse
    {
        $this->authorize('delete', $featureItem);

        $featureItem->delete();

        return redirect()
            ->route('feature-items.index')
            ->with('success', __('Item deleted successfully'));
    }
}
```

## 6. Routes

**Add to routes/web.php:**

```php
// Feature Items
Route::middleware(['auth', 'verified'])->group(function () {
    Route::resource('feature-items', FeatureItemController::class);
});
```

**Generate Wayfinder routes:**

```bash
php artisan wayfinder:generate
```

## 7. Policy (Authorization)

**Create policy:**

```bash
php artisan make:policy FeatureItemPolicy --model=FeatureItem --no-interaction
```

**Policy template:**

```php
<?php

namespace App\Policies;

use App\Models\FeatureItem;
use App\Models\User;

class FeatureItemPolicy
{
    public function view(User $user, FeatureItem $featureItem): bool
    {
        return $user->id === $featureItem->user_id;
    }

    public function update(User $user, FeatureItem $featureItem): bool
    {
        return $user->id === $featureItem->user_id;
    }

    public function delete(User $user, FeatureItem $featureItem): bool
    {
        return $user->id === $featureItem->user_id;
    }
}
```

**Register in AuthServiceProvider or auto-discovery.**
