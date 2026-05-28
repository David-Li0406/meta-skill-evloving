"""
Better Auth JWT Verification Template

Usage:
1. Copy this file to your project (e.g., app/auth.py)
2. Set BETTER_AUTH_URL environment variable
3. Install dependencies: pip install pyjwt cryptography httpx
4. Use get_current_user as a FastAPI dependency
"""

import os
import time
import httpx
import jwt
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Header, status

# === CONFIGURATION ===
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
JWKS_CACHE_TTL = 300  # 5 minutes


# === USER MODEL ===
@dataclass
class User:
    """User data extracted from JWT.

    Add additional fields as needed based on your JWT claims.
    """

    id: str
    email: str
    name: Optional[str] = None
    # Add custom fields as needed:
    # role: Optional[str] = None
    # organization_id: Optional[str] = None


# === JWKS CACHE ===
@dataclass
class _JWKSCache:
    keys: dict
    expires_at: float


_cache: Optional[_JWKSCache] = None


async def _get_jwks() -> dict:
    """Fetch JWKS from Better Auth server with TTL caching."""
    global _cache

    now = time.time()

    # Return cached keys if still valid
    if _cache and now < _cache.expires_at:
        return _cache.keys

    # Fetch fresh JWKS
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BETTER_AUTH_URL}/.well-known/jwks.json",
            timeout=10.0,
        )
        response.raise_for_status()
        jwks = response.json()

    # Build key lookup by kid
    keys = {}
    for key in jwks.get("keys", []):
        keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(key)

    # Cache the keys
    _cache = _JWKSCache(keys=keys, expires_at=now + JWKS_CACHE_TTL)

    return keys


def clear_jwks_cache():
    """Clear the JWKS cache. Useful for key rotation scenarios."""
    global _cache
    _cache = None


# === TOKEN VERIFICATION ===
async def verify_token(token: str) -> User:
    """Verify JWT and extract user data.

    Args:
        token: JWT token (with or without "Bearer " prefix)

    Returns:
        User object with data from JWT claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Get public keys
        public_keys = await _get_jwks()

        # Get the key ID from the token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid or kid not in public_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify and decode the token
        payload = jwt.decode(
            token,
            public_keys[kid],
            algorithms=["RS256"],
            options={"verify_aud": False},  # Adjust based on your setup
        )

        # Extract user data from claims
        return User(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name"),
            # Add custom claim extraction:
            # role=payload.get("role"),
            # organization_id=payload.get("organization_id"),
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify token - auth server unavailable",
        )


# === FASTAPI DEPENDENCY ===
async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
) -> User:
    """FastAPI dependency to get the current authenticated user.

    Usage:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    return await verify_token(authorization)


# === OPTIONAL: Role-based access ===
def require_role(required_role: str):
    """Dependency factory for role-based access control.

    Usage:
        @app.get("/admin")
        async def admin_route(user: User = Depends(require_role("admin"))):
            return {"admin_id": user.id}
    """

    async def role_checker(user: User = Depends(get_current_user)) -> User:
        # Assumes user has a 'role' attribute from JWT claims
        if not hasattr(user, "role") or user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return user

    return role_checker
