# Authentication & OAuth

## Patterns


---
  #### **Name**
OAuth 2.0 Authorization Code Flow
  #### **Description**
    The most secure OAuth flow for server-side apps. User authenticates
    with provider, provider returns code, server exchanges code for tokens.
    
  #### **Example**
    // Step 1: Redirect to OAuth provider
    app.get('/auth/google', (req, res) => {
      const state = crypto.randomBytes(32).toString('hex');
      req.session.oauthState = state;
    
      const params = new URLSearchParams({
        client_id: process.env.GOOGLE_CLIENT_ID,
        redirect_uri: 'https://app.example.com/auth/callback',
        response_type: 'code',
        scope: 'openid email profile',
        state: state,
        // PKCE for extra security
        code_challenge: codeChallenge,
        code_challenge_method: 'S256',
      });
    
      res.redirect(`https://accounts.google.com/o/oauth2/auth?${params}`);
    });
    
    // Step 2: Handle callback
    app.get('/auth/callback', async (req, res) => {
      const { code, state } = req.query;
    
      // Validate state to prevent CSRF
      if (state !== req.session.oauthState) {
        return res.status(403).send('Invalid state');
      }
    
      // Exchange code for tokens
      const tokenResponse = await fetch(
        'https://oauth2.googleapis.com/token',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            code,
            client_id: process.env.GOOGLE_CLIENT_ID,
            client_secret: process.env.GOOGLE_CLIENT_SECRET,
            redirect_uri: 'https://app.example.com/auth/callback',
            grant_type: 'authorization_code',
            code_verifier: codeVerifier,  // PKCE
          }),
        }
      );
    
      const tokens = await tokenResponse.json();
    
      // Validate ID token and extract user info
      const payload = await verifyIdToken(tokens.id_token);
    
      // Create or update user
      const user = await upsertUser({
        email: payload.email,
        name: payload.name,
        googleId: payload.sub,
      });
    
      // Create session
      req.session.userId = user.id;
      res.redirect('/dashboard');
    });
    
  #### **When**
Server-side web applications

---
  #### **Name**
JWT Access + Refresh Token Pattern
  #### **Description**
    Short-lived access tokens for API calls, long-lived refresh tokens
    for getting new access tokens without re-authentication.
    
  #### **Example**
    // Token generation
    function generateTokens(user: User) {
      const accessToken = jwt.sign(
        { sub: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '15m' }  // Short-lived
      );
    
      const refreshToken = jwt.sign(
        { sub: user.id, tokenFamily: crypto.randomUUID() },
        process.env.JWT_REFRESH_SECRET,
        { expiresIn: '7d' }  // Longer-lived
      );
    
      // Store refresh token hash in database
      await db.refreshToken.create({
        data: {
          userId: user.id,
          tokenHash: hashToken(refreshToken),
          expiresAt: addDays(new Date(), 7),
        }
      });
    
      return { accessToken, refreshToken };
    }
    
    // Refresh endpoint
    app.post('/auth/refresh', async (req, res) => {
      const { refreshToken } = req.body;
    
      try {
        const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);
    
        // Check if token exists and not revoked
        const storedToken = await db.refreshToken.findFirst({
          where: {
            tokenHash: hashToken(refreshToken),
            userId: payload.sub,
            revokedAt: null,
          }
        });
    
        if (!storedToken) {
          throw new Error('Token revoked or not found');
        }
    
        // Rotate refresh token (prevents reuse)
        await db.refreshToken.update({
          where: { id: storedToken.id },
          data: { revokedAt: new Date() }
        });
    
        const user = await db.user.findUnique({ where: { id: payload.sub } });
        const tokens = await generateTokens(user);
    
        res.json(tokens);
      } catch (error) {
        res.status(401).json({ error: 'Invalid refresh token' });
      }
    });
    
  #### **When**
API authentication, mobile apps, SPAs

---
  #### **Name**
Secure Session Management
  #### **Description**
    Server-side sessions with secure cookie settings. Session data stays
    on server, only session ID sent to client.
    
  #### **Example**
    import session from 'express-session';
    import RedisStore from 'connect-redis';
    
    app.use(session({
      store: new RedisStore({ client: redisClient }),
      name: 'sessionId',  // Don't use default 'connect.sid'
      secret: process.env.SESSION_SECRET,
      resave: false,
      saveUninitialized: false,
      cookie: {
        secure: true,         // HTTPS only
        httpOnly: true,       // No JavaScript access
        sameSite: 'lax',      // CSRF protection
        maxAge: 24 * 60 * 60 * 1000,  // 24 hours
        domain: '.example.com',  // Subdomain sharing if needed
      },
      // Rotate session ID on login
      genid: () => crypto.randomUUID(),
    }));
    
    // Regenerate session on privilege change
    app.post('/auth/login', async (req, res) => {
      const user = await authenticateUser(req.body);
    
      // Regenerate to prevent session fixation
      req.session.regenerate((err) => {
        req.session.userId = user.id;
        req.session.loginTime = Date.now();
        res.json({ success: true });
      });
    });
    
    // Session timeout with activity tracking
    app.use((req, res, next) => {
      if (req.session.userId) {
        const lastActivity = req.session.lastActivity || 0;
        const now = Date.now();
    
        // Absolute timeout: 24 hours
        if (now - req.session.loginTime > 24 * 60 * 60 * 1000) {
          return req.session.destroy(() => {
            res.status(401).json({ error: 'Session expired' });
          });
        }
    
        // Idle timeout: 30 minutes
        if (now - lastActivity > 30 * 60 * 1000) {
          return req.session.destroy(() => {
            res.status(401).json({ error: 'Session idle timeout' });
          });
        }
    
        req.session.lastActivity = now;
      }
      next();
    });
    
  #### **When**
Traditional web apps, when you control both client and server

---
  #### **Name**
Secure Password Handling
  #### **Description**
    Hash passwords with bcrypt or Argon2, never store plaintext,
    implement secure password reset flow.
    
  #### **Example**
    import bcrypt from 'bcrypt';
    import crypto from 'crypto';
    
    const SALT_ROUNDS = 12;  // Adjust based on hardware
    
    // Hash password on registration
    async function registerUser(email: string, password: string) {
      // Validate password strength first
      if (!isPasswordStrong(password)) {
        throw new Error('Password too weak');
      }
    
      const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    
      return db.user.create({
        data: {
          email: email.toLowerCase().trim(),
          passwordHash,
        }
      });
    }
    
    // Verify password on login
    async function login(email: string, password: string) {
      const user = await db.user.findUnique({
        where: { email: email.toLowerCase().trim() }
      });
    
      if (!user) {
        // Prevent timing attacks - hash anyway
        await bcrypt.hash(password, SALT_ROUNDS);
        throw new Error('Invalid credentials');
      }
    
      const valid = await bcrypt.compare(password, user.passwordHash);
      if (!valid) {
        throw new Error('Invalid credentials');
      }
    
      return user;
    }
    
    // Password reset flow
    async function requestPasswordReset(email: string) {
      const user = await db.user.findUnique({ where: { email } });
    
      // Always return success to prevent email enumeration
      if (!user) return;
    
      const token = crypto.randomBytes(32).toString('hex');
      const tokenHash = crypto.createHash('sha256').update(token).digest('hex');
    
      await db.passwordReset.create({
        data: {
          userId: user.id,
          tokenHash,
          expiresAt: addHours(new Date(), 1),  // 1 hour expiry
        }
      });
    
      await sendEmail(user.email, {
        subject: 'Password Reset',
        body: `Reset link: https://app.example.com/reset?token=${token}`
      });
    }
    
    async function resetPassword(token: string, newPassword: string) {
      const tokenHash = crypto.createHash('sha256').update(token).digest('hex');
    
      const resetRequest = await db.passwordReset.findFirst({
        where: {
          tokenHash,
          expiresAt: { gt: new Date() },
          usedAt: null,
        }
      });
    
      if (!resetRequest) {
        throw new Error('Invalid or expired token');
      }
    
      const passwordHash = await bcrypt.hash(newPassword, SALT_ROUNDS);
    
      await db.$transaction([
        db.user.update({
          where: { id: resetRequest.userId },
          data: { passwordHash }
        }),
        db.passwordReset.update({
          where: { id: resetRequest.id },
          data: { usedAt: new Date() }
        }),
        // Invalidate all sessions
        db.session.deleteMany({
          where: { userId: resetRequest.userId }
        })
      ]);
    }
    
  #### **When**
Email/password authentication

---
  #### **Name**
PKCE for Public Clients
  #### **Description**
    Proof Key for Code Exchange adds security for mobile apps and SPAs
    where client secret cannot be kept confidential.
    
  #### **Example**
    // Generate PKCE values on client
    function generatePKCE() {
      const verifier = base64URLEncode(crypto.getRandomValues(new Uint8Array(32)));
      const challenge = base64URLEncode(
        await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier))
      );
      return { verifier, challenge };
    }
    
    // Store verifier in sessionStorage
    const pkce = generatePKCE();
    sessionStorage.setItem('pkce_verifier', pkce.verifier);
    
    // Include challenge in auth request
    const authUrl = new URL('https://auth.example.com/authorize');
    authUrl.searchParams.set('client_id', CLIENT_ID);
    authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('scope', 'openid profile');
    authUrl.searchParams.set('code_challenge', pkce.challenge);
    authUrl.searchParams.set('code_challenge_method', 'S256');
    
    // On callback, exchange code with verifier
    async function handleCallback(code: string) {
      const verifier = sessionStorage.getItem('pkce_verifier');
      sessionStorage.removeItem('pkce_verifier');
    
      const response = await fetch('https://auth.example.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          grant_type: 'authorization_code',
          code,
          redirect_uri: REDIRECT_URI,
          client_id: CLIENT_ID,
          code_verifier: verifier,
        }),
      });
    
      return response.json();
    }
    
  #### **When**
Mobile apps, SPAs, any public client

---
  #### **Name**
Multi-Factor Authentication
  #### **Description**
    Add second factor with TOTP (authenticator apps), SMS, or security keys.
    TOTP is preferred over SMS.
    
  #### **Example**
    import { authenticator } from 'otplib';
    import QRCode from 'qrcode';
    
    // Generate TOTP secret for user
    async function setupMFA(userId: string) {
      const secret = authenticator.generateSecret();
    
      // Store encrypted secret
      await db.user.update({
        where: { id: userId },
        data: {
          mfaSecret: encrypt(secret),
          mfaEnabled: false,  // Enable after verification
        }
      });
    
      const otpauth = authenticator.keyuri(
        user.email,
        'MyApp',
        secret
      );
    
      // Generate QR code for authenticator app
      const qrCode = await QRCode.toDataURL(otpauth);
    
      return { secret, qrCode };
    }
    
    // Verify and enable MFA
    async function verifyMFASetup(userId: string, code: string) {
      const user = await db.user.findUnique({ where: { id: userId } });
      const secret = decrypt(user.mfaSecret);
    
      if (!authenticator.verify({ token: code, secret })) {
        throw new Error('Invalid code');
      }
    
      // Generate backup codes
      const backupCodes = Array.from({ length: 10 }, () =>
        crypto.randomBytes(4).toString('hex')
      );
    
      await db.user.update({
        where: { id: userId },
        data: {
          mfaEnabled: true,
          backupCodes: backupCodes.map(c => hashCode(c)),
        }
      });
    
      return { backupCodes };  // Show once, user must save
    }
    
    // Login with MFA
    async function loginWithMFA(email: string, password: string, mfaCode: string) {
      const user = await login(email, password);  // First factor
    
      if (user.mfaEnabled) {
        const secret = decrypt(user.mfaSecret);
        const valid = authenticator.verify({ token: mfaCode, secret });
    
        if (!valid) {
          // Check backup codes
          const backupValid = await verifyBackupCode(user.id, mfaCode);
          if (!backupValid) {
            throw new Error('Invalid MFA code');
          }
        }
      }
    
      return user;
    }
    
  #### **When**
High-security applications, user accounts with sensitive data

---
  #### **Name**
Token Storage Best Practices
  #### **Description**
    Choose appropriate storage based on token type and threat model.
    HttpOnly cookies for web, secure storage for mobile.
    
  #### **Example**
    // Web: HttpOnly cookie for refresh token, memory for access token
    // This protects refresh token from XSS while keeping access token available
    
    // Server sets refresh token in HttpOnly cookie
    res.cookie('refreshToken', refreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'strict',
      path: '/auth/refresh',  // Only sent to refresh endpoint
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });
    
    // Access token returned in response body
    res.json({ accessToken });
    
    // Client stores access token in memory (variable, not localStorage)
    let accessToken = null;
    
    async function login(credentials) {
      const response = await fetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
      const data = await response.json();
      accessToken = data.accessToken;  // In-memory only
    }
    
    // Refresh using HttpOnly cookie
    async function refreshAccessToken() {
      const response = await fetch('/auth/refresh', {
        method: 'POST',
        credentials: 'include',  // Send cookies
      });
      const data = await response.json();
      accessToken = data.accessToken;
    }
    
    // Mobile: Use secure storage
    import * as SecureStore from 'expo-secure-store';
    
    await SecureStore.setItemAsync('refreshToken', token);
    const token = await SecureStore.getItemAsync('refreshToken');
    
  #### **When**
Any application storing authentication tokens

## Anti-Patterns


---
  #### **Name**
JWT in localStorage
  #### **Description**
Storing JWT tokens in localStorage
  #### **Why**
    localStorage is accessible via JavaScript. Any XSS vulnerability
    allows attackers to steal tokens. Unlike cookies, localStorage has
    no expiry or httpOnly protection.
    
  #### **Instead**
    - Store access tokens in memory (JavaScript variable)
    - Store refresh tokens in HttpOnly cookies
    - For mobile, use platform secure storage
    

---
  #### **Name**
Long-Lived Access Tokens
  #### **Description**
Access tokens that last hours or days
  #### **Why**
    If stolen, long-lived tokens give attackers extended access.
    Can't revoke access tokens without infrastructure.
    
  #### **Instead**
    - Access tokens: 5-15 minutes
    - Refresh tokens: hours to days (with rotation)
    - Implement token refresh flow
    

---
  #### **Name**
No Session Regeneration
  #### **Description**
Keeping same session ID after login
  #### **Why**
    Session fixation attack - attacker sets session ID before login,
    user logs in with that ID, attacker now has authenticated session.
    
  #### **Instead**
    Always regenerate session ID:
    - On login (unauthenticated → authenticated)
    - On privilege elevation
    - On sensitive operations
    

---
  #### **Name**
Plaintext Password Storage
  #### **Description**
Storing passwords without hashing
  #### **Why**
    Database breach exposes all passwords. Users reuse passwords,
    so breach affects their other accounts too.
    
  #### **Instead**
    - Hash with bcrypt (cost 12+) or Argon2
    - Never encrypt passwords (encryption is reversible)
    - Never use MD5/SHA1 for passwords
    

---
  #### **Name**
Rolling Your Own Auth
  #### **Description**
Implementing authentication from scratch when libraries exist
  #### **Why**
    Auth has many subtle security requirements. Missing one creates
    vulnerabilities. Battle-tested libraries catch edge cases.
    
  #### **Instead**
    Use established libraries:
    - NextAuth.js / Auth.js
    - Passport.js
    - Auth0, Clerk, Supabase Auth
    - Firebase Auth
    

---
  #### **Name**
No OAuth State Parameter
  #### **Description**
OAuth flow without state/nonce validation
  #### **Why**
    Without state validation, attacker can CSRF the callback to link
    their OAuth account to victim's session.
    
  #### **Instead**
    - Generate random state on auth start
    - Store in session
    - Validate on callback
    - Use PKCE for additional protection
    