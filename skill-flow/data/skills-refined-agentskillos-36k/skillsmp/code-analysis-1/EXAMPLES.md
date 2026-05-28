# Code Analysis Examples

## Example 1: Python Function Analysis

### Input Code

```python
def process_user_data(data):
    result = []
    for item in data:
        if item['age'] > 18:
            if item['status'] == 'active':
                if item['verified'] == True:
                    user = {
                        'name': item['name'],
                        'email': item['email'],
                        'age': item['age']
                    }
                    result.append(user)
    return result
```

### Analysis Report

**Summary**
- Complexity: Medium-High
- Code Smells: Deep nesting, magic numbers
- Priority Issues: 2 Medium, 1 Low

**Issues Detected:**

1. **Deep Nesting (Medium)**
   - Location: Lines 3-12
   - Issue: Three levels of nested if statements reduce readability
   - Recommendation: Use early returns or combine conditions
   
2. **Magic Number (Medium)**
   - Location: Line 3
   - Issue: Hardcoded age threshold (18) without explanation
   - Recommendation: Extract to named constant
   
3. **Boolean Comparison (Low)**
   - Location: Line 5
   - Issue: `== True` is redundant
   - Recommendation: Use `if item['verified']:`

**Improved Version:**

```python
MINIMUM_AGE = 18

def process_user_data(data):
    """Extract verified active users above minimum age."""
    result = []
    for item in data:
        if not _is_eligible_user(item):
            continue
            
        user = {
            'name': item['name'],
            'email': item['email'],
            'age': item['age']
        }
        result.append(user)
    return result

def _is_eligible_user(item):
    """Check if user meets all eligibility criteria."""
    return (
        item.get('age', 0) > MINIMUM_AGE
        and item.get('status') == 'active'
        and item.get('verified', False)
    )
```

**Improvements Made:**
- Reduced nesting with early continue
- Extracted magic number to constant
- Created helper function for eligibility check
- Added error handling with `.get()`
- Added docstrings
- Removed redundant boolean comparison

---

## Example 2: JavaScript Async Pattern Analysis

### Input Code

```javascript
function getUserData(userId) {
    fetch('/api/user/' + userId)
        .then(response => response.json())
        .then(user => {
            fetch('/api/posts/' + user.id)
                .then(response => response.json())
                .then(posts => {
                    fetch('/api/comments/' + user.id)
                        .then(response => response.json())
                        .then(comments => {
                            console.log(user, posts, comments);
                        });
                });
        });
}
```

### Analysis Report

**Summary**
- Complexity: High
- Code Smells: Callback hell, no error handling
- Priority Issues: 1 High, 1 Medium

**Critical Issues:**

1. **Callback Hell (High)**
   - Location: Entire function
   - Issue: Nested promises create hard-to-maintain code
   - Impact: Difficult to debug, test, and extend
   
2. **No Error Handling (High)**
   - Location: All fetch calls
   - Issue: Network failures will crash or hang
   - Impact: Poor user experience, debugging difficulty

3. **String Concatenation in URLs (Medium)**
   - Location: Lines 2, 5, 8
   - Issue: Doesn't handle special characters
   - Recommendation: Use template literals

**Improved Version:**

```javascript
async function getUserData(userId) {
    try {
        const userResponse = await fetch(`/api/user/${userId}`);
        if (!userResponse.ok) {
            throw new Error(`Failed to fetch user: ${userResponse.status}`);
        }
        const user = await userResponse.json();
        
        // Parallel fetch for better performance
        const [postsResponse, commentsResponse] = await Promise.all([
            fetch(`/api/posts/${user.id}`),
            fetch(`/api/comments/${user.id}`)
        ]);
        
        if (!postsResponse.ok || !commentsResponse.ok) {
            throw new Error('Failed to fetch user data');
        }
        
        const [posts, comments] = await Promise.all([
            postsResponse.json(),
            commentsResponse.json()
        ]);
        
        return { user, posts, comments };
        
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error; // Re-throw for caller to handle
    }
}
```

**Improvements Made:**
- Used async/await for cleaner syntax
- Added comprehensive error handling
- Parallelized independent requests with `Promise.all()`
- Used template literals for URLs
- Added response status checking
- Returns data instead of console.log
- Added error logging

---

## Example 3: Java Class Design Analysis

### Input Code

```java
public class DataProcessor {
    private Database db;
    private Logger logger;
    private EmailService emailService;
    
    public void processData(String data) {
        try {
            String[] parts = data.split(",");
            int id = Integer.parseInt(parts[0]);
            String name = parts[1];
            String email = parts[2];
            
            db.connect();
            db.execute("INSERT INTO users VALUES (" + id + ", '" + name + "', '" + email + "')");
            db.disconnect();
            
            logger.log("User added: " + name);
            emailService.send(email, "Welcome", "Welcome to our system");
            
        } catch (Exception e) {
            logger.log("Error: " + e.getMessage());
        }
    }
}
```

### Analysis Report

**Summary**
- Complexity: Medium
- SOLID Violations: Multiple
- Priority Issues: 3 High, 2 Medium

**Critical Issues:**

1. **SQL Injection Vulnerability (High)**
   - Location: Line 14
   - Issue: String concatenation in SQL query
   - Impact: Security risk - database compromise
   - Recommendation: Use PreparedStatement

2. **God Class / SRP Violation (High)**
   - Location: Entire class
   - Issue: Handles parsing, database, logging, and email
   - Impact: Hard to test, maintain, and reuse
   - Recommendation: Separate concerns into distinct classes

3. **Poor Error Handling (High)**
   - Location: Line 20
   - Issue: Catches all exceptions without proper handling
   - Impact: Fails silently, difficult debugging

4. **Resource Management (Medium)**
   - Location: Lines 13-15
   - Issue: Manual connection management, no cleanup on error
   - Recommendation: Use try-with-resources

5. **No Input Validation (Medium)**
   - Location: Lines 8-10
   - Issue: Assumes data format without validation
   - Recommendation: Validate before processing

**Improved Version:**

```java
// Single Responsibility: Parse data
public class UserDataParser {
    public UserData parse(String data) throws InvalidDataException {
        String[] parts = data.split(",");
        if (parts.length != 3) {
            throw new InvalidDataException("Expected 3 fields, got " + parts.length);
        }
        
        try {
            int id = Integer.parseInt(parts[0]);
            String name = parts[1].trim();
            String email = parts[2].trim();
            
            validateEmail(email);
            
            return new UserData(id, name, email);
        } catch (NumberFormatException e) {
            throw new InvalidDataException("Invalid ID format", e);
        }
    }
    
    private void validateEmail(String email) throws InvalidDataException {
        if (!email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
            throw new InvalidDataException("Invalid email format: " + email);
        }
    }
}

// Single Responsibility: Database operations
public class UserRepository {
    private final DataSource dataSource;
    
    public UserRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }
    
    public void save(UserData user) throws DatabaseException {
        String sql = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)";
        
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, user.getId());
            stmt.setString(2, user.getName());
            stmt.setString(3, user.getEmail());
            stmt.executeUpdate();
            
        } catch (SQLException e) {
            throw new DatabaseException("Failed to save user", e);
        }
    }
}

// Single Responsibility: Orchestration
public class UserRegistrationService {
    private final UserDataParser parser;
    private final UserRepository repository;
    private final NotificationService notificationService;
    private final Logger logger;
    
    public UserRegistrationService(
            UserDataParser parser,
            UserRepository repository,
            NotificationService notificationService,
            Logger logger) {
        this.parser = parser;
        this.repository = repository;
        this.notificationService = notificationService;
        this.logger = logger;
    }
    
    public void registerUser(String rawData) {
        try {
            UserData user = parser.parse(rawData);
            repository.save(user);
            notificationService.sendWelcomeEmail(user);
            logger.info("User registered successfully: " + user.getName());
            
        } catch (InvalidDataException e) {
            logger.error("Invalid user data: " + e.getMessage());
            throw new RegistrationException("Invalid user data", e);
            
        } catch (DatabaseException e) {
            logger.error("Database error during registration: " + e.getMessage());
            throw new RegistrationException("Registration failed", e);
            
        } catch (NotificationException e) {
            // User saved but notification failed - log but don't fail registration
            logger.warn("Failed to send welcome email: " + e.getMessage());
        }
    }
}

// Value Object
public class UserData {
    private final int id;
    private final String name;
    private final String email;
    
    public UserData(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters...
}
```

**Improvements Made:**
- **Single Responsibility**: Each class has one clear purpose
- **Security**: PreparedStatement prevents SQL injection
- **Error Handling**: Specific exceptions with context
- **Resource Management**: Try-with-resources ensures cleanup
- **Input Validation**: Validates data before processing
- **Dependency Injection**: Testable, flexible design
- **Immutability**: UserData as value object
- **Type Safety**: Custom exceptions instead of generic Exception

---

## Example 4: Go Idiomatic Code Analysis

### Input Code

```go
type Server struct {
    config map[string]string
}

func (s *Server) Start() {
    port := s.config["port"]
    host := s.config["host"]
    timeout := s.config["timeout"]
    
    // Start server
    http.HandleFunc("/", s.handleRequest)
    http.ListenAndServe(host+":"+port, nil)
}

func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    data := r.URL.Query().Get("data")
    result := processData(data)
    w.Write([]byte(result))
}
```

### Analysis Report

**Summary**
- Go Idioms: Several violations
- Error Handling: Missing
- Priority Issues: 2 High, 3 Medium

**Issues Detected:**

1. **No Error Handling (High)**
   - Location: Lines 12, 18
   - Issue: Ignored errors from `ListenAndServe` and `Write`
   - Impact: Silent failures, difficult debugging

2. **Unsafe Configuration Access (High)**
   - Location: Lines 6-8
   - Issue: No validation of required config values
   - Impact: Runtime panics if keys missing

3. **Non-idiomatic Config Type (Medium)**
   - Location: Line 2
   - Issue: `map[string]string` instead of struct
   - Recommendation: Use typed configuration struct

4. **No Context Usage (Medium)**
   - Location: Entire code
   - Issue: No context for cancellation/timeout
   - Recommendation: Accept and propagate context

5. **Direct HTTP Handler (Medium)**
   - Location: Lines 15-18
   - Issue: No middleware, logging, or error handling
   - Recommendation: Use proper middleware pattern

**Improved Version:**

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "log"
    "net/http"
    "time"
)

// Config represents server configuration
type Config struct {
    Host    string
    Port    int
    Timeout time.Duration
}

// Validate checks if configuration is valid
func (c Config) Validate() error {
    if c.Port < 1 || c.Port > 65535 {
        return fmt.Errorf("invalid port: %d", c.Port)
    }
    if c.Timeout <= 0 {
        return errors.New("timeout must be positive")
    }
    return nil
}

// Server represents an HTTP server
type Server struct {
    config Config
    logger *log.Logger
    server *http.Server
}

// NewServer creates a new server with validated configuration
func NewServer(config Config, logger *log.Logger) (*Server, error) {
    if err := config.Validate(); err != nil {
        return nil, fmt.Errorf("invalid config: %w", err)
    }
    
    return &Server{
        config: config,
        logger: logger,
    }, nil
}

// Start starts the HTTP server
func (s *Server) Start(ctx context.Context) error {
    mux := http.NewServeMux()
    mux.HandleFunc("/", s.handleRequest)
    
    s.server = &http.Server{
        Addr:         fmt.Sprintf("%s:%d", s.config.Host, s.config.Port),
        Handler:      s.loggingMiddleware(mux),
        ReadTimeout:  s.config.Timeout,
        WriteTimeout: s.config.Timeout,
    }
    
    // Start server in goroutine
    errChan := make(chan error, 1)
    go func() {
        s.logger.Printf("Starting server on %s", s.server.Addr)
        if err := s.server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            errChan <- err
        }
    }()
    
    // Wait for context cancellation or server error
    select {
    case err := <-errChan:
        return fmt.Errorf("server error: %w", err)
    case <-ctx.Done():
        return s.Shutdown(context.Background())
    }
}

// Shutdown gracefully stops the server
func (s *Server) Shutdown(ctx context.Context) error {
    s.logger.Println("Shutting down server...")
    
    shutdownCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel()
    
    if err := s.server.Shutdown(shutdownCtx); err != nil {
        return fmt.Errorf("shutdown error: %w", err)
    }
    
    s.logger.Println("Server stopped")
    return nil
}

// handleRequest handles incoming HTTP requests
func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    data := r.URL.Query().Get("data")
    if data == "" {
        http.Error(w, "missing data parameter", http.StatusBadRequest)
        return
    }
    
    result, err := processData(r.Context(), data)
    if err != nil {
        s.logger.Printf("Error processing data: %v", err)
        http.Error(w, "internal server error", http.StatusInternalServerError)
        return
    }
    
    if _, err := w.Write([]byte(result)); err != nil {
        s.logger.Printf("Error writing response: %v", err)
    }
}

// loggingMiddleware logs HTTP requests
func (s *Server) loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        s.logger.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
        s.logger.Printf("Completed in %v", time.Since(start))
    })
}

// processData processes the input data
func processData(ctx context.Context, data string) (string, error) {
    // Check context cancellation
    select {
    case <-ctx.Done():
        return "", ctx.Err()
    default:
    }
    
    // Process data...
    return "processed: " + data, nil
}
```

**Improvements Made:**
- **Error Handling**: All errors properly checked and returned
- **Configuration**: Type-safe struct with validation
- **Context Usage**: Proper context propagation and cancellation
- **Graceful Shutdown**: Clean server shutdown on context cancellation
- **Middleware Pattern**: Logging middleware following Go conventions
- **Validation**: Input validation with proper error responses
- **Structured Logging**: Better log messages
- **Constructor Pattern**: `NewServer` with validation
- **Idiomatic Go**: Follows Go best practices and conventions
