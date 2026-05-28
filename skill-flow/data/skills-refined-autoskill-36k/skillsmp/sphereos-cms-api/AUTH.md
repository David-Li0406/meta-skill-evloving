# Authentication

## Login

```graphql
mutation Login($input: LoginInput!) {
  login(input: $input) {
    accessToken
    refreshToken
    user {
      id
      email
      firstName
      lastName
      displayName
      isActive
      userRoles {
        id
        role { name description }
        organization { id name slug }
      }
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "admin@example.com",
    "password": "SecurePassword123"
  }
}
```

## Refresh Token

```graphql
mutation RefreshToken($refreshToken: String!) {
  refreshToken(refreshToken: $refreshToken) {
    accessToken
    refreshToken
  }
}
```

## Logout

```graphql
mutation Logout($refreshToken: String!) {
  logout(refreshToken: $refreshToken)
}
```

## Logout All Devices

```graphql
mutation LogoutAllDevices {
  logoutAllDevices
}
```

## Get Current User

```graphql
query Me {
  me {
    id
    email
    firstName
    lastName
    displayName
    avatarUrl
    isActive
    lastLoginAt
    createdAt
    userRoles {
      role { name description isSystemRole }
      organization { id name slug }
    }
  }
}
```

## Change Password

```graphql
mutation ChangePassword($input: ChangePasswordInput!) {
  changePassword(input: $input)
}
```

**Variables:**
```json
{
  "input": {
    "currentPassword": "OldPassword123",
    "newPassword": "NewSecurePassword456"
  }
}
```

## Update My Profile

```graphql
mutation UpdateMyProfile($input: UpdateUserInput!) {
  updateMyProfile(input: $input) {
    id
    firstName
    lastName
    displayName
    avatarUrl
    updatedAt
  }
}
```
