package pipeline

import (
	"context"
	"errors"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

func TestDefaultExecutorConfig(t *testing.T) {
	cfg := DefaultExecutorConfig("test-session")

	if cfg.Session != "test-session" {
		t.Errorf("Session = %q, want %q", cfg.Session, "test-session")
	}
	if cfg.DefaultTimeout != 5*time.Minute {
		t.Errorf("DefaultTimeout = %v, want 5m", cfg.DefaultTimeout)
	}
	if cfg.GlobalTimeout != 30*time.Minute {
		t.Errorf("GlobalTimeout = %v, want 30m", cfg.GlobalTimeout)
	}
	if cfg.ProgressInterval != time.Second {
		t.Errorf("ProgressInterval = %v, want 1s", cfg.ProgressInterval)
	}
	if cfg.DryRun {
		t.Error("DryRun should be false by default")
	}
}

func TestNewExecutor(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	if e == nil {
		t.Fatal("NewExecutor returned nil")
	}
	if e.config.Session != "test" {
		t.Errorf("config.Session = %q, want %q", e.config.Session, "test")
	}
	if e.detector == nil {
		t.Error("detector should not be nil")
	}
	if e.router == nil {
		t.Error("router should not be nil")
	}
	if e.scorer == nil {
		t.Error("scorer should not be nil")
	}
}

func TestExecutor_SetNotifier(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Initially nil
	if e.notifier != nil {
		t.Error("notifier should initially be nil")
	}

	// Set notifier using NewNotifier
	notifier := NewNotifier(NotifierConfig{
		Channels: []string{"desktop"},
	})
	e.SetNotifier(notifier)

	if e.notifier != notifier {
		t.Error("notifier should be set to the same pointer")
	}

	// Set to nil
	e.SetNotifier(nil)
	if e.notifier != nil {
		t.Error("notifier should be nil after setting to nil")
	}
}

func TestExecutor_Validate(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Steps: []Step{
			{ID: "step1", Prompt: "Hello"},
		},
	}

	result := e.Validate(workflow)
	if !result.Valid {
		t.Errorf("Validation failed: %v", result.Errors)
	}
}

func TestExecutor_Validate_Invalid(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Missing required fields
	workflow := &Workflow{}

	result := e.Validate(workflow)
	if result.Valid {
		t.Error("Validation should fail for empty workflow")
	}
	if len(result.Errors) == 0 {
		t.Error("Should have validation errors")
	}
}

func TestSubstituteVariables(t *testing.T) {
	cfg := DefaultExecutorConfig("test-session")
	e := NewExecutor(cfg)

	// Set up mock state
	e.state = &ExecutionState{
		RunID:      "run-123",
		WorkflowID: "my-workflow",
		Variables: map[string]interface{}{
			"name":              "Alice",
			"count":             42,
			"steps.prev.output": "previous result",
		},
	}

	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "no variables",
			input: "Hello world",
			want:  "Hello world",
		},
		{
			name:  "vars substitution",
			input: "Hello ${vars.name}",
			want:  "Hello Alice",
		},
		{
			name:  "vars number",
			input: "Count: ${vars.count}",
			want:  "Count: 42",
		},
		{
			name:  "session reference",
			input: "Session: ${session}",
			want:  "Session: test-session",
		},
		{
			name:  "run_id reference",
			input: "Run: ${run_id}",
			want:  "Run: run-123",
		},
		{
			name:  "workflow reference",
			input: "Workflow: ${workflow}",
			want:  "Workflow: my-workflow",
		},
		{
			name:  "step output reference",
			input: "Previous: ${steps.prev.output}",
			want:  "Previous: previous result",
		},
		{
			name:  "missing variable unchanged",
			input: "Missing: ${vars.unknown}",
			want:  "Missing: ${vars.unknown}",
		},
		{
			name:  "multiple substitutions",
			input: "Hello ${vars.name}, run ${run_id}",
			want:  "Hello Alice, run run-123",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := e.substituteVariables(tt.input)
			if got != tt.want {
				t.Errorf("substituteVariables(%q) = %q, want %q", tt.input, got, tt.want)
			}
		})
	}
}

func TestSubstituteVariables_Env(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)
	e.state = &ExecutionState{Variables: make(map[string]interface{})}

	// Set test env var
	os.Setenv("TEST_EXECUTOR_VAR", "test-value")
	defer os.Unsetenv("TEST_EXECUTOR_VAR")

	input := "Env: ${env.TEST_EXECUTOR_VAR}"
	got := e.substituteVariables(input)
	want := "Env: test-value"

	if got != want {
		t.Errorf("substituteVariables(%q) = %q, want %q", input, got, want)
	}
}

func TestEvaluateCondition(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)
	e.state = &ExecutionState{
		Variables: map[string]interface{}{
			"enabled": "true",
			"flag":    "false",
		},
	}

	tests := []struct {
		name      string
		condition string
		wantSkip  bool
		wantErr   bool
	}{
		{
			name:      "truthy string - don't skip",
			condition: "hello",
			wantSkip:  false,
		},
		{
			name:      "empty string - no condition means don't skip",
			condition: "",
			wantSkip:  false,
		},
		{
			name:      "false string - skip",
			condition: "false",
			wantSkip:  true,
		},
		{
			name:      "0 - skip",
			condition: "0",
			wantSkip:  true,
		},
		{
			name:      "negation of false - don't skip",
			condition: "!false",
			wantSkip:  false,
		},
		{
			name:      "negation of true - skip",
			condition: "!true",
			wantSkip:  true,
		},
		{
			name:      "equality true - don't skip",
			condition: "hello == 'hello'",
			wantSkip:  false,
		},
		{
			name:      "equality false - skip",
			condition: "hello == 'world'",
			wantSkip:  true,
		},
		{
			name:      "inequality true - don't skip",
			condition: "hello != 'world'",
			wantSkip:  false,
		},
		{
			name:      "inequality false - skip",
			condition: "hello != 'hello'",
			wantSkip:  true,
		},
		{
			name:      "variable substitution - truthy",
			condition: "${vars.enabled}",
			wantSkip:  false,
		},
		{
			name:      "variable substitution - falsy",
			condition: "${vars.flag}",
			wantSkip:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			skip, err := e.evaluateCondition(tt.condition)
			if (err != nil) != tt.wantErr {
				t.Errorf("evaluateCondition() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if skip != tt.wantSkip {
				t.Errorf("evaluateCondition(%q) = %v, want %v", tt.condition, skip, tt.wantSkip)
			}
		})
	}
}

func TestParseOutput(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	tests := []struct {
		name    string
		output  string
		parse   OutputParse
		want    interface{}
		wantErr bool
	}{
		{
			name:   "first_line",
			output: "first\nsecond\nthird",
			parse:  OutputParse{Type: "first_line"},
			want:   "first",
		},
		{
			name:   "first_line with empty lines",
			output: "\n\nfirst\nsecond",
			parse:  OutputParse{Type: "first_line"},
			want:   "first",
		},
		{
			name:   "lines",
			output: "one\ntwo\nthree",
			parse:  OutputParse{Type: "lines"},
			want:   []string{"one", "two", "three"},
		},
		{
			name:   "lines with empty",
			output: "one\n\nthree",
			parse:  OutputParse{Type: "lines"},
			want:   []string{"one", "three"},
		},
		{
			name:   "regex simple",
			output: "version: 1.2.3",
			parse:  OutputParse{Type: "regex", Pattern: `version: (\d+\.\d+\.\d+)`},
			want:   []string{"1.2.3"},
		},
		{
			name:    "regex invalid pattern",
			output:  "test",
			parse:   OutputParse{Type: "regex", Pattern: `[invalid`},
			wantErr: true,
		},
		{
			name:    "regex missing pattern",
			output:  "test",
			parse:   OutputParse{Type: "regex"},
			wantErr: true,
		},
		{
			name:   "json parsing",
			output: `{"key": "value"}`,
			parse:  OutputParse{Type: "json"},
			want:   map[string]interface{}{"key": "value"},
		},
		{
			name:   "default passthrough",
			output: "raw output",
			parse:  OutputParse{Type: ""},
			want:   "raw output",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := e.parseOutput(tt.output, tt.parse)
			if (err != nil) != tt.wantErr {
				t.Errorf("parseOutput() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr {
				return
			}

			// Compare based on type
			switch want := tt.want.(type) {
			case string:
				if got != want {
					t.Errorf("parseOutput() = %v, want %v", got, want)
				}
			case []string:
				gotSlice, ok := got.([]string)
				if !ok {
					t.Errorf("parseOutput() returned %T, want []string", got)
					return
				}
				if len(gotSlice) != len(want) {
					t.Errorf("parseOutput() len = %d, want %d", len(gotSlice), len(want))
					return
				}
				for i, w := range want {
					if gotSlice[i] != w {
						t.Errorf("parseOutput()[%d] = %q, want %q", i, gotSlice[i], w)
					}
				}
			case map[string]interface{}:
				gotMap, ok := got.(map[string]interface{})
				if !ok {
					t.Errorf("parseOutput() returned %T, want map[string]interface{}", got)
					return
				}
				for k, wantVal := range want {
					if gotVal, exists := gotMap[k]; !exists || gotVal != wantVal {
						t.Errorf("parseOutput()[%q] = %v, want %v", k, gotVal, wantVal)
					}
				}
			}
		})
	}
}

func TestCalculateRetryDelay(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	base := time.Second

	tests := []struct {
		name    string
		attempt int
		backoff string
		want    time.Duration
	}{
		{
			name:    "no backoff",
			attempt: 1,
			backoff: "",
			want:    time.Second,
		},
		{
			name:    "no backoff attempt 3",
			attempt: 3,
			backoff: "none",
			want:    time.Second,
		},
		{
			name:    "linear attempt 1",
			attempt: 1,
			backoff: "linear",
			want:    time.Second,
		},
		{
			name:    "linear attempt 3",
			attempt: 3,
			backoff: "linear",
			want:    3 * time.Second,
		},
		{
			name:    "exponential attempt 1",
			attempt: 1,
			backoff: "exponential",
			want:    time.Second, // 1 * 2^0 = 1
		},
		{
			name:    "exponential attempt 2",
			attempt: 2,
			backoff: "exponential",
			want:    2 * time.Second, // 1 * 2^1 = 2
		},
		{
			name:    "exponential attempt 3",
			attempt: 3,
			backoff: "exponential",
			want:    4 * time.Second, // 1 * 2^2 = 4
		},
		{
			name:    "exponential attempt 4",
			attempt: 4,
			backoff: "exponential",
			want:    8 * time.Second, // 1 * 2^3 = 8
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := e.calculateRetryDelay(base, tt.attempt, tt.backoff)
			if got != tt.want {
				t.Errorf("calculateRetryDelay(%v, %d, %q) = %v, want %v",
					base, tt.attempt, tt.backoff, got, tt.want)
			}
		})
	}
}

func TestCalculateProgress(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Create a workflow with 4 steps
	workflow := &Workflow{
		Steps: []Step{
			{ID: "step1", Prompt: "a"},
			{ID: "step2", Prompt: "b"},
			{ID: "step3", Prompt: "c"},
			{ID: "step4", Prompt: "d"},
		},
	}

	e.graph = NewDependencyGraph(workflow)
	e.state = &ExecutionState{
		Steps: make(map[string]StepResult),
	}

	// No steps completed
	got := e.calculateProgress()
	if got != 0.0 {
		t.Errorf("progress with 0 completed = %v, want 0.0", got)
	}

	// 1 step completed
	e.state.Steps["step1"] = StepResult{Status: StatusCompleted}
	got = e.calculateProgress()
	if got != 0.25 {
		t.Errorf("progress with 1/4 completed = %v, want 0.25", got)
	}

	// 2 steps completed, 1 skipped
	e.state.Steps["step2"] = StepResult{Status: StatusCompleted}
	e.state.Steps["step3"] = StepResult{Status: StatusSkipped}
	got = e.calculateProgress()
	if got != 0.75 {
		t.Errorf("progress with 3/4 completed/skipped = %v, want 0.75", got)
	}

	// All steps done
	e.state.Steps["step4"] = StepResult{Status: StatusFailed}
	got = e.calculateProgress()
	if got != 1.0 {
		t.Errorf("progress with 4/4 done = %v, want 1.0", got)
	}
}

func TestEmitProgress(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Create channel for progress events
	progress := make(chan ProgressEvent, 10)
	e.progress = progress

	e.emitProgress("step_start", "step1", "Starting step", 0.5)

	select {
	case event := <-progress:
		if event.Type != "step_start" {
			t.Errorf("Type = %q, want %q", event.Type, "step_start")
		}
		if event.StepID != "step1" {
			t.Errorf("StepID = %q, want %q", event.StepID, "step1")
		}
		if event.Message != "Starting step" {
			t.Errorf("Message = %q, want %q", event.Message, "Starting step")
		}
		if event.Progress != 0.5 {
			t.Errorf("Progress = %v, want 0.5", event.Progress)
		}
	case <-time.After(time.Second):
		t.Error("Timeout waiting for progress event")
	}
}

func TestEmitProgress_NilChannel(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)
	e.progress = nil

	// Should not panic
	e.emitProgress("test", "step1", "message", 0.5)
}

func TestEmitProgress_FullChannel(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Create a full unbuffered channel
	progress := make(chan ProgressEvent)
	e.progress = progress

	// Should not block (non-blocking send)
	done := make(chan bool)
	go func() {
		e.emitProgress("test", "step1", "message", 0.5)
		done <- true
	}()

	select {
	case <-done:
		// Good, didn't block
	case <-time.After(time.Second):
		t.Error("emitProgress blocked on full channel")
	}
}

func TestTruncatePrompt(t *testing.T) {
	tests := []struct {
		name  string
		input string
		n     int
		want  string
	}{
		{
			name:  "short string",
			input: "hello",
			n:     10,
			want:  "hello",
		},
		{
			name:  "exact length",
			input: "hello",
			n:     5,
			want:  "hello",
		},
		{
			name:  "truncated",
			input: "hello world",
			n:     8,
			want:  "hello...",
		},
		{
			name:  "with newlines",
			input: "hello\nworld",
			n:     20,
			want:  "hello world",
		},
		{
			name:  "with tabs",
			input: "hello\tworld",
			n:     20,
			want:  "hello world",
		},
		{
			// UTF-8: "αβγδ" is 8 bytes (2 per char), n=4 means content max is 1 byte
			// No full 2-byte rune fits in 1 byte, so return just "..."
			name:  "utf8 multibyte truncate small",
			input: "αβγδ", // 8 bytes
			n:     4,
			want:  "...", // Can't fit any full rune + "..."
		},
		{
			// UTF-8: "αβγδ" is 8 bytes, n=5 means content max is 2 bytes (exactly one α)
			name:  "utf8 multibyte exact rune boundary",
			input: "αβγδ", // 8 bytes
			n:     5,
			want:  "α...", // 2 + 3 = 5 bytes
		},
		{
			// UTF-8: "αβγδ" is 8 bytes, n=6 means content max is 3 bytes
			// Only one 2-byte rune fits (can't fit β which starts at byte 2)
			// This tests the edge case where targetLen falls between rune boundaries
			name:  "utf8 multibyte between boundaries",
			input: "αβγδ", // 8 bytes
			n:     6,
			want:  "α...", // 2 + 3 = 5 bytes (must not exceed 6)
		},
		{
			// UTF-8: "αβγδ" is 8 bytes, n=7 means content max is 4 bytes
			// Two 2-byte runes fit exactly
			name:  "utf8 multibyte two runes fit",
			input: "αβγδ", // 8 bytes
			n:     7,
			want:  "αβ...", // 4 + 3 = 7 bytes
		},
		{
			// Mixed ASCII and UTF-8: "aβcδe" is 6 bytes (a=1, β=2, c=1, δ=2)
			// n=5 means content max is 2 bytes
			name:  "utf8 mixed ascii needs truncation",
			input: "aβcδ", // 5 bytes (a=1, β=2, c=1, δ=2 = 6 bytes total)
			n:     5,
			want:  "a...", // Only 'a' (1 byte) fits in content, total 4 bytes
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := truncatePrompt(tt.input, tt.n)
			if got != tt.want {
				t.Errorf("truncatePrompt(%q, %d) = %q, want %q", tt.input, tt.n, got, tt.want)
			}
		})
	}
}

func TestGenerateRunID(t *testing.T) {
	id1 := generateRunID()
	id2 := generateRunID()

	// Should start with "run-"
	if !strings.HasPrefix(id1, "run-") {
		t.Errorf("ID should start with 'run-', got %q", id1)
	}

	// Should be unique
	if id1 == id2 {
		t.Error("Two consecutive IDs should be different")
	}

	// Should have reasonable length
	if len(id1) < 20 {
		t.Errorf("ID too short: %q (len=%d)", id1, len(id1))
	}
}

func TestVariableContext_GetVariable(t *testing.T) {
	vc := &VariableContext{
		Vars: map[string]interface{}{
			"name": "Alice",
			"age":  30,
		},
		Steps: map[string]StepResult{
			"step1": {
				Output:   "step1 output",
				Status:   StatusCompleted,
				PaneUsed: "pane-1",
			},
		},
		Session:  "my-session",
		RunID:    "run-123",
		Workflow: "my-workflow",
	}

	// Set env for testing
	os.Setenv("TEST_VC_VAR", "env-value")
	defer os.Unsetenv("TEST_VC_VAR")

	tests := []struct {
		name   string
		ref    string
		want   interface{}
		wantOk bool
	}{
		{"vars.name", "vars.name", "Alice", true},
		{"vars.age", "vars.age", 30, true},
		{"vars.missing", "vars.missing", nil, false},
		{"steps.step1.output", "steps.step1.output", "step1 output", true},
		{"steps.step1.status", "steps.step1.status", "completed", true},
		{"steps.step1.pane", "steps.step1.pane", "pane-1", true},
		{"steps.missing.output", "steps.missing.output", nil, false},
		{"session", "session", "my-session", true},
		{"run_id", "run_id", "run-123", true},
		{"workflow", "workflow", "my-workflow", true},
		{"env.TEST_VC_VAR", "env.TEST_VC_VAR", "env-value", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, ok := vc.GetVariable(tt.ref)
			if ok != tt.wantOk {
				t.Errorf("GetVariable(%q) ok = %v, want %v", tt.ref, ok, tt.wantOk)
			}
			if tt.wantOk && got != tt.want {
				t.Errorf("GetVariable(%q) = %v, want %v", tt.ref, got, tt.want)
			}
		})
	}
}

func TestVariableContext_SetVariable(t *testing.T) {
	vc := &VariableContext{}

	// Initially nil
	if vc.Vars != nil {
		t.Error("Vars should be nil initially")
	}

	// Set a variable (should initialize map)
	vc.SetVariable("test", "value")

	if vc.Vars == nil {
		t.Error("Vars should be initialized after SetVariable")
	}
	if vc.Vars["test"] != "value" {
		t.Errorf("Vars[test] = %v, want 'value'", vc.Vars["test"])
	}
}

func TestVariableContext_EvaluateString(t *testing.T) {
	vc := &VariableContext{
		Vars: map[string]interface{}{
			"name": "Alice",
		},
		Session: "my-session",
	}

	input := "Hello ${vars.name} in ${session}"
	want := "Hello Alice in my-session"

	got := vc.EvaluateString(input)
	if got != want {
		t.Errorf("EvaluateString(%q) = %q, want %q", input, got, want)
	}
}

func TestParseBool(t *testing.T) {
	tests := []struct {
		input string
		want  bool
	}{
		{"true", true},
		{"TRUE", true},
		{"True", true},
		{"yes", true},
		{"YES", true},
		{"1", true},
		{"on", true},
		{"false", false},
		{"FALSE", false},
		{"no", false},
		{"0", false},
		{"off", false},
		{"", false},
		{"maybe", false},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := ParseBool(tt.input)
			if got != tt.want {
				t.Errorf("ParseBool(%q) = %v, want %v", tt.input, got, tt.want)
			}
		})
	}
}

func TestParseInt(t *testing.T) {
	tests := []struct {
		input string
		def   int
		want  int
	}{
		{"42", 0, 42},
		{"-1", 0, -1},
		{"", 10, 10},
		{"abc", 5, 5},
		{"3.14", 0, 0}, // Invalid, returns default
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := ParseInt(tt.input, tt.def)
			if got != tt.want {
				t.Errorf("ParseInt(%q, %d) = %d, want %d", tt.input, tt.def, got, tt.want)
			}
		})
	}
}

func TestExecutor_Cancel(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Cancel should be safe to call even without a running workflow
	e.Cancel()

	// Set up a cancel function
	ctx, cancel := context.WithCancel(context.Background())
	e.cancelFn = cancel

	// Cancel should call the cancel function
	e.Cancel()

	// Verify context is cancelled
	select {
	case <-ctx.Done():
		// Good, context was cancelled
	default:
		t.Error("Cancel() should have cancelled the context")
	}
}

func TestExecutor_GetState(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Initially nil
	if e.GetState() != nil {
		t.Error("GetState should return nil before Run")
	}

	// Set state
	e.state = &ExecutionState{
		RunID:      "test-run",
		WorkflowID: "test-workflow",
	}

	state := e.GetState()
	if state == nil {
		t.Fatal("GetState should return state after it's set")
	}
	if state.RunID != "test-run" {
		t.Errorf("state.RunID = %q, want %q", state.RunID, "test-run")
	}
}

func TestExecutor_ResolvePrompt(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	t.Run("prompt string", func(t *testing.T) {
		step := &Step{Prompt: "Hello world"}
		got, err := e.resolvePrompt(step)
		if err != nil {
			t.Errorf("resolvePrompt() error = %v", err)
		}
		if got != "Hello world" {
			t.Errorf("resolvePrompt() = %q, want %q", got, "Hello world")
		}
	})

	t.Run("neither prompt nor file", func(t *testing.T) {
		step := &Step{}
		_, err := e.resolvePrompt(step)
		if err == nil {
			t.Error("resolvePrompt() should error with no prompt")
		}
	})

	t.Run("prompt_file not found", func(t *testing.T) {
		step := &Step{PromptFile: "/nonexistent/path/prompt.txt"}
		_, err := e.resolvePrompt(step)
		if err == nil {
			t.Error("resolvePrompt() should error with nonexistent file")
		}
	})
}

// Integration-style test for the execution workflow
func TestExecutor_Run_ValidationError(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Create workflow with circular dependency
	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Steps: []Step{
			{ID: "step1", Prompt: "a", DependsOn: []string{"step2"}},
			{ID: "step2", Prompt: "b", DependsOn: []string{"step1"}},
		},
	}

	ctx := context.Background()
	state, err := e.Run(ctx, workflow, nil, nil)

	if err == nil {
		t.Error("Run() should return error for circular dependency")
	}
	if state.Status != StatusFailed {
		t.Errorf("state.Status = %v, want Failed", state.Status)
	}
	if len(state.Errors) == 0 {
		t.Error("state.Errors should contain dependency error")
	}
}

func TestExecutorConfig_Overrides(t *testing.T) {
	cfg := ExecutorConfig{
		Session:          "custom-session",
		DefaultTimeout:   10 * time.Minute,
		GlobalTimeout:    1 * time.Hour,
		ProgressInterval: 500 * time.Millisecond,
		DryRun:           true,
		Verbose:          true,
	}

	e := NewExecutor(cfg)

	if e.config.Session != "custom-session" {
		t.Errorf("Session = %q, want %q", e.config.Session, "custom-session")
	}
	if e.config.DefaultTimeout != 10*time.Minute {
		t.Errorf("DefaultTimeout = %v, want 10m", e.config.DefaultTimeout)
	}
	if e.config.GlobalTimeout != time.Hour {
		t.Errorf("GlobalTimeout = %v, want 1h", e.config.GlobalTimeout)
	}
	if e.config.ProgressInterval != 500*time.Millisecond {
		t.Errorf("ProgressInterval = %v, want 500ms", e.config.ProgressInterval)
	}
	if !e.config.DryRun {
		t.Error("DryRun should be true")
	}
	if !e.config.Verbose {
		t.Error("Verbose should be true")
	}
}

func TestShouldRerunStep(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name   string
		result StepResult
		want   bool
	}{
		{
			name:   "failed status",
			result: StepResult{Status: StatusFailed},
			want:   true,
		},
		{
			name:   "cancelled status",
			result: StepResult{Status: StatusCancelled},
			want:   true,
		},
		{
			name:   "running status",
			result: StepResult{Status: StatusRunning},
			want:   true,
		},
		{
			name:   "pending status",
			result: StepResult{Status: StatusPending},
			want:   true,
		},
		{
			name:   "empty status",
			result: StepResult{Status: ""},
			want:   true,
		},
		{
			name:   "completed status",
			result: StepResult{Status: StatusCompleted},
			want:   false,
		},
		{
			name:   "skipped - dependency failed",
			result: StepResult{Status: StatusSkipped, SkipReason: "dependency failed: step1"},
			want:   true,
		},
		{
			name:   "skipped - cancelled",
			result: StepResult{Status: StatusSkipped, SkipReason: "cancelled during execution"},
			want:   true,
		},
		{
			name:   "skipped - when condition false",
			result: StepResult{Status: StatusSkipped, SkipReason: "when condition evaluated to false"},
			want:   false,
		},
		{
			name:   "skipped - no reason",
			result: StepResult{Status: StatusSkipped, SkipReason: ""},
			want:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := shouldRerunStep(tt.result)
			if got != tt.want {
				t.Errorf("shouldRerunStep(%+v) = %v, want %v", tt.result, got, tt.want)
			}
		})
	}
}

func TestExecutor_ClearStepVariables(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name          string
		state         *ExecutionState
		workflow      *Workflow
		stepID        string
		wantVariables map[string]interface{}
	}{
		{
			name:          "nil state",
			state:         nil,
			workflow:      &Workflow{},
			stepID:        "step1",
			wantVariables: nil,
		},
		{
			name: "nil variables in state",
			state: &ExecutionState{
				Variables: nil,
			},
			workflow:      &Workflow{},
			stepID:        "step1",
			wantVariables: nil,
		},
		{
			name: "clears step output variables",
			state: &ExecutionState{
				Variables: map[string]interface{}{
					"steps.step1.output": "some output",
					"steps.step1.data":   map[string]interface{}{"key": "value"},
					"steps.step2.output": "other output",
					"other_var":          "keep this",
				},
			},
			workflow: &Workflow{
				Steps: []Step{{ID: "step1", Prompt: "test"}},
			},
			stepID: "step1",
			wantVariables: map[string]interface{}{
				"steps.step2.output": "other output",
				"other_var":          "keep this",
			},
		},
		{
			name: "clears custom output_var",
			state: &ExecutionState{
				Variables: map[string]interface{}{
					"steps.step1.output":   "output",
					"steps.step1.data":     "data",
					"my_custom_var":        "custom value",
					"my_custom_var_parsed": map[string]interface{}{"parsed": true},
					"keep_me":              "still here",
				},
			},
			workflow: &Workflow{
				Steps: []Step{{ID: "step1", Prompt: "test", OutputVar: "my_custom_var"}},
			},
			stepID: "step1",
			wantVariables: map[string]interface{}{
				"keep_me": "still here",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			// Create executor
			cfg := DefaultExecutorConfig("test")
			e := NewExecutor(cfg)
			e.state = tt.state

			// Create dependency graph if workflow provided
			if tt.workflow != nil {
				e.graph = NewDependencyGraph(tt.workflow)
			}

			// Run clearStepVariables
			e.clearStepVariables(tt.stepID)

			// Verify results
			if tt.wantVariables == nil {
				if tt.state != nil && tt.state.Variables != nil {
					// State was nil or variables were nil, nothing to check
					return
				}
				return
			}

			if len(e.state.Variables) != len(tt.wantVariables) {
				t.Errorf("clearStepVariables() left %d variables, want %d", len(e.state.Variables), len(tt.wantVariables))
				t.Errorf("got: %v", e.state.Variables)
				t.Errorf("want: %v", tt.wantVariables)
				return
			}

			for k, want := range tt.wantVariables {
				got, ok := e.state.Variables[k]
				if !ok {
					t.Errorf("clearStepVariables() missing variable %q", k)
					continue
				}
				// For simple string comparisons
				if gotStr, ok := got.(string); ok {
					if wantStr, ok := want.(string); ok {
						if gotStr != wantStr {
							t.Errorf("variable %q = %q, want %q", k, gotStr, wantStr)
						}
					}
				}
			}
		})
	}
}

func TestExecutor_ApplyResumeState(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name         string
		state        *ExecutionState
		workflow     *Workflow
		wantExecuted []string
		wantRemoved  []string
	}{
		{
			name:     "nil state",
			state:    nil,
			workflow: &Workflow{},
		},
		{
			name: "completed steps are marked executed",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {StepID: "step1", Status: StatusCompleted},
					"step2": {StepID: "step2", Status: StatusCompleted},
				},
			},
			workflow: &Workflow{
				Steps: []Step{
					{ID: "step1", Prompt: "test1"},
					{ID: "step2", Prompt: "test2"},
				},
			},
			wantExecuted: []string{"step1", "step2"},
		},
		{
			name: "failed steps are cleared for rerun",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {StepID: "step1", Status: StatusCompleted},
					"step2": {StepID: "step2", Status: StatusFailed},
				},
				Variables: map[string]interface{}{
					"steps.step2.output": "old output",
				},
			},
			workflow: &Workflow{
				Steps: []Step{
					{ID: "step1", Prompt: "test1"},
					{ID: "step2", Prompt: "test2"},
				},
			},
			wantExecuted: []string{"step1"},
			wantRemoved:  []string{"step2"},
		},
		{
			name: "running steps are cleared for rerun",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {StepID: "step1", Status: StatusRunning},
				},
				Variables: map[string]interface{}{},
			},
			workflow: &Workflow{
				Steps: []Step{
					{ID: "step1", Prompt: "test1"},
				},
			},
			wantExecuted: []string{},
			wantRemoved:  []string{"step1"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			cfg := DefaultExecutorConfig("test")
			e := NewExecutor(cfg)
			e.state = tt.state

			if tt.workflow != nil {
				e.graph = NewDependencyGraph(tt.workflow)
			}

			e.applyResumeState()

			// Check executed steps
			for _, stepID := range tt.wantExecuted {
				if !e.graph.IsExecuted(stepID) {
					t.Errorf("step %q should be marked executed", stepID)
				}
			}

			// Check removed steps
			for _, stepID := range tt.wantRemoved {
				if _, exists := e.state.Steps[stepID]; exists {
					t.Errorf("step %q should be removed from state", stepID)
				}
			}
		})
	}
}

// TestExecutor_Run_DryRun tests full workflow execution in dry run mode
func TestExecutor_Run_DryRun(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Steps: []Step{
			{ID: "step1", Prompt: "Do task 1"},
			{ID: "step2", Prompt: "Do task 2", DependsOn: []string{"step1"}},
		},
	}

	ctx := context.Background()
	state, err := e.Run(ctx, workflow, nil, nil)

	if err != nil {
		t.Fatalf("Run() returned error in dry run mode: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
	if len(state.Steps) != 2 {
		t.Errorf("expected 2 step results, got %d", len(state.Steps))
	}
	for _, stepID := range []string{"step1", "step2"} {
		result, ok := state.Steps[stepID]
		if !ok {
			t.Errorf("missing step result for %s", stepID)
			continue
		}
		if result.Status != StatusCompleted {
			t.Errorf("step %s status = %v, want Completed", stepID, result.Status)
		}
		if !strings.Contains(result.Output, "[DRY RUN]") {
			t.Errorf("step %s output should contain [DRY RUN], got %q", stepID, result.Output)
		}
	}
}

// TestExecutor_Run_DryRun_WithVariables tests variable substitution in dry run mode
func TestExecutor_Run_DryRun_WithVariables(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Vars: map[string]VarDef{
			"target": {Default: "default-target"},
		},
		Steps: []Step{
			{ID: "step1", Prompt: "Process ${vars.target}"},
		},
	}

	ctx := context.Background()
	vars := map[string]interface{}{"target": "custom-target"}
	state, err := e.Run(ctx, workflow, vars, nil)

	if err != nil {
		t.Fatalf("Run() returned error: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
	// Variable should be substituted
	if state.Variables["target"] != "custom-target" {
		t.Errorf("variable target = %v, want custom-target", state.Variables["target"])
	}
}

// TestExecutor_Run_DryRun_WithConditional tests conditional steps in dry run mode
func TestExecutor_Run_DryRun_WithConditional(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Vars: map[string]VarDef{
			"enabled": {Default: false},
		},
		Steps: []Step{
			{ID: "always", Prompt: "Always run"},
			{ID: "conditional", Prompt: "Maybe run", When: "${vars.enabled}"},
		},
	}

	ctx := context.Background()
	state, err := e.Run(ctx, workflow, nil, nil)

	if err != nil {
		t.Fatalf("Run() returned error: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
	// "always" should complete
	if result := state.Steps["always"]; result.Status != StatusCompleted {
		t.Errorf("always step status = %v, want Completed", result.Status)
	}
	// "conditional" should be skipped (vars.enabled is false)
	if result := state.Steps["conditional"]; result.Status != StatusSkipped {
		t.Errorf("conditional step status = %v, want Skipped", result.Status)
	}
}

// TestExecutor_Resume_DryRun tests resume functionality in dry run mode
func TestExecutor_Resume_DryRun(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Steps: []Step{
			{ID: "step1", Prompt: "Do task 1"},
			{ID: "step2", Prompt: "Do task 2", DependsOn: []string{"step1"}},
			{ID: "step3", Prompt: "Do task 3", DependsOn: []string{"step2"}},
		},
	}

	// Create prior state with step1 already completed
	prior := &ExecutionState{
		RunID:      "resume-test",
		WorkflowID: "test-workflow",
		Status:     StatusRunning,
		StartedAt:  time.Now().Add(-time.Minute),
		Steps: map[string]StepResult{
			"step1": {
				StepID:     "step1",
				Status:     StatusCompleted,
				Output:     "step1 output",
				StartedAt:  time.Now().Add(-time.Minute),
				FinishedAt: time.Now().Add(-30 * time.Second),
			},
		},
		Variables: make(map[string]interface{}),
	}

	ctx := context.Background()
	state, err := e.Resume(ctx, workflow, prior, nil)

	if err != nil {
		t.Fatalf("Resume() returned error: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
	// step1 should still be completed (from prior)
	if state.Steps["step1"].Status != StatusCompleted {
		t.Errorf("step1 status = %v, want Completed (from prior)", state.Steps["step1"].Status)
	}
	// step2 and step3 should be newly completed
	for _, stepID := range []string{"step2", "step3"} {
		if result := state.Steps[stepID]; result.Status != StatusCompleted {
			t.Errorf("step %s status = %v, want Completed", stepID, result.Status)
		}
	}
}

// TestExecutor_Resume_NilState tests resume with nil state
func TestExecutor_Resume_NilState(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Steps:         []Step{{ID: "step1", Prompt: "task"}},
	}

	ctx := context.Background()
	_, err := e.Resume(ctx, workflow, nil, nil)

	if err == nil {
		t.Error("Resume() should return error for nil state")
	}
}

// TestExecutor_sendNotification tests notification sending
func TestExecutor_sendNotification(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	e := NewExecutor(cfg)

	// Set up state for notification
	e.state = &ExecutionState{
		RunID:      "notify-test",
		WorkflowID: "test-workflow",
		Status:     StatusCompleted,
		StartedAt:  time.Now(),
		FinishedAt: time.Now(),
		Steps:      make(map[string]StepResult),
	}

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings: WorkflowSettings{
			NotifyOnComplete: true,
		},
	}

	// Test with nil notifier (should not panic)
	e.sendNotification(context.Background(), workflow, NotifyCompleted)

	// Test with notifier set
	notifier := NewNotifier(NotifierConfig{
		Channels: []string{"desktop"},
	})
	e.SetNotifier(notifier)

	// This should call the notifier (won't actually send since no real desktop)
	e.sendNotification(context.Background(), workflow, NotifyCompleted)

	// Test with event that shouldn't notify
	workflow.Settings.NotifyOnComplete = false
	e.sendNotification(context.Background(), workflow, NotifyCompleted)
}

// TestExecutor_selectPane_DryRun tests selectPane returns dummy values in dry run mode
func TestExecutor_selectPane_DryRun(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	step := &Step{ID: "step1", Prompt: "test prompt"}
	paneID, agentType, err := e.selectPane(step)

	if err != nil {
		t.Fatalf("selectPane() returned error: %v", err)
	}
	if paneID != "dry-run-pane" {
		t.Errorf("paneID = %q, want %q", paneID, "dry-run-pane")
	}
	if agentType != "dry-run-agent" {
		t.Errorf("agentType = %q, want %q", agentType, "dry-run-agent")
	}
}

// TestExecutor_Run_DryRun_ProgressEvents tests progress events are emitted in dry run mode
func TestExecutor_Run_DryRun_ProgressEvents(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Steps: []Step{
			{ID: "step1", Prompt: "Task 1"},
		},
	}

	progress := make(chan ProgressEvent, 100)
	ctx := context.Background()
	_, err := e.Run(ctx, workflow, nil, progress)

	if err != nil {
		t.Fatalf("Run() returned error: %v", err)
	}

	// Collect progress events
	close(progress)
	events := make([]ProgressEvent, 0)
	for event := range progress {
		events = append(events, event)
	}

	// Should have at least workflow_start, step_start, step_complete, workflow_complete
	if len(events) < 4 {
		t.Errorf("expected at least 4 progress events, got %d", len(events))
	}

	// First event should be workflow_start
	if len(events) > 0 && events[0].Type != "workflow_start" {
		t.Errorf("first event type = %q, want workflow_start", events[0].Type)
	}

	// Last event should be workflow_complete
	if len(events) > 0 && events[len(events)-1].Type != "workflow_complete" {
		t.Errorf("last event type = %q, want workflow_complete", events[len(events)-1].Type)
	}
}

func TestCaptureErrorContext_DryRun(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	// DryRun mode should return empty string
	result := e.captureErrorContext("pane-1", 100)
	if result != "" {
		t.Errorf("captureErrorContext in DryRun = %q, want empty string", result)
	}
}

func TestCaptureErrorContext_EmptyPaneID(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Empty paneID should return empty string
	result := e.captureErrorContext("", 100)
	if result != "" {
		t.Errorf("captureErrorContext with empty paneID = %q, want empty string", result)
	}
}

func TestDetectAgentState_DryRun(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	// DryRun mode should return empty string
	result := e.detectAgentState("pane-1")
	if result != "" {
		t.Errorf("detectAgentState in DryRun = %q, want empty string", result)
	}
}

func TestDetectAgentState_EmptyPaneID(t *testing.T) {
	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	// Empty paneID should return empty string
	result := e.detectAgentState("")
	if result != "" {
		t.Errorf("detectAgentState with empty paneID = %q, want empty string", result)
	}
}

// TestExecutor_selectPaneExcluding_DryRun tests selectPaneExcluding in dry run mode
func TestExecutor_selectPaneExcluding_DryRun(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	step := &Step{ID: "step1", Prompt: "test prompt"}
	usedPanes := make(map[string]bool)
	var mu sync.Mutex

	paneID, agentType, err := e.selectPaneExcluding(step, usedPanes, &mu)

	if err != nil {
		t.Fatalf("selectPaneExcluding() returned error: %v", err)
	}
	if paneID != "dry-run-pane" {
		t.Errorf("paneID = %q, want %q", paneID, "dry-run-pane")
	}
	if agentType != "dry-run-agent" {
		t.Errorf("agentType = %q, want %q", agentType, "dry-run-agent")
	}
}

// TestExecutor_selectPaneExcluding_DryRun_WithUsedPanes tests that dry run ignores usedPanes
func TestExecutor_selectPaneExcluding_DryRun_WithUsedPanes(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	step := &Step{ID: "step1", Prompt: "test prompt"}
	usedPanes := map[string]bool{
		"dry-run-pane": true, // Already marked as used
	}
	var mu sync.Mutex

	// In dry run mode, should still return dry-run-pane regardless of usedPanes
	paneID, agentType, err := e.selectPaneExcluding(step, usedPanes, &mu)

	if err != nil {
		t.Fatalf("selectPaneExcluding() returned error: %v", err)
	}
	if paneID != "dry-run-pane" {
		t.Errorf("paneID = %q, want %q", paneID, "dry-run-pane")
	}
	if agentType != "dry-run-agent" {
		t.Errorf("agentType = %q, want %q", agentType, "dry-run-agent")
	}
}

// TestWaitForIdle_ContextCancelled tests waitForIdle with cancelled context
func TestWaitForIdle_ContextCancelled(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	cfg.ProgressInterval = 50 * time.Millisecond // Fast for testing
	e := NewExecutor(cfg)

	// Create already cancelled context
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	err := e.waitForIdle(ctx, "pane-1", 5*time.Second)

	if err == nil {
		t.Error("waitForIdle() should return error for cancelled context")
	}
	if !errors.Is(err, context.Canceled) {
		t.Errorf("waitForIdle() error = %v, want context.Canceled", err)
	}
}

// TestWaitForIdle_ContextDeadline tests waitForIdle with deadline exceeded
func TestWaitForIdle_ContextDeadline(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	cfg.ProgressInterval = 50 * time.Millisecond // Fast for testing
	e := NewExecutor(cfg)

	// Create context with very short deadline
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
	defer cancel()

	err := e.waitForIdle(ctx, "pane-1", 5*time.Second)

	if err == nil {
		t.Error("waitForIdle() should return error for deadline exceeded")
	}
	// Should get context error before timeout
	if !errors.Is(err, context.DeadlineExceeded) {
		t.Errorf("waitForIdle() error = %v, want context.DeadlineExceeded", err)
	}
}

// TestPersistState_NilState tests persistState with nil state
func TestPersistState_NilState(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)
	e.state = nil

	// Should not panic with nil state
	e.persistState()
}

// TestPersistState_EmptyProjectDir tests persistState with empty project dir
func TestPersistState_EmptyProjectDir(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	cfg.ProjectDir = "" // Empty project dir
	e := NewExecutor(cfg)
	e.state = &ExecutionState{
		RunID:      "test-run",
		WorkflowID: "test-workflow",
	}

	// Should not panic and should return early
	e.persistState()
}

// TestSnapshotState tests snapshotState function
func TestSnapshotState(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)

	now := time.Now()
	e.state = &ExecutionState{
		RunID:      "test-run",
		WorkflowID: "test-workflow",
		Status:     StatusRunning,
		StartedAt:  now,
		Steps: map[string]StepResult{
			"step1": {StepID: "step1", Status: StatusCompleted, Output: "output1"},
		},
		Variables: map[string]interface{}{
			"var1": "value1",
		},
	}

	snapshot := e.snapshotState()

	if snapshot == nil {
		t.Fatal("snapshotState() returned nil")
	}
	if snapshot.RunID != "test-run" {
		t.Errorf("snapshot.RunID = %q, want %q", snapshot.RunID, "test-run")
	}
	if len(snapshot.Steps) != 1 {
		t.Errorf("snapshot.Steps length = %d, want 1", len(snapshot.Steps))
	}
	if len(snapshot.Variables) != 1 {
		t.Errorf("snapshot.Variables length = %d, want 1", len(snapshot.Variables))
	}

	// Verify it's a copy, not the same reference
	e.state.Variables["var2"] = "value2"
	if _, exists := snapshot.Variables["var2"]; exists {
		t.Error("snapshot.Variables should be a copy, not a reference")
	}
}

// TestSnapshotState_NilState tests snapshotState with nil state
func TestSnapshotState_NilState(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test")
	e := NewExecutor(cfg)
	e.state = nil

	snapshot := e.snapshotState()

	if snapshot != nil {
		t.Error("snapshotState() should return nil for nil state")
	}
}

// TestExecutor_Run_DryRun_WithParallel tests parallel step execution in dry run mode
func TestExecutor_Run_DryRun_WithParallel(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Steps: []Step{
			{ID: "step1", Prompt: "Task 1"},
			{
				ID: "step2",
				Parallel: []Step{
					{ID: "parallel-a", Prompt: "Parallel task A"},
					{ID: "parallel-b", Prompt: "Parallel task B"},
				},
			},
			{ID: "step3", Prompt: "Task 3", DependsOn: []string{"step2"}},
		},
	}

	ctx := context.Background()
	state, err := e.Run(ctx, workflow, nil, nil)

	if err != nil {
		t.Fatalf("Run() returned error: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
}

// TestExecutor_Run_DryRun_WithLoop tests loop step execution in dry run mode
func TestExecutor_Run_DryRun_WithLoop(t *testing.T) {
	t.Parallel()

	cfg := DefaultExecutorConfig("test-session")
	cfg.DryRun = true
	e := NewExecutor(cfg)

	workflow := &Workflow{
		SchemaVersion: SchemaVersion,
		Name:          "test-workflow",
		Settings:      DefaultWorkflowSettings(),
		Vars: map[string]VarDef{
			"items": {Default: []interface{}{"item1", "item2", "item3"}},
		},
		Steps: []Step{
			{
				ID:     "loop-step",
				Prompt: "Process ${loop.item}",
				Loop: &LoopConfig{
					Items: "${vars.items}",
				},
			},
		},
	}

	ctx := context.Background()
	state, err := e.Run(ctx, workflow, nil, nil)

	if err != nil {
		t.Fatalf("Run() returned error: %v", err)
	}
	if state.Status != StatusCompleted {
		t.Errorf("state.Status = %v, want Completed", state.Status)
	}
}
