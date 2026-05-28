# Complete FastAPI Authentication Server Example
# Install: pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Auth API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )
    return conn

# Pydantic Models
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    emailVerified: bool

class AuthResponse(BaseModel):
    user: UserResponse
    token: str

class RoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]

# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("userId")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id, email, name, email_verified FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()

        if user is None:
            raise credentials_exception

        return dict(user)
    finally:
        cur.close()
        conn.close()

# Routes

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignUpRequest):
    # Validation
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if user exists
        cur.execute("SELECT id FROM users WHERE email = %s", (data.email,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")

        # Begin transaction
        conn.autocommit = False

        # Create user
        cur.execute(
            """INSERT INTO users (email, name, email_verified)
               VALUES (%s, %s, %s) RETURNING id, email, name, email_verified, created_at""",
            (data.email, data.name, False)
        )
        user = cur.fetchone()

        # Hash and store password
        hashed_password = get_password_hash(data.password)
        cur.execute(
            "INSERT INTO passwords (user_id, hashed_password) VALUES (%s, %s)",
            (user["id"], hashed_password)
        )

        # Assign default user role
        cur.execute("SELECT id FROM roles WHERE name = %s", ("user",))
        role = cur.fetchone()
        if role:
            cur.execute(
                "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)",
                (user["id"], role["id"])
            )

        conn.commit()

        # Generate JWT token
        token = create_access_token({"userId": user["id"]})

        return {
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "emailVerified": user["email_verified"],
            },
            "token": token,
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cur.close()
        conn.close()

@app.post("/api/auth/signin", response_model=AuthResponse)
async def signin(data: SignInRequest):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Get user with password
        cur.execute(
            """SELECT u.id, u.email, u.name, u.email_verified, p.hashed_password
               FROM users u
               JOIN passwords p ON u.id = p.user_id
               WHERE u.email = %s""",
            (data.email,)
        )
        user = cur.fetchone()

        if not user or not verify_password(data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Generate JWT token
        token = create_access_token({"userId": user["id"]})

        return {
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "emailVerified": user["email_verified"],
            },
            "token": token,
        }
    finally:
        cur.close()
        conn.close()

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user["name"],
        "emailVerified": current_user["email_verified"],
    }

@app.post("/api/auth/signout")
async def signout():
    return {"message": "Signed out successfully"}

@app.get("/api/user/roles")
async def get_user_roles(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """SELECT r.id, r.name, r.description
               FROM roles r
               JOIN user_roles ur ON r.id = ur.role_id
               WHERE ur.user_id = %s""",
            (current_user["id"],)
        )
        roles = cur.fetchall()
        return {"roles": [dict(role) for role in roles]}
    finally:
        cur.close()
        conn.close()

@app.get("/api/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user": current_user,
    }

@app.get("/api/admin")
async def admin_route(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """SELECT r.name FROM roles r
               JOIN user_roles ur ON r.id = ur.role_id
               WHERE ur.user_id = %s AND r.name = 'admin'""",
            (current_user["id"],)
        )
        admin_role = cur.fetchone()

        if not admin_role:
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

        return {"message": "Admin route accessed successfully"}
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
