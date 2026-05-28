# Security Checklist

Validate these security requirements before completing Laravel tasks.

## Mass Assignment Protection

- [ ] Use `$fillable` or `$guarded` on all Eloquent models
- [ ] Never use `$guarded = []` in production models
- [ ] Review fillable fields to ensure sensitive fields are excluded

```php
// Good
protected $fillable = ['name', 'email'];

// Good
protected $guarded = ['id', 'is_admin', 'created_at', 'updated_at'];

// Bad
protected $guarded = [];  // Allows mass assignment of all fields
```

## Input Validation

- [ ] Use Form Requests for all user input validation
- [ ] Never validate directly in controllers
- [ ] Sanitize HTML input with `strip_tags()` or use `HTMLPurifier`
- [ ] Validate file uploads (type, size, extension)

```php
// Form Request validation
public function rules(): array
{
    return [
        'email' => ['required', 'email', 'max:255'],
        'file' => ['required', 'file', 'mimes:pdf,doc', 'max:2048'],
    ];
}
```

## Authentication

- [ ] Hash passwords with `Hash::make()`, never store plain text
- [ ] Use `bcrypt` or `argon2id` for password hashing
- [ ] Implement password requirements with `Password::defaults()`
- [ ] Use Laravel Sanctum or Passport for API authentication
- [ ] Implement rate limiting on login endpoints

```php
// Hash passwords
$user->password = Hash::make($request->password);

// Verify passwords
if (Hash::check($plainPassword, $user->password)) {
    // Authenticated
}

// Password validation
'password' => ['required', Password::defaults()],
```

## Authorization

- [ ] Use policies for authorization checks
- [ ] Check authorization in Form Request `authorize()` method
- [ ] Use `@can` directives in Blade templates
- [ ] Never rely on client-side authorization alone

```php
// Policy
public function update(User $user, Post $post): bool
{
    return $user->id === $post->user_id;
}

// Form Request
public function authorize(): bool
{
    return $this->user()->can('update', $this->route('post'));
}

// Controller
$this->authorize('update', $post);
```

## CSRF Protection

- [ ] Enable CSRF protection (enabled by default)
- [ ] Use `@csrf` directive in all forms
- [ ] Include CSRF token in AJAX requests
- [ ] Add routes to `$except` array in `VerifyCsrfToken` middleware only when absolutely necessary

```html
<form method="POST" action="/users">
    @csrf
    <!-- form fields -->
</form>
```

```javascript
// AJAX with CSRF token
axios.defaults.headers.common['X-CSRF-TOKEN'] = document.querySelector('meta[name="csrf-token"]').content;
```

## SQL Injection Prevention

- [ ] Always use Eloquent or Query Builder (never raw SQL with user input)
- [ ] Use parameter binding for raw queries
- [ ] Never concatenate user input into SQL queries

```php
// Good - parameterized query
DB::select('SELECT * FROM users WHERE email = ?', [$email]);

// Good - Query Builder
User::where('email', $email)->first();

// Bad - SQL injection vulnerability
DB::select("SELECT * FROM users WHERE email = '$email'");
```

## XSS Prevention

- [ ] Use Blade's `{{ }}` syntax (auto-escapes output)
- [ ] Never use `{!! !!}` with user input
- [ ] Sanitize user input before storing in database
- [ ] Set proper Content Security Policy headers

```php
// Good - auto-escaped
{{ $user->name }}

// Dangerous - use only for trusted content
{!! $trustedHtml !!}
```

## Sensitive Data

- [ ] Use `encrypt()` for sensitive data at rest
- [ ] Store API keys and secrets in `.env` file
- [ ] Add `.env` to `.gitignore`
- [ ] Never commit sensitive data to version control
- [ ] Use `hidden` property on models to exclude sensitive fields from JSON

```php
// Encrypt sensitive data
$user->ssn = encrypt($request->ssn);

// Decrypt
$ssn = decrypt($user->ssn);

// Hide from JSON
protected $hidden = ['password', 'remember_token', 'ssn'];
```

## URL Security

- [ ] Use signed URLs for sensitive actions (password resets, email verification)
- [ ] Validate signed URLs with `hasValidSignature()`
- [ ] Set expiration time on signed URLs

```php
// Generate signed URL
$url = URL::temporarySignedRoute(
    'password.reset',
    now()->addMinutes(30),
    ['user' => $user->id]
);

// Validate
if (!$request->hasValidSignature()) {
    abort(401);
}
```

## File Upload Security

- [ ] Validate file MIME type and extension
- [ ] Limit file size
- [ ] Store uploads outside web root or use S3
- [ ] Generate random filenames to prevent overwriting
- [ ] Scan files for malware if possible

```php
public function rules(): array
{
    return [
        'avatar' => [
            'required',
            'file',
            'mimes:jpeg,png,gif',
            'max:2048',  // 2MB
        ],
    ];
}

// Store with random name
$path = $request->file('avatar')->store('avatars', 'private');
```

## Rate Limiting

- [ ] Apply rate limiting to authentication endpoints
- [ ] Protect API endpoints with throttle middleware
- [ ] Use custom rate limits for sensitive operations

```php
// In routes
Route::middleware('throttle:60,1')->group(function () {
    // 60 requests per minute
});

// Custom rate limiter
RateLimiter::for('login', function (Request $request) {
    return Limit::perMinute(5)->by($request->ip());
});
```

## Session Security

- [ ] Use secure session configuration in production
- [ ] Set `SESSION_SECURE_COOKIE=true` in production
- [ ] Set `SESSION_HTTP_ONLY=true`
- [ ] Use `SESSION_SAME_SITE=lax` or `strict`
- [ ] Regenerate session ID after login

```php
// After login
$request->session()->regenerate();

// config/session.php
'secure' => env('SESSION_SECURE_COOKIE', true),
'http_only' => true,
'same_site' => 'lax',
```

## Environment Configuration

- [ ] Set `APP_DEBUG=false` in production
- [ ] Use `APP_ENV=production`
- [ ] Set proper `APP_KEY`
- [ ] Disable directory listing
- [ ] Set proper file permissions (644 for files, 755 for directories)

## API Security

- [ ] Use API authentication (Sanctum/Passport)
- [ ] Validate Content-Type header
- [ ] Implement CORS properly
- [ ] Version your API
- [ ] Return proper HTTP status codes

```php
// CORS configuration
'paths' => ['api/*'],
'allowed_methods' => ['GET', 'POST', 'PUT', 'DELETE'],
'allowed_origins' => [config('app.frontend_url')],
'allowed_headers' => ['Content-Type', 'Authorization'],
```

## Database Security

- [ ] Use database transactions for critical operations
- [ ] Implement soft deletes for important data
- [ ] Backup database regularly
- [ ] Use separate database users with minimal privileges
- [ ] Encrypt database connection

```php
// Transaction
DB::transaction(function () use ($data) {
    $user = User::create($data);
    $profile = $user->profile()->create($profileData);
});

// Soft deletes
use Illuminate\Database\Eloquent\SoftDeletes;
use SoftDeletes;
```

## Logging and Monitoring

- [ ] Log authentication attempts
- [ ] Log authorization failures
- [ ] Monitor for suspicious activity
- [ ] Never log sensitive data (passwords, tokens, SSN)
- [ ] Set up error monitoring (Sentry, Bugsnag)

```php
// Log without sensitive data
Log::info('User login attempt', [
    'email' => $request->email,
    'ip' => $request->ip(),
]);
```
