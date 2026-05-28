---
name: testing-patterns
description: Use this skill when you need to implement effective testing strategies, patterns, and best practices across various test types, including unit, integration, and end-to-end tests.
---

# Skill body

## Test Pyramid

```
        /\
       /  \    E2E Tests (few, slow, expensive)
      /----\
     /      \  Integration Tests (some)
    /--------\
   /          \ Unit Tests (many, fast, cheap)
  --------------
```

## Unit Testing Patterns

### Arrange-Act-Assert (AAA)
```python
def test_user_can_change_email():
    # Arrange
    user = User(email="old@example.com")

    # Act
    user.change_email("new@example.com")

    # Assert
    assert user.email == "new@example.com"
```

### Given-When-Then (BDD Style)
```python
def test_user_can_change_email():
    # Given a user with an email
    user = User(email="old@example.com")

    # When they change their email
    user.change_email("new@example.com")

    # Then the email is updated
    assert user.email == "new@example.com"
```

### Test Data Builders
```python
class UserBuilder:
    def __init__(self):
        self.name = "Default Name"
        self.email = "default@example.com"
        self.role = "user"

    def with_name(self, name):
        self.name = name
        return self

    def with_admin_role(self):
        self.role = "admin"
        return self

    def build(self):
        return User(self.name, self.email, self.role)

# Usage
admin = UserBuilder().with_name("Admin").with_admin_role().build()
```

### Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Integration Testing Patterns

### Database Tests
```python
@pytest.fixture
def db_session():
    # Setup
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # Teardown
    session.close()

def test_user_repository(db_session):
    repo = UserRepository(db_session)
    user = repo.create(User(name="Test"))

    found = repo.find_by_id(user.id)
    assert found.name == "Test"
```

### API Tests
```python
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post("/users", json={"name": "Test"})

    assert response.status_code == 201  # Assuming 201 is the expected status code for a successful creation
```