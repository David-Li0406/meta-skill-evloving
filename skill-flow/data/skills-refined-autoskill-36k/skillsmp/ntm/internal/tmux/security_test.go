package tmux

import (
	"fmt"
	"testing"
)

func TestBuildPaneCommand_Security(t *testing.T) {
	// Test directory with characters that are dangerous in double quotes but safe in single quotes
	dir := "$HOME"
	cmd := "ls"

	// Go's %q produces "$HOME" which allows shell expansion
	// We want '$HOME' which prevents expansion

	// Check current behavior (vulnerable) or fixed behavior
	got, err := BuildPaneCommand(dir, cmd)
	if err != nil {
		t.Fatalf("BuildPaneCommand failed: %v", err)
	}

	// We expect single quotes for maximum safety
	expected := fmt.Sprintf("cd '%s' && %s", dir, cmd)
	if got != expected {
		// If it's currently using %q, it will likely be: cd "$HOME" && ls
		t.Logf("Got: %s", got)
		t.Logf("Expected: %s", expected)

		// This assertion will fail on the current codebase, confirming the "vulnerability" (or lack of strict quoting)
		// We want to verify it fails first, then fix it.
		// For now, I'll fail if it matches the unsafe pattern
		if got == fmt.Sprintf("cd %q && %s", dir, cmd) {
			t.Errorf("BuildPaneCommand is using unsafe double quotes: %s", got)
		} else if got != expected {
			// It might be something else entirely
			t.Errorf("BuildPaneCommand returned unexpected format. Got: %s, Want: %s", got, expected)
		}
	}
}
