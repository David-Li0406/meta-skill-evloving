package git

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"
)

func TestFindProjectRoot(t *testing.T) {
	// Create a temporary directory
	tmpDir, err := os.MkdirTemp("", "ntm-git-test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	// Initialize git repo
	cmd := exec.Command("git", "init")
	cmd.Dir = tmpDir
	if err := cmd.Run(); err != nil {
		t.Skip("git init failed, skipping test:", err)
	}

	// Create a subdirectory
	subDir := filepath.Join(tmpDir, "subdir")
	if err := os.Mkdir(subDir, 0755); err != nil {
		t.Fatal(err)
	}

	// Test from root
	root, err := FindProjectRoot(tmpDir)
	if err != nil {
		t.Errorf("FindProjectRoot(root) error: %v", err)
	}
	// On Mac/Linux, /tmp might be a symlink to /private/tmp, so resolve symlinks
	realTmp, _ := filepath.EvalSymlinks(tmpDir)
	realRoot, _ := filepath.EvalSymlinks(root)
	if realRoot != realTmp {
		t.Errorf("expected root %s, got %s", realTmp, realRoot)
	}

	// Test from subdir
	root, err = FindProjectRoot(subDir)
	if err != nil {
		t.Errorf("FindProjectRoot(subdir) error: %v", err)
	}
	realRoot, _ = filepath.EvalSymlinks(root)
	if realRoot != realTmp {
		t.Errorf("expected root %s, got %s", realTmp, realRoot)
	}
}
