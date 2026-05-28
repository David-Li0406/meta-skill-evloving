# Validator Validation Tags

## Basic Usage

```go
import (
    "github.com/go-playground/validator/v10"
)

type User struct {
    Name     string `validate:"required,min=2,max=100"`
    Email    string `validate:"required,email"`
    Age      int    `validate:"gte=0,lte=130"`
    Password string `validate:"required,min=8"`
}

func main() {
    validate := validator.New()

    user := User{
        Name:     "J",
        Email:    "invalid",
        Age:      -1,
        Password: "short",
    }

    err := validate.Struct(user)
    if err != nil {
        for _, err := range err.(validator.ValidationErrors) {
            fmt.Printf("Field: %s, Tag: %s, Value: %v\n",
                err.Field(), err.Tag(), err.Value())
        }
    }
}
```

## Common Tags

```go
type Example struct {
    // Required fields
    Required    string `validate:"required"`
    RequiredIf  string `validate:"required_if=Type email"`
    RequiredWith string `validate:"required_with=Other"`
    
    // String length
    MinLen      string `validate:"min=3"`
    MaxLen      string `validate:"max=100"`
    Len         string `validate:"len=10"`
    
    // Numeric ranges
    Gt          int    `validate:"gt=0"`
    Gte         int    `validate:"gte=1"`
    Lt          int    `validate:"lt=100"`
    Lte         int    `validate:"lte=99"`
    
    // Format validators
    Email       string `validate:"email"`
    URL         string `validate:"url"`
    UUID        string `validate:"uuid"`
    IP          string `validate:"ip"`
    IPv4        string `validate:"ipv4"`
    
    // Comparisons
    Eq          string `validate:"eq=admin"`
    Ne          string `validate:"ne=guest"`
    OneOf       string `validate:"oneof=red green blue"`
    
    // Content
    Alpha       string `validate:"alpha"`
    Alphanum    string `validate:"alphanum"`
    Numeric     string `validate:"numeric"`
    Contains    string `validate:"contains=@"`
    StartsWith  string `validate:"startswith=prefix_"`
    EndsWith    string `validate:"endswith=_suffix"`
}
```

## Nested Validation

```go
type Address struct {
    Street  string `validate:"required"`
    City    string `validate:"required"`
    ZipCode string `validate:"required,numeric,len=5"`
}

type User struct {
    Name    string  `validate:"required"`
    Address Address `validate:"required"` // Validates nested struct
}

// Slice validation with dive
type Order struct {
    Items []OrderItem `validate:"required,dive"` // Validates each item
}

type OrderItem struct {
    ProductID string `validate:"required,uuid"`
    Quantity  int    `validate:"required,gt=0"`
}

// Map validation
type Config struct {
    Settings map[string]string `validate:"dive,keys,required,endkeys,required"`
}
```

## Custom Validators

```go
func main() {
    validate := validator.New()

    // Custom validation function
    validate.RegisterValidation("strongpassword", func(fl validator.FieldLevel) bool {
        password := fl.Field().String()
        hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
        hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
        hasNumber := regexp.MustCompile(`[0-9]`).MatchString(password)
        return len(password) >= 8 && hasUpper && hasLower && hasNumber
    })

    type User struct {
        Password string `validate:"required,strongpassword"`
    }
}
```

## Conditional Validation

```go
type Payment struct {
    Type       string `validate:"required,oneof=card bank crypto"`
    CardNumber string `validate:"required_if=Type card,omitempty,credit_card"`
    BankAccount string `validate:"required_if=Type bank,omitempty"`
    WalletAddress string `validate:"required_if=Type crypto,omitempty"`
}

type User struct {
    Type     string `validate:"required,oneof=individual company"`
    // Required only if Type is "company"
    CompanyName string `validate:"required_if=Type company"`
    TaxID       string `validate:"required_if=Type company"`
}
```

## Error Handling

```go
func validateAndRespond(w http.ResponseWriter, data interface{}) error {
    if err := validate.Struct(data); err != nil {
        var errors []string
        
        for _, err := range err.(validator.ValidationErrors) {
            field := err.Field()
            tag := err.Tag()
            param := err.Param()
            
            var message string
            switch tag {
            case "required":
                message = fmt.Sprintf("%s is required", field)
            case "email":
                message = fmt.Sprintf("%s must be a valid email", field)
            case "min":
                message = fmt.Sprintf("%s must be at least %s characters", field, param)
            case "max":
                message = fmt.Sprintf("%s must be at most %s characters", field, param)
            default:
                message = fmt.Sprintf("%s failed validation: %s", field, tag)
            }
            
            errors = append(errors, message)
        }
        
        return fmt.Errorf("validation failed: %v", errors)
    }
    
    return nil
}
```

## Integration with Gin/Echo

```go
// Gin
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=2"`
    Email string `json:"email" binding:"required,email"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
}

// Echo (custom validator)
type CustomValidator struct {
    validator *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
    return cv.validator.Struct(i)
}

e.Validator = &CustomValidator{validator: validator.New()}
```
