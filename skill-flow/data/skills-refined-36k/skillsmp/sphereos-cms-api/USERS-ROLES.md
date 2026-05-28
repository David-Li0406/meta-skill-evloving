# Users & Roles

## Create User (Admin Only)

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    email
    firstName
    lastName
    displayName
    isActive
    createdAt
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "newuser@example.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "password": "SecurePassword123"
  }
}
```

## Query All Users

```graphql
query GetUsers($isActive: Boolean) {
  users(isActive: $isActive) {
    id
    email
    firstName
    lastName
    displayName
    isActive
    lastLoginAt
    userRoles {
      role { name }
      organization { name }
    }
  }
}
```

## Query User by ID

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    email
    firstName
    lastName
    displayName
    avatarUrl
    isActive
    userRoles {
      role { name description }
      organization { id name slug }
    }
  }
}
```

## Query Organization Users

```graphql
query GetOrganizationUsers($organizationId: ID!) {
  organizationUsers(organizationId: $organizationId) {
    id
    email
    firstName
    lastName
    isActive
    userRoles { role { name } }
  }
}
```

## Update User

```graphql
mutation UpdateUser($input: UpdateUserInput!) {
  updateUser(input: $input) {
    id
    firstName
    lastName
    displayName
    avatarUrl
    isActive
    updatedAt
  }
}
```

## Deactivate User

```graphql
mutation DeactivateUser($id: ID!) {
  deactivateUser(id: $id) {
    id
    email
    isActive
  }
}
```

## Set User Password

```graphql
mutation SetUserPassword($input: SetPasswordInput!) {
  setUserPassword(input: $input)
}
```

---

## Roles

### Available Roles

| Role | Description |
|------|-------------|
| `SYSTEM_ADMIN` | Full system access |
| `ORG_ADMIN` | Organization administrator |
| `ORG_MEMBER` | Organization member |
| `CONTENT_EDITOR` | Can edit content |
| `VIEWER` | Read-only access |

### Query All Roles

```graphql
query GetRoles {
  roles {
    id
    name
    description
    isSystemRole
  }
}
```

### Assign Role

```graphql
mutation AssignRole($input: AssignRoleInput!) {
  assignRole(input: $input) {
    id
    user { id email }
    role { name }
    organization { id name }
  }
}
```

**Variables:**
```json
{
  "input": {
    "userId": "user_abc123",
    "roleName": "CONTENT_EDITOR",
    "organizationId": "org_abc123"
  }
}
```

### Revoke Role

```graphql
mutation RevokeRole($input: RevokeRoleInput!) {
  revokeRole(input: $input)
}
```

**Variables:**
```json
{
  "input": {
    "userId": "user_abc123",
    "roleName": "CONTENT_EDITOR",
    "organizationId": "org_abc123"
  }
}
```
