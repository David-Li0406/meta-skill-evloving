package robot

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"
)

// =============================================================================
// RobotFormat Tests
// =============================================================================

func TestRobotFormatString(t *testing.T) {
	tests := []struct {
		format   RobotFormat
		expected string
	}{
		{FormatJSON, "json"},
		{FormatTOON, "toon"},
		{FormatAuto, "auto"},
	}

	for _, tc := range tests {
		t.Run(tc.expected, func(t *testing.T) {
			if got := tc.format.String(); got != tc.expected {
				t.Errorf("RobotFormat.String() = %q, want %q", got, tc.expected)
			}
		})
	}
}

func TestRobotFormatIsValid(t *testing.T) {
	tests := []struct {
		format RobotFormat
		valid  bool
	}{
		{FormatJSON, true},
		{FormatTOON, true},
		{FormatAuto, true},
		{RobotFormat("yaml"), false},
		{RobotFormat("xml"), false},
		{RobotFormat(""), false},
	}

	for _, tc := range tests {
		t.Run(string(tc.format), func(t *testing.T) {
			if got := tc.format.IsValid(); got != tc.valid {
				t.Errorf("RobotFormat(%q).IsValid() = %v, want %v", tc.format, got, tc.valid)
			}
		})
	}
}

func TestParseRobotFormat(t *testing.T) {
	tests := []struct {
		input    string
		expected RobotFormat
		wantErr  bool
	}{
		{"json", FormatJSON, false},
		{"toon", FormatTOON, false},
		{"auto", FormatAuto, false},
		{"", FormatAuto, false}, // Empty defaults to auto
		{"yaml", "", true},
		{"XML", "", true},
		{"JSON", "", true}, // Case sensitive
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			got, err := ParseRobotFormat(tc.input)
			if tc.wantErr {
				if err == nil {
					t.Errorf("ParseRobotFormat(%q) should return error", tc.input)
				}
				return
			}
			if err != nil {
				t.Errorf("ParseRobotFormat(%q) unexpected error: %v", tc.input, err)
				return
			}
			if got != tc.expected {
				t.Errorf("ParseRobotFormat(%q) = %q, want %q", tc.input, got, tc.expected)
			}
		})
	}
}

// =============================================================================
// JSON Renderer Tests
// =============================================================================

func TestNewJSONRenderer(t *testing.T) {
	r := NewJSONRenderer()
	if r == nil {
		t.Fatal("NewJSONRenderer() returned nil")
	}
	if r.Indent != "  " {
		t.Errorf("default indent = %q, want %q", r.Indent, "  ")
	}
}

func TestJSONRendererRender(t *testing.T) {
	r := NewJSONRenderer()

	t.Run("simple struct", func(t *testing.T) {
		payload := struct {
			Name  string `json:"name"`
			Count int    `json:"count"`
		}{
			Name:  "test",
			Count: 42,
		}

		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		// Verify valid JSON
		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("output is not valid JSON: %v", err)
		}

		if parsed["name"] != "test" {
			t.Errorf("name = %v, want %q", parsed["name"], "test")
		}
		if parsed["count"] != float64(42) {
			t.Errorf("count = %v, want %v", parsed["count"], 42)
		}
	})

	t.Run("RobotResponse", func(t *testing.T) {
		payload := NewRobotResponse(true)
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("output is not valid JSON: %v", err)
		}

		if parsed["success"] != true {
			t.Error("expected success to be true")
		}
		if parsed["timestamp"] == nil {
			t.Error("expected timestamp to be present")
		}
	})

	t.Run("pretty printed", func(t *testing.T) {
		payload := map[string]string{"key": "value"}
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		// Should contain newlines (pretty printed)
		if !strings.Contains(output, "\n") {
			t.Error("expected pretty-printed output with newlines")
		}
		// Should contain indentation
		if !strings.Contains(output, "  ") {
			t.Error("expected indentation in output")
		}
	})

	t.Run("custom indent", func(t *testing.T) {
		r := &JSONRenderer{Indent: "\t"}
		payload := map[string]string{"key": "value"}
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		if !strings.Contains(output, "\t") {
			t.Error("expected tab indentation")
		}
	})

	t.Run("nil payload", func(t *testing.T) {
		output, err := r.Render(nil)
		if err != nil {
			t.Fatalf("Render(nil) error: %v", err)
		}
		if strings.TrimSpace(output) != "null" {
			t.Errorf("Render(nil) = %q, want %q", output, "null")
		}
	})

	t.Run("empty array", func(t *testing.T) {
		output, err := r.Render([]string{})
		if err != nil {
			t.Fatalf("Render([]) error: %v", err)
		}
		if strings.TrimSpace(output) != "[]" {
			t.Errorf("Render([]) = %q, want %q", output, "[]")
		}
	})
}

func TestJSONRendererContentType(t *testing.T) {
	r := NewJSONRenderer()
	ct := r.ContentType()
	if ct != "application/json" {
		t.Errorf("ContentType() = %q, want %q", ct, "application/json")
	}
}

func TestJSONRendererFormat(t *testing.T) {
	r := NewJSONRenderer()
	f := r.Format()
	if f != FormatJSON {
		t.Errorf("Format() = %q, want %q", f, FormatJSON)
	}
}

// =============================================================================
// TOON Renderer Tests
// =============================================================================

func TestNewTOONRenderer(t *testing.T) {
	r := NewTOONRenderer()
	if r == nil {
		t.Fatal("NewTOONRenderer() returned nil")
	}
	if r.Delimiter != "\t" {
		t.Errorf("default delimiter = %q, want %q", r.Delimiter, "\t")
	}
}

func TestTOONRendererRenderSimpleObject(t *testing.T) {
	r := NewTOONRenderer()
	payload := map[string]string{"key": "value"}

	output, err := r.Render(payload)
	if err != nil {
		t.Fatalf("TOON Render() error: %v", err)
	}

	// Output should contain the key-value pair
	if !strings.Contains(output, "key:") || !strings.Contains(output, "value") {
		t.Errorf("TOON output missing expected content: %q", output)
	}
}

func TestTOONRendererRenderArray(t *testing.T) {
	r := NewTOONRenderer()

	t.Run("array of objects", func(t *testing.T) {
		payload := []map[string]interface{}{
			{"id": 1, "name": "Alice"},
			{"id": 2, "name": "Bob"},
		}
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("TOON Render() error: %v", err)
		}
		// Should have tabular header with field names
		if !strings.Contains(output, "[2]{") {
			t.Errorf("TOON output missing array header: %q", output)
		}
		// Should contain field names (alphabetically sorted)
		if !strings.Contains(output, "id") || !strings.Contains(output, "name") {
			t.Errorf("TOON output missing field names: %q", output)
		}
	})

	t.Run("primitive array", func(t *testing.T) {
		payload := []int{1, 2, 3}
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("TOON Render() error: %v", err)
		}
		// Should have inline format
		if !strings.Contains(output, "[3]:") {
			t.Errorf("TOON output missing array inline format: %q", output)
		}
	})

	t.Run("empty array", func(t *testing.T) {
		payload := []string{}
		output, err := r.Render(payload)
		if err != nil {
			t.Fatalf("TOON Render() error: %v", err)
		}
		if strings.TrimSpace(output) != "[]" {
			t.Errorf("TOON empty array output = %q, want %q", output, "[]")
		}
	})
}

func TestTOONRendererRenderPrimitives(t *testing.T) {
	r := NewTOONRenderer()

	tests := []struct {
		name     string
		payload  interface{}
		expected string
	}{
		{"nil", nil, "null\n"},
		{"true", true, "true\n"},
		{"false", false, "false\n"},
		{"int", 42, "42\n"},
		{"float", 3.14, "3.14\n"},
		{"string identifier", "hello", "hello\n"},
		{"string with spaces", "hello world", "\"hello world\"\n"},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			output, err := r.Render(tc.payload)
			if err != nil {
				t.Fatalf("TOON Render() error: %v", err)
			}
			if output != tc.expected {
				t.Errorf("TOON Render(%v) = %q, want %q", tc.payload, output, tc.expected)
			}
		})
	}
}

func TestTOONRendererDeterministicOrder(t *testing.T) {
	r := NewTOONRenderer()
	payload := map[string]int{
		"zebra":  1,
		"apple":  2,
		"banana": 3,
	}

	// Render multiple times to verify deterministic output
	output1, _ := r.Render(payload)
	output2, _ := r.Render(payload)
	output3, _ := r.Render(payload)

	if output1 != output2 || output2 != output3 {
		t.Errorf("TOON output not deterministic:\n%s\nvs\n%s", output1, output2)
	}

	// Fields should be alphabetically sorted
	appleIdx := strings.Index(output1, "apple")
	bananaIdx := strings.Index(output1, "banana")
	zebraIdx := strings.Index(output1, "zebra")

	if appleIdx > bananaIdx || bananaIdx > zebraIdx {
		t.Errorf("TOON fields not alphabetically sorted: %s", output1)
	}
}

func TestTOONRendererContentType(t *testing.T) {
	r := NewTOONRenderer()
	ct := r.ContentType()
	if ct != "text/x-toon" {
		t.Errorf("ContentType() = %q, want %q", ct, "text/x-toon")
	}
}

func TestTOONRendererFormat(t *testing.T) {
	r := NewTOONRenderer()
	f := r.Format()
	if f != FormatTOON {
		t.Errorf("Format() = %q, want %q", f, FormatTOON)
	}
}

// =============================================================================
// Global Render Function Tests
// =============================================================================

func TestRender(t *testing.T) {
	payload := struct {
		Message string `json:"message"`
	}{
		Message: "hello",
	}

	t.Run("FormatJSON", func(t *testing.T) {
		output, err := Render(payload, FormatJSON)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("output is not valid JSON: %v", err)
		}
		if parsed["message"] != "hello" {
			t.Errorf("message = %v, want %q", parsed["message"], "hello")
		}
	})

	t.Run("FormatTOON renders successfully", func(t *testing.T) {
		output, err := Render(payload, FormatTOON)
		if err != nil {
			t.Fatalf("Render() with TOON error: %v", err)
		}
		// TOON output should contain the message field
		if !strings.Contains(output, "message") || !strings.Contains(output, "hello") {
			t.Errorf("TOON output missing expected content: %q", output)
		}
	})

	t.Run("FormatAuto defaults to JSON", func(t *testing.T) {
		output, err := Render(payload, FormatAuto)
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("output should be valid JSON (auto defaults to JSON): %v", err)
		}
	})

	t.Run("unknown format defaults to JSON", func(t *testing.T) {
		output, err := Render(payload, RobotFormat("unknown"))
		if err != nil {
			t.Fatalf("Render() error: %v", err)
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("unknown format should fall back to JSON: %v", err)
		}
	})
}

func TestGetRenderer(t *testing.T) {
	tests := []struct {
		format       RobotFormat
		expectedType string
	}{
		{FormatJSON, "*robot.JSONRenderer"},
		{FormatTOON, "*robot.TOONRenderer"},
		{FormatAuto, "*robot.JSONRenderer"},             // Auto defaults to JSON
		{RobotFormat("invalid"), "*robot.JSONRenderer"}, // Invalid falls back to JSON
	}

	for _, tc := range tests {
		t.Run(string(tc.format), func(t *testing.T) {
			r := GetRenderer(tc.format)
			if r == nil {
				t.Fatal("GetRenderer() returned nil")
			}
			// Check it's a valid renderer by calling a method
			_ = r.ContentType()
		})
	}
}

func TestGetContentType(t *testing.T) {
	tests := []struct {
		format      RobotFormat
		contentType string
	}{
		{FormatJSON, "application/json"},
		{FormatTOON, "text/x-toon"},
		{FormatAuto, "application/json"}, // Auto defaults to JSON
	}

	for _, tc := range tests {
		t.Run(string(tc.format), func(t *testing.T) {
			ct := GetContentType(tc.format)
			if ct != tc.contentType {
				t.Errorf("GetContentType(%q) = %q, want %q", tc.format, ct, tc.contentType)
			}
		})
	}
}

// =============================================================================
// Output Helper Tests
// =============================================================================

func TestOutputTo(t *testing.T) {
	payload := map[string]int{"count": 5}

	t.Run("writes to buffer", func(t *testing.T) {
		var buf bytes.Buffer
		err := OutputTo(&buf, payload, FormatJSON)
		if err != nil {
			t.Fatalf("OutputTo() error: %v", err)
		}

		output := buf.String()
		if output == "" {
			t.Error("expected non-empty output")
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(output), &parsed); err != nil {
			t.Fatalf("output is not valid JSON: %v", err)
		}
	})

	t.Run("TOON writes to buffer", func(t *testing.T) {
		var buf bytes.Buffer
		err := OutputTo(&buf, payload, FormatTOON)
		if err != nil {
			t.Fatalf("OutputTo() with TOON error: %v", err)
		}
		output := buf.String()
		if output == "" {
			t.Error("expected non-empty output")
		}
		if !strings.Contains(output, "count") {
			t.Errorf("TOON output missing expected content: %q", output)
		}
	})
}

// =============================================================================
// RenderResult Tests
// =============================================================================

func TestRenderWithMeta(t *testing.T) {
	payload := struct {
		Data string `json:"data"`
	}{
		Data: "test",
	}

	t.Run("JSON format", func(t *testing.T) {
		result, err := RenderWithMeta(payload, FormatJSON)
		if err != nil {
			t.Fatalf("RenderWithMeta() error: %v", err)
		}

		if result.Output == "" {
			t.Error("expected non-empty output")
		}
		if result.ContentType != "application/json" {
			t.Errorf("ContentType = %q, want %q", result.ContentType, "application/json")
		}
		if result.Format != FormatJSON {
			t.Errorf("Format = %q, want %q", result.Format, FormatJSON)
		}

		// Verify output is valid JSON
		var parsed map[string]interface{}
		if err := json.Unmarshal([]byte(result.Output), &parsed); err != nil {
			t.Fatalf("output is not valid JSON: %v", err)
		}
	})

	t.Run("TOON format", func(t *testing.T) {
		result, err := RenderWithMeta(payload, FormatTOON)
		if err != nil {
			t.Fatalf("RenderWithMeta() with TOON error: %v", err)
		}
		if result.Output == "" {
			t.Error("expected non-empty output")
		}
		if result.ContentType != "text/x-toon" {
			t.Errorf("ContentType = %q, want %q", result.ContentType, "text/x-toon")
		}
		if result.Format != FormatTOON {
			t.Errorf("Format = %q, want %q", result.Format, FormatTOON)
		}
		if !strings.Contains(result.Output, "data") {
			t.Errorf("TOON output missing expected content: %q", result.Output)
		}
	})
}

// =============================================================================
// Backward Compatibility Tests
// =============================================================================

// TestJSONRendererMatchesEncodeJSON verifies that the JSON renderer produces
// output identical to the existing encodeJSON function.
func TestJSONRendererMatchesEncodeJSON(t *testing.T) {
	testCases := []struct {
		name    string
		payload interface{}
	}{
		{"RobotResponse", NewRobotResponse(true)},
		{"ErrorResponse", NewErrorResponse(nil, ErrCodeInternalError, "test hint")},
		{"simple map", map[string]string{"key": "value"}},
		{"nested struct", struct {
			Outer struct {
				Inner string `json:"inner"`
			} `json:"outer"`
		}{Outer: struct {
			Inner string `json:"inner"`
		}{Inner: "nested"}}},
		{"array of strings", []string{"a", "b", "c"}},
		{"empty array", []string{}},
	}

	renderer := NewJSONRenderer()

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Render using the new renderer
			rendererOutput, err := renderer.Render(tc.payload)
			if err != nil {
				t.Fatalf("Render() error: %v", err)
			}

			// Generate expected output using json.Encoder (same as encodeJSON)
			var buf bytes.Buffer
			encoder := json.NewEncoder(&buf)
			encoder.SetIndent("", "  ")
			if err := encoder.Encode(tc.payload); err != nil {
				t.Fatalf("json.Encode() error: %v", err)
			}
			expectedOutput := buf.String()

			// Compare outputs
			if rendererOutput != expectedOutput {
				t.Errorf("output mismatch:\ngot:\n%s\nwant:\n%s", rendererOutput, expectedOutput)
			}
		})
	}
}

// TestRendererInterfaceCompliance verifies both renderers implement the interface correctly.
func TestRendererInterfaceCompliance(t *testing.T) {
	renderers := []struct {
		name     string
		renderer Renderer
	}{
		{"JSONRenderer", NewJSONRenderer()},
		{"TOONRenderer", NewTOONRenderer()},
	}

	for _, tc := range renderers {
		t.Run(tc.name, func(t *testing.T) {
			// All methods should be callable without panic
			ct := tc.renderer.ContentType()
			if ct == "" {
				t.Error("ContentType() should not return empty string")
			}

			f := tc.renderer.Format()
			if !f.IsValid() {
				t.Errorf("Format() returned invalid format: %q", f)
			}

			// Render should return some result (error or output)
			output, err := tc.renderer.Render(map[string]string{"test": "data"})
			if err == nil && output == "" {
				t.Error("Render() should return non-empty output on success")
			}
		})
	}
}

// =============================================================================
// OutputFormat Global Variable Tests
// =============================================================================

func TestOutputFormatDefault(t *testing.T) {
	// Save original and restore after test
	original := OutputFormat
	defer func() { OutputFormat = original }()

	// Default should be FormatAuto
	if OutputFormat != FormatAuto {
		t.Errorf("OutputFormat default = %q, want %q", OutputFormat, FormatAuto)
	}
}

func TestOutputFormatAffectsEncodeJSON(t *testing.T) {
	// Save original and restore after test
	original := OutputFormat
	defer func() { OutputFormat = original }()

	payload := map[string]string{"key": "value"}

	// Test with JSON format
	OutputFormat = FormatJSON
	jsonOutput, err := Render(payload, OutputFormat)
	if err != nil {
		t.Fatalf("Render with FormatJSON error: %v", err)
	}

	// Verify it's valid JSON
	var parsed map[string]interface{}
	if err := json.Unmarshal([]byte(jsonOutput), &parsed); err != nil {
		t.Fatalf("JSON output is not valid JSON: %v", err)
	}

	// Test with TOON format
	OutputFormat = FormatTOON
	toonOutput, err := Render(payload, OutputFormat)
	if err != nil {
		t.Fatalf("Render with FormatTOON error: %v", err)
	}

	// TOON output should be different from JSON
	if toonOutput == jsonOutput {
		t.Error("TOON output should differ from JSON output")
	}

	// TOON output should contain key-value format
	if !strings.Contains(toonOutput, "key") || !strings.Contains(toonOutput, "value") {
		t.Errorf("TOON output missing expected content: %q", toonOutput)
	}
}

// =============================================================================
// Snapshot + Error Path Tests (bd-3aejn)
// =============================================================================

func TestRenderSnapshotsJSONAndTOON(t *testing.T) {
	type item struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	}

	items := []item{{ID: 1, Name: "alpha"}, {ID: 2, Name: "beta"}}

	t.Run("json array snapshot", func(t *testing.T) {
		output, err := Render(items, FormatJSON)
		if err != nil {
			t.Fatalf("Render(JSON) error: %v", err)
		}

		expected := "[\n  {\n    \"id\": 1,\n    \"name\": \"alpha\"\n  },\n  {\n    \"id\": 2,\n    \"name\": \"beta\"\n  }\n]\n"
		if output != expected {
			t.Errorf("JSON snapshot mismatch:\n--- got ---\n%s--- want ---\n%s", output, expected)
		}
	})

	t.Run("toon array snapshot", func(t *testing.T) {
		output, err := Render(items, FormatTOON)
		if err != nil {
			t.Fatalf("Render(TOON) error: %v", err)
		}

		expected := "[2]{id,name}:\n 1\talpha\n 2\tbeta\n"
		if output != expected {
			t.Errorf("TOON snapshot mismatch:\n--- got ---\n%s--- want ---\n%s", output, expected)
		}
	})

	t.Run("robot response snapshot", func(t *testing.T) {
		payload := RobotResponse{
			Success:   true,
			Timestamp: "2026-01-01T00:00:00Z",
		}

		jsonOutput, err := Render(payload, FormatJSON)
		if err != nil {
			t.Fatalf("Render(JSON) error: %v", err)
		}

		expectedJSON := "{\n  \"success\": true,\n  \"timestamp\": \"2026-01-01T00:00:00Z\"\n}\n"
		if jsonOutput != expectedJSON {
			t.Errorf("RobotResponse JSON snapshot mismatch:\n--- got ---\n%s--- want ---\n%s", jsonOutput, expectedJSON)
		}

		toonOutput, err := Render(payload, FormatTOON)
		if err != nil {
			t.Fatalf("Render(TOON) error: %v", err)
		}

		expectedTOON := "error: \"\"\nerror_code: \"\"\nhint: \"\"\nstructured_error: null\nsuccess: true\ntimestamp: \"2026-01-01T00:00:00Z\"\n"
		if toonOutput != expectedTOON {
			t.Errorf("RobotResponse TOON snapshot mismatch:\n--- got ---\n%s--- want ---\n%s", toonOutput, expectedTOON)
		}
	})
}

func TestRenderFormatAutoDefaultsToJSON(t *testing.T) {
	payload := map[string]string{"key": "value"}

	jsonOutput, err := Render(payload, FormatJSON)
	if err != nil {
		t.Fatalf("Render(JSON) error: %v", err)
	}

	autoOutput, err := Render(payload, FormatAuto)
	if err != nil {
		t.Fatalf("Render(Auto) error: %v", err)
	}

	if autoOutput != jsonOutput {
		t.Errorf("FormatAuto should match JSON output:\n--- auto ---\n%s--- json ---\n%s", autoOutput, jsonOutput)
	}
}

func TestRenderTOONUnsupportedTypeReturnsError(t *testing.T) {
	type badPayload struct {
		Ch chan int `json:"ch"`
	}

	_, err := Render(badPayload{}, FormatTOON)
	if err == nil {
		t.Fatal("expected error for unsupported TOON payload, got nil")
	}
	if !strings.Contains(err.Error(), "unsupported") {
		t.Fatalf("expected unsupported error, got: %v", err)
	}
}
