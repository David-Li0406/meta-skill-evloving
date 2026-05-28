package checkpoint

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestRestoreOptions_Defaults(t *testing.T) {
	opts := RestoreOptions{}

	// All options should be false by default
	if opts.Force {
		t.Error("Force should be false by default")
	}
	if opts.SkipGitCheck {
		t.Error("SkipGitCheck should be false by default")
	}
	if opts.InjectContext {
		t.Error("InjectContext should be false by default")
	}
	if opts.DryRun {
		t.Error("DryRun should be false by default")
	}
	if opts.CustomDirectory != "" {
		t.Error("CustomDirectory should be empty by default")
	}
}

func TestRestoreResult_Fields(t *testing.T) {
	result := &RestoreResult{
		SessionName:     "test-session",
		PanesRestored:   3,
		ContextInjected: true,
		Warnings:        []string{"warning1", "warning2"},
		DryRun:          false,
	}

	if result.SessionName != "test-session" {
		t.Errorf("SessionName = %q, want %q", result.SessionName, "test-session")
	}
	if result.PanesRestored != 3 {
		t.Errorf("PanesRestored = %d, want %d", result.PanesRestored, 3)
	}
	if !result.ContextInjected {
		t.Error("ContextInjected should be true")
	}
	if len(result.Warnings) != 2 {
		t.Errorf("len(Warnings) = %d, want %d", len(result.Warnings), 2)
	}
}

func TestNewRestorer(t *testing.T) {
	r := NewRestorer()
	if r == nil {
		t.Fatal("NewRestorer() returned nil")
	}
	if r.storage == nil {
		t.Error("Restorer.storage should not be nil")
	}
}

func TestNewRestorerWithStorage(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	storage := NewStorageWithDir(tmpDir)
	r := NewRestorerWithStorage(storage)

	if r.storage != storage {
		t.Error("Restorer should use provided storage")
	}
}

func TestRestorer_RestoreFromCheckpoint_DirectoryNotFound(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	cp := &Checkpoint{
		ID:          "test-checkpoint",
		SessionName: "test-session",
		WorkingDir:  "/nonexistent/path/that/does/not/exist",
		Session: SessionState{
			Panes: []PaneState{{Index: 0, ID: "%0"}},
		},
	}

	_, err = r.RestoreFromCheckpoint(cp, RestoreOptions{})
	if err == nil {
		t.Error("RestoreFromCheckpoint should fail for nonexistent directory")
	}
}

func TestRestorer_RestoreFromCheckpoint_NoPanes(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	cp := &Checkpoint{
		ID:          "test-checkpoint",
		SessionName: "test-session",
		WorkingDir:  tmpDir,
		Session: SessionState{
			Panes: []PaneState{}, // Empty panes
		},
	}

	_, err = r.RestoreFromCheckpoint(cp, RestoreOptions{})
	if err != ErrNoAgentsToRestore {
		t.Errorf("Expected ErrNoAgentsToRestore, got: %v", err)
	}
}

func TestRestorer_RestoreFromCheckpoint_DryRun(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	cp := &Checkpoint{
		ID:          "test-checkpoint",
		SessionName: "test-dryrun-session",
		WorkingDir:  tmpDir,
		Session: SessionState{
			Panes: []PaneState{
				{Index: 0, ID: "%0", Title: "pane1"},
				{Index: 1, ID: "%1", Title: "pane2"},
			},
		},
	}

	result, err := r.RestoreFromCheckpoint(cp, RestoreOptions{DryRun: true})
	if err != nil {
		t.Fatalf("RestoreFromCheckpoint(DryRun) failed: %v", err)
	}

	if !result.DryRun {
		t.Error("Result.DryRun should be true")
	}
	if result.PanesRestored != 2 {
		t.Errorf("PanesRestored = %d, want 2", result.PanesRestored)
	}
}

func TestRestorer_RestoreFromCheckpoint_DryRun_CustomDirectory(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	cp := &Checkpoint{
		ID:          "test-checkpoint",
		SessionName: "test-session",
		WorkingDir:  "/original/nonexistent/path",
		Session: SessionState{
			Panes: []PaneState{{Index: 0, ID: "%0"}},
		},
	}

	// Should succeed with custom directory override
	result, err := r.RestoreFromCheckpoint(cp, RestoreOptions{
		DryRun:          true,
		CustomDirectory: tmpDir,
	})
	if err != nil {
		t.Fatalf("RestoreFromCheckpoint with CustomDirectory failed: %v", err)
	}

	if result.PanesRestored != 1 {
		t.Errorf("PanesRestored = %d, want 1", result.PanesRestored)
	}
}

func TestRestorer_ValidateCheckpoint_DirectoryNotFound(t *testing.T) {
	r := NewRestorer()

	cp := &Checkpoint{
		WorkingDir: "/nonexistent/path",
		Session: SessionState{
			Panes: []PaneState{{Index: 0}},
		},
	}

	issues := r.ValidateCheckpoint(cp, RestoreOptions{})

	found := false
	for _, issue := range issues {
		if containsSubstr(issue, "directory not found") {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected directory not found issue")
	}
}

func TestRestorer_ValidateCheckpoint_NoPanes(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorer()

	cp := &Checkpoint{
		WorkingDir: tmpDir,
		Session: SessionState{
			Panes: []PaneState{}, // Empty
		},
	}

	issues := r.ValidateCheckpoint(cp, RestoreOptions{})

	found := false
	for _, issue := range issues {
		if containsSubstr(issue, "no panes") {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected 'no panes' issue")
	}
}

func TestRestorer_ValidateCheckpoint_MissingScrollback(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	storage := NewStorageWithDir(tmpDir)
	r := NewRestorerWithStorage(storage)

	// Create a checkpoint directory without scrollback files
	cp := &Checkpoint{
		ID:          "test-checkpoint",
		SessionName: "test-session",
		WorkingDir:  tmpDir,
		Session: SessionState{
			Panes: []PaneState{
				{
					Index:          0,
					ID:             "%0",
					ScrollbackFile: "panes/pane_0.txt", // File doesn't exist
				},
			},
		},
	}

	// Create the checkpoint directory
	cpDir := storage.CheckpointDir(cp.SessionName, cp.ID)
	if err := os.MkdirAll(cpDir, 0755); err != nil {
		t.Fatalf("Failed to create checkpoint dir: %v", err)
	}

	issues := r.ValidateCheckpoint(cp, RestoreOptions{InjectContext: true})

	found := false
	for _, issue := range issues {
		if containsSubstr(issue, "scrollback file missing") {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected 'scrollback file missing' issue, got: %v", issues)
	}
}

func TestTruncateToLines(t *testing.T) {
	tests := []struct {
		content  string
		maxLines int
		want     string
	}{
		{"", 5, ""},
		{"one", 5, "one"},
		{"one\ntwo\nthree", 5, "one\ntwo\nthree"},
		{"one\ntwo\nthree", 2, "two\nthree"},
		{"one\ntwo\nthree\nfour\nfive", 3, "three\nfour\nfive"},
		{"one\ntwo\nthree", 1, "three"},
	}

	for _, tt := range tests {
		got := truncateToLines(tt.content, tt.maxLines)
		if got != tt.want {
			t.Errorf("truncateToLines(%q, %d) = %q, want %q",
				tt.content, tt.maxLines, got, tt.want)
		}
	}
}

func TestSplitLines(t *testing.T) {
	tests := []struct {
		input string
		want  int
	}{
		{"", 0},
		{"one", 1},
		{"one\n", 1}, // trailing newline doesn't add extra line
		{"one\ntwo", 2},
		{"one\ntwo\n", 2}, // trailing newline doesn't add extra line
		{"one\ntwo\nthree", 3},
	}

	for _, tt := range tests {
		got := splitLines(tt.input)
		if len(got) != tt.want {
			t.Errorf("len(splitLines(%q)) = %d, want %d", tt.input, len(got), tt.want)
		}
	}
}

func TestJoinLines(t *testing.T) {
	tests := []struct {
		lines []string
		want  string
	}{
		{nil, ""},
		{[]string{}, ""},
		{[]string{"one"}, "one"},
		{[]string{"one", "two"}, "one\ntwo"},
		{[]string{"one", "two", "three"}, "one\ntwo\nthree"},
	}

	for _, tt := range tests {
		got := joinLines(tt.lines)
		if got != tt.want {
			t.Errorf("joinLines(%v) = %q, want %q", tt.lines, got, tt.want)
		}
	}
}

func TestTrimSpace(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{"", ""},
		{"hello", "hello"},
		{"  hello", "hello"},
		{"hello  ", "hello"},
		{"  hello  ", "hello"},
		{"\n\thello\n\t", "hello"},
		{"  \n\t  ", ""},
	}

	for _, tt := range tests {
		got := trimSpace(tt.input)
		if got != tt.want {
			t.Errorf("trimSpace(%q) = %q, want %q", tt.input, got, tt.want)
		}
	}
}

func TestFormatDuration(t *testing.T) {
	tests := []struct {
		d    time.Duration
		want string
	}{
		{30 * time.Second, "just now"},
		{5 * time.Minute, "5m"},
		{90 * time.Minute, "1h"},
		{3 * time.Hour, "3h"},
		{36 * time.Hour, "1d"},
		{72 * time.Hour, "3d"},
	}

	for _, tt := range tests {
		got := formatDuration(tt.d)
		if got != tt.want {
			t.Errorf("formatDuration(%v) = %q, want %q", tt.d, got, tt.want)
		}
	}
}

func TestFormatContextInjection(t *testing.T) {
	content := "Hello\nWorld"
	checkpointTime := time.Now().Add(-2 * time.Hour)

	result := formatContextInjection(content, checkpointTime)

	if !containsSubstr(result, "Context from checkpoint") {
		t.Error("Expected header with 'Context from checkpoint'")
	}
	if !containsSubstr(result, "Hello") {
		t.Error("Expected content to be included")
	}
	if !containsSubstr(result, "World") {
		t.Error("Expected content to be included")
	}
}

func TestRestorer_Restore_CheckpointNotFound(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	_, err = r.Restore("nonexistent-session", "nonexistent-checkpoint", RestoreOptions{})
	if err == nil {
		t.Error("Restore should fail for nonexistent checkpoint")
	}
}

func TestRestorer_RestoreLatest_NoCheckpoints(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-restore-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	r := NewRestorerWithStorage(NewStorageWithDir(tmpDir))

	_, err = r.RestoreLatest("nonexistent-session", RestoreOptions{})
	if err == nil {
		t.Error("RestoreLatest should fail when no checkpoints exist")
	}
}

// containsSubstr checks if s contains substr (case-insensitive).
func containsSubstr(s, substr string) bool {
	return filepath.Base(s) == substr || len(s) >= len(substr) && findSubstr(s, substr)
}

func findSubstr(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if matchIgnoreCase(s[i:i+len(substr)], substr) {
			return true
		}
	}
	return false
}

func matchIgnoreCase(a, b string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := 0; i < len(a); i++ {
		ca, cb := a[i], b[i]
		if ca >= 'A' && ca <= 'Z' {
			ca += 'a' - 'A'
		}
		if cb >= 'A' && cb <= 'Z' {
			cb += 'a' - 'A'
		}
		if ca != cb {
			return false
		}
	}
	return true
}
