---
name: php-cakephp-development
description: Use this skill when designing functional architecture and implementing production code for PHP/CakePHP applications based on detailed specifications.
---

# PHP/CakePHP Development

A comprehensive skill for designing functional architecture and implementing production-ready code for PHP/CakePHP applications.

## Core Responsibilities

### 1. Functional Architecture Design

**Component Mapping:**
```yaml
Functional Component Design:
  Controllers:
    - name: [Controller]Controller
    - actions: [list of actions]
    - authentication: required|optional
    - authorization: role-based permissions

  Models:
    - Tables: [list of Table classes]
    - Entities: [list of Entity classes]
    - Associations: [relationships]
    - Validation: [rules]

  Views:
    - Templates: [list of .php files]
    - Elements: [reusable components]
    - Layouts: [page structures]

  Components:
    - Custom components needed
    - Third-party integrations
```

### 2. Implementation Standards

**CakePHP Conventions:**
```php
// Controller naming
class UsersController extends AppController

// Model naming
class UsersTable extends Table
class User extends Entity

// Component naming
class AuthorizationComponent extends Component

// View template naming
// templates/User/Users/index.php
// templates/User/Users/view.php
```

### 3. Controller Implementation

**Standard Controller Pattern:**
```php
<?php
declare(strict_types=1);

namespace App\Controller\User;

use App\Controller\AppController;
use Cake\Event\EventInterface;
use Cake\Http\Response;

/**
 * Users Controller
 *
 * @property \App\Model\Table\UsersTable $Users
 */
class UsersController extends AppController
{
    public function initialize(): void
    {
        parent::initialize();
        $this->loadComponent('MessageDeliveryDbAccessor');
    }

    public function index()
    {
        // Get company-specific connection
        $companyId = $this->Auth->user('eco_company_id');
        $conn = $this->MessageDeliveryDbAccessor->getUserMessageDeliveryDbConnection($companyId);
        $this->Users->setConnection($conn);

        // Paginate with conditions
        $query = $this->Users->find()->where(['del_flg' => Configure::read('Common.del_flg.off')])->order(['created' => 'DESC']);
        $users = $this->paginate($query);
        $this->set(compact('users'));
    }
}
```

### 4. Model Implementation

**Table Class Pattern:**
```php
<?php
declare(strict_types=1);

namespace App\Model\Table;

use Cake\ORM\Table;
use Cake\Validation\Validator;
use Cake\ORM\RulesChecker;

/**
 * Users Model
 */
class UsersTable extends Table
{
    public function initialize(array $config): void
    {
        parent::initialize($config);
        $this->setTable('users');
        $this->setDisplayField('name');
        $this->setPrimaryKey('id');
        $this->addBehavior('Timestamp');
        $this->belongsTo('Companys', ['foreignKey' => 'company_id', 'joinType' => 'INNER']);
        $this->hasMany('Orders', ['foreignKey' => 'user_id', 'dependent' => true]);
    }

    public function validationDefault(Validator $validator): Validator
    {
        $validator->integer('id')->allowEmptyString('id', null, 'create');
        $validator->email('email')->requirePresence('email', 'create')->notEmptyString('email');
        $validator->scalar('name')->maxLength('name', 255)->requirePresence('name', 'create')->notEmptyString('name');
        return $validator;
    }
}
```

### 5. API Design Specification

**RESTful Endpoint Design:**
```yaml
API Endpoint:
  method: GET|POST|PUT|DELETE
  path: /api/v1/[resource]
  authentication: required|optional

  request:
    headers:
      Content-Type: application/json
      Authorization: Bearer [token]
    body:
      field1: type
      field2: type

  response:
    success:
      status: 200
      body: {data: [...]}
    error:
      status: 400|401|404|500
      body: {error: "message"}
```

### 6. Data Flow Design

**Request Lifecycle:**
```
1. Route → Controller
2. Controller → Authorization Check
3. Controller → Validation
4. Controller → Model/Service
5. Model → Database
6. Model → Entity
7. Controller → View/JSON Response
```

### 7. Error Handling
```php
try {
    // Operation
    $result = $this->performOperation();
    if (!$result) {
        throw new \RuntimeException('Operation failed');
    }
} catch (\Exception $e) {
    Log::error('Operation error: ' . $e->getMessage());
    $this->Flash->error(__('エラーが発生しました'));
    return $this->redirect(['action' => 'index']);
}
```

### 8. Transaction Management
```php
$connection = $this->Model->getConnection();
try {
    $connection->begin();
    // Multiple operations
    $this->Model1->save($entity1);
    $this->Model2->save($entity2);
    $connection->commit();
} catch (\Exception $e) {
    $connection->rollback();
    throw $e;
}
```

## Code Quality Standards

### PHP Standards
```php
// Use strict types
declare(strict_types=1);

// Type hints for parameters and returns
public function processData(array $data): bool

// Use null coalescing operator
$value = $data['key'] ?? 'default';
```

### CakePHP Best Practices
1. **Use Configure::read()** for configuration values
2. **Use TableRegistry** for getting table instances
3. **Use ConnectionManager** for database connections
4. **Use Log::write()** for logging
5. **Use Flash messages** for user feedback

## Output Examples

### Example 1: User Registration Implementation
```php
// Controller action
public function register()
{
    $user = $this->Users->newEmptyEntity();
    if ($this->request->is('post')) {
        $user = $this->Users->patchEntity($user, $this->request->getData());
        if ($this->Users->save($user)) {
            $this->Flash->success(__('登録が完了しました'));
            return $this->redirect(['action' => 'login']);
        }
        $this->Flash->error(__('登録に失敗しました'));
    }
    $this->set(compact('user'));
}
```

### Example 2: Order Processing Implementation
```php
// Service method
public function createOrder(array $orderData): Order
{
    $connection = $this->Orders->getConnection();
    try {
        $connection->begin();
        // Create order
        $order = $this->Orders->newEntity($orderData);
        $this->Orders->saveOrFail($order);
        // Create order items
        foreach ($orderData['items'] as $itemData) {
            $item = $this->OrderItems->newEntity($itemData);
            $item->order_id = $order->id;
            $this->OrderItems->saveOrFail($item);
        }
        $connection->commit();
        return $order;
    } catch (\Exception $e) {
        $connection->rollback();
        throw new \RuntimeException('Order creation failed: ' . $e->getMessage());
    }
}
```

## Best Practices

1. **Follow MVC Pattern**: Keep controllers thin, models fat
2. **Use Services**: Complex business logic in service classes
3. **Type Safety**: Use strict types and type hints
4. **Error Handling**: Proper try-catch blocks
5. **Logging**: Log errors and important events

Remember: Good implementation follows design specifications while maintaining code quality and framework conventions.