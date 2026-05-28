---
id: php-eloquent
name: "Eloquent Patterns"
domain: PHP
skill: faion-software-developer
category: "backend"
---

## Eloquent Patterns

### Problem
Efficient database queries with Eloquent ORM.

### Framework: Model Definition

```php
<?php
// app/Models/User.php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Builder;

class User extends Authenticatable
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'settings' => 'array',
    ];

    // Relationships
    public function orders(): HasMany
    {
        return $this->hasMany(Order::class);
    }

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class)
            ->withTimestamps()
            ->withPivot('assigned_by');
    }

    // Scopes
    public function scopeActive(Builder $query): Builder
    {
        return $query->where('is_active', true);
    }

    public function scopeWithRole(Builder $query, string $role): Builder
    {
        return $query->whereHas('roles', fn ($q) => $q->where('name', $role));
    }

    public function scopeSearch(Builder $query, ?string $term): Builder
    {
        if (empty($term)) {
            return $query;
        }

        return $query->where(function ($q) use ($term) {
            $q->where('name', 'LIKE', "%{$term}%")
              ->orWhere('email', 'LIKE', "%{$term}%");
        });
    }

    // Accessors & Mutators
    protected function email(): Attribute
    {
        return Attribute::make(
            set: fn (string $value) => strtolower($value),
        );
    }

    // Methods
    public function hasRole(string $role): bool
    {
        return $this->roles()->where('name', $role)->exists();
    }
}
```

### Repository Pattern

```php
<?php
// app/Repositories/UserRepository.php

namespace App\Repositories;

use App\Models\User;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

class UserRepository
{
    public function __construct(
        private readonly User $model
    ) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->model
            ->with(['roles'])
            ->latest()
            ->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->model
            ->with(['roles', 'orders'])
            ->findOrFail($id);
    }

    public function create(array $data): User
    {
        return $this->model->create($data);
    }

    public function update(int $id, array $data): User
    {
        $user = $this->model->findOrFail($id);
        $user->update($data);
        return $user->fresh();
    }

    public function delete(int $id): bool
    {
        return $this->model->findOrFail($id)->delete();
    }

    public function findByEmail(string $email): ?User
    {
        return $this->model->where('email', $email)->first();
    }
}
```

### Agent

faion-backend-agent
