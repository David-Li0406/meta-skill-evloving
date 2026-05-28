# Testify Assert Patterns

## Assertions

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestUserService(t *testing.T) {
    // Basic assertions (non-fatal, continues on failure)
    assert.Equal(t, expected, actual)
    assert.NotEqual(t, expected, actual)
    assert.True(t, condition)
    assert.False(t, condition)
    assert.Nil(t, value)
    assert.NotNil(t, value)
    assert.Empty(t, slice)
    assert.NotEmpty(t, slice)
    assert.Len(t, slice, 5)
    assert.Contains(t, slice, element)
    assert.ElementsMatch(t, expected, actual)

    // Require (fatal, stops on failure)
    require.NoError(t, err)
    require.NotNil(t, user)
    
    // Error assertions
    assert.Error(t, err)
    assert.NoError(t, err)
    assert.ErrorIs(t, err, ErrNotFound)
    assert.ErrorContains(t, err, "not found")

    // Type assertions
    assert.IsType(t, &User{}, obj)
    assert.Implements(t, (*io.Reader)(nil), obj)

    // Numeric comparisons
    assert.Greater(t, 5, 3)
    assert.GreaterOrEqual(t, 5, 5)
    assert.Less(t, 3, 5)
    assert.InDelta(t, 3.14, result, 0.01)

    // String assertions
    assert.Regexp(t, `^[a-z]+$`, str)
    assert.JSONEq(t, `{"name":"John"}`, jsonStr)
}
```

## Table-Driven Tests

```go
func TestCalculator_Add(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed numbers", -2, 3, 1},
        {"zeros", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

## Test Suites

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type UserServiceTestSuite struct {
    suite.Suite
    db      *Database
    service *UserService
}

// Run before each test
func (s *UserServiceTestSuite) SetupTest() {
    s.db = NewTestDatabase()
    s.service = NewUserService(s.db)
}

// Run after each test
func (s *UserServiceTestSuite) TearDownTest() {
    s.db.Close()
}

// Run once before all tests
func (s *UserServiceTestSuite) SetupSuite() {
    // Initialize shared resources
}

func (s *UserServiceTestSuite) TestCreateUser() {
    user, err := s.service.Create("John", "john@example.com")
    
    s.NoError(err)
    s.NotNil(user)
    s.Equal("John", user.Name)
}

func (s *UserServiceTestSuite) TestFindUser() {
    // Setup
    s.db.Insert(&User{ID: 1, Name: "John"})
    
    // Test
    user, err := s.service.FindByID(1)
    
    // Assert
    s.Require().NoError(err)
    s.Equal("John", user.Name)
}

// Run the suite
func TestUserServiceTestSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

## Mocking

```go
import "github.com/stretchr/testify/mock"

type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByID(id int) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Save(user *User) error {
    args := m.Called(user)
    return args.Error(0)
}

func TestUserService_GetUser(t *testing.T) {
    // Setup mock
    mockRepo := new(MockUserRepository)
    mockRepo.On("FindByID", 1).Return(&User{ID: 1, Name: "John"}, nil)
    
    service := NewUserService(mockRepo)
    
    // Test
    user, err := service.GetUser(1)
    
    // Assert
    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)
    mockRepo.AssertExpectations(t)
    mockRepo.AssertCalled(t, "FindByID", 1)
}
```
