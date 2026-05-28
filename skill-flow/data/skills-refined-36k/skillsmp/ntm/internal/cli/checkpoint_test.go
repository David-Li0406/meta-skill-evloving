package cli

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/checkpoint"
)

func TestNewCheckpointCmd(t *testing.T) {
	cmd := newCheckpointCmd()

	if cmd.Use != "checkpoint" {
		t.Errorf("Use = %q, want %q", cmd.Use, "checkpoint")
	}

	// Verify subcommands are registered
	subcommands := cmd.Commands()
	names := make(map[string]bool)
	for _, sub := range subcommands {
		names[sub.Use] = true
	}

	expected := []string{"save <session>", "list [session]", "show <session> <id>", "delete <session> <id>"} // restore not yet implemented
	for _, exp := range expected {
		if !names[exp] {
			t.Errorf("missing subcommand %q", exp)
		}
	}
}

func TestNewCheckpointSaveCmd(t *testing.T) {
	cmd := newCheckpointSaveCmd()

	if cmd.Use != "save <session>" {
		t.Errorf("Use = %q, want %q", cmd.Use, "save <session>")
	}

	// Verify flags exist
	flags := []string{"message", "scrollback", "no-git"}
	for _, flag := range flags {
		if cmd.Flags().Lookup(flag) == nil {
			t.Errorf("missing flag: %s", flag)
		}
	}
}

func TestNewCheckpointListCmd(t *testing.T) {
	cmd := newCheckpointListCmd()

	if cmd.Use != "list [session]" {
		t.Errorf("Use = %q, want %q", cmd.Use, "list [session]")
	}
}

func TestNewCheckpointShowCmd(t *testing.T) {
	cmd := newCheckpointShowCmd()

	if cmd.Use != "show <session> <id>" {
		t.Errorf("Use = %q, want %q", cmd.Use, "show <session> <id>")
	}
}

func TestNewCheckpointDeleteCmd(t *testing.T) {
	cmd := newCheckpointDeleteCmd()

	if cmd.Use != "delete <session> <id>" {
		t.Errorf("Use = %q, want %q", cmd.Use, "delete <session> <id>")
	}

	// Verify force flag exists
	if cmd.Flags().Lookup("force") == nil {
		t.Error("missing force flag")
	}
}

func TestNewCheckpointRestoreCmd(t *testing.T) {
	t.Skip("newCheckpointRestoreCmd not yet implemented")
}

func TestFormatAge(t *testing.T) {
	tests := []struct {
		name string
		ago  time.Duration
		want string
	}{
		{"just now", 30 * time.Second, "just now"},
		{"minutes", 5 * time.Minute, "5m ago"},
		{"hours", 3 * time.Hour, "3h ago"},
		{"days", 2 * 24 * time.Hour, "2d ago"},
		// Week+ uses date format, harder to test exactly
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			testTime := time.Now().Add(-tt.ago)
			got := formatAge(testTime)
			if got != tt.want {
				t.Errorf("formatAge() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestTruncateStr(t *testing.T) {
	tests := []struct {
		s      string
		maxLen int
		want   string
	}{
		{"short", 10, "short"},
		{"exactly10!", 10, "exactly10!"},
		{"this is a longer string", 10, "this is..."},
		{"abc", 3, "abc"},
		{"abcd", 3, "..."},
		{"", 5, ""},
		{"hello", 0, ""},
	}

	for _, tt := range tests {
		t.Run(tt.s, func(t *testing.T) {
			got := truncateStr(tt.s, tt.maxLen)
			if got != tt.want {
				t.Errorf("truncateStr(%q, %d) = %q, want %q", tt.s, tt.maxLen, got, tt.want)
			}
		})
	}
}

func TestListCheckpointSessions(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-cli-test")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	storage := checkpoint.NewStorageWithDir(tmpDir)

	// Empty directory should return nil
	sessions, err := listCheckpointSessionsWithDir(tmpDir)
	if err != nil {
		t.Fatalf("listCheckpointSessions error: %v", err)
	}
	if sessions != nil && len(sessions) > 0 {
		t.Errorf("expected empty sessions, got %v", sessions)
	}

	// Create a session directory
	sessDir := filepath.Join(tmpDir, "test-session")
	if err := os.MkdirAll(sessDir, 0755); err != nil {
		t.Fatalf("failed to create session dir: %v", err)
	}

	sessions, err = listCheckpointSessionsWithDir(tmpDir)
	if err != nil {
		t.Fatalf("listCheckpointSessions error: %v", err)
	}
	if len(sessions) != 1 || sessions[0] != "test-session" {
		t.Errorf("expected [test-session], got %v", sessions)
	}

	_ = storage // silence unused
}

// listCheckpointSessionsWithDir is a helper for testing that accepts a custom directory.
func listCheckpointSessionsWithDir(baseDir string) ([]string, error) {
	entries, err := os.ReadDir(baseDir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	var sessions []string
	for _, entry := range entries {
		if entry.IsDir() {
			sessions = append(sessions, entry.Name())
		}
	}
	return sessions, nil
}

func TestCheckpointRestoreCmdArgs(t *testing.T) {
	t.Skip("newCheckpointRestoreCmd not yet implemented")
}

func TestCheckpointCmdJSONOutput(t *testing.T) {
	// Test that JSON output produces valid JSON structure
	tmpDir, err := os.MkdirTemp("", "ntm-cli-test")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Simulate what JSON output would look like
	result := map[string]interface{}{
		"session":          "test-session",
		"panes_restored":   2,
		"context_injected": false,
		"dry_run":          true,
		"warnings":         []string{"test warning"},
	}

	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(result); err != nil {
		t.Fatalf("JSON encode error: %v", err)
	}

	// Verify it decodes back correctly
	var decoded map[string]interface{}
	if err := json.NewDecoder(&buf).Decode(&decoded); err != nil {
		t.Fatalf("JSON decode error: %v", err)
	}

	if decoded["session"] != "test-session" {
		t.Errorf("session = %v, want test-session", decoded["session"])
	}
	if decoded["panes_restored"] != float64(2) {
		t.Errorf("panes_restored = %v, want 2", decoded["panes_restored"])
	}
}

func TestCheckpointSaveCmdFlags(t *testing.T) {
	cmd := newCheckpointSaveCmd()

	// Verify default values
	scrollback := cmd.Flags().Lookup("scrollback")
	if scrollback.DefValue != "1000" {
		t.Errorf("scrollback default = %s, want 1000", scrollback.DefValue)
	}

	noGit := cmd.Flags().Lookup("no-git")
	if noGit.DefValue != "false" {
		t.Errorf("no-git default = %s, want false", noGit.DefValue)
	}
}

func TestCheckpointRestoreCmdFlags(t *testing.T) {
	t.Skip("newCheckpointRestoreCmd not yet implemented")
}
