---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication System Skill

## Instructions

1. **User Signup**
   - Collect email and password
   - Validate input fields
   - Hash password before saving
   - Store user in database

2. **User Signin**
   - Verify email exists
   - Compare hashed passwords
   - Handle invalid credentials
   - Return auth response

3. **Password Hashing**
   - Use bcrypt or argon2
   - Never store plain text passwords
   - Apply proper salt rounds

4. **JWT Tokens**
   - Generate access token on signin
   - Include user ID in payload
   - Set token expiration
   - Verify token on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Connect with database
   - Use built-in session handling
   - Secure cookies and tokens

## Best Practices
- Always hash passwords
- Use HTTPS only
- Set short token expiry
- Store secrets in environment variables
- Protect all private routes

## Example Flow
```ts
// Signup
User → Hash Password → Save User

// Signin
User → Verify Password → Generate JWT

// Protected Route
Request → Verify JWT → Allow Access
