# Go Testing 最佳实践

Go 语言测试框架的配置和最佳实践指南。

## 目录

- [项目配置](#项目配置)
- [测试结构](#测试结构)
- [断言最佳实践](#断言最佳实践)
- [表驱动测试](#表驱动测试)
- [Mock 策略](#mock-策略)
- [并发测试](#并发测试)
- [基准测试](#基准测试)
- [覆盖率配置](#覆盖率配置)

---

## 项目配置

### 推荐依赖

```go
// go.mod
module myproject

go 1.21

require (
    github.com/stretchr/testify v1.8.4
    github.com/golang/mock v1.6.0
    go.uber.org/mock v0.4.0
)
```

### 安装测试工具

```bash
# testify - 断言和 mock 库
go get github.com/stretchr/testify

# gomock - Google 的 mock 框架
go install go.uber.org/mock/mockgen@latest

# gotests - 自动生成测试
go install github.com/cweill/gotests/gotests@latest
```

### 目录结构

```
myproject/
├── user/
│   ├── service.go
│   ├── service_test.go      # 单元测试
│   ├── repository.go
│   └── repository_test.go
├── integration/
│   └── user_test.go         # 集成测试
├── testutil/
│   ├── fixtures.go          # 测试数据
│   └── helpers.go           # 测试辅助函数
└── mocks/
    └── user_repository.go   # 生成的 mock
```

---

## 测试结构

### 基本结构

```go
package user

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestUserService_CreateUser(t *testing.T) {
    // Arrange
    repo := NewInMemoryRepository()
    service := NewUserService(repo)
    request := CreateUserRequest{
        Email: "test@example.com",
        Name:  "Test User",
    }

    // Act
    user, err := service.CreateUser(request)

    // Assert
    require.NoError(t, err)
    assert.NotEmpty(t, user.ID)
    assert.Equal(t, "test@example.com", user.Email)
    assert.Equal(t, "Test User", user.Name)
}

func TestUserService_CreateUser_DuplicateEmail(t *testing.T) {
    // Arrange
    repo := NewInMemoryRepository()
    repo.Save(&User{Email: "existing@example.com"})
    service := NewUserService(repo)

    // Act
    _, err := service.CreateUser(CreateUserRequest{
        Email: "existing@example.com",
        Name:  "New User",
    })

    // Assert
    assert.Error(t, err)
    assert.ErrorIs(t, err, ErrDuplicateEmail)
}
```

### 子测试

```go
func TestUserService(t *testing.T) {
    t.Run("CreateUser", func(t *testing.T) {
        t.Run("should create user when input is valid", func(t *testing.T) {
            // ...
        })

        t.Run("should return error when email exists", func(t *testing.T) {
            // ...
        })
    })

    t.Run("GetUser", func(t *testing.T) {
        t.Run("should return user when exists", func(t *testing.T) {
            // ...
        })

        t.Run("should return error when not found", func(t *testing.T) {
            // ...
        })
    })
}
```

### 测试命名规范

```go
// ❌ 不好的命名
func TestCreate(t *testing.T) {}
func Test1(t *testing.T) {}

// ✅ 好的命名 - 函数名_场景_预期结果
func TestCreateUser_WhenInputValid_ReturnsUser(t *testing.T) {}
func TestCreateUser_WhenEmailExists_ReturnsError(t *testing.T) {}

// ✅ 好的命名 - 使用子测试描述
func TestCreateUser(t *testing.T) {
    t.Run("returns user when input is valid", func(t *testing.T) {})
    t.Run("returns error when email exists", func(t *testing.T) {})
}
```

---

## 断言最佳实践

### 使用 testify

```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestExample(t *testing.T) {
    // require - 失败时立即停止测试
    require.NotNil(t, result)  // 如果为 nil，后续断言不会执行

    // assert - 失败时继续执行
    assert.Equal(t, expected, actual)
    assert.NotEmpty(t, result.ID)
}
```

### 禁止弱断言

```go
// ❌ 弱断言 - 几乎不验证任何东西
assert.NotNil(t, result)
assert.NotEmpty(t, list)
assert.True(t, ok)

// ✅ 强断言 - 验证具体值
assert.Equal(t, "success", result.Status)
assert.Len(t, list, 3)
assert.Equal(t, expectedUser, result)
```

### 常用断言

```go
// 相等性
assert.Equal(t, expected, actual)
assert.NotEqual(t, unexpected, actual)
assert.EqualValues(t, expected, actual)  // 类型转换后比较

// 布尔值
assert.True(t, condition)
assert.False(t, condition)

// Nil 检查
assert.Nil(t, err)
assert.NotNil(t, result)

// 错误检查
assert.NoError(t, err)
assert.Error(t, err)
assert.ErrorIs(t, err, ErrNotFound)
assert.ErrorContains(t, err, "not found")

// 集合
assert.Len(t, slice, 3)
assert.Empty(t, slice)
assert.Contains(t, slice, item)
assert.ElementsMatch(t, expected, actual)  // 忽略顺序

// 字符串
assert.Contains(t, str, "substring")
assert.Regexp(t, regexp.MustCompile(`\d+`), str)

// 类型
assert.IsType(t, &User{}, result)

// JSON
assert.JSONEq(t, expectedJSON, actualJSON)
```

### 自定义错误消息

```go
assert.Equal(t, expected, actual, "user email should match")

assert.Truef(t, condition, "expected %s to be valid", input)

// 使用 require 确保关键断言
require.NoError(t, err, "failed to create user")
```

---

## 表驱动测试

### 基本表驱动测试

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name     string
        email    string
        expected bool
    }{
        {
            name:     "valid email",
            email:    "test@example.com",
            expected: true,
        },
        {
            name:     "missing @",
            email:    "testexample.com",
            expected: false,
        },
        {
            name:     "missing domain",
            email:    "test@",
            expected: false,
        },
        {
            name:     "empty string",
            email:    "",
            expected: false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := ValidateEmail(tt.email)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

### 包含错误的表驱动测试

```go
func TestUserService_GetUser(t *testing.T) {
    tests := []struct {
        name        string
        userID      int
        setupRepo   func(*MockRepository)
        expected    *User
        expectedErr error
    }{
        {
            name:   "returns user when exists",
            userID: 1,
            setupRepo: func(r *MockRepository) {
                r.On("FindByID", 1).Return(&User{ID: 1, Name: "Test"}, nil)
            },
            expected:    &User{ID: 1, Name: "Test"},
            expectedErr: nil,
        },
        {
            name:   "returns error when not found",
            userID: 999,
            setupRepo: func(r *MockRepository) {
                r.On("FindByID", 999).Return(nil, ErrNotFound)
            },
            expected:    nil,
            expectedErr: ErrNotFound,
        },
        {
            name:   "returns error when ID is negative",
            userID: -1,
            setupRepo: func(r *MockRepository) {
                // 不需要设置，验证发生在调用 repo 之前
            },
            expected:    nil,
            expectedErr: ErrInvalidID,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Arrange
            repo := new(MockRepository)
            tt.setupRepo(repo)
            service := NewUserService(repo)

            // Act
            result, err := service.GetUser(tt.userID)

            // Assert
            if tt.expectedErr != nil {
                assert.ErrorIs(t, err, tt.expectedErr)
                assert.Nil(t, result)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.expected, result)
            }

            repo.AssertExpectations(t)
        })
    }
}
```

### 并行表驱动测试

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        discount int
        expected float64
    }{
        {"no discount", 100, 0, 100},
        {"10% discount", 100, 10, 90},
        {"25% discount", 200, 25, 150},
        {"50% discount", 1000, 50, 500},
    }

    for _, tt := range tests {
        tt := tt  // 捕获循环变量
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // 并行执行

            result := CalculateDiscount(tt.price, tt.discount)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

---

## Mock 策略

### 使用 testify/mock

```go
// mocks/user_repository.go
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) Save(user *User) error {
    args := m.Called(user)
    return args.Error(0)
}

func (m *MockUserRepository) FindByID(id int) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) FindByEmail(email string) (*User, error) {
    args := m.Called(email)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}
```

### 使用 Mock

```go
func TestUserService_CreateUser(t *testing.T) {
    // Arrange
    repo := new(MockUserRepository)
    repo.On("FindByEmail", "test@example.com").Return(nil, ErrNotFound)
    repo.On("Save", mock.AnythingOfType("*user.User")).Return(nil)

    service := NewUserService(repo)

    // Act
    user, err := service.CreateUser(CreateUserRequest{
        Email: "test@example.com",
        Name:  "Test",
    })

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "test@example.com", user.Email)

    // 验证调用
    repo.AssertExpectations(t)
    repo.AssertCalled(t, "FindByEmail", "test@example.com")
    repo.AssertCalled(t, "Save", mock.AnythingOfType("*user.User"))
}
```

### 使用 gomock

```go
//go:generate mockgen -destination=mocks/user_repository.go -package=mocks . UserRepository

type UserRepository interface {
    Save(user *User) error
    FindByID(id int) (*User, error)
}
```

```go
func TestUserService_CreateUser_WithGoMock(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    // Arrange
    repo := mocks.NewMockUserRepository(ctrl)
    repo.EXPECT().FindByEmail("test@example.com").Return(nil, ErrNotFound)
    repo.EXPECT().Save(gomock.Any()).DoAndReturn(func(u *User) error {
        u.ID = 1
        return nil
    })

    service := NewUserService(repo)

    // Act
    user, err := service.CreateUser(CreateUserRequest{
        Email: "test@example.com",
        Name:  "Test",
    })

    // Assert
    require.NoError(t, err)
    assert.Equal(t, 1, user.ID)
}
```

### Mock HTTP 请求

```go
import (
    "net/http"
    "net/http/httptest"
)

func TestAPIClient_GetUser(t *testing.T) {
    // Arrange
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        assert.Equal(t, "/users/1", r.URL.Path)
        assert.Equal(t, "GET", r.Method)

        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"id": 1, "name": "Test"}`))
    }))
    defer server.Close()

    client := NewAPIClient(server.URL)

    // Act
    user, err := client.GetUser(1)

    // Assert
    require.NoError(t, err)
    assert.Equal(t, 1, user.ID)
    assert.Equal(t, "Test", user.Name)
}
```

---

## 并发测试

### 竞态检测

```bash
# 运行测试时启用竞态检测
go test -race ./...
```

### 并发安全测试

```go
func TestCounter_ConcurrentIncrement(t *testing.T) {
    counter := NewThreadSafeCounter()
    var wg sync.WaitGroup

    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }

    wg.Wait()
    assert.Equal(t, 100, counter.Value())
}

func TestCache_ConcurrentAccess(t *testing.T) {
    cache := NewCache()
    var wg sync.WaitGroup

    // 并发写入
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            cache.Set(fmt.Sprintf("key%d", i), i)
        }(i)
    }

    // 并发读取
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            cache.Get(fmt.Sprintf("key%d", i))
        }(i)
    }

    wg.Wait()
}
```

---

## 基准测试

### 基本基准测试

```go
func BenchmarkUserService_CreateUser(b *testing.B) {
    repo := NewInMemoryRepository()
    service := NewUserService(repo)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        service.CreateUser(CreateUserRequest{
            Email: fmt.Sprintf("user%d@example.com", i),
            Name:  "Test",
        })
    }
}

func BenchmarkHashPassword(b *testing.B) {
    password := "SecurePassword123"

    for i := 0; i < b.N; i++ {
        HashPassword(password)
    }
}
```

### 子基准测试

```go
func BenchmarkSort(b *testing.B) {
    sizes := []int{100, 1000, 10000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
            data := generateRandomSlice(size)
            b.ResetTimer()

            for i := 0; i < b.N; i++ {
                sort.Ints(data)
            }
        })
    }
}
```

### 内存基准测试

```go
func BenchmarkCreateUsers(b *testing.B) {
    b.ReportAllocs()  // 报告内存分配

    for i := 0; i < b.N; i++ {
        users := make([]*User, 1000)
        for j := 0; j < 1000; j++ {
            users[j] = &User{ID: j, Name: "Test"}
        }
    }
}
```

---

## 覆盖率配置

### 基本覆盖率

```bash
# 运行测试并生成覆盖率
go test -cover ./...

# 生成覆盖率文件
go test -coverprofile=coverage.out ./...

# 查看覆盖率报告
go tool cover -func=coverage.out

# 生成 HTML 报告
go tool cover -html=coverage.out -o coverage.html
```

### 覆盖率门禁脚本

```bash
#!/bin/bash
# scripts/check-coverage.sh

THRESHOLD=80

# 生成覆盖率报告
go test -coverprofile=coverage.out ./...

# 提取总覆盖率
COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')

echo "Total coverage: ${COVERAGE}%"

# 检查是否达到门禁
if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
    echo "Coverage ${COVERAGE}% is below threshold ${THRESHOLD}%"
    exit 1
fi

echo "Coverage check passed!"
```

### 排除文件

```go
// 在文件头部添加注释排除覆盖率统计
//go:build !coverage

package generated

// 或者使用构建标签
// go test -cover -tags=coverage ./...
```

---

## TestMain

### 全局 Setup/Teardown

```go
func TestMain(m *testing.M) {
    // 全局 setup
    db := setupTestDatabase()

    // 运行测试
    code := m.Run()

    // 全局 teardown
    db.Close()

    os.Exit(code)
}
```

### 集成测试标签

```go
//go:build integration

package integration

func TestMain(m *testing.M) {
    // 只在集成测试时运行
    container := startTestContainer()
    defer container.Stop()

    os.Exit(m.Run())
}
```

```bash
# 运行集成测试
go test -tags=integration ./integration/...
```

---

## 常用命令

```bash
# 运行所有测试
go test ./...

# 运行特定包
go test ./user/...

# 运行特定测试
go test -run TestUserService ./user

# 运行匹配模式的测试
go test -run "TestUserService.*Create" ./...

# 详细输出
go test -v ./...

# 启用竞态检测
go test -race ./...

# 覆盖率
go test -cover ./...
go test -coverprofile=coverage.out ./...

# 基准测试
go test -bench=. ./...
go test -bench=BenchmarkSort -benchmem ./...

# 短测试模式（跳过长时间测试）
go test -short ./...

# 超时设置
go test -timeout 30s ./...

# 并行度
go test -parallel 4 ./...
```

---

## 参考资源

- [Go Testing Package](https://pkg.go.dev/testing)
- [testify Documentation](https://github.com/stretchr/testify)
- [gomock Documentation](https://github.com/uber-go/mock)
- [Go Code Coverage](https://go.dev/blog/cover)
