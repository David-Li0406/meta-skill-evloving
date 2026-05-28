package robot

import (
	"encoding/json"
	"testing"
)

func TestPrintSave(t *testing.T) {
	// Need a session to save
	// But PrintSave checks session existence.
	// We can mock or use real session.
	// robot package calls tmux directly.

	// If no session, it should return error.
	opts := SaveOptions{Session: "nonexistent"}
	output, _ := captureStdout(t, func() error { return PrintSave(opts) })

	var resp map[string]interface{}
	if err := json.Unmarshal([]byte(output), &resp); err != nil {
		t.Fatalf("Failed to parse JSON: %v", err)
	}

	// Should have error
	if resp["error"] == nil {
		t.Error("Expected error in response for nonexistent session")
	}
}

func TestPrintRestore(t *testing.T) {
	// Restore from non-existent file
	opts := RestoreOptions{SavedName: "nonexistent_file"}
	output, _ := captureStdout(t, func() error { return PrintRestore(opts) })

	var resp map[string]interface{}
	if err := json.Unmarshal([]byte(output), &resp); err != nil {
		t.Fatalf("Failed to parse JSON: %v", err)
	}

	if resp["error"] == nil {
		t.Error("Expected error for nonexistent file")
	}
}
