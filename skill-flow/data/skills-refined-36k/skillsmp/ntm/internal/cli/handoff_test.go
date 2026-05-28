package cli

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/handoff"
)

func TestNewHandoffCmd(t *testing.T) {
	cmd := newHandoffCmd()
	if cmd == nil {
		t.Fatal("newHandoffCmd() returned nil")
	}
	if cmd.Use != "handoff" {
		t.Errorf("Use = %q, want %q", cmd.Use, "handoff")
	}
	if !cmd.HasSubCommands() {
		t.Error("expected handoff command to have subcommands")
	}
}

func TestNewHandoffCreateCmd(t *testing.T) {
	cmd := newHandoffCreateCmd()
	if cmd == nil {
		t.Fatal("newHandoffCreateCmd() returned nil")
	}
	if cmd.Use != "create [session]" {
		t.Errorf("Use = %q, want %q", cmd.Use, "create [session]")
	}

	// Check flags exist
	flags := []string{"goal", "now", "from-file", "auto", "description", "json"}
	for _, name := range flags {
		if cmd.Flags().Lookup(name) == nil {
			t.Errorf("expected flag %q to exist", name)
		}
	}
}

func TestNewHandoffListCmd(t *testing.T) {
	cmd := newHandoffListCmd()
	if cmd == nil {
		t.Fatal("newHandoffListCmd() returned nil")
	}
	if cmd.Use != "list [session]" {
		t.Errorf("Use = %q, want %q", cmd.Use, "list [session]")
	}

	// Check flags exist
	flags := []string{"limit", "json"}
	for _, name := range flags {
		if cmd.Flags().Lookup(name) == nil {
			t.Errorf("expected flag %q to exist", name)
		}
	}
}

func TestNewHandoffShowCmd(t *testing.T) {
	cmd := newHandoffShowCmd()
	if cmd == nil {
		t.Fatal("newHandoffShowCmd() returned nil")
	}
	if cmd.Use != "show <path>" {
		t.Errorf("Use = %q, want %q", cmd.Use, "show <path>")
	}

	// Check flags exist
	if cmd.Flags().Lookup("json") == nil {
		t.Error("expected flag 'json' to exist")
	}
}

func TestGenerateDescription(t *testing.T) {
	tests := []struct {
		goal     string
		expected string
	}{
		{"", "handoff"},
		{"Implemented authentication", "implemented-authentication"},
		{"Fixed bug in the API handler", "fixed-bug-in-the-api-handler"},
		{"A VERY LONG GOAL THAT EXCEEDS THE LIMIT", "a-very-long-goal-that-exceeds"},
		{"With  multiple   spaces", "with-multiple-spaces"},
		{"Special!@#$%^&*()chars", "specialchars"},
		{"kebab-case-already", "kebab-case-already"},
	}

	for _, tc := range tests {
		t.Run(tc.goal, func(t *testing.T) {
			got := generateDescription(tc.goal)
			if got != tc.expected {
				t.Errorf("generateDescription(%q) = %q, want %q", tc.goal, got, tc.expected)
			}
		})
	}
}

func TestTruncateForDisplay(t *testing.T) {
	tests := []struct {
		input    string
		maxLen   int
		expected string
	}{
		{"hello", 10, "hello"},
		{"hello world", 10, "hello w..."},
		{"hi", 10, "hi"},
		{"abc", 3, "abc"},
		{"abcd", 3, "abc"},
		{"", 10, ""},
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			got := truncateForDisplay(tc.input, tc.maxLen)
			if got != tc.expected {
				t.Errorf("truncateForDisplay(%q, %d) = %q, want %q", tc.input, tc.maxLen, got, tc.expected)
			}
		})
	}
}

func TestSplitAndTrim(t *testing.T) {
	tests := []struct {
		input    string
		sep      string
		expected []string
	}{
		{"a,b,c", ",", []string{"a", "b", "c"}},
		{"a, b , c", ",", []string{"a", "b", "c"}},
		{" a , b , c ", ",", []string{"a", "b", "c"}},
		{"", ",", []string{}},
		{"a,,b", ",", []string{"a", "b"}}, // Empty entries removed
		{"single", ",", []string{"single"}},
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			got := splitAndTrim(tc.input, tc.sep)
			if len(got) != len(tc.expected) {
				t.Errorf("splitAndTrim(%q, %q) length = %d, want %d", tc.input, tc.sep, len(got), len(tc.expected))
				return
			}
			for i := range got {
				if got[i] != tc.expected[i] {
					t.Errorf("splitAndTrim(%q, %q)[%d] = %q, want %q", tc.input, tc.sep, i, got[i], tc.expected[i])
				}
			}
		})
	}
}

func TestRunHandoffCreateWithFlags(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run create with flags
	err = runHandoffCreate(cmd, "testsession", "Test goal", "Next task", "", false, "test-desc", false)
	if err != nil {
		t.Fatalf("runHandoffCreate() error: %v", err)
	}

	// Verify output
	output := buf.String()
	if !strings.Contains(output, "Handoff created:") {
		t.Errorf("expected output to contain 'Handoff created:', got: %s", output)
	}
	if !strings.Contains(output, "testsession") {
		t.Errorf("expected output to contain session name, got: %s", output)
	}

	// Verify file was created
	reader := handoff.NewReader(tmpDir)
	h, path, err := reader.FindLatest("testsession")
	if err != nil {
		t.Fatalf("FindLatest() error: %v", err)
	}
	if h == nil {
		t.Fatal("expected handoff to be created")
	}
	if h.Goal != "Test goal" {
		t.Errorf("Goal = %q, want %q", h.Goal, "Test goal")
	}
	if h.Now != "Next task" {
		t.Errorf("Now = %q, want %q", h.Now, "Next task")
	}
	if !strings.Contains(path, "test-desc") {
		t.Errorf("expected path to contain 'test-desc', got: %s", path)
	}
}

func TestRunHandoffCreateJSONOutput(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run create with JSON output
	err = runHandoffCreate(cmd, "testsession", "Test goal", "Next task", "", false, "", true)
	if err != nil {
		t.Fatalf("runHandoffCreate() error: %v", err)
	}

	// Verify JSON output
	var result map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &result); err != nil {
		t.Fatalf("failed to parse JSON output: %v", err)
	}

	if result["success"] != true {
		t.Errorf("expected success = true, got %v", result["success"])
	}
	if result["session"] != "testsession" {
		t.Errorf("session = %q, want %q", result["session"], "testsession")
	}
	if result["goal"] != "Test goal" {
		t.Errorf("goal = %q, want %q", result["goal"], "Test goal")
	}
	if result["now"] != "Next task" {
		t.Errorf("now = %q, want %q", result["now"], "Next task")
	}
	if result["path"] == nil || result["path"] == "" {
		t.Error("expected path to be set")
	}
}

func TestRunHandoffList(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a handoff first
	writer := handoff.NewWriter(tmpDir)
	h := handoff.New("testsession")
	h.Goal = "Test goal"
	h.Now = "Next task"
	h.Status = handoff.StatusComplete
	_, err = writer.Write(h, "test")
	if err != nil {
		t.Fatalf("failed to write handoff: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run list for session
	err = runHandoffList(cmd, "testsession", 10, false)
	if err != nil {
		t.Fatalf("runHandoffList() error: %v", err)
	}

	// Verify output
	output := buf.String()
	if !strings.Contains(output, "testsession") {
		t.Errorf("expected output to contain session name, got: %s", output)
	}
	if !strings.Contains(output, "Test goal") {
		t.Errorf("expected output to contain goal, got: %s", output)
	}
}

func TestRunHandoffListSessions(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create handoffs for two sessions
	writer := handoff.NewWriter(tmpDir)

	h1 := handoff.New("session1")
	h1.Goal = "Goal 1"
	h1.Now = "Now 1"
	h1.Status = handoff.StatusComplete
	_, err = writer.Write(h1, "test1")
	if err != nil {
		t.Fatalf("failed to write handoff 1: %v", err)
	}

	h2 := handoff.New("session2")
	h2.Goal = "Goal 2"
	h2.Now = "Now 2"
	h2.Status = handoff.StatusComplete
	_, err = writer.Write(h2, "test2")
	if err != nil {
		t.Fatalf("failed to write handoff 2: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run list without session (should list sessions)
	err = runHandoffList(cmd, "", 10, false)
	if err != nil {
		t.Fatalf("runHandoffList() error: %v", err)
	}

	// Verify output contains both sessions
	output := buf.String()
	if !strings.Contains(output, "session1") {
		t.Errorf("expected output to contain 'session1', got: %s", output)
	}
	if !strings.Contains(output, "session2") {
		t.Errorf("expected output to contain 'session2', got: %s", output)
	}
}

func TestRunHandoffListJSONOutput(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a handoff first
	writer := handoff.NewWriter(tmpDir)
	h := handoff.New("testsession")
	h.Goal = "Test goal"
	h.Now = "Next task"
	h.Status = handoff.StatusComplete
	_, err = writer.Write(h, "test")
	if err != nil {
		t.Fatalf("failed to write handoff: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run list with JSON output
	err = runHandoffList(cmd, "testsession", 10, true)
	if err != nil {
		t.Fatalf("runHandoffList() error: %v", err)
	}

	// Verify JSON output
	var result map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &result); err != nil {
		t.Fatalf("failed to parse JSON output: %v", err)
	}

	if result["session"] != "testsession" {
		t.Errorf("session = %q, want %q", result["session"], "testsession")
	}
	handoffs := result["handoffs"].([]interface{})
	if len(handoffs) != 1 {
		t.Errorf("expected 1 handoff, got %d", len(handoffs))
	}
}

func TestRunHandoffShow(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a handoff
	writer := handoff.NewWriter(tmpDir)
	h := handoff.New("testsession")
	h.Goal = "Test goal for show"
	h.Now = "Next task for show"
	h.Status = handoff.StatusComplete
	h.Outcome = handoff.OutcomeSucceeded
	h.Blockers = []string{"Blocker 1", "Blocker 2"}
	h.Decisions = map[string]string{"arch": "microservices"}
	h.Next = []string{"Step 1", "Step 2"}
	path, err := writer.Write(h, "test")
	if err != nil {
		t.Fatalf("failed to write handoff: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run show
	err = runHandoffShow(cmd, path, false)
	if err != nil {
		t.Fatalf("runHandoffShow() error: %v", err)
	}

	// Verify output
	output := buf.String()
	expectedParts := []string{
		"Handoff:",
		"Session: testsession",
		"Goal: Test goal for show",
		"Now: Next task for show",
		"Status: complete",
		"Blockers:",
		"Blocker 1",
		"Decisions:",
		"arch: microservices",
		"Next Steps:",
		"Step 1",
	}
	for _, part := range expectedParts {
		if !strings.Contains(output, part) {
			t.Errorf("expected output to contain %q, got: %s", part, output)
		}
	}
}

func TestRunHandoffShowJSONOutput(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a handoff
	writer := handoff.NewWriter(tmpDir)
	h := handoff.New("testsession")
	h.Goal = "Test goal"
	h.Now = "Next task"
	h.Status = handoff.StatusComplete
	path, err := writer.Write(h, "test")
	if err != nil {
		t.Fatalf("failed to write handoff: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run show with JSON output
	err = runHandoffShow(cmd, path, true)
	if err != nil {
		t.Fatalf("runHandoffShow() error: %v", err)
	}

	// Verify JSON output
	var result handoff.Handoff
	if err := json.Unmarshal(buf.Bytes(), &result); err != nil {
		t.Fatalf("failed to parse JSON output: %v", err)
	}

	if result.Session != "testsession" {
		t.Errorf("Session = %q, want %q", result.Session, "testsession")
	}
	if result.Goal != "Test goal" {
		t.Errorf("Goal = %q, want %q", result.Goal, "Test goal")
	}
	if result.Now != "Next task" {
		t.Errorf("Now = %q, want %q", result.Now, "Next task")
	}
}

func TestRunHandoffCreateFromFile(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a source handoff file first
	writer := handoff.NewWriter(tmpDir)
	sourceHandoff := handoff.New("sourcesession")
	sourceHandoff.Goal = "Source goal"
	sourceHandoff.Now = "Source now"
	sourceHandoff.Status = handoff.StatusComplete
	sourceHandoff.Blockers = []string{"Blocker from file"}
	sourcePath, err := writer.Write(sourceHandoff, "source")
	if err != nil {
		t.Fatalf("failed to write source handoff: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run create from file, overriding session name
	err = runHandoffCreate(cmd, "newsession", "", "", sourcePath, false, "from-file", false)
	if err != nil {
		t.Fatalf("runHandoffCreate() error: %v", err)
	}

	// Verify the new handoff was created with new session name
	reader := handoff.NewReader(tmpDir)
	h, _, err := reader.FindLatest("newsession")
	if err != nil {
		t.Fatalf("FindLatest() error: %v", err)
	}
	if h == nil {
		t.Fatal("expected handoff to be created")
	}
	if h.Session != "newsession" {
		t.Errorf("Session = %q, want %q", h.Session, "newsession")
	}
	if h.Goal != "Source goal" {
		t.Errorf("Goal = %q, want %q", h.Goal, "Source goal")
	}
	if len(h.Blockers) != 1 || h.Blockers[0] != "Blocker from file" {
		t.Errorf("Blockers not preserved: %v", h.Blockers)
	}
}

func TestRunHandoffListLimit(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create multiple handoffs
	writer := handoff.NewWriter(tmpDir)
	for i := 0; i < 5; i++ {
		h := handoff.New("testsession")
		h.Goal = "Goal " + string(rune('A'+i))
		h.Now = "Now " + string(rune('A'+i))
		h.Status = handoff.StatusComplete
		_, err = writer.Write(h, "test-"+string(rune('a'+i)))
		if err != nil {
			t.Fatalf("failed to write handoff %d: %v", i, err)
		}
		// Small delay to ensure different timestamps
		time.Sleep(10 * time.Millisecond)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run list with limit
	err = runHandoffList(cmd, "testsession", 2, true)
	if err != nil {
		t.Fatalf("runHandoffList() error: %v", err)
	}

	// Verify JSON output has limited results
	var result map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &result); err != nil {
		t.Fatalf("failed to parse JSON output: %v", err)
	}

	handoffs := result["handoffs"].([]interface{})
	if len(handoffs) != 2 {
		t.Errorf("expected 2 handoffs with limit, got %d", len(handoffs))
	}
}

func TestRunHandoffShowRelativePath(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a handoff
	writer := handoff.NewWriter(tmpDir)
	h := handoff.New("testsession")
	h.Goal = "Test goal"
	h.Now = "Next task"
	h.Status = handoff.StatusComplete
	path, err := writer.Write(h, "test")
	if err != nil {
		t.Fatalf("failed to write handoff: %v", err)
	}

	// Get relative path
	relPath, err := filepath.Rel(tmpDir, path)
	if err != nil {
		t.Fatalf("failed to get relative path: %v", err)
	}

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run show with relative path
	err = runHandoffShow(cmd, relPath, false)
	if err != nil {
		t.Fatalf("runHandoffShow() with relative path error: %v", err)
	}

	// Verify output
	output := buf.String()
	if !strings.Contains(output, "Test goal") {
		t.Errorf("expected output to contain goal, got: %s", output)
	}
}

func TestRunHandoffListNoHandoffs(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	// Create a test command with buffer for output
	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run list for non-existent session
	err = runHandoffList(cmd, "nonexistent", 10, false)
	if err != nil {
		t.Fatalf("runHandoffList() error: %v", err)
	}

	// Verify output indicates no handoffs
	output := buf.String()
	if !strings.Contains(output, "No handoffs found") {
		t.Errorf("expected output to indicate no handoffs, got: %s", output)
	}
}

func TestRunHandoffCreateValidation(t *testing.T) {
	// Create temp directory for test
	tmpDir, err := os.MkdirTemp("", "handoff-test-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Change to temp directory
	oldWd, _ := os.Getwd()
	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("failed to change to temp dir: %v", err)
	}
	defer os.Chdir(oldWd)

	var buf bytes.Buffer
	cmd := &cobra.Command{}
	cmd.SetOut(&buf)

	// Run create with goal but without now should still work (uses defaults)
	err = runHandoffCreate(cmd, "testsession", "Test goal", "Task now", "", false, "", false)
	if err != nil {
		t.Fatalf("runHandoffCreate() with goal and now should succeed: %v", err)
	}
}
