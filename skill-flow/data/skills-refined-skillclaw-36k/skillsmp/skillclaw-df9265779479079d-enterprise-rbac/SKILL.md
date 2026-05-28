---
name: enterprise-rbac
description: Use this skill when configuring enterprise SSO, role-based access control, and organization management across various platforms.
---

# Enterprise RBAC

## Overview
Configure enterprise-grade access control for integrations with various platforms.

## Prerequisites
- Enterprise tier subscription for the platform
- Identity Provider (IdP) with SAML/OIDC support
- Understanding of role-based access patterns
- Audit logging infrastructure

## Role Definitions

| Role | Permissions | Use Case |
|------|-------------|----------|
| Admin | Full access | Platform administrators |
| Developer | Read/write, no delete | Active development |
| Viewer | Read-only | Stakeholders, auditors |
| Service | API access only | Automated systems |

## Role Implementation

```typescript
enum Role {
  Admin = 'admin',
  Developer = 'developer',
  Viewer = 'viewer',
  Service = 'service',
}

interface Permissions {
  read: boolean;
  write: boolean;
  delete: boolean;
  admin: boolean;
}

const ROLE_PERMISSIONS: Record<Role, Permissions> = {
  admin: { read: true, write: true, delete: true, admin: true },
  developer: { read: true, write: true, delete: false, admin: false },
  viewer: { read: true, write: false, delete: false, admin: false },
  service: { read: true, write: true, delete: false, admin: false },
};

function checkPermission(
  role: Role,
  action: keyof Permissions
): boolean {
  return ROLE_PERMISSIONS[role][action];
}
```

## SSO Integration

### SAML Configuration

```typescript
// SAML setup
const samlConfig = {
  entryPoint: 'https://idp.company.com/saml/sso',
  issuer: 'https://yourplatform.com/saml/metadata',
  cert: process.env.SAML_CERT,
  callbackUrl: 'https://app.yourcompany.com/auth/callback',
};

// Map IdP groups to roles
const groupRoleMapping: Record<string, Role> = {
  'Engineering': Role.Developer,
  'Platform-Admins': Role.Admin,
  'Data-Team': Role.Viewer,
};
```

### OAuth2/OIDC Integration

```typescript
import { OAuth2Client } from '@yourplatform/sdk';

const oauthClient = new OAuth2Client({
  clientId: process.env.OAUTH_CLIENT_ID!,
  clientSecret: process.env.OAUTH_CLIENT_SECRET!,
});
```