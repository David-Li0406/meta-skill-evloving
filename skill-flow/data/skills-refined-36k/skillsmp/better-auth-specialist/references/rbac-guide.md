# Role-Based Access Control (RBAC) Guide

Complete guide to implementing role-based access control with Better Auth.

## RBAC Concepts

### Core Components

1. **Users** - People using the system
2. **Roles** - Named collections of permissions (e.g., admin, user, moderator)
3. **Permissions** - Specific actions on resources (e.g., user:read, post:delete)
4. **Resources** - What is being accessed (e.g., user, post, comment)
5. **Actions** - Operations on resources (e.g., read, write, delete)

### Permission Format

Use the format: `resource:action`

Examples:
- `user:read` - Read user information
- `user:write` - Create/update users
- `user:delete` - Delete users
- `post:create` - Create posts
- `post:publish` - Publish posts
- `admin:access` - Access admin panel

## Implementation Patterns

### Database Setup

See [database-schemas.md](database-schemas.md) for complete schema definitions.

### Backend Implementation

#### Node.js/Express

```typescript
// services/rbac.ts
import { prisma } from "@/lib/prisma";

export async function getUserRoles(userId: string) {
  const userRoles = await prisma.userRole.findMany({
    where: { userId },
    include: {
      role: {
        include: {
          rolePermissions: {
            include: {
              permission: true,
            },
          },
        },
      },
    },
  });

  return userRoles.map((ur) => ur.role);
}

export async function getUserPermissions(userId: string) {
  const roles = await getUserRoles(userId);

  const permissions = roles.flatMap((role) =>
    role.rolePermissions.map((rp) => rp.permission)
  );

  // Remove duplicates
  return [...new Map(permissions.map((p) => [p.id, p])).values()];
}

export async function checkPermission(
  userId: string,
  resource: string,
  action: string
): Promise<boolean> {
  const permissions = await getUserPermissions(userId);

  return permissions.some(
    (p) => p.resource === resource && p.action === action
  );
}

export async function checkAnyPermission(
  userId: string,
  requiredPermissions: Array<{ resource: string; action: string }>
): Promise<boolean> {
  const permissions = await getUserPermissions(userId);

  return requiredPermissions.some((required) =>
    permissions.some(
      (p) => p.resource === required.resource && p.action === required.action
    )
  );
}
```

#### FastAPI

```python
# services/rbac.py
from sqlalchemy.orm import Session
from typing import List, Dict
from app.models import User, Role, Permission, UserRole, RolePermission

async def get_user_roles(db: Session, user_id: str) -> List[Role]:
    """Get all roles for a user"""
    user_roles = db.query(UserRole).filter(
        UserRole.user_id == user_id
    ).join(Role).all()

    return [ur.role for ur in user_roles]

async def get_user_permissions(db: Session, user_id: str) -> List[Permission]:
    """Get all permissions for a user"""
    roles = await get_user_roles(db, user_id)

    permissions = []
    for role in roles:
        role_perms = db.query(RolePermission).filter(
            RolePermission.role_id == role.id
        ).join(Permission).all()

        permissions.extend([rp.permission for rp in role_perms])

    # Remove duplicates
    unique_permissions = {p.id: p for p in permissions}
    return list(unique_permissions.values())

async def check_permission(
    db: Session,
    user_id: str,
    resource: str,
    action: str
) -> bool:
    """Check if user has a specific permission"""
    permissions = await get_user_permissions(db, user_id)

    return any(
        p.resource == resource and p.action == action
        for p in permissions
    )

async def check_any_permission(
    db: Session,
    user_id: str,
    required_permissions: List[Dict[str, str]]
) -> bool:
    """Check if user has any of the required permissions"""
    permissions = await get_user_permissions(db, user_id)

    return any(
        any(p.resource == req["resource"] and p.action == req["action"]
            for p in permissions)
        for req in required_permissions
    )
```

### Middleware Implementation

#### Node.js/Express Role Middleware

```typescript
// middleware/rbac.ts
import { Request, Response, NextFunction } from "express";
import { checkPermission, getUserRoles } from "@/services/rbac";

export function requireRole(...roles: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    try {
      const userRoles = await getUserRoles(req.user.id);
      const hasRole = userRoles.some((role) => roles.includes(role.name));

      if (!hasRole) {
        return res.status(403).json({
          error: "Insufficient permissions",
          required: roles,
        });
      }

      req.userRoles = userRoles;
      next();
    } catch (error) {
      return res.status(500).json({ error: "Internal server error" });
    }
  };
}

export function requirePermission(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    try {
      const hasPermission = await checkPermission(
        req.user.id,
        resource,
        action
      );

      if (!hasPermission) {
        return res.status(403).json({
          error: "Insufficient permissions",
          required: `${resource}:${action}`,
        });
      }

      next();
    } catch (error) {
      return res.status(500).json({ error: "Internal server error" });
    }
  };
}

// Usage
router.get("/users", requireAuth, requireRole("admin"), async (req, res) => {
  // Only admins can access
});

router.delete("/users/:id", requireAuth, requirePermission("user", "delete"), async (req, res) => {
  // Only users with user:delete permission
});
```

#### FastAPI Dependencies

```python
# dependencies/rbac.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_current_user, get_db
from app.services.rbac import get_user_roles, check_permission

def require_role(*roles: str):
    """Dependency to require specific roles"""
    async def role_checker(
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user_roles = await get_user_roles(db, user["id"])
        user_role_names = [role.name for role in user_roles]

        if not any(role in user_role_names for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(roles)}"
            )

        return user

    return role_checker

def require_permission(resource: str, action: str):
    """Dependency to require specific permission"""
    async def permission_checker(
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        has_permission = await check_permission(
            db, user["id"], resource, action
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required permission: {resource}:{action}"
            )

        return user

    return permission_checker

# Usage
@router.get("/users")
async def get_users(user: dict = Depends(require_role("admin"))):
    # Only admins can access
    pass

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    user: dict = Depends(require_permission("user", "delete"))
):
    # Only users with user:delete permission
    pass
```

### Frontend Implementation

#### Role Check Hook

```typescript
// hooks/use-rbac.ts
"use client";

import { useSession } from "@/lib/auth-client";
import { useEffect, useState } from "react";

interface Permission {
  id: string;
  name: string;
  resource: string;
  action: string;
}

interface Role {
  id: string;
  name: string;
  permissions: Permission[];
}

export function useRBAC() {
  const { data: session } = useSession();
  const [roles, setRoles] = useState<Role[]>([]);
  const [permissions, setPermissions] = useState<Permission[]>([]);

  useEffect(() => {
    if (session?.user) {
      // Fetch user roles and permissions
      fetchUserRoles();
    }
  }, [session]);

  const fetchUserRoles = async () => {
    const response = await fetch("/api/user/roles");
    const data = await response.json();
    setRoles(data.roles);

    // Flatten permissions from all roles
    const allPermissions = data.roles.flatMap((role: Role) => role.permissions);
    setPermissions(allPermissions);
  };

  const hasRole = (roleName: string): boolean => {
    return roles.some((role) => role.name === roleName);
  };

  const hasAnyRole = (roleNames: string[]): boolean => {
    return roleNames.some((name) => hasRole(name));
  };

  const hasPermission = (resource: string, action: string): boolean => {
    return permissions.some(
      (p) => p.resource === resource && p.action === action
    );
  };

  const hasAnyPermission = (
    requiredPermissions: Array<{ resource: string; action: string }>
  ): boolean => {
    return requiredPermissions.some((required) =>
      hasPermission(required.resource, required.action)
    );
  };

  return {
    roles,
    permissions,
    hasRole,
    hasAnyRole,
    hasPermission,
    hasAnyPermission,
  };
}
```

#### Role Guard Component

```typescript
// components/rbac/role-guard.tsx
"use client";

import { useRBAC } from "@/hooks/use-rbac";
import { ReactNode } from "react";

interface RoleGuardProps {
  roles: string[];
  children: ReactNode;
  fallback?: ReactNode;
}

export function RoleGuard({ roles, children, fallback = null }: RoleGuardProps) {
  const { hasAnyRole } = useRBAC();

  if (!hasAnyRole(roles)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

// Usage
<RoleGuard roles={["admin", "moderator"]} fallback={<p>Access denied</p>}>
  <AdminPanel />
</RoleGuard>
```

#### Permission Guard Component

```typescript
// components/rbac/permission-guard.tsx
"use client";

import { useRBAC } from "@/hooks/use-rbac";
import { ReactNode } from "react";

interface PermissionGuardProps {
  resource: string;
  action: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export function PermissionGuard({
  resource,
  action,
  children,
  fallback = null,
}: PermissionGuardProps) {
  const { hasPermission } = useRBAC();

  if (!hasPermission(resource, action)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

// Usage
<PermissionGuard resource="user" action="delete">
  <Button variant="destructive">Delete User</Button>
</PermissionGuard>
```

## Role Management API

### Create Role

**Node.js/Express**
```typescript
router.post("/roles", requireAuth, requireRole("admin"), async (req, res) => {
  const { name, description, permissionIds } = req.body;

  const role = await prisma.role.create({
    data: {
      id: `role_${name}`,
      name,
      description,
      rolePermissions: {
        create: permissionIds.map((permissionId: string) => ({
          permissionId,
        })),
      },
    },
    include: {
      rolePermissions: {
        include: {
          permission: true,
        },
      },
    },
  });

  return res.status(201).json(role);
});
```

**FastAPI**
```python
@router.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_role(
    data: CreateRoleRequest,
    user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    role = Role(
        id=f"role_{data.name}",
        name=data.name,
        description=data.description
    )
    db.add(role)

    for permission_id in data.permission_ids:
        role_permission = RolePermission(
            role_id=role.id,
            permission_id=permission_id
        )
        db.add(role_permission)

    db.commit()
    db.refresh(role)

    return role
```

### Assign Role to User

**Node.js/Express**
```typescript
router.post("/users/:userId/roles", requireAuth, requireRole("admin"), async (req, res) => {
  const { userId } = req.params;
  const { roleId } = req.body;

  const userRole = await prisma.userRole.create({
    data: {
      userId,
      roleId,
    },
  });

  return res.status(201).json(userRole);
});
```

**FastAPI**
```python
@router.post("/users/{user_id}/roles", status_code=status.HTTP_201_CREATED)
async def assign_role(
    user_id: str,
    data: AssignRoleRequest,
    user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    user_role = UserRole(
        user_id=user_id,
        role_id=data.role_id
    )
    db.add(user_role)
    db.commit()
    db.refresh(user_role)

    return user_role
```

## Common RBAC Patterns

### Hierarchical Roles

```typescript
const roleHierarchy: Record<string, string[]> = {
  admin: ["admin", "moderator", "user"],
  moderator: ["moderator", "user"],
  user: ["user"],
};

export function hasRoleOrHigher(userRoles: string[], requiredRole: string): boolean {
  const allowedRoles = roleHierarchy[requiredRole] || [requiredRole];

  return userRoles.some((role) => allowedRoles.includes(role));
}
```

### Resource Ownership

```typescript
export async function canAccessResource(
  userId: string,
  resourceType: string,
  resourceId: string
): Promise<boolean> {
  // Check if user owns the resource
  const resource = await prisma[resourceType].findUnique({
    where: { id: resourceId },
  });

  if (resource?.userId === userId) {
    return true;
  }

  // Check if user has admin permission
  return await checkPermission(userId, resourceType, "admin");
}
```

### Dynamic Permissions

```typescript
export async function canModifyUser(
  actorId: string,
  targetUserId: string
): Promise<boolean> {
  // Users can modify themselves
  if (actorId === targetUserId) {
    return true;
  }

  // Admins can modify anyone
  return await checkPermission(actorId, "user", "write");
}
```

## Testing RBAC

```typescript
// tests/rbac.test.ts
import { checkPermission, getUserRoles } from "@/services/rbac";

describe("RBAC", () => {
  it("should grant admin all permissions", async () => {
    const userId = "admin-user-id";
    const hasPermission = await checkPermission(userId, "user", "delete");
    expect(hasPermission).toBe(true);
  });

  it("should deny regular users admin permissions", async () => {
    const userId = "regular-user-id";
    const hasPermission = await checkPermission(userId, "admin", "access");
    expect(hasPermission).toBe(false);
  });

  it("should return user roles", async () => {
    const userId = "user-id";
    const roles = await getUserRoles(userId);
    expect(roles).toContainEqual(
      expect.objectContaining({ name: "user" })
    );
  });
});
```

## Best Practices

1. **Principle of Least Privilege** - Grant minimum necessary permissions
2. **Role Hierarchy** - Use hierarchical roles when appropriate
3. **Permission Naming** - Use consistent `resource:action` format
4. **Audit Logging** - Log permission checks and role changes
5. **Cache Permissions** - Cache user permissions to improve performance
6. **Regular Reviews** - Periodically review and update roles/permissions
7. **Default Deny** - Deny access by default, explicitly grant permissions
8. **Separate Admin** - Keep admin roles and permissions isolated
