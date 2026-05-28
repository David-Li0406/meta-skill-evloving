---
title: Always Define $fillable or $guarded
impact: CRITICAL
impactDescription: Prevents mass assignment vulnerabilities
tags: security, mass-assignment, fillable, guarded
---

## Always Define $fillable or $guarded

Mass assignment allows attackers to modify unintended fields. Always explicitly define which attributes are mass assignable.

**Incorrect (unprotected model):**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    // ❌ No protection - all attributes can be mass assigned
    // Attacker can set: is_admin, role, email_verified_at, etc.
}

// Controller
public function store(Request $request)
{
    // ❌ Creates user with ALL request data
    User::create($request->all());
}
```

**Correct (protected with $fillable):**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    // ✓ Only these fields can be mass assigned
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    // Sensitive fields automatically protected:
    // is_admin, role, email_verified_at, etc.
}

// Controller
public function store(Request $request)
{
    // ✓ Only fillable fields are set
    User::create($request->validated());
}
```

**Alternative: using $guarded:**

```php
<?php

class User extends Model
{
    // Block specific fields, allow everything else
    protected $guarded = [
        'id',
        'is_admin',
        'role',
        'email_verified_at',
    ];
}

// Empty guarded = allow all (dangerous, but explicit)
protected $guarded = []; // Only if you know what you're doing
```

**Best practice - combine with validation:**

```php
<?php

public function store(StoreUserRequest $request)
{
    // ✓ Validated AND fillable protection
    User::create($request->validated());
}

// StoreUserRequest
public function rules(): array
{
    return [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'unique:users'],
        'password' => ['required', 'min:8', 'confirmed'],
        // is_admin, role NOT in rules = can't be submitted
    ];
}
```

Reference: [Mass Assignment](https://laravel.com/docs/eloquent#mass-assignment)
