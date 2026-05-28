# Authentication & Authorization Patterns

## Overview

Authentication verifies identity ("who are you?"). Authorization determines access ("what can you do?"). Both are critical security layers.

---

## Authentication Patterns

### Session-Based Authentication

Traditional server-side sessions.

```
1. User submits credentials
2. Server validates, creates session
3. Server stores session in memory/database/Redis
4. Server sends session ID in cookie
5. Client sends cookie with every request
6. Server looks up session, validates user
```

**Pros:**
- Easy to implement
- Easy to invalidate (delete session)
- Server controls session completely

**Cons:**
- Requires server-side storage
- Harder to scale (sticky sessions or shared storage)
- CSRF protection needed

```python
# Session configuration
SESSION_CONFIG = {
    "secret_key": os.environ["SESSION_SECRET"],  # From env!
    "cookie_name": "session_id",
    "cookie_secure": True,       # HTTPS only
    "cookie_httponly": True,     # No JavaScript access
    "cookie_samesite": "Lax",    # CSRF protection
    "session_lifetime": 3600,    # 1 hour
}

# Login flow
def login(email, password):
    user = User.verify_credentials(email, password)
    if not user:
        log_failed_login(email)
        raise AuthenticationError("Invalid credentials")

    # Create new session
    session_id = create_session(user.id)

    # Set cookie
    response.set_cookie(
        "session_id",
        session_id,
        secure=True,
        httponly=True,
        samesite="Lax",
        max_age=3600,
    )

    log_successful_login(user.id)
    return user

# Authentication middleware
def require_auth(func):
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise AuthenticationError("Not authenticated")

        session = get_session(session_id)
        if not session or session.is_expired:
            raise AuthenticationError("Session expired")

        # Attach user to request context
        g.user = User.get(session.user_id)
        return func(*args, **kwargs)
    return wrapper
```

---

### JWT (JSON Web Token) Authentication

Stateless token-based authentication.

```
1. User submits credentials
2. Server validates, creates signed JWT
3. Server sends JWT to client
4. Client stores JWT (localStorage, memory)
5. Client sends JWT in Authorization header
6. Server validates JWT signature, extracts claims
```

**Pros:**
- Stateless (no server storage needed)
- Scales easily
- Works well for APIs and microservices

**Cons:**
- Cannot invalidate until expiration (use short-lived + refresh tokens)
- Token theft is dangerous
- Larger than session IDs

```python
import jwt
from datetime import datetime, timedelta

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)

def create_access_token(user_id: str) -> str:
    """Create short-lived access token."""
    payload = {
        "sub": user_id,
        "type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    """Create long-lived refresh token."""
    token_id = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": token_id,  # Token ID for revocation
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + REFRESH_TOKEN_LIFETIME,
    }
    # Store token_id in database for revocation
    store_refresh_token(user_id, token_id)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_access_token(token: str) -> dict:
    """Verify and decode access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Not an access token")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

# Usage in request
def require_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationError("Missing token")

        token = auth_header.split(" ")[1]
        payload = verify_access_token(token)
        g.user_id = payload["sub"]
        return func(*args, **kwargs)
    return wrapper
```

---

### OAuth 2.0 / OpenID Connect

Delegated authentication via third-party providers.

```
1. User clicks "Login with Google"
2. Redirect to provider's auth page
3. User authenticates with provider
4. Provider redirects back with authorization code
5. Server exchanges code for tokens
6. Server gets user info from provider
7. Server creates local session/JWT
```

```python
# OAuth 2.0 flow (simplified)
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()

    # Find or create local user
    user = User.find_or_create_by_oauth(
        provider='google',
        provider_id=user_info['id'],
        email=user_info['email'],
        name=user_info['name'],
    )

    # Create local session
    return create_session_response(user)
```

---

## Authorization Patterns

### Role-Based Access Control (RBAC)

Users have roles, roles have permissions.

```python
# Define roles and permissions
ROLES = {
    "admin": ["read", "write", "delete", "manage_users"],
    "editor": ["read", "write"],
    "viewer": ["read"],
}

class User:
    def __init__(self, id, roles):
        self.id = id
        self.roles = roles  # e.g., ["editor"]

    def has_permission(self, permission: str) -> bool:
        """Check if user has permission via any of their roles."""
        for role in self.roles:
            if permission in ROLES.get(role, []):
                return True
        return False

# Authorization decorator
def require_permission(permission: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not g.user.has_permission(permission):
                raise AuthorizationError(f"Permission denied: {permission}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.route('/api/articles', methods=['POST'])
@require_auth
@require_permission('write')
def create_article():
    # Only users with 'write' permission can access
    ...
```

---

### Attribute-Based Access Control (ABAC)

Decisions based on attributes of user, resource, and environment.

```python
def can_access_document(user, document, action):
    """
    ABAC policy evaluation.
    Consider: user attributes, resource attributes, environment.
    """
    # User is owner
    if document.owner_id == user.id:
        return True

    # User is in document's team
    if user.team_id == document.team_id:
        if action == "read":
            return True
        if action == "write" and user.role in ["admin", "editor"]:
            return True

    # Document is public
    if document.is_public and action == "read":
        return True

    # Admin override
    if user.is_admin:
        return True

    return False

# Usage
@app.route('/api/documents/<doc_id>')
@require_auth
def get_document(doc_id):
    document = Document.get(doc_id)
    if not can_access_document(g.user, document, "read"):
        raise AuthorizationError("Access denied")
    return document.to_dict()
```

---

### Resource-Based Authorization

Check ownership/access on every resource access.

```python
@app.route('/api/posts/<post_id>', methods=['PUT'])
@require_auth
def update_post(post_id):
    post = Post.get(post_id)

    if not post:
        raise NotFoundError("Post not found")

    # Check ownership
    if post.author_id != g.user.id:
        # Check if admin
        if not g.user.is_admin:
            raise AuthorizationError("Cannot edit others' posts")

    # Proceed with update
    post.update(request.json)
    return post.to_dict()
```

---

## Password Security

### Password Requirements

```python
import re
from typing import Tuple, List

def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password strength.
    Following NIST SP 800-63B guidelines.
    """
    issues = []

    # Minimum length (primary requirement)
    if len(password) < 12:
        issues.append("Password must be at least 12 characters")

    # Maximum length (prevent DoS)
    if len(password) > 128:
        issues.append("Password must be at most 128 characters")

    # Check common passwords
    if password.lower() in load_common_passwords():
        issues.append("Password is too common")

    # Check for user-specific data (email, name)
    # Would need user context to check this

    return len(issues) == 0, issues
```

### Password Hashing

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password with bcrypt."""
    # Cost factor 12 = ~250ms on modern hardware
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )

# Alternative: Argon2 (newer, recommended)
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=65536,  # 64 MB
    parallelism=1,
)

def hash_password_argon2(password: str) -> str:
    return ph.hash(password)

def verify_password_argon2(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except:
        return False
```

---

## Multi-Factor Authentication

### TOTP (Time-based One-Time Password)

```python
import pyotp

def setup_mfa(user_id: str) -> dict:
    """Initialize MFA for user."""
    # Generate secret
    secret = pyotp.random_base32()

    # Store secret (encrypted!) for user
    store_mfa_secret(user_id, secret)

    # Generate provisioning URI for authenticator apps
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="MyApp"
    )

    return {
        "secret": secret,  # Show once for manual entry
        "uri": uri,        # For QR code
    }

def verify_mfa(user_id: str, code: str) -> bool:
    """Verify MFA code."""
    secret = get_mfa_secret(user_id)
    totp = pyotp.TOTP(secret)

    # valid_window allows for clock skew (1 period = 30 seconds)
    return totp.verify(code, valid_window=1)

# Login flow with MFA
def login_with_mfa(email: str, password: str, mfa_code: str = None):
    user = User.verify_credentials(email, password)
    if not user:
        raise AuthenticationError("Invalid credentials")

    if user.mfa_enabled:
        if not mfa_code:
            raise MFARequiredError("MFA code required")
        if not verify_mfa(user.id, mfa_code):
            raise AuthenticationError("Invalid MFA code")

    return create_session(user)
```

---

## Session Security

### Session Configuration

```python
SESSION_CONFIG = {
    # Secure cookie settings
    "cookie_secure": True,        # HTTPS only
    "cookie_httponly": True,      # No JavaScript access
    "cookie_samesite": "Lax",     # CSRF protection

    # Session lifetime
    "absolute_timeout": 8 * 3600,  # 8 hours max
    "idle_timeout": 1800,          # 30 min of inactivity

    # Security
    "regenerate_on_auth": True,    # Prevent session fixation
    "bind_to_ip": False,           # Can break for mobile users
    "bind_to_user_agent": True,    # Basic fingerprinting
}
```

### Session Fixation Prevention

```python
def login(email: str, password: str):
    user = User.verify_credentials(email, password)
    if not user:
        raise AuthenticationError("Invalid credentials")

    # IMPORTANT: Regenerate session ID after authentication
    # Prevents session fixation attacks
    old_session_id = request.cookies.get("session_id")
    if old_session_id:
        invalidate_session(old_session_id)

    # Create new session with new ID
    new_session_id = create_session(user.id)
    return set_session_cookie(new_session_id)
```

### Session Invalidation

```python
def logout():
    """Logout and invalidate session."""
    session_id = request.cookies.get("session_id")
    if session_id:
        invalidate_session(session_id)

    response = make_response(redirect('/'))
    response.delete_cookie("session_id")
    return response

def logout_all_sessions(user_id: str):
    """Logout user from all devices."""
    invalidate_all_sessions(user_id)

def password_changed(user_id: str):
    """Invalidate all sessions when password changes."""
    invalidate_all_sessions(user_id)
```

---

## Brute Force Protection

```python
from datetime import datetime, timedelta
from collections import defaultdict

# In-memory store (use Redis in production)
failed_attempts = defaultdict(list)
lockouts = {}

MAX_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)
ATTEMPT_WINDOW = timedelta(minutes=5)

def check_lockout(identifier: str) -> bool:
    """Check if identifier (email/IP) is locked out."""
    if identifier in lockouts:
        if datetime.utcnow() < lockouts[identifier]:
            return True
        else:
            del lockouts[identifier]
    return False

def record_failed_attempt(identifier: str):
    """Record failed login attempt."""
    now = datetime.utcnow()

    # Clean old attempts
    cutoff = now - ATTEMPT_WINDOW
    failed_attempts[identifier] = [
        t for t in failed_attempts[identifier]
        if t > cutoff
    ]

    # Add new attempt
    failed_attempts[identifier].append(now)

    # Check if should lock out
    if len(failed_attempts[identifier]) >= MAX_ATTEMPTS:
        lockouts[identifier] = now + LOCKOUT_DURATION
        log_security_event("account_locked", identifier)

def clear_failed_attempts(identifier: str):
    """Clear failed attempts on successful login."""
    failed_attempts.pop(identifier, None)
    lockouts.pop(identifier, None)

# Usage in login
def login(email: str, password: str):
    if check_lockout(email):
        raise RateLimitError("Account temporarily locked. Try again later.")

    user = User.verify_credentials(email, password)
    if not user:
        record_failed_attempt(email)
        raise AuthenticationError("Invalid credentials")

    clear_failed_attempts(email)
    return create_session(user)
```

---

## Quick Reference

### Checklist

- [ ] Passwords hashed with bcrypt/Argon2 (cost factor 12+)
- [ ] Session cookies: Secure, HttpOnly, SameSite
- [ ] Session regenerated on login
- [ ] Brute force protection implemented
- [ ] MFA available for sensitive accounts
- [ ] Authorization checked on every request
- [ ] Failed auth attempts logged
- [ ] Password reset tokens single-use and time-limited
- [ ] JWT refresh tokens stored securely and revocable
