---
name: security-auditor
description: Audit NutriProfile code for security vulnerabilities. Use this skill when reviewing authentication, authorization, data validation, API security, or RGPD compliance. Covers OWASP Top 10 and European data protection requirements.
allowed-tools: Read,Grep,Glob
---

# NutriProfile Security Auditor Skill

You are a security expert for the NutriProfile application. This skill helps you audit code for vulnerabilities, ensure RGPD compliance, and maintain secure development practices.

## Security Context

NutriProfile handles sensitive data:
- User credentials (email, password)
- Personal health information (weight, height, medical conditions)
- Dietary preferences and allergies
- Payment information (via Lemon Squeezy)
- AI-generated health advice

## OWASP Top 10 Checklist

### 1. Injection (A03:2021)

#### SQL Injection
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ SECURE - Use SQLAlchemy ORM
result = await db.execute(
    select(User).where(User.email == email)
)

# ✅ SECURE - Parameterized queries
result = await db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

#### Command Injection
```python
# ❌ VULNERABLE
os.system(f"convert {user_input}")

# ✅ SECURE - Use subprocess with array
subprocess.run(["convert", validated_input], check=True)
```

### 2. Broken Authentication (A07:2021)

#### Password Security
```python
# Password hashing with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

#### JWT Configuration
```python
# Secure JWT settings
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Short-lived
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"

# Token validation
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")
```

### 3. Sensitive Data Exposure (A02:2021)

#### Never Log Sensitive Data
```python
# ❌ DANGEROUS
logger.info(f"User login: {email}, password: {password}")

# ✅ SECURE
logger.info(f"User login attempt: {email}")
```

#### Mask Sensitive Fields
```python
# In Pydantic models
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    # Never include: password, hashed_password, tokens
```

### 4. Broken Access Control (A01:2021)

#### Always Verify Ownership
```python
# ❌ VULNERABLE - IDOR
@router.get("/food-logs/{log_id}")
async def get_log(log_id: int):
    return await db.get(FoodLog, log_id)  # Any user can access!

# ✅ SECURE - Verify ownership
@router.get("/food-logs/{log_id}")
async def get_log(
    log_id: int,
    current_user: User = Depends(get_current_user)
):
    log = await db.get(FoodLog, log_id)
    if log.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return log
```

### 5. Security Misconfiguration (A05:2021)

#### CORS Configuration
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nutriprofile.pages.dev",
        "http://localhost:5173"  # Dev only
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

#### Environment Variables
```python
# Never commit secrets
# .env (git-ignored)
SECRET_KEY=your-256-bit-secret
DATABASE_URL=postgres://...
HUGGINGFACE_TOKEN=hf_...

# Validate required env vars at startup
class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v
```

### 6. XSS (Cross-Site Scripting) (A03:2021)

#### React Auto-Escapes
```tsx
// React automatically escapes - SAFE
<div>{userInput}</div>

// ❌ DANGEROUS - dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

#### Sanitize When Necessary
```typescript
import DOMPurify from 'dompurify'

// If you MUST render HTML
const sanitized = DOMPurify.sanitize(userInput)
```

### 7. Insecure Deserialization (A08:2021)

#### Validate All Input
```python
# Pydantic validates automatically
class RecipeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    prep_time: int = Field(..., ge=0, le=480)

    @validator('name')
    def validate_name(cls, v):
        if '<script>' in v.lower():
            raise ValueError('Invalid characters in name')
        return v
```

### 8. Components with Known Vulnerabilities (A06:2021)

```bash
# Check for vulnerabilities
npm audit
pip-audit

# Update dependencies regularly
npm update
pip install --upgrade -r requirements.txt
```

## Authentication Flow Security

### Registration
```python
@router.post("/register")
async def register(user_data: UserCreate):
    # 1. Validate email format (Pydantic)
    # 2. Check email not already registered
    # 3. Validate password strength
    # 4. Hash password with bcrypt
    # 5. Create user with trial period
    # 6. Return token (no password in response)
```

### Login
```python
@router.post("/login")
async def login(credentials: LoginRequest):
    # 1. Find user by email
    # 2. Verify password hash
    # 3. Check user is active
    # 4. Generate access + refresh tokens
    # 5. Log login attempt (without password)
```

### Password Reset
```python
# 1. Generate secure random token
# 2. Store hashed token with expiry
# 3. Send token via email (HTTPS link)
# 4. Validate token on reset
# 5. Invalidate token after use
```

## RGPD Compliance

### Data Minimization
- Only collect necessary data
- Delete data when no longer needed
- Anonymize analytics data

### User Rights Implementation

#### Right to Access
```python
@router.get("/users/me/data")
async def get_user_data(current_user: User):
    """Return all user's personal data."""
    return {
        "profile": await get_profile(current_user.id),
        "food_logs": await get_all_food_logs(current_user.id),
        "recipes": await get_all_recipes(current_user.id),
        "activities": await get_all_activities(current_user.id),
    }
```

#### Right to Deletion
```python
@router.delete("/users/me")
async def delete_account(current_user: User):
    """Delete user and all associated data."""
    # 1. Cancel subscription
    # 2. Delete all food logs
    # 3. Delete all recipes
    # 4. Delete profile
    # 5. Delete user
    # 6. Log deletion (anonymized)
```

#### Right to Portability
```python
@router.get("/users/me/export")
async def export_data(current_user: User):
    """Export all data in JSON format."""
    data = await get_user_data(current_user)
    return JSONResponse(
        content=data,
        headers={
            "Content-Disposition": "attachment; filename=nutriprofile_data.json"
        }
    )
```

### Consent Management
- Explicit consent for data collection
- Clear privacy policy
- Cookie consent banner
- Marketing opt-in (not opt-out)

## API Security

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/vision/analyze")
@limiter.limit("10/minute")
async def analyze_food(request: Request, ...):
    ...
```

### Input Validation
```python
# File upload validation
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

async def validate_image(file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")
```

## Security Audit Checklist

### Authentication
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens have short expiry
- [ ] Refresh tokens are secure
- [ ] No sensitive data in tokens
- [ ] Account lockout after failed attempts

### Authorization
- [ ] All endpoints check authentication
- [ ] Resource ownership verified
- [ ] Tier limits enforced backend
- [ ] Admin endpoints protected

### Data Protection
- [ ] HTTPS enforced
- [ ] Sensitive data encrypted
- [ ] No secrets in code/logs
- [ ] Database credentials secure
- [ ] Backups encrypted

### RGPD
- [ ] Privacy policy exists
- [ ] Cookie consent implemented
- [ ] Data export endpoint
- [ ] Account deletion works
- [ ] Data retention policy

### Infrastructure
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Dependencies updated
- [ ] Security headers set
- [ ] Error messages generic

## Files to Audit

### Critical Security Files
- `backend/app/services/auth.py` - Authentication logic
- `backend/app/api/v1/auth.py` - Auth endpoints
- `backend/app/config.py` - Configuration/secrets
- `backend/app/main.py` - Middleware/CORS

### Data Access Files
- `backend/app/api/v1/*.py` - All endpoints
- `backend/app/services/*.py` - Business logic

### Frontend Security
- `frontend/src/services/api.ts` - API calls
- `frontend/src/store/authStore.ts` - Token storage
