# FastAPI Backend Implementation

Complete guide for protecting FastAPI endpoints with Clerk JWT verification.

## Core Dependencies

```bash
pip install fastapi uvicorn python-jose requests clerk-backend-api python-dotenv
```

## Environment Configuration

Create a `.env` file in your project root:

```bash
# Clerk Configuration
CLERK_SECRET_KEY=sk_test_your_secret_key_here
CLERK_ISSUER=https://your-clerk-instance.clerk.accounts.dev
CLERK_JWKS_URL=https://your-clerk-instance.clerk.accounts.dev/.well-known/jwks.json

# Optional: API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Security Module (auth.py)

This module handles JWKS fetching, token decoding, and user verification.

```python
import os
import requests
import logging
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, jwk
from jose.exceptions import JWTError
from clerk_backend_api import Clerk
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configuration
CLERK_ISSUER = os.getenv("CLERK_ISSUER")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

# Validate required environment variables
if not all([CLERK_ISSUER, CLERK_JWKS_URL, CLERK_SECRET_KEY]):
    raise ValueError("Missing required Clerk environment variables. Please check your .env file.")

# Setup
security = HTTPBearer()
logger = logging.getLogger(__name__)

# Optional: Cache for JWKS to reduce external API calls
_jwks_cache = None

def get_jwks() -> Dict[str, Any]:
    """
    Fetch JSON Web Key Set from Clerk.
    Implements basic caching to reduce API calls.
    """
    global _jwks_cache
    
    # Return cached JWKS if available
    # In production, implement proper caching with TTL
    if _jwks_cache is not None:
        return _jwks_cache
    
    try:
        response = requests.get(CLERK_JWKS_URL, timeout=10)
        response.raise_for_status()
        _jwks_cache = response.json()
        return _jwks_cache
    except requests.RequestException as e:
        logger.error(f"Failed to fetch JWKS: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Unable to verify authentication. Please try again later."
        )

def get_public_key(kid: str, jwks: Dict[str, Any]):
    """
    Find the correct public key from JWKS using the key ID (kid).
    
    Args:
        kid: Key ID from the JWT header
        jwks: JSON Web Key Set containing public keys
        
    Returns:
        Public key for JWT verification
        
    Raises:
        HTTPException: If key ID is not found in JWKS
    """
    for key in jwks.get('keys', []):
        if key.get('kid') == kid:
            return jwk.construct(key)
    
    logger.warning(f"Key ID {kid} not found in JWKS")
    raise HTTPException(
        status_code=401, 
        detail="Invalid token signing key"
    )

async def verify_clerk_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    FastAPI Dependency to verify the Bearer token from Clerk.
    
    This function:
    1. Extracts the JWT token from the Authorization header
    2. Decodes the token header to find the Key ID (kid)
    3. Fetches the appropriate public key from Clerk's JWKS endpoint
    4. Verifies the token signature and claims
    5. Returns the user_id and full payload
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Dictionary containing:
            - user_id: The authenticated user's ID
            - payload: Complete JWT payload with all claims
            
    Raises:
        HTTPException: If token is invalid or verification fails
        
    Example:
        @app.get("/protected")
        async def protected_route(auth_data = Depends(verify_clerk_token)):
            user_id = auth_data["user_id"]
            return {"message": f"Hello, user {user_id}"}
    """
    token = credentials.credentials
    
    try:
        # Step 1: Decode headers to find the Key ID (kid)
        headers = jwt.get_unverified_headers(token)
        kid = headers.get('kid')
        
        if not kid:
            raise HTTPException(
                status_code=401,
                detail="Token missing key ID"
            )
        
        # Step 2: Get the public key from JWKS
        jwks = get_jwks()
        public_key = get_public_key(kid, jwks)
        
        # Step 3: Decode and verify the token
        payload = jwt.decode(
            token,
            public_key.to_pem().decode('utf-8'),
            algorithms=['RS256'],
            audience=None,  # Set if your app uses specific audience
            issuer=CLERK_ISSUER,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_iss": True,
            }
        )
        
        # Step 4: Extract user ID from payload
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in token"
            )
        
        logger.info(f"Successfully authenticated user: {user_id}")
        return {
            "user_id": user_id,
            "payload": payload
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTClaimsError as e:
        logger.warning(f"Invalid token claims: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid token claims"
        )
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    except Exception as e:
        logger.error(f"Unexpected authentication error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Authentication failed"
        )

async def require_role(
    required_role: str,
    auth_data: Dict[str, Any] = Depends(verify_clerk_token)
) -> Dict[str, Any]:
    """
    Dependency to check if user has a specific role.
    
    Args:
        required_role: The role required to access the endpoint
        auth_data: Authenticated user data from verify_clerk_token
        
    Returns:
        auth_data if user has the required role
        
    Raises:
        HTTPException: If user doesn't have the required role
        
    Example:
        from functools import partial
        
        require_admin = partial(require_role, "admin")
        
        @app.get("/admin")
        async def admin_route(auth_data = Depends(require_admin)):
            return {"message": "Admin access granted"}
    """
    roles = auth_data["payload"].get("roles", [])
    
    if required_role not in roles:
        logger.warning(
            f"User {auth_data['user_id']} attempted to access "
            f"resource requiring role '{required_role}'"
        )
        raise HTTPException(
            status_code=403,
            detail=f"'{required_role}' role required"
        )
    
    return auth_data

def get_user_details(user_id: str) -> Dict[str, Any]:
    """
    Fetch complete user profile from Clerk API using the Backend SDK.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        User details dictionary
        
    Example:
        user = get_user_details(auth_data["user_id"])
        print(user.email_addresses[0].email_address)
    """
    try:
        clerk_sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)
        user = clerk_sdk.users.get(user_id=user_id)
        return user
    except Exception as e:
        logger.error(f"Failed to fetch user details: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user details"
        )
```

## Main Application (main.py)

Example FastAPI application with protected routes:

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import verify_clerk_token, require_role, get_user_details
from functools import partial
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Clerk Protected API",
    description="API with Clerk authentication",
    version="1.0.0"
)

# CORS Configuration
# Update with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        # Add your production frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public endpoint (no authentication required)
@app.get("/")
async def root():
    """Public endpoint - no authentication required."""
    return {
        "message": "Welcome to the API",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Protected endpoint - requires authentication
@app.get("/protected")
async def protected_route(auth_data = Depends(verify_clerk_token)):
    """
    Protected endpoint requiring valid Clerk authentication.
    Returns basic user information.
    """
    return {
        "message": "Access granted",
        "user_id": auth_data["user_id"],
        "authenticated": True
    }

# Get current user details
@app.get("/me")
async def get_current_user(auth_data = Depends(verify_clerk_token)):
    """
    Get detailed information about the currently authenticated user.
    """
    user_details = get_user_details(auth_data["user_id"])
    return {
        "user_id": auth_data["user_id"],
        "email": user_details.email_addresses[0].email_address if user_details.email_addresses else None,
        "first_name": user_details.first_name,
        "last_name": user_details.last_name,
        "created_at": user_details.created_at
    }

# Admin-only endpoint
require_admin = partial(require_role, "admin")

@app.get("/admin")
async def admin_route(auth_data = Depends(require_admin)):
    """
    Admin-only endpoint.
    Requires user to have 'admin' role in their token.
    """
    return {
        "message": "Admin access granted",
        "user_id": auth_data["user_id"]
    }

# Example: Protected POST endpoint
@app.post("/api/data")
async def create_data(
    data: dict,
    auth_data = Depends(verify_clerk_token)
):
    """
    Protected POST endpoint example.
    User must be authenticated to create data.
    """
    return {
        "message": "Data created successfully",
        "user_id": auth_data["user_id"],
        "data": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

## Testing Your Implementation

### 1. Using curl

```bash
# Get a token from your frontend first, then:
TOKEN="your_jwt_token_here"

# Test protected endpoint
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/protected

# Test public endpoint (no token needed)
curl http://localhost:8000/

# Test admin endpoint (requires admin role)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/admin
```

### 2. Using Python requests

```python
import requests

# Your JWT token from Clerk
token = "your_jwt_token_here"

headers = {
    "Authorization": f"Bearer {token}"
}

# Test protected endpoint
response = requests.get(
    "http://localhost:8000/protected",
    headers=headers
)
print(response.json())
```

## Advanced Features

### Rate Limiting

```python
from fastapi import Request
from fastapi.responses import JSONResponse
import time
from collections import defaultdict

# Simple in-memory rate limiter
rate_limit_store = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    """
    Simple rate limiting middleware.
    In production, use Redis or similar for distributed rate limiting.
    """
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests (older than 1 minute)
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip]
        if current_time - req_time < 60
    ]
    
    # Check if limit exceeded (e.g., 100 requests per minute)
    if len(rate_limit_store[client_ip]) >= 100:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )
    
    rate_limit_store[client_ip].append(current_time)
    response = await call_next(request)
    return response

app.middleware("http")(rate_limit_middleware)
```

### Request Logging

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing."""
    start_time = time.time()
    
    # Get user_id if available
    user_id = "anonymous"
    if "authorization" in request.headers:
        # You can extract user_id here if needed
        pass
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"User: {user_id} - "
        f"Status: {response.status_code} - "
        f"Duration: {process_time:.3f}s"
    )
    
    return response
```

## Production Considerations

1. **JWKS Caching**: Implement proper caching with TTL for JWKS
2. **Error Monitoring**: Use Sentry or similar for error tracking
3. **Rate Limiting**: Use Redis for distributed rate limiting
4. **Logging**: Implement structured logging
5. **HTTPS**: Always use HTTPS in production
6. **CORS**: Restrict CORS to your specific domains
7. **Token Validation**: Validate all token claims thoroughly
8. **Environment Variables**: Use secrets management (AWS Secrets Manager, etc.)

## Troubleshooting

### Issue: "Failed to fetch JWKS"
**Solution**: Check your CLERK_JWKS_URL and ensure your server can reach Clerk's API

### Issue: "Invalid token signing key"
**Solution**: Verify the token's kid matches a key in your JWKS. Clear JWKS cache if needed.

### Issue: "Token has expired"
**Solution**: Token has expired. User needs to refresh their session on the frontend.

### Issue: "User ID not found in token"
**Solution**: Token is malformed or not from Clerk. Verify the token is being sent correctly.

## Next Steps

- See [react-frontend.md](react-frontend.md) for frontend implementation
- See [user-management.md](user-management.md) for user operations
- See [examples.md](examples.md) for complete working examples
