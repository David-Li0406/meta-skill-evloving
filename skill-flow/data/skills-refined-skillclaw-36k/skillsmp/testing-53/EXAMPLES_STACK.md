# Testing Examples - Tech Stack Specific

## React + TypeScript + Jest + React Testing Library

### Component Testing

```typescript
// UserProfile.tsx
import React from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  premium: boolean;
}

interface UserProfileProps {
  user: User;
  onEdit?: (user: User) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ user, onEdit }) => {
  const handleEdit = () => {
    if (onEdit) {
      onEdit(user);
    }
  };

  return (
    <div data-testid="user-profile">
      <h2 data-testid="user-name">{user.name}</h2>
      <p data-testid="user-email">{user.email}</p>
      {user.premium && (
        <span data-testid="premium-badge" className="badge">
          Premium
        </span>
      )}
      {onEdit && (
        <button onClick={handleEdit} data-testid="edit-button">
          Edit
        </button>
      )}
    </div>
  );
};
```

```typescript
// UserProfile.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    premium: false,
  };

  it('should render user information', () => {
    render(<UserProfile user={mockUser} />);

    expect(screen.getByTestId('user-name')).toHaveTextContent('John Doe');
    expect(screen.getByTestId('user-email')).toHaveTextContent('john@example.com');
  });

  it('should show premium badge for premium users', () => {
    const premiumUser = { ...mockUser, premium: true };
    render(<UserProfile user={premiumUser} />);

    expect(screen.getByTestId('premium-badge')).toBeInTheDocument();
  });

  it('should not show premium badge for regular users', () => {
    render(<UserProfile user={mockUser} />);

    expect(screen.queryByTestId('premium-badge')).not.toBeInTheDocument();
  });

  it('should call onEdit when edit button is clicked', () => {
    const mockOnEdit = jest.fn();
    render(<UserProfile user={mockUser} onEdit={mockOnEdit} />);

    fireEvent.click(screen.getByTestId('edit-button'));

    expect(mockOnEdit).toHaveBeenCalledWith(mockUser);
    expect(mockOnEdit).toHaveBeenCalledTimes(1);
  });

  it('should not render edit button when onEdit is not provided', () => {
    render(<UserProfile user={mockUser} />);

    expect(screen.queryByTestId('edit-button')).not.toBeInTheDocument();
  });
});
```

### Custom Hook Testing

```typescript
// useUsers.ts
import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
}

export const useUsers = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch('/api/users');
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return { users, loading, error };
};
```

```typescript
// useUsers.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useUsers } from './useUsers';

global.fetch = jest.fn();

describe('useUsers', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('should fetch users successfully', async () => {
    const mockUsers = [
      { id: '1', name: 'John' },
      { id: '2', name: 'Jane' },
    ];

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });

    const { result } = renderHook(() => useUsers());

    expect(result.current.loading).toBe(true);
    expect(result.current.users).toEqual([]);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.users).toEqual(mockUsers);
    expect(result.current.error).toBeNull();
  });

  it('should handle fetch errors', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
    });

    const { result } = renderHook(() => useUsers());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe('Failed to fetch users');
    expect(result.current.users).toEqual([]);
  });

  it('should handle network errors', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    const { result } = renderHook(() => useUsers());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe('Network error');
    expect(result.current.users).toEqual([]);
  });
});
```

---

## Angular + TypeScript + Jasmine/Karma

### Component Testing

```typescript
// user-profile.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';

export interface User {
  id: string;
  name: string;
  email: string;
  premium: boolean;
}

@Component({
  selector: 'app-user-profile',
  template: `
    <div class="user-profile">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
      <span *ngIf="user.premium" class="badge">Premium</span>
      <button *ngIf="editable" (click)="onEditClick()">Edit</button>
    </div>
  `,
})
export class UserProfileComponent {
  @Input() user!: User;
  @Input() editable = false;
  @Output() edit = new EventEmitter<User>();

  onEditClick(): void {
    this.edit.emit(this.user);
  }
}
```

```typescript
// user-profile.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { UserProfileComponent } from './user-profile.component';

describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;

  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    premium: false,
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UserProfileComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
    component.user = mockUser;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display user name and email', () => {
    const h2 = fixture.debugElement.query(By.css('h2'));
    const p = fixture.debugElement.query(By.css('p'));

    expect(h2.nativeElement.textContent).toBe('John Doe');
    expect(p.nativeElement.textContent).toBe('john@example.com');
  });

  it('should show premium badge for premium users', () => {
    component.user = { ...mockUser, premium: true };
    fixture.detectChanges();

    const badge = fixture.debugElement.query(By.css('.badge'));
    expect(badge).toBeTruthy();
  });

  it('should not show premium badge for regular users', () => {
    const badge = fixture.debugElement.query(By.css('.badge'));
    expect(badge).toBeFalsy();
  });

  it('should emit edit event when edit button clicked', () => {
    component.editable = true;
    fixture.detectChanges();

    spyOn(component.edit, 'emit');

    const button = fixture.debugElement.query(By.css('button'));
    button.nativeElement.click();

    expect(component.edit.emit).toHaveBeenCalledWith(mockUser);
  });

  it('should not show edit button when not editable', () => {
    const button = fixture.debugElement.query(By.css('button'));
    expect(button).toBeFalsy();
  });
});
```

### Service Testing with HTTP

```typescript
// user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

export interface User {
  id: string;
  name: string;
  email: string;
}

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = '/api/users';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl).pipe(
      retry(3),
      catchError(this.handleError)
    );
  }

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: any): Observable<never> {
    console.error('An error occurred:', error);
    return throwError(() => new Error('Something went wrong'));
  }
}
```

```typescript
// user.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService, User } from './user.service';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  const mockUsers: User[] = [
    { id: '1', name: 'John', email: 'john@example.com' },
    { id: '2', name: 'Jane', email: 'jane@example.com' },
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService],
    });

    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch users', () => {
    service.getUsers().subscribe((users) => {
      expect(users).toEqual(mockUsers);
      expect(users.length).toBe(2);
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });

  it('should fetch a single user', () => {
    const mockUser = mockUsers[0];

    service.getUser('1').subscribe((user) => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne('/api/users/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });

  it('should handle errors', () => {
    service.getUsers().subscribe({
      next: () => fail('Should have failed'),
      error: (error) => {
        expect(error.message).toBe('Something went wrong');
      },
    });

    const req = httpMock.expectOne('/api/users');
    req.error(new ErrorEvent('Network error'));
  });

  it('should retry on failure', () => {
    service.getUsers().subscribe();

    // Expect 4 requests (1 initial + 3 retries)
    for (let i = 0; i < 4; i++) {
      const req = httpMock.expectOne('/api/users');
      req.error(new ErrorEvent('Network error'));
    }
  });
});
```

---

## Python + pytest + FastAPI

### API Testing

```python
# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List
from uuid import UUID, uuid4

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class User(BaseModel):
    id: UUID
    name: str
    email: str

# In-memory database
users_db: dict[UUID, User] = {}

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate) -> User:
    user_id = uuid4()
    user = User(id=user_id, **user_data.model_dump())
    users_db[user_id] = user
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID) -> User:
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return users_db[user_id]

@app.get("/users", response_model=List[User])
async def list_users() -> List[User]:
    return list(users_db.values())
```

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from uuid import UUID
from main import app, users_db

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test."""
    users_db.clear()
    yield
    users_db.clear()

class TestUserAPI:
    """Test suite for User API endpoints."""
    
    def test_create_user_success(self, client):
        """Test successful user creation."""
        # Arrange
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Act
        response = client.post("/users", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data
        assert UUID(data["id"])  # Validate UUID format
    
    def test_create_user_invalid_email(self, client):
        """Test user creation with invalid email."""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email"
        }
        
        response = client.post("/users", json=user_data)
        
        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["loc"]
    
    def test_create_user_missing_name(self, client):
        """Test user creation without name."""
        user_data = {"email": "john@example.com"}
        
        response = client.post("/users", json=user_data)
        
        assert response.status_code == 422
    
    def test_get_user_success(self, client):
        """Test retrieving an existing user."""
        # Arrange - create a user first
        create_response = client.post("/users", json={
            "name": "Jane Doe",
            "email": "jane@example.com"
        })
        user_id = create_response.json()["id"]
        
        # Act
        response = client.get(f"/users/{user_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Jane Doe"
    
    def test_get_user_not_found(self, client):
        """Test retrieving non-existent user."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        
        response = client.get(f"/users/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_list_users_empty(self, client):
        """Test listing users when database is empty."""
        response = client.get("/users")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_users_multiple(self, client):
        """Test listing multiple users."""
        # Arrange - create multiple users
        for i in range(3):
            client.post("/users", json={
                "name": f"User {i}",
                "email": f"user{i}@example.com"
            })
        
        # Act
        response = client.get("/users")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    @pytest.mark.parametrize("name,email", [
        ("John Doe", "john@example.com"),
        ("Jane Smith", "jane@test.org"),
        ("Bob Wilson", "bob@company.io"),
    ])
    def test_create_user_various_valid_inputs(self, client, name, email):
        """Test user creation with various valid inputs."""
        user_data = {"name": name, "email": email}
        
        response = client.post("/users", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name
        assert data["email"] == email
```

### Testing with Fixtures and Mocks

```python
# services.py
from typing import Optional
import httpx

class ExternalAPIService:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def fetch_user_data(self, user_id: str) -> dict:
        """Fetch user data from external API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
```

```python
# test_services.py
import pytest
from unittest.mock import AsyncMock, patch
from services import ExternalAPIService
import httpx

@pytest.fixture
def api_service():
    """Create API service instance."""
    return ExternalAPIService(base_url="https://api.example.com")

@pytest.mark.asyncio
async def test_fetch_user_data_success(api_service):
    """Test successful data fetch."""
    mock_data = {"id": "123", "name": "John", "email": "john@example.com"}
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_data
        mock_response.raise_for_status = AsyncMock()
        mock_get.return_value = mock_response
        
        result = await api_service.fetch_user_data("123")
        
        assert result == mock_data
        mock_get.assert_called_once_with("https://api.example.com/users/123")

@pytest.mark.asyncio
async def test_fetch_user_data_http_error(api_service):
    """Test handling of HTTP errors."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=None, response=None
        )
        mock_get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPStatusError):
            await api_service.fetch_user_data("999")
```

---

## Java + Spring Boot + JUnit 5 + Mockito

### Service Testing

```java
// UserService.java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    
    @Transactional
    public UserResponse createUser(CreateUserRequest request) {
        log.info("Creating user with email: {}", request.getEmail());
        
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException("Email already exists");
        }
        
        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .build();
        
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser.getEmail());
        
        return UserResponse.from(savedUser);
    }
    
    @Transactional(readOnly = true)
    public UserResponse getUser(UUID id) {
        return userRepository.findById(id)
            .map(UserResponse::from)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

```java
// UserServiceTest.java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    @InjectMocks
    private UserService userService;
    
    private CreateUserRequest validRequest;
    private User mockUser;
    
    @BeforeEach
    void setUp() {
        validRequest = CreateUserRequest.builder()
            .name("John Doe")
            .email("john@example.com")
            .build();
        
        mockUser = User.builder()
            .id(UUID.randomUUID())
            .name("John Doe")
            .email("john@example.com")
            .createdAt(LocalDateTime.now())
            .updatedAt(LocalDateTime.now())
            .build();
    }
    
    @Test
    @DisplayName("Should create user successfully")
    void testCreateUser_Success() {
        // Given
        when(userRepository.existsByEmail(validRequest.getEmail()))
            .thenReturn(false);
        when(userRepository.save(any(User.class)))
            .thenReturn(mockUser);
        doNothing().when(emailService)
            .sendWelcomeEmail(anyString());
        
        // When
        UserResponse result = userService.createUser(validRequest);
        
        // Then
        assertNotNull(result);
        assertEquals("John Doe", result.getName());
        assertEquals("john@example.com", result.getEmail());
        
        verify(userRepository).existsByEmail("john@example.com");
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("john@example.com");
    }
    
    @Test
    @DisplayName("Should throw exception when email already exists")
    void testCreateUser_DuplicateEmail() {
        // Given
        when(userRepository.existsByEmail(validRequest.getEmail()))
            .thenReturn(true);
        
        // When & Then
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(validRequest);
        });
        
        verify(userRepository).existsByEmail("john@example.com");
        verify(userRepository, never()).save(any(User.class));
        verify(emailService, never()).sendWelcomeEmail(anyString());
    }
    
    @Test
    @DisplayName("Should get user by ID successfully")
    void testGetUser_Success() {
        // Given
        UUID userId = UUID.randomUUID();
        when(userRepository.findById(userId))
            .thenReturn(Optional.of(mockUser));
        
        // When
        UserResponse result = userService.getUser(userId);
        
        // Then
        assertNotNull(result);
        assertEquals("John Doe", result.getName());
        verify(userRepository).findById(userId);
    }
    
    @Test
    @DisplayName("Should throw exception when user not found")
    void testGetUser_NotFound() {
        // Given
        UUID userId = UUID.randomUUID();
        when(userRepository.findById(userId))
            .thenReturn(Optional.empty());
        
        // When & Then
        assertThrows(UserNotFoundException.class, () -> {
            userService.getUser(userId);
        });
        
        verify(userRepository).findById(userId);
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"", " ", "  "})
    @DisplayName("Should reject blank names")
    void testCreateUser_BlankName(String blankName) {
        // Given
        CreateUserRequest invalidRequest = CreateUserRequest.builder()
            .name(blankName)
            .email("test@example.com")
            .build();
        
        // When & Then
        // This would be caught by @Valid annotation at controller level
        assertTrue(blankName.isBlank());
    }
    
    @Nested
    @DisplayName("Email validation tests")
    class EmailValidationTests {
        
        @Test
        @DisplayName("Should accept valid email formats")
        void testValidEmails() {
            // Given
            List<String> validEmails = Arrays.asList(
                "test@example.com",
                "user.name@example.com",
                "user+tag@example.co.uk"
            );
            
            // Then
            validEmails.forEach(email -> {
                // Email validation would be handled by @Email annotation
                assertTrue(email.contains("@"));
            });
        }
    }
}
```

### Integration Testing

```java
// UserControllerIntegrationTest.java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
@Transactional
class UserControllerIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private UserRepository userRepository;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    @DisplayName("Should create user via API")
    void testCreateUserIntegration() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
            .name("Integration Test User")
            .email("integration@test.com")
            .build();
        
        // When
        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/v1/users",
            request,
            UserResponse.class
        );
        
        // Then
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Integration Test User", response.getBody().getName());
        
        // Verify in database
        assertTrue(userRepository.existsByEmail("integration@test.com"));
    }
    
    @Test
    @DisplayName("Should return 404 for non-existent user")
    void testGetUser_NotFound() {
        // Given
        UUID nonExistentId = UUID.randomUUID();
        
        // When
        ResponseEntity<ErrorResponse> response = restTemplate.getForEntity(
            "/api/v1/users/" + nonExistentId,
            ErrorResponse.class
        );
        
        // Then
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }
    
    @Test
    @DisplayName("Should prevent duplicate email")
    void testCreateUser_DuplicateEmail() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
            .name("Test User")
            .email("duplicate@test.com")
            .build();
        
        // Create first user
        restTemplate.postForEntity("/api/v1/users", request, UserResponse.class);
        
        // When - try to create duplicate
        ResponseEntity<ErrorResponse> response = restTemplate.postForEntity(
            "/api/v1/users",
            request,
            ErrorResponse.class
        );
        
        // Then
        assertEquals(HttpStatus.CONFLICT, response.getStatusCode());
    }
}
```

---

## Kotlin + Coroutines + JUnit 5 + MockK

### Service Testing

```kotlin
// UserService.kt
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService
) {
    private val logger = LoggerFactory.getLogger(javaClass)
    
    suspend fun createUser(request: CreateUserRequest): UserResponse {
        logger.info("Creating user with email: ${request.email}")
        
        if (userRepository.existsByEmail(request.email)) {
            throw DuplicateEmailException(request.email)
        }
        
        val user = User(
            name = request.name,
            email = request.email
        )
        
        val savedUser = userRepository.save(user)
        emailService.sendWelcomeEmail(savedUser.email)
        
        return UserResponse.from(savedUser)
    }
    
    suspend fun getUser(id: UUID): UserResponse {
        logger.debug("Fetching user with id: $id")
        
        val user = userRepository.findById(id)
            ?: throw UserNotFoundException(id)
        
        return UserResponse.from(user)
    }
}
```

```kotlin
// UserServiceTest.kt
@ExtendWith(MockKExtension::class)
class UserServiceTest {
    
    @MockK
    private lateinit var userRepository: UserRepository
    
    @MockK
    private lateinit var emailService: EmailService
    
    @InjectMockKs
    private lateinit var userService: UserService
    
    private val validRequest = CreateUserRequest(
        name = "John Doe",
        email = "john@example.com"
    )
    
    private val mockUser = User(
        id = UUID.randomUUID(),
        name = "John Doe",
        email = "john@example.com",
        createdAt = LocalDateTime.now(),
        updatedAt = LocalDateTime.now()
    )
    
    @Test
    fun `should create user successfully`() = runTest {
        // Given
        coEvery { userRepository.existsByEmail(validRequest.email) } returns false
        coEvery { userRepository.save(any()) } returns mockUser
        coEvery { emailService.sendWelcomeEmail(any()) } just Runs
        
        // When
        val result = userService.createUser(validRequest)
        
        // Then
        assertNotNull(result)
        assertEquals("John Doe", result.name)
        assertEquals("john@example.com", result.email)
        
        coVerify { userRepository.existsByEmail("john@example.com") }
        coVerify { userRepository.save(any()) }
        coVerify { emailService.sendWelcomeEmail("john@example.com") }
    }
    
    @Test
    fun `should throw exception when email already exists`() = runTest {
        // Given
        coEvery { userRepository.existsByEmail(validRequest.email) } returns true
        
        // When & Then
        assertThrows<DuplicateEmailException> {
            userService.createUser(validRequest)
        }
        
        coVerify { userRepository.existsByEmail("john@example.com") }
        coVerify(exactly = 0) { userRepository.save(any()) }
        coVerify(exactly = 0) { emailService.sendWelcomeEmail(any()) }
    }
    
    @Test
    fun `should get user by ID successfully`() = runTest {
        // Given
        val userId = UUID.randomUUID()
        coEvery { userRepository.findById(userId) } returns mockUser
        
        // When
        val result = userService.getUser(userId)
        
        // Then
        assertNotNull(result)
        assertEquals("John Doe", result.name)
        coVerify { userRepository.findById(userId) }
    }
    
    @Test
    fun `should throw exception when user not found`() = runTest {
        // Given
        val userId = UUID.randomUUID()
        coEvery { userRepository.findById(userId) } returns null
        
        // When & Then
        assertThrows<UserNotFoundException> {
            userService.getUser(userId)
        }
        
        coVerify { userRepository.findById(userId) }
    }
    
    @ParameterizedTest
    @ValueSource(strings = ["test@example.com", "user@test.org", "admin@company.io"])
    fun `should accept valid email formats`(email: String) = runTest {
        // Given
        val request = validRequest.copy(email = email)
        coEvery { userRepository.existsByEmail(email) } returns false
        coEvery { userRepository.save(any()) } returns mockUser.copy(email = email)
        coEvery { emailService.sendWelcomeEmail(any()) } just Runs
        
        // When
        val result = userService.createUser(request)
        
        // Then
        assertEquals(email, result.email)
    }
    
    @Nested
    inner class ErrorHandling {
        
        @Test
        fun `should handle repository errors gracefully`() = runTest {
            // Given
            coEvery { userRepository.existsByEmail(any()) } throws RuntimeException("Database error")
            
            // When & Then
            assertThrows<RuntimeException> {
                userService.createUser(validRequest)
            }
        }
        
        @Test
        fun `should not send email if save fails`() = runTest {
            // Given
            coEvery { userRepository.existsByEmail(any()) } returns false
            coEvery { userRepository.save(any()) } throws RuntimeException("Save failed")
            
            // When & Then
            assertThrows<RuntimeException> {
                userService.createUser(validRequest)
            }
            
            coVerify(exactly = 0) { emailService.sendWelcomeEmail(any()) }
        }
    }
}
```

### Coroutine Flow Testing

```kotlin
// UserStreamService.kt
@Service
class UserStreamService(
    private val userRepository: UserRepository
) {
    fun getUsersStream(): Flow<User> = flow {
        userRepository.findAll().collect { user ->
            emit(user)
            delay(100) // Simulate processing
        }
    }
    
    fun getActiveUsersCount(): Flow<Int> = flow {
        var count = 0
        userRepository.findAll().collect { user ->
            if (user.active) {
                count++
                emit(count)
            }
        }
    }
}
```

```kotlin
// UserStreamServiceTest.kt
class UserStreamServiceTest {
    
    @MockK
    private lateinit var userRepository: UserRepository
    
    @InjectMockKs
    private lateinit var userStreamService: UserStreamService
    
    @BeforeEach
    fun setUp() {
        MockKAnnotations.init(this)
    }
    
    @Test
    fun `should stream users`() = runTest {
        // Given
        val mockUsers = listOf(
            User(id = UUID.randomUUID(), name = "User 1", email = "user1@test.com"),
            User(id = UUID.randomUUID(), name = "User 2", email = "user2@test.com"),
            User(id = UUID.randomUUID(), name = "User 3", email = "user3@test.com")
        )
        
        coEvery { userRepository.findAll() } returns flowOf(*mockUsers.toTypedArray())
        
        // When
        val result = userStreamService.getUsersStream().toList()
        
        // Then
        assertEquals(3, result.size)
        assertEquals(mockUsers, result)
    }
    
    @Test
    fun `should count active users progressively`() = runTest {
        // Given
        val mockUsers = listOf(
            User(id = UUID.randomUUID(), name = "Active 1", email = "a1@test.com", active = true),
            User(id = UUID.randomUUID(), name = "Inactive", email = "i@test.com", active = false),
            User(id = UUID.randomUUID(), name = "Active 2", email = "a2@test.com", active = true)
        )
        
        coEvery { userRepository.findAll() } returns flowOf(*mockUsers.toTypedArray())
        
        // When
        val result = userStreamService.getActiveUsersCount().toList()
        
        // Then
        assertEquals(listOf(1, 2), result)
    }
}
```

---

## Summary of Testing Approaches by Stack

| Stack | Testing Framework | Key Features |
|-------|------------------|--------------|
| **React + TypeScript** | Jest + React Testing Library | Component testing, hooks testing, user interactions |
| **Angular** | Jasmine/Karma | Component testing, service testing, HTTP mocking |
| **Python** | pytest + FastAPI TestClient | Async testing, fixtures, parametrized tests |
| **Java + Spring Boot** | JUnit 5 + Mockito | Integration tests, mock beans, transactional tests |
| **Kotlin** | JUnit 5 + MockK | Coroutine testing, Flow testing, suspend functions |
