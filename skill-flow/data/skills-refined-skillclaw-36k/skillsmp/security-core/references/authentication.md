# Authentication Patterns

Comprehensive guide to implementing authentication across TypeScript, Python, and Rust applications.

## Table of Contents

1. [Authentication Strategies](#authentication-strategies)
2. [JWT Authentication](#jwt-authentication)
3. [Session-Based Authentication](#session-based-authentication)
4. [OAuth 2.0](#oauth-20)
5. [OAuth for CLI, TUI, and Desktop Apps](#oauth-for-cli-tui-and-desktop-apps)
6. [Multi-Factor Authentication (MFA)](#multi-factor-authentication-mfa)
7. [Password Security](#password-security)
8. [Token Storage Best Practices](#token-storage-best-practices)

## Authentication Strategies

### Choosing an Authentication Method

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| JWT | Stateless APIs, microservices | Scalable, no server-side storage | Can't revoke without blacklist |
| Sessions | Traditional web apps | Easy revocation, simpler | Requires server-side storage |
| OAuth 2.0 | Third-party auth, SSO | Delegated auth, no password handling | Complex implementation |
| API Keys | Service-to-service | Simple, good for services | Not suitable for users |

## JWT Authentication

### JWT Structure

A JWT consists of three parts: Header, Payload, and Signature.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### TypeScript Implementation

**Using `jsonwebtoken` library:**

```typescript
import jwt from 'jsonwebtoken';
import { Effect } from 'effect';

// Generate JWT
interface JWTPayload {
  userId: string;
  email: string;
  role: string;
}

function signToken(payload: JWTPayload, secret: string, expiresIn: string = '1h'): string {
  return jwt.sign(payload, secret, {
    expiresIn,
    algorithm: 'HS256',
    issuer: 'your-app',
  });
}

// Verify JWT with Effect
function verifyToken(token: string, secret: string): Effect.Effect<JWTPayload, Error> {
  return Effect.try({
    try: () => jwt.verify(token, secret) as JWTPayload,
    catch: (error) => new Error(`Token verification failed: ${error}`),
  });
}

// Middleware example (Express)
import { Request, Response, NextFunction } from 'express';

interface AuthRequest extends Request {
  user?: JWTPayload;
}

function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);

  Effect.runPromise(verifyToken(token, process.env.JWT_SECRET!))
    .then((payload) => {
      req.user = payload;
      next();
    })
    .catch((error) => {
      res.status(401).json({ error: 'Invalid token' });
    });
}
```

### Python Implementation (FastAPI)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

class TokenPayload(BaseModel):
    user_id: str
    email: str
    role: str
    exp: datetime

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayload:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Usage in endpoint
@app.get("/protected")
async def protected_route(token: TokenPayload = Depends(verify_token)):
    return {"user_id": token.user_id, "email": token.email}
```

### Rust Implementation (Axum)

```rust
use axum::{
    extract::Extension,
    http::{Request, StatusCode},
    middleware::Next,
    response::Response,
    Json,
};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    email: String,
    role: String,
    exp: usize,
}

struct JwtConfig {
    secret: String,
}

fn create_token(user_id: &str, email: &str, role: &str, secret: &str) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration = chrono::Utc::now()
        .checked_add_signed(chrono::Duration::hours(1))
        .unwrap()
        .timestamp() as usize;

    let claims = Claims {
        sub: user_id.to_owned(),
        email: email.to_owned(),
        role: role.to_owned(),
        exp: expiration,
    };

    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(secret.as_ref()),
    )
}

async fn auth_middleware<B>(
    Extension(config): Extension<Arc<JwtConfig>>,
    mut req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let auth_header = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok());

    let token = auth_header
        .and_then(|h| h.strip_prefix("Bearer "))
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let claims = decode::<Claims>(
        token,
        &DecodingKey::from_secret(config.secret.as_ref()),
        &Validation::default(),
    )
    .map_err(|_| StatusCode::UNAUTHORIZED)?
    .claims;

    req.extensions_mut().insert(claims);

    Ok(next.run(req).await)
}
```

### JWT Best Practices

1. **Use strong secrets** - At least 256 bits (32 bytes) of randomness
2. **Set appropriate expiration** - Short-lived tokens (15 minutes to 1 hour)
3. **Implement refresh tokens** - Long-lived tokens for obtaining new access tokens
4. **Use RS256 for production** - Asymmetric signing is more secure
5. **Never store sensitive data in JWT** - Payload is base64-encoded, not encrypted
6. **Implement token revocation** - Use blacklist or check database for logout
7. **Validate all claims** - Check `exp`, `iss`, `aud` claims

## Session-Based Authentication

### TypeScript Implementation (Express + Redis)

```typescript
import express from 'express';
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({
  url: process.env.REDIS_URL,
});
redisClient.connect();

const app = express();

app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === 'production', // HTTPS only in production
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24, // 24 hours
      sameSite: 'strict',
    },
  })
);

// Login endpoint
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  // Verify credentials (pseudo-code)
  const user = await verifyCredentials(email, password);

  if (user) {
    req.session.userId = user.id;
    req.session.role = user.role;
    res.json({ success: true });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Logout endpoint
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      res.status(500).json({ error: 'Logout failed' });
    } else {
      res.clearCookie('connect.sid');
      res.json({ success: true });
    }
  });
});

// Protected route
app.get('/profile', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  res.json({ userId: req.session.userId });
});
```

### Python Implementation (FastAPI + Redis)

```python
from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from redis import Redis
import secrets
import hashlib

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

SESSION_EXPIRE_SECONDS = 86400  # 24 hours

def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)
    redis_client.setex(f"session:{session_id}", SESSION_EXPIRE_SECONDS, user_id)
    return session_id

def get_session(session_id: str | None) -> str | None:
    if not session_id:
        return None
    user_id = redis_client.get(f"session:{session_id}")
    return user_id

def delete_session(session_id: str):
    redis_client.delete(f"session:{session_id}")

@app.post("/login")
async def login(response: Response, email: str, password: str):
    # Verify credentials (pseudo-code)
    user = await verify_credentials(email, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = create_session(user.id)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="strict",
        max_age=SESSION_EXPIRE_SECONDS,
    )

    return {"success": True}

@app.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(None)):
    if session_id:
        delete_session(session_id)

    response.delete_cookie(key="session_id")
    return {"success": True}

@app.get("/profile")
async def profile(session_id: str | None = Cookie(None)):
    user_id = get_session(session_id)

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"user_id": user_id}
```

## OAuth 2.0

### OAuth 2.0 Flows

**Authorization Code Flow** (most secure, for web apps):
1. User clicks "Login with X"
2. Redirect to provider with client_id and redirect_uri
3. User authenticates and approves
4. Provider redirects back with authorization code
5. Exchange code for access token (server-side)

**PKCE Flow** (for mobile/SPA):
- Extension of Authorization Code Flow
- Uses code_verifier and code_challenge
- No client_secret needed

**Device Flow** (for CLI/TUI/devices):
- See dedicated section below

### TypeScript OAuth Implementation

```typescript
import { Effect } from 'effect';
import axios from 'axios';

interface OAuthConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  authorizationEndpoint: string;
  tokenEndpoint: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  expires_in: number;
  token_type: string;
}

class OAuthClient {
  constructor(private config: OAuthConfig) {}

  getAuthorizationUrl(state: string, scopes: string[]): string {
    const params = new URLSearchParams({
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      response_type: 'code',
      scope: scopes.join(' '),
      state,
    });

    return `${this.config.authorizationEndpoint}?${params.toString()}`;
  }

  exchangeCodeForToken(code: string): Effect.Effect<TokenResponse, Error> {
    return Effect.tryPromise({
      try: async () => {
        const response = await axios.post<TokenResponse>(
          this.config.tokenEndpoint,
          {
            grant_type: 'authorization_code',
            code,
            redirect_uri: this.config.redirectUri,
            client_id: this.config.clientId,
            client_secret: this.config.clientSecret,
          },
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        return response.data;
      },
      catch: (error) => new Error(`Token exchange failed: ${error}`),
    });
  }

  refreshAccessToken(refreshToken: string): Effect.Effect<TokenResponse, Error> {
    return Effect.tryPromise({
      try: async () => {
        const response = await axios.post<TokenResponse>(
          this.config.tokenEndpoint,
          {
            grant_type: 'refresh_token',
            refresh_token: refreshToken,
            client_id: this.config.clientId,
            client_secret: this.config.clientSecret,
          }
        );

        return response.data;
      },
      catch: (error) => new Error(`Token refresh failed: ${error}`),
    });
  }
}
```

## OAuth for CLI, TUI, and Desktop Apps

OAuth authentication for command-line, terminal UI, and desktop applications requires special flows since they can't use traditional browser redirects.

### Device Authorization Flow (OAuth 2.0 Device Flow)

Best for CLI and TUI applications without a browser or with limited input capabilities.

**Flow:**
1. App requests device code from authorization server
2. Server returns device_code, user_code, and verification_uri
3. App displays user_code and verification_uri to user
4. User opens browser, visits URL, enters code
5. App polls token endpoint with device_code
6. Once user approves, app receives access token

### TypeScript CLI Implementation

```typescript
import axios from 'axios';
import { Effect } from 'effect';
import ora from 'ora';
import open from 'open';

interface DeviceCodeResponse {
  device_code: string;
  user_code: string;
  verification_uri: string;
  verification_uri_complete?: string;
  expires_in: number;
  interval: number;
}

interface DeviceTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  scope?: string;
}

class DeviceFlowClient {
  constructor(
    private clientId: string,
    private deviceAuthorizationEndpoint: string,
    private tokenEndpoint: string
  ) {}

  async authenticate(scopes: string[]): Promise<DeviceTokenResponse> {
    // Step 1: Request device code
    const deviceCodeResponse = await this.requestDeviceCode(scopes);

    // Step 2: Display instructions to user
    console.log('\n🔐 Authentication Required\n');
    console.log(`Please visit: ${deviceCodeResponse.verification_uri}`);
    console.log(`And enter code: ${deviceCodeResponse.user_code}\n`);

    // Open browser automatically if complete URI available
    if (deviceCodeResponse.verification_uri_complete) {
      console.log('Opening browser...\n');
      await open(deviceCodeResponse.verification_uri_complete);
    }

    // Step 3: Poll for token
    const spinner = ora('Waiting for authorization...').start();

    try {
      const token = await this.pollForToken(
        deviceCodeResponse.device_code,
        deviceCodeResponse.interval,
        deviceCodeResponse.expires_in
      );

      spinner.succeed('Authentication successful!');
      return token;
    } catch (error) {
      spinner.fail('Authentication failed');
      throw error;
    }
  }

  private async requestDeviceCode(scopes: string[]): Promise<DeviceCodeResponse> {
    const response = await axios.post(
      this.deviceAuthorizationEndpoint,
      {
        client_id: this.clientId,
        scope: scopes.join(' '),
      },
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }
    );

    return response.data;
  }

  private async pollForToken(
    deviceCode: string,
    interval: number,
    expiresIn: number
  ): Promise<DeviceTokenResponse> {
    const pollInterval = interval * 1000;
    const expiresAt = Date.now() + expiresIn * 1000;

    while (Date.now() < expiresAt) {
      await this.sleep(pollInterval);

      try {
        const response = await axios.post(
          this.tokenEndpoint,
          {
            grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
            device_code: deviceCode,
            client_id: this.clientId,
          },
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        return response.data;
      } catch (error: any) {
        if (error.response?.data?.error === 'authorization_pending') {
          // Continue polling
          continue;
        } else if (error.response?.data?.error === 'slow_down') {
          // Increase polling interval
          await this.sleep(5000);
          continue;
        } else {
          throw error;
        }
      }
    }

    throw new Error('Device code expired');
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// Usage
const client = new DeviceFlowClient(
  process.env.CLIENT_ID!,
  'https://oauth.provider.com/device/code',
  'https://oauth.provider.com/token'
);

const token = await client.authenticate(['read', 'write']);
```

### Python CLI Implementation

```python
import requests
import time
import webbrowser
from typing import Dict, List

class DeviceFlowClient:
    def __init__(
        self,
        client_id: str,
        device_authorization_endpoint: str,
        token_endpoint: str
    ):
        self.client_id = client_id
        self.device_authorization_endpoint = device_authorization_endpoint
        self.token_endpoint = token_endpoint

    def authenticate(self, scopes: List[str]) -> Dict[str, str]:
        # Step 1: Request device code
        device_code_response = self._request_device_code(scopes)

        # Step 2: Display instructions
        print("\n🔐 Authentication Required\n")
        print(f"Please visit: {device_code_response['verification_uri']}")
        print(f"And enter code: {device_code_response['user_code']}\n")

        # Open browser if complete URI available
        if 'verification_uri_complete' in device_code_response:
            print("Opening browser...\n")
            webbrowser.open(device_code_response['verification_uri_complete'])

        # Step 3: Poll for token
        print("Waiting for authorization...")
        token = self._poll_for_token(
            device_code_response['device_code'],
            device_code_response.get('interval', 5),
            device_code_response['expires_in']
        )

        print("✅ Authentication successful!")
        return token

    def _request_device_code(self, scopes: List[str]) -> Dict[str, any]:
        response = requests.post(
            self.device_authorization_endpoint,
            data={
                'client_id': self.client_id,
                'scope': ' '.join(scopes)
            }
        )
        response.raise_for_status()
        return response.json()

    def _poll_for_token(
        self,
        device_code: str,
        interval: int,
        expires_in: int
    ) -> Dict[str, str]:
        poll_interval = interval
        expires_at = time.time() + expires_in

        while time.time() < expires_at:
            time.sleep(poll_interval)

            try:
                response = requests.post(
                    self.token_endpoint,
                    data={
                        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                        'device_code': device_code,
                        'client_id': self.client_id
                    }
                )

                if response.status_code == 200:
                    return response.json()

                error = response.json().get('error')

                if error == 'authorization_pending':
                    continue
                elif error == 'slow_down':
                    poll_interval += 5
                    continue
                else:
                    raise Exception(f"Authentication failed: {error}")

            except requests.RequestException as e:
                raise Exception(f"Polling failed: {e}")

        raise Exception("Device code expired")
```

### Rust CLI Implementation

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::time::Duration;
use tokio::time::sleep;

#[derive(Debug, Deserialize)]
struct DeviceCodeResponse {
    device_code: String,
    user_code: String,
    verification_uri: String,
    verification_uri_complete: Option<String>,
    expires_in: u64,
    interval: u64,
}

#[derive(Debug, Deserialize)]
struct TokenResponse {
    access_token: String,
    token_type: String,
    expires_in: u64,
    refresh_token: Option<String>,
}

#[derive(Debug, Deserialize)]
struct TokenError {
    error: String,
}

struct DeviceFlowClient {
    client_id: String,
    device_authorization_endpoint: String,
    token_endpoint: String,
    client: Client,
}

impl DeviceFlowClient {
    pub fn new(
        client_id: String,
        device_authorization_endpoint: String,
        token_endpoint: String,
    ) -> Self {
        Self {
            client_id,
            device_authorization_endpoint,
            token_endpoint,
            client: Client::new(),
        }
    }

    pub async fn authenticate(&self, scopes: Vec<String>) -> Result<TokenResponse, Box<dyn std::error::Error>> {
        // Step 1: Request device code
        let device_code_response = self.request_device_code(scopes).await?;

        // Step 2: Display instructions
        println!("\n🔐 Authentication Required\n");
        println!("Please visit: {}", device_code_response.verification_uri);
        println!("And enter code: {}\n", device_code_response.user_code);

        // Open browser if complete URI available
        if let Some(uri) = &device_code_response.verification_uri_complete {
            println!("Opening browser...\n");
            let _ = open::that(uri);
        }

        // Step 3: Poll for token
        println!("Waiting for authorization...");
        let token = self
            .poll_for_token(
                &device_code_response.device_code,
                device_code_response.interval,
                device_code_response.expires_in,
            )
            .await?;

        println!("✅ Authentication successful!");
        Ok(token)
    }

    async fn request_device_code(&self, scopes: Vec<String>) -> Result<DeviceCodeResponse, Box<dyn std::error::Error>> {
        let response = self
            .client
            .post(&self.device_authorization_endpoint)
            .form(&[
                ("client_id", self.client_id.as_str()),
                ("scope", &scopes.join(" ")),
            ])
            .send()
            .await?
            .json::<DeviceCodeResponse>()
            .await?;

        Ok(response)
    }

    async fn poll_for_token(
        &self,
        device_code: &str,
        interval: u64,
        expires_in: u64,
    ) -> Result<TokenResponse, Box<dyn std::error::Error>> {
        let mut poll_interval = interval;
        let start = std::time::Instant::now();
        let expires_duration = Duration::from_secs(expires_in);

        while start.elapsed() < expires_duration {
            sleep(Duration::from_secs(poll_interval)).await;

            let response = self
                .client
                .post(&self.token_endpoint)
                .form(&[
                    ("grant_type", "urn:ietf:params:oauth:grant-type:device_code"),
                    ("device_code", device_code),
                    ("client_id", &self.client_id),
                ])
                .send()
                .await?;

            if response.status().is_success() {
                return Ok(response.json::<TokenResponse>().await?);
            }

            if let Ok(error) = response.json::<TokenError>().await {
                match error.error.as_str() {
                    "authorization_pending" => continue,
                    "slow_down" => {
                        poll_interval += 5;
                        continue;
                    }
                    _ => return Err(format!("Authentication failed: {}", error.error).into()),
                }
            }
        }

        Err("Device code expired".into())
    }
}
```

### Desktop App OAuth (Electron/Tauri)

For desktop applications with embedded browsers:

**Loopback Method:**
1. Start local HTTP server on `http://localhost:PORT`
2. Open system browser with OAuth URL and redirect_uri=`http://localhost:PORT/callback`
3. User authenticates in browser
4. Browser redirects to localhost callback
5. Local server receives authorization code
6. Exchange code for token
7. Shut down local server

**Security considerations:**
- Use PKCE (Proof Key for Code Exchange)
- Don't embed client_secret in desktop apps
- Use localhost with random port
- Implement proper timeout

## Multi-Factor Authentication (MFA)

### TOTP (Time-based One-Time Password)

```typescript
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

interface MFASetup {
  secret: string;
  qrCodeUrl: string;
}

async function setupMFA(userId: string, email: string): Promise<MFASetup> {
  const secret = speakeasy.generateSecret({
    name: `YourApp (${email})`,
    issuer: 'YourApp',
  });

  const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url!);

  // Store secret in database associated with user
  await database.saveMFASecret(userId, secret.base32);

  return {
    secret: secret.base32,
    qrCodeUrl,
  };
}

function verifyMFAToken(secret: string, token: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2, // Allow 2 time steps (60 seconds) before/after
  });
}
```

### SMS/Email OTP

```typescript
import crypto from 'crypto';

function generateOTP(length: number = 6): string {
  const digits = '0123456789';
  let otp = '';

  for (let i = 0; i < length; i++) {
    const randomIndex = crypto.randomInt(0, digits.length);
    otp += digits[randomIndex];
  }

  return otp;
}

async function sendOTP(userId: string, method: 'sms' | 'email'): Promise<void> {
  const otp = generateOTP();
  const expiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes

  // Store OTP in database or Redis
  await redis.setex(`otp:${userId}`, 300, otp);

  // Send via SMS or email
  if (method === 'sms') {
    await sendSMS(userId, `Your verification code is: ${otp}`);
  } else {
    await sendEmail(userId, `Your verification code is: ${otp}`);
  }
}
```

## Password Security

### Password Hashing

**Never store plain-text passwords!** Always use proper hashing algorithms.

#### TypeScript (bcrypt)

```typescript
import bcrypt from 'bcrypt';
import { Effect } from 'effect';

const SALT_ROUNDS = 12;

function hashPassword(password: string): Effect.Effect<string, Error> {
  return Effect.tryPromise({
    try: () => bcrypt.hash(password, SALT_ROUNDS),
    catch: (error) => new Error(`Password hashing failed: ${error}`),
  });
}

function verifyPassword(password: string, hash: string): Effect.Effect<boolean, Error> {
  return Effect.tryPromise({
    try: () => bcrypt.compare(password, hash),
    catch: (error) => new Error(`Password verification failed: ${error}`),
  });
}
```

#### Python (bcrypt)

```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

#### Rust (argon2)

```rust
use argon2::{
    password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};
use rand::rngs::OsRng;

pub fn hash_password(password: &str) -> Result<String, argon2::password_hash::Error> {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    let password_hash = argon2.hash_password(password.as_bytes(), &salt)?;
    Ok(password_hash.to_string())
}

pub fn verify_password(password: &str, hash: &str) -> Result<bool, argon2::password_hash::Error> {
    let parsed_hash = PasswordHash::new(hash)?;
    Ok(Argon2::default()
        .verify_password(password.as_bytes(), &parsed_hash)
        .is_ok())
}
```

### Password Policy Recommendations

1. **Minimum length**: 12 characters (prefer passphrases)
2. **Complexity**: Don't enforce arbitrary rules (they reduce security)
3. **Check against breach databases**: Use [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3)
4. **Rate limiting**: Prevent brute force attacks
5. **No password hints**: They weaken security
6. **Support password managers**: Allow paste, no max length restrictions

## Token Storage Best Practices

### Web Applications

**✅ Best: HttpOnly Cookies**
```typescript
res.cookie('auth_token', token, {
  httpOnly: true,      // Prevents JavaScript access
  secure: true,        // HTTPS only
  sameSite: 'strict',  // CSRF protection
  maxAge: 3600000,     // 1 hour
});
```

**❌ Bad: localStorage**
- Vulnerable to XSS attacks
- Accessible to any JavaScript code

**❌ Bad: sessionStorage**
- Same XSS vulnerability as localStorage
- Lost on tab close

### Mobile/Desktop Applications

**✅ Best: Secure platform-specific storage**
- iOS: Keychain
- Android: Keystore
- Desktop: OS credential manager (e.g., keytar for Electron)

**❌ Bad: Plain files or shared preferences**
- Can be accessed by other apps or users

### CLI Applications

**✅ Best: OS credential store or encrypted config**
- macOS: Keychain
- Windows: Credential Manager
- Linux: Secret Service API (e.g., gnome-keyring)

**Fallback: Encrypted configuration file**
```typescript
import fs from 'fs/promises';
import crypto from 'crypto';
import os from 'os';
import path from 'path';

const CONFIG_DIR = path.join(os.homedir(), '.your-app');
const TOKEN_FILE = path.join(CONFIG_DIR, 'token.enc');

async function saveToken(token: string, password: string): Promise<void> {
  await fs.mkdir(CONFIG_DIR, { recursive: true, mode: 0o700 });

  const key = crypto.scryptSync(password, 'salt', 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);

  let encrypted = cipher.update(token, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  await fs.writeFile(
    TOKEN_FILE,
    JSON.stringify({ iv: iv.toString('hex'), data: encrypted }),
    { mode: 0o600 }
  );
}
```

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Store passwords with bcrypt/argon2 (never plain text)
- [ ] Use HttpOnly cookies for web tokens
- [ ] Implement CSRF protection
- [ ] Set appropriate token expiration
- [ ] Implement refresh token rotation
- [ ] Add rate limiting to auth endpoints
- [ ] Log authentication events
- [ ] Implement account lockout after failed attempts
- [ ] Use MFA for sensitive operations
- [ ] Validate and sanitize all inputs
- [ ] Keep authentication libraries updated
- [ ] Use secure random for tokens/secrets
- [ ] Implement proper password reset flow
- [ ] Test authentication thoroughly
