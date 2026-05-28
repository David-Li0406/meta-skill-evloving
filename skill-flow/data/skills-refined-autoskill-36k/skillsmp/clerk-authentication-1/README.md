# Clerk Authentication Implementation - Claude Skill

A comprehensive Claude Skill for implementing Clerk authentication in full-stack web applications with React frontends and Python/FastAPI backends.

## Overview

This skill provides complete, production-ready implementation patterns for:
- User authentication with JWT verification
- Protected API endpoints
- User management and administration
- Multi-tenant applications with Organizations
- Complete working examples

## Skill Files

### Core Files

1. **SKILL.md** - Main skill definition and overview
   - When to use this skill
   - Core concepts and authentication flow
   - Quick start guide
   - Common use cases and troubleshooting

2. **fastapi-backend.md** - Complete backend implementation
   - FastAPI setup with JWT verification
   - JWKS-based token validation
   - Protected route patterns
   - Error handling and security
   - Rate limiting and logging
   - Production considerations

3. **react-frontend.md** - Complete frontend implementation
   - React setup with Clerk components
   - Protected routes and navigation
   - Making authenticated API requests
   - User profile management
   - Custom styling and theming

4. **user-management.md** - Backend user operations
   - User CRUD operations
   - Metadata management
   - Session management
   - Password verification
   - Admin operations (ban, lock, etc.)

5. **organizations.md** - Multi-tenant features
   - Organization creation and management
   - Member management and roles
   - Invitations system
   - Frontend organization components
   - FastAPI integration

6. **examples.md** - Complete working examples
   - Todo app with authentication
   - Multi-tenant dashboard
   - Complete authentication flow
   - Running instructions

## Quick Start

### For Users Asking Claude

When you need to implement Clerk authentication, simply ask:

```
"Help me implement Clerk authentication for my React and FastAPI app"
```

Claude will:
1. Read the appropriate skill files
2. Provide implementation code
3. Guide you through setup
4. Help troubleshoot issues

### For Skill Developers

To add this skill to your Claude environment:

1. Create a folder: `/mnt/skills/user/clerk-authentication/`

2. Copy all files into the folder:
   ```
   clerk-authentication/
   ├── SKILL.md
   ├── fastapi-backend.md
   ├── react-frontend.md
   ├── user-management.md
   ├── organizations.md
   ├── examples.md
   └── README.md (this file)
   ```

3. Claude will automatically detect and use the skill when relevant

## What Claude Can Help With

### Frontend Implementation
- Setting up Clerk in React, Next.js, Vue, etc.
- Creating sign-in/sign-up pages
- Protecting routes
- Displaying user information
- Making authenticated API requests
- Custom styling

### Backend Implementation
- JWT token verification with JWKS
- Protecting FastAPI endpoints
- User management operations
- Session management
- Role-based access control
- Organization management

### Full-Stack Features
- Complete authentication flows
- Multi-tenant applications
- Admin dashboards
- User profile management
- Invitation systems

## Environment Requirements

### Frontend
- React 18+ (or other supported frameworks)
- @clerk/clerk-react
- Node.js 16+

### Backend
- Python 3.9+
- FastAPI
- python-jose
- requests
- clerk-backend-api

## Key Features

### Security
✅ JWT verification using Clerk's public JWKS
✅ Secure token handling
✅ Rate limiting patterns
✅ Error handling best practices
✅ CORS configuration

### User Management
✅ Complete CRUD operations
✅ Metadata management
✅ Session control
✅ Admin operations
✅ OAuth integration

### Organizations
✅ Multi-tenant support
✅ Role-based access
✅ Member management
✅ Invitation system
✅ Organization switching

### Developer Experience
✅ Type hints and documentation
✅ Error handling
✅ Logging
✅ Testing examples
✅ Production patterns

## Common Use Cases

1. **Protecting an API endpoint:**
   ```python
   from auth import verify_clerk_token
   
   @app.get("/protected")
   async def protected_route(auth_data = Depends(verify_clerk_token)):
       return {"user_id": auth_data["user_id"]}
   ```

2. **Creating a protected React route:**
   ```javascript
   import { useUser, RedirectToSignIn } from '@clerk/clerk-react'
   
   function ProtectedRoute({ children }) {
       const { isSignedIn } = useUser()
       return isSignedIn ? children : <RedirectToSignIn />
   }
   ```

3. **Managing users from backend:**
   ```python
   from clerk_backend_api import Clerk
   
   clerk = Clerk(bearer_auth=SECRET_KEY)
   user = clerk.users.get(user_id="user_123")
   ```

## Troubleshooting

### Token Verification Issues
- Check CLERK_JWKS_URL is correct
- Verify CLERK_ISSUER matches your instance
- Ensure token is being sent in Authorization header

### CORS Errors
- Add frontend URL to CORS configuration
- Check Clerk Dashboard allowed origins

### Import Errors
- Verify all dependencies are installed
- Check Python version (3.9+ required)

## Additional Resources

- [Clerk Official Documentation](https://clerk.com/docs)
- [Clerk Python SDK](https://github.com/clerk/clerk-sdk-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)

## Support

When asking Claude for help:
1. Be specific about your tech stack
2. Share error messages
3. Describe what you're trying to achieve
4. Ask for clarification if needed

## Version

Current Version: 1.0.0
Last Updated: December 2024
Compatible with:
- Clerk Python SDK 4.x
- @clerk/clerk-react 4.x
- FastAPI 0.100+

## Contributing

This skill is maintained as part of Claude's skill system. For updates or improvements, work with Claude to refine the patterns and add new use cases.

## License

This skill documentation is provided as-is for use with Claude. Follow Clerk's licensing for the actual Clerk SDK.
