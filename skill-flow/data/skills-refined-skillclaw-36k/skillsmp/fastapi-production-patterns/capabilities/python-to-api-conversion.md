# Python to API Conversion

## Overview
Converting existing Python functions and utilities to FastAPI endpoints, adding validation, error handling, and async capabilities.

## Problem Statement
**Converting Python utilities to APIs requires:**
- Adding input validation (Pydantic models)
- Making functions async if they do I/O
- Replacing exceptions with HTTPException
- Adding proper return types and response models
- Using dependency injection for shared resources

## Transformation Process

### Step-by-Step Conversion

**1. Original Python Utility**
```python
# utils/payment.py
def process_payment(user_id: int, amount: float, card: dict) -> dict:
    # Blocking database call
    result = db.execute(f"SELECT * FROM users WHERE id = {user_id}")

    # Business logic
    if result['balance'] < amount:
        raise ValueError("Insufficient funds")

    # Process payment
    transaction_id = payment_gateway.charge(card, amount)
    return {"status": "success", "transaction_id": transaction_id}
```

**2. Add Pydantic Models**
```python
# models.py
from pydantic import BaseModel, Field, validator

class CreditCard(BaseModel):
    number: str = Field(..., min_length=13, max_length=19)
    expiry: str
    cvv: str = Field(..., min_length=3, max_length=4)

    @validator('number')
    def luhn_check(cls, v):
        if not luhn_valid(v):
            raise ValueError('Invalid card number')
        return v

class PaymentRequest(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0)  # Must be positive
    card: CreditCard

class PaymentResponse(BaseModel):
    status: str
    transaction_id: str
```

**3. Make Async**
```python
# utils/payment.py (async version)
async def process_payment_async(
    user_id: int,
    amount: float,
    card: CreditCard,
    db: AsyncSession
) -> str:
    # Async database call
    user = await db.get(User, user_id)

    if user.balance < amount:
        raise ValueError("Insufficient funds")

    # Async payment gateway
    transaction_id = await payment_gateway.charge_async(card, amount)

    return transaction_id
```

**4. Create FastAPI Endpoint**
```python
# routes/payments.py
from fastapi import HTTPException, Depends

@app.post("/payments", response_model=PaymentResponse)
async def payment_endpoint(
    request: PaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    # Validate user exists
    user = await db.get(User, request.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check balance
    if user.balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )

    # Process payment
    try:
        transaction_id = await process_payment_async(
            request.user_id,
            request.amount,
            request.card,
            db
        )
    except PaymentGatewayError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment gateway error: {str(e)}"
        )

    return PaymentResponse(
        status="success",
        transaction_id=transaction_id
    )
```

## Conversion Checklist

| Step | What to Do | Why |
|------|------------|-----|
| 1. Add Pydantic models | Create Request/Response models | Automatic validation |
| 2. Make async | Add async/await for I/O operations | Non-blocking |
| 3. Replace exceptions | Use HTTPException with status codes | Proper HTTP responses |
| 4. Add response_model | Specify return model in decorator | Output validation |
| 5. Use dependencies | Replace globals with Depends() | Testability |

## Common Conversions

### Sync Database → Async
```python
# Before
def get_user(user_id: int):
    return session.query(User).filter(User.id == user_id).first()

# After
async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### Dict → Pydantic Model
```python
# Before
def create_user(data: dict) -> dict:
    user = User(**data)
    return user.to_dict()

# After
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

### Exception → HTTPException
```python
# Before
def update_item(item_id: int, data: dict):
    item = get_item(item_id)
    if not item:
        raise ValueError("Item not found")  # Returns 500!

# After
@app.put("/items/{item_id}")
async def update_item(item_id: int, data: ItemUpdate):
    item = await get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return item
```

## Real-World Example

### Data Processing Utility → API

**Original Utility:**
```python
# analytics.py
def generate_report(start_date: date, end_date: date) -> dict:
    data = db.query(Sales).filter(
        Sales.date.between(start_date, end_date)
    ).all()

    total = sum(s.amount for s in data)
    average = total / len(data) if data else 0

    return {
        "total_sales": total,
        "average_sale": average,
        "transaction_count": len(data)
    }
```

**API Version:**
```python
# routes/reports.py
from datetime import date
from pydantic import BaseModel

class ReportRequest(BaseModel):
    start_date: date
    end_date: date

    @validator('end_date')
    def end_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class ReportResponse(BaseModel):
    total_sales: float
    average_sale: float
    transaction_count: int
    period_start: date
    period_end: date

@app.post("/reports/sales", response_model=ReportResponse)
async def generate_sales_report(
    request: ReportRequest,
    db: AsyncSession = Depends(get_db)
):
    # Async database query
    result = await db.execute(
        select(Sales).where(
            Sales.date.between(request.start_date, request.end_date)
        )
    )
    sales = result.scalars().all()

    # Calculate metrics
    total = sum(s.amount for s in sales)
    average = total / len(sales) if sales else 0

    return ReportResponse(
        total_sales=total,
        average_sale=average,
        transaction_count=len(sales),
        period_start=request.start_date,
        period_end=request.end_date
    )
```

## Best Practices

1. **Keep business logic separate**
   - Utilities in separate modules
   - Routes just handle HTTP concerns

2. **Validate early**
   - Pydantic validators for input
   - Database constraints for data integrity

3. **Return proper status codes**
   - 200: Success
   - 201: Created
   - 400: Bad request (validation error)
   - 404: Not found
   - 422: Validation error
   - 500: Server error

4. **Document with examples**
   - Pydantic `json_schema_extra` for examples
   - Auto-generated OpenAPI docs

## See Also
- [Async Conversion](async-conversion.md)
- [Pydantic Partial Updates](pydantic-partial-updates.md)
- [Request Validation](request_validation.md)
