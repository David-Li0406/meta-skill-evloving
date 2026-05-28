package handoff

import (
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"

	"gopkg.in/yaml.v3"
)

func TestNewWriter(t *testing.T) {
	w := NewWriter("/tmp/testproject")

	expectedBase := filepath.Join("/tmp/testproject", ".ntm", "handoffs")
	if w.baseDir != expectedBase {
		t.Errorf("expected baseDir=%s, got %s", expectedBase, w.baseDir)
	}
	if w.maxPerDir != DefaultMaxPerDir {
		t.Errorf("expected maxPerDir=%d, got %d", DefaultMaxPerDir, w.maxPerDir)
	}
}

func TestNewWriterWithOptions(t *testing.T) {
	w := NewWriterWithOptions("/tmp/testproject", 25, nil)

	if w.maxPerDir != 25 {
		t.Errorf("expected maxPerDir=25, got %d", w.maxPerDir)
	}

	// Test default maxPerDir when <= 0 is passed
	w2 := NewWriterWithOptions("/tmp/testproject", 0, nil)
	if w2.maxPerDir != DefaultMaxPerDir {
		t.Errorf("expected default maxPerDir=%d for 0, got %d", DefaultMaxPerDir, w2.maxPerDir)
	}

	w3 := NewWriterWithOptions("/tmp/testproject", -5, nil)
	if w3.maxPerDir != DefaultMaxPerDir {
		t.Errorf("expected default maxPerDir=%d for -5, got %d", DefaultMaxPerDir, w3.maxPerDir)
	}
}

func TestSanitizeDescription(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"simple", "simple"},
		{"Two Words", "two-words"},
		{"with_underscores", "with-underscores"},
		{"MixedCase", "mixedcase"},
		{"special!@#$chars", "specialchars"},
		{"multiple---hyphens", "multiple-hyphens"},
		{"-leading-trailing-", "leading-trailing"},
		{"", ""},
		{"a very long description that exceeds the maximum allowed length for filenames", "a-very-long-description-that-exceeds-the-maximum-a"},
		{"  spaces  around  ", "spaces-around"},
		{"123numbers", "123numbers"},
		{"kebab-case-already", "kebab-case-already"},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := sanitizeDescription(tt.input)
			if got != tt.expected {
				t.Errorf("sanitizeDescription(%q) = %q, want %q", tt.input, got, tt.expected)
			}
		})
	}
}

func TestTruncateLog(t *testing.T) {
	tests := []struct {
		input    string
		max      int
		expected string
	}{
		{"short", 10, "short"},
		{"exactly10!", 10, "exactly10!"},
		{"this is too long", 10, "this is..."},
		{"", 5, ""},
		{"abc", 3, "abc"},
		{"abcd", 3, ""},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := truncateLog(tt.input, tt.max)
			if got != tt.expected {
				t.Errorf("truncateLog(%q, %d) = %q, want %q", tt.input, tt.max, got, tt.expected)
			}
		})
	}
}

func TestWriterEnsureDir(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Test creating session directory
	err := w.EnsureDir("test-session")
	if err != nil {
		t.Fatalf("EnsureDir failed: %v", err)
	}

	expectedDir := filepath.Join(tmpDir, ".ntm", "handoffs", "test-session")
	info, err := os.Stat(expectedDir)
	if err != nil {
		t.Fatalf("directory not created: %v", err)
	}
	if !info.IsDir() {
		t.Error("expected directory, got file")
	}

	// Test empty session name defaults to "general"
	err = w.EnsureDir("")
	if err != nil {
		t.Fatalf("EnsureDir with empty name failed: %v", err)
	}
	generalDir := filepath.Join(tmpDir, ".ntm", "handoffs", "general")
	if _, err := os.Stat(generalDir); err != nil {
		t.Errorf("general directory not created: %v", err)
	}

	// Test idempotent (calling again doesn't error)
	err = w.EnsureDir("test-session")
	if err != nil {
		t.Fatalf("second EnsureDir failed: %v", err)
	}
}

func TestWriterWrite(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test-session").
		WithGoalAndNow("Implemented feature X", "Write tests next").
		WithStatus(StatusComplete, OutcomeSucceeded)

	path, err := w.Write(h, "feature-x-complete")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	// Verify file exists
	if _, err := os.Stat(path); err != nil {
		t.Fatalf("written file doesn't exist: %v", err)
	}

	// Verify filename format
	filename := filepath.Base(path)
	if !strings.HasSuffix(filename, "_feature-x-complete.yaml") {
		t.Errorf("unexpected filename format: %s", filename)
	}
	if !strings.Contains(filename, time.Now().Format("2006-01-02")) {
		t.Errorf("filename missing date: %s", filename)
	}

	// Verify content is valid YAML
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read written file: %v", err)
	}

	var parsed Handoff
	if err := yaml.Unmarshal(data, &parsed); err != nil {
		t.Fatalf("written YAML is invalid: %v", err)
	}

	if parsed.Goal != "Implemented feature X" {
		t.Errorf("goal mismatch: got %q", parsed.Goal)
	}
	if parsed.Now != "Write tests next" {
		t.Errorf("now mismatch: got %q", parsed.Now)
	}
	if parsed.Version != HandoffVersion {
		t.Errorf("version mismatch: got %q", parsed.Version)
	}
}

func TestWriterWriteValidationFailure(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Missing required fields
	h := &Handoff{
		Session: "test",
		// Goal and Now are missing
	}

	_, err := w.Write(h, "test")
	if err == nil {
		t.Error("expected validation error for missing goal/now")
	}
	if !strings.Contains(err.Error(), "validation failed") {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestWriterWriteInvalidSession(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("invalid session!").
		WithGoalAndNow("Test", "Test")

	_, err := w.Write(h, "test")
	if err == nil {
		t.Error("expected error for invalid session name")
	}
	// Validate() catches invalid session names with a validation error
	if !strings.Contains(err.Error(), "validation failed") {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestWriterWriteDefaultDescription(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test").WithGoalAndNow("Test goal", "Test now")

	// Empty description should default to "handoff"
	path, err := w.Write(h, "")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	filename := filepath.Base(path)
	if !strings.HasSuffix(filename, "_handoff.yaml") {
		t.Errorf("expected default description, got: %s", filename)
	}
}

func TestWriterWriteAuto(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test-session").
		WithGoalAndNow("Test goal", "Test now").
		SetTokenInfo(80000, 100000)

	path, err := w.WriteAuto(h)
	if err != nil {
		t.Fatalf("WriteAuto failed: %v", err)
	}

	// Verify filename format
	filename := filepath.Base(path)
	if !strings.HasPrefix(filename, "auto-handoff-") {
		t.Errorf("unexpected auto filename format: %s", filename)
	}
	if !strings.HasSuffix(filename, ".yaml") {
		t.Errorf("missing .yaml extension: %s", filename)
	}

	// Verify content
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read written file: %v", err)
	}

	var parsed Handoff
	if err := yaml.Unmarshal(data, &parsed); err != nil {
		t.Fatalf("written YAML is invalid: %v", err)
	}

	if parsed.TokensPct != 80.0 {
		t.Errorf("tokens_pct mismatch: got %f", parsed.TokensPct)
	}
}

func TestWriterRotation(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriterWithOptions(tmpDir, 3, nil) // Keep only 3 files

	h := New("test").WithGoalAndNow("Goal", "Now")

	// Write 5 files with distinct names
	var paths []string
	for i := 0; i < 5; i++ {
		// Ensure distinct timestamps by sleeping briefly
		time.Sleep(10 * time.Millisecond)
		path, err := w.Write(h, "test-"+string(rune('a'+i)))
		if err != nil {
			t.Fatalf("Write %d failed: %v", i, err)
		}
		paths = append(paths, path)
	}

	// Check that only 3 files remain in main directory
	dir := filepath.Join(tmpDir, ".ntm", "handoffs", "test")
	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("failed to read dir: %v", err)
	}

	yamlCount := 0
	for _, e := range entries {
		if !e.IsDir() && strings.HasSuffix(e.Name(), ".yaml") {
			yamlCount++
		}
	}

	if yamlCount != 3 {
		t.Errorf("expected 3 yaml files after rotation, got %d", yamlCount)
	}

	// Check that archive directory exists and has 2 files
	archiveDir := filepath.Join(dir, ".archive")
	archiveEntries, err := os.ReadDir(archiveDir)
	if err != nil {
		t.Fatalf("archive dir should exist: %v", err)
	}

	archiveCount := 0
	for _, e := range archiveEntries {
		if strings.HasSuffix(e.Name(), ".yaml") {
			archiveCount++
		}
	}

	if archiveCount != 2 {
		t.Errorf("expected 2 archived files, got %d", archiveCount)
	}
}

func TestWriterArchive(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test").WithGoalAndNow("Goal", "Now")
	path, err := w.Write(h, "to-archive")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	err = w.Archive(path)
	if err != nil {
		t.Fatalf("Archive failed: %v", err)
	}

	// Original should not exist
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Error("original file should be removed after archive")
	}

	// Archived file should exist
	archivePath := filepath.Join(filepath.Dir(path), ".archive", filepath.Base(path))
	if _, err := os.Stat(archivePath); err != nil {
		t.Errorf("archived file should exist: %v", err)
	}
}

func TestWriterArchiveAlreadyArchived(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Create a file in archive manually
	archiveDir := filepath.Join(tmpDir, ".ntm", "handoffs", "test", ".archive")
	if err := os.MkdirAll(archiveDir, 0755); err != nil {
		t.Fatalf("failed to create archive dir: %v", err)
	}
	archivedFile := filepath.Join(archiveDir, "already-archived.yaml")
	if err := os.WriteFile(archivedFile, []byte("test"), 0644); err != nil {
		t.Fatalf("failed to create test file: %v", err)
	}

	err := w.Archive(archivedFile)
	if err == nil {
		t.Error("expected error when archiving already-archived file")
	}
	if !strings.Contains(err.Error(), "already archived") {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestWriterDelete(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test").WithGoalAndNow("Goal", "Now")
	path, err := w.Write(h, "to-delete")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	err = w.Delete(path)
	if err != nil {
		t.Fatalf("Delete failed: %v", err)
	}

	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Error("file should be deleted")
	}
}

func TestWriterDeleteOutsideBaseDir(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Try to delete a file outside the handoff directory
	err := w.Delete("/tmp/some-other-file.yaml")
	if err == nil {
		t.Error("expected error when deleting file outside base dir")
	}
	if !strings.Contains(err.Error(), "not within handoff directory") {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestWriterCleanArchive(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Create archive with old files
	archiveDir := filepath.Join(tmpDir, ".ntm", "handoffs", "test", ".archive")
	if err := os.MkdirAll(archiveDir, 0755); err != nil {
		t.Fatalf("failed to create archive dir: %v", err)
	}

	// Create a file and make it "old" by modifying its mtime
	oldFile := filepath.Join(archiveDir, "old-handoff.yaml")
	if err := os.WriteFile(oldFile, []byte("test"), 0644); err != nil {
		t.Fatalf("failed to create test file: %v", err)
	}
	oldTime := time.Now().Add(-48 * time.Hour)
	if err := os.Chtimes(oldFile, oldTime, oldTime); err != nil {
		t.Fatalf("failed to set mtime: %v", err)
	}

	// Create a recent file
	newFile := filepath.Join(archiveDir, "new-handoff.yaml")
	if err := os.WriteFile(newFile, []byte("test"), 0644); err != nil {
		t.Fatalf("failed to create test file: %v", err)
	}

	// Clean files older than 24 hours
	removed, err := w.CleanArchive("test", 24*time.Hour)
	if err != nil {
		t.Fatalf("CleanArchive failed: %v", err)
	}

	if removed != 1 {
		t.Errorf("expected 1 removed, got %d", removed)
	}

	// Old file should be gone
	if _, err := os.Stat(oldFile); !os.IsNotExist(err) {
		t.Error("old file should be removed")
	}

	// New file should remain
	if _, err := os.Stat(newFile); err != nil {
		t.Error("new file should still exist")
	}
}

func TestWriterCleanArchiveNoArchive(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Clean non-existent archive should not error
	removed, err := w.CleanArchive("nonexistent", 24*time.Hour)
	if err != nil {
		t.Fatalf("CleanArchive failed: %v", err)
	}
	if removed != 0 {
		t.Errorf("expected 0 removed for non-existent archive, got %d", removed)
	}
}

func TestWriterConcurrentWrites(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	var wg sync.WaitGroup
	errors := make(chan error, 10)

	// Write 10 handoffs concurrently
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			h := New("concurrent").WithGoalAndNow("Goal", "Now")
			_, err := w.Write(h, "concurrent-"+string(rune('a'+idx)))
			if err != nil {
				errors <- err
			}
		}(i)
	}

	wg.Wait()
	close(errors)

	// Check for any errors
	for err := range errors {
		t.Errorf("concurrent write error: %v", err)
	}

	// Verify all files were written
	dir := filepath.Join(tmpDir, ".ntm", "handoffs", "concurrent")
	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("failed to read dir: %v", err)
	}

	yamlCount := 0
	for _, e := range entries {
		if !e.IsDir() && strings.HasSuffix(e.Name(), ".yaml") {
			yamlCount++
		}
	}

	if yamlCount != 10 {
		t.Errorf("expected 10 yaml files, got %d", yamlCount)
	}
}

func TestWriterAtomicWriteIntegrity(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test").
		WithGoalAndNow("Important goal", "Important next step").
		WithStatus(StatusComplete, OutcomeSucceeded).
		AddTask("Task 1", "file1.go").
		AddTask("Task 2", "file2.go").
		AddDecision("approach", "Use atomic writes").
		AddFinding("insight", "Temp files prevent corruption")

	path, err := w.Write(h, "atomic-test")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	// Read back and verify all data is intact
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}

	var parsed Handoff
	if err := yaml.Unmarshal(data, &parsed); err != nil {
		t.Fatalf("YAML parse failed: %v", err)
	}

	if parsed.Goal != "Important goal" {
		t.Errorf("goal corrupted: %s", parsed.Goal)
	}
	if len(parsed.DoneThisSession) != 2 {
		t.Errorf("tasks corrupted: got %d", len(parsed.DoneThisSession))
	}
	if parsed.Decisions["approach"] != "Use atomic writes" {
		t.Errorf("decision corrupted: %v", parsed.Decisions)
	}
}

func TestWriterBaseDir(t *testing.T) {
	w := NewWriter("/tmp/myproject")
	expected := filepath.Join("/tmp/myproject", ".ntm", "handoffs")
	if w.BaseDir() != expected {
		t.Errorf("BaseDir() = %s, want %s", w.BaseDir(), expected)
	}
}

func TestWriterGeneralSession(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	// Test "general" session (special case)
	h := New("general").WithGoalAndNow("Goal", "Now")
	path, err := w.Write(h, "general-test")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	expectedDir := filepath.Join(tmpDir, ".ntm", "handoffs", "general")
	if !strings.HasPrefix(path, expectedDir) {
		t.Errorf("file not in general dir: %s", path)
	}
}

func TestWriterFilePermissions(t *testing.T) {
	tmpDir := t.TempDir()
	w := NewWriter(tmpDir)

	h := New("test").WithGoalAndNow("Goal", "Now")
	path, err := w.Write(h, "perms-test")
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	info, err := os.Stat(path)
	if err != nil {
		t.Fatalf("Stat failed: %v", err)
	}

	// Check file permissions (should be 0644)
	perm := info.Mode().Perm()
	if perm != 0644 {
		t.Errorf("expected permissions 0644, got %o", perm)
	}
}
