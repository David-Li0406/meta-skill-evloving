---
name: jikime-lang-go
description: Go 1.23+ development specialist covering Fiber, Gin, GORM, and concurrent programming patterns. Use when building high-performance microservices, CLI tools, or cloud-native applications.
version: 1.0.0
tags: ["language", "go", "fiber", "gin", "gorm", "microservices", "cloud-native"]
triggers:
  keywords: ["go", "golang", "fiber", "gin", "gorm", "goroutine", "고랭"]
  phases: ["run"]
  agents: ["backend"]
  languages: ["go"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Go Development Guide

Go 1.23+ 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| Web Framework | **Fiber** | 빠름, Express 스타일 |
| Web Framework | **Gin** | 인기, 미들웨어 풍부 |
| ORM | **GORM** | 풀 기능 ORM |
| SQL | **sqlc** | 타입 안전 SQL |

## Project Setup

```bash
# 새 프로젝트
go mod init github.com/user/project

# 주요 패키지
go get github.com/gofiber/fiber/v2
go get github.com/gin-gonic/gin
go get gorm.io/gorm gorm.io/driver/postgres
```

## Web Framework Patterns

### Fiber v2

```go
package main

import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New()

    app.Get("/api/users/:id", func(c *fiber.Ctx) error {
        id := c.Params("id")
        return c.JSON(fiber.Map{"id": id})
    })

    app.Listen(":3000")
}
```

### Gin

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()

    r.GET("/api/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        c.JSON(200, gin.H{"id": id})
    })

    r.Run(":3000")
}
```

## GORM Patterns

### Model Definition

```go
type User struct {
    gorm.Model
    Name  string `gorm:"uniqueIndex;not null"`
    Email string `gorm:"uniqueIndex;not null"`
    Posts []Post `gorm:"foreignKey:AuthorID"`
}

type Post struct {
    gorm.Model
    Title    string
    Content  string
    AuthorID uint
}
```

### CRUD Operations

```go
// Create
db.Create(&User{Name: "John", Email: "john@example.com"})

// Read
var user User
db.First(&user, 1)
db.Where("email = ?", "john@example.com").First(&user)

// Update
db.Model(&user).Update("Name", "Jane")

// Delete
db.Delete(&user, 1)
```

### Transaction

```go
db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&user).Error; err != nil {
        return err // rollback
    }
    if err := tx.Create(&profile).Error; err != nil {
        return err // rollback
    }
    return nil // commit
})
```

## Concurrency Patterns

### Goroutine with errgroup

```go
import "golang.org/x/sync/errgroup"

func processAll(ctx context.Context) error {
    g, ctx := errgroup.WithContext(ctx)

    g.Go(func() error { return processUsers(ctx) })
    g.Go(func() error { return processOrders(ctx) })

    return g.Wait()
}
```

### Channel Pattern

```go
func worker(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Start workers
    for w := 0; w < 3; w++ {
        go worker(jobs, results)
    }

    // Send jobs
    for j := 0; j < 5; j++ {
        jobs <- j
    }
    close(jobs)

    // Collect results
    for r := 0; r < 5; r++ {
        fmt.Println(<-results)
    }
}
```

## Testing

```go
// user_test.go
func TestUserService_Create(t *testing.T) {
    // Arrange
    service := NewUserService(mockDB)
    input := CreateUserInput{Name: "John", Email: "john@example.com"}

    // Act
    user, err := service.Create(input)

    // Assert
    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)
}

// Table-driven test
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
    }{
        {"positive", 5, 10},
        {"zero", 0, 0},
        {"negative", -5, -10},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Calculate(tt.input)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

## Project Structure

```
project/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   └── model/
├── pkg/
│   └── utils/
├── go.mod
└── go.sum
```

## Best Practices

- **Error Handling**: 항상 에러 반환하고 처리
- **Context**: 취소와 타임아웃에 context 사용
- **Defer**: 리소스 정리에 defer 사용
- **Interface**: 테스트를 위해 인터페이스로 추상화
- **Naming**: 짧고 명확한 이름 사용

---

Last Updated: 2026-01-21
Version: 2.0.0
