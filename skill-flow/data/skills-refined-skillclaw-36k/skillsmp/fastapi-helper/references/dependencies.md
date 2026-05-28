# FastAPI Dependencies Reference

## Basic Dependencies

```python
from fastapi import Depends

# Function dependency
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

# Class dependency
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return {"q": commons.q, "skip": commons.skip}

# Shorthand for class
@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

## Nested Dependencies

```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: str | None = Cookie(default=None)
):
    return q or last_query

@app.get("/items/")
async def read_items(query: str = Depends(query_or_cookie_extractor)):
    return {"query": query}
```

## Dependencies with Yield (Context Managers)

```python
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## Global Dependencies

```python
# On app
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# On router
router = APIRouter(dependencies=[Depends(verify_token)])

# On specific route
@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return []
```

## Security Dependencies

```python
from fastapi import Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
    APIKeyHeader,
    APIKeyQuery,
    APIKeyCookie
)

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return decode_token(token)

# Login endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

# HTTP Basic Auth
security = HTTPBasic()

@app.get("/users/me")
async def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username}

# API Key
api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/items/")
async def read_items(api_key: str = Security(api_key_header)):
    return {"api_key": api_key}
```

## Dependency Override (Testing)

```python
# In tests
def override_get_db():
    return TestingSessionLocal()

app.dependency_overrides[get_db] = override_get_db

# Clean up
app.dependency_overrides = {}
```
