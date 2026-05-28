---
name: php-cakephp-application-developer
description: Use this skill when you need to design functional specifications and implement production code for PHP/CakePHP applications.
---

# Skill body

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

### 2. API Design Specification

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

### 3. Implementation Standards

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

### 4. Controller Implementation

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
 * @property \App\Controller\Component\MessageDeliveryDbAccessorComponent $MessageDeliveryDbAccessor
 */
class UsersController extends AppController
{
    /**
     * Initialize method
     */
    public function initialize(): void
    {
        parent::initialize();
        $this->loadComponent('MessageDeliveryDbAccessor');
    }

    /**
     * Index method - List users
     *
     * @return \Cake\Http\Response|null|void
     */
    public function index()
    {
        // Get company-specific connection
        $companyId = $this->Auth->user('eco_company_id');
        $conn = $this->MessageDeliveryDbAccessor
            ->getUserMessageDeliveryDbConnection($companyId);

        $this->Users->setConnection($conn);

        // Paginate with conditions
        $query = $this->Users->find()
            ->where(['del_flg' => Configure::read('Common.del_flg.off')])
            ->order(['created' => 'DESC']);

        $users = $this->paginate($query);
        $this->set(compact('users'));
    }
}
```

### 5. Data Flow Design

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

**Data Transformation:**
```php
Input Data → Validation → Business Logic → Entity → Output Format
```

### 6. Design Document Template

```markdown
# Functional Design: [Feature Name]

## 1. Overview
### Purpose
[Brief description of what this feature does]

### Scope
- In Scope: [what's included]
- Out of Scope: [what's not included]
```