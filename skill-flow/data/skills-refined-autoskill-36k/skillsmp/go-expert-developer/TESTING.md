## Testing Instructions

### Table-Driven Tests

- Use standrd table-driven tests for all test cases.
- Use `t.Parallel()` to run allow tests to run concurrently.

```go
func TestValidateEmail(t *testing.T) {
    t.Parallel() // ✓ Use t.Parallel() for concurrency

    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {name: "valid", email: "user@example.com", wantErr: false},
        {name: "empty", email: "", wantErr: true},
        {name: "no @", email: "userexample.com", wantErr: true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // ✓ Use t.Parallel() for concurrency
            err := validateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("validateEmail(%q) error = %v, wantErr %v", tt.email, err, tt.wantErr)
            }
        })
    }
}
```

### Test Helpers

Use `t.Helper()` to improve test output:

```go
func assertUserEqual(t *testing.T, got, want *User) {
    t.Helper()  // ✓ Mark as test helper
    if got.ID != want.ID {
        t.Errorf("got ID %d, want %d", got.ID, want.ID)
    }
    if got.Email != want.Email {
        t.Errorf("got email %q, want %q", got.Email, want.Email)
    }
}
```

### Naming Conventions

- Test files should have the same base name as the file being tested
- Tests should be named `TestFunctionName` or `TestMethodName`
