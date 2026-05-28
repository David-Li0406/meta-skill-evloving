# JWT Verification Examples

Complete examples for verifying Better Auth JWTs in Python.

## Basic JWT Verification

```python
# app/auth.py
import os
import httpx
import jwt
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Header, status

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")


@dataclass
class User:
    """User data extracted from JWT."""
    id: str
    email: str
    name: Optional[str] = None


# JWKS cache
_jwks_cache: dict = {}


async def get_jwks() -> dict:
    """Fetch JWKS from Better Auth server with caching."""
    global _jwks_cache

    if not _jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BETTER_AUTH_URL}/.well-known/jwks.json")
            response.raise_for_status()
            _jwks_cache = response.json()

    return _jwks_cache


async def verify_token(token: str) -> User:
    """Verify JWT and extract user data."""
    try:
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Get JWKS
        jwks = await get_jwks()
        public_keys = {}

        for key in jwks.get("keys", []):
            public_keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        # Get the key ID from the token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid or kid not in public_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key"
            )

        # Verify and decode
        payload = jwt.decode(
            token,
            public_keys[kid],
            algorithms=["RS256"],
            options={"verify_aud": False}  # Adjust based on your setup
        )

        return User(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name"),
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user(
    authorization: str = Header(..., alias="Authorization")
) -> User:
    """FastAPI dependency to get current authenticated user."""
    return await verify_token(authorization)
```

## Session-Based Verification (Alternative)

```python
# app/auth.py - Alternative using session API
import os
import httpx
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Request, status

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")


@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None


async def get_current_user(request: Request) -> User:
    """Verify session by calling Better Auth API."""
    cookies = request.cookies

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BETTER_AUTH_URL}/api/auth/get-session",
            cookies=cookies,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session"
            )

        data = response.json()
        user_data = data.get("user", {})

        return User(
            id=user_data.get("id"),
            email=user_data.get("email"),
            name=user_data.get("name"),
        )
```

## JWKS with TTL Cache

```python
# app/auth.py - Production-ready with proper caching
import os
import time
import httpx
import jwt
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Header, status

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
JWKS_CACHE_TTL = 300  # 5 minutes


@dataclass
class JWKSCache:
    keys: dict
    expires_at: float


_cache: Optional[JWKSCache] = None


async def get_jwks() -> dict:
    """Fetch JWKS with TTL-based caching."""
    global _cache

    now = time.time()

    if _cache and now < _cache.expires_at:
        return _cache.keys

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BETTER_AUTH_URL}/.well-known/jwks.json",
            timeout=10.0
        )
        response.raise_for_status()
        jwks = response.json()

        # Build key lookup
        keys = {}
        for key in jwks.get("keys", []):
            keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        _cache = JWKSCache(
            keys=keys,
            expires_at=now + JWKS_CACHE_TTL
        )

        return keys


def clear_jwks_cache():
    """Clear the JWKS cache (useful for key rotation)."""
    global _cache
    _cache = None
```

## Custom Claims Extraction

```python
@dataclass
class User:
    """User with custom claims from JWT."""
    id: str
    email: str
    name: Optional[str] = None
    role: Optional[str] = None
    organization_id: Optional[str] = None
    permissions: list[str] = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []


async def verify_token(token: str) -> User:
    """Verify JWT and extract user data with custom claims."""
    # ... verification logic ...

    payload = jwt.decode(token, public_keys[kid], algorithms=["RS256"])

    return User(
        id=payload.get("sub"),
        email=payload.get("email"),
        name=payload.get("name"),
        role=payload.get("role"),
        organization_id=payload.get("organization_id"),
        permissions=payload.get("permissions", []),
    )
```

## Synchronous Version (Non-Async)

```python
# app/auth_sync.py - For sync FastAPI routes
import os
import requests
import jwt
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Header, status

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

_jwks_cache: dict = {}


def get_jwks_sync() -> dict:
    """Fetch JWKS synchronously."""
    global _jwks_cache

    if not _jwks_cache:
        response = requests.get(
            f"{BETTER_AUTH_URL}/.well-known/jwks.json",
            timeout=10
        )
        response.raise_for_status()
        _jwks_cache = response.json()

    return _jwks_cache


def verify_token_sync(token: str) -> User:
    """Verify JWT synchronously."""
    try:
        if token.startswith("Bearer "):
            token = token[7:]

        jwks = get_jwks_sync()
        public_keys = {}

        for key in jwks.get("keys", []):
            public_keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid or kid not in public_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key"
            )

        payload = jwt.decode(
            token,
            public_keys[kid],
            algorithms=["RS256"],
            options={"verify_aud": False}
        )

        return User(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name"),
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


def get_current_user_sync(
    authorization: str = Header(..., alias="Authorization")
) -> User:
    """FastAPI dependency for sync routes."""
    return verify_token_sync(authorization)
```

## Error Handling Patterns

```python
from enum import Enum


class AuthError(str, Enum):
    TOKEN_MISSING = "token_missing"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_INVALID = "token_invalid"
    TOKEN_MALFORMED = "token_malformed"
    JWKS_UNAVAILABLE = "jwks_unavailable"


class AuthException(HTTPException):
    """Custom auth exception with error codes."""

    def __init__(self, error: AuthError, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": error.value, "message": detail},
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_token(token: str) -> User:
    """Verify JWT with detailed error responses."""
    if not token:
        raise AuthException(AuthError.TOKEN_MISSING, "Authorization header required")

    try:
        if token.startswith("Bearer "):
            token = token[7:]

        jwks = await get_jwks()
        # ... rest of verification

    except httpx.HTTPError:
        raise AuthException(
            AuthError.JWKS_UNAVAILABLE,
            "Unable to verify token - auth server unavailable"
        )
    except jwt.ExpiredSignatureError:
        raise AuthException(AuthError.TOKEN_EXPIRED, "Token has expired")
    except jwt.DecodeError:
        raise AuthException(AuthError.TOKEN_MALFORMED, "Token is malformed")
    except jwt.InvalidTokenError as e:
        raise AuthException(AuthError.TOKEN_INVALID, str(e))
```
