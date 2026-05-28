# Go

Use for Go projects with `testing`. Load when targeting Go unit tests. Table-driven tests recommended; keep subtests independent. Use GoDoc comments (`// Name ...`) for helpers.

```go
package main

import (
  "testing"
)

func TestFunctionName(t *testing.T) {
  tests := []struct {
    name     string
    input    InputType
    expected OutputType
    wantErr  bool
  }{
    {
      name:     "valid input returns expected",
      input:    validInput,
      expected: expectedOutput,
      wantErr:  false,
    },
    {
      name:     "empty input returns default",
      input:    emptyInput,
      expected: defaultValue,
      wantErr:  false,
    },
    {
      name:    "invalid input returns error",
      input:   invalidInput,
      wantErr: true,
    },
  }

  for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
      result, err := FunctionUnderTest(tt.input)
      if (err != nil) != tt.wantErr {
        t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
        return
      }
      if result != tt.expected {
        t.Errorf("got %v, want %v", result, tt.expected)
      }
    })
  }
}
```
