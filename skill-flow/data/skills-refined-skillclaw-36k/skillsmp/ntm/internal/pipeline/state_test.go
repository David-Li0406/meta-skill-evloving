package pipeline

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestSaveState(t *testing.T) {
	// Create temp directory
	tmpDir := t.TempDir()

	state := &ExecutionState{
		RunID:      "test-run-123",
		WorkflowID: "my-workflow",
		Status:     StatusRunning,
		StartedAt:  time.Now(),
		Variables: map[string]interface{}{
			"name":  "Alice",
			"count": 42,
		},
		Steps: map[string]StepResult{
			"step1": {
				Status: StatusCompleted,
				Output: "step1 output",
			},
		},
	}

	err := SaveState(tmpDir, state)
	if err != nil {
		t.Fatalf("SaveState() error = %v", err)
	}

	// Verify file exists
	path := filepath.Join(tmpDir, ".ntm", "pipelines", "test-run-123.json")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Errorf("State file not created at %s", path)
	}

	// Verify file contents are valid JSON
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("Failed to read state file: %v", err)
	}

	var loaded ExecutionState
	if err := json.Unmarshal(data, &loaded); err != nil {
		t.Fatalf("State file is not valid JSON: %v", err)
	}

	if loaded.RunID != "test-run-123" {
		t.Errorf("RunID = %q, want %q", loaded.RunID, "test-run-123")
	}
	if loaded.WorkflowID != "my-workflow" {
		t.Errorf("WorkflowID = %q, want %q", loaded.WorkflowID, "my-workflow")
	}
	if loaded.Status != StatusRunning {
		t.Errorf("Status = %v, want %v", loaded.Status, StatusRunning)
	}
}

func TestSaveState_NilState(t *testing.T) {
	tmpDir := t.TempDir()
	err := SaveState(tmpDir, nil)
	if err == nil {
		t.Error("SaveState(nil) should return error")
	}
}

func TestSaveState_EmptyRunID(t *testing.T) {
	tmpDir := t.TempDir()
	state := &ExecutionState{
		RunID: "", // Empty
	}
	err := SaveState(tmpDir, state)
	if err == nil {
		t.Error("SaveState with empty RunID should return error")
	}
}

func TestSaveState_Overwrite(t *testing.T) {
	tmpDir := t.TempDir()

	// Save initial state
	state1 := &ExecutionState{
		RunID:  "run-1",
		Status: StatusRunning,
	}
	if err := SaveState(tmpDir, state1); err != nil {
		t.Fatalf("First SaveState() error = %v", err)
	}

	// Save updated state with same run ID
	state2 := &ExecutionState{
		RunID:  "run-1",
		Status: StatusCompleted,
	}
	if err := SaveState(tmpDir, state2); err != nil {
		t.Fatalf("Second SaveState() error = %v", err)
	}

	// Load and verify it was overwritten
	loaded, err := LoadState(tmpDir, "run-1")
	if err != nil {
		t.Fatalf("LoadState() error = %v", err)
	}
	if loaded.Status != StatusCompleted {
		t.Errorf("Status = %v, want %v (state should be overwritten)", loaded.Status, StatusCompleted)
	}
}

func TestLoadState(t *testing.T) {
	tmpDir := t.TempDir()

	// Save a state first
	state := &ExecutionState{
		RunID:       "load-test-123",
		WorkflowID:  "test-workflow",
		Status:      StatusCompleted,
		CurrentStep: "step3",
		Variables: map[string]interface{}{
			"result": "success",
		},
		Steps: map[string]StepResult{
			"step1": {Status: StatusCompleted, Output: "out1"},
			"step2": {Status: StatusCompleted, Output: "out2"},
			"step3": {Status: StatusCompleted, Output: "out3"},
		},
	}
	if err := SaveState(tmpDir, state); err != nil {
		t.Fatalf("SaveState() error = %v", err)
	}

	// Load the state
	loaded, err := LoadState(tmpDir, "load-test-123")
	if err != nil {
		t.Fatalf("LoadState() error = %v", err)
	}

	if loaded.RunID != "load-test-123" {
		t.Errorf("RunID = %q, want %q", loaded.RunID, "load-test-123")
	}
	if loaded.WorkflowID != "test-workflow" {
		t.Errorf("WorkflowID = %q, want %q", loaded.WorkflowID, "test-workflow")
	}
	if loaded.Status != StatusCompleted {
		t.Errorf("Status = %v, want %v", loaded.Status, StatusCompleted)
	}
	if loaded.CurrentStep != "step3" {
		t.Errorf("CurrentStep = %q, want %q", loaded.CurrentStep, "step3")
	}
	if len(loaded.Steps) != 3 {
		t.Errorf("len(Steps) = %d, want 3", len(loaded.Steps))
	}
	if loaded.Variables["result"] != "success" {
		t.Errorf("Variables[result] = %v, want 'success'", loaded.Variables["result"])
	}
}

func TestLoadState_EmptyRunID(t *testing.T) {
	tmpDir := t.TempDir()
	_, err := LoadState(tmpDir, "")
	if err == nil {
		t.Error("LoadState with empty runID should return error")
	}
}

func TestLoadState_NotFound(t *testing.T) {
	tmpDir := t.TempDir()
	_, err := LoadState(tmpDir, "nonexistent-run")
	if err == nil {
		t.Error("LoadState for nonexistent run should return error")
	}
}

func TestLoadState_InvalidJSON(t *testing.T) {
	tmpDir := t.TempDir()

	// Create directory structure
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Write invalid JSON
	path := filepath.Join(dir, "invalid.json")
	if err := os.WriteFile(path, []byte("not valid json {"), 0644); err != nil {
		t.Fatalf("Failed to write file: %v", err)
	}

	_, err := LoadState(tmpDir, "invalid")
	if err == nil {
		t.Error("LoadState should return error for invalid JSON")
	}
}

func TestLoadState_EmptyRunIDInFile(t *testing.T) {
	tmpDir := t.TempDir()

	// Create directory structure
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Write JSON with empty RunID - should be filled from filename
	path := filepath.Join(dir, "from-filename.json")
	data := `{"run_id":"","status":"running"}`
	if err := os.WriteFile(path, []byte(data), 0644); err != nil {
		t.Fatalf("Failed to write file: %v", err)
	}

	loaded, err := LoadState(tmpDir, "from-filename")
	if err != nil {
		t.Fatalf("LoadState() error = %v", err)
	}
	if loaded.RunID != "from-filename" {
		t.Errorf("RunID = %q, want 'from-filename' (should be filled from filename)", loaded.RunID)
	}
}

func TestCleanupStates(t *testing.T) {
	tmpDir := t.TempDir()

	// Create some state files with different ages
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Create files
	oldFile := filepath.Join(dir, "old-run.json")
	newFile := filepath.Join(dir, "new-run.json")

	if err := os.WriteFile(oldFile, []byte(`{"run_id":"old-run"}`), 0644); err != nil {
		t.Fatalf("Failed to write old file: %v", err)
	}
	if err := os.WriteFile(newFile, []byte(`{"run_id":"new-run"}`), 0644); err != nil {
		t.Fatalf("Failed to write new file: %v", err)
	}

	// Make old file look old
	oldTime := time.Now().Add(-48 * time.Hour)
	if err := os.Chtimes(oldFile, oldTime, oldTime); err != nil {
		t.Fatalf("Failed to set old file time: %v", err)
	}

	// Cleanup files older than 24 hours
	deleted, err := CleanupStates(tmpDir, 24*time.Hour)
	if err != nil {
		t.Fatalf("CleanupStates() error = %v", err)
	}

	if deleted != 1 {
		t.Errorf("deleted = %d, want 1", deleted)
	}

	// Verify old file is gone
	if _, err := os.Stat(oldFile); !os.IsNotExist(err) {
		t.Error("Old file should be deleted")
	}

	// Verify new file still exists
	if _, err := os.Stat(newFile); os.IsNotExist(err) {
		t.Error("New file should still exist")
	}
}

func TestCleanupStates_ZeroDuration(t *testing.T) {
	tmpDir := t.TempDir()
	_, err := CleanupStates(tmpDir, 0)
	if err == nil {
		t.Error("CleanupStates with zero duration should return error")
	}
}

func TestCleanupStates_NegativeDuration(t *testing.T) {
	tmpDir := t.TempDir()
	_, err := CleanupStates(tmpDir, -time.Hour)
	if err == nil {
		t.Error("CleanupStates with negative duration should return error")
	}
}

func TestCleanupStates_NonExistentDir(t *testing.T) {
	tmpDir := t.TempDir()
	// Don't create the pipelines directory

	deleted, err := CleanupStates(tmpDir, time.Hour)
	if err != nil {
		t.Errorf("CleanupStates() error = %v, want nil for nonexistent dir", err)
	}
	if deleted != 0 {
		t.Errorf("deleted = %d, want 0 for nonexistent dir", deleted)
	}
}

func TestCleanupStates_SkipsNonJSON(t *testing.T) {
	tmpDir := t.TempDir()
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Create a non-JSON file
	txtFile := filepath.Join(dir, "notes.txt")
	if err := os.WriteFile(txtFile, []byte("just notes"), 0644); err != nil {
		t.Fatalf("Failed to write txt file: %v", err)
	}

	// Make it old
	oldTime := time.Now().Add(-48 * time.Hour)
	if err := os.Chtimes(txtFile, oldTime, oldTime); err != nil {
		t.Fatalf("Failed to set time: %v", err)
	}

	deleted, err := CleanupStates(tmpDir, time.Hour)
	if err != nil {
		t.Fatalf("CleanupStates() error = %v", err)
	}
	if deleted != 0 {
		t.Errorf("deleted = %d, want 0 (should skip non-JSON)", deleted)
	}

	// Verify txt file still exists
	if _, err := os.Stat(txtFile); os.IsNotExist(err) {
		t.Error("Non-JSON file should not be deleted")
	}
}

func TestCleanupStates_SkipsDirectories(t *testing.T) {
	tmpDir := t.TempDir()
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Create a subdirectory
	subDir := filepath.Join(dir, "subdir")
	if err := os.MkdirAll(subDir, 0755); err != nil {
		t.Fatalf("Failed to create subdir: %v", err)
	}

	deleted, err := CleanupStates(tmpDir, time.Hour)
	if err != nil {
		t.Fatalf("CleanupStates() error = %v", err)
	}
	if deleted != 0 {
		t.Errorf("deleted = %d, want 0 (should skip directories)", deleted)
	}

	// Verify subdir still exists
	if _, err := os.Stat(subDir); os.IsNotExist(err) {
		t.Error("Subdirectory should not be deleted")
	}
}

func TestPipelineStateDir(t *testing.T) {
	got := pipelineStateDir("/project")
	want := filepath.Join("/project", ".ntm", "pipelines")
	if got != want {
		t.Errorf("pipelineStateDir() = %q, want %q", got, want)
	}
}

func TestPipelineStatePath(t *testing.T) {
	got := pipelineStatePath("/project", "run-123")
	want := filepath.Join("/project", ".ntm", "pipelines", "run-123.json")
	if got != want {
		t.Errorf("pipelineStatePath() = %q, want %q", got, want)
	}
}

func TestSaveAndLoadState_ComplexState(t *testing.T) {
	tmpDir := t.TempDir()

	// Create a complex state with all fields populated
	now := time.Now().Truncate(time.Second) // Truncate for comparison
	state := &ExecutionState{
		RunID:        "complex-run",
		WorkflowID:   "complex-workflow",
		Status:       StatusFailed,
		CurrentStep:  "step2",
		StartedAt:    now,
		UpdatedAt:    now.Add(time.Minute),
		FinishedAt:   now.Add(2 * time.Minute),
		Session:      "my-session",
		WorkflowFile: "/path/to/workflow.yaml",
		Variables: map[string]interface{}{
			"string_var": "hello",
			"int_var":    float64(42), // JSON unmarshals numbers as float64
			"bool_var":   true,
			"nested": map[string]interface{}{
				"inner": "value",
			},
		},
		Steps: map[string]StepResult{
			"step1": {
				Status:     StatusCompleted,
				Output:     "step1 output",
				StartedAt:  now,
				FinishedAt: now.Add(30 * time.Second),
				PaneUsed:   "pane-1",
			},
			"step2": {
				Status:     StatusFailed,
				Output:     "",
				Error:      &StepError{Type: "agent_error", Message: "Something went wrong"},
				StartedAt:  now.Add(30 * time.Second),
				FinishedAt: now.Add(40 * time.Second),
				Attempts:   3,
			},
		},
		Errors: []ExecutionError{
			{Type: "step_error", Message: "Error in step2", Fatal: false},
			{Type: "retry", Message: "Retry failed", Fatal: true},
		},
	}

	if err := SaveState(tmpDir, state); err != nil {
		t.Fatalf("SaveState() error = %v", err)
	}

	loaded, err := LoadState(tmpDir, "complex-run")
	if err != nil {
		t.Fatalf("LoadState() error = %v", err)
	}

	// Verify all fields
	if loaded.RunID != state.RunID {
		t.Errorf("RunID = %q, want %q", loaded.RunID, state.RunID)
	}
	if loaded.WorkflowID != state.WorkflowID {
		t.Errorf("WorkflowID = %q, want %q", loaded.WorkflowID, state.WorkflowID)
	}
	if loaded.Status != state.Status {
		t.Errorf("Status = %v, want %v", loaded.Status, state.Status)
	}
	if loaded.CurrentStep != state.CurrentStep {
		t.Errorf("CurrentStep = %q, want %q", loaded.CurrentStep, state.CurrentStep)
	}
	if loaded.Session != state.Session {
		t.Errorf("Session = %q, want %q", loaded.Session, state.Session)
	}
	if loaded.WorkflowFile != state.WorkflowFile {
		t.Errorf("WorkflowFile = %q, want %q", loaded.WorkflowFile, state.WorkflowFile)
	}

	// Check variables
	if loaded.Variables["string_var"] != "hello" {
		t.Errorf("Variables[string_var] = %v, want 'hello'", loaded.Variables["string_var"])
	}
	if loaded.Variables["int_var"] != float64(42) {
		t.Errorf("Variables[int_var] = %v, want 42", loaded.Variables["int_var"])
	}
	if loaded.Variables["bool_var"] != true {
		t.Errorf("Variables[bool_var] = %v, want true", loaded.Variables["bool_var"])
	}

	// Check steps
	if len(loaded.Steps) != 2 {
		t.Errorf("len(Steps) = %d, want 2", len(loaded.Steps))
	}
	step1 := loaded.Steps["step1"]
	if step1.Status != StatusCompleted {
		t.Errorf("step1.Status = %v, want %v", step1.Status, StatusCompleted)
	}
	if step1.Output != "step1 output" {
		t.Errorf("step1.Output = %q, want 'step1 output'", step1.Output)
	}

	step2 := loaded.Steps["step2"]
	if step2.Status != StatusFailed {
		t.Errorf("step2.Status = %v, want %v", step2.Status, StatusFailed)
	}
	if step2.Error == nil || step2.Error.Message != "Something went wrong" {
		t.Errorf("step2.Error.Message = %v, want 'Something went wrong'", step2.Error)
	}
	if step2.Attempts != 3 {
		t.Errorf("step2.Attempts = %d, want 3", step2.Attempts)
	}

	// Check errors
	if len(loaded.Errors) != 2 {
		t.Errorf("len(Errors) = %d, want 2", len(loaded.Errors))
	}
}

func TestCleanupStates_MultipleFiles(t *testing.T) {
	tmpDir := t.TempDir()
	dir := filepath.Join(tmpDir, ".ntm", "pipelines")
	if err := os.MkdirAll(dir, 0755); err != nil {
		t.Fatalf("Failed to create dir: %v", err)
	}

	// Create 5 files: 3 old, 2 new
	oldTime := time.Now().Add(-72 * time.Hour)
	newTime := time.Now().Add(-1 * time.Hour)

	for i := 1; i <= 3; i++ {
		path := filepath.Join(dir, "old-"+string(rune('0'+i))+".json")
		if err := os.WriteFile(path, []byte(`{}`), 0644); err != nil {
			t.Fatalf("Failed to write: %v", err)
		}
		if err := os.Chtimes(path, oldTime, oldTime); err != nil {
			t.Fatalf("Failed to set time: %v", err)
		}
	}

	for i := 1; i <= 2; i++ {
		path := filepath.Join(dir, "new-"+string(rune('0'+i))+".json")
		if err := os.WriteFile(path, []byte(`{}`), 0644); err != nil {
			t.Fatalf("Failed to write: %v", err)
		}
		if err := os.Chtimes(path, newTime, newTime); err != nil {
			t.Fatalf("Failed to set time: %v", err)
		}
	}

	deleted, err := CleanupStates(tmpDir, 24*time.Hour)
	if err != nil {
		t.Fatalf("CleanupStates() error = %v", err)
	}
	if deleted != 3 {
		t.Errorf("deleted = %d, want 3", deleted)
	}

	// Count remaining files
	entries, _ := os.ReadDir(dir)
	if len(entries) != 2 {
		t.Errorf("remaining files = %d, want 2", len(entries))
	}
}
