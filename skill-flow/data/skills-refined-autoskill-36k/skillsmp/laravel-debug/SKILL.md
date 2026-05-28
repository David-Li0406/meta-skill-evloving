---
name: laravel-debug
description: Debug Laravel application issues using browser logs, tinker, database queries, and systematic troubleshooting. Use this when encountering errors, unexpected behavior, or performance issues.
allowed-tools: Bash,Read,Grep,Glob
---

# Laravel Debugger

Systematically debug Laravel applications using Laravel Boost tools and best practices.

## Debugging Workflow

### 1. Gather Information

**Read recent browser logs** (Laravel Boost tool):
- Only recent logs are useful; ignore old ones
- Look for JavaScript errors, console warnings, failed requests
- Check for 419 (session expired), 403 (forbidden), 404 (not found), 500 (server error)

**Check Laravel logs:**
```bash
tail -n 50 storage/logs/laravel.log
```

**Review error details:**
- Exception type and message
- Stack trace and file/line numbers
- Request data (method, URL, parameters)
- User context (authenticated, permissions)

### 2. Reproduce the Issue

**Create a focused test** to reproduce:
```bash
php artisan make:test Debug/[Issue]Test --pest --no-interaction
```

Write a minimal test that triggers the bug:
```php
test('reproduces [issue description]', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->post('/endpoint', ['data' => 'value']);

    // Add assertion that currently fails
    $response->assertSuccessful();
});
```

Run the test:
```bash
php artisan test --filter=[TestName]
```

### 3. Use Laravel Boost Tools

#### Tinker for PHP/Eloquent Debugging
Use Laravel Boost's `tinker` tool to:
- Query Eloquent models directly
- Test relationships and scopes
- Debug query results
- Execute PHP to verify logic

**When to use tinker:**
- Need to inspect database records
- Test model methods
- Verify relationships work correctly
- Check query results

#### Database Query for Read-Only Operations
Use Laravel Boost's `database-query` tool when you only need to read from database:
- Faster than tinker for simple queries
- Good for checking data existence
- Useful for inspecting table structure

#### Browser Logs
Use Laravel Boost's `browser-logs` tool to:
- Read JavaScript errors
- See failed AJAX/Livewire requests
- Check console warnings
- Only recent logs are useful!

### 4. Common Issue Patterns

#### Vite/Asset Issues
**Error:** "Unable to locate file in Vite manifest"

**Solutions:**
1. Build assets: `npm run build`
2. Ask user to run: `npm run dev` or `composer run dev`
3. Check `vite.config.js` for correct paths

#### N+1 Query Problems
**Symptoms:** Slow page loads, many database queries

**Debug:**
```bash
# Enable query logging in tinker
DB::enableQueryLog();
# Run your code
DB::getQueryLog();
```

**Fix:** Add eager loading
```php
// ❌ Bad: N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // Separate query each time!
}

// ✅ Good: 2 queries total
$posts = Post::with('user')->get();
foreach ($posts as $post) {
    echo $post->user->name;
}
```

#### Validation Errors Not Showing
**Check:**
1. Form Request exists and is being used
2. Validation rules are correct
3. Frontend displays `$errors` variable
4. Livewire components call `$this->validate()`

**Test validation:**
```php
test('validates required field', function () {
    $response = $this->post('/endpoint', ['field' => '']);

    $response->assertSessionHasErrors(['field']);
});
```

#### Authorization Issues (403 Forbidden)
**Debug steps:**
1. Check if user is authenticated
2. Verify policy exists and is correct
3. Test gate/policy in tinker:
```php
$user = User::find(1);
$post = Post::find(1);
$user->can('update', $post); // Should return true/false
```

4. Check middleware is applied correctly in routes

#### Session/CSRF Issues (419)
**Common causes:**
- Session expired
- CSRF token mismatch
- Domain/cookie configuration issues

**Check:**
```bash
# Review session config
cat config/session.php

# Check .env settings
grep SESSION .env
```

**Frontend handling:**
```javascript
document.addEventListener('livewire:init', function () {
    Livewire.hook('request', ({ fail }) => {
        if (fail && fail.status === 419) {
            alert('Your session expired. Please refresh the page.');
            window.location.reload();
        }
    });
});
```

#### Livewire Component Issues
**Common problems:**
1. Missing single root element
2. Missing `wire:key` in loops
3. Public property not reactive
4. Event not dispatched correctly

**Debug checklist:**
- [ ] Single root element exists
- [ ] `wire:key` present in `@foreach` loops
- [ ] Public properties declared with `state()` or as public
- [ ] Events use `$this->dispatch()` (not `emit`)
- [ ] Listening with correct event name

**Test Livewire:**
```php
use Livewire\Volt\Volt;

test('component loads correctly', function () {
    Volt::test('feature.component')
        ->assertSee('Expected Text')
        ->assertSet('property', 'expected value')
        ->assertNoErrors();
});
```

#### Query Errors
**Syntax errors in queries:**
1. Use database-query tool to test query
2. Check for proper escaping
3. Verify column names exist
4. Check relationship names match methods

**Missing relationships:**
```php
// Check model has relationship defined
class Post extends Model {
    public function user(): BelongsTo {
        return $this->belongsTo(User::class);
    }
}
```

### 5. Performance Debugging

**Slow Pages:**
1. Check for N+1 queries (add eager loading)
2. Review complex computations (move to queued jobs)
3. Add database indexes for frequently queried columns
4. Cache expensive operations

**Queue Jobs:**
```bash
# Check failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry [id]

# Retry all failed
php artisan queue:retry all
```

### 6. Testing Strategy

Write tests to prevent regression:

```php
// Feature test
test('feature works correctly', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->post('/endpoint', ['valid' => 'data']);

    $response->assertSuccessful();
    expect(Model::count())->toBe(1);
});

// Validation test
test('validates input', function () {
    $response = $this->post('/endpoint', ['invalid' => 'data']);

    $response->assertSessionHasErrors(['field']);
});

// Authorization test
test('prevents unauthorized access', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->get('/admin/dashboard');

    $response->assertForbidden();
});
```

### 7. Systematic Approach

Use TodoWrite to track debugging steps:

```
1. Gather error information (logs, browser console)
2. Create reproduction test
3. Identify root cause
4. Implement fix
5. Verify tests pass
6. Run full test suite
```

## Output

After debugging:
1. ✅ **Explain root cause** clearly
2. ✅ **Show the fix** with file references: `[FileName.php:42](path/to/FileName.php#L42)`
3. ✅ **Add/update tests** to prevent regression
4. ✅ **Run tests** to confirm fix works
5. ✅ **Run Pint** if code was modified: `vendor/bin/pint --dirty`

## Important Reminders

- **ALWAYS** use Laravel Boost tools (`tinker`, `database-query`, `browser-logs`)
- **ALWAYS** create tests to reproduce bugs
- **ALWAYS** check recent logs (ignore old ones)
- **NEVER** debug in production without proper logging
- **NEVER** commit debugging code (`dd()`, `dump()`, `console.log()`)
- **NEVER** add dark mode support (light mode only)
- **NEVER** customize Flux UI component colors, typography, or borders (only padding/margins)
- **ASK** user to run `npm run dev` if assets aren't compiling
