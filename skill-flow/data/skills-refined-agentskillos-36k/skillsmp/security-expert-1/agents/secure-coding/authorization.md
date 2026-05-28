---
name: authorization
description: Expert controle d'acces - RBAC, ABAC, policies et permissions
---

# Controle d'Acces (Authorization)

Tu es expert en **controle d'acces** et gestion des permissions.

## Mission

> S'assurer que chaque utilisateur ne peut acceder qu'aux ressources autorisees.

## Difference AuthN vs AuthZ

| Aspect | Authentication | Authorization |
|--------|----------------|---------------|
| Question | "Qui es-tu ?" | "Que peux-tu faire ?" |
| Verif | Identite | Permissions |
| Quand | Connexion | Chaque action |

## Modeles de Controle d'Acces

### RBAC (Role-Based Access Control)

```typescript
// Definition des roles et permissions
const ROLES = {
  admin: ['read', 'write', 'delete', 'manage_users'],
  editor: ['read', 'write'],
  viewer: ['read'],
} as const;

type Role = keyof typeof ROLES;
type Permission = typeof ROLES[Role][number];

// Verification
function hasPermission(role: Role, permission: Permission): boolean {
  return ROLES[role].includes(permission);
}

// Middleware
function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.user?.role as Role;

    if (!userRole || !hasPermission(userRole, permission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Usage
app.delete('/posts/:id',
  authMiddleware,
  requirePermission('delete'),
  deletePostHandler
);
```

### ABAC (Attribute-Based Access Control)

```typescript
interface PolicyContext {
  user: {
    id: string;
    role: string;
    department: string;
  };
  resource: {
    type: string;
    ownerId: string;
    status: string;
  };
  action: string;
  environment: {
    time: Date;
    ip: string;
  };
}

// Policies
const policies: Policy[] = [
  // Users can read their own resources
  {
    effect: 'allow',
    condition: (ctx) =>
      ctx.action === 'read' &&
      ctx.resource.ownerId === ctx.user.id,
  },
  // Managers can approve in their department
  {
    effect: 'allow',
    condition: (ctx) =>
      ctx.action === 'approve' &&
      ctx.user.role === 'manager' &&
      ctx.resource.department === ctx.user.department,
  },
  // No access outside business hours for non-admins
  {
    effect: 'deny',
    condition: (ctx) => {
      const hour = ctx.environment.time.getHours();
      return ctx.user.role !== 'admin' && (hour < 8 || hour > 18);
    },
  },
];

function evaluate(ctx: PolicyContext): boolean {
  // Deny by default
  let allowed = false;

  for (const policy of policies) {
    if (policy.condition(ctx)) {
      if (policy.effect === 'deny') return false;
      if (policy.effect === 'allow') allowed = true;
    }
  }

  return allowed;
}
```

### Resource-Level Permissions

```typescript
// Verifier que l'utilisateur peut acceder a une ressource specifique
async function canAccessPost(userId: string, postId: string): Promise<boolean> {
  const post = await db.post.findUnique({
    where: { id: postId },
    select: { authorId: true, visibility: true },
  });

  if (!post) return false;

  // Public posts
  if (post.visibility === 'public') return true;

  // Own posts
  if (post.authorId === userId) return true;

  // Check if user is in allowed list
  const access = await db.postAccess.findFirst({
    where: { postId, userId },
  });

  return !!access;
}

// Middleware
async function authorizePost(req: Request, res: Response, next: NextFunction) {
  const userId = req.user?.id;
  const postId = req.params.id;

  if (!await canAccessPost(userId, postId)) {
    return res.status(403).json({ error: 'Access denied to this post' });
  }

  next();
}
```

## Implementation avec CASL

```typescript
import { AbilityBuilder, createMongoAbility, MongoAbility } from '@casl/ability';

type Actions = 'create' | 'read' | 'update' | 'delete' | 'manage';
type Subjects = 'Post' | 'User' | 'Comment' | 'all';

export type AppAbility = MongoAbility<[Actions, Subjects]>;

export function defineAbilityFor(user: User): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(createMongoAbility);

  if (user.role === 'admin') {
    can('manage', 'all'); // Admin peut tout faire
  } else if (user.role === 'editor') {
    can('read', 'Post');
    can('create', 'Post');
    can('update', 'Post', { authorId: user.id }); // Seulement ses posts
    can('delete', 'Post', { authorId: user.id });
    cannot('delete', 'Post', { status: 'published' }); // Sauf si publie
  } else {
    // viewer
    can('read', 'Post', { visibility: 'public' });
  }

  return build();
}

// Usage
const ability = defineAbilityFor(user);

if (ability.can('update', post)) {
  // Autoriser modification
}

// Express middleware
function authorize(action: Actions, subject: Subjects) {
  return (req: Request, res: Response, next: NextFunction) => {
    const ability = defineAbilityFor(req.user);

    if (ability.cannot(action, subject)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}
```

## Patterns Securises

### 1. Deny by Default

```typescript
// Toujours commencer par refuser
function checkAccess(user: User, resource: Resource, action: string): boolean {
  // Default: deny
  if (!user || !resource) return false;

  // Explicit allows
  if (isOwner(user, resource)) return true;
  if (hasExplicitPermission(user, resource, action)) return true;

  return false;
}
```

### 2. Verification Systematique

```typescript
// Verifier a chaque action, pas juste au login
app.get('/api/users/:id', authMiddleware, async (req, res) => {
  const targetUserId = req.params.id;
  const requestingUser = req.user;

  // Verifier que l'utilisateur peut voir ce profil
  if (targetUserId !== requestingUser.id && requestingUser.role !== 'admin') {
    return res.status(403).json({ error: 'Cannot access this user' });
  }

  // ...
});
```

### 3. Eviter les References Directes (IDOR)

```typescript
// BAD: Acces direct sans verification
app.get('/api/documents/:id', async (req, res) => {
  const doc = await db.document.findUnique({
    where: { id: req.params.id }
  });
  res.json(doc); // N'importe qui peut acceder
});

// GOOD: Toujours verifier l'appartenance
app.get('/api/documents/:id', authMiddleware, async (req, res) => {
  const doc = await db.document.findFirst({
    where: {
      id: req.params.id,
      OR: [
        { ownerId: req.user.id },
        { sharedWith: { some: { userId: req.user.id } } },
        { visibility: 'public' },
      ],
    },
  });

  if (!doc) {
    return res.status(404).json({ error: 'Document not found' });
  }

  res.json(doc);
});
```

## Audit des Acces

```typescript
// Logger les acces sensibles
async function logAccess(
  userId: string,
  action: string,
  resourceType: string,
  resourceId: string,
  allowed: boolean
) {
  await db.accessLog.create({
    data: {
      userId,
      action,
      resourceType,
      resourceId,
      allowed,
      timestamp: new Date(),
      ip: req.ip,
      userAgent: req.headers['user-agent'],
    },
  });
}
```

## Anti-Patterns

| Pattern | Risque | Solution |
|---------|--------|----------|
| Verification frontend only | Bypass | Verifier cote serveur |
| Role en JWT non-verifie | Privilege escalation | Verifier en DB |
| `if (admin) show(all)` | Trop permissif | Least privilege |
| ID sequentiels | IDOR enumeration | UUIDs + authz check |

## Voir Aussi

- `secure-coding/authentication` pour AuthN
- `penetration/owasp-top10` A01 Broken Access Control
- `compliance/rgpd` pour droits d'acces donnees
