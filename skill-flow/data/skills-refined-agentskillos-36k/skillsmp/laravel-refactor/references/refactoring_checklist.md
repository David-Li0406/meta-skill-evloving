# Laravel/Livewire Refactoring Checklist

## Pre-Refactoring Assessment

### 1. Understand Current Codebase

- [ ] Review existing functionality and business logic
- [ ] Identify dependencies and relationships
- [ ] Document current behavior with tests if missing
- [ ] Identify pain points and technical debt areas

### 2. Set Refactoring Goals

- [ ] Define specific improvements (performance, maintainability, security)
- [ ] Prioritize refactoring tasks (high-impact vs. quick wins)
- [ ] Establish success metrics
- [ ] Consider backward compatibility requirements

### 3. Prepare Safety Net

- [ ] Ensure comprehensive test coverage exists
- [ ] Create backup/branch for rollback
- [ ] Set up local development environment
- [ ] Review deployment process

## Refactoring Workflow

### Phase 1: Analysis

1. **Run automated analysis**

   ```bash
   python3 scripts/analyze_code.py app/Http/Controllers
   python3 scripts/analyze_code.py app/Http/Livewire
   ```

2. **Manual code review**
   - [ ] Review controller methods (should be < 20 lines)
   - [ ] Check for N+1 queries (use Laravel Debugbar/Telescope)
   - [ ] Identify duplicated code
   - [ ] Review security concerns (mass assignment, SQL injection)

3. **Document findings**
   - [ ] List all identified issues by priority
   - [ ] Note breaking change risks
   - [ ] Estimate refactoring effort

### Phase 2: Structure Refactoring

#### Controllers

- [ ] Extract business logic to Actions/Services

  ```php
  // Before: Fat controller
  public function store(Request $request) {
      // 50 lines of logic
  }

  // After: Delegated to action
  public function store(StoreRequest $request, CreatePostAction $action) {
      return $action->execute($request->validated());
  }
  ```

- [ ] Move validation to Form Requests
- [ ] Implement route model binding
- [ ] Add type hints and return types
- [ ] Keep controllers thin (< 20 lines per method)

#### Models

- [ ] Add proper $fillable/$guarded properties
- [ ] Define relationships clearly
- [ ] Extract complex queries to scopes
- [ ] Add type hints to properties (PHP 8.1+)
- [ ] Consider using enums for status fields

#### Services/Actions

- [ ] Extract complex business logic
- [ ] Make single-responsibility classes
- [ ] Add comprehensive type hints
- [ ] Implement proper error handling
- [ ] Write unit tests for business logic

### Phase 3: Database Optimization

#### Query Optimization

- [ ] Add eager loading to prevent N+1

  ```php
  // Before
  $posts = Post::all();

  // After
  $posts = Post::with(['user', 'comments'])->get();
  ```

- [ ] Use select() to limit columns
- [ ] Replace count() queries with exists() for boolean checks
- [ ] Use chunk() or lazy() for large datasets
- [ ] Add database indexes for frequent queries

#### Relationships

- [ ] Optimize relationship queries
- [ ] Add composite keys where appropriate
- [ ] Review polymorphic relationships
- [ ] Consider eager loading defaults in models

### Phase 4: Livewire Refactoring

#### Component Structure

- [ ] Extract business logic to actions
- [ ] Use Form Objects (Livewire 3)
- [ ] Implement computed properties with #[Computed]
- [ ] Add loading states and skeleton screens
- [ ] Implement progressive/lazy loading

#### Performance

- [ ] Use wire:model.lazy for non-critical fields
- [ ] Add debouncing to search inputs
- [ ] Implement pagination for lists
- [ ] Use events for component communication
- [ ] Avoid deep component nesting

#### Security

- [ ] Bind specific properties, not entire models
- [ ] Validate all public properties
- [ ] Implement authorization checks
- [ ] Use Form Requests for validation

### Phase 5: Security & Best Practices

#### Security Checklist

- [ ] Replace $request->all() with validated()
- [ ] Add CSRF protection
- [ ] Implement authorization policies
- [ ] Review SQL injection vulnerabilities
- [ ] Check XSS vulnerabilities in blade templates
- [ ] Validate file uploads properly
- [ ] Use encrypted database fields where needed

#### Error Handling

- [ ] Add try-catch blocks for critical operations
- [ ] Use specific exception types
- [ ] Implement proper logging
- [ ] Return user-friendly error messages
- [ ] Add error reporting (Sentry, Bugsnag, etc.)

#### Code Quality

- [ ] Remove commented-out code
- [ ] Remove unused imports and variables
- [ ] Add PHPDoc blocks for complex methods
- [ ] Follow PSR-12 coding standards
- [ ] Run PHP CS Fixer or Laravel Pint

### Phase 6: Modern Laravel Features

#### Adopt New Patterns

- [ ] Convert to invokable controllers where appropriate
- [ ] Use pipeline pattern for complex workflows
- [ ] Implement repository pattern if needed
- [ ] Use events and listeners for side effects
- [ ] Consider using DTOs for complex data transfer

#### Upgrade Syntax

- [ ] Use short array syntax []
- [ ] Use null coalescing operator ??
- [ ] Use arrow functions for callbacks
- [ ] Use match() instead of switch where appropriate
- [ ] Leverage named arguments (PHP 8.0+)

### Phase 7: Testing

#### Test Coverage

- [ ] Write/update unit tests for business logic
- [ ] Add feature tests for critical paths
- [ ] Test Livewire components
- [ ] Add integration tests for APIs
- [ ] Verify edge cases and error scenarios

#### Test Quality

- [ ] Follow AAA pattern (Arrange, Act, Assert)
- [ ] Use factories for test data
- [ ] Mock external services
- [ ] Test validation rules
- [ ] Test authorization policies

### Phase 8: Documentation

#### Code Documentation

- [ ] Add PHPDoc blocks for public methods
- [ ] Document complex algorithms
- [ ] Add inline comments for non-obvious code
- [ ] Update README if architecture changed

#### Architecture Documentation

- [ ] Document service/action responsibilities
- [ ] Update API documentation
- [ ] Document database schema changes
- [ ] Create/update architecture diagrams

## Post-Refactoring Checklist

### Testing & Validation

- [ ] Run full test suite
- [ ] Manual testing of critical features
- [ ] Performance testing (before/after metrics)
- [ ] Code review with team
- [ ] Security audit

### Deployment

- [ ] Update dependencies
- [ ] Clear all caches
- [ ] Run database migrations
- [ ] Deploy to staging first
- [ ] Monitor error logs
- [ ] Verify production deployment

### Monitoring

- [ ] Set up application monitoring
- [ ] Review performance metrics
- [ ] Monitor error rates
- [ ] Check user feedback
- [ ] Track database query performance

## Common Refactoring Patterns

### Extract Method

When a method is too long:

```php
// Before
public function process() {
    // 100 lines of code
}

// After
public function process() {
    $data = $this->prepareData();
    $result = $this->performCalculation($data);
    return $this->formatResult($result);
}
```

### Extract Class

When a class has too many responsibilities:

```php
// Before: User class handles authentication, profile, and notifications
class User {
    public function login() { }
    public function updateProfile() { }
    public function sendNotification() { }
}

// After: Separated concerns
class User { }
class UserAuthenticator { }
class UserProfileManager { }
class UserNotificationService { }
```

### Replace Conditional with Polymorphism

When you have type-based conditionals:

```php
// Before
public function getDiscount($userType) {
    if ($userType === 'premium') {
        return 0.20;
    } elseif ($userType === 'regular') {
        return 0.10;
    }
    return 0;
}

// After: Use strategy pattern
interface DiscountStrategy {
    public function calculate(): float;
}

class PremiumDiscount implements DiscountStrategy {
    public function calculate(): float { return 0.20; }
}
```

### Introduce Parameter Object

When methods have many parameters:

```php
// Before
public function createOrder($userId, $productId, $quantity, $price, $discount, $shippingAddress)

// After
public function createOrder(OrderData $orderData)
```

## Performance Metrics to Track

### Before/After Comparison

- Query count per request
- Page load time
- Memory usage
- Database query time
- API response time
- Cache hit rate

### Tools to Use

- Laravel Debugbar (query analysis)
- Laravel Telescope (application insights)
- Blackfire.io (performance profiling)
- New Relic (production monitoring)
