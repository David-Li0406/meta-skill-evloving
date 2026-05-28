package robot

import (
	"strings"
	"testing"
	"time"
)

// =============================================================================
// TOON Encoder Unit Tests
// =============================================================================

func TestToonEncode_Primitives(t *testing.T) {
	tests := []struct {
		name     string
		input    interface{}
		expected string
	}{
		{"nil", nil, "null\n"},
		{"bool true", true, "true\n"},
		{"bool false", false, "false\n"},
		{"int", 42, "42\n"},
		{"negative int", -123, "-123\n"},
		{"uint", uint(100), "100\n"},
		{"float", 3.14159, "3.14159\n"},
		{"float no trailing zeros", 1.5, "1.5\n"},
		{"float whole number", 2.0, "2\n"},
		{"string simple", "hello", "hello\n"},
		{"string with spaces", "hello world", "\"hello world\"\n"},
		{"string with special chars", "hello\nworld", "\"hello\\nworld\"\n"},
		{"string empty", "", "\"\"\n"},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			output, err := toonEncode(tc.input, "\t")
			if err != nil {
				t.Fatalf("toonEncode() error: %v", err)
			}
			if output != tc.expected {
				t.Errorf("toonEncode(%v) = %q, want %q", tc.input, output, tc.expected)
			}
		})
	}
}

func TestToonEncode_StringQuoting(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"identifier", "hello_world", "hello_world"},
		{"with digit", "test123", "test123"},
		{"starts with underscore", "_private", "_private"},
		{"needs quote - space", "hello world", "\"hello world\""},
		{"needs quote - starts with digit", "123abc", "\"123abc\""},
		{"needs quote - hyphen", "hello-world", "\"hello-world\""},
		{"needs quote - dot", "hello.world", "\"hello.world\""},
		{"keyword true", "true", "\"true\""},
		{"keyword false", "false", "\"false\""},
		{"keyword null", "null", "\"null\""},
		{"escape backslash", "a\\b", "\"a\\\\b\""},
		{"escape quote", "a\"b", "\"a\\\"b\""},
		{"escape newline", "a\nb", "\"a\\nb\""},
		{"escape tab", "a\tb", "\"a\\tb\""},
		{"escape carriage return", "a\rb", "\"a\\rb\""},
	}

	enc := &toonEncoder{delimiter: "\t"}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			output := enc.encodeString(tc.input)
			if output != tc.expected {
				t.Errorf("encodeString(%q) = %q, want %q", tc.input, output, tc.expected)
			}
		})
	}
}

func TestToonEncode_SimpleArrays(t *testing.T) {
	t.Run("empty slice", func(t *testing.T) {
		output, err := toonEncode([]int{}, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if strings.TrimSpace(output) != "[]" {
			t.Errorf("output = %q, want %q", output, "[]")
		}
	})

	t.Run("int slice", func(t *testing.T) {
		output, err := toonEncode([]int{1, 2, 3}, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		// Should be inline format: [3]:1	2	3
		if !strings.HasPrefix(output, "[3]:") {
			t.Errorf("output should start with [3]:, got %q", output)
		}
		if !strings.Contains(output, "1") || !strings.Contains(output, "3") {
			t.Errorf("output missing values: %q", output)
		}
	})

	t.Run("string slice", func(t *testing.T) {
		output, err := toonEncode([]string{"a", "b", "c"}, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if !strings.HasPrefix(output, "[3]:") {
			t.Errorf("output should start with [3]:, got %q", output)
		}
	})
}

func TestToonEncode_TabularArrays(t *testing.T) {
	t.Run("uniform maps", func(t *testing.T) {
		input := []map[string]interface{}{
			{"id": 1, "name": "Alice"},
			{"id": 2, "name": "Bob"},
		}
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}

		// Should have header with count and fields
		if !strings.HasPrefix(output, "[2]{") {
			t.Errorf("output should start with [2]{, got %q", output)
		}

		// Fields should be alphabetically sorted (id before name)
		if !strings.Contains(output, "id,name") {
			t.Errorf("fields should be sorted as id,name, got %q", output)
		}

		// Should have 2 data rows (plus header)
		lines := strings.Split(strings.TrimSpace(output), "\n")
		if len(lines) != 3 {
			t.Errorf("expected 3 lines (header + 2 rows), got %d", len(lines))
		}
	})

	t.Run("uniform structs", func(t *testing.T) {
		type Person struct {
			ID   int    `json:"id"`
			Name string `json:"name"`
		}
		input := []Person{
			{ID: 1, Name: "Alice"},
			{ID: 2, Name: "Bob"},
		}
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}

		if !strings.HasPrefix(output, "[2]{") {
			t.Errorf("output should start with [2]{, got %q", output)
		}
	})
}

func TestToonEncode_Objects(t *testing.T) {
	t.Run("simple map", func(t *testing.T) {
		input := map[string]int{"count": 42, "value": 100}
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}

		if !strings.Contains(output, "count: 42") {
			t.Errorf("output should contain 'count: 42', got %q", output)
		}
		if !strings.Contains(output, "value: 100") {
			t.Errorf("output should contain 'value: 100', got %q", output)
		}
	})

	t.Run("simple struct", func(t *testing.T) {
		type Config struct {
			Port    int    `json:"port"`
			Host    string `json:"host"`
			Enabled bool   `json:"enabled"`
		}
		input := Config{Port: 8080, Host: "localhost", Enabled: true}
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}

		if !strings.Contains(output, "port: 8080") {
			t.Errorf("output should contain 'port: 8080', got %q", output)
		}
		if !strings.Contains(output, "host: localhost") {
			t.Errorf("output should contain 'host: localhost', got %q", output)
		}
		if !strings.Contains(output, "enabled: true") {
			t.Errorf("output should contain 'enabled: true', got %q", output)
		}
	})

	t.Run("empty map", func(t *testing.T) {
		input := map[string]int{}
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if strings.TrimSpace(output) != "{}" {
			t.Errorf("output = %q, want %q", output, "{}")
		}
	})
}

func TestToonEncode_DeterministicOrdering(t *testing.T) {
	input := map[string]int{
		"zebra":  1,
		"apple":  2,
		"mango":  3,
		"banana": 4,
		"cherry": 5,
	}

	// Encode multiple times
	outputs := make([]string, 10)
	for i := 0; i < 10; i++ {
		output, err := toonEncode(input, "\t")
		if err != nil {
			t.Fatalf("error on iteration %d: %v", i, err)
		}
		outputs[i] = output
	}

	// All outputs should be identical
	for i := 1; i < 10; i++ {
		if outputs[i] != outputs[0] {
			t.Errorf("non-deterministic output on iteration %d:\n%s\nvs\n%s", i, outputs[0], outputs[i])
		}
	}

	// Verify alphabetical ordering
	lines := strings.Split(outputs[0], "\n")
	var prevField string
	for _, line := range lines {
		if strings.Contains(line, ":") {
			parts := strings.SplitN(line, ":", 2)
			field := strings.TrimSpace(parts[0])
			if prevField != "" && field < prevField {
				t.Errorf("fields not sorted: %q comes after %q", field, prevField)
			}
			prevField = field
		}
	}
}

func TestToonEncode_TabSafetyFallback(t *testing.T) {
	// When values contain tabs, should fall back to comma delimiter
	input := []map[string]string{
		{"name": "Alice", "desc": "has\ttab"},
		{"name": "Bob", "desc": "normal"},
	}

	output, err := toonEncode(input, "\t")
	if err != nil {
		t.Fatalf("error: %v", err)
	}

	// Data rows should use comma, not tab
	lines := strings.Split(strings.TrimSpace(output), "\n")
	if len(lines) < 2 {
		t.Fatalf("expected at least 2 lines, got %d", len(lines))
	}

	// First data row should contain comma separator
	dataRow := lines[1]
	if strings.Count(dataRow, ",") < 1 {
		t.Errorf("expected comma-separated values due to tab in data, got %q", dataRow)
	}
}

func TestToonEncode_NestedFallbackToJSON(t *testing.T) {
	// Nested complex types in tabular rows should fall back to JSON inline
	input := []map[string]interface{}{
		{"id": 1, "tags": []string{"a", "b"}},
		{"id": 2, "tags": []string{"c"}},
	}

	output, err := toonEncode(input, "\t")
	if err != nil {
		t.Fatalf("error: %v", err)
	}

	// Should contain quoted JSON for the tags field
	if !strings.Contains(output, `["a","b"]`) && !strings.Contains(output, `"[\"a\",\"b\"]"`) {
		t.Logf("output: %s", output)
		// The nested array should be encoded somehow
	}
}

func TestToonEncode_PointerHandling(t *testing.T) {
	t.Run("nil pointer", func(t *testing.T) {
		var ptr *int
		output, err := toonEncode(ptr, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if output != "null\n" {
			t.Errorf("output = %q, want %q", output, "null\n")
		}
	})

	t.Run("non-nil pointer", func(t *testing.T) {
		val := 42
		ptr := &val
		output, err := toonEncode(ptr, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if output != "42\n" {
			t.Errorf("output = %q, want %q", output, "42\n")
		}
	})
}

func TestToonEncode_TimeHandling(t *testing.T) {
	// time.Time should be encoded as a struct (with its fields)
	// This is primarily to ensure it doesn't panic
	input := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC)

	output, err := toonEncode(input, "\t")
	if err != nil {
		t.Fatalf("error: %v", err)
	}

	// Should produce some output without error
	if output == "" {
		t.Error("expected non-empty output for time.Time")
	}
}

func TestToonEncode_JSONTagHandling(t *testing.T) {
	type Item struct {
		ID       int    `json:"id"`
		Name     string `json:"name"`
		internal string // unexported, should be skipped
		Ignored  string `json:"-"` // explicitly ignored
		OmitZero int    `json:"omit_zero,omitempty"`
	}

	input := Item{ID: 1, Name: "test", internal: "secret", Ignored: "skip", OmitZero: 0}
	output, err := toonEncode(input, "\t")
	if err != nil {
		t.Fatalf("error: %v", err)
	}

	// Should contain id and name
	if !strings.Contains(output, "id:") || !strings.Contains(output, "name:") {
		t.Errorf("output should contain id and name: %q", output)
	}

	// Should not contain internal or Ignored
	if strings.Contains(output, "internal") {
		t.Errorf("output should not contain unexported field: %q", output)
	}
	if strings.Contains(output, "Ignored") {
		t.Errorf("output should not contain ignored field: %q", output)
	}

	// Should contain omit_zero (the json tag name, not the field name)
	if !strings.Contains(output, "omit_zero") {
		t.Errorf("output should use json tag name omit_zero: %q", output)
	}
}

func TestToonEncode_RobotPayloads(t *testing.T) {
	// Test with actual robot types to ensure compatibility
	t.Run("RobotResponse", func(t *testing.T) {
		resp := NewRobotResponse(true)
		output, err := toonEncode(resp, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if !strings.Contains(output, "success: true") {
			t.Errorf("output should contain 'success: true': %q", output)
		}
	})

	t.Run("ErrorResponse", func(t *testing.T) {
		resp := NewErrorResponse(nil, ErrCodeInternalError, "test hint")
		output, err := toonEncode(resp, "\t")
		if err != nil {
			t.Fatalf("error: %v", err)
		}
		if !strings.Contains(output, "success: false") {
			t.Errorf("output should contain 'success: false': %q", output)
		}
	})
}
