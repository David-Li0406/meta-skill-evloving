//go:build integration

package tmux

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"sync"
	"testing"
	"time"
)

// =============================================================================
// Session Real Integration Tests (ntm-960v)
//
// These tests create real tmux sessions and verify behavior without any mocks.
// Run with: go test -tags=integration ./internal/tmux/...
// =============================================================================

// uniqueSessionName generates a unique session name for tests
func uniqueSessionName(prefix string) string {
	return fmt.Sprintf("ntm_test_%s_%d", prefix, time.Now().UnixNano())
}

// cleanupSession ensures a session is killed, logging but not failing on error
func cleanupSession(t *testing.T, name string) {
	t.Helper()
	if err := KillSession(name); err != nil {
		t.Logf("cleanup: failed to kill session %s: %v (may not exist)", name, err)
	}
}

// =============================================================================
// Session Creation Tests
// =============================================================================

func TestRealSessionCreationBasic(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("create")
	t.Cleanup(func() { cleanupSession(t, name) })

	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}

	// Wait for session to be ready
	time.Sleep(100 * time.Millisecond)

	// Verify via SessionExists
	if !SessionExists(name) {
		t.Error("session should exist after creation")
	}

	// Verify via tmux list-sessions
	out, err := exec.Command(BinaryPath(), "list-sessions", "-F", "#{session_name}").Output()
	if err != nil {
		t.Fatalf("tmux list-sessions failed: %v", err)
	}
	if !strings.Contains(string(out), name) {
		t.Errorf("session %s not found in tmux list-sessions output", name)
	}
}

func TestRealSessionCreationWithValidNamingPatterns(t *testing.T) {
	skipIfNoTmux(t)

	patterns := []string{
		"simple",
		"with-dashes",
		"with_underscores",
		"MixedCase",
		"with123numbers",
		"a",                       // Single character
		"session-with-many-parts", // Multiple dashes
	}

	for _, pattern := range patterns {
		pattern := pattern
		t.Run(pattern, func(t *testing.T) {
			name := uniqueSessionName(pattern)
			t.Cleanup(func() { cleanupSession(t, name) })

			err := CreateSession(name, t.TempDir())
			if err != nil {
				t.Fatalf("CreateSession(%q) failed: %v", name, err)
			}

			time.Sleep(100 * time.Millisecond)

			if !SessionExists(name) {
				t.Errorf("session %s should exist", name)
			}
		})
	}
}

func TestRealSessionCreationWithCustomWorkDir(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("workdir")
	t.Cleanup(func() { cleanupSession(t, name) })

	// Create a custom working directory
	workDir := t.TempDir()
	testFile := "ntm_test_marker.txt"
	if err := os.WriteFile(workDir+"/"+testFile, []byte("test"), 0644); err != nil {
		t.Fatalf("failed to create test file: %v", err)
	}

	err := CreateSession(name, workDir)
	if err != nil {
		t.Fatalf("CreateSession with workDir failed: %v", err)
	}

	time.Sleep(200 * time.Millisecond)

	// Verify session was created
	if !SessionExists(name) {
		t.Fatal("session should exist")
	}

	// Verify working directory by listing files in the pane
	panes, err := GetPanes(name)
	if err != nil {
		t.Fatalf("GetPanes failed: %v", err)
	}
	if len(panes) == 0 {
		t.Fatal("expected at least one pane")
	}

	// Send ls command to verify working directory
	if err := SendKeys(panes[0].ID, "ls", true); err != nil {
		t.Fatalf("SendKeys failed: %v", err)
	}
	time.Sleep(500 * time.Millisecond) // Wait for command to execute

	output, err := CapturePaneOutput(panes[0].ID, 30)
	if err != nil {
		t.Fatalf("CapturePaneOutput failed: %v", err)
	}

	// The test file should appear in the ls output
	// Note: Terminal may wrap long filenames, so remove newlines for comparison
	normalizedOutput := strings.ReplaceAll(output, "\n", "")
	if !strings.Contains(normalizedOutput, testFile) {
		// Sometimes the shell prompt hasn't finished rendering; retry once
		time.Sleep(500 * time.Millisecond)
		output, _ = CapturePaneOutput(panes[0].ID, 30)
		normalizedOutput = strings.ReplaceAll(output, "\n", "")
		if !strings.Contains(normalizedOutput, testFile) {
			t.Logf("pane output: %q", output)
			t.Errorf("expected to find %s in pane output", testFile)
		}
	}
}

func TestRealSessionNamingCollision(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("collision")
	t.Cleanup(func() { cleanupSession(t, name) })

	// Create first session
	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("first CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Try to create session with same name - should fail
	err = CreateSession(name, t.TempDir())
	if err == nil {
		t.Error("CreateSession with duplicate name should fail")
	} else {
		t.Logf("expected error for duplicate: %v", err)
	}

	// Original session should still exist
	if !SessionExists(name) {
		t.Error("original session should still exist after collision attempt")
	}
}

// =============================================================================
// Session Lifecycle Tests
// =============================================================================

func TestRealSessionKillAndCleanup(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("kill")

	// Create session
	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Verify it exists
	if !SessionExists(name) {
		t.Fatal("session should exist before kill")
	}

	// Kill session
	err = KillSession(name)
	if err != nil {
		t.Errorf("KillSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Verify it's gone
	if SessionExists(name) {
		t.Error("session should not exist after kill")
	}
}

func TestRealSessionResurrectionAfterKill(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("resurrect")
	t.Cleanup(func() { cleanupSession(t, name) })

	// Create session
	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("first CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Kill it
	err = KillSession(name)
	if err != nil {
		t.Fatalf("KillSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Verify it's gone
	if SessionExists(name) {
		t.Fatal("session should be dead")
	}

	// Recreate with same name
	err = CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("second CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Verify it exists again
	if !SessionExists(name) {
		t.Error("session should exist after resurrection")
	}
}

func TestRealSessionNoOrphanProcesses(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("orphan")

	// Create session
	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Get panes and start a background process in one
	panes, err := GetPanes(name)
	if err != nil {
		t.Fatalf("GetPanes failed: %v", err)
	}
	if len(panes) == 0 {
		t.Fatal("expected at least one pane")
	}

	// Start a process that writes to a temp file every second
	markerFile := t.TempDir() + "/process_marker"
	cmd := fmt.Sprintf("while true; do date >> %s; sleep 1; done &", markerFile)
	SendKeys(panes[0].ID, cmd, true)
	time.Sleep(500 * time.Millisecond)

	// Verify process is running (file should be created)
	if _, err := os.Stat(markerFile); os.IsNotExist(err) {
		t.Log("marker file not created yet, process may not have started")
	}

	// Kill session
	err = KillSession(name)
	if err != nil {
		t.Fatalf("KillSession failed: %v", err)
	}
	time.Sleep(500 * time.Millisecond)

	// Session should be gone
	if SessionExists(name) {
		t.Error("session should not exist after kill")
	}

	// Note: The background process may or may not be killed depending on tmux config.
	// This test verifies the session is properly cleaned up. Process cleanup depends
	// on shell settings (huponexit) and is outside tmux's direct control.
}

func TestRealSessionKillNonExistent(t *testing.T) {
	skipIfNoTmux(t)

	// Killing a non-existent session should return an error
	err := KillSession("ntm_definitely_nonexistent_session_xyz")
	if err == nil {
		t.Error("KillSession for non-existent session should return error")
	} else {
		t.Logf("expected error: %v", err)
	}
}

// =============================================================================
// Edge Case Tests
// =============================================================================

func TestRealSessionLongName(t *testing.T) {
	skipIfNoTmux(t)

	// tmux has a limit on session names (typically 256 chars)
	// Test with a moderately long name that should work
	longName := uniqueSessionName(strings.Repeat("x", 50))
	t.Cleanup(func() { cleanupSession(t, longName) })

	err := CreateSession(longName, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession with long name failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	if !SessionExists(longName) {
		t.Error("session with long name should exist")
	}
}

func TestRealSessionInvalidNames(t *testing.T) {
	skipIfNoTmux(t)

	// These names should be rejected by ValidateSessionName
	invalidNames := []string{
		"",               // empty
		"with space",     // space
		"with:colon",     // colon
		"with.period",    // period
		"with/slash",     // slash
		"with;semicolon", // semicolon
	}

	for _, name := range invalidNames {
		t.Run(name, func(t *testing.T) {
			err := ValidateSessionName(name)
			if err == nil {
				t.Errorf("ValidateSessionName(%q) should fail", name)
			}
		})
	}
}

func TestRealSessionConcurrentCreation(t *testing.T) {
	skipIfNoTmux(t)

	const numSessions = 5
	var wg sync.WaitGroup
	var mu sync.Mutex
	sessions := make([]string, 0, numSessions)
	errors := make([]error, 0)

	// Create multiple sessions concurrently
	for i := 0; i < numSessions; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()

			name := uniqueSessionName(fmt.Sprintf("concurrent_%d", idx))
			mu.Lock()
			sessions = append(sessions, name)
			mu.Unlock()

			err := CreateSession(name, t.TempDir())
			if err != nil {
				mu.Lock()
				errors = append(errors, fmt.Errorf("session %d: %w", idx, err))
				mu.Unlock()
			}
		}(i)
	}

	wg.Wait()

	// Cleanup all sessions
	t.Cleanup(func() {
		for _, name := range sessions {
			cleanupSession(t, name)
		}
	})

	// Report any errors
	for _, err := range errors {
		t.Errorf("concurrent creation error: %v", err)
	}

	// Wait for sessions to be ready
	time.Sleep(200 * time.Millisecond)

	// Verify all sessions exist
	successCount := 0
	for _, name := range sessions {
		if SessionExists(name) {
			successCount++
		} else {
			t.Errorf("session %s should exist", name)
		}
	}

	t.Logf("successfully created %d/%d sessions concurrently", successCount, numSessions)
}

func TestRealSessionWithTmuxServerRestart(t *testing.T) {
	skipIfNoTmux(t)
	t.Skip("skipping tmux server restart test - destructive to other tests")

	// This test would restart the tmux server which affects other tests.
	// It's documented here for completeness but skipped by default.
	// To test manually:
	// 1. tmux kill-server
	// 2. Run session creation
	// 3. Verify session is created
}

// =============================================================================
// Session Info Tests
// =============================================================================

func TestRealGetSessionInfo(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("info")
	t.Cleanup(func() { cleanupSession(t, name) })

	workDir := t.TempDir()
	err := CreateSession(name, workDir)
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Get session info
	session, err := GetSession(name)
	if err != nil {
		t.Fatalf("GetSession failed: %v", err)
	}

	// Verify session info
	if session.Name != name {
		t.Errorf("session name = %q, want %q", session.Name, name)
	}
	if session.Windows < 1 {
		t.Errorf("session should have at least 1 window, got %d", session.Windows)
	}
}

func TestRealListSessionsWithMultiple(t *testing.T) {
	skipIfNoTmux(t)

	// Create multiple sessions
	names := make([]string, 3)
	for i := 0; i < 3; i++ {
		names[i] = uniqueSessionName(fmt.Sprintf("list_%d", i))
		if err := CreateSession(names[i], t.TempDir()); err != nil {
			t.Fatalf("CreateSession %d failed: %v", i, err)
		}
	}

	t.Cleanup(func() {
		for _, name := range names {
			cleanupSession(t, name)
		}
	})

	time.Sleep(200 * time.Millisecond)

	// List sessions
	sessions, err := ListSessions()
	if err != nil {
		t.Fatalf("ListSessions failed: %v", err)
	}

	// Verify all our sessions are listed
	found := make(map[string]bool)
	for _, s := range sessions {
		for _, name := range names {
			if s.Name == name {
				found[name] = true
			}
		}
	}

	for _, name := range names {
		if !found[name] {
			t.Errorf("session %s not found in ListSessions", name)
		}
	}
}

// =============================================================================
// Session Pane Integration Tests
// =============================================================================

func TestRealSessionWithPanes(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("panes")
	t.Cleanup(func() { cleanupSession(t, name) })

	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Initially should have 1 pane
	panes, err := GetPanes(name)
	if err != nil {
		t.Fatalf("GetPanes failed: %v", err)
	}
	if len(panes) != 1 {
		t.Errorf("new session should have 1 pane, got %d", len(panes))
	}

	// Add more panes
	for i := 0; i < 3; i++ {
		_, err := SplitWindow(name, t.TempDir())
		if err != nil {
			t.Fatalf("SplitWindow %d failed: %v", i, err)
		}
	}
	time.Sleep(200 * time.Millisecond)

	// Verify pane count
	panes, err = GetPanes(name)
	if err != nil {
		t.Fatalf("GetPanes after split failed: %v", err)
	}
	if len(panes) != 4 {
		t.Errorf("expected 4 panes after splits, got %d", len(panes))
	}
}

func TestRealSessionPaneCleanupOnKill(t *testing.T) {
	skipIfNoTmux(t)

	name := uniqueSessionName("pane_cleanup")

	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Create several panes
	for i := 0; i < 4; i++ {
		_, err := SplitWindow(name, t.TempDir())
		if err != nil {
			t.Fatalf("SplitWindow %d failed: %v", i, err)
		}
	}
	time.Sleep(200 * time.Millisecond)

	// Verify panes exist
	panes, err := GetPanes(name)
	if err != nil {
		t.Fatalf("GetPanes failed: %v", err)
	}
	if len(panes) != 5 {
		t.Errorf("expected 5 panes, got %d", len(panes))
	}

	// Kill session
	err = KillSession(name)
	if err != nil {
		t.Fatalf("KillSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Verify session and all panes are gone
	if SessionExists(name) {
		t.Error("session should not exist")
	}

	_, err = GetPanes(name)
	if err == nil {
		t.Error("GetPanes should fail for killed session")
	}
}
