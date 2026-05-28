# Auth Specialist

## Patterns


---
  #### **Name**
OAuth 2.1 with PKCE
  #### **Description**
Modern OAuth flow with mandatory PKCE for all clients
  #### **When**
Implementing OAuth/OIDC in any application (web, mobile, or SPA)
  #### **Example**
    import crypto from 'crypto';
    
    // Generate PKCE pair
    function generatePKCE() {
      const verifier = crypto.randomBytes(32)
        .toString('base64url');
      const challenge = crypto
        .createHash('sha256')
        .update(verifier)
        .digest('base64url');
      return { verifier, challenge };
    }
    
    // Authorization request
    const { verifier, challenge } = generatePKCE();
    const authUrl = new URL('https://auth.example.com/authorize');
    authUrl.searchParams.set('client_id', CLIENT_ID);
    authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('scope', 'openid profile email');
    authUrl.searchParams.set('state', crypto.randomUUID());
    authUrl.searchParams.set('code_challenge', challenge);
    authUrl.searchParams.set('code_challenge_method', 'S256');
    
    // Store verifier in session for token exchange
    session.pkceVerifier = verifier;
    
    // Token exchange (server-side)
    const tokenResponse = await fetch('https://auth.example.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code: authorizationCode,
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID,
        code_verifier: session.pkceVerifier,  // PKCE proof
      }),
    });
    

---
  #### **Name**
Refresh Token Rotation
  #### **Description**
Single-use refresh tokens with automatic invalidation
  #### **When**
Implementing token refresh for long-lived sessions
  #### **Example**
    interface TokenFamily {
      familyId: string;
      currentToken: string;
      userId: string;
      createdAt: Date;
      lastUsed: Date;
    }
    
    async function rotateRefreshToken(
      oldRefreshToken: string
    ): Promise<{ accessToken: string; refreshToken: string }> {
      const family = await db.tokenFamilies.findByToken(oldRefreshToken);
    
      if (!family) {
        throw new Error('Invalid refresh token');
      }
    
      // Reuse detection: token already used = compromise
      if (family.currentToken !== oldRefreshToken) {
        // Invalidate entire family - both legitimate user
        // and attacker lose access, forcing re-auth
        await db.tokenFamilies.delete(family.familyId);
        await notifySecurityTeam(family.userId, 'token_reuse_detected');
        throw new Error('Token reuse detected - session invalidated');
      }
    
      // Generate new tokens
      const newRefreshToken = generateSecureToken();
      const accessToken = generateAccessToken(family.userId, {
        expiresIn: '15m',  // Short-lived
      });
    
      // Rotate: update family with new token
      await db.tokenFamilies.update(family.familyId, {
        currentToken: newRefreshToken,
        lastUsed: new Date(),
      });
    
      return { accessToken, refreshToken: newRefreshToken };
    }
    

---
  #### **Name**
Password Hashing with Argon2id
  #### **Description**
Modern memory-hard password hashing with proper parameters
  #### **When**
Storing passwords for local authentication
  #### **Example**
    import argon2 from 'argon2';
    
    // OWASP recommended parameters for Argon2id
    const ARGON2_OPTIONS = {
      type: argon2.argon2id,
      memoryCost: 47104,      // 46 MiB
      timeCost: 1,            // 1 iteration
      parallelism: 1,         // 1 thread
      hashLength: 32,         // 256 bits
    };
    
    async function hashPassword(password: string): Promise<string> {
      // Argon2 includes salt automatically
      return argon2.hash(password, ARGON2_OPTIONS);
    }
    
    async function verifyPassword(
      password: string,
      hash: string
    ): Promise<boolean> {
      try {
        // verify() is constant-time
        return await argon2.verify(hash, password);
      } catch {
        return false;
      }
    }
    
    // Migration from bcrypt
    async function verifyAndMigrate(
      password: string,
      oldHash: string,
      userId: string
    ): Promise<boolean> {
      // Check if it's an old bcrypt hash
      if (oldHash.startsWith('$2')) {
        const valid = await bcrypt.compare(password, oldHash);
        if (valid) {
          // Re-hash with Argon2id on successful login
          const newHash = await hashPassword(password);
          await db.users.updateHash(userId, newHash);
        }
        return valid;
      }
      return argon2.verify(oldHash, password);
    }
    

---
  #### **Name**
JWT Verification with Explicit Algorithm
  #### **Description**
Safe JWT verification that prevents algorithm confusion attacks
  #### **When**
Validating JWTs in your application
  #### **Example**
    import jwt from 'jsonwebtoken';
    
    // CRITICAL: Always specify expected algorithm explicitly
    const JWT_CONFIG = {
      algorithms: ['RS256'] as const,  // NEVER let token header dictate
      issuer: 'https://auth.example.com',
      audience: 'https://api.example.com',
    };
    
    function verifyToken(token: string): TokenPayload {
      // Use verify(), NEVER decode() for validation
      // decode() does NOT verify signature!
      try {
        const payload = jwt.verify(token, PUBLIC_KEY, {
          algorithms: JWT_CONFIG.algorithms,  // Explicit algorithm
          issuer: JWT_CONFIG.issuer,
          audience: JWT_CONFIG.audience,
          complete: false,
        });
        return payload as TokenPayload;
      } catch (error) {
        if (error instanceof jwt.TokenExpiredError) {
          throw new AuthError('TOKEN_EXPIRED');
        }
        if (error instanceof jwt.JsonWebTokenError) {
          throw new AuthError('INVALID_TOKEN');
        }
        throw error;
      }
    }
    
    // For HS256 symmetric signing
    function verifyHmacToken(token: string): TokenPayload {
      return jwt.verify(token, SECRET_KEY, {
        algorithms: ['HS256'],  // Only allow HMAC
        // Blocks: 'none', RS256 (algorithm confusion)
      }) as TokenPayload;
    }
    

---
  #### **Name**
Session Cookie Security Configuration
  #### **Description**
Proper cookie settings for session-based auth
  #### **When**
Using cookies for session management
  #### **Example**
    import session from 'express-session';
    
    const sessionConfig = {
      name: '__Host-session',  // __Host- prefix enforces security
      secret: process.env.SESSION_SECRET!,
      resave: false,
      saveUninitialized: false,
      cookie: {
        httpOnly: true,        // No JS access (XSS protection)
        secure: true,          // HTTPS only (MITM protection)
        sameSite: 'lax',       // CSRF protection
        maxAge: 24 * 60 * 60 * 1000,  // 24 hours
        path: '/',
        domain: undefined,     // Current domain only
      },
      rolling: true,           // Refresh on activity
    };
    
    // For cross-site scenarios (OAuth callbacks), temporarily use:
    // sameSite: 'none', secure: true
    // But revert to 'lax' or 'strict' after auth completes
    

## Anti-Patterns


---
  #### **Name**
JWT in localStorage
  #### **Description**
Storing JWTs in browser localStorage
  #### **Why**
    localStorage is accessible to any JavaScript on the page. A single XSS
    vulnerability exposes all tokens. Unlike cookies, localStorage has no
    expiration, HttpOnly, or SameSite protections.
    
  #### **Instead**
Store in HttpOnly cookies, or keep in memory with refresh via HttpOnly cookie

---
  #### **Name**
Implicit Grant Flow
  #### **Description**
Using OAuth implicit flow (response_type=token)
  #### **Why**
    Deprecated in OAuth 2.1. Access token appears in URL fragment, logged
    in browser history, referrer headers, and proxy logs. No refresh token
    support means repeated full auth flows.
    
  #### **Instead**
Use Authorization Code flow with PKCE for all clients including SPAs

---
  #### **Name**
decode() for Validation
  #### **Description**
Using jwt.decode() thinking it validates the token
  #### **Why**
    decode() only base64-decodes the token. It does NOT verify the signature.
    An attacker can forge any payload and decode() will happily return it.
    This is the #1 JWT implementation mistake.
    
  #### **Instead**
Always use jwt.verify() with explicit algorithm parameter

---
  #### **Name**
Long-Lived Access Tokens
  #### **Description**
Access tokens valid for days or weeks
  #### **Why**
    If compromised, attacker has extended access window. No way to revoke
    without checking a blocklist (defeating stateless benefit). Refresh
    tokens exist specifically to solve this.
    
  #### **Instead**
Access tokens 15-60 minutes max, use refresh token rotation for longevity

---
  #### **Name**
MD5/SHA1 for Passwords
  #### **Description**
Using fast hash algorithms for password storage
  #### **Why**
    MD5 and SHA1 are designed to be fast. Modern GPUs can hash billions
    per second. Password cracking is trivial. These are for integrity
    checking, not password storage.
    
  #### **Instead**
Use Argon2id (preferred) or bcrypt with cost factor 12+

---
  #### **Name**
SMS as Primary MFA
  #### **Description**
Relying on SMS OTP as the main second factor
  #### **Why**
    SS7 vulnerabilities allow SMS interception. SIM swapping is trivial
    with social engineering. Not phishing-resistant - user enters code
    on fake site, attacker replays immediately.
    
  #### **Instead**
TOTP as baseline, WebAuthn/passkeys for high-security flows