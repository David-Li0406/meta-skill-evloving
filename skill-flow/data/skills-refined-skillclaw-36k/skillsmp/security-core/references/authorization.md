# Authorization Patterns

Comprehensive guide to implementing authorization including RBAC, ABAC, and Row Level Security (RLS) across different platforms.

## Table of Contents

1. [Authorization Strategies](#authorization-strategies)
2. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
3. [Attribute-Based Access Control (ABAC)](#attribute-based-access-control-abac)
4. [Row Level Security (RLS)](#row-level-security-rls)
5. [Permission Checking Patterns](#permission-checking-patterns)
6. [Implementation Examples](#implementation-examples)

## Authorization Strategies

### Choosing an Authorization Model

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| RBAC | Simple hierarchies, standard roles | Easy to understand, easy to implement | Can become complex with many roles |
| ABAC | Complex policies, dynamic rules | Flexible, fine-grained control | More complex to implement |
| RLS | Multi-tenant apps, data isolation | Database-enforced, performant | Database-specific, harder to debug |
| Permission-based | Granular actions | Very flexible | Can require many permissions |

### When to Use Each Model

**Use RBAC when:**
- You have clear role hierarchies (Admin, Manager, User)
- Permissions are relatively static
- Users have one or few roles
- Simple permission checks

**Use ABAC when:**
- Permissions depend on context (time, location, resource state)
- Complex policy requirements
- Dynamic permission calculation needed
- Multiple attributes determine access

**Use RLS when:**
- Multi-tenant applications with data isolation requirements
- Users should only see their own data
- Performance is critical (database-level filtering)
- Using Supabase, PostgreSQL, or similar databases

## Role-Based Access Control (RBAC)

### Simple RBAC Implementation

#### TypeScript

```typescript
enum Role {
  Admin = 'admin',
  Manager = 'manager',
  User = 'user',
}

interface User {
  id: string;
  email: string;
  roles: Role[];
}

class RBACService {
  private roleHierarchy: Map<Role, Role[]> = new Map([
    [Role.Admin, [Role.Manager, Role.User]],
    [Role.Manager, [Role.User]],
    [Role.User, []],
  ]);

  hasRole(user: User, requiredRole: Role): boolean {
    if (user.roles.includes(requiredRole)) {
      return true;
    }

    // Check if user has a higher role that includes the required role
    for (const userRole of user.roles) {
      const inheritedRoles = this.roleHierarchy.get(userRole) || [];
      if (inheritedRoles.includes(requiredRole)) {
        return true;
      }
    }

    return false;
  }

  requireRole(requiredRole: Role) {
    return (req: any, res: any, next: any) => {
      const user: User = req.user;

      if (!user) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      if (!this.hasRole(user, requiredRole)) {
        return res.status(403).json({ error: 'Insufficient permissions' });
      }

      next();
    };
  }
}

// Usage
const rbac = new RBACService();

app.get('/admin/users', rbac.requireRole(Role.Admin), (req, res) => {
  // Only admins can access
});

app.get('/manager/reports', rbac.requireRole(Role.Manager), (req, res) => {
  // Admins and managers can access
});
```

#### Python (FastAPI)

```python
from enum import Enum
from fastapi import Depends, HTTPException, status
from typing import List

class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class User:
    def __init__(self, id: str, email: str, roles: List[Role]):
        self.id = id
        self.email = email
        self.roles = roles

class RBACService:
    def __init__(self):
        self.role_hierarchy = {
            Role.ADMIN: [Role.MANAGER, Role.USER],
            Role.MANAGER: [Role.USER],
            Role.USER: [],
        }

    def has_role(self, user: User, required_role: Role) -> bool:
        if required_role in user.roles:
            return True

        # Check hierarchy
        for user_role in user.roles:
            inherited_roles = self.role_hierarchy.get(user_role, [])
            if required_role in inherited_roles:
                return True

        return False

    def require_role(self, required_role: Role):
        def dependency(user: User = Depends(get_current_user)):
            if not self.has_role(user, required_role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return user
        return dependency

# Usage
rbac = RBACService()

@app.get("/admin/users")
async def admin_users(user: User = Depends(rbac.require_role(Role.ADMIN))):
    # Only admins can access
    pass

@app.get("/manager/reports")
async def manager_reports(user: User = Depends(rbac.require_role(Role.MANAGER))):
    # Admins and managers can access
    pass
```

### Permission-Based RBAC

More granular control using explicit permissions:

```typescript
enum Permission {
  UserRead = 'user:read',
  UserWrite = 'user:write',
  UserDelete = 'user:delete',
  PostRead = 'post:read',
  PostWrite = 'post:write',
  PostDelete = 'post:delete',
}

interface Role {
  name: string;
  permissions: Permission[];
}

interface User {
  id: string;
  roles: Role[];
}

class PermissionService {
  private roles: Map<string, Role> = new Map([
    [
      'admin',
      {
        name: 'admin',
        permissions: [
          Permission.UserRead,
          Permission.UserWrite,
          Permission.UserDelete,
          Permission.PostRead,
          Permission.PostWrite,
          Permission.PostDelete,
        ],
      },
    ],
    [
      'editor',
      {
        name: 'editor',
        permissions: [Permission.PostRead, Permission.PostWrite],
      },
    ],
    [
      'viewer',
      {
        name: 'viewer',
        permissions: [Permission.UserRead, Permission.PostRead],
      },
    ],
  ]);

  getUserPermissions(user: User): Set<Permission> {
    const permissions = new Set<Permission>();

    for (const role of user.roles) {
      const roleDefinition = this.roles.get(role.name);
      if (roleDefinition) {
        roleDefinition.permissions.forEach((p) => permissions.add(p));
      }
    }

    return permissions;
  }

  hasPermission(user: User, permission: Permission): boolean {
    const userPermissions = this.getUserPermissions(user);
    return userPermissions.has(permission);
  }

  requirePermission(permission: Permission) {
    return (req: any, res: any, next: any) => {
      const user: User = req.user;

      if (!user) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      if (!this.hasPermission(user, permission)) {
        return res.status(403).json({ error: 'Missing required permission' });
      }

      next();
    };
  }
}

// Usage
const permissions = new PermissionService();

app.delete('/users/:id', permissions.requirePermission(Permission.UserDelete), (req, res) => {
  // Only users with user:delete permission can access
});
```

## Attribute-Based Access Control (ABAC)

ABAC evaluates attributes of the user, resource, action, and environment to make access decisions.

### TypeScript ABAC Implementation

```typescript
interface Policy {
  effect: 'allow' | 'deny';
  actions: string[];
  resources: string[];
  conditions?: Condition[];
}

interface Condition {
  attribute: string;
  operator: 'eq' | 'ne' | 'gt' | 'lt' | 'in' | 'contains';
  value: any;
}

interface Context {
  user: {
    id: string;
    role: string;
    department: string;
  };
  resource: {
    id: string;
    type: string;
    owner: string;
    department: string;
  };
  action: string;
  environment: {
    time: Date;
    ipAddress: string;
  };
}

class ABACService {
  private policies: Policy[] = [
    {
      effect: 'allow',
      actions: ['read'],
      resources: ['document'],
      conditions: [
        {
          attribute: 'user.department',
          operator: 'eq',
          value: 'resource.department',
        },
      ],
    },
    {
      effect: 'allow',
      actions: ['write', 'delete'],
      resources: ['document'],
      conditions: [
        {
          attribute: 'user.id',
          operator: 'eq',
          value: 'resource.owner',
        },
      ],
    },
    {
      effect: 'allow',
      actions: ['*'],
      resources: ['*'],
      conditions: [
        {
          attribute: 'user.role',
          operator: 'eq',
          value: 'admin',
        },
      ],
    },
  ];

  isAuthorized(context: Context): boolean {
    for (const policy of this.policies) {
      if (this.matchesPolicy(context, policy)) {
        return policy.effect === 'allow';
      }
    }

    return false; // Deny by default
  }

  private matchesPolicy(context: Context, policy: Policy): boolean {
    // Check action
    if (!policy.actions.includes('*') && !policy.actions.includes(context.action)) {
      return false;
    }

    // Check resource
    if (
      !policy.resources.includes('*') &&
      !policy.resources.includes(context.resource.type)
    ) {
      return false;
    }

    // Check conditions
    if (policy.conditions) {
      for (const condition of policy.conditions) {
        if (!this.evaluateCondition(context, condition)) {
          return false;
        }
      }
    }

    return true;
  }

  private evaluateCondition(context: Context, condition: Condition): boolean {
    const leftValue = this.resolveAttribute(context, condition.attribute);
    const rightValue =
      typeof condition.value === 'string' && condition.value.includes('.')
        ? this.resolveAttribute(context, condition.value)
        : condition.value;

    switch (condition.operator) {
      case 'eq':
        return leftValue === rightValue;
      case 'ne':
        return leftValue !== rightValue;
      case 'gt':
        return leftValue > rightValue;
      case 'lt':
        return leftValue < rightValue;
      case 'in':
        return Array.isArray(rightValue) && rightValue.includes(leftValue);
      case 'contains':
        return Array.isArray(leftValue) && leftValue.includes(rightValue);
      default:
        return false;
    }
  }

  private resolveAttribute(context: any, path: string): any {
    return path.split('.').reduce((obj, key) => obj?.[key], context);
  }
}

// Usage
const abac = new ABACService();

app.get('/documents/:id', async (req, res) => {
  const document = await getDocument(req.params.id);

  const context: Context = {
    user: req.user,
    resource: {
      id: document.id,
      type: 'document',
      owner: document.ownerId,
      department: document.department,
    },
    action: 'read',
    environment: {
      time: new Date(),
      ipAddress: req.ip,
    },
  };

  if (!abac.isAuthorized(context)) {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.json(document);
});
```

## Row Level Security (RLS)

RLS enforces access control at the database level, ensuring users can only access rows they're authorized to see.

### PostgreSQL / Supabase RLS

#### Setting Up RLS

```sql
-- Enable RLS on a table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Policy 1: Users can view their own posts
CREATE POLICY "Users can view own posts"
  ON posts
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy 2: Users can view public posts
CREATE POLICY "Anyone can view public posts"
  ON posts
  FOR SELECT
  USING (is_public = true);

-- Policy 3: Users can insert their own posts
CREATE POLICY "Users can insert own posts"
  ON posts
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy 4: Users can update their own posts
CREATE POLICY "Users can update own posts"
  ON posts
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy 5: Users can delete their own posts
CREATE POLICY "Users can delete own posts"
  ON posts
  FOR DELETE
  USING (auth.uid() = user_id);
```

#### Multi-Tenant RLS

```sql
-- Enable RLS on tenants table
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Organization membership table
CREATE TABLE organization_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id),
  user_id UUID REFERENCES auth.users(id),
  role TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;

-- Helper function to check organization membership
CREATE OR REPLACE FUNCTION user_has_org_access(org_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1
    FROM organization_members
    WHERE organization_id = org_id
      AND user_id = auth.uid()
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- RLS Policies

-- Organizations: Users can only see organizations they're members of
CREATE POLICY "Users can view own organizations"
  ON organizations
  FOR SELECT
  USING (user_has_org_access(id));

-- Projects: Users can see projects in their organizations
CREATE POLICY "Users can view organization projects"
  ON projects
  FOR SELECT
  USING (user_has_org_access(organization_id));

-- Projects: Users can create projects in their organizations
CREATE POLICY "Users can create projects in own organizations"
  ON projects
  FOR INSERT
  WITH CHECK (user_has_org_access(organization_id));
```

#### Role-Based RLS

```sql
-- Helper function to get user role in organization
CREATE OR REPLACE FUNCTION get_user_org_role(org_id UUID)
RETURNS TEXT AS $$
  SELECT role
  FROM organization_members
  WHERE organization_id = org_id
    AND user_id = auth.uid()
  LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER;

-- Admin-only operations
CREATE POLICY "Admins can delete projects"
  ON projects
  FOR DELETE
  USING (get_user_org_role(organization_id) = 'admin');

-- Managers and admins can update
CREATE POLICY "Managers can update projects"
  ON projects
  FOR UPDATE
  USING (
    get_user_org_role(organization_id) IN ('admin', 'manager')
  )
  WITH CHECK (
    get_user_org_role(organization_id) IN ('admin', 'manager')
  );
```

### Supabase Client Usage

#### TypeScript with Supabase

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
);

// RLS is automatically enforced
// User will only see their own posts
async function getUserPosts(userId: string) {
  const { data, error } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', userId);

  if (error) throw error;
  return data;
}

// Insert with RLS - will only succeed if policy allows
async function createPost(title: string, content: string) {
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) throw new Error('Not authenticated');

  const { data, error } = await supabase.from('posts').insert({
    title,
    content,
    user_id: user.id,
    is_public: false,
  });

  if (error) throw error;
  return data;
}

// Update with RLS - will only succeed if user owns the post
async function updatePost(postId: string, updates: { title?: string; content?: string }) {
  const { data, error } = await supabase
    .from('posts')
    .update(updates)
    .eq('id', postId);

  if (error) throw error;
  return data;
}
```

#### Python with Supabase

```python
from supabase import create_client, Client

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

# RLS is automatically enforced
async def get_user_posts(user_id: str):
    response = supabase.table('posts').select('*').eq('user_id', user_id).execute()
    return response.data

async def create_post(title: str, content: str):
    user = supabase.auth.get_user()
    if not user:
        raise Exception("Not authenticated")

    response = supabase.table('posts').insert({
        'title': title,
        'content': content,
        'user_id': user.id,
        'is_public': False
    }).execute()

    return response.data
```

### Advanced RLS Patterns

#### Time-Based Access

```sql
-- Posts are only visible during working hours (9 AM - 5 PM)
CREATE POLICY "Posts visible during working hours"
  ON posts
  FOR SELECT
  USING (
    EXTRACT(HOUR FROM NOW()) >= 9
    AND EXTRACT(HOUR FROM NOW()) < 17
  );

-- Posts are only editable within 24 hours of creation
CREATE POLICY "Posts editable within 24 hours"
  ON posts
  FOR UPDATE
  USING (
    auth.uid() = user_id
    AND created_at > NOW() - INTERVAL '24 hours'
  );
```

#### Hierarchical Access

```sql
-- Department hierarchy
CREATE TABLE departments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  parent_id UUID REFERENCES departments(id)
);

-- Recursive function to check department access
CREATE OR REPLACE FUNCTION user_has_department_access(dept_id UUID)
RETURNS BOOLEAN AS $$
WITH RECURSIVE dept_tree AS (
  -- Base case: direct department membership
  SELECT d.id
  FROM departments d
  JOIN users u ON u.department_id = d.id
  WHERE u.id = auth.uid()

  UNION

  -- Recursive case: parent departments
  SELECT d.id
  FROM departments d
  JOIN dept_tree dt ON d.parent_id = dt.id
)
SELECT EXISTS (
  SELECT 1 FROM dept_tree WHERE id = dept_id
);
$$ LANGUAGE sql SECURITY DEFINER;

-- Policy using hierarchical access
CREATE POLICY "Users can view department documents"
  ON documents
  FOR SELECT
  USING (user_has_department_access(department_id));
```

## Permission Checking Patterns

### Decorator Pattern (TypeScript)

```typescript
function RequirePermission(permission: Permission) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const user = this.getCurrentUser(); // Assume this method exists

      if (!hasPermission(user, permission)) {
        throw new Error('Insufficient permissions');
      }

      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

class PostController {
  @RequirePermission(Permission.PostWrite)
  async createPost(data: CreatePostDto) {
    // Only users with post:write permission can execute this
    return this.postService.create(data);
  }

  @RequirePermission(Permission.PostDelete)
  async deletePost(id: string) {
    // Only users with post:delete permission can execute this
    return this.postService.delete(id);
  }
}
```

### Resource-Based Authorization

```typescript
interface Resource {
  id: string;
  ownerId: string;
  organizationId: string;
  isPublic: boolean;
}

class AuthorizationService {
  canView(user: User, resource: Resource): boolean {
    // Public resources
    if (resource.isPublic) {
      return true;
    }

    // Owner can always view
    if (resource.ownerId === user.id) {
      return true;
    }

    // Same organization members can view
    if (resource.organizationId === user.organizationId) {
      return true;
    }

    // Admins can view everything
    if (user.roles.includes(Role.Admin)) {
      return true;
    }

    return false;
  }

  canEdit(user: User, resource: Resource): boolean {
    // Owner can edit
    if (resource.ownerId === user.id) {
      return true;
    }

    // Organization admins can edit
    if (
      resource.organizationId === user.organizationId &&
      user.roles.includes(Role.Admin)
    ) {
      return true;
    }

    return false;
  }

  canDelete(user: User, resource: Resource): boolean {
    // Only owner or admin can delete
    return (
      resource.ownerId === user.id ||
      user.roles.includes(Role.Admin)
    );
  }
}

// Usage
app.get('/posts/:id', async (req, res) => {
  const post = await getPost(req.params.id);
  const user = req.user;

  if (!authz.canView(user, post)) {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.json(post);
});
```

## Testing Authorization

### Unit Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('RBACService', () => {
  it('should allow admin to access admin routes', () => {
    const user: User = {
      id: '1',
      email: 'admin@example.com',
      roles: [Role.Admin],
    };

    const rbac = new RBACService();
    expect(rbac.hasRole(user, Role.Admin)).toBe(true);
    expect(rbac.hasRole(user, Role.Manager)).toBe(true); // Hierarchy
  });

  it('should deny user from accessing admin routes', () => {
    const user: User = {
      id: '2',
      email: 'user@example.com',
      roles: [Role.User],
    };

    const rbac = new RBACService();
    expect(rbac.hasRole(user, Role.Admin)).toBe(false);
  });
});
```

### Integration Tests with RLS

```typescript
import { createClient } from '@supabase/supabase-js';

describe('RLS Policies', () => {
  it('should only return user own posts', async () => {
    // Create authenticated client for user 1
    const user1Client = createClient(url, key);
    await user1Client.auth.signInWithPassword({
      email: 'user1@example.com',
      password: 'password',
    });

    // Create authenticated client for user 2
    const user2Client = createClient(url, key);
    await user2Client.auth.signInWithPassword({
      email: 'user2@example.com',
      password: 'password',
    });

    // User 1 creates a post
    await user1Client.from('posts').insert({
      title: 'User 1 Post',
      content: 'Content',
    });

    // User 2 should not see user 1's post
    const { data } = await user2Client.from('posts').select('*');

    expect(data).toHaveLength(0);
  });
});
```

## Authorization Best Practices

1. **Principle of Least Privilege** - Grant minimum permissions necessary
2. **Defense in Depth** - Implement authorization at multiple layers (API, database, UI)
3. **Explicit Deny** - Deny by default, require explicit allow
4. **Audit Logging** - Log all authorization decisions
5. **Regular Reviews** - Audit and update permissions regularly
6. **Separation of Concerns** - Keep authorization logic separate from business logic
7. **Test Thoroughly** - Test both positive and negative authorization cases
8. **Use RLS for Data Isolation** - Let database enforce row-level access
9. **Cache Wisely** - Cache permissions but invalidate on changes
10. **Document Policies** - Clearly document authorization rules

## Security Checklist

- [ ] Authorization checks on all protected endpoints
- [ ] RLS enabled on multi-tenant tables
- [ ] Role hierarchy properly configured
- [ ] Permission checks before data operations
- [ ] Authorization failures logged
- [ ] Regular permission audits scheduled
- [ ] Tests for authorization logic
- [ ] Separation of admin and user contexts
- [ ] Proper error messages (don't leak info)
- [ ] Authorization middleware on sensitive routes
