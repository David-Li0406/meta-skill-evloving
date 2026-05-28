---
name: backend-api-design
description: Use this skill when designing and implementing backend APIs to ensure consistency and best practices.
---

# Backend API Design

Guidelines and patterns for designing and implementing backend APIs effectively.

## URL Naming Conventions

- Use **plural nouns** for resources: `/trips`, `/ledgers`, `/transactions`
- Use **kebab-case** for multi-word resources: `/trip-members`
- Nested resources follow parent: `/ledgers/{id}/transactions`
- Use **path parameters** for IDs: `/trips/{id}`
- Use **query parameters** for filtering: `/transactions?category=food`

## HTTP Methods and Response Codes

| Method | Usage | Response Code |
|--------|-------|---------------|
| `GET` | Retrieve resource(s) | 200 OK |
| `POST` | Create resource | 201 Created |
| `PUT` | Update resource (full) | 200 OK |
| `PATCH` | Update resource (partial) | 200 OK |
| `DELETE` | Delete resource | 200 OK |

## Request Body Structures

### Create Request Example
```go
type CreateTripRequest struct {
    Name        string     `json:"name" binding:"required,min=1,max=100"`
    Description string     `json:"description"`
    StartDate   *time.Time `json:"start_date"`
}
```

### Update Request Example
```go
type UpdateTripRequest struct {
    Name        string     `json:"name" binding:"omitempty,min=1,max=100"`
    Description string     `json:"description"`
}
```

**Rules:**
- For create requests, use `binding:"required"` for mandatory fields.
- For update requests, use `binding:"omitempty"` for optional fields.
- Use pointers for optional fields to distinguish between "not provided" and "zero value".

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
Use a consistent error format:

```go
c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
c.JSON(http.StatusNotFound, gin.H{"error": "Trip not found"})
c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create trip"})
```

### Delete Response
```go
c.JSON(http.StatusOK, gin.H{"message": "Trip deleted"})
```

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

## Handler Structure Example

```go
type TripHandler struct {
    db *gorm.DB
}
```