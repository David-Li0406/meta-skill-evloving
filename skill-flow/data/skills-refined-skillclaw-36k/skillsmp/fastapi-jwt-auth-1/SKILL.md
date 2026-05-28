---
name: "fastapi-jwt-auth"
description: "Expert skill for implementing JWT-based authentication in FastAPI applications. Handles token generation, verification, user authentication, protected routes, and security best practices. Includes setup for password hashing, OAuth2 schemes, and user data isolation. Use when implementing JWT authentication in FastAPI applications, securing API endpoints with token-based authentication, or implementing user registration and login functionality."
---

# FastAPI JWT Authentication Skill

## When to Use This Skill

- User wants to implement JWT authentication in FastAPI
- Need to secure API endpoints with token-based authentication
- Want to implement user registration and login functionality
- Looking for OAuth2 password flow implementation
- Need to set up password hashing and verification

## How This Skill Works (Step-by-Step Execution)

1. **Dependency Installation**
   - Install `pyjwt`, `pwdlib[argon2]`, and other required packages
   - Set up environment variables for secret keys

2. **User Model and Database Setup**
   - Create User model with proper fields
   - Set up database connection and session management
   - Implement password hashing utilities

3. **JWT Token Generation**
   - Create token generation function with proper expiration
   - Implement OAuth2PasswordBearer security scheme
   - Add token verification utilities

4. **Authentication Endpoints**
   - Create `/token` endpoint for login
   - Implement user retrieval and validation
   - Add protected route examples

5. **Security Implementation**
   - Add proper error handling for authentication failures
   - Implement user isolation
   - Configure security headers

## Output You Will Receive

After activation, I will deliver:

- Complete dependency installation commands
- User model and database setup
- JWT token generation and verification functions
- Login endpoint with proper error handling
- Protected route examples
- Security best practices and configurations

## Example Usage

**User says:**
"I need to add JWT authentication to my FastAPI application."

**This Skill Instantly Activates → Delivers:**

- Complete dependency setup with `pyjwt` and `pwdlib`
- User model with proper password hashing
- OAuth2 password flow implementation
- Token generation and verification functions
- Protected route examples
- Security best practices

**User says:**
"Secure my API endpoints with JWT tokens in FastAPI."

**This Skill Responds:**
→ Sets up OAuth2PasswordBearer security scheme
→ Creates token generation endpoint
→ Implements JWT verification middleware
→ Provides protected route examples with user isolation

## Activate This Skill By Saying

- "Add JWT authentication to my FastAPI app"
- "Secure my API endpoints with JWT tokens"
- "Implement login and registration in FastAPI"
- "I need OAuth2 password flow in FastAPI"

## Core Implementation Steps

### 1. Install Dependencies
```bash
pip install pyjwt pwdlib[argon2]
```

### 2. User Model and Password Hashing
```python
from pwdlib import PasswordHash
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)
```

### 3. JWT Token Generation
```python
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your-secret-key"  # Use environment variable
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### 4. Authentication Endpoint
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### 5. Protected Route
```python
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```
