# Database Schemas for Better Auth

Database schemas for user authentication with Better Auth supporting both SQL and NoSQL databases.

## SQL Schemas (PostgreSQL/MySQL)

### Core User Table

```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Sessions Table

```sql
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### Accounts Table (for OAuth)

```sql
CREATE TABLE accounts (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    provider VARCHAR(255) NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    token_type VARCHAR(50),
    scope TEXT,
    id_token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_provider_account (provider, provider_account_id)
);

CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_accounts_provider ON accounts(provider);
```

### Verification Tokens Table

```sql
CREATE TABLE verification_tokens (
    id VARCHAR(255) PRIMARY KEY,
    identifier VARCHAR(255) NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_verification_tokens_token ON verification_tokens(token);
CREATE INDEX idx_verification_tokens_identifier ON verification_tokens(identifier);
```

### Roles and Permissions (RBAC)

```sql
CREATE TABLE roles (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    resource VARCHAR(100),
    action VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE role_permissions (
    role_id VARCHAR(255) NOT NULL,
    permission_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

CREATE TABLE user_roles (
    user_id VARCHAR(255) NOT NULL,
    role_id VARCHAR(255) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
```

### Password Table (if using email/password)

```sql
CREATE TABLE passwords (
    user_id VARCHAR(255) PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## NoSQL Schemas (MongoDB)

### Users Collection

```javascript
{
  _id: ObjectId,
  id: String, // UUID for compatibility
  email: String, // indexed, unique
  emailVerified: Boolean,
  name: String,
  image: String,
  createdAt: Date,
  updatedAt: Date
}

// Indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ id: 1 }, { unique: true })
```

### Sessions Collection

```javascript
{
  _id: ObjectId,
  id: String, // UUID
  userId: String, // references users.id
  expiresAt: Date, // indexed
  token: String, // indexed, unique
  ipAddress: String,
  userAgent: String,
  createdAt: Date
}

// Indexes
db.sessions.createIndex({ token: 1 }, { unique: true })
db.sessions.createIndex({ userId: 1 })
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 }) // TTL index
```

### Accounts Collection (OAuth)

```javascript
{
  _id: ObjectId,
  id: String, // UUID
  userId: String, // references users.id
  accountId: String,
  provider: String,
  providerAccountId: String,
  accessToken: String,
  refreshToken: String,
  expiresAt: Date,
  tokenType: String,
  scope: String,
  idToken: String,
  createdAt: Date,
  updatedAt: Date
}

// Indexes
db.accounts.createIndex({ userId: 1 })
db.accounts.createIndex({ provider: 1, providerAccountId: 1 }, { unique: true })
```

### Verification Tokens Collection

```javascript
{
  _id: ObjectId,
  id: String, // UUID
  identifier: String,
  token: String, // indexed, unique
  expiresAt: Date,
  createdAt: Date
}

// Indexes
db.verificationTokens.createIndex({ token: 1 }, { unique: true })
db.verificationTokens.createIndex({ identifier: 1 })
db.verificationTokens.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 }) // TTL
```

### Roles Collection (RBAC)

```javascript
{
  _id: ObjectId,
  id: String, // UUID
  name: String, // indexed, unique
  description: String,
  permissions: [
    {
      id: String,
      name: String,
      resource: String,
      action: String
    }
  ],
  createdAt: Date
}

// Indexes
db.roles.createIndex({ name: 1 }, { unique: true })
db.roles.createIndex({ "permissions.name": 1 })
```

### Users with Roles (Extended User Document)

```javascript
{
  _id: ObjectId,
  id: String,
  email: String,
  emailVerified: Boolean,
  name: String,
  image: String,
  roles: [
    {
      roleId: String,
      roleName: String,
      assignedAt: Date
    }
  ],
  password: {
    hash: String,
    updatedAt: Date
  },
  createdAt: Date,
  updatedAt: Date
}

// Indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ "roles.roleId": 1 })
```

## Migration Scripts

### SQL Migration (PostgreSQL Example)

```sql
-- Create all tables in order
BEGIN;

CREATE TABLE users (...);
CREATE TABLE sessions (...);
CREATE TABLE accounts (...);
CREATE TABLE verification_tokens (...);
CREATE TABLE passwords (...);
CREATE TABLE roles (...);
CREATE TABLE permissions (...);
CREATE TABLE role_permissions (...);
CREATE TABLE user_roles (...);

-- Insert default roles
INSERT INTO roles (id, name, description) VALUES
  ('role_admin', 'admin', 'Administrator with full access'),
  ('role_user', 'user', 'Standard user with limited access'),
  ('role_moderator', 'moderator', 'Moderator with elevated privileges');

-- Insert default permissions
INSERT INTO permissions (id, name, resource, action, description) VALUES
  ('perm_user_read', 'user:read', 'user', 'read', 'Read user information'),
  ('perm_user_write', 'user:write', 'user', 'write', 'Create/update users'),
  ('perm_user_delete', 'user:delete', 'user', 'delete', 'Delete users'),
  ('perm_admin_access', 'admin:access', 'admin', 'access', 'Access admin panel');

-- Assign permissions to admin role
INSERT INTO role_permissions (role_id, permission_id) VALUES
  ('role_admin', 'perm_user_read'),
  ('role_admin', 'perm_user_write'),
  ('role_admin', 'perm_user_delete'),
  ('role_admin', 'perm_admin_access');

-- Assign permissions to user role
INSERT INTO role_permissions (role_id, permission_id) VALUES
  ('role_user', 'perm_user_read');

COMMIT;
```

### MongoDB Initialization Script

```javascript
// Initialize collections and indexes
db.createCollection("users");
db.createCollection("sessions");
db.createCollection("accounts");
db.createCollection("verificationTokens");
db.createCollection("roles");

// Create indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ id: 1 }, { unique: true });
db.sessions.createIndex({ token: 1 }, { unique: true });
db.sessions.createIndex({ userId: 1 });
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
db.accounts.createIndex({ userId: 1 });
db.accounts.createIndex({ provider: 1, providerAccountId: 1 }, { unique: true });
db.verificationTokens.createIndex({ token: 1 }, { unique: true });
db.verificationTokens.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
db.roles.createIndex({ name: 1 }, { unique: true });

// Insert default roles
db.roles.insertMany([
  {
    id: "role_admin",
    name: "admin",
    description: "Administrator with full access",
    permissions: [
      { id: "perm_user_read", name: "user:read", resource: "user", action: "read" },
      { id: "perm_user_write", name: "user:write", resource: "user", action: "write" },
      { id: "perm_user_delete", name: "user:delete", resource: "user", action: "delete" },
      { id: "perm_admin_access", name: "admin:access", resource: "admin", action: "access" }
    ],
    createdAt: new Date()
  },
  {
    id: "role_user",
    name: "user",
    description: "Standard user with limited access",
    permissions: [
      { id: "perm_user_read", name: "user:read", resource: "user", action: "read" }
    ],
    createdAt: new Date()
  },
  {
    id: "role_moderator",
    name: "moderator",
    description: "Moderator with elevated privileges",
    permissions: [
      { id: "perm_user_read", name: "user:read", resource: "user", action: "read" },
      { id: "perm_user_write", name: "user:write", resource: "user", action: "write" }
    ],
    createdAt: new Date()
  }
]);
```

## TypeScript Types

```typescript
// User types
interface User {
  id: string;
  email: string;
  emailVerified: boolean;
  name?: string;
  image?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface Session {
  id: string;
  userId: string;
  expiresAt: Date;
  token: string;
  ipAddress?: string;
  userAgent?: string;
  createdAt: Date;
}

interface Account {
  id: string;
  userId: string;
  accountId: string;
  provider: string;
  providerAccountId: string;
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: Date;
  tokenType?: string;
  scope?: string;
  idToken?: string;
}

// RBAC types
interface Role {
  id: string;
  name: string;
  description?: string;
  createdAt: Date;
}

interface Permission {
  id: string;
  name: string;
  description?: string;
  resource?: string;
  action?: string;
  createdAt: Date;
}

interface UserWithRoles extends User {
  roles: Role[];
  permissions: Permission[];
}
```
