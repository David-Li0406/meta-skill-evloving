---
name: api-conventions
description: API design conventions and patterns for backend development
---

# API Conventions

Guidelines for designing and implementing Backend APIs.

## URL Naming

- Use **plural nouns** for resources: `/trips`, `/ledgers`, `/transactions`
- Use **kebab-case** for multi-word resources: `/trip-members`
- Nested resources follow parent: `/ledgers/{id}/transactions`
- Use **path parameters** for IDs: `/trips/{id}`
- Use **query parameters** for filtering: `/transactions?category=food`

## HTTP Methods

| Method | Usage | Response Code |
|--------|-------|---------------|
| `GET` | Retrieve resource(s) | 200 OK |
| `POST` | Create resource | 201 Created |
| `PUT` | Update resource (full) | 200 OK |
| `PATCH` | Update resource (partial) | 200 OK |
| `DELETE` | Delete resource | 200 OK |

## Request Body

### Create Request
```go
type CreateTripRequest struct {
    Name        string     `json:"name" binding:"required,min=1,max=100"`
    Description string     `json:"description"`
    StartDate   *time.Time `json:"start_date"`
}
```

### Update Request
```go
type UpdateTripRequest struct {
    Name        string     `json:"name" binding:"omitempty,min=1,max=100"`
    Description string     `json:"description"`
}
```

**Rules:**
- Create requests: use `binding:"required"` for mandatory fields
- Update requests: use `binding:"omitempty"` for optional fields
- Use pointers for optional fields that distinguish between "not provided" and "zero value"

---

## Response Format

### Success Response
Return the resource directly (no wrapper):

```go
// Single resource
c.JSON(http.StatusOK, trip)

// List of resources
c.JSON(http.StatusOK, trips)

// Created resource
c.JSON(http.StatusCreated, trip)
```

### Error Response
Use consistent error format:

```go
c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
c.JSON(http.StatusNotFound, gin.H{"error": "Trip not found"})
c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create trip"})
```

### Delete Response
```go
c.JSON(http.StatusOK, gin.H{"message": "Trip deleted"})
```

---

## HTTP Status Codes

| Code | When to Use |
|------|-------------|
| 200 | Success (GET, PUT, DELETE) |
| 201 | Resource created (POST) |
| 400 | Bad request, validation error |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Resource not found |
| 500 | Internal server error |

---

## Handler Structure

```go
type TripHandler struct {
    db *gorm.DB
}

func NewTripHandler(db *gorm.DB) *TripHandler {
    return &TripHandler{db: db}
}

func (h *TripHandler) Create(c *gin.Context) {
    userID := c.MustGet("userID").(uuid.UUID)
    
    // 1. Parse request
    var req CreateTripRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    
    // 2. Business logic
    trip := &models.Trip{...}
    
    // 3. Database operation
    if err := h.db.Create(trip).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create trip"})
        return
    }
    
    // 4. Return response
    c.JSON(http.StatusCreated, trip)
}
```

---

## Validation

Use Gin binding tags for validation:

```go
`binding:"required"`           // Field is required
`binding:"required,min=1"`     // Required with min length
`binding:"omitempty,max=100"`  // Optional with max length
`binding:"email"`              // Must be valid email
```

---

## ID Generation

Use short IDs that automatically grow on collision.

### Configuration (internal/utils/id.go)
```go
const (
    DefaultIDLength = 5      // Initial length
    MaxRetries      = 3      // Collisions before growing
    IDCharset       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)
```

### Usage
```go
// Generate short ID with collision check
tripID, err := utils.NewShortID(h.db, "trips", "id")

// For internal entities, use UUID
memberID := uuid.New()
```

### ID Type by Resource
| ID Type | Usage | Example |
|---------|-------|---------|
| Short ID | URL-exposed (trips, transactions, stores) | `abc12` |
| UUID | Internal (users, members, items) | `550e8400-e29b-41d4-a716-446655440000` |

---

## Authorization

Always verify ownership/access before operations:

```go
func (h *TripHandler) verifyTripAccess(tripID string, userID uuid.UUID) (*models.Trip, error) {
    // Check ownership or membership
}
```

---

## Summary

| Aspect | Convention |
|--------|-----------|
| URL | Plural nouns, kebab-case |
| Success | Return resource directly |
| Error | `gin.H{"error": "message"}` |
| Create | Return 201 + created resource |
| Update | Return 200 + updated resource |
| Delete | Return 200 + `gin.H{"message": "..."}` |
