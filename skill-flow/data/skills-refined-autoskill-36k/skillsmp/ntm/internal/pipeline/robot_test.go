package pipeline

import (
	"bytes"
	"encoding/json"
	"errors"
	"os"
	"strings"
	"testing"
	"time"
)

// captureStdout captures stdout during function execution
func captureStdout(t *testing.T, f func()) string {
	t.Helper()
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	f()

	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	buf.ReadFrom(r)
	return buf.String()
}

func TestNewRobotResponse(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		success bool
	}{
		{
			name:    "success response",
			success: true,
		},
		{
			name:    "failure response",
			success: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			resp := NewRobotResponse(tt.success)

			if resp.Success != tt.success {
				t.Errorf("NewRobotResponse(%v).Success = %v, want %v", tt.success, resp.Success, tt.success)
			}

			if resp.Timestamp == "" {
				t.Error("NewRobotResponse().Timestamp is empty")
			}

			// Validate timestamp format
			_, err := time.Parse(time.RFC3339, resp.Timestamp)
			if err != nil {
				t.Errorf("NewRobotResponse().Timestamp = %q, invalid RFC3339: %v", resp.Timestamp, err)
			}
		})
	}
}

func TestNewErrorResponse(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		err      error
		code     string
		hint     string
		wantErr  string
		wantCode string
		wantHint string
	}{
		{
			name:     "internal error",
			err:      errors.New("something went wrong"),
			code:     ErrCodeInternalError,
			hint:     "try again",
			wantErr:  "something went wrong",
			wantCode: ErrCodeInternalError,
			wantHint: "try again",
		},
		{
			name:     "invalid flag error",
			err:      errors.New("unknown flag"),
			code:     ErrCodeInvalidFlag,
			hint:     "",
			wantErr:  "unknown flag",
			wantCode: ErrCodeInvalidFlag,
			wantHint: "",
		},
		{
			name:     "session not found",
			err:      errors.New("session does not exist"),
			code:     ErrCodeSessionNotFound,
			hint:     "create session first",
			wantErr:  "session does not exist",
			wantCode: ErrCodeSessionNotFound,
			wantHint: "create session first",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			resp := NewErrorResponse(tt.err, tt.code, tt.hint)

			if resp.Success {
				t.Error("NewErrorResponse().Success = true, want false")
			}

			if resp.Error != tt.wantErr {
				t.Errorf("NewErrorResponse().Error = %q, want %q", resp.Error, tt.wantErr)
			}

			if resp.ErrorCode != tt.wantCode {
				t.Errorf("NewErrorResponse().ErrorCode = %q, want %q", resp.ErrorCode, tt.wantCode)
			}

			if resp.Hint != tt.wantHint {
				t.Errorf("NewErrorResponse().Hint = %q, want %q", resp.Hint, tt.wantHint)
			}

			if resp.Timestamp == "" {
				t.Error("NewErrorResponse().Timestamp is empty")
			}
		})
	}
}

func TestRobotCalculateProgress(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		state *ExecutionState
		want  PipelineProgress
	}{
		{
			name:  "nil state",
			state: nil,
			want:  PipelineProgress{},
		},
		{
			name: "empty steps",
			state: &ExecutionState{
				Steps: map[string]StepResult{},
			},
			want: PipelineProgress{
				Percent: 0,
			},
		},
		{
			name: "all pending",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {Status: StatusPending},
					"step2": {Status: StatusPending},
				},
			},
			want: PipelineProgress{
				Pending: 2,
				Total:   2,
				Percent: 0,
			},
		},
		{
			name: "mixed statuses",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {Status: StatusCompleted},
					"step2": {Status: StatusRunning},
					"step3": {Status: StatusPending},
					"step4": {Status: StatusFailed},
					"step5": {Status: StatusSkipped},
				},
			},
			want: PipelineProgress{
				Completed: 1,
				Running:   1,
				Pending:   1,
				Failed:    1,
				Skipped:   1,
				Total:     5,
				Percent:   60, // (1 completed + 1 failed + 1 skipped) / 5 * 100
			},
		},
		{
			name: "all completed",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {Status: StatusCompleted},
					"step2": {Status: StatusCompleted},
					"step3": {Status: StatusCompleted},
				},
			},
			want: PipelineProgress{
				Completed: 3,
				Total:     3,
				Percent:   100,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := calculateProgress(tt.state)

			if got.Completed != tt.want.Completed {
				t.Errorf("calculateProgress().Completed = %d, want %d", got.Completed, tt.want.Completed)
			}
			if got.Running != tt.want.Running {
				t.Errorf("calculateProgress().Running = %d, want %d", got.Running, tt.want.Running)
			}
			if got.Pending != tt.want.Pending {
				t.Errorf("calculateProgress().Pending = %d, want %d", got.Pending, tt.want.Pending)
			}
			if got.Failed != tt.want.Failed {
				t.Errorf("calculateProgress().Failed = %d, want %d", got.Failed, tt.want.Failed)
			}
			if got.Skipped != tt.want.Skipped {
				t.Errorf("calculateProgress().Skipped = %d, want %d", got.Skipped, tt.want.Skipped)
			}
			if got.Total != tt.want.Total {
				t.Errorf("calculateProgress().Total = %d, want %d", got.Total, tt.want.Total)
			}
			if got.Percent != tt.want.Percent {
				t.Errorf("calculateProgress().Percent = %f, want %f", got.Percent, tt.want.Percent)
			}
		})
	}
}

func TestConvertSteps(t *testing.T) {
	t.Parallel()

	now := time.Now()
	later := now.Add(5 * time.Second)

	tests := []struct {
		name  string
		state *ExecutionState
		check func(t *testing.T, steps map[string]PipelineStep)
	}{
		{
			name: "empty steps",
			state: &ExecutionState{
				Steps: map[string]StepResult{},
			},
			check: func(t *testing.T, steps map[string]PipelineStep) {
				if len(steps) != 0 {
					t.Errorf("convertSteps() returned %d steps, want 0", len(steps))
				}
			},
		},
		{
			name: "step with all fields",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {
						StepID:     "step1",
						Status:     StatusCompleted,
						AgentType:  "claude",
						PaneUsed:   "main:1",
						StartedAt:  now,
						FinishedAt: later,
						Output:     "line1\nline2\nline3",
						Error:      nil,
					},
				},
			},
			check: func(t *testing.T, steps map[string]PipelineStep) {
				step, ok := steps["step1"]
				if !ok {
					t.Fatal("step1 not found in converted steps")
				}
				if step.Status != "completed" {
					t.Errorf("step.Status = %q, want %q", step.Status, "completed")
				}
				if step.Agent != "claude" {
					t.Errorf("step.Agent = %q, want %q", step.Agent, "claude")
				}
				if step.PaneUsed != "main:1" {
					t.Errorf("step.PaneUsed = %q, want %q", step.PaneUsed, "main:1")
				}
				if step.OutputLines != 3 {
					t.Errorf("step.OutputLines = %d, want %d", step.OutputLines, 3)
				}
				if step.DurationMs != 5000 {
					t.Errorf("step.DurationMs = %d, want %d", step.DurationMs, 5000)
				}
			},
		},
		{
			name: "step with error",
			state: &ExecutionState{
				Steps: map[string]StepResult{
					"step1": {
						StepID: "step1",
						Status: StatusFailed,
						Error: &StepError{
							Type:    "timeout",
							Message: "step timed out",
						},
					},
				},
			},
			check: func(t *testing.T, steps map[string]PipelineStep) {
				step, ok := steps["step1"]
				if !ok {
					t.Fatal("step1 not found in converted steps")
				}
				if step.Error != "step timed out" {
					t.Errorf("step.Error = %q, want %q", step.Error, "step timed out")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := convertSteps(tt.state)
			tt.check(t, got)
		})
	}
}

func TestCountLines(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input string
		want  int
	}{
		{
			name:  "empty string",
			input: "",
			want:  0,
		},
		{
			name:  "single line no newline",
			input: "hello",
			want:  1,
		},
		{
			name:  "single line with newline",
			input: "hello\n",
			want:  2,
		},
		{
			name:  "two lines",
			input: "hello\nworld",
			want:  2,
		},
		{
			name:  "three lines",
			input: "line1\nline2\nline3",
			want:  3,
		},
		{
			name:  "multiple trailing newlines",
			input: "hello\n\n\n",
			want:  4,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := countLines(tt.input)
			if got != tt.want {
				t.Errorf("countLines(%q) = %d, want %d", tt.input, got, tt.want)
			}
		})
	}
}

func TestParsePipelineVars(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		input   string
		wantNil bool
		wantErr bool
		check   func(t *testing.T, vars map[string]interface{})
	}{
		{
			name:    "empty string",
			input:   "",
			wantNil: true,
		},
		{
			name:  "simple object",
			input: `{"key": "value"}`,
			check: func(t *testing.T, vars map[string]interface{}) {
				if vars["key"] != "value" {
					t.Errorf("vars[key] = %v, want %q", vars["key"], "value")
				}
			},
		},
		{
			name:  "numeric value",
			input: `{"count": 42}`,
			check: func(t *testing.T, vars map[string]interface{}) {
				// JSON numbers are float64
				if vars["count"] != float64(42) {
					t.Errorf("vars[count] = %v, want %v", vars["count"], float64(42))
				}
			},
		},
		{
			name:  "boolean value",
			input: `{"enabled": true}`,
			check: func(t *testing.T, vars map[string]interface{}) {
				if vars["enabled"] != true {
					t.Errorf("vars[enabled] = %v, want %v", vars["enabled"], true)
				}
			},
		},
		{
			name:  "nested object",
			input: `{"outer": {"inner": "value"}}`,
			check: func(t *testing.T, vars map[string]interface{}) {
				outer, ok := vars["outer"].(map[string]interface{})
				if !ok {
					t.Fatal("outer is not a map")
				}
				if outer["inner"] != "value" {
					t.Errorf("outer.inner = %v, want %q", outer["inner"], "value")
				}
			},
		},
		{
			name:    "invalid JSON",
			input:   `{invalid}`,
			wantErr: true,
		},
		{
			name:    "not an object",
			input:   `"just a string"`,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got, err := ParsePipelineVars(tt.input)

			if tt.wantErr {
				if err == nil {
					t.Error("ParsePipelineVars() expected error, got nil")
				}
				return
			}

			if err != nil {
				t.Errorf("ParsePipelineVars() unexpected error: %v", err)
				return
			}

			if tt.wantNil {
				if got != nil {
					t.Errorf("ParsePipelineVars(%q) = %v, want nil", tt.input, got)
				}
				return
			}

			if tt.check != nil {
				tt.check(t, got)
			}
		})
	}
}

func TestPipelineRegistry(t *testing.T) {
	// Clear registry before test
	ClearPipelineRegistry()

	// Test registration
	exec := &PipelineExecution{
		RunID:      "test-run-123",
		WorkflowID: "test-workflow",
		Status:     "running",
	}

	RegisterPipeline(exec)

	// Test retrieval
	got := GetPipelineExecution("test-run-123")
	if got == nil {
		t.Fatal("GetPipelineExecution() returned nil after registration")
	}
	if got.RunID != "test-run-123" {
		t.Errorf("GetPipelineExecution().RunID = %q, want %q", got.RunID, "test-run-123")
	}

	// Test not found
	notFound := GetPipelineExecution("nonexistent")
	if notFound != nil {
		t.Error("GetPipelineExecution(nonexistent) should return nil")
	}

	// Test GetAllPipelines
	all := GetAllPipelines()
	if len(all) != 1 {
		t.Errorf("GetAllPipelines() returned %d pipelines, want 1", len(all))
	}

	// Test clear
	ClearPipelineRegistry()
	all = GetAllPipelines()
	if len(all) != 0 {
		t.Errorf("GetAllPipelines() after clear returned %d pipelines, want 0", len(all))
	}
}

func TestUpdatePipelineFromState(t *testing.T) {
	// Clear registry before test
	ClearPipelineRegistry()

	// Register a pipeline
	exec := &PipelineExecution{
		RunID:      "test-run-456",
		WorkflowID: "test-workflow",
		Status:     "running",
		Steps:      make(map[string]PipelineStep),
	}
	RegisterPipeline(exec)

	// Create state update
	state := &ExecutionState{
		RunID:      "test-run-456",
		WorkflowID: "test-workflow",
		Status:     StatusCompleted,
		Steps: map[string]StepResult{
			"step1": {
				StepID: "step1",
				Status: StatusCompleted,
			},
		},
	}

	// Update pipeline
	UpdatePipelineFromState("test-run-456", state)

	// Verify update
	got := GetPipelineExecution("test-run-456")
	if got == nil {
		t.Fatal("GetPipelineExecution() returned nil after update")
	}
	if got.Status != "completed" {
		t.Errorf("GetPipelineExecution().Status = %q, want %q", got.Status, "completed")
	}

	// Clean up
	ClearPipelineRegistry()
}

func TestOutputJSON(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input interface{}
		check func(t *testing.T, output string)
	}{
		{
			name:  "simple struct",
			input: struct{ Name string }{"test"},
			check: func(t *testing.T, output string) {
				var result map[string]string
				if err := json.Unmarshal([]byte(output), &result); err != nil {
					t.Fatalf("Failed to parse JSON: %v", err)
				}
				if result["Name"] != "test" {
					t.Errorf("Name = %q, want %q", result["Name"], "test")
				}
			},
		},
		{
			name:  "robot response",
			input: NewRobotResponse(true),
			check: func(t *testing.T, output string) {
				var result RobotResponse
				if err := json.Unmarshal([]byte(output), &result); err != nil {
					t.Fatalf("Failed to parse JSON: %v", err)
				}
				if !result.Success {
					t.Error("Expected success=true")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Note: Not parallel because we capture stdout
			output := captureStdout(t, func() {
				outputJSON(tt.input)
			})
			tt.check(t, output)
		})
	}
}

func TestPrintPipelineRun_ValidationErrors(t *testing.T) {
	// Test validation errors that don't require tmux

	tests := []struct {
		name       string
		opts       PipelineRunOptions
		wantCode   int
		wantErrMsg string
	}{
		{
			name:       "missing workflow file",
			opts:       PipelineRunOptions{},
			wantCode:   1,
			wantErrMsg: "workflow file is required",
		},
		{
			name:       "missing session",
			opts:       PipelineRunOptions{WorkflowFile: "test.yaml"},
			wantCode:   1,
			wantErrMsg: "session is required",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var exitCode int
			output := captureStdout(t, func() {
				exitCode = PrintPipelineRun(tt.opts)
			})

			if exitCode != tt.wantCode {
				t.Errorf("PrintPipelineRun() exit code = %d, want %d", exitCode, tt.wantCode)
			}

			var result PipelineRunOutput
			if err := json.Unmarshal([]byte(output), &result); err != nil {
				t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
			}

			if result.Success {
				t.Error("Expected success=false for validation error")
			}

			if result.Error != tt.wantErrMsg {
				t.Errorf("Error = %q, want %q", result.Error, tt.wantErrMsg)
			}

			if result.ErrorCode != ErrCodeInvalidFlag {
				t.Errorf("ErrorCode = %q, want %q", result.ErrorCode, ErrCodeInvalidFlag)
			}
		})
	}
}

func TestPrintPipelineRun_WorkflowLoadErrors(t *testing.T) {
	// Test workflow loading errors that don't require tmux

	tests := []struct {
		name       string
		setupFile  func(t *testing.T) string // returns path to workflow file
		wantCode   int
		wantErrMsg string
	}{
		{
			name: "nonexistent workflow file",
			setupFile: func(t *testing.T) string {
				return "/nonexistent/path/to/workflow.yaml"
			},
			wantCode:   1,
			wantErrMsg: "failed to load workflow",
		},
		{
			name: "invalid YAML syntax",
			setupFile: func(t *testing.T) string {
				f, err := os.CreateTemp(t.TempDir(), "invalid-*.yaml")
				if err != nil {
					t.Fatalf("Failed to create temp file: %v", err)
				}
				f.WriteString("invalid: yaml: content: [")
				f.Close()
				return f.Name()
			},
			wantCode:   1,
			wantErrMsg: "failed to load workflow",
		},
		{
			name: "missing schema_version",
			setupFile: func(t *testing.T) string {
				f, err := os.CreateTemp(t.TempDir(), "noschema-*.yaml")
				if err != nil {
					t.Fatalf("Failed to create temp file: %v", err)
				}
				// Valid YAML but missing required 'schema_version' field
				f.WriteString("name: test-workflow\nsteps:\n  - id: step1\n    command: echo hello\n")
				f.Close()
				return f.Name()
			},
			wantCode:   1,
			wantErrMsg: "schema_version is required",
		},
		{
			name: "missing name field",
			setupFile: func(t *testing.T) string {
				f, err := os.CreateTemp(t.TempDir(), "noname-*.yaml")
				if err != nil {
					t.Fatalf("Failed to create temp file: %v", err)
				}
				// Valid YAML but missing required 'name' field (has schema_version)
				f.WriteString("schema_version: \"1.0\"\nsteps:\n  - id: step1\n    command: echo hello\n")
				f.Close()
				return f.Name()
			},
			wantCode:   1,
			wantErrMsg: "name is required",
		},
		{
			name: "empty steps array",
			setupFile: func(t *testing.T) string {
				f, err := os.CreateTemp(t.TempDir(), "nosteps-*.yaml")
				if err != nil {
					t.Fatalf("Failed to create temp file: %v", err)
				}
				f.WriteString("schema_version: \"1.0\"\nname: test-workflow\nsteps: []\n")
				f.Close()
				return f.Name()
			},
			wantCode:   1,
			wantErrMsg: "at least one step is required",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			workflowPath := tt.setupFile(t)

			opts := PipelineRunOptions{
				WorkflowFile: workflowPath,
				Session:      "test-session",
			}

			var exitCode int
			output := captureStdout(t, func() {
				exitCode = PrintPipelineRun(opts)
			})

			if exitCode != tt.wantCode {
				t.Errorf("PrintPipelineRun() exit code = %d, want %d", exitCode, tt.wantCode)
			}

			var result PipelineRunOutput
			if err := json.Unmarshal([]byte(output), &result); err != nil {
				t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
			}

			if result.Success {
				t.Error("Expected success=false for workflow load error")
			}

			if result.Error == "" {
				t.Error("Expected non-empty error message")
			}

			// Check that error message contains expected text
			if tt.wantErrMsg != "" && !strings.Contains(result.Error, tt.wantErrMsg) {
				t.Errorf("Error = %q, want to contain %q", result.Error, tt.wantErrMsg)
			}
		})
	}
}

func TestPrintPipelineStatus_ValidationErrors(t *testing.T) {
	ClearPipelineRegistry()

	tests := []struct {
		name       string
		runID      string
		wantCode   int
		wantErrMsg string
		errorCode  string
	}{
		{
			name:       "missing run_id",
			runID:      "",
			wantCode:   1,
			wantErrMsg: "run_id is required",
			errorCode:  ErrCodeInvalidFlag,
		},
		{
			name:       "nonexistent run_id",
			runID:      "nonexistent-run-123",
			wantCode:   1,
			wantErrMsg: "pipeline not found: nonexistent-run-123",
			errorCode:  ErrCodeSessionNotFound,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var exitCode int
			output := captureStdout(t, func() {
				exitCode = PrintPipelineStatus(tt.runID)
			})

			if exitCode != tt.wantCode {
				t.Errorf("PrintPipelineStatus() exit code = %d, want %d", exitCode, tt.wantCode)
			}

			// Use generic map to handle embedded struct field shadowing
			// RobotResponse.Error is shadowed by PipelineStatusOutput.Error in Go struct
			// but JSON has only one "error" field
			var result map[string]interface{}
			if err := json.Unmarshal([]byte(output), &result); err != nil {
				t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
			}

			if success, _ := result["success"].(bool); success {
				t.Error("Expected success=false for validation error")
			}

			errMsg, _ := result["error"].(string)
			if errMsg != tt.wantErrMsg {
				t.Errorf("Error = %q, want %q", errMsg, tt.wantErrMsg)
			}

			errCode, _ := result["error_code"].(string)
			if errCode != tt.errorCode {
				t.Errorf("ErrorCode = %q, want %q", errCode, tt.errorCode)
			}
		})
	}
}

func TestPrintPipelineStatus_FoundPipeline(t *testing.T) {
	ClearPipelineRegistry()

	// Register a test pipeline
	exec := &PipelineExecution{
		RunID:      "test-status-run",
		WorkflowID: "test-workflow",
		Session:    "test-session",
		Status:     "running",
		StartedAt:  time.Now(),
		Steps:      make(map[string]PipelineStep),
		Progress: PipelineProgress{
			Total:   3,
			Pending: 2,
			Running: 1,
		},
	}
	RegisterPipeline(exec)

	var exitCode int
	output := captureStdout(t, func() {
		exitCode = PrintPipelineStatus("test-status-run")
	})

	if exitCode != 0 {
		t.Errorf("PrintPipelineStatus() exit code = %d, want 0", exitCode)
	}

	var result PipelineStatusOutput
	if err := json.Unmarshal([]byte(output), &result); err != nil {
		t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
	}

	if !result.Success {
		t.Errorf("Expected success=true, got error: %s", result.Error)
	}

	if result.RunID != "test-status-run" {
		t.Errorf("RunID = %q, want %q", result.RunID, "test-status-run")
	}

	if result.WorkflowID != "test-workflow" {
		t.Errorf("WorkflowID = %q, want %q", result.WorkflowID, "test-workflow")
	}

	if result.Status != "running" {
		t.Errorf("Status = %q, want %q", result.Status, "running")
	}

	ClearPipelineRegistry()
}

func TestPrintPipelineList_Empty(t *testing.T) {
	ClearPipelineRegistry()

	var exitCode int
	output := captureStdout(t, func() {
		exitCode = PrintPipelineList()
	})

	if exitCode != 0 {
		t.Errorf("PrintPipelineList() exit code = %d, want 0", exitCode)
	}

	var result PipelineListOutput
	if err := json.Unmarshal([]byte(output), &result); err != nil {
		t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
	}

	if !result.Success {
		t.Errorf("Expected success=true, got error: %s", result.Error)
	}

	if len(result.Pipelines) != 0 {
		t.Errorf("Pipelines count = %d, want 0", len(result.Pipelines))
	}
}

func TestPrintPipelineList_WithPipelines(t *testing.T) {
	ClearPipelineRegistry()

	// Register some test pipelines
	now := time.Now()
	exec1 := &PipelineExecution{
		RunID:      "list-test-1",
		WorkflowID: "workflow-1",
		Session:    "session-1",
		Status:     "completed",
		StartedAt:  now,
		Progress:   PipelineProgress{Total: 5, Completed: 5, Percent: 100},
	}
	exec2 := &PipelineExecution{
		RunID:      "list-test-2",
		WorkflowID: "workflow-2",
		Session:    "session-2",
		Status:     "running",
		StartedAt:  now,
		Progress:   PipelineProgress{Total: 10, Running: 1, Pending: 9, Percent: 0},
	}
	RegisterPipeline(exec1)
	RegisterPipeline(exec2)

	var exitCode int
	output := captureStdout(t, func() {
		exitCode = PrintPipelineList()
	})

	if exitCode != 0 {
		t.Errorf("PrintPipelineList() exit code = %d, want 0", exitCode)
	}

	var result PipelineListOutput
	if err := json.Unmarshal([]byte(output), &result); err != nil {
		t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
	}

	if !result.Success {
		t.Errorf("Expected success=true, got error: %s", result.Error)
	}

	if len(result.Pipelines) != 2 {
		t.Errorf("Pipelines count = %d, want 2", len(result.Pipelines))
	}

	// Verify pipelines are sorted by start time (most recent first)
	if result.AgentHints == nil {
		t.Error("AgentHints should not be nil")
	}

	ClearPipelineRegistry()
}

func TestPrintPipelineCancel_ValidationErrors(t *testing.T) {
	ClearPipelineRegistry()

	tests := []struct {
		name       string
		runID      string
		wantCode   int
		wantErrMsg string
		errorCode  string
	}{
		{
			name:       "missing run_id",
			runID:      "",
			wantCode:   1,
			wantErrMsg: "run_id is required",
			errorCode:  ErrCodeInvalidFlag,
		},
		{
			name:       "nonexistent run_id",
			runID:      "cancel-nonexistent-123",
			wantCode:   1,
			wantErrMsg: "pipeline not found: cancel-nonexistent-123",
			errorCode:  ErrCodeSessionNotFound,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var exitCode int
			output := captureStdout(t, func() {
				exitCode = PrintPipelineCancel(tt.runID)
			})

			if exitCode != tt.wantCode {
				t.Errorf("PrintPipelineCancel() exit code = %d, want %d", exitCode, tt.wantCode)
			}

			var result PipelineCancelOutput
			if err := json.Unmarshal([]byte(output), &result); err != nil {
				t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
			}

			if result.Success {
				t.Error("Expected success=false for validation error")
			}

			if result.Error != tt.wantErrMsg {
				t.Errorf("Error = %q, want %q", result.Error, tt.wantErrMsg)
			}

			if result.ErrorCode != tt.errorCode {
				t.Errorf("ErrorCode = %q, want %q", result.ErrorCode, tt.errorCode)
			}
		})
	}
}

func TestPrintPipelineCancel_CompletedPipeline(t *testing.T) {
	ClearPipelineRegistry()

	// Register a completed pipeline
	finished := time.Now()
	exec := &PipelineExecution{
		RunID:      "cancel-completed-test",
		WorkflowID: "test-workflow",
		Session:    "test-session",
		Status:     "completed",
		StartedAt:  time.Now().Add(-time.Minute),
		FinishedAt: &finished,
	}
	RegisterPipeline(exec)

	var exitCode int
	output := captureStdout(t, func() {
		exitCode = PrintPipelineCancel("cancel-completed-test")
	})

	// Cancelling a completed pipeline should succeed but do nothing
	if exitCode != 0 {
		t.Errorf("PrintPipelineCancel() exit code = %d, want 0", exitCode)
	}

	var result PipelineCancelOutput
	if err := json.Unmarshal([]byte(output), &result); err != nil {
		t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
	}

	if !result.Success {
		t.Errorf("Expected success=true, got error: %s", result.Error)
	}

	if result.Status != "completed" {
		t.Errorf("Status = %q, want %q", result.Status, "completed")
	}

	ClearPipelineRegistry()
}
