# Laravel Refactoring Patterns

## Common Anti-Patterns and Their Solutions

### 1. Fat Controllers

**Problem:**
```php
// Bad: Business logic in controller
public function store(Request $request)
{
    $validated = $request->validate([...]);
    
    $user = User::create($validated);
    
    Mail::to($user->email)->send(new WelcomeEmail($user));
    
    event(new UserRegistered($user));
    
    Log::info('User registered', ['user_id' => $user->id]);
    
    return redirect()->route('dashboard');
}
```

**Solution: Service Classes or Actions**
```php
// Good: Delegate to service/action
public function store(Request $request, RegisterUserAction $action)
{
    $user = $action->execute($request->validated());
    
    return redirect()->route('dashboard');
}

// RegisterUserAction.php
class RegisterUserAction
{
    public function execute(array $data): User
    {
        $user = User::create($data);
        
        Mail::to($user->email)->queue(new WelcomeEmail($user));
        event(new UserRegistered($user));
        
        return $user;
    }
}
```

### 2. N+1 Query Problems

**Problem:**
```php
// Bad: N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // Triggers query for each post
}
```

**Solution: Eager Loading**
```php
// Good: Eager load relationships
$posts = Post::with('user')->get();
foreach ($posts as $post) {
    echo $post->user->name; // Uses loaded data
}

// Better: Add eager loading to model
class Post extends Model
{
    protected $with = ['user']; // Auto-eager load
}
```

### 3. Missing Type Hints and Return Types

**Problem:**
```php
// Bad: No type hints
public function getUserOrders($userId)
{
    return Order::where('user_id', $userId)->get();
}
```

**Solution: Strict Types**
```php
// Good: Type hints and return types
public function getUserOrders(int $userId): Collection
{
    return Order::where('user_id', $userId)->get();
}
```

### 4. Direct Eloquent Queries in Controllers

**Problem:**
```php
// Bad: Repository pattern violation
public function index()
{
    $activeUsers = User::where('status', 'active')
        ->with('profile')
        ->latest()
        ->paginate(20);
        
    return view('users.index', compact('activeUsers'));
}
```

**Solution: Repository Pattern**
```php
// Good: Use repository
public function index(UserRepository $users)
{
    $activeUsers = $users->getActivePaginated(20);
    
    return view('users.index', compact('activeUsers'));
}

// UserRepository.php
class UserRepository
{
    public function getActivePaginated(int $perPage = 20): LengthAwarePaginator
    {
        return User::query()
            ->where('status', 'active')
            ->with('profile')
            ->latest()
            ->paginate($perPage);
    }
}
```

### 5. Magic Numbers and Strings

**Problem:**
```php
// Bad: Magic values
if ($user->role === 'admin') {
    // ...
}

if ($order->status === 2) {
    // ...
}
```

**Solution: Constants/Enums**
```php
// Good: Use enums (PHP 8.1+)
enum UserRole: string
{
    case ADMIN = 'admin';
    case USER = 'user';
    case GUEST = 'guest';
}

enum OrderStatus: int
{
    case PENDING = 1;
    case PROCESSING = 2;
    case COMPLETED = 3;
}

if ($user->role === UserRole::ADMIN->value) {
    // ...
}
```

### 6. Poor Validation Organization

**Problem:**
```php
// Bad: Inline validation
public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
        // 20+ more fields...
    ]);
}
```

**Solution: Form Requests**
```php
// Good: Form Request class
public function store(StoreUserRequest $request)
{
    $validated = $request->validated();
    // ...
}

// StoreUserRequest.php
class StoreUserRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', Rule::unique('users')],
            'password' => ['required', 'min:8', 'confirmed'],
        ];
    }
    
    public function messages(): array
    {
        return [
            'email.unique' => 'This email is already registered.',
        ];
    }
}
```

### 7. Mass Assignment Vulnerabilities

**Problem:**
```php
// Bad: Unprotected mass assignment
User::create($request->all());
```

**Solution: Fillable/Guarded Properties**
```php
// Good: Define fillable
class User extends Model
{
    protected $fillable = [
        'name',
        'email',
        'password',
    ];
    
    // Or use guarded for everything except:
    protected $guarded = [
        'id',
        'is_admin',
        'email_verified_at',
    ];
}

User::create($request->validated());
```

### 8. Poor Exception Handling

**Problem:**
```php
// Bad: Generic catch
try {
    $payment = $gateway->charge($amount);
} catch (\Exception $e) {
    return back()->with('error', 'Something went wrong');
}
```

**Solution: Specific Exception Handling**
```php
// Good: Specific exceptions
try {
    $payment = $gateway->charge($amount);
} catch (InsufficientFundsException $e) {
    return back()->with('error', 'Insufficient funds');
} catch (PaymentGatewayException $e) {
    Log::error('Payment failed', ['exception' => $e]);
    return back()->with('error', 'Payment processing failed');
} catch (\Exception $e) {
    report($e);
    return back()->with('error', 'An unexpected error occurred');
}
```

### 9. Database Transactions Missing

**Problem:**
```php
// Bad: No transaction for multi-step operations
public function transferFunds(User $from, User $to, float $amount)
{
    $from->decrement('balance', $amount);
    $to->increment('balance', $amount);
    
    Transaction::create([
        'from_user_id' => $from->id,
        'to_user_id' => $to->id,
        'amount' => $amount,
    ]);
}
```

**Solution: Use Database Transactions**
```php
// Good: Wrap in transaction
public function transferFunds(User $from, User $to, float $amount): Transaction
{
    return DB::transaction(function () use ($from, $to, $amount) {
        $from->decrement('balance', $amount);
        $to->increment('balance', $amount);
        
        return Transaction::create([
            'from_user_id' => $from->id,
            'to_user_id' => $to->id,
            'amount' => $amount,
        ]);
    });
}
```

### 10. Unnecessary Queries in Loops

**Problem:**
```php
// Bad: Query in loop
foreach ($userIds as $userId) {
    $user = User::find($userId);
    $results[] = $user->processData();
}
```

**Solution: Batch Operations**
```php
// Good: Single query
$users = User::whereIn('id', $userIds)->get();
foreach ($users as $user) {
    $results[] = $user->processData();
}

// Better: Collection operations
$results = User::whereIn('id', $userIds)
    ->get()
    ->map(fn($user) => $user->processData());
```

## Modern Laravel Features to Adopt

### Route Model Binding
```php
// Old
public function show($id)
{
    $post = Post::findOrFail($id);
    return view('posts.show', compact('post'));
}

// New: Automatic model binding
public function show(Post $post)
{
    return view('posts.show', compact('post'));
}
```

### Invokable Controllers
```php
// Old: Single action controller with invoke
class ShowProfileController extends Controller
{
    public function __invoke(User $user)
    {
        return view('profile', compact('user'));
    }
}

// Route
Route::get('/profile/{user}', ShowProfileController::class);
```

### Attribute-Based Routing (Laravel 11+)
```php
use Illuminate\Support\Facades\Route;

#[Route('/posts', name: 'posts.')]
class PostController extends Controller
{
    #[Route('/', name: 'index', methods: ['GET'])]
    public function index() { }
    
    #[Route('/{post}', name: 'show', methods: ['GET'])]
    public function show(Post $post) { }
}
```

### Pipeline Pattern
```php
// Old: Nested conditionals
$data = $request->all();
if ($request->has('trim')) {
    $data = array_map('trim', $data);
}
if ($request->has('uppercase')) {
    $data = array_map('strtoupper', $data);
}

// New: Pipeline
$data = app(Pipeline::class)
    ->send($request->all())
    ->through([
        TrimStrings::class,
        UppercaseStrings::class,
    ])
    ->thenReturn();
```

## Query Optimization Patterns

### Chunking Large Datasets
```php
// Bad: Load everything into memory
User::where('active', true)->get()->each(function ($user) {
    $this->sendNotification($user);
});

// Good: Process in chunks
User::where('active', true)->chunk(100, function ($users) {
    foreach ($users as $user) {
        $this->sendNotification($user);
    }
});

// Better: Lazy loading
User::where('active', true)->lazy()->each(function ($user) {
    $this->sendNotification($user);
});
```

### Efficient Counting
```php
// Bad: Loading all records to count
$count = Post::where('published', true)->get()->count();

// Good: Database count
$count = Post::where('published', true)->count();

// Even better: exists() for boolean checks
$hasPublished = Post::where('published', true)->exists();
```

### Select Only Needed Columns
```php
// Bad: Select all columns
$users = User::all();

// Good: Select specific columns
$users = User::select(['id', 'name', 'email'])->get();

// For relationships
$posts = Post::with(['user:id,name'])->get();
```
