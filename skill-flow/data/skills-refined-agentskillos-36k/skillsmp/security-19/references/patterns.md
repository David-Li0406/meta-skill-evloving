# Security

## Patterns


---
  #### **Name**
Defense in Depth
  #### **Description**
Multiple security layers so single failure doesn't cause breach
  #### **When**
Architecting any system that handles sensitive data
  #### **Example**
    Layer 1: Rate limiting at edge
    Layer 2: Authentication required
    Layer 3: Authorization checks per resource
    Layer 4: Input validation and sanitization
    Layer 5: Parameterized queries
    Layer 6: Audit logging
    

---
  #### **Name**
Fail Secure by Default
  #### **Description**
When errors occur, deny access rather than allowing
  #### **When**
Implementing any authorization or security check
  #### **Example**
    function canAccess(user, resource) {
      try {
        const permissions = getPermissions(user);
        return permissions.includes(resource.requiredPermission);
      } catch (error) {
        logSecurityEvent('permission_check_failed', { user, resource, error });
        return false; // Deny on error
      }
    }
    

---
  #### **Name**
Security Headers on All Responses
  #### **Description**
Set security headers to prevent common attacks
  #### **When**
Configuring web application middleware
  #### **Example**
    headers: {
      'Content-Security-Policy': "default-src 'self'",
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Strict-Transport-Security': 'max-age=31536000',
      'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    

---
  #### **Name**
Parameterized Queries Always
  #### **Description**
Never concatenate user input into SQL or database queries
  #### **When**
Any database interaction with user input
  #### **Example**
    // Safe
    const user = await db.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );
    
    // Unsafe - SQL injection
    const user = await db.query(
      `SELECT * FROM users WHERE id = ${userId}`
    );
    

---
  #### **Name**
Secrets in Environment, Never in Code
  #### **Description**
All API keys, tokens, passwords in environment variables
  #### **When**
Configuring any external service integration
  #### **Example**
    # .env (gitignored)
    DATABASE_URL=postgresql://...
    STRIPE_SECRET_KEY=sk_live_...
    
    # .env.example (checked in)
    DATABASE_URL=
    STRIPE_SECRET_KEY=
    
    # Validate at startup
    if (!process.env.STRIPE_SECRET_KEY) {
      throw new Error('STRIPE_SECRET_KEY required');
    }
    

---
  #### **Name**
Rate Limiting by User and IP
  #### **Description**
Prevent brute force and abuse with rate limits
  #### **When**
Any authentication endpoint or expensive operation
  #### **Example**
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 5, // 5 attempts
      keyGenerator: (req) => req.user?.id || req.ip,
      skipSuccessfulRequests: true
    });
    
    app.post('/login', limiter, loginHandler);
    

## Anti-Patterns


---
  #### **Name**
Client-Side Security
  #### **Description**
Relying on client-side validation or hiding for security
  #### **Why**
Client can be modified, bypassed, or inspected by attacker
  #### **Instead**
    Client-side validation is UX, not security.
    Always validate, authorize, and sanitize server-side.
    Assume client is hostile.
    

---
  #### **Name**
Security Through Obscurity
  #### **Description**
Hiding implementation details as primary security measure
  #### **Why**
Obscurity will be discovered, must be secure even when public
  #### **Instead**
    Design as if attacker has source code.
    Use real security: authentication, encryption, signing.
    Obscurity is defense-in-depth layer, never primary.
    

---
  #### **Name**
Ignoring OWASP Top 10
  #### **Description**
Not checking code against known vulnerability patterns
  #### **Why**
These are the most common ways applications get breached
  #### **Instead**
    Review OWASP Top 10 annually.
    Use automated scanners (SAST/DAST).
    Security testing in CI/CD.
    

---
  #### **Name**
Logging Sensitive Data
  #### **Description**
Writing passwords, tokens, PII to logs
  #### **Why**
Logs are often less secured than database, compliance violation
  #### **Instead**
    Redact sensitive fields before logging.
    Log security events, not security credentials.
    Never log: passwords, tokens, full credit cards, SSNs.
    

---
  #### **Name**
Rolling Your Own Crypto
  #### **Description**
Implementing custom encryption or hashing algorithms
  #### **Why**
Cryptography is hard, experts make mistakes, you will too
  #### **Instead**
    Use battle-tested libraries: bcrypt, scrypt, Argon2.
    Use platform crypto APIs: Web Crypto, Node crypto.
    Never implement encryption yourself.
    

---
  #### **Name**
No Security in Development
  #### **Description**
Disabling security features in development environment
  #### **Why**
Security bugs ship to production when not caught early
  #### **Instead**
    Test with security enabled.
    Use development API keys, not disabled security.
    Security should be frictionless, not disabled.
    