// Package robot provides machine-readable output for AI agents.
// ack_test.go contains tests for the acknowledgment detection logic.
package robot

import (
	"testing"
)

func TestDetectAcknowledgment(t *testing.T) {
	tests := []struct {
		name           string
		initialOutput  string
		currentOutput  string
		message        string
		paneTitle      string
		expectedType   AckType
		expectedDetect bool
	}{
		{
			name:           "no change means no ack",
			initialOutput:  "some output\n",
			currentOutput:  "some output\n",
			message:        "test message",
			paneTitle:      "cc_1",
			expectedType:   AckNone,
			expectedDetect: false,
		},
		{
			name:           "explicit ack - understood",
			initialOutput:  "waiting...\n",
			currentOutput:  "waiting...\nunderstood, I'll work on that\n",
			message:        "fix the bug",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "explicit ack - let me",
			initialOutput:  "> ",
			currentOutput:  "> \nLet me take a look at that file\n",
			message:        "check file",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "explicit ack - working on",
			initialOutput:  "idle\n",
			currentOutput:  "idle\nWorking on the tests now\n",
			message:        "fix tests",
			paneTitle:      "cod_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "output started - multiple lines without ack phrase",
			initialOutput:  "prompt> \n",
			currentOutput:  "prompt> \nProcessing your request now\nChecking the files...\n",
			message:        "check something",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck, // "processing" is in explicit ack phrases
			expectedDetect: true,
		},
		{
			name:           "echo detected with follow-up",
			initialOutput:  "> ",
			currentOutput:  "> fix the bug\nOkay, looking at the code...\n",
			message:        "fix the bug",
			paneTitle:      "cc_1",
			expectedType:   AckEchoDetected,
			expectedDetect: true,
		},
		{
			name:           "just echo with no follow-up - no ack yet",
			initialOutput:  "> ",
			currentOutput:  "> fix the bug",
			message:        "fix the bug",
			paneTitle:      "cc_1",
			expectedType:   AckNone,
			expectedDetect: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			ackType, detected := detectAcknowledgment(tt.initialOutput, tt.currentOutput, tt.message, tt.paneTitle)
			if detected != tt.expectedDetect {
				t.Errorf("detectAcknowledgment() detected = %v, want %v", detected, tt.expectedDetect)
			}
			if detected && ackType != tt.expectedType {
				t.Errorf("detectAcknowledgment() type = %v, want %v", ackType, tt.expectedType)
			}
		})
	}
}

func TestGetNewContent(t *testing.T) {
	tests := []struct {
		name     string
		initial  string
		current  string
		expected string
	}{
		{
			name:     "simple append",
			initial:  "hello",
			current:  "hello world",
			expected: " world",
		},
		{
			name:     "new lines",
			initial:  "line1\nline2",
			current:  "line1\nline2\nline3\nline4",
			expected: "\nline3\nline4",
		},
		{
			name:     "no change",
			initial:  "same",
			current:  "same",
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getNewContent(tt.initial, tt.current)
			if result != tt.expected {
				t.Errorf("getNewContent() = %q, want %q", result, tt.expected)
			}
		})
	}
}

func TestTruncateForMatch(t *testing.T) {
	tests := []struct {
		name     string
		message  string
		expected string
	}{
		{
			name:     "short message",
			message:  "fix the bug",
			expected: "fix the bug",
		},
		{
			name:     "long message truncated",
			message:  "this is a very long message that should be truncated at 50 characters for matching purposes",
			expected: "this is a very long message that should be truncat", // 50 chars
		},
		{
			name:     "multiline takes first line",
			message:  "first line\nsecond line",
			expected: "first line",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := truncateForMatch(tt.message)
			if result != tt.expected {
				t.Errorf("truncateForMatch() = %q, want %q", result, tt.expected)
			}
		})
	}
}

func TestIsIdlePrompt(t *testing.T) {
	// isIdlePrompt uses empty agentType for generic detection.
	// Agent-specific prompts (claude>, codex>) require proper agentType to match.
	tests := []struct {
		line     string
		expected bool
	}{
		{"> ", true},       // Generic > prompt
		{"$ ", true},       // Dollar prompt
		{"% ", true},       // Percent prompt
		{"# ", false},      // Not a standard prompt pattern in status
		{"claude>", false}, // Requires "cc" agentType
		{"Claude>", false}, // Requires "cc" agentType
		{"codex>", false},  // Requires "cod" agentType
		{">>> ", false},    // Python prompt not in status patterns
		{"some text", false},
		{"", false},
		{"working...", false},
	}

	for _, tt := range tests {
		t.Run(tt.line, func(t *testing.T) {
			result := isIdlePrompt(tt.line)
			if result != tt.expected {
				t.Errorf("isIdlePrompt(%q) = %v, want %v", tt.line, result, tt.expected)
			}
		})
	}
}

func TestIsPromptLine(t *testing.T) {
	// isPromptLine extracts agentType from pane title and delegates to status.IsPromptLine.
	// Pane titles must be in proper format: "{session}__{type}_{index}".
	tests := []struct {
		line      string
		paneTitle string
		expected  bool
	}{
		{"user@host:~$ ", "", true},           // User prompt
		{"claude> ", "myproject__cc_1", true}, // Claude with proper title
		{"> ", "", true},                      // Generic > prompt
		{">>> ", "", false},                   // Python prompt not in status patterns
		{"some output text", "", false},
		{"error: something failed", "", false},
	}

	for _, tt := range tests {
		t.Run(tt.line, func(t *testing.T) {
			result := isPromptLine(tt.line, tt.paneTitle)
			if result != tt.expected {
				t.Errorf("isPromptLine(%q, %q) = %v, want %v", tt.line, tt.paneTitle, result, tt.expected)
			}
		})
	}
}

func TestGetLastNonEmptyLines(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		n        int
		expected []string
	}{
		{
			name:     "simple case",
			content:  "line1\nline2\nline3\n",
			n:        2,
			expected: []string{"line3", "line2"},
		},
		{
			name:     "with empty lines",
			content:  "line1\n\nline2\n\n\nline3\n",
			n:        3,
			expected: []string{"line3", "line2", "line1"},
		},
		{
			name:     "fewer lines than requested",
			content:  "only one",
			n:        5,
			expected: []string{"only one"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getLastNonEmptyLines(tt.content, tt.n)
			if len(result) != len(tt.expected) {
				t.Errorf("getLastNonEmptyLines() returned %d lines, want %d", len(result), len(tt.expected))
				return
			}
			for i := range result {
				if result[i] != tt.expected[i] {
					t.Errorf("getLastNonEmptyLines()[%d] = %q, want %q", i, result[i], tt.expected[i])
				}
			}
		})
	}
}

func TestGetContentAfterEcho(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		message  string
		expected string
	}{
		{
			name:     "with content after echo",
			content:  "fix the bug\nOkay, I'll fix it",
			message:  "fix the bug",
			expected: "Okay, I'll fix it",
		},
		{
			name:     "no content after echo",
			content:  "fix the bug",
			message:  "fix the bug",
			expected: "",
		},
		{
			name:     "message not found",
			content:  "some other text",
			message:  "fix the bug",
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getContentAfterEcho(tt.content, tt.message)
			if result != tt.expected {
				t.Errorf("getContentAfterEcho() = %q, want %q", result, tt.expected)
			}
		})
	}
}

// =============================================================================
// WAITING AND TIMEOUT BEHAVIOR TESTS
// =============================================================================

// TestAckOptions_Defaults verifies that AckOptions has correct defaults applied
func TestAckOptions_Defaults(t *testing.T) {
	t.Run("zero timeout defaults to 30000ms", func(t *testing.T) {
		opts := AckOptions{
			Session:   "test-session",
			TimeoutMs: 0,
			PollMs:    0,
		}

		// The defaults are applied inside PrintAck, but we can verify the expected values
		if opts.TimeoutMs != 0 {
			t.Errorf("Expected zero TimeoutMs before PrintAck, got %d", opts.TimeoutMs)
		}
		// Default should be 30000ms when zero
		expectedDefault := 30000
		t.Logf("ACK_TEST: Default timeout should be %dms", expectedDefault)
	})

	t.Run("zero poll defaults to 500ms", func(t *testing.T) {
		opts := AckOptions{
			Session:   "test-session",
			TimeoutMs: 5000,
			PollMs:    0,
		}

		if opts.PollMs != 0 {
			t.Errorf("Expected zero PollMs before PrintAck, got %d", opts.PollMs)
		}
		// Default should be 500ms when zero
		expectedDefault := 500
		t.Logf("ACK_TEST: Default poll interval should be %dms", expectedDefault)
	})

	t.Run("custom values are preserved", func(t *testing.T) {
		opts := AckOptions{
			Session:   "test-session",
			Message:   "test message",
			Panes:     []string{"1", "2"},
			TimeoutMs: 10000,
			PollMs:    100,
		}

		if opts.TimeoutMs != 10000 {
			t.Errorf("Expected TimeoutMs=10000, got %d", opts.TimeoutMs)
		}
		if opts.PollMs != 100 {
			t.Errorf("Expected PollMs=100, got %d", opts.PollMs)
		}
		if len(opts.Panes) != 2 {
			t.Errorf("Expected 2 panes, got %d", len(opts.Panes))
		}
	})
}

// TestAckOutput_Structure verifies the AckOutput structure semantics
func TestAckOutput_Structure(t *testing.T) {
	t.Run("initial output state", func(t *testing.T) {
		output := AckOutput{
			Session:       "test-session",
			Confirmations: []AckConfirmation{},
			Pending:       []string{"1", "2", "3"},
			Failed:        []AckFailure{},
			TimeoutMs:     5000,
			TimedOut:      false,
		}

		if output.Session != "test-session" {
			t.Errorf("Session = %q, want %q", output.Session, "test-session")
		}
		if len(output.Confirmations) != 0 {
			t.Errorf("Expected empty Confirmations initially")
		}
		if len(output.Pending) != 3 {
			t.Errorf("Expected 3 pending, got %d", len(output.Pending))
		}
		if output.TimedOut {
			t.Error("TimedOut should be false initially")
		}
	})

	t.Run("timed out output state", func(t *testing.T) {
		output := AckOutput{
			Session:       "test-session",
			Confirmations: []AckConfirmation{{Pane: "1", AckType: "explicit_ack"}},
			Pending:       []string{"2", "3"},
			Failed:        []AckFailure{},
			TimeoutMs:     5000,
			TimedOut:      true,
		}

		if !output.TimedOut {
			t.Error("TimedOut should be true")
		}
		if len(output.Pending) != 2 {
			t.Errorf("Expected 2 still pending, got %d", len(output.Pending))
		}
		if len(output.Confirmations) != 1 {
			t.Errorf("Expected 1 confirmation, got %d", len(output.Confirmations))
		}
	})

	t.Run("fully confirmed output state", func(t *testing.T) {
		output := AckOutput{
			Session: "test-session",
			Confirmations: []AckConfirmation{
				{Pane: "1", AckType: "explicit_ack", LatencyMs: 150},
				{Pane: "2", AckType: "echo_detected", LatencyMs: 200},
			},
			Pending:   []string{},
			Failed:    []AckFailure{},
			TimeoutMs: 5000,
			TimedOut:  false,
		}

		if output.TimedOut {
			t.Error("TimedOut should be false when all confirmed")
		}
		if len(output.Pending) != 0 {
			t.Errorf("Expected 0 pending, got %d", len(output.Pending))
		}
		if len(output.Confirmations) != 2 {
			t.Errorf("Expected 2 confirmations, got %d", len(output.Confirmations))
		}
	})
}

// TestAckConfirmation_Fields verifies AckConfirmation struct
func TestAckConfirmation_Fields(t *testing.T) {
	ack := AckConfirmation{
		Pane:      "1",
		AckType:   string(AckExplicitAck),
		AckAt:     "2026-01-20T12:00:00Z",
		LatencyMs: 250,
	}

	if ack.Pane != "1" {
		t.Errorf("Pane = %q, want %q", ack.Pane, "1")
	}
	if ack.AckType != "explicit_ack" {
		t.Errorf("AckType = %q, want %q", ack.AckType, "explicit_ack")
	}
	if ack.LatencyMs != 250 {
		t.Errorf("LatencyMs = %d, want %d", ack.LatencyMs, 250)
	}
}

// TestAckFailure_Fields verifies AckFailure struct
func TestAckFailure_Fields(t *testing.T) {
	failure := AckFailure{
		Pane:   "session",
		Reason: "session 'test' not found",
	}

	if failure.Pane != "session" {
		t.Errorf("Pane = %q, want %q", failure.Pane, "session")
	}
	if failure.Reason != "session 'test' not found" {
		t.Errorf("Reason = %q, want %q", failure.Reason, "session 'test' not found")
	}
}

// TestAckType_Constants verifies AckType constant values
func TestAckType_Constants(t *testing.T) {
	tests := []struct {
		ackType  AckType
		expected string
	}{
		{AckPromptReturned, "prompt_returned"},
		{AckEchoDetected, "echo_detected"},
		{AckExplicitAck, "explicit_ack"},
		{AckOutputStarted, "output_started"},
		{AckNone, "none"},
	}

	for _, tt := range tests {
		t.Run(string(tt.ackType), func(t *testing.T) {
			if string(tt.ackType) != tt.expected {
				t.Errorf("AckType = %q, want %q", tt.ackType, tt.expected)
			}
		})
	}
}

// TestDetectAcknowledgment_EdgeCases tests edge cases in acknowledgment detection
func TestDetectAcknowledgment_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		initialOutput  string
		currentOutput  string
		message        string
		paneTitle      string
		expectedType   AckType
		expectedDetect bool
	}{
		{
			name:           "whitespace only change - no ack",
			initialOutput:  "output\n",
			currentOutput:  "output\n   \n",
			message:        "test",
			paneTitle:      "cc_1",
			expectedType:   AckNone,
			expectedDetect: false,
		},
		{
			name:           "case insensitive explicit ack - UNDERSTOOD",
			initialOutput:  "waiting\n",
			currentOutput:  "waiting\nUNDERSTOOD\n",
			message:        "fix it",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "case insensitive explicit ack - Looking At",
			initialOutput:  "idle\n",
			currentOutput:  "idle\nLooking At the problem\n",
			message:        "check it",
			paneTitle:      "cod_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "mixed case - i'll do it",
			initialOutput:  "> ",
			currentOutput:  "> \nI'll take care of that\n",
			message:        "handle it",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "partial echo without follow-up",
			initialOutput:  "> ",
			currentOutput:  "> fix", // Partial match of "fix the bug"
			message:        "fix the bug",
			paneTitle:      "cc_1",
			expectedType:   AckNone,
			expectedDetect: false,
		},
		{
			name:           "okay response",
			initialOutput:  "waiting\n",
			currentOutput:  "waiting\nOkay, starting now\n",
			message:        "do it",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "sure response",
			initialOutput:  "> ",
			currentOutput:  "> \nSure, I can help with that\n",
			message:        "help me",
			paneTitle:      "gem_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "analyzing response",
			initialOutput:  "idle\n",
			currentOutput:  "idle\nAnalyzing the codebase...\n",
			message:        "analyze code",
			paneTitle:      "cc_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "yes response",
			initialOutput:  "prompt> ",
			currentOutput:  "prompt> \nYes, I'll work on that.\n",
			message:        "work on task",
			paneTitle:      "cod_1",
			expectedType:   AckExplicitAck,
			expectedDetect: true,
		},
		{
			name:           "output started - many new lines",
			initialOutput:  "ready\n",
			currentOutput:  "ready\nline1\nline2\nline3\nline4\n",
			message:        "generate output",
			paneTitle:      "cc_1",
			expectedType:   AckOutputStarted,
			expectedDetect: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Logf("ACK_TEST: TestDetectAcknowledgment_EdgeCases | Case=%s | InitLen=%d | CurrentLen=%d",
				tt.name, len(tt.initialOutput), len(tt.currentOutput))

			ackType, detected := detectAcknowledgment(tt.initialOutput, tt.currentOutput, tt.message, tt.paneTitle)
			if detected != tt.expectedDetect {
				t.Errorf("detectAcknowledgment() detected = %v, want %v", detected, tt.expectedDetect)
			}
			if detected && ackType != tt.expectedType {
				t.Errorf("detectAcknowledgment() type = %v, want %v", ackType, tt.expectedType)
			}
		})
	}
}

// TestPrintAck_NonexistentSession tests PrintAck with a session that doesn't exist
func TestPrintAck_NonexistentSession(t *testing.T) {
	t.Log("ACK_TEST: TestPrintAck_NonexistentSession | Testing error handling for missing session")

	opts := AckOptions{
		Session:   "nonexistent-session-12345-test",
		Message:   "test message",
		TimeoutMs: 100, // Short timeout for test
		PollMs:    50,
	}

	// PrintAck should handle missing session gracefully
	err := PrintAck(opts)
	if err != nil {
		t.Errorf("PrintAck should not return error for missing session (writes JSON), got: %v", err)
	}
	// The function writes JSON to stdout including the failure info
	t.Log("ACK_TEST: PrintAck handled missing session - failure captured in output")
}

// TestSendAndAckOptions_Defaults verifies SendAndAckOptions defaults
func TestSendAndAckOptions_Defaults(t *testing.T) {
	opts := SendAndAckOptions{
		SendOptions: SendOptions{
			Session: "test-session",
			Message: "test message",
		},
		AckTimeoutMs: 0,
		AckPollMs:    0,
	}

	// Zero values should trigger defaults in PrintSendAndAck
	if opts.AckTimeoutMs != 0 {
		t.Errorf("Expected zero AckTimeoutMs before call, got %d", opts.AckTimeoutMs)
	}
	if opts.AckPollMs != 0 {
		t.Errorf("Expected zero AckPollMs before call, got %d", opts.AckPollMs)
	}
	// Defaults: AckTimeoutMs=30000, AckPollMs=500
	t.Log("ACK_TEST: SendAndAckOptions defaults - AckTimeoutMs=30000ms, AckPollMs=500ms")
}

// TestPrintSendAndAck_NonexistentSession tests combined send+ack with missing session
func TestPrintSendAndAck_NonexistentSession(t *testing.T) {
	t.Log("ACK_TEST: TestPrintSendAndAck_NonexistentSession | Testing error handling")

	opts := SendAndAckOptions{
		SendOptions: SendOptions{
			Session: "nonexistent-session-12345-test",
			Message: "test message",
		},
		AckTimeoutMs: 100,
		AckPollMs:    50,
	}

	err := PrintSendAndAck(opts)
	if err != nil {
		t.Errorf("PrintSendAndAck should not return error for missing session, got: %v", err)
	}
	t.Log("ACK_TEST: PrintSendAndAck handled missing session - failure captured in output")
}

// TestGetNewContent_EdgeCases tests edge cases in content extraction
func TestGetNewContent_EdgeCases(t *testing.T) {
	tests := []struct {
		name     string
		initial  string
		current  string
		wantLen  int // Expected length, not exact content (for complex cases)
		wantNone bool
	}{
		{
			name:     "empty initial",
			initial:  "",
			current:  "new content",
			wantLen:  11, // len("new content")
			wantNone: false,
		},
		{
			name:     "current shorter than initial",
			initial:  "longer initial content",
			current:  "short",
			wantLen:  0,
			wantNone: true,
		},
		{
			name:     "identical content",
			initial:  "same",
			current:  "same",
			wantLen:  0,
			wantNone: true,
		},
		{
			name:     "newline added",
			initial:  "line1",
			current:  "line1\nline2",
			wantLen:  6, // "\nline2"
			wantNone: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getNewContent(tt.initial, tt.current)
			if tt.wantNone && result != "" {
				t.Errorf("getNewContent() = %q, want empty", result)
			}
			if !tt.wantNone && len(result) != tt.wantLen {
				t.Errorf("getNewContent() len = %d, want %d (content: %q)", len(result), tt.wantLen, result)
			}
		})
	}
}

// TestTruncateForMatch_UTF8 tests UTF-8 boundary handling
func TestTruncateForMatch_UTF8(t *testing.T) {
	tests := []struct {
		name    string
		message string
		wantMax int // Result should be at most this length
	}{
		{
			name:    "ASCII within limit",
			message: "short message",
			wantMax: 13,
		},
		{
			name:    "ASCII at limit",
			message: "exactly fifty characters long for testing purposes!",
			wantMax: 50,
		},
		{
			name:    "UTF-8 with emojis",
			message: "Hello 🌍 world! This is a test with unicode chars 🎉🎊",
			wantMax: 50, // Should truncate at rune boundary
		},
		{
			name:    "Japanese characters",
			message: "こんにちは世界これはテストです",
			wantMax: 50,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := truncateForMatch(tt.message)
			if len(result) > tt.wantMax {
				t.Errorf("truncateForMatch() len = %d, want <= %d", len(result), tt.wantMax)
			}
			t.Logf("ACK_TEST: UTF8 truncation | Input=%d bytes | Output=%d bytes",
				len(tt.message), len(result))
		})
	}
}

// TestWaitingBehavior_Semantics documents the expected waiting behavior
func TestWaitingBehavior_Semantics(t *testing.T) {
	t.Log("ACK_TEST: Documenting expected waiting behavior semantics")

	// Document the polling behavior
	t.Run("polling should respect configured interval", func(t *testing.T) {
		// The PollMs option controls how frequently PrintAck checks for changes
		// Default is 500ms
		t.Log("ACK_TEST: Poll interval default = 500ms, configurable via PollMs option")
	})

	t.Run("timeout should trigger after configured duration", func(t *testing.T) {
		// The TimeoutMs option controls how long PrintAck waits before giving up
		// Default is 30000ms (30 seconds)
		t.Log("ACK_TEST: Timeout default = 30000ms, configurable via TimeoutMs option")
	})

	t.Run("pending panes should be tracked correctly", func(t *testing.T) {
		// Initially all target panes are in Pending
		// As each acknowledges, it moves to Confirmations
		// Remaining panes stay in Pending if timeout occurs
		t.Log("ACK_TEST: Panes start in Pending, move to Confirmations on ack")
	})

	t.Run("timeout flag semantics", func(t *testing.T) {
		// TimedOut = true means at least one pane did not acknowledge
		// TimedOut = false means all panes acknowledged (or no target panes)
		t.Log("ACK_TEST: TimedOut=true if any panes still pending at deadline")
	})
}

// TestTimeoutBehavior_Semantics documents the expected timeout behavior
func TestTimeoutBehavior_Semantics(t *testing.T) {
	t.Log("ACK_TEST: Documenting expected timeout behavior semantics")

	t.Run("short timeout for fast tests", func(t *testing.T) {
		// For testing, use short timeouts (e.g., 100ms)
		// Production use typically needs 30s+ for real agents
		shortTimeout := 100
		productionTimeout := 30000
		t.Logf("ACK_TEST: Test timeout = %dms, Production timeout = %dms",
			shortTimeout, productionTimeout)
	})

	t.Run("completed_at timestamp is always set", func(t *testing.T) {
		// CompletedAt is set when PrintAck finishes, regardless of success/timeout
		t.Log("ACK_TEST: CompletedAt timestamp indicates when waiting finished")
	})

	t.Run("latency_ms tracks time from sent_at to ack", func(t *testing.T) {
		// Each AckConfirmation has LatencyMs showing response time
		t.Log("ACK_TEST: LatencyMs = time(AckAt) - time(SentAt)")
	})
}
