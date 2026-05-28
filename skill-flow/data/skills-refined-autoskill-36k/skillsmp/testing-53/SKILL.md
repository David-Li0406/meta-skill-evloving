---
name: testing
description: Create and execute comprehensive testing strategies including unit tests, integration tests, test-driven development, and test coverage analysis. Use when writing tests, implementing TDD, checking test coverage, or when user mentions testing, test cases, or test automation.
---

# Testing

A comprehensive testing skill that helps design, implement, and maintain effective test suites across different testing levels and frameworks.

## Quick Start

Basic testing workflow:

```python
# Identify testable components
# Design test cases
# Implement tests following patterns
# Run tests and verify coverage
# Maintain and refactor tests
```

## Core Capabilities

### 1. Test Strategy Design

Plan comprehensive testing approaches:

- **Test Pyramid**: Balance unit, integration, and E2E tests
- **Test Coverage**: Identify what needs testing
- **Test Data**: Design test fixtures and mocks
- **Test Environments**: Configure test infrastructure
- **CI/CD Integration**: Automate test execution

### 2. Unit Testing

Test individual components in isolation:

- **Function Tests**: Test pure functions and methods
- **Class Tests**: Test class behavior and state
- **Mock Dependencies**: Isolate units from dependencies
- **Edge Cases**: Test boundary conditions
- **Error Handling**: Test exception paths

### 3. Integration Testing

Test component interactions:

- **API Testing**: Test HTTP endpoints and responses
- **Database Testing**: Test data persistence and queries
- **Service Integration**: Test service-to-service communication
- **External Dependencies**: Test third-party integrations
- **Contract Testing**: Verify API contracts

### 4. Test-Driven Development (TDD)

Follow the TDD red-green-refactor cycle:

1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

### 5. Test Quality

Ensure high-quality tests:

- **Readability**: Clear test names and structure
- **Maintainability**: DRY principles, shared fixtures
- **Performance**: Fast test execution
- **Reliability**: Deterministic, no flaky tests
- **Independence**: Tests don't depend on each other

## Testing Patterns

### AAA Pattern (Arrange-Act-Assert)

```python
def test_calculate_total_with_tax():
    # Arrange
    items = [
        {'name': 'Item 1', 'price': 10.0},
        {'name': 'Item 2', 'price': 20.0}
    ]
    tax_rate = 0.1
    
    # Act
    result = calculate_total(items, tax_rate)
    
    # Assert
    assert result == 33.0
```

### Given-When-Then (BDD Style)

```python
def test_user_registration():
    # Given a new user with valid credentials
    user_data = {
        'email': 'test@example.com',
        'password': 'SecurePass123!',
        'name': 'Test User'
    }
    
    # When registering the user
    response = register_user(user_data)
    
    # Then user is created and confirmation email is sent
    assert response.status_code == 201
    assert response.data['id'] is not None
    assert mock_email_service.send.called
```

### Test Fixtures

```python
import pytest

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return {
        'id': 1,
        'email': 'test@example.com',
        'name': 'Test User'
    }

@pytest.fixture
def database_session():
    """Provide a clean database session for each test."""
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

def test_create_user(database_session, sample_user):
    # Use fixtures in test
    user = User(**sample_user)
    database_session.add(user)
    database_session.commit()
    
    assert user.id is not None
```

## Testing by Framework

### React + TypeScript (Jest + React Testing Library)

- **Component Testing**: Renderizado, interacciones, estados
- **Hook Testing**: Custom hooks con renderHook
- **Event Testing**: Clicks, inputs, formularios
- **Async Testing**: waitFor, findBy queries
- **Mock Testing**: jest.fn(), jest.mock()

### Angular (Jasmine/Karma)

- **Component Testing**: TestBed, fixtures, change detection
- **Service Testing**: HttpClientTestingModule, mock HttpClient
- **Dependency Injection**: TestBed.inject()
- **Async Testing**: fakeAsync, tick, flush
- **Integration Testing**: RouterTestingModule, componentes integrados

### Python (pytest + FastAPI)

- **Unit Testing**: pytest fixtures, parametrize
- **API Testing**: TestClient, async testing
- **Mock Testing**: unittest.mock, pytest-mock
- **Database Testing**: fixtures con rollback
- **Integration Testing**: test containers, real databases

### Java + Spring Boot (JUnit 5 + Mockito)

- **Unit Testing**: @ExtendWith, @Mock, @InjectMocks
- **Service Testing**: Mockito mocks, verify, when
- **Integration Testing**: @SpringBootTest, @AutoConfigureTestDatabase
- **REST API Testing**: MockMvc, TestRestTemplate
- **Transaction Testing**: @Transactional en tests

### Kotlin (JUnit 5 + MockK + Coroutines)

- **Coroutine Testing**: runTest, runBlocking
- **Mock Testing**: mockk, coEvery, coVerify
- **Flow Testing**: turbine, toList()
- **Suspend Function Testing**: TestCoroutineDispatcher
- **Integration Testing**: Spring Boot con coroutines

**Nota**: Para ejemplos completos específicos de tu stack tecnológico (React, Angular, Python, Java, Kotlin), consulta [EXAMPLES_STACK.md](EXAMPLES_STACK.md).

### Ejemplos Genéricos (Legacy)

#### Python (pytest)

```javascript
import { UserService } from './user-service';
import { EmailService } from './email-service';

// Mock the email service
jest.mock('./email-service');

describe('UserService', () => {
  let userService;
  let emailService;
  
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    
    // Create instances
    emailService = new EmailService();
    userService = new UserService(emailService);
  });
  
  describe('createUser', () => {
    it('should create user and send welcome email', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        name: 'Test User'
      };
      
      // Act
      const user = await userService.createUser(userData);
      
      // Assert
      expect(user.email).toBe('test@example.com');
      expect(user.name).toBe('Test User');
      expect(emailService.sendWelcome).toHaveBeenCalledWith(user);
      expect(emailService.sendWelcome).toHaveBeenCalledTimes(1);
    });
    
    it('should throw error for duplicate email', async () => {
      // Arrange
      const userData = { email: 'existing@example.com', name: 'User' };
      
      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Email already exists');
    });
    
    it.each([
      ['not-an-email'],
      ['@example.com'],
      ['test@'],
      [''],
    ])('should throw error for invalid email: %s', async (invalidEmail) => {
      const userData = { email: invalidEmail, name: 'User' };
      
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Invalid email format');
    });
  });
  
  describe('getUserById', () => {
    it('should return user when found', async () => {
      const userId = '123';
      const expectedUser = { id: userId, name: 'Test User' };
      
      const user = await userService.getUserById(userId);
      
      expect(user).toEqual(expectedUser);
    });
    
    it('should return null when user not found', async () => {
      const userId = 'nonexistent';
      
      const user = await userService.getUserById(userId);
      
      expect(user).toBeNull();
    });
  });
});
```

### Java (JUnit 5)

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class UserServiceTest {
    
    @Mock
    private EmailService emailService;
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    @DisplayName("Should create user and send welcome email")
    void testCreateUserSuccess() {
        // Arrange
        UserDTO userData = new UserDTO("test@example.com", "Test User");
        User expectedUser = new User(1L, "test@example.com", "Test User");
        
        when(userRepository.existsByEmail(userData.getEmail()))
            .thenReturn(false);
        when(userRepository.save(any(User.class)))
            .thenReturn(expectedUser);
        
        // Act
        User result = userService.createUser(userData);
        
        // Assert
        assertNotNull(result);
        assertEquals("test@example.com", result.getEmail());
        assertEquals("Test User", result.getName());
        
        verify(userRepository).existsByEmail("test@example.com");
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcome(expectedUser);
    }
    
    @Test
    @DisplayName("Should throw exception for duplicate email")
    void testCreateUserDuplicateEmail() {
        // Arrange
        UserDTO userData = new UserDTO("existing@example.com", "User");
        when(userRepository.existsByEmail(userData.getEmail()))
            .thenReturn(true);
        
        // Act & Assert
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(userData);
        });
        
        verify(userRepository).existsByEmail("existing@example.com");
        verify(userRepository, never()).save(any(User.class));
        verify(emailService, never()).sendWelcome(any(User.class));
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"not-an-email", "@example.com", "test@", ""})
    @DisplayName("Should throw exception for invalid email")
    void testCreateUserInvalidEmail(String invalidEmail) {
        UserDTO userData = new UserDTO(invalidEmail, "User");
        
        assertThrows(InvalidEmailException.class, () -> {
            userService.createUser(userData);
        });
    }
    
    @Nested
    @DisplayName("GetUserById tests")
    class GetUserByIdTests {
        
        @Test
        @DisplayName("Should return user when found")
        void testGetUserByIdFound() {
            Long userId = 1L;
            User expectedUser = new User(userId, "test@example.com", "Test User");
            
            when(userRepository.findById(userId))
                .thenReturn(Optional.of(expectedUser));
            
            Optional<User> result = userService.getUserById(userId);
            
            assertTrue(result.isPresent());
            assertEquals(expectedUser, result.get());
        }
        
        @Test
        @DisplayName("Should return empty when user not found")
        void testGetUserByIdNotFound() {
            Long userId = 999L;
            
            when(userRepository.findById(userId))
                .thenReturn(Optional.empty());
            
            Optional<User> result = userService.getUserById(userId);
            
            assertFalse(result.isPresent());
        }
    }
}
```

## Integration Testing

### API Integration Test (Python)

```python
import pytest
from fastapi.testclient import TestClient
from myapp import app, database

@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the API."""
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function")
def clean_database():
    """Provide a clean database for each test."""
    database.create_all()
    yield
    database.drop_all()

class TestUserAPI:
    """Integration tests for User API endpoints."""
    
    def test_create_user_endpoint(self, test_client, clean_database):
        """Test POST /users creates a new user."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
        
        # Act
        response = test_client.post("/users", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert "id" in data
        assert "password" not in data  # Password should not be returned
    
    def test_get_user_endpoint(self, test_client, clean_database):
        """Test GET /users/{id} retrieves user."""
        # Arrange - create a user first
        user_data = {"email": "test@example.com", "name": "Test User"}
        create_response = test_client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Act
        response = test_client.get(f"/users/{user_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "test@example.com"
    
    def test_list_users_pagination(self, test_client, clean_database):
        """Test GET /users with pagination."""
        # Arrange - create multiple users
        for i in range(15):
            test_client.post("/users", json={
                "email": f"user{i}@example.com",
                "name": f"User {i}"
            })
        
        # Act
        response = test_client.get("/users?page=1&per_page=10")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1
```

## Test Coverage

Aim for comprehensive coverage:

```python
# Generate coverage report
pytest --cov=myapp --cov-report=html tests/

# Coverage goals
# - Overall: > 80%
# - Critical paths: 100%
# - New code: 100%
```

Focus coverage on:
- Business logic
- Error handling
- Edge cases
- Security-critical code

## Best Practices

1. **Test Naming**: Use descriptive names that explain what's being tested
2. **One Assertion Per Test**: Focus each test on one behavior
3. **Test Independence**: Tests should not depend on execution order
4. **Fast Tests**: Keep unit tests under 100ms
5. **Avoid Logic in Tests**: Tests should be simple and obvious
6. **Use Fixtures**: Share setup code via fixtures
7. **Mock External Dependencies**: Isolate unit tests
8. **Test Error Cases**: Don't just test the happy path
9. **Keep Tests Maintainable**: Apply same quality standards as production code
10. **Test Behavior, Not Implementation**: Test what, not how

## When to Use This Skill

Use this skill when:
- Writing new tests for existing code
- Implementing TDD for new features
- Improving test coverage
- Designing test strategies
- Setting up testing infrastructure
- Debugging failing tests
- Refactoring test code
- Creating test fixtures and mocks
- Implementing integration tests
- Setting up CI/CD test pipelines

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete testing examples across different scenarios and frameworks.

For test templates, see [templates/](templates/).

For test utilities and helpers, see [scripts/test_helpers.py](scripts/test_helpers.py).
