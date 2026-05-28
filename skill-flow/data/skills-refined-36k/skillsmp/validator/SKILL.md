---
name: Validator
description: Struct validation using tags for Go.
metadata:
  labels: [golang, validator, validation]
  triggers:
    files: ['**/*.go']
    keywords: [validator, validate, binding, Validate]
---

# Validator Standards

## Basic Usage

```go
import (
    "github.com/go-playground/validator/v10"
)

var validate = validator.New()

type User struct {
    Name     string `validate:"required,min=2,max=100"`
    Email    string `validate:"required,email"`
    Age      int    `validate:"gte=0,lte=120"`
    Password string `validate:"required,min=8"`
}

func ValidateUser(user User) error {
    return validate.Struct(user)
}

// Error handling
err := validate.Struct(user)
if err != nil {
    for _, err := range err.(validator.ValidationErrors) {
        fmt.Printf("Field: %s, Tag: %s, Value: %v\n",
            err.Field(), err.Tag(), err.Value())
    }
}
```

## Common Validations

```go
type Request struct {
    // Required
    Name string `validate:"required"`

    // String length
    Title string `validate:"min=1,max=100"`

    // Numbers
    Age   int     `validate:"gte=0,lte=150"`
    Price float64 `validate:"gt=0"`

    // Email, URL
    Email   string `validate:"email"`
    Website string `validate:"url"`

    // UUID
    ID string `validate:"uuid4"`

    // Enum
    Status string `validate:"oneof=pending active completed"`

    // Contains
    Code string `validate:"contains=PREFIX"`

    // Regex (alpha, alphanum, numeric, etc.)
    Username string `validate:"alphanum,min=3,max=20"`

    // Date/Time
    StartDate string `validate:"datetime=2006-01-02"`
}
```

## Nested Structs

```go
type Address struct {
    Street  string `validate:"required"`
    City    string `validate:"required"`
    ZipCode string `validate:"required,len=5"`
}

type User struct {
    Name    string  `validate:"required"`
    Address Address `validate:"required"`  // Validates nested
}

type Company struct {
    Employees []User `validate:"required,min=1,dive"` // Validates each element
}

type Config struct {
    Settings map[string]string `validate:"required,dive,keys,required,endkeys,required"`
}
```

## Cross-Field Validation

```go
type DateRange struct {
    StartDate time.Time `validate:"required"`
    EndDate   time.Time `validate:"required,gtfield=StartDate"`
}

type PasswordChange struct {
    Password        string `validate:"required,min=8"`
    ConfirmPassword string `validate:"required,eqfield=Password"`
}

type Transfer struct {
    FromAccount string `validate:"required"`
    ToAccount   string `validate:"required,nefield=FromAccount"`
}
```

## Custom Validators

```go
func init() {
    validate.RegisterValidation("nowhitespace", noWhitespaceValidator)
    validate.RegisterValidation("strongpassword", strongPasswordValidator)
}

func noWhitespaceValidator(fl validator.FieldLevel) bool {
    return !strings.Contains(fl.Field().String(), " ")
}

func strongPasswordValidator(fl validator.FieldLevel) bool {
    password := fl.Field().String()
    hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
    hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
    hasNumber := regexp.MustCompile(`[0-9]`).MatchString(password)
    hasSpecial := regexp.MustCompile(`[!@#$%^&*]`).MatchString(password)
    return hasUpper && hasLower && hasNumber && hasSpecial
}

type User struct {
    Username string `validate:"required,nowhitespace"`
    Password string `validate:"required,min=8,strongpassword"`
}
```

## Conditional Validation

```go
type User struct {
    Type  string `validate:"required,oneof=personal business"`
    TaxID string `validate:"required_if=Type business"`
}

type Order struct {
    PaymentMethod string `validate:"required,oneof=card cash"`
    CardNumber    string `validate:"required_if=PaymentMethod card"`
}

// Other conditional tags:
// required_unless, required_with, required_without
// required_with_all, required_without_all
```

## Gin Integration

```go
import (
    "github.com/gin-gonic/gin"
    "github.com/gin-gonic/gin/binding"
    "github.com/go-playground/validator/v10"
)

func init() {
    if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
        v.RegisterValidation("customtag", customValidator)
    }
}

type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=2"`
    Email string `json:"email" binding:"required,email"`
}

func CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    // req is validated
}
```

## Error Translation

```go
import (
    "github.com/go-playground/locales/en"
    ut "github.com/go-playground/universal-translator"
    en_translations "github.com/go-playground/validator/v10/translations/en"
)

var (
    uni      *ut.UniversalTranslator
    trans    ut.Translator
    validate *validator.Validate
)

func init() {
    en := en.New()
    uni = ut.New(en, en)
    trans, _ = uni.GetTranslator("en")

    validate = validator.New()
    en_translations.RegisterDefaultTranslations(validate, trans)
}

func translateError(err error) []string {
    var messages []string
    for _, e := range err.(validator.ValidationErrors) {
        messages = append(messages, e.Translate(trans))
    }
    return messages
}
```

## Best Practices

1. **Singleton**: Create one validator instance
2. **Custom validators**: Register at init time
3. **Dive**: Use for slices and maps
4. **Translations**: Provide user-friendly messages
5. **Gin**: Use binding tags for automatic validation
