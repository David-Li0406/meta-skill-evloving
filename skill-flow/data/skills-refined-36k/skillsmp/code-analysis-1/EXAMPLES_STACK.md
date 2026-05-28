# Code Analysis Examples - Tech Stack Specific

## Example 1: React + TypeScript Component Analysis

### Input Code

```typescript
import React from 'react';

function UserProfile(props) {
  const data = props.data;
  
  return (
    <div>
      {data.map((item, i) => (
        <div key={i}>
          <h2>{item.name}</h2>
          <p>{item.email}</p>
          {item.premium ? <span>Premium</span> : null}
        </div>
      ))}
    </div>
  );
}

export default UserProfile;
```

### Analysis Report

**Summary**
- Complexity: Low-Medium
- Type Safety: Missing
- React Best Practices: Several violations
- Priority Issues: 3 High, 2 Medium

**Issues Detected:**

1. **Missing TypeScript Types (High)**
   - Location: Component props
   - Issue: Using `any` implicitly, no interface defined
   - Recommendation: Create proper TypeScript interfaces

2. **Array Index as Key (High)**
   - Location: Line 8
   - Issue: Using array index as React key causes re-render issues
   - Recommendation: Use unique ID from data

3. **Prop Drilling (Medium)**
   - Location: Props destructuring
   - Issue: Not destructuring props at parameter level
   - Recommendation: Destructure for clarity

4. **Inline Conditional Rendering (Medium)**
   - Location: Line 11
   - Issue: Ternary with `null` can be simplified
   - Recommendation: Use `&&` operator

5. **Missing Memoization (Low)**
   - Issue: No performance optimization for list rendering
   - Recommendation: Consider `React.memo` or `useMemo`

**Improved Version:**

```typescript
import React from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  premium: boolean;
}

interface UserProfileProps {
  users: User[];
}

const UserProfile: React.FC<UserProfileProps> = ({ users }) => {
  return (
    <div className="user-profile-container">
      {users.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
};

interface UserCardProps {
  user: User;
}

const UserCard: React.FC<UserCardProps> = React.memo(({ user }) => {
  return (
    <div className="user-card">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {user.premium && <span className="badge">Premium</span>}
    </div>
  );
});

UserCard.displayName = 'UserCard';

export default UserProfile;
```

**Improvements Made:**
- ✅ Full TypeScript type safety with interfaces
- ✅ Proper destructuring of props
- ✅ Unique ID as React key
- ✅ Component extraction for better organization
- ✅ React.memo for performance optimization
- ✅ Display names for debugging
- ✅ Semantic class names
- ✅ Simplified conditional rendering

---

## Example 2: Angular Service with Observables

### Input Code

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}
  
  getUser(id) {
    return this.http.get('https://api.example.com/users/' + id);
  }
  
  updateUser(id, data) {
    return this.http.put('https://api.example.com/users/' + id, data);
  }
  
  deleteUser(id) {
    return this.http.delete('https://api.example.com/users/' + id);
  }
}
```

### Analysis Report

**Summary**
- TypeScript Usage: Incomplete
- Angular Best Practices: Missing error handling
- API Design: No type safety
- Priority Issues: 2 High, 2 Medium

**Critical Issues:**

1. **No Type Safety (High)**
   - Location: All methods
   - Issue: Missing type annotations for parameters and return types
   - Impact: Runtime errors, no IntelliSense support

2. **No Error Handling (High)**
   - Location: All HTTP calls
   - Issue: Observables don't handle errors
   - Impact: Unhandled promise rejections

3. **String Concatenation in URLs (Medium)**
   - Location: All API calls
   - Issue: Not using template literals
   - Recommendation: Use template strings

4. **Hardcoded API URL (Medium)**
   - Location: All methods
   - Issue: Base URL duplicated
   - Recommendation: Extract to constant or environment

**Improved Version:**

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { environment } from '../environments/environment';

export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export interface UpdateUserDto {
  name?: string;
  email?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly apiUrl = `${environment.apiBaseUrl}/users`;

  constructor(private readonly http: HttpClient) {}

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`).pipe(
      retry(3),
      catchError(this.handleError)
    );
  }

  updateUser(id: string, data: UpdateUserDto): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/${id}`, data).pipe(
      catchError(this.handleError)
    );
  }

  deleteUser(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }

    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
```

**Improvements Made:**
- ✅ Complete TypeScript type safety
- ✅ Proper interfaces for data models
- ✅ Environment-based configuration
- ✅ Error handling with catchError
- ✅ Retry logic for transient failures
- ✅ Readonly properties for immutability
- ✅ Template literals for URLs
- ✅ Proper Observable typing

---

## Example 3: Python FastAPI Service

### Input Code

```python
from fastapi import FastAPI

app = FastAPI()

users = []

@app.post("/users")
def create_user(data: dict):
    users.append(data)
    return data

@app.get("/users/{id}")
def get_user(id: int):
    for u in users:
        if u['id'] == id:
            return u
    return None
```

### Analysis Report

**Summary**
- Type Safety: Minimal
- Validation: Missing
- Error Handling: None
- Data Persistence: In-memory (not production-ready)
- Priority Issues: 3 High, 2 Medium

**Critical Issues:**

1. **No Data Validation (High)**
   - Location: create_user endpoint
   - Issue: Accepts any dict without validation
   - Impact: Data integrity issues, security risks

2. **No Error Handling (High)**
   - Location: get_user endpoint
   - Issue: Returns None instead of proper 404
   - Impact: Unclear API responses

3. **In-Memory Storage (High)**
   - Location: Global users list
   - Issue: Data lost on restart, not thread-safe
   - Impact: Not production-ready

4. **Type Annotations (Medium)**
   - Issue: Missing Pydantic models
   - Recommendation: Use proper data models

5. **No Status Codes (Medium)**
   - Issue: Not using proper HTTP status codes
   - Recommendation: Use FastAPI's Response models

**Improved Version:**

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI(title="User API", version="1.0.0")

# Pydantic models for validation
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "created_at": "2026-01-12T10:00:00",
                "updated_at": "2026-01-12T10:00:00"
            }
        }

# In-memory storage (replace with database in production)
users_db: dict[UUID, User] = {}

@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user with validated data"
)
async def create_user(user_data: UserCreate) -> User:
    """
    Create a new user with the following information:
    
    - **name**: User's full name (required)
    - **email**: Valid email address (required)
    - **age**: User's age (optional, 0-150)
    """
    user_id = uuid4()
    now = datetime.utcnow()
    
    user = User(
        id=user_id,
        **user_data.model_dump(),
        created_at=now,
        updated_at=now
    )
    
    users_db[user_id] = user
    return user

@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique ID"
)
async def get_user(user_id: UUID) -> User:
    """
    Get user by ID.
    
    Raises:
        HTTPException: 404 if user not found
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return users_db[user_id]

@app.get(
    "/users",
    response_model=List[User],
    summary="List all users",
    description="Retrieve a list of all users"
)
async def list_users(
    skip: int = 0,
    limit: int = Field(default=100, le=100)
) -> List[User]:
    """
    List users with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    users_list = list(users_db.values())
    return users_list[skip : skip + limit]

@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update user",
    description="Update an existing user's information"
)
async def update_user(user_id: UUID, user_data: UserCreate) -> User:
    """Update an existing user."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    existing_user = users_db[user_id]
    updated_user = User(
        id=user_id,
        **user_data.model_dump(),
        created_at=existing_user.created_at,
        updated_at=datetime.utcnow()
    )
    
    users_db[user_id] = updated_user
    return updated_user

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by ID"
)
async def delete_user(user_id: UUID) -> None:
    """Delete a user."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    del users_db[user_id]
```

**Improvements Made:**
- ✅ Pydantic models for validation
- ✅ Proper type hints everywhere
- ✅ HTTP status codes
- ✅ Comprehensive error handling
- ✅ API documentation with OpenAPI
- ✅ Input validation (email, age ranges)
- ✅ UUID for IDs
- ✅ Pagination support
- ✅ Timestamps for audit trail
- ✅ Async/await for better performance

---

## Example 4: Java Spring Boot Service

### Input Code

```java
@RestController
public class UserController {
    
    List<User> users = new ArrayList<>();
    
    @PostMapping("/users")
    public User createUser(@RequestBody Map<String, Object> data) {
        User user = new User();
        user.setName((String) data.get("name"));
        user.setEmail((String) data.get("email"));
        users.add(user);
        return user;
    }
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable int id) {
        return users.get(id);
    }
}
```

### Analysis Report

**Summary**
- Architecture: No service layer
- Validation: Missing
- Error Handling: None
- Type Safety: Weak
- Priority Issues: 4 High, 2 Medium

**Critical Issues:**

1. **No Validation (High)**
   - Location: createUser method
   - Issue: No input validation
   - Impact: Invalid data in system

2. **No Error Handling (High)**
   - Location: getUser method
   - Issue: IndexOutOfBoundsException possible
   - Impact: 500 errors for missing users

3. **No Service Layer (High)**
   - Location: Controller
   - Issue: Business logic in controller
   - Impact: Violates Single Responsibility

4. **Weak Type Safety (High)**
   - Location: createUser parameter
   - Issue: Using Map instead of DTO
   - Impact: No compile-time safety

5. **In-Memory Storage (Medium)**
   - Issue: Not using repository/database
   - Impact: Data loss, not scalable

6. **No Response DTOs (Medium)**
   - Issue: Exposing entity directly
   - Impact: Tight coupling, security risks

**Improved Version:**

```java
// Entity
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}

// DTOs
@Data
@Builder
public class CreateUserRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 1, max = 100, message = "Name must be between 1 and 100 characters")
    private String name;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;
}

@Data
@Builder
public class UserResponse {
    private UUID id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    public static UserResponse from(User user) {
        return UserResponse.builder()
            .id(user.getId())
            .name(user.getName())
            .email(user.getEmail())
            .createdAt(user.getCreatedAt())
            .updatedAt(user.getUpdatedAt())
            .build();
    }
}

// Custom Exception
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(UUID id) {
        super("User not found with id: " + id);
    }
}

// Repository
@Repository
public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}

// Service
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    private final UserRepository userRepository;
    
    @Transactional
    public UserResponse createUser(CreateUserRequest request) {
        log.info("Creating user with email: {}", request.getEmail());
        
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException("Email already exists: " + request.getEmail());
        }
        
        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .build();
        
        User savedUser = userRepository.save(user);
        log.info("User created successfully with id: {}", savedUser.getId());
        
        return UserResponse.from(savedUser);
    }
    
    @Transactional(readOnly = true)
    public UserResponse getUser(UUID id) {
        log.debug("Fetching user with id: {}", id);
        
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
        
        return UserResponse.from(user);
    }
    
    @Transactional(readOnly = true)
    public List<UserResponse> listUsers(Pageable pageable) {
        log.debug("Listing users with pagination: {}", pageable);
        
        return userRepository.findAll(pageable)
            .stream()
            .map(UserResponse::from)
            .toList();
    }
    
    @Transactional
    public UserResponse updateUser(UUID id, CreateUserRequest request) {
        log.info("Updating user with id: {}", id);
        
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
        
        if (!user.getEmail().equals(request.getEmail()) &&
            userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException("Email already exists: " + request.getEmail());
        }
        
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        
        User updatedUser = userRepository.save(user);
        log.info("User updated successfully");
        
        return UserResponse.from(updatedUser);
    }
    
    @Transactional
    public void deleteUser(UUID id) {
        log.info("Deleting user with id: {}", id);
        
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException(id);
        }
        
        userRepository.deleteById(id);
        log.info("User deleted successfully");
    }
}

// Controller
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
@Tag(name = "Users", description = "User management API")
public class UserController {
    private final UserService userService;
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create a new user", description = "Creates a new user with validated data")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "User created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid input"),
        @ApiResponse(responseCode = "409", description = "Email already exists")
    })
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        return userService.createUser(request);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID", description = "Retrieve a specific user by their unique ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "User found"),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public UserResponse getUser(@PathVariable UUID id) {
        return userService.getUser(id);
    }
    
    @GetMapping
    @Operation(summary = "List all users", description = "Retrieve a paginated list of all users")
    public Page<UserResponse> listUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "createdAt") String sortBy,
        @RequestParam(defaultValue = "DESC") Sort.Direction direction
    ) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortBy));
        return new PageImpl<>(userService.listUsers(pageable), pageable, userRepository.count());
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update user", description = "Update an existing user's information")
    public UserResponse updateUser(
        @PathVariable UUID id,
        @Valid @RequestBody CreateUserRequest request
    ) {
        return userService.updateUser(id, request);
    }
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "Delete user", description = "Delete a user by ID")
    public void deleteUser(@PathVariable UUID id) {
        userService.deleteUser(id);
    }
}

// Global Exception Handler
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        log.error("User not found: {}", ex.getMessage());
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.NOT_FOUND.value())
            .error("Not Found")
            .message(ex.getMessage())
            .build();
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult().getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage
            ));
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Invalid input parameters")
            .validationErrors(errors)
            .build();
        
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }
}
```

**Improvements Made:**
- ✅ Proper layered architecture (Controller → Service → Repository)
- ✅ JPA entities with proper annotations
- ✅ DTOs for request/response separation
- ✅ Bean validation with @Valid
- ✅ Global exception handling
- ✅ Proper HTTP status codes
- ✅ Transactional boundaries
- ✅ Logging with SLF4J
- ✅ OpenAPI/Swagger documentation
- ✅ Pagination support
- ✅ Custom exceptions
- ✅ Lombok for boilerplate reduction

---

## Example 5: Kotlin + Coroutines Service

### Input Code

```kotlin
@RestController
class UserController {
    val users = mutableListOf<User>()
    
    @PostMapping("/users")
    fun createUser(@RequestBody data: Map<String, Any>): User {
        val user = User(
            name = data["name"] as String,
            email = data["email"] as String
        )
        users.add(user)
        return user
    }
    
    @GetMapping("/users/{id}")
    fun getUser(@PathVariable id: Int): User {
        return users[id]
    }
}
```

### Analysis Report

**Summary**
- Kotlin Features: Under-utilized
- Async/Coroutines: Not used
- Type Safety: Weak (using Map)
- Error Handling: Missing
- Priority Issues: 3 High, 2 Medium

**Critical Issues:**

1. **Not Using Coroutines (High)**
   - Location: All methods
   - Issue: Blocking operations
   - Impact: Poor scalability, blocking threads

2. **Weak Type Safety (High)**
   - Location: createUser parameter
   - Issue: Using Map instead of data class
   - Impact: Runtime errors, no null safety

3. **No Validation (High)**
   - Location: All methods
   - Issue: No input validation
   - Impact: Invalid data possible

4. **Mutable State (Medium)**
   - Location: users list
   - Issue: Mutable collection in controller
   - Impact: Thread safety issues

**Improved Version:**

```kotlin
// Domain Model
@Entity
@Table(name = "users")
data class User(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID = UUID.randomUUID(),
    
    @Column(nullable = false, length = 100)
    val name: String,
    
    @Column(nullable = false, unique = true)
    val email: String,
    
    @Column(name = "created_at", nullable = false, updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "updated_at", nullable = false)
    var updatedAt: LocalDateTime = LocalDateTime.now()
)

// DTOs
data class CreateUserRequest(
    @field:NotBlank(message = "Name is required")
    @field:Size(min = 1, max = 100, message = "Name must be between 1 and 100 characters")
    val name: String,
    
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String
)

data class UserResponse(
    val id: UUID,
    val name: String,
    val email: String,
    val createdAt: LocalDateTime,
    val updatedAt: LocalDateTime
) {
    companion object {
        fun from(user: User) = UserResponse(
            id = user.id,
            name = user.name,
            email = user.email,
            createdAt = user.createdAt,
            updatedAt = user.updatedAt
        )
    }
}

// Custom Exceptions
sealed class UserException(message: String) : RuntimeException(message)

class UserNotFoundException(id: UUID) : UserException("User not found with id: $id")

class DuplicateEmailException(email: String) : UserException("Email already exists: $email")

// Repository (Coroutines support)
@Repository
interface UserRepository : CoroutineCrudRepository<User, UUID> {
    suspend fun findByEmail(email: String): User?
    suspend fun existsByEmail(email: String): Boolean
}

// Service
@Service
class UserService(
    private val userRepository: UserRepository
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
        logger.info("User created successfully with id: ${savedUser.id}")
        
        return UserResponse.from(savedUser)
    }
    
    suspend fun getUser(id: UUID): UserResponse {
        logger.debug("Fetching user with id: $id")
        
        val user = userRepository.findById(id)
            ?: throw UserNotFoundException(id)
        
        return UserResponse.from(user)
    }
    
    suspend fun listUsers(): List<UserResponse> {
        logger.debug("Listing all users")
        
        return userRepository.findAll()
            .map { UserResponse.from(it) }
            .toList()
    }
    
    suspend fun updateUser(id: UUID, request: CreateUserRequest): UserResponse {
        logger.info("Updating user with id: $id")
        
        val user = userRepository.findById(id)
            ?: throw UserNotFoundException(id)
        
        if (user.email != request.email && userRepository.existsByEmail(request.email)) {
            throw DuplicateEmailException(request.email)
        }
        
        val updatedUser = user.copy(
            name = request.name,
            email = request.email,
            updatedAt = LocalDateTime.now()
        )
        
        val saved = userRepository.save(updatedUser)
        logger.info("User updated successfully")
        
        return UserResponse.from(saved)
    }
    
    suspend fun deleteUser(id: UUID) {
        logger.info("Deleting user with id: $id")
        
        if (!userRepository.existsById(id)) {
            throw UserNotFoundException(id)
        }
        
        userRepository.deleteById(id)
        logger.info("User deleted successfully")
    }
}

// Controller
@RestController
@RequestMapping("/api/v1/users")
@Validated
class UserController(
    private val userService: UserService
) {
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun createUser(
        @Valid @RequestBody request: CreateUserRequest
    ): UserResponse = userService.createUser(request)
    
    @GetMapping("/{id}")
    suspend fun getUser(
        @PathVariable id: UUID
    ): UserResponse = userService.getUser(id)
    
    @GetMapping
    suspend fun listUsers(): List<UserResponse> = userService.listUsers()
    
    @PutMapping("/{id}")
    suspend fun updateUser(
        @PathVariable id: UUID,
        @Valid @RequestBody request: CreateUserRequest
    ): UserResponse = userService.updateUser(id, request)
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    suspend fun deleteUser(
        @PathVariable id: UUID
    ) = userService.deleteUser(id)
}

// Exception Handler
@RestControllerAdvice
class GlobalExceptionHandler {
    private val logger = LoggerFactory.getLogger(javaClass)
    
    @ExceptionHandler(UserNotFoundException::class)
    fun handleUserNotFound(ex: UserNotFoundException): ResponseEntity<ErrorResponse> {
        logger.error("User not found: ${ex.message}")
        val error = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.NOT_FOUND.value(),
            error = "Not Found",
            message = ex.message ?: "User not found"
        )
        return ResponseEntity(error, HttpStatus.NOT_FOUND)
    }
    
    @ExceptionHandler(DuplicateEmailException::class)
    fun handleDuplicateEmail(ex: DuplicateEmailException): ResponseEntity<ErrorResponse> {
        logger.error("Duplicate email: ${ex.message}")
        val error = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.CONFLICT.value(),
            error = "Conflict",
            message = ex.message ?: "Duplicate email"
        )
        return ResponseEntity(error, HttpStatus.CONFLICT)
    }
    
    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidationErrors(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors
            .associate { it.field to (it.defaultMessage ?: "Invalid value") }
        
        val error = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.BAD_REQUEST.value(),
            error = "Validation Failed",
            message = "Invalid input parameters",
            validationErrors = errors
        )
        
        return ResponseEntity(error, HttpStatus.BAD_REQUEST)
    }
}

data class ErrorResponse(
    val timestamp: LocalDateTime,
    val status: Int,
    val error: String,
    val message: String,
    val validationErrors: Map<String, String>? = null
)
```

**Improvements Made:**
- ✅ Full Kotlin coroutines support with `suspend` functions
- ✅ Non-blocking async operations
- ✅ Data classes for immutability
- ✅ Proper null safety with Kotlin's type system
- ✅ Extension functions and companion objects
- ✅ Sealed classes for exception hierarchy
- ✅ Smart casts and type inference
- ✅ Destructuring and copy()
- ✅ Bean validation
- ✅ Repository with coroutine support
- ✅ Proper error handling
- ✅ Idiomatic Kotlin code

---

## Summary of Improvements Across Stack

### React + TypeScript
- ✅ Full type safety with interfaces
- ✅ React best practices (keys, memoization)
- ✅ Component composition
- ✅ Performance optimization

### Angular
- ✅ RxJS operators for error handling
- ✅ Proper TypeScript typing
- ✅ Environment-based configuration
- ✅ Service layer architecture

### Python (FastAPI)
- ✅ Pydantic models for validation
- ✅ Async/await support
- ✅ Type hints everywhere
- ✅ Auto-generated OpenAPI docs

### Java (Spring Boot)
- ✅ Layered architecture
- ✅ JPA/Hibernate integration
- ✅ Global exception handling
- ✅ Bean validation
- ✅ Lombok for clean code

### Kotlin
- ✅ Coroutines for async operations
- ✅ Data classes and immutability
- ✅ Null safety
- ✅ Idiomatic Kotlin patterns
- ✅ Sealed classes for type safety
