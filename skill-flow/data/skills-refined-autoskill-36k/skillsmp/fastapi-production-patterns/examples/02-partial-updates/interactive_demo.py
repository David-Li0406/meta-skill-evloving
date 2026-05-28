"""
Interactive demonstration of PATCH endpoint behavior
Shows exactly how partial updates work step by step
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


# Simplified models for demonstration
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


def demonstrate_update_scenario(scenario_name: str, request_json: dict, existing_user: User):
    """Demonstrate a single update scenario"""
    print(f"\n{'='*70}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*70}")

    # Step 1: Show request
    print("\n1. CLIENT REQUEST:")
    print(f"   PATCH /users/{existing_user.id}")
    print(f"   {request_json}")

    # Step 2: Parse with Pydantic
    user_update = UserUpdate(**request_json)
    print("\n2. PYDANTIC PARSED MODEL:")
    print(f"   UserUpdate(")
    print(f"     name={repr(user_update.name)},")
    print(f"     email={repr(user_update.email)},")
    print(f"     age={repr(user_update.age)}")
    print(f"   )")

    # Step 3: Extract with exclude_unset
    update_data = user_update.model_dump(exclude_unset=True)
    print("\n3. EXTRACT PROVIDED FIELDS (exclude_unset=True):")
    if update_data:
        for key, value in update_data.items():
            print(f"   {key}: {repr(value)}")
    else:
        print("   {} (empty - no fields provided)")

    # Step 4: Show existing user
    print("\n4. EXISTING USER:")
    print(f"   {existing_user.model_dump()}")

    # Step 5: Apply update
    if update_data:
        updated_user = existing_user.model_copy(update=update_data)
        print("\n5. APPLY PARTIAL UPDATE:")
        print(f"   existing_user.model_copy(update={update_data})")
    else:
        updated_user = existing_user
        print("\n5. NO UPDATE NEEDED:")
        print(f"   Returning existing user unchanged")

    # Step 6: Show result
    print("\n6. RESULT:")
    result = updated_user.model_dump()
    print(f"   {result}")

    # Step 7: Highlight changes
    print("\n7. CHANGES:")
    existing_dict = existing_user.model_dump()
    changes_found = False

    for field in ["name", "email", "age"]:
        if field in update_data:
            old_val = existing_dict[field]
            new_val = result[field]
            print(f"   ✓ {field}: {repr(old_val)} → {repr(new_val)}")
            changes_found = True
        else:
            print(f"   - {field}: unchanged")

    if not changes_found:
        print(f"   (no changes)")

    return updated_user


def main():
    print("\n" + "="*70)
    print("INTERACTIVE PATCH ENDPOINT DEMONSTRATION")
    print("="*70)
    print("\nThis demonstrates exactly how PATCH partial updates work")
    print("using Pydantic models and the exclude_unset pattern")

    # Start with initial user
    user = User(id=1, name="John Doe", email="john@example.com", age=30)

    print("\n" + "="*70)
    print("INITIAL STATE")
    print("="*70)
    print(f"\nStarting user:")
    print(f"  {user.model_dump()}")

    # Scenario 1: Update only name
    user = demonstrate_update_scenario(
        "Update Only Name",
        {"name": "John Updated"},
        user
    )

    # Scenario 2: Update only age
    user = demonstrate_update_scenario(
        "Update Only Age",
        {"age": 35},
        user
    )

    # Scenario 3: Update multiple fields
    user = demonstrate_update_scenario(
        "Update Multiple Fields",
        {"name": "John Smith", "email": "john.smith@example.com"},
        user
    )

    # Scenario 4: Empty update
    user = demonstrate_update_scenario(
        "Empty Update (No Fields)",
        {},
        user
    )

    # Scenario 5: Update all fields
    user = demonstrate_update_scenario(
        "Update All Fields",
        {"name": "John Final", "email": "john.final@example.com", "age": 32},
        user
    )

    print("\n" + "="*70)
    print("FINAL STATE")
    print("="*70)
    print(f"\nFinal user:")
    print(f"  {user.model_dump()}")

    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)

    print("""
1. Optional Fields in Model
   - Allows clients to provide any subset of fields
   - Unprovided fields default to None

2. exclude_unset=True
   - Returns ONLY fields that were explicitly set
   - Crucial for partial updates!
   - Without it, all fields (including None) would be included

3. model_copy(update=...)
   - Creates new instance with only specified fields updated
   - Preserves all other field values
   - Immutable (doesn't modify original)

4. Empty Check
   - Returns early if no fields provided
   - Avoids unnecessary operations
   - Returns user unchanged

This pattern is the idiomatic way to implement PATCH endpoints
in FastAPI with Pydantic models.
    """)


if __name__ == "__main__":
    main()
