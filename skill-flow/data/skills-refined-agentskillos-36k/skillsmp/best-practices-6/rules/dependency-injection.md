---
title: Dependency Injection
impact: HIGH
impactDescription: Clean architecture, testability, resource management
tags: depends, dependencies, lifecycle, testing
---

# Dependency Injection

FastAPI's `Depends` is powerful. Use it correctly for clean, testable code.

## Rule 1: Use Depends for Shared Logic

```python
# ❌ INCORRECT - repeated code in every endpoint
@app.get("/items/")
async def get_items(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    if limit > 100:
        limit = 100
    # ... pagination logic repeated

@app.get("/users/")
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    if limit > 100:
        limit = 100
    # ... same pagination logic

# ✅ CORRECT - extracted to dependency
from fastapi import Query

class Pagination:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def get_items(
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db)
):
    pass
```

## Rule 2: Use yield for Resource Cleanup

```python
# ❌ INCORRECT - no cleanup guarantee
async def get_db():
    db = AsyncSession(engine)
    return db  # never closed!

# ✅ CORRECT - yield ensures cleanup
async def get_db():
    async with AsyncSession(engine) as session:
        yield session
    # session automatically closed after request

# ✅ ALSO CORRECT - explicit try/finally
async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
```

## Rule 3: Dependency Caching per Request

```python
# Dependencies are cached per request by default
# This means multiple uses of the same dependency share the instance

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # This is called ONCE per request, even if used in multiple places
    return await decode_token(token)

@app.get("/items/")
async def get_items(
    user: User = Depends(get_current_user),  # First call
    validator: Validator = Depends(get_validator)  # Uses same user
):
    pass

# To disable caching (for unique instances):
@app.get("/items/")
async def get_items(
    id1: str = Depends(generate_id, use_cache=False),
    id2: str = Depends(generate_id, use_cache=False)  # Different ID
):
    pass
```

## Rule 4: Dependency Classes for Complex Logic

```python
# ❌ INCORRECT - complex function dependency
def complex_dependency(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings)
):
    # ... complex logic
    return result

# ✅ CORRECT - class-based dependency
class ItemService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
        self.db = db
        self.user = user

    async def get_items(self):
        return await self.db.execute(
            select(Item).where(Item.owner_id == self.user.id)
        )

@app.get("/items/")
async def get_items(service: ItemService = Depends()):
    return await service.get_items()
```

## Rule 5: Dependency Hierarchy

```python
# Build dependencies that depend on other dependencies

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await db.get(User, decode_token(token).user_id)
    if not user:
        raise HTTPException(401)
    return user

async def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Admin required")
    return user

# Clean endpoint - all dependencies resolved automatically
@app.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    await db.delete(await db.get(User, user_id))
```

## Rule 6: Testing with Dependency Overrides

```python
# ✅ CORRECT - dependencies are easily testable

# In your tests:
from fastapi.testclient import TestClient

def get_test_db():
    return TestSession()

def get_test_user():
    return User(id=1, email="test@test.com")

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = get_test_user

client = TestClient(app)
response = client.get("/items/")
assert response.status_code == 200

# Clean up
app.dependency_overrides.clear()
```

## Anti-Patterns

```python
# ❌ WRONG - global state instead of dependency
db = get_database_connection()  # global!

@app.get("/items/")
async def get_items():
    return db.query(Item).all()  # untestable, not request-scoped

# ❌ WRONG - creating resources in endpoint
@app.get("/items/")
async def get_items():
    db = await create_connection()  # who closes this?
    return await db.fetch_all()

# ❌ WRONG - not using type hints
@app.get("/items/")
async def get_items(db=Depends(get_db)):  # no type hint!
    pass
```
