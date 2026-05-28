---
name: security-review
description: Security review guidance. Use when reviewing code for security vulnerabilities, assessing authentication/authorization, or evaluating data handling.
---

# Security Review

## Focus Areas

- Input validation and sanitization
- Authentication and authorization checks
- SQL injection and parameterized queries
- Cross-site scripting (XSS) prevention
- Cross-site request forgery (CSRF) protection
- Sensitive data exposure
- Security misconfigurations
- Dependency vulnerabilities

## Process

1. Identify all entry points (API endpoints, form inputs, URL parameters)
2. Trace data flow from input to storage/output
3. Check for proper validation at trust boundaries
4. Verify authentication/authorization on protected resources
5. Assess error handling (no sensitive info in errors)
6. Review logging practices (no secrets logged)

# Web Application Security

## Backend (Clojure/Ring)

- Ensure all database queries use parameterized statements
- Verify middleware stack includes security headers
- Check that sessions are properly secured (httpOnly, secure flags)
- Validate that file uploads are restricted and sanitized
- Confirm rate limiting on sensitive endpoints

## Frontend (ClojureScript/Re-frame)

- Sanitize any user content before rendering
- Avoid using `dangerouslySetInnerHTML` or equivalent
- Ensure sensitive data is not stored in localStorage
- Verify API calls include proper authentication tokens
- Check for exposed secrets in client-side code

## Data Handling

- Passwords must be hashed (bcrypt, argon2)
- PII should be encrypted at rest when possible
- Audit logging for sensitive operations
- Proper cleanup of temporary data
