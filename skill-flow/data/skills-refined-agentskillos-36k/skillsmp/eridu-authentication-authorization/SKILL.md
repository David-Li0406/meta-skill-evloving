---
name: eridu-authentication-authorization
description: Provides general authentication and authorization principles for designing secure systems. This skill should be used when implementing login flows, protecting endpoints, enforcing permissions, or designing API security.
---

# Eridu Services - Authentication & Authorization Skill

Provides general guidance for authentication and authorization across Eridu Services monorepo.

**This skill covers general principles. For implementation details, refer to**:

- **authentication-authorization-backend/SKILL.md** - Backend patterns (validation, authorization, service-to-service)
- **authentication-authorization-frontend/SKILL.md** - Frontend patterns (token storage, protected routes, user context)
- **backend-controller-pattern/SKILL.md** - Controller patterns for protecting endpoints

## General Principles (All Apps)

### Always Protect Sensitive Operations

**Rule**: Require authentication for any operation that:
- Modifies user data
- Accesses user-specific resources
- Changes permissions or roles
- Accesses client/studio-specific data

**Examples**:
- ✅ Public: `/health`, `/api/reference`, login page
- ✅ Authenticated: `/me/*`, dashboard, user profile updates
- ✅ Authorized: `/admin/*`, moderation tools, financial reports

### Validate on Every Access

**Rule**: Don't trust client-sent identifiers

- Backend validates credentials/tokens on every request
- User ID comes from validated credentials, never from URL/body
- Permissions are fetched from authoritative source (database)
- Frontend checks auth status before rendering sensitive content

### Clear Error Messages (For Users)

**Authentication Failures** (401):
- User message: "Invalid credentials"
- Don't reveal: Whether username exists, password requirements

**Authorization Failures** (403):
- User message: "Access denied"
- Don't reveal: What resources exist, which permissions are missing

### Token Security Standards

**Best Practices**:
- ✅ Use industry-standard formats (JWT with RS256/EdDSA)
- ✅ Include token expiration times
- ✅ Implement refresh mechanisms
- ✅ Validate signatures using public keys
- ✅ Use HTTPS/TLS for transmission
- ✅ Store securely (HTTP-only cookies preferred)
- ❌ Never log tokens
- ❌ Never expose in URLs
- ❌ Never hardcode secrets

## Authorization Levels

### Public Access (No Authentication)

**Use when**: Information is freely available to everyone
- Health checks
- API documentation
- Login/registration pages
- Public blog posts

### User Authentication (Logged In)

**Use when**: User must be logged in, but any logged-in user can access
- User profile (`/me`)
- Personal dashboard
- User-specific settings
- History/preferences

### Role-Based Authorization (Admin/Special Role)

**Use when**: Only specific roles can access
- Admin panels (`/admin/*`)
- Moderation tools
- Financial reports
- User management

### Resource-Level Authorization

**Use when**: User owns the resource or has explicit permission
- Edit own comments (not others')
- View client-specific data
- Manage team members
- Update project settings

## Implementation Guidance by Application

### Backend Applications (erify_api, eridu_auth API)

Refer to **authentication-authorization-backend/SKILL.md** for:
- Server-side token validation
- Authorization enforcement
- User context management
- Service-to-service authentication
- Error handling and logging
- Security best practices

Key responsibilities:
- Validate every request
- Enforce permissions
- Log sensitive operations
- Protect credentials

### Frontend Applications (erify_creators, erify_studios, eridu_auth UI)

Refer to **authentication-authorization-frontend/SKILL.md** for:
- Token storage strategies
- Protected route implementation
- User context providers
- Logout flows
- Token refresh mechanisms
- API interceptors

Key responsibilities:
- Store tokens securely
- Redirect to login when needed
- Manage user state
- Handle token expiration

## Related Skills

- **authentication-authorization-backend/SKILL.md** - Backend implementation details
- **authentication-authorization-frontend/SKILL.md** - Frontend implementation details
- **service-pattern/SKILL.md** - Services receive authenticated user context
- **controller-pattern/SKILL.md** - Controllers handle authentication/authorization
- **data-validation/SKILL.md** - Input validation (complement to auth)

## Quick Decision Tree

**Am I building a backend service?**
→ See **authentication-authorization-backend/SKILL.md**
- Validate tokens on every request
- Enforce permissions before processing
- Log sensitive operations

**Am I building a React frontend app?**
→ See **authentication-authorization-frontend/SKILL.md**
- Store tokens securely
- Protect sensitive routes
- Manage user context
- Handle token refresh

**Am I unsure about general principles?**
→ Stay here and read through general principles
- Then go to backend or frontend guide for specifics
