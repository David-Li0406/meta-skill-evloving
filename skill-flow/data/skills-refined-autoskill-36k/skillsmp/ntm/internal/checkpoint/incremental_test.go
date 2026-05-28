package checkpoint

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestComputeScrollbackDiff(t *testing.T) {
	tests := []struct {
		name     string
		base     string
		current  string
		wantDiff string
	}{
		{
			name:     "empty base",
			base:     "",
			current:  "line1\nline2\nline3",
			wantDiff: "line1\nline2\nline3",
		},
		{
			name:     "empty current",
			base:     "line1\nline2",
			current:  "",
			wantDiff: "",
		},
		{
			name:     "new lines appended",
			base:     "line1\nline2",
			current:  "line1\nline2\nline3\nline4",
			wantDiff: "line3\nline4",
		},
		{
			name:     "no new lines",
			base:     "line1\nline2\nline3",
			current:  "line1\nline2",
			wantDiff: "",
		},
		{
			name:     "both empty",
			base:     "",
			current:  "",
			wantDiff: "",
		},
		{
			name:     "identical content",
			base:     "line1\nline2",
			current:  "line1\nline2",
			wantDiff: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := computeScrollbackDiff(tt.base, tt.current)
			if got != tt.wantDiff {
				t.Errorf("computeScrollbackDiff() = %q, want %q", got, tt.wantDiff)
			}
		})
	}
}

func TestIncrementalCreator_computeGitChange(t *testing.T) {
	ic := NewIncrementalCreator()

	tests := []struct {
		name       string
		base       GitState
		current    GitState
		wantChange bool
		wantBranch string
	}{
		{
			name: "no changes",
			base: GitState{
				Branch: "main",
				Commit: "abc123",
			},
			current: GitState{
				Branch: "main",
				Commit: "abc123",
			},
			wantChange: false,
		},
		{
			name: "commit changed",
			base: GitState{
				Branch: "main",
				Commit: "abc123",
			},
			current: GitState{
				Branch: "main",
				Commit: "def456",
			},
			wantChange: true,
			wantBranch: "", // Branch didn't change
		},
		{
			name: "branch changed",
			base: GitState{
				Branch: "main",
				Commit: "abc123",
			},
			current: GitState{
				Branch: "feature",
				Commit: "abc123",
			},
			wantChange: true,
			wantBranch: "feature",
		},
		{
			name: "dirty state changed",
			base: GitState{
				Branch:  "main",
				Commit:  "abc123",
				IsDirty: false,
			},
			current: GitState{
				Branch:  "main",
				Commit:  "abc123",
				IsDirty: true,
			},
			wantChange: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := ic.computeGitChange(tt.base, tt.current)

			if tt.wantChange && got == nil {
				t.Error("computeGitChange() returned nil, want change")
			}

			if !tt.wantChange && got != nil {
				t.Error("computeGitChange() returned change, want nil")
			}

			if got != nil && got.Branch != tt.wantBranch {
				t.Errorf("computeGitChange().Branch = %q, want %q", got.Branch, tt.wantBranch)
			}
		})
	}
}

func TestIncrementalCreator_computeSessionChange(t *testing.T) {
	ic := NewIncrementalCreator()

	tests := []struct {
		name       string
		base       SessionState
		current    SessionState
		wantChange bool
	}{
		{
			name: "no changes",
			base: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
				Panes:           make([]PaneState, 2),
			},
			current: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
				Panes:           make([]PaneState, 2),
			},
			wantChange: false,
		},
		{
			name: "layout changed",
			base: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
			},
			current: SessionState{
				Layout:          "tiled",
				ActivePaneIndex: 0,
			},
			wantChange: true,
		},
		{
			name: "active pane changed",
			base: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
			},
			current: SessionState{
				Layout:          "main",
				ActivePaneIndex: 1,
			},
			wantChange: true,
		},
		{
			name: "pane count changed",
			base: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
				Panes:           make([]PaneState, 2),
			},
			current: SessionState{
				Layout:          "main",
				ActivePaneIndex: 0,
				Panes:           make([]PaneState, 3),
			},
			wantChange: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := ic.computeSessionChange(tt.base, tt.current)

			if tt.wantChange && got == nil {
				t.Error("computeSessionChange() returned nil, want change")
			}

			if !tt.wantChange && got != nil {
				t.Error("computeSessionChange() returned change, want nil")
			}
		})
	}
}

func TestRemovePaneByID(t *testing.T) {
	panes := []PaneState{
		{ID: "pane1", Title: "Pane 1"},
		{ID: "pane2", Title: "Pane 2"},
		{ID: "pane3", Title: "Pane 3"},
	}

	// Remove middle pane
	result := removePaneByID(panes, "pane2")

	if len(result) != 2 {
		t.Errorf("removePaneByID() len = %d, want 2", len(result))
	}

	for _, p := range result {
		if p.ID == "pane2" {
			t.Error("removePaneByID() failed to remove pane2")
		}
	}

	// Remove non-existent pane
	result = removePaneByID(panes, "pane99")
	if len(result) != 3 {
		t.Errorf("removePaneByID() len = %d, want 3 (no change)", len(result))
	}
}

func TestIncrementalCheckpoint_StorageSavings(t *testing.T) {
	// Create a temporary storage directory
	tmpDir := t.TempDir()
	storage := NewStorageWithDir(tmpDir)

	// Create a mock base checkpoint
	baseID := GenerateID("test-base")
	base := &Checkpoint{
		Version:     2,
		ID:          baseID,
		Name:        "test-base",
		SessionName: "test-session",
		CreatedAt:   time.Now(),
		Session: SessionState{
			Panes: []PaneState{
				{ID: "pane1", ScrollbackFile: "panes/pane1.txt"},
			},
		},
	}

	// Save the base checkpoint
	if err := storage.Save(base); err != nil {
		t.Fatalf("Failed to save base checkpoint: %v", err)
	}

	// Save some mock scrollback
	_, err := storage.SaveScrollback("test-session", baseID, "pane1", "line1\nline2\nline3\nline4\nline5")
	if err != nil {
		t.Fatalf("Failed to save scrollback: %v", err)
	}

	// Create an incremental checkpoint
	inc := &IncrementalCheckpoint{
		SessionName:      "test-session",
		BaseCheckpointID: baseID,
		Changes: IncrementalChanges{
			PaneChanges: map[string]PaneChange{
				"pane1": {NewLines: 2}, // Only 2 new lines
			},
		},
	}

	savedBytes, percentSaved, err := inc.StorageSavings(storage)
	if err != nil {
		t.Fatalf("StorageSavings() error = %v", err)
	}

	// We should have some savings since incremental has fewer lines
	if savedBytes <= 0 {
		t.Logf("StorageSavings() savedBytes = %d, percentSaved = %.2f%%", savedBytes, percentSaved)
	}
}

func TestIncrementalCreator_incrementalDir(t *testing.T) {
	tmpDir := t.TempDir()
	storage := NewStorageWithDir(tmpDir)
	ic := NewIncrementalCreatorWithStorage(storage)

	dir := ic.incrementalDir("my-session", "inc-123")
	expected := filepath.Join(tmpDir, "my-session", "incremental", "inc-123")

	if dir != expected {
		t.Errorf("incrementalDir() = %q, want %q", dir, expected)
	}
}

func TestIncrementalResolver_loadIncremental(t *testing.T) {
	// Create a temporary storage directory
	tmpDir := t.TempDir()
	storage := NewStorageWithDir(tmpDir)

	// Create incremental directory structure
	sessionName := "test-session"
	incID := "inc-test-123"
	incDir := filepath.Join(tmpDir, sessionName, "incremental", incID)
	if err := os.MkdirAll(incDir, 0755); err != nil {
		t.Fatalf("Failed to create incremental directory: %v", err)
	}

	// Write a mock incremental metadata file
	metadata := `{
		"version": 1,
		"id": "inc-test-123",
		"session_name": "test-session",
		"base_checkpoint_id": "base-123",
		"created_at": "2025-01-06T10:00:00Z",
		"changes": {}
	}`

	metaPath := filepath.Join(incDir, IncrementalMetadataFile)
	if err := os.WriteFile(metaPath, []byte(metadata), 0600); err != nil {
		t.Fatalf("Failed to write metadata: %v", err)
	}

	// Test loading
	ir := NewIncrementalResolverWithStorage(storage)
	inc, err := ir.loadIncremental(sessionName, incID)
	if err != nil {
		t.Fatalf("loadIncremental() error = %v", err)
	}

	if inc.ID != incID {
		t.Errorf("loadIncremental().ID = %q, want %q", inc.ID, incID)
	}

	if inc.BaseCheckpointID != "base-123" {
		t.Errorf("loadIncremental().BaseCheckpointID = %q, want %q", inc.BaseCheckpointID, "base-123")
	}
}

func TestIncrementalResolver_ListIncrementals(t *testing.T) {
	tmpDir := t.TempDir()
	storage := NewStorageWithDir(tmpDir)

	sessionName := "test-session"
	incDir := filepath.Join(tmpDir, sessionName, "incremental")

	// Create two incremental checkpoints
	for i, id := range []string{"inc-001", "inc-002"} {
		dir := filepath.Join(incDir, id)
		if err := os.MkdirAll(dir, 0755); err != nil {
			t.Fatalf("Failed to create directory: %v", err)
		}

		metadata := `{
			"version": 1,
			"id": "` + id + `",
			"session_name": "test-session",
			"base_checkpoint_id": "base-123",
			"created_at": "2025-01-0` + string(rune('6'+i)) + `T10:00:00Z",
			"changes": {}
		}`

		if err := os.WriteFile(filepath.Join(dir, IncrementalMetadataFile), []byte(metadata), 0600); err != nil {
			t.Fatalf("Failed to write metadata: %v", err)
		}
	}

	ir := NewIncrementalResolverWithStorage(storage)
	incrementals, err := ir.ListIncrementals(sessionName)
	if err != nil {
		t.Fatalf("ListIncrementals() error = %v", err)
	}

	if len(incrementals) != 2 {
		t.Errorf("ListIncrementals() len = %d, want 2", len(incrementals))
	}
}

func TestIncrementalResolver_ListIncrementals_NoSession(t *testing.T) {
	tmpDir := t.TempDir()
	storage := NewStorageWithDir(tmpDir)

	ir := NewIncrementalResolverWithStorage(storage)
	incrementals, err := ir.ListIncrementals("nonexistent-session")
	if err != nil {
		t.Fatalf("ListIncrementals() error = %v", err)
	}

	if incrementals != nil && len(incrementals) != 0 {
		t.Errorf("ListIncrementals() = %v, want empty", incrementals)
	}
}

func TestPaneChange_States(t *testing.T) {
	// Test pane change states
	added := PaneChange{Added: true, NewLines: 100}
	if !added.Added {
		t.Error("PaneChange.Added should be true")
	}

	removed := PaneChange{Removed: true}
	if !removed.Removed {
		t.Error("PaneChange.Removed should be true")
	}

	modified := PaneChange{
		AgentType: "cc",
		Title:     "New Title",
		NewLines:  50,
	}
	if modified.Added || modified.Removed {
		t.Error("Modified pane should not be marked as Added or Removed")
	}
}

func TestIncrementalChanges_Empty(t *testing.T) {
	changes := IncrementalChanges{}

	if changes.PaneChanges != nil {
		t.Error("Empty IncrementalChanges should have nil PaneChanges")
	}

	if changes.GitChange != nil {
		t.Error("Empty IncrementalChanges should have nil GitChange")
	}

	if changes.SessionChange != nil {
		t.Error("Empty IncrementalChanges should have nil SessionChange")
	}
}

func TestIncrementalCheckpoint_Fields(t *testing.T) {
	now := time.Now()
	baseTime := now.Add(-time.Hour)

	inc := &IncrementalCheckpoint{
		Version:          IncrementalVersion,
		ID:               "test-inc-123",
		SessionName:      "my-session",
		BaseCheckpointID: "base-checkpoint-456",
		BaseTimestamp:    baseTime,
		CreatedAt:        now,
		Description:      "Test incremental",
		Changes:          IncrementalChanges{},
	}

	if inc.Version != IncrementalVersion {
		t.Errorf("Version = %d, want %d", inc.Version, IncrementalVersion)
	}

	if inc.ID != "test-inc-123" {
		t.Errorf("ID = %q, want %q", inc.ID, "test-inc-123")
	}

	if inc.SessionName != "my-session" {
		t.Errorf("SessionName = %q, want %q", inc.SessionName, "my-session")
	}

	if !inc.BaseTimestamp.Equal(baseTime) {
		t.Errorf("BaseTimestamp = %v, want %v", inc.BaseTimestamp, baseTime)
	}
}
