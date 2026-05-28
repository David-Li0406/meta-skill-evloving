// Package watcher tests for file reservation watcher.
package watcher

import (
	"context"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/agentmail"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// TestNewFileReservationWatcher tests the constructor and options.
func TestNewFileReservationWatcher(t *testing.T) {
	t.Run("default values", func(t *testing.T) {
		w := NewFileReservationWatcher()
		t.Logf("RESERVATION_TEST: default_values | pollInterval=%v | idleTimeout=%v | reservationTTL=%v",
			w.pollInterval, w.idleTimeout, w.reservationTTL)

		if w.pollInterval != DefaultPollIntervalReservation {
			t.Errorf("expected pollInterval=%v, got %v", DefaultPollIntervalReservation, w.pollInterval)
		}
		if w.idleTimeout != DefaultIdleTimeout {
			t.Errorf("expected idleTimeout=%v, got %v", DefaultIdleTimeout, w.idleTimeout)
		}
		if w.reservationTTL != DefaultReservationTTL {
			t.Errorf("expected reservationTTL=%v, got %v", DefaultReservationTTL, w.reservationTTL)
		}
		if w.captureLines != DefaultCaptureLinesReservation {
			t.Errorf("expected captureLines=%d, got %d", DefaultCaptureLinesReservation, w.captureLines)
		}
		if w.activeReservations == nil {
			t.Error("activeReservations should be initialized")
		}
	})

	t.Run("with options", func(t *testing.T) {
		client := agentmail.NewClient()
		w := NewFileReservationWatcher(
			WithWatcherClient(client),
			WithProjectDir("/test/project"),
			WithAgentName("TestAgent"),
			WithReservationPollInterval(5*time.Second),
			WithIdleTimeout(5*time.Minute),
			WithReservationTTL(10*time.Minute),
			WithDebug(true),
		)

		t.Logf("RESERVATION_TEST: with_options | projectDir=%s | agentName=%s | debug=%v",
			w.projectDir, w.agentName, w.debug)

		if w.client != client {
			t.Error("client not set correctly")
		}
		if w.projectDir != "/test/project" {
			t.Errorf("expected projectDir=/test/project, got %s", w.projectDir)
		}
		if w.agentName != "TestAgent" {
			t.Errorf("expected agentName=TestAgent, got %s", w.agentName)
		}
		if w.pollInterval != 5*time.Second {
			t.Errorf("expected pollInterval=5s, got %v", w.pollInterval)
		}
		if w.idleTimeout != 5*time.Minute {
			t.Errorf("expected idleTimeout=5m, got %v", w.idleTimeout)
		}
		if w.reservationTTL != 10*time.Minute {
			t.Errorf("expected reservationTTL=10m, got %v", w.reservationTTL)
		}
		if !w.debug {
			t.Error("expected debug=true")
		}
	})

	t.Run("zero duration options ignored", func(t *testing.T) {
		w := NewFileReservationWatcher(
			WithReservationPollInterval(0),
			WithIdleTimeout(0),
			WithReservationTTL(0),
		)

		// Zero values should not override defaults
		if w.pollInterval != DefaultPollIntervalReservation {
			t.Errorf("zero pollInterval should use default, got %v", w.pollInterval)
		}
		if w.idleTimeout != DefaultIdleTimeout {
			t.Errorf("zero idleTimeout should use default, got %v", w.idleTimeout)
		}
		if w.reservationTTL != DefaultReservationTTL {
			t.Errorf("zero reservationTTL should use default, got %v", w.reservationTTL)
		}
	})
}

// TestMapAgentTypeToPatternAgent tests agent type mapping.
func TestMapAgentTypeToPatternAgent(t *testing.T) {
	tests := []struct {
		agentType tmux.AgentType
		expected  string
	}{
		{tmux.AgentClaude, "claude"},
		{tmux.AgentCodex, "codex"},
		{tmux.AgentGemini, "gemini"},
		{tmux.AgentUser, "*"},
		{tmux.AgentType("unknown"), "*"},
	}

	for _, tc := range tests {
		t.Run(string(tc.agentType), func(t *testing.T) {
			result := mapAgentTypeToPatternAgent(tc.agentType)
			t.Logf("RESERVATION_TEST: mapAgentType | input=%s | result=%s", tc.agentType, result)
			if result != tc.expected {
				t.Errorf("expected %s, got %s", tc.expected, result)
			}
		})
	}
}

// TestExtractEditedFiles tests file path extraction from agent output.
func TestExtractEditedFiles(t *testing.T) {
	tests := []struct {
		name      string
		output    string
		agentType string
		expected  []string
	}{
		{
			name:      "claude JSON file_path",
			output:    `{"file_path": "/src/main.go", "old_string": "foo"}`,
			agentType: "claude",
			expected:  []string{"/src/main.go"},
		},
		{
			name:      "claude edited file",
			output:    "I edited file: /internal/watcher/watcher.go to add the new function",
			agentType: "claude",
			expected:  []string{"/internal/watcher/watcher.go"},
		},
		{
			name:      "claude modified file",
			output:    "Modified /cmd/main.go with the new imports",
			agentType: "claude",
			expected:  []string{"/cmd/main.go"},
		},
		{
			name:      "claude created file",
			output:    "Created new file: /internal/utils/helper.go",
			agentType: "claude",
			expected:  []string{"/internal/utils/helper.go"},
		},
		{
			name:      "claude writing to file",
			output:    "Writing to /pkg/config/config.go",
			agentType: "claude",
			expected:  []string{"/pkg/config/config.go"},
		},
		{
			name:      "claude wrote file",
			output:    "Wrote to file /test/test_helper.go",
			agentType: "claude",
			expected:  []string{"/test/test_helper.go"},
		},
		{
			name:      "codex editing file",
			output:    "Editing /src/components/Button.tsx",
			agentType: "codex",
			expected:  []string{"/src/components/Button.tsx"},
		},
		{
			name:      "gemini Writing prefix",
			output:    "Writing: /app/models/user.py",
			agentType: "gemini",
			expected:  []string{"/app/models/user.py"},
		},
		{
			name:      "gemini Editing prefix",
			output:    "Editing: /app/views/home.py",
			agentType: "gemini",
			expected:  []string{"/app/views/home.py"},
		},
		{
			name:      "gemini Created prefix",
			output:    "Created: /tests/test_user.py",
			agentType: "gemini",
			expected:  []string{"/tests/test_user.py"},
		},
		{
			name:      "generic checkmark edited",
			output:    "✓ edited: /src/app.rs",
			agentType: "*",
			expected:  []string{"/src/app.rs"},
		},
		{
			name:      "generic checkmark created",
			output:    "✓ created: /src/lib.rs",
			agentType: "*",
			expected:  []string{"/src/lib.rs"},
		},
		{
			name: "multiple files",
			output: `{"file_path": "/src/a.go"}
			{"file_path": "/src/b.go"}
			Modified /src/c.go`,
			agentType: "claude",
			expected:  []string{"/src/a.go", "/src/b.go", "/src/c.go"},
		},
		{
			name:      "relative path",
			output:    "Edited ./internal/config.go",
			agentType: "claude",
			expected:  []string{"./internal/config.go"},
		},
		{
			name:      "path without extension - ignored",
			output:    "Modified /src/config",
			agentType: "claude",
			expected:  []string{},
		},
		{
			name:      "no files",
			output:    "Just some text without file paths",
			agentType: "claude",
			expected:  []string{},
		},
		{
			name:      "deduplication",
			output:    `{"file_path": "/src/main.go"} and also modified /src/main.go`,
			agentType: "claude",
			expected:  []string{"/src/main.go"},
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := extractEditedFiles(tc.output, tc.agentType)
			t.Logf("RESERVATION_TEST: extractEditedFiles | name=%s | agentType=%s | files=%v",
				tc.name, tc.agentType, result)

			if len(result) != len(tc.expected) {
				t.Errorf("expected %d files, got %d: %v", len(tc.expected), len(result), result)
				return
			}

			// Check each expected file is in result
			for _, exp := range tc.expected {
				found := false
				for _, got := range result {
					if got == exp {
						found = true
						break
					}
				}
				if !found {
					t.Errorf("expected file %s not found in result %v", exp, result)
				}
			}
		})
	}
}

// TestCleanFilePathForReservation tests file path cleaning.
func TestCleanFilePathForReservation(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"/src/main.go", "/src/main.go"},
		{`"/src/main.go"`, "/src/main.go"},
		{`'/src/main.go'`, "/src/main.go"},
		{"  /src/main.go  ", "/src/main.go"},
		{"/src/main.go.", "/src/main.go"},
		{"/src/main.go,", "/src/main.go"},
		{"/src/main.go;", "/src/main.go"},
		{"/src/main.go:", "/src/main.go"},
		{"/src/main.go!", "/src/main.go"},
		{"/src/main.go?", "/src/main.go"},
		{`'  /src/main.go  '`, "/src/main.go"},
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			result := cleanFilePathForReservation(tc.input)
			t.Logf("RESERVATION_TEST: cleanFilePath | input=%q | result=%q", tc.input, result)
			if result != tc.expected {
				t.Errorf("expected %q, got %q", tc.expected, result)
			}
		})
	}
}

// TestIsValidFilePathForReservation tests file path validation.
func TestIsValidFilePathForReservation(t *testing.T) {
	tests := []struct {
		path     string
		expected bool
	}{
		// Valid paths
		{"/src/main.go", true},
		{"./internal/config.go", true},
		{"internal/config.go", true},
		{"/path/to/file.tsx", true},
		{"file.py", true},
		{"/deep/nested/path/file.rs", true},
		{"a.b", true}, // minimal valid

		// Invalid paths
		{"", false},
		{"/src/config", false}, // no extension
		{"path/without/extension", false},
		{"/path/with<invalid>.go", false},
		{"/path/with>invalid.go", false},
		{"/path/with|invalid.go", false},
		{"/path/with*invalid.go", false},
		{"/path/with?invalid.go", false},
		{"/path/with\ninvalid.go", false},
		{"/path/with\tinvalid.go", false},
		{"example.com", false},                  // domain-like
		{"localhost.test", false},               // domain-like
		{"api.v1", false},                       // version-like
		{"v1.0", false},                         // version-like
		{"/path/file.verylongextension", false}, // extension too long
		{".", false},                            // just a dot
		{"file.", false},                        // extension empty
	}

	for _, tc := range tests {
		t.Run(tc.path, func(t *testing.T) {
			result := isValidFilePathForReservation(tc.path)
			t.Logf("RESERVATION_TEST: isValidFilePath | path=%q | result=%v", tc.path, result)
			if result != tc.expected {
				t.Errorf("expected %v, got %v", tc.expected, result)
			}
		})
	}
}

// TestGetActiveReservations tests getting a copy of active reservations.
func TestGetActiveReservations(t *testing.T) {
	w := NewFileReservationWatcher()

	// Add some test reservations
	w.mu.Lock()
	w.activeReservations["pane1"] = &PaneReservation{
		PaneID:        "pane1",
		AgentName:     "Agent1",
		Files:         []string{"/file1.go", "/file2.go"},
		ReservationID: []int{1, 2},
		LastActivity:  time.Now(),
	}
	w.activeReservations["pane2"] = &PaneReservation{
		PaneID:        "pane2",
		AgentName:     "Agent2",
		Files:         []string{"/file3.go"},
		ReservationID: []int{3},
		LastActivity:  time.Now(),
	}
	w.mu.Unlock()

	t.Run("returns copy", func(t *testing.T) {
		result := w.GetActiveReservations()
		t.Logf("RESERVATION_TEST: getActiveReservations | count=%d", len(result))

		if len(result) != 2 {
			t.Errorf("expected 2 reservations, got %d", len(result))
		}

		// Verify it's a copy by modifying the result
		result["pane1"].Files = append(result["pane1"].Files, "/modified.go")

		// Original should be unchanged
		w.mu.Lock()
		if len(w.activeReservations["pane1"].Files) != 2 {
			t.Error("original reservation should not be modified")
		}
		w.mu.Unlock()
	})

	t.Run("empty reservations", func(t *testing.T) {
		emptyW := NewFileReservationWatcher()
		result := emptyW.GetActiveReservations()
		t.Logf("RESERVATION_TEST: getActiveReservations_empty | count=%d", len(result))
		if len(result) != 0 {
			t.Errorf("expected 0 reservations, got %d", len(result))
		}
	})
}

// TestFileReservationWatcherStartStop tests the start/stop lifecycle.
func TestFileReservationWatcherStartStop(t *testing.T) {
	t.Run("start and stop", func(t *testing.T) {
		w := NewFileReservationWatcher(
			WithReservationPollInterval(50 * time.Millisecond),
		)

		ctx := context.Background()
		w.Start(ctx)
		t.Logf("RESERVATION_TEST: watcher started")

		// Let it run briefly
		time.Sleep(100 * time.Millisecond)

		w.Stop()
		t.Logf("RESERVATION_TEST: watcher stopped")

		// Verify it stopped
		if w.cancelFunc != nil {
			// cancelFunc is set during Start, should still be set
			// but calling it again should be safe
		}
	})

	t.Run("stop without start", func(t *testing.T) {
		w := NewFileReservationWatcher()
		// Should not panic
		w.Stop()
		t.Logf("RESERVATION_TEST: stop_without_start completed safely")
	})
}

// TestOnFileEditNoClient tests OnFileEdit behavior without a client.
func TestOnFileEditNoClient(t *testing.T) {
	w := NewFileReservationWatcher(
		WithProjectDir("/test/project"),
		WithAgentName("TestAgent"),
	)

	// Should not panic when client is nil
	ctx := context.Background()
	pane := tmux.Pane{
		ID:   "%1",
		Type: tmux.AgentClaude,
	}

	// This should be a no-op since client is nil
	w.OnFileEdit(ctx, "test-session", pane, []string{"/file.go"})
	t.Logf("RESERVATION_TEST: OnFileEdit_no_client | completed without panic")

	// Verify no reservations were added
	reservations := w.GetActiveReservations()
	if len(reservations) != 0 {
		t.Errorf("expected 0 reservations with nil client, got %d", len(reservations))
	}
}

// TestOnFileEditNoProjectDir tests OnFileEdit behavior without a project directory.
func TestOnFileEditNoProjectDir(t *testing.T) {
	client := agentmail.NewClient()
	w := NewFileReservationWatcher(
		WithWatcherClient(client),
		// No project dir
	)

	ctx := context.Background()
	pane := tmux.Pane{
		ID:   "%1",
		Type: tmux.AgentClaude,
	}

	// This should be a no-op since projectDir is empty
	w.OnFileEdit(ctx, "test-session", pane, []string{"/file.go"})
	t.Logf("RESERVATION_TEST: OnFileEdit_no_projectDir | completed without panic")

	reservations := w.GetActiveReservations()
	if len(reservations) != 0 {
		t.Errorf("expected 0 reservations with empty projectDir, got %d", len(reservations))
	}
}

// TestFilePathPatterns tests that all pattern categories are present.
func TestFilePathPatterns(t *testing.T) {
	expectedAgents := []string{"claude", "codex", "gemini", "*"}

	for _, agent := range expectedAgents {
		t.Run(agent, func(t *testing.T) {
			patterns, ok := filePathPatterns[agent]
			t.Logf("RESERVATION_TEST: filePathPatterns | agent=%s | found=%v | count=%d",
				agent, ok, len(patterns))
			if !ok {
				t.Errorf("expected patterns for agent %s", agent)
			}
			if len(patterns) == 0 {
				t.Errorf("expected non-empty patterns for agent %s", agent)
			}
		})
	}
}

// TestPaneReservationStruct tests the PaneReservation struct.
func TestPaneReservationStruct(t *testing.T) {
	now := time.Now()
	pr := &PaneReservation{
		PaneID:        "%1",
		AgentName:     "TestAgent",
		Files:         []string{"/a.go", "/b.go"},
		ReservationID: []int{1, 2},
		LastActivity:  now,
		LastOutput:    "output hash",
	}

	t.Logf("RESERVATION_TEST: PaneReservation | PaneID=%s | AgentName=%s | Files=%v | IDs=%v",
		pr.PaneID, pr.AgentName, pr.Files, pr.ReservationID)

	if pr.PaneID != "%1" {
		t.Errorf("unexpected PaneID: %s", pr.PaneID)
	}
	if pr.AgentName != "TestAgent" {
		t.Errorf("unexpected AgentName: %s", pr.AgentName)
	}
	if len(pr.Files) != 2 {
		t.Errorf("unexpected Files count: %d", len(pr.Files))
	}
	if len(pr.ReservationID) != 2 {
		t.Errorf("unexpected ReservationID count: %d", len(pr.ReservationID))
	}
	if !pr.LastActivity.Equal(now) {
		t.Error("LastActivity not set correctly")
	}
}
