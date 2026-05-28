"""
Test file demonstrating PATCH endpoint behavior for partial updates

This shows exactly how the PATCH endpoint handles different scenarios:
1. Partial updates (only some fields provided)
2. Full updates (all fields provided)
3. Empty updates (no fields provided)
"""

from fastapi.testclient import TestClient
from patch_endpoint_example import app, UserUpdate


# Create test client
client = TestClient(app)


def test_partial_update_name_only():
    """
    Test updating only the name field.

    Expected: Only name is updated, email and age remain unchanged.
    """
    response = client.patch(
        "/users/1",
        json={"name": "John Updated"}
    )

    assert response.status_code == 200
    data = response.json()

    # Only name should be updated
    assert data["name"] == "John Updated"
    assert data["email"] == "john@example.com"  # Unchanged
    assert data["age"] == 30  # Unchanged
    assert data["id"] == 1

    print("✓ Test 1 passed: Partial update (name only)")
    print(f"  Updated user: {data}")


def test_partial_update_age_only():
    """
    Test updating only the age field.

    Expected: Only age is updated, name and email remain unchanged.
    """
    response = client.patch(
        "/users/2",
        json={"age": 26}
    )

    assert response.status_code == 200
    data = response.json()

    # Only age should be updated
    assert data["name"] == "Jane Smith"  # Unchanged
    assert data["email"] == "jane@example.com"  # Unchanged
    assert data["age"] == 26  # Updated
    assert data["id"] == 2

    print("✓ Test 2 passed: Partial update (age only)")
    print(f"  Updated user: {data}")


def test_partial_update_multiple_fields():
    """
    Test updating multiple fields at once.

    Expected: All provided fields are updated, unprovided fields remain unchanged.
    """
    response = client.patch(
        "/users/3",
        json={
            "name": "Robert Johnson",
            "email": "robert@example.com"
        }
    )

    assert response.status_code == 200
    data = response.json()

    # Name and email should be updated
    assert data["name"] == "Robert Johnson"
    assert data["email"] == "robert@example.com"
    assert data["age"] == 35  # Unchanged
    assert data["id"] == 3

    print("✓ Test 3 passed: Partial update (multiple fields)")
    print(f"  Updated user: {data}")


def test_empty_update():
    """
    Test sending an empty request body.

    Expected: User is returned unchanged.
    """
    # First, get the current state
    get_response = client.get("/users/1")
    original_data = get_response.json()

    # Send empty update
    patch_response = client.patch(
        "/users/1",
        json={}
    )

    assert patch_response.status_code == 200
    data = patch_response.json()

    # Everything should be unchanged
    assert data == original_data

    print("✓ Test 4 passed: Empty update (no changes)")
    print(f"  User remains: {data}")


def test_full_update():
    """
    Test updating all fields.

    Expected: All fields are updated with new values.
    """
    response = client.patch(
        "/users/1",
        json={
            "name": "John Complete Update",
            "email": "john.complete@example.com",
            "age": 32
        }
    )

    assert response.status_code == 200
    data = response.json()

    # All fields should be updated
    assert data["name"] == "John Complete Update"
    assert data["email"] == "john.complete@example.com"
    assert data["age"] == 32
    assert data["id"] == 1

    print("✓ Test 5 passed: Full update (all fields)")
    print(f"  Updated user: {data}")


def test_model_dump_exclude_unset():
    """
    Demonstrate how Pydantic's exclude_unset works.

    This is the key mechanism that makes partial updates possible.
    """
    print("\n" + "="*70)
    print("PYDANTIC MODEL DEMONSTRATION")
    print("="*70)

    # Create an update model with only name set
    update_data = UserUpdate(name="Test Name")

    print("\nModel with only 'name' field set:")
    print(f"  update_data.model_dump() = {update_data.model_dump()}")
    print(f"  -> Includes all fields with defaults (None)")

    print("\nupdate_data.model_dump(exclude_unset=True):")
    print(f"  -> {update_data.model_dump(exclude_unset=True)}")
    print(f"  -> Includes ONLY fields that were explicitly set!")

    # Create with multiple fields
    update_data2 = UserUpdate(name="Test", age=25)
    print("\nModel with 'name' and 'age' fields set:")
    print(f"  update_data.model_dump(exclude_unset=True) = {update_data2.model_dump(exclude_unset=True)}")

    # Create with no fields
    update_data3 = UserUpdate()
    print("\nModel with no fields set:")
    print(f"  update_data.model_dump(exclude_unset=True) = {update_data3.model_dump(exclude_unset=True)}")
    print(f"  -> Returns empty dict!")

    print("\n" + "="*70)


def test_update_user_with_model_copy():
    """
    Demonstrate how model_copy(update=...) works for partial updates.

    This is the other key mechanism for PATCH endpoints.
    """
    print("\n" + "="*70)
    print("MODEL_COPY DEMONSTRATION")
    print("="*70)

    from patch_endpoint_example import User

    original_user = User(id=1, name="John Doe", email="john@example.com", age=30)

    print("\nOriginal user:")
    print(f"  {original_user.model_dump()}")

    # Simulate partial update - only name and age
    update_data = {"name": "John Updated", "age": 35}

    print("\nUpdate data (only name and age):")
    print(f"  {update_data}")

    # Use model_copy with update parameter
    updated_user = original_user.model_copy(update=update_data)

    print("\nUpdated user using model_copy(update=...):")
    print(f"  {updated_user.model_dump()}")

    print("\nNotice:")
    print(f"  - name changed: {original_user.name} -> {updated_user.name}")
    print(f"  - age changed: {original_user.age} -> {updated_user.age}")
    print(f"  - email unchanged: {updated_user.email}")

    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("FASTAPI PATCH ENDPOINT - DEMONSTRATION & TESTS")
    print("="*70)

    # Run model demonstrations first
    test_model_dump_exclude_unset()
    test_update_user_with_model_copy()

    print("\n" + "="*70)
    print("RUNNING TESTS")
    print("="*70 + "\n")

    # Run tests
    test_partial_update_name_only()
    test_partial_update_age_only()
    test_partial_update_multiple_fields()
    test_empty_update()
    test_full_update()

    print("\n" + "="*70)
    print("ALL TESTS PASSED!")
    print("="*70)

    print("""
SUMMARY:
--------
The PATCH endpoint works correctly by:

1. Using Optional fields in the Pydantic model (UserUpdate)
2. Using exclude_unset=True to get only provided fields
3. Using model_copy(update=...) to apply partial updates
4. Returning the user unchanged if no fields are provided

This allows clients to update only the fields they need to change,
without having to send the entire object.
    """)
