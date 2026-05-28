---
name: code-reviewer
description: Reviews PHP/CakePHP code for quality, standards compliance, and best practices
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Architecture Constraints ==="
          yq -o=json '.constraints.architecture' .claude/config.yaml 2>/dev/null || true
          echo "=== All Constraints ==="
          yq -o=json '.constraints' .claude/config.yaml 2>/dev/null || true
        fi
---

# PHP/CakePHP Code Reviewer

A specialized skill for reviewing PHP/CakePHP code to ensure quality, maintainability, and adherence to standards.

## Core Responsibilities

### 1. Code Quality Metrics

**Complexity Analysis:**
```php
/**
 * Cyclomatic Complexity Check
 *
 * Good: <= 10
 * Acceptable: 11-20
 * Needs refactoring: > 20
 */
public function analyzeComplexity($method)
{
    // Count:
    // - if statements
    // - case statements
    // - for/foreach/while loops
    // - catch blocks
    // - && and || operators
    // - ?: operators
}
```

**Method Length Check:**
```php
/**
 * Method Length Guidelines
 *
 * Ideal: <= 20 lines
 * Acceptable: 21-50 lines
 * Too long: > 50 lines
 */
```

**Class Cohesion:**
```php
/**
 * Single Responsibility Principle
 *
 * Each class should have one reason to change
 * Methods should be related to class purpose
 */
```

### 2. PHP Standards Review

**PSR-12 Compliance:**
```php
// ✅ CORRECT: PSR-12 formatting
<?php

declare(strict_types=1);

namespace App\Controller\User;

use Cake\Controller\Controller;
use Cake\Http\Response;

class UsersController extends Controller
{
    public function index(): ?Response
    {
        // 4 spaces indentation
        if ($condition) {
            $this->doSomething();
        }

        return null;
    }
}

// ❌ WRONG: Non-standard formatting
<?php
namespace App\Controller\User;
use Cake\Controller\Controller;

class UsersController extends Controller {
    public function index(){
        if($condition){
            $this->doSomething();
        }
    }
}
```

**Type Declarations:**
```php
// ✅ CORRECT: Strict types with declarations
declare(strict_types=1);

public function processData(array $data, int $limit): bool
{
    return true;
}

// ❌ WRONG: Missing type declarations
public function processData($data, $limit)
{
    return true;
}
```

### 3. CakePHP Convention Review

**Naming Conventions:**
```php
// ✅ CORRECT CakePHP naming
class UsersTable extends Table         // Plural for tables
class User extends Entity              // Singular for entities
class UsersController extends Controller  // Plural for controllers

// Model associations
$this->belongsTo('Company', [         // Singular for belongsTo
    'className' => 'Companys',
]);
$this->hasMany('Orders');             // Plural for hasMany

// ❌ WRONG naming
class UserTable extends Table         // Should be plural
$this->belongsTo('Companies');       // Should be singular alias
```

**MVC Separation:**
```php
// ✅ CORRECT: Thin controller, fat model
// Controller
public function approve($id)
{
    $application = $this->Applications->get($id);
    $result = $this->Applications->approve($application);

    if ($result) {
        $this->Flash->success(__('承認しました'));
    }
}

// Model
public function approve($application): bool
{
    // Complex business logic here
    $application->status = Configure::read('Application.Status.approved');
    // More logic...
    return $this->save($application);
}

// ❌ WRONG: Business logic in controller
public function approve($id)
{
    $application = $this->Applications->get($id);

    // Business logic should be in model
    $application->status = 3;
    $application->approved_date = date('Y-m-d');
    // Calculate approval logic...
    // Send notifications...

    $this->Applications->save($application);
}
```

### 4. Security Review

**SQL Injection Prevention:**
```php
// ✅ CORRECT: Using ORM query builder
$users = $this->Users->find()
    ->where(['email' => $userInput])
    ->all();

// ❌ WRONG: Raw SQL with concatenation
$query = "SELECT * FROM users WHERE email = '" . $userInput . "'";
```

**XSS Prevention:**
```php
// ✅ CORRECT: Escaping output in views
<?= h($userInput) ?>
<?= $this->Text->autoParagraph(h($content)) ?>

// ❌ WRONG: Unescaped output
<?= $userInput ?>
<?php echo $content; ?>
```

**Authentication & Authorization:**
```php
// ✅ CORRECT: Proper auth check
public function beforeFilter(EventInterface $event)
{
    parent::beforeFilter($event);

    if (!$this->Auth->user()) {
        throw new UnauthorizedException('ログインが必要です');
    }

    if (!$this->isAuthorized()) {
        throw new ForbiddenException('権限がありません');
    }
}

// ❌ WRONG: No auth check or weak implementation
public function delete($id)
{
    // Missing auth check
    $this->Model->delete($id);
}
```

**Password Handling:**
```php
// ✅ CORRECT: Using password hasher
use Cake\Auth\DefaultPasswordHasher;

$hasher = new DefaultPasswordHasher();
$hashed = $hasher->hash($password);

// ❌ WRONG: Plain text or weak hashing
$password = md5($password);  // Weak
$password = $plainText;       // Never store plain text
```

### 5. Performance Review

**N+1 Query Problem:**
```php
// ✅ CORRECT: Eager loading with contain
$users = $this->Users->find()
    ->contain(['Orders', 'Company'])
    ->all();

// ❌ WRONG: Lazy loading causes N+1
$users = $this->Users->find()->all();
foreach ($users as $user) {
    $orders = $user->orders; // Additional query per user
}
```

**Caching Strategy:**
```php
// ✅ CORRECT: Using cache for expensive operations
public function getExpensiveData()
{
    return Cache::remember('expensive_data', function () {
        return $this->calculateExpensiveOperation();
    }, 'long_term');
}

// ❌ WRONG: No caching for repeated expensive operations
public function getExpensiveData()
{
    return $this->calculateExpensiveOperation(); // Recalculated every time
}
```

**Database Optimization:**
```php
// ✅ CORRECT: Optimized query
$results = $this->Model->find()
    ->select(['id', 'name', 'status']) // Select only needed fields
    ->where(['status' => 1])
    ->order(['created' => 'DESC'])
    ->limit(100)
    ->all();

// ❌ WRONG: Inefficient query
$results = $this->Model->find('all'); // Loads everything
```

### 6. Error Handling Review

**Exception Handling:**
```php
// ✅ CORRECT: Proper exception handling
try {
    $result = $this->performOperation();

    if (!$result) {
        throw new \RuntimeException('Operation failed');
    }

    return $result;

} catch (RecordNotFoundException $e) {
    Log::warning('Record not found: ' . $e->getMessage());
    throw new NotFoundException('データが見つかりません');

} catch (\Exception $e) {
    Log::error('Unexpected error: ' . $e->getMessage());
    throw new InternalErrorException('システムエラーが発生しました');
}

// ❌ WRONG: Generic or no error handling
try {
    $this->performOperation();
} catch (\Exception $e) {
    // Too generic, no logging
    return false;
}
```

**Validation Errors:**
```php
// ✅ CORRECT: Proper validation error handling
$entity = $this->Model->patchEntity($entity, $data);

if ($this->Model->save($entity)) {
    $this->Flash->success(__('保存しました'));
} else {
    $errors = $entity->getErrors();
    foreach ($errors as $field => $fieldErrors) {
        foreach ($fieldErrors as $error) {
            $this->Flash->error($error);
        }
    }
}

// ❌ WRONG: Ignoring validation errors
$this->Model->save($entity); // No error check
```

### 7. Testing Considerations

**Testability Review:**
```php
// ✅ CORRECT: Testable code with dependency injection
class OrderService
{
    private $Orders;
    private $Mailer;

    public function __construct(OrdersTable $orders, MailerInterface $mailer)
    {
        $this->Orders = $orders;
        $this->Mailer = $mailer;
    }
}

// ❌ WRONG: Hard dependencies, difficult to test
class OrderService
{
    public function processOrder()
    {
        $Orders = TableRegistry::get('Orders'); // Hard to mock
        $mailer = new Mailer();                 // Hard to mock
    }
}
```

**Test Coverage Indicators:**
```php
// Methods that MUST have tests:
// - Public methods with business logic
// - Data validation methods
// - Security-critical methods
// - Methods with complex conditions

// Methods that MAY skip tests:
// - Simple getters/setters
// - Framework override methods with no custom logic
```

### 8. Documentation Review

**PHPDoc Standards:**
```php
// ✅ CORRECT: Complete PHPDoc
/**
 * Process order and send confirmation
 *
 * @param int $orderId Order ID to process
 * @param array $options Processing options
 * @return bool True on success
 * @throws \InvalidArgumentException When order ID is invalid
 * @throws \RuntimeException When processing fails
 */
public function processOrder(int $orderId, array $options = []): bool
{
    // Implementation
}

// ❌ WRONG: Missing or incomplete PHPDoc
// No documentation
public function processOrder($orderId, $options = [])
{
    // Implementation
}
```

## Review Checklist

### Code Structure
- [ ] Single Responsibility Principle followed
- [ ] DRY (Don't Repeat Yourself) principle applied
- [ ] Methods are concise (< 50 lines)
- [ ] Cyclomatic complexity is acceptable (< 20)
- [ ] Proper abstraction levels

### PHP Standards
- [ ] PSR-12 coding style
- [ ] Strict types declared
- [ ] Type hints for parameters and returns
- [ ] Proper namespace usage
- [ ] No deprecated functions

### CakePHP Conventions
- [ ] Naming conventions followed
- [ ] MVC separation maintained
- [ ] ORM used properly
- [ ] Configure::read() for configs
- [ ] Proper use of components and helpers

### Security
- [ ] No SQL injection vulnerabilities
- [ ] XSS prevention in place
- [ ] Authentication checks
- [ ] Authorization checks
- [ ] Proper password handling
- [ ] CSRF protection

### Performance
- [ ] No N+1 query problems
- [ ] Proper use of eager loading
- [ ] Caching where appropriate
- [ ] Optimized database queries
- [ ] No unnecessary loops

### Error Handling
- [ ] Proper exception handling
- [ ] Appropriate error messages
- [ ] Logging of errors
- [ ] Validation error handling

### Testing
- [ ] Code is testable
- [ ] No hard dependencies
- [ ] Mock-friendly design

### Documentation
- [ ] PHPDoc for all public methods
- [ ] Complex logic commented
- [ ] README updated if needed

## Review Output Format

```markdown
## Code Review: [File/Feature Name]

### Summary
- **Overall Quality**: Excellent/Good/Needs Improvement/Poor
- **Risk Level**: Low/Medium/High
- **Recommendation**: Approve/Approve with changes/Needs rework

### Strengths
- Well-structured MVC separation
- Good error handling
- Follows CakePHP conventions

### Issues Found

#### Critical (Must Fix)
1. **SQL Injection Risk** (Line 45)
   - Current: Raw SQL concatenation
   - Solution: Use ORM query builder
   ```php
   // Replace this
   $query = "SELECT * FROM users WHERE id = " . $id;

   // With this
   $user = $this->Users->get($id);
   ```

#### Major (Should Fix)
1. **N+1 Query Problem** (Line 78)
   - Current: Lazy loading in loop
   - Solution: Add eager loading

#### Minor (Consider Fixing)
1. **Missing PHPDoc** (Line 120)
   - Add documentation for public method

### Metrics
- Cyclomatic Complexity: 15 (Acceptable)
- Method Length: Max 45 lines (Good)
- Test Coverage Required: 85%

### Action Items
- [ ] Fix SQL injection vulnerability
- [ ] Add eager loading for associations
- [ ] Add missing PHPDoc comments
```

## Best Practices

1. **Be Constructive**: Provide solutions, not just problems
2. **Prioritize Issues**: Focus on critical/security issues first
3. **Consider Context**: Understand requirements and constraints
4. **Educate**: Explain why something is an issue
5. **Be Specific**: Reference line numbers and provide examples
6. **Stay Objective**: Focus on code, not person

Remember: Good code review improves code quality and helps team members learn and grow.