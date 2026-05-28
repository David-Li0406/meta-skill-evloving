package pipeline

import (
	"os"
	"testing"
	"time"
)

func TestSubstitutor_Substitute(t *testing.T) {
	state := &ExecutionState{
		RunID:      "run-123",
		WorkflowID: "test-workflow",
		Variables: map[string]interface{}{
			"name":  "Alice",
			"count": 42,
			"flag":  true,
			"nested": map[string]interface{}{
				"deep": map[string]interface{}{
					"value": "found",
				},
				"items": []interface{}{"a", "b", "c"},
			},
		},
		Steps: map[string]StepResult{
			"step1": {
				StepID:     "step1",
				Status:     StatusCompleted,
				Output:     "step1 output",
				PaneUsed:   "pane-1",
				AgentType:  "claude",
				StartedAt:  time.Now().Add(-time.Minute),
				FinishedAt: time.Now(),
				ParsedData: map[string]interface{}{
					"result": "parsed value",
					"count":  100,
				},
			},
		},
	}

	sub := NewSubstitutor(state, "test-session", "my-workflow")

	tests := []struct {
		name     string
		template string
		want     string
		wantErr  bool
	}{
		{
			name:     "simple var",
			template: "Hello ${vars.name}!",
			want:     "Hello Alice!",
		},
		{
			name:     "numeric var",
			template: "Count: ${vars.count}",
			want:     "Count: 42",
		},
		{
			name:     "boolean var",
			template: "Flag: ${vars.flag}",
			want:     "Flag: true",
		},
		{
			name:     "nested var",
			template: "Value: ${vars.nested.deep.value}",
			want:     "Value: found",
		},
		{
			name:     "array access",
			template: "Second: ${vars.nested.items.1}",
			want:     "Second: b",
		},
		{
			name:     "step output",
			template: "Output: ${steps.step1.output}",
			want:     "Output: step1 output",
		},
		{
			name:     "step status",
			template: "Status: ${steps.step1.status}",
			want:     "Status: completed",
		},
		{
			name:     "step pane",
			template: "Pane: ${steps.step1.pane}",
			want:     "Pane: pane-1",
		},
		{
			name:     "step agent",
			template: "Agent: ${steps.step1.agent}",
			want:     "Agent: claude",
		},
		{
			name:     "step parsed data",
			template: "Result: ${steps.step1.data.result}",
			want:     "Result: parsed value",
		},
		{
			name:     "session context",
			template: "Session: ${session}",
			want:     "Session: test-session",
		},
		{
			name:     "run_id context",
			template: "Run: ${run_id}",
			want:     "Run: run-123",
		},
		{
			name:     "workflow context",
			template: "Workflow: ${workflow}",
			want:     "Workflow: my-workflow",
		},
		{
			name:     "default value (var undefined)",
			template: "User: ${vars.undefined | \"default\"}",
			want:     "User: default",
		},
		{
			name:     "default value (var defined)",
			template: "Name: ${vars.name | \"fallback\"}",
			want:     "Name: Alice",
		},
		{
			name:     "default single quotes",
			template: "X: ${vars.missing | 'single'}",
			want:     "X: single",
		},
		{
			name:     "default no quotes",
			template: "Y: ${vars.missing | bare}",
			want:     "Y: bare",
		},
		{
			name:     "escaped variable",
			template: "Literal: \\${vars.name}",
			want:     "Literal: ${vars.name}",
		},
		{
			name:     "mixed escaped and real",
			template: "Real: ${vars.name}, Literal: \\${vars.count}",
			want:     "Real: Alice, Literal: ${vars.count}",
		},
		{
			name:     "multiple vars",
			template: "${vars.name} has ${vars.count} items",
			want:     "Alice has 42 items",
		},
		{
			name:     "no vars",
			template: "Plain text",
			want:     "Plain text",
		},
		{
			name:     "timestamp exists",
			template: "Time: ${timestamp}",
			want:     "", // Will check it matches pattern
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := sub.Substitute(tt.template)
			if (err != nil) != tt.wantErr {
				t.Errorf("Substitute() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if tt.name == "timestamp exists" {
				// Just verify it's a valid timestamp
				if got == "" || got == "Time: ${timestamp}" {
					t.Errorf("Substitute() timestamp not resolved")
				}
				return
			}

			if got != tt.want {
				t.Errorf("Substitute() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestSubstitutor_EnvVars(t *testing.T) {
	// Set test env var
	os.Setenv("TEST_VAR", "test_value")
	defer os.Unsetenv("TEST_VAR")

	state := &ExecutionState{
		Variables: map[string]interface{}{},
	}

	sub := NewSubstitutor(state, "sess", "wf")

	got, err := sub.Substitute("Env: ${env.TEST_VAR}")
	if err != nil {
		t.Fatalf("Substitute() error = %v", err)
	}
	if got != "Env: test_value" {
		t.Errorf("Substitute() = %q, want %q", got, "Env: test_value")
	}

	// Unset env var returns empty string
	got2, _ := sub.Substitute("Missing: ${env.NONEXISTENT_VAR_123}")
	if got2 != "Missing: " {
		t.Errorf("Missing env var should return empty, got %q", got2)
	}
}

func TestSubstitutor_LoopVars(t *testing.T) {
	state := &ExecutionState{
		Variables: map[string]interface{}{},
	}

	// Set loop context
	SetLoopVars(state, "file", "test.txt", 2, 5)

	sub := NewSubstitutor(state, "sess", "wf")

	tests := []struct {
		template string
		want     string
	}{
		{"File: ${loop.file}", "File: test.txt"},
		{"Item: ${loop.item}", "Item: test.txt"},
		{"Index: ${loop.index}", "Index: 2"},
		{"Count: ${loop.count}", "Count: 5"},
		{"First: ${loop.first}", "First: false"},
		{"Last: ${loop.last}", "Last: false"},
	}

	for _, tt := range tests {
		got, err := sub.Substitute(tt.template)
		if err != nil {
			t.Errorf("Substitute(%q) error = %v", tt.template, err)
			continue
		}
		if got != tt.want {
			t.Errorf("Substitute(%q) = %q, want %q", tt.template, got, tt.want)
		}
	}

	// Test clear
	ClearLoopVars(state, "file")
	got, _ := sub.Substitute("After clear: ${loop.file | \"cleared\"}")
	if got != "After clear: cleared" {
		t.Errorf("After clear should use default, got %q", got)
	}
}

func TestSubstitutor_SubstituteStrict(t *testing.T) {
	state := &ExecutionState{
		Variables: map[string]interface{}{
			"defined": "value",
		},
	}

	sub := NewSubstitutor(state, "sess", "wf")

	// Should succeed for defined var
	got, err := sub.SubstituteStrict("Value: ${vars.defined}")
	if err != nil {
		t.Errorf("SubstituteStrict() unexpected error: %v", err)
	}
	if got != "Value: value" {
		t.Errorf("SubstituteStrict() = %q, want %q", got, "Value: value")
	}

	// Should fail for undefined var without default
	_, err = sub.SubstituteStrict("Value: ${vars.undefined}")
	if err == nil {
		t.Error("SubstituteStrict() should error for undefined var")
	}

	// Should succeed for undefined var with default
	got, err = sub.SubstituteStrict("Value: ${vars.undefined | \"default\"}")
	if err != nil {
		t.Errorf("SubstituteStrict() with default unexpected error: %v", err)
	}
	if got != "Value: default" {
		t.Errorf("SubstituteStrict() = %q, want %q", got, "Value: default")
	}
}

func TestOutputParser_ParseFirstLine(t *testing.T) {
	parser := NewOutputParser()

	tests := []struct {
		output string
		want   string
	}{
		{"first\nsecond\nthird", "first"},
		{"\n\nthird", "third"},
		{"single", "single"},
		{"  trimmed  \nnext", "trimmed"},
		{"", ""},
	}

	for _, tt := range tests {
		got, err := parser.Parse(tt.output, OutputParse{Type: "first_line"})
		if err != nil {
			t.Errorf("Parse(%q, first_line) error = %v", tt.output, err)
			continue
		}
		if got != tt.want {
			t.Errorf("Parse(%q, first_line) = %q, want %q", tt.output, got, tt.want)
		}
	}
}

func TestOutputParser_ParseLines(t *testing.T) {
	parser := NewOutputParser()

	output := "line1\n\nline2\n  line3  \n"
	got, err := parser.Parse(output, OutputParse{Type: "lines"})
	if err != nil {
		t.Fatalf("Parse() error = %v", err)
	}

	lines, ok := got.([]string)
	if !ok {
		t.Fatalf("Parse() returned %T, want []string", got)
	}

	want := []string{"line1", "line2", "line3"}
	if len(lines) != len(want) {
		t.Fatalf("Parse() returned %d lines, want %d", len(lines), len(want))
	}

	for i, line := range lines {
		if line != want[i] {
			t.Errorf("lines[%d] = %q, want %q", i, line, want[i])
		}
	}
}

func TestOutputParser_ParseJSON(t *testing.T) {
	parser := NewOutputParser()

	tests := []struct {
		name   string
		output string
		check  func(interface{}) bool
	}{
		{
			name:   "simple object",
			output: `{"key": "value", "count": 42}`,
			check: func(v interface{}) bool {
				m, ok := v.(map[string]interface{})
				return ok && m["key"] == "value" && m["count"] == float64(42)
			},
		},
		{
			name:   "array",
			output: `[1, 2, 3]`,
			check: func(v interface{}) bool {
				a, ok := v.([]interface{})
				return ok && len(a) == 3
			},
		},
		{
			name:   "json with prefix",
			output: `Some text here {"key": "value"}`,
			check: func(v interface{}) bool {
				m, ok := v.(map[string]interface{})
				return ok && m["key"] == "value"
			},
		},
		{
			name:   "json with suffix",
			output: `{"key": "value"} and more text`,
			check: func(v interface{}) bool {
				m, ok := v.(map[string]interface{})
				return ok && m["key"] == "value"
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := parser.Parse(tt.output, OutputParse{Type: "json"})
			if err != nil {
				t.Fatalf("Parse() error = %v", err)
			}
			if !tt.check(got) {
				t.Errorf("Parse() = %v, check failed", got)
			}
		})
	}
}

func TestOutputParser_ParseYAML(t *testing.T) {
	parser := NewOutputParser()

	output := `
name: test
items:
  - one
  - two
count: 10
`

	got, err := parser.Parse(output, OutputParse{Type: "yaml"})
	if err != nil {
		t.Fatalf("Parse() error = %v", err)
	}

	m, ok := got.(map[string]interface{})
	if !ok {
		t.Fatalf("Parse() returned %T, want map", got)
	}

	if m["name"] != "test" {
		t.Errorf("name = %v, want test", m["name"])
	}
	if m["count"] != 10 {
		t.Errorf("count = %v, want 10", m["count"])
	}

	items, ok := m["items"].([]interface{})
	if !ok || len(items) != 2 {
		t.Errorf("items = %v, want [one, two]", m["items"])
	}
}

func TestOutputParser_ParseRegex(t *testing.T) {
	parser := NewOutputParser()

	tests := []struct {
		name    string
		output  string
		pattern string
		check   func(interface{}) bool
	}{
		{
			name:    "named groups",
			output:  "Count: 42, Name: Alice",
			pattern: `Count: (?P<count>\d+), Name: (?P<name>\w+)`,
			check: func(v interface{}) bool {
				m, ok := v.(map[string]interface{})
				return ok && m["count"] == "42" && m["name"] == "Alice"
			},
		},
		{
			name:    "single capture group",
			output:  "The value is 123",
			pattern: `value is (\d+)`,
			check: func(v interface{}) bool {
				// Returns []string for backward compatibility
				a, ok := v.([]string)
				return ok && len(a) == 1 && a[0] == "123"
			},
		},
		{
			name:    "multiple capture groups",
			output:  "X=10 Y=20",
			pattern: `X=(\d+) Y=(\d+)`,
			check: func(v interface{}) bool {
				// Returns []string for backward compatibility
				a, ok := v.([]string)
				return ok && len(a) == 2 && a[0] == "10" && a[1] == "20"
			},
		},
		{
			name:    "no match",
			output:  "no numbers here",
			pattern: `\d+`,
			check: func(v interface{}) bool {
				return v == nil
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := parser.Parse(tt.output, OutputParse{Type: "regex", Pattern: tt.pattern})
			if err != nil {
				t.Fatalf("Parse() error = %v", err)
			}
			if !tt.check(got) {
				t.Errorf("Parse() = %v, check failed", got)
			}
		})
	}
}

func TestNavigateNested(t *testing.T) {
	data := map[string]interface{}{
		"level1": map[string]interface{}{
			"level2": map[string]interface{}{
				"value": "deep",
			},
			"array": []interface{}{"a", "b", "c"},
		},
	}

	tests := []struct {
		parts   []string
		want    interface{}
		wantErr bool
	}{
		{[]string{"level1", "level2", "value"}, "deep", false},
		{[]string{"level1", "array", "1"}, "b", false},
		{[]string{"level1", "array", "5"}, nil, true},          // out of bounds
		{[]string{"level1", "missing"}, nil, true},             // field not found
		{[]string{"level1", "array", "notanumber"}, nil, true}, // invalid index
	}

	for _, tt := range tests {
		got, err := navigateNested(data, tt.parts)
		if (err != nil) != tt.wantErr {
			t.Errorf("navigateNested(%v) error = %v, wantErr %v", tt.parts, err, tt.wantErr)
			continue
		}
		if !tt.wantErr && got != tt.want {
			t.Errorf("navigateNested(%v) = %v, want %v", tt.parts, got, tt.want)
		}
	}
}

func TestNavigateNested_EdgeCases(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		value   interface{}
		parts   []string
		want    interface{}
		wantErr bool
	}{
		{
			name:    "nil value",
			value:   nil,
			parts:   []string{"foo"},
			wantErr: true,
		},
		{
			name: "map[interface{}]interface{} - YAML style",
			value: map[interface{}]interface{}{
				"key1": "value1",
				"key2": map[interface{}]interface{}{
					"nested": "nestedvalue",
				},
			},
			parts: []string{"key1"},
			want:  "value1",
		},
		{
			name: "map[interface{}]interface{} - nested",
			value: map[interface{}]interface{}{
				"outer": map[interface{}]interface{}{
					"inner": "deep",
				},
			},
			parts: []string{"outer", "inner"},
			want:  "deep",
		},
		{
			name: "map[interface{}]interface{} - missing key",
			value: map[interface{}]interface{}{
				"key1": "value1",
			},
			parts:   []string{"missing"},
			wantErr: true,
		},
		{
			name:  "[]string array",
			value: []string{"alpha", "beta", "gamma"},
			parts: []string{"1"},
			want:  "beta",
		},
		{
			name:    "[]string array - out of bounds",
			value:   []string{"alpha", "beta"},
			parts:   []string{"5"},
			wantErr: true,
		},
		{
			name:    "[]string array - invalid index",
			value:   []string{"alpha", "beta"},
			parts:   []string{"abc"},
			wantErr: true,
		},
		{
			name:    "[]string array - negative index",
			value:   []string{"alpha", "beta"},
			parts:   []string{"-1"},
			wantErr: true,
		},
		{
			name:    "[]interface{} array - negative index",
			value:   []interface{}{"a", "b"},
			parts:   []string{"-1"},
			wantErr: true,
		},
		{
			name:    "unsupported type (struct)",
			value:   struct{ Field string }{"value"},
			parts:   []string{"Field"},
			wantErr: true,
		},
		{
			name:    "access field on string",
			value:   "just a string",
			parts:   []string{"field"},
			wantErr: true,
		},
		{
			name:  "empty parts returns original",
			value: "original",
			parts: []string{},
			want:  "original",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got, err := navigateNested(tt.value, tt.parts)
			if tt.wantErr {
				if err == nil {
					t.Errorf("navigateNested() expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("navigateNested() unexpected error: %v", err)
				return
			}
			if got != tt.want {
				t.Errorf("navigateNested() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestFormatValue(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		value interface{}
		want  string
	}{
		{
			name:  "nil",
			value: nil,
			want:  "",
		},
		{
			name:  "string",
			value: "hello world",
			want:  "hello world",
		},
		{
			name:  "bool true",
			value: true,
			want:  "true",
		},
		{
			name:  "bool false",
			value: false,
			want:  "false",
		},
		{
			name:  "int positive",
			value: 42,
			want:  "42",
		},
		{
			name:  "int negative",
			value: -10,
			want:  "-10",
		},
		{
			name:  "int zero",
			value: 0,
			want:  "0",
		},
		{
			name:  "int64",
			value: int64(9223372036854775807),
			want:  "9223372036854775807",
		},
		{
			name:  "float64 integer-like",
			value: 42.0,
			want:  "42",
		},
		{
			name:  "float64 with decimals",
			value: 3.14159,
			want:  "3.14159",
		},
		{
			name:  "[]byte",
			value: []byte("byte slice"),
			want:  "byte slice",
		},
		{
			name:  "map - JSON marshaled",
			value: map[string]string{"key": "value"},
			want:  `{"key":"value"}`,
		},
		{
			name:  "slice - JSON marshaled",
			value: []int{1, 2, 3},
			want:  "[1,2,3]",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := formatValue(tt.value)
			if got != tt.want {
				t.Errorf("formatValue(%v) = %q, want %q", tt.value, got, tt.want)
			}
		})
	}
}

func TestFormatValue_TimeTypes(t *testing.T) {
	// Time tests aren't parallel because they use fixed time values

	// Test time.Time
	testTime := time.Date(2025, 6, 15, 10, 30, 0, 0, time.UTC)
	got := formatValue(testTime)
	want := "2025-06-15T10:30:00Z"
	if got != want {
		t.Errorf("formatValue(time.Time) = %q, want %q", got, want)
	}

	// Test time.Duration
	duration := 5*time.Hour + 30*time.Minute + 15*time.Second
	got = formatValue(duration)
	want = "5h30m15s"
	if got != want {
		t.Errorf("formatValue(time.Duration) = %q, want %q", got, want)
	}
}

func TestStoreStepOutput(t *testing.T) {
	state := &ExecutionState{}

	StoreStepOutput(state, "step1", "raw output", map[string]interface{}{"key": "value"})

	if state.Variables["steps.step1.output"] != "raw output" {
		t.Errorf("output not stored correctly")
	}

	if state.Variables["steps.step1.data"] == nil {
		t.Errorf("parsed data not stored")
	}
}

func TestValidateVarRefs(t *testing.T) {
	available := []string{"name", "count", "vars.name", "vars.count"}

	tests := []struct {
		template string
		wantLen  int // number of invalid refs
	}{
		{"${vars.name}", 0},
		{"${vars.undefined}", 1},
		{"${env.PATH}", 0},         // env is always valid
		{"${session}", 0},          // context vars are valid
		{"${unknown.var}", 1},      // unknown namespace
		{"\\${vars.name}", 0},      // escaped is ignored
		{"${vars.x} ${vars.y}", 2}, // both undefined
	}

	for _, tt := range tests {
		invalid := ValidateVarRefs(tt.template, available)
		if len(invalid) != tt.wantLen {
			t.Errorf("ValidateVarRefs(%q) = %v, want %d invalid", tt.template, invalid, tt.wantLen)
		}
	}
}

func TestParseDefault(t *testing.T) {
	tests := []struct {
		expr       string
		wantPath   string
		wantDef    string
		wantHasDef bool
	}{
		{"vars.name", "vars.name", "", false},
		{"vars.x | \"default\"", "vars.x", "default", true},
		{"vars.x | 'single'", "vars.x", "single", true},
		{"vars.x | bare", "vars.x", "bare", true},
		{"vars.x|compact", "vars.x", "compact", true},
		{"vars.x  |  spaced  ", "vars.x", "spaced", true},
	}

	for _, tt := range tests {
		path, def, hasDef := parseDefault(tt.expr)
		if path != tt.wantPath {
			t.Errorf("parseDefault(%q) path = %q, want %q", tt.expr, path, tt.wantPath)
		}
		if def != tt.wantDef {
			t.Errorf("parseDefault(%q) default = %q, want %q", tt.expr, def, tt.wantDef)
		}
		if hasDef != tt.wantHasDef {
			t.Errorf("parseDefault(%q) hasDefault = %v, want %v", tt.expr, hasDef, tt.wantHasDef)
		}
	}
}

func TestExtractJSONBlock(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{`{"key": "value"}`, `{"key": "value"}`},
		{`{"key": "value"} extra`, `{"key": "value"}`},
		{`[1, 2, 3]`, `[1, 2, 3]`},
		{`{"nested": {"a": 1}}`, `{"nested": {"a": 1}}`},
		{`{"quoted": "with } brace"}`, `{"quoted": "with } brace"}`},
		{`not json`, `not json`},
	}

	for _, tt := range tests {
		got := extractJSONBlock(tt.input)
		if got != tt.want {
			t.Errorf("extractJSONBlock(%q) = %q, want %q", tt.input, got, tt.want)
		}
	}
}

func TestSubstitutionError_Error(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		err     SubstitutionError
		wantMsg string
	}{
		{
			name: "simple variable",
			err: SubstitutionError{
				VarRef:  "myvar",
				Message: "variable not defined",
			},
			wantMsg: "variable substitution error for 'myvar': variable not defined",
		},
		{
			name: "nested variable",
			err: SubstitutionError{
				VarRef:  "steps.step1.output",
				Message: "step not executed",
			},
			wantMsg: "variable substitution error for 'steps.step1.output': step not executed",
		},
		{
			name: "env variable",
			err: SubstitutionError{
				VarRef:  "env.MY_VAR",
				Message: "environment variable not set",
			},
			wantMsg: "variable substitution error for 'env.MY_VAR': environment variable not set",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := tt.err.Error()
			if got != tt.wantMsg {
				t.Errorf("SubstitutionError.Error() = %q, want %q", got, tt.wantMsg)
			}
		})
	}
}
