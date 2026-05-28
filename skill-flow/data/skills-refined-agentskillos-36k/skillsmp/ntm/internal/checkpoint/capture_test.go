package checkpoint

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"
)

func TestCapturer_CaptureGitState(t *testing.T) {
	// Create temp dir for git repo
	tmpDir, err := os.MkdirTemp("", "ntm-capture-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Initialize git repo
	if err := exec.Command("git", "-C", tmpDir, "init").Run(); err != nil {
		t.Fatalf("Failed to git init: %v", err)
	}

	// Configure git user for commits
	exec.Command("git", "-C", tmpDir, "config", "user.email", "test@example.com").Run()
	exec.Command("git", "-C", tmpDir, "config", "user.name", "Test User").Run()

	// Create a file and commit it
	readme := filepath.Join(tmpDir, "README.md")
	if err := os.WriteFile(readme, []byte("test"), 0644); err != nil {
		t.Fatalf("Failed to create file: %v", err)
	}
	exec.Command("git", "-C", tmpDir, "add", ".").Run()
	exec.Command("git", "-C", tmpDir, "commit", "-m", "Initial commit").Run()

	c := NewCapturer()

	// Test success case
	state, err := c.captureGitState(tmpDir, "session", "chk-1")
	if err != nil {
		t.Errorf("captureGitState failed on valid repo: %v", err)
	}
	if state.Branch == "" {
		t.Error("Expected branch to be captured")
	}

	// Test failure case: corrupt the repo
	// Deleting .git/HEAD makes many git commands fail
	if err := os.Remove(filepath.Join(tmpDir, ".git", "HEAD")); err != nil {
		t.Fatalf("Failed to remove .git/HEAD: %v", err)
	}

	_, err = c.captureGitState(tmpDir, "session", "chk-2")
	if err == nil {
		t.Error("captureGitState should fail on corrupt repo")
	}
}
