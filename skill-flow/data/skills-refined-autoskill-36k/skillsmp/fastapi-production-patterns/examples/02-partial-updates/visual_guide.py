"""
Visual Guide: How PATCH Endpoint Handles Partial Updates

This file shows the step-by-step flow of how partial updates work.
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FASTAPI PATCH ENDPOINT - VISUAL GUIDE                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

SCENARIO: Client wants to update only the user's name
───────────────────────────────────────────────────────────────────────────────

1. CLIENT REQUEST
   PATCH /users/1
   Content-Type: application/json

   {
     "name": "John Updated"
   }


2. FASTAPI RECEIVES REQUEST
   ┌─────────────────────────────────────────────────────────┐
   │ UserUpdate(name="John Updated", email=None, age=None)  │
   └─────────────────────────────────────────────────────────┘
   ↓
   Pydantic parses JSON and creates model with:
   - name = "John Updated"  ← explicitly set
   - email = None           ← not provided, defaults to None
   - age = None             ← not provided, defaults to None


3. EXTRACT PROVIDED FIELDS
   user_update.model_dump(exclude_unset=True)
   ↓
   ┌────────────────────────────┐
   │ {"name": "John Updated"}   │
   └────────────────────────────┘

   Key point: exclude_unset=True ONLY includes fields that were
   explicitly set in the request, not fields with None values!


4. GET EXISTING USER
   ┌──────────────────────────────────────────────────────────────┐
   │ User(id=1, name="John Doe", email="john@example.com", age=30)│
   └──────────────────────────────────────────────────────────────┘


5. APPLY PARTIAL UPDATE
   existing_user.model_copy(update={"name": "John Updated"})
   ↓
   ┌───────────────────────────────────────────────────────────────┐
   │ User(id=1,                                                    │
   │      name="John Updated",      ← UPDATED                      │
   │      email="john@example.com", ← UNCHANGED                    │
   │      age=30)                   ← UNCHANGED                    │
   └───────────────────────────────────────────────────────────────┘

   model_copy(update=...) creates a new instance:
   - Updates ONLY fields in the update dict
   - Preserves existing values for other fields
   - Does NOT modify the original object


6. RETURN UPDATED USER
   HTTP 200 OK
   Content-Type: application/json

   {
     "id": 1,
     "name": "John Updated",        ← Changed
     "email": "john@example.com",   ← Unchanged
     "age": 30                      ← Unchanged
   }


╔══════════════════════════════════════════════════════════════════════════════╗
║                         DIFFERENT SCENARIOS                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

SCENARIO A: Update multiple fields
───────────────────────────────────

Request:
  {"name": "Jane", "age": 25}

exclude_unset=True → {"name": "Jane", "age": 25}

Result:
  name: UPDATED
  email: UNCHANGED
  age: UPDATED


SCENARIO B: Update single field
────────────────────────────────

Request:
  {"age": 35}

exclude_unset=True → {"age": 35}

Result:
  name: UNCHANGED
  email: UNCHANGED
  age: UPDATED


SCENARIO C: Empty request
──────────────────────────

Request:
  {}

exclude_unset=True → {}

Result:
  ALL FIELDS UNCHANGED (early return)


╔══════════════════════════════════════════════════════════════════════════════╗
║                      KEY IMPLEMENTATION DETAILS                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. PYDANTIC MODEL DESIGN
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   class UserUpdate(BaseModel):
       name: Optional[str] = None     # ← Optional allows field to be omitted
       email: Optional[EmailStr] = None
       age: Optional[int] = None

   All fields are Optional with default None:
   ✓ Clients can provide any subset of fields
   ✗ If fields were required, couldn't do partial updates


2. EXTRACTING PROVIDED FIELDS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   RIGHT: update_data = user_update.model_dump(exclude_unset=True)
          → Returns ONLY fields that were explicitly set

   WRONG: update_data = user_update.model_dump()
          → Returns ALL fields, with None for unprovided fields
          → Would overwrite existing data with None!


3. APPLYING UPDATES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   RIGHT: updated_user = existing_user.model_copy(update=update_data)
          → Creates NEW instance with updates applied
          → Preserves original object (immutable)
          → Only updates fields in update_data

   WRONG: for field, value in update_data.items():
              setattr(existing_user, field, value)
          → Mutates original object
          → Less idiomatic for Pydantic


4. HANDLING EMPTY UPDATES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   if not update_data:
       return existing_user

   ✓ Avoids unnecessary database write
   ✓ Returns quickly without processing
   ✓ Clear intent: no changes needed


╔══════════════════════════════════════════════════════════════════════════════╗
║                          PUT vs PATCH                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PUT - Complete replacement
──────────────────────────
PUT /users/1
{
  "name": "John",
  "email": "john@example.com",  ← Must include ALL fields
  "age": 30                      ← Even if not changing
}
↓
Replaces ENTIRE resource


PATCH - Partial update
──────────────────────
PATCH /users/1
{
  "name": "John"    ← Only include CHANGED fields
}
↓
Updates ONLY provided fields


╔══════════════════════════════════════════════════════════════════════════════╗
║                        SUMMARY                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

To implement a PATCH endpoint that only updates provided fields:

1. Create update model with ALL Optional fields
2. Use model_dump(exclude_unset=True) to get provided fields
3. Use model_copy(update=...) to apply updates
4. Handle empty updates with early return
5. Return the updated user

This approach:
✓ Is idiomatic FastAPI/Pydantic
✓ Handles all edge cases
✓ Is type-safe
✓ Provides automatic API documentation
✓ Is easy to test and maintain

╔══════════════════════════════════════════════════════════════════════════════╗
""")
