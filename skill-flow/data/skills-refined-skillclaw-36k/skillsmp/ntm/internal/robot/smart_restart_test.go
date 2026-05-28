package robot

import (
	"testing"
)

// =============================================================================
// Unit Tests for --robot-smart-restart (bd-2c7f4, bd-2eo1l)
// =============================================================================

// TestDecideRestart tests the decision matrix for restart actions.
func TestDecideRestart(t *testing.T) {
	tests := []struct {
		name               string
		status             PaneWorkStatus
		force              bool
		wantRestart        bool
		wantReasonContains string
		wantWarning        bool
	}{
		// Working agent scenarios
		{
			name: "working agent without force - skip",
			status: PaneWorkStatus{
				IsWorking:      true,
				Recommendation: "DO_NOT_INTERRUPT",
			},
			force:              false,
			wantRestart:        false,
			wantReasonContains: "actively working",
		},
		{
			name: "working agent with force - restart with warning",
			status: PaneWorkStatus{
				IsWorking:      true,
				Recommendation: "DO_NOT_INTERRUPT",
			},
			force:              true,
			wantRestart:        true,
			wantReasonContains: "FORCED",
			wantWarning:        true,
		},

		// Idle agent scenarios
		{
			name: "idle agent safe to restart",
			status: PaneWorkStatus{
				IsIdle:         true,
				IsWorking:      false,
				Recommendation: "SAFE_TO_RESTART",
			},
			force:              false,
			wantRestart:        true,
			wantReasonContains: "idle",
		},

		// Context low scenarios
		{
			name: "low context working - skip",
			status: PaneWorkStatus{
				IsWorking:      true,
				IsContextLow:   true,
				Recommendation: "CONTEXT_LOW_CONTINUE",
			},
			force:              false,
			wantRestart:        false,
			wantReasonContains: "working", // IsWorking check comes first
		},
		{
			name: "low context idle - restart",
			status: PaneWorkStatus{
				IsWorking:        false,
				IsIdle:           true,
				IsContextLow:     true,
				ContextRemaining: float64Ptr(12.0),
				Recommendation:   "CONTEXT_LOW_CONTINUE",
			},
			force:              false,
			wantRestart:        true,
			wantReasonContains: "low context",
		},

		// Rate limited scenarios
		{
			name: "rate limited without force - skip",
			status: PaneWorkStatus{
				IsRateLimited:  true,
				Recommendation: "RATE_LIMITED_WAIT",
			},
			force:              false,
			wantRestart:        false,
			wantReasonContains: "Rate limited",
		},
		{
			name: "rate limited with force - restart with warning",
			status: PaneWorkStatus{
				IsRateLimited:  true,
				Recommendation: "RATE_LIMITED_WAIT",
			},
			force:              true,
			wantRestart:        true,
			wantReasonContains: "FORCED",
			wantWarning:        true,
		},

		// Error state scenarios
		{
			name: "error state - restart",
			status: PaneWorkStatus{
				Recommendation: "ERROR_STATE",
			},
			force:              false,
			wantRestart:        true,
			wantReasonContains: "error state",
		},

		// Unknown state scenarios
		{
			name: "unknown state without force - skip",
			status: PaneWorkStatus{
				Recommendation: "UNKNOWN",
			},
			force:              false,
			wantRestart:        false,
			wantReasonContains: "manual inspection",
		},
		{
			name: "unknown state with force - restart with warning",
			status: PaneWorkStatus{
				Recommendation: "UNKNOWN",
			},
			force:              true,
			wantRestart:        true,
			wantReasonContains: "FORCED",
			wantWarning:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			shouldRestart, reason, warning := decideRestart(&tt.status, tt.force)

			if shouldRestart != tt.wantRestart {
				t.Errorf("decideRestart() shouldRestart = %v, want %v", shouldRestart, tt.wantRestart)
			}

			if !smartContains(reason, tt.wantReasonContains) {
				t.Errorf("decideRestart() reason = %q, want to contain %q", reason, tt.wantReasonContains)
			}

			if tt.wantWarning && warning == "" {
				t.Errorf("decideRestart() expected warning, got empty")
			}
			if !tt.wantWarning && warning != "" {
				t.Errorf("decideRestart() expected no warning, got %q", warning)
			}
		})
	}
}

// TestDefaultSmartRestartOptions tests default options.
func TestDefaultSmartRestartOptions(t *testing.T) {
	opts := DefaultSmartRestartOptions()

	if opts.LinesCaptured != 100 {
		t.Errorf("DefaultSmartRestartOptions().LinesCaptured = %d, want 100", opts.LinesCaptured)
	}

	if opts.PostWaitTime != 6000000000 { // 6 seconds in nanoseconds
		t.Errorf("DefaultSmartRestartOptions().PostWaitTime = %v, want 6s", opts.PostWaitTime)
	}

	if opts.Force {
		t.Error("DefaultSmartRestartOptions().Force should be false")
	}

	if opts.DryRun {
		t.Error("DefaultSmartRestartOptions().DryRun should be false")
	}
}

// TestRestartActionTypes tests action type constants.
func TestRestartActionTypes(t *testing.T) {
	tests := []struct {
		action   RestartActionType
		expected string
	}{
		{ActionRestarted, "RESTARTED"},
		{ActionSkipped, "SKIPPED"},
		{ActionWaiting, "WAITING"},
		{ActionFailed, "FAILED"},
		{ActionWouldRestart, "WOULD_RESTART"},
	}

	for _, tt := range tests {
		if string(tt.action) != tt.expected {
			t.Errorf("RestartActionType = %q, want %q", tt.action, tt.expected)
		}
	}
}

// TestBuildWaitInfo tests wait info construction.
func TestBuildWaitInfo(t *testing.T) {
	status := &PaneWorkStatus{
		IsRateLimited: true,
	}

	info := buildWaitInfo(status)

	if info == nil {
		t.Fatal("buildWaitInfo() returned nil")
	}

	if info.Suggestion == "" {
		t.Error("buildWaitInfo() should provide a suggestion")
	}

	if info.WaitSeconds <= 0 {
		t.Errorf("buildWaitInfo() WaitSeconds = %d, want > 0", info.WaitSeconds)
	}
}

// TestAppendPaneToAction tests pane tracking in summary.
func TestAppendPaneToAction(t *testing.T) {
	panesByAction := make(map[string][]int)

	appendPaneToAction(panesByAction, "RESTARTED", 2)
	appendPaneToAction(panesByAction, "RESTARTED", 3)
	appendPaneToAction(panesByAction, "SKIPPED", 4)

	if len(panesByAction["RESTARTED"]) != 2 {
		t.Errorf("RESTARTED panes = %d, want 2", len(panesByAction["RESTARTED"]))
	}

	if len(panesByAction["SKIPPED"]) != 1 {
		t.Errorf("SKIPPED panes = %d, want 1", len(panesByAction["SKIPPED"]))
	}

	// Check pane values
	if panesByAction["RESTARTED"][0] != 2 || panesByAction["RESTARTED"][1] != 3 {
		t.Errorf("RESTARTED panes = %v, want [2, 3]", panesByAction["RESTARTED"])
	}
}

// TestLooksLikeShellPrompt tests shell prompt detection.
func TestLooksLikeShellPrompt(t *testing.T) {
	tests := []struct {
		name   string
		output string
		want   bool
	}{
		{
			name:   "bash prompt with dollar",
			output: "user@host:~$ ",
			want:   true,
		},
		{
			name:   "zsh prompt with percent",
			output: "user@host % ",
			want:   true,
		},
		{
			name:   "root prompt with hash",
			output: "root@host:~# ",
			want:   true,
		},
		{
			name:   "fish prompt",
			output: "user@host ~/projects ❯ ",
			want:   true,
		},
		{
			name:   "simple arrow prompt",
			output: "→ ",
			want:   true,
		},
		{
			name:   "ends with dollar",
			output: "some text$",
			want:   true,
		},
		{
			name:   "ends with greater than",
			output: "prompt>",
			want:   true,
		},
		{
			name:   "claude code output",
			output: "╭─ Claude Code\n│ Working on task...\n╰─────────────────────",
			want:   false,
		},
		{
			name:   "codex output",
			output: "Codex> Processing your request...",
			want:   false,
		},
		{
			name:   "empty output",
			output: "",
			want:   false,
		},
		{
			name:   "multiline with prompt at end",
			output: "some output\nmore output\nuser@host:~$ ",
			want:   true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := looksLikeShellPrompt(tt.output)
			if got != tt.want {
				t.Errorf("looksLikeShellPrompt(%q) = %v, want %v", tt.output, got, tt.want)
			}
		})
	}
}

// TestContainsSuffix tests suffix checking.
func TestContainsSuffix(t *testing.T) {
	tests := []struct {
		s      string
		suffix string
		want   bool
	}{
		{"hello world", "world", true},
		{"hello world", "hello", false},
		{"test", "test", true},
		{"test", "testing", false},
		{"", "", true},
		{"a", "ab", false},
	}

	for _, tt := range tests {
		got := containsSuffix(tt.s, tt.suffix)
		if got != tt.want {
			t.Errorf("containsSuffix(%q, %q) = %v, want %v", tt.s, tt.suffix, got, tt.want)
		}
	}
}

// TestTrimSpace tests whitespace trimming.
func TestTrimSpace(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{"  hello  ", "hello"},
		{"\t\ttab\t\t", "tab"},
		{"\n\nnewline\n\n", "newline"},
		{"no whitespace", "no whitespace"},
		{"   ", ""},
		{"", ""},
		{" a ", "a"},
	}

	for _, tt := range tests {
		got := trimSpace(tt.input)
		if got != tt.want {
			t.Errorf("trimSpace(%q) = %q, want %q", tt.input, got, tt.want)
		}
	}
}

// TestIsSpace tests whitespace character detection.
func TestIsSpace(t *testing.T) {
	tests := []struct {
		c    byte
		want bool
	}{
		{' ', true},
		{'\t', true},
		{'\n', true},
		{'\r', true},
		{'a', false},
		{'0', false},
		{'$', false},
	}

	for _, tt := range tests {
		got := isSpace(tt.c)
		if got != tt.want {
			t.Errorf("isSpace(%q) = %v, want %v", tt.c, got, tt.want)
		}
	}
}

// TestFormatReasonWithPercent tests percentage formatting in reasons.
func TestFormatReasonWithPercent(t *testing.T) {
	tests := []struct {
		format string
		pct    float64
		want   string
	}{
		{"Idle with low context (%.0f%%)", 12.0, "Idle with low context (12%)"},
		{"Usage at %.0f%%", 85.5, "Usage at 86%"}, // Rounds up
		{"%.0f%% remaining", 0.0, "0% remaining"},
		{"No format", 50.0, "No format"},
	}

	for _, tt := range tests {
		got := formatReasonWithPercent(tt.format, tt.pct)
		if got != tt.want {
			t.Errorf("formatReasonWithPercent(%q, %.1f) = %q, want %q", tt.format, tt.pct, got, tt.want)
		}
	}
}

// TestSimpleError tests the error helper.
func TestSimpleError(t *testing.T) {
	err := newError("test error")
	if err.Error() != "test error" {
		t.Errorf("newError() = %q, want %q", err.Error(), "test error")
	}

	wrapped := wrapError("prefix", err)
	if wrapped.Error() != "prefix: test error" {
		t.Errorf("wrapError() = %q, want %q", wrapped.Error(), "prefix: test error")
	}
}

// TestPreCheckInfo tests the PreCheckInfo structure.
func TestPreCheckInfo(t *testing.T) {
	pct := 15.0
	info := PreCheckInfo{
		Recommendation:   "SAFE_TO_RESTART",
		IsWorking:        false,
		IsIdle:           true,
		IsRateLimited:    false,
		IsContextLow:     true,
		ContextRemaining: &pct,
		Confidence:       0.95,
		AgentType:        "cc",
	}

	if info.Recommendation != "SAFE_TO_RESTART" {
		t.Error("PreCheckInfo.Recommendation mismatch")
	}
	if info.IsWorking {
		t.Error("PreCheckInfo.IsWorking should be false")
	}
	if !info.IsIdle {
		t.Error("PreCheckInfo.IsIdle should be true")
	}
	if info.IsRateLimited {
		t.Error("PreCheckInfo.IsRateLimited should be false")
	}
	if !info.IsContextLow {
		t.Error("PreCheckInfo.IsContextLow should be true")
	}
	if info.ContextRemaining == nil || *info.ContextRemaining != 15.0 {
		t.Error("PreCheckInfo.ContextRemaining mismatch")
	}
	if info.Confidence != 0.95 {
		t.Error("PreCheckInfo.Confidence mismatch")
	}
	if info.AgentType != "cc" {
		t.Error("PreCheckInfo.AgentType mismatch")
	}
}

// TestRestartSequence tests the RestartSequence structure.
func TestRestartSequence(t *testing.T) {
	seq := RestartSequence{
		ExitMethod:     "double_ctrl_c",
		ExitDurationMs: 3000,
		ShellConfirmed: true,
		AgentLaunched:  true,
		AgentType:      "cc",
		PromptSent:     true,
	}

	if seq.ExitMethod != "double_ctrl_c" {
		t.Error("RestartSequence.ExitMethod mismatch")
	}
	if seq.ExitDurationMs != 3000 {
		t.Error("RestartSequence.ExitDurationMs mismatch")
	}
	if !seq.ShellConfirmed {
		t.Error("RestartSequence.ShellConfirmed should be true")
	}
	if !seq.AgentLaunched {
		t.Error("RestartSequence.AgentLaunched should be true")
	}
	if seq.AgentType != "cc" {
		t.Error("RestartSequence.AgentType mismatch")
	}
	if !seq.PromptSent {
		t.Error("RestartSequence.PromptSent should be true")
	}
}

// TestPostStateInfo tests the PostStateInfo structure.
func TestPostStateInfo(t *testing.T) {
	info := PostStateInfo{
		AgentRunning: true,
		AgentType:    "cod",
		Confidence:   0.87,
	}

	if !info.AgentRunning {
		t.Error("PostStateInfo.AgentRunning should be true")
	}
	if info.AgentType != "cod" {
		t.Error("PostStateInfo.AgentType mismatch")
	}
	if info.Confidence != 0.87 {
		t.Error("PostStateInfo.Confidence mismatch")
	}
}

// TestWaitInfo tests the WaitInfo structure.
func TestWaitInfo(t *testing.T) {
	info := WaitInfo{
		ResetsAt:    "2026-01-20T18:00:00Z",
		WaitSeconds: 3600,
		Suggestion:  "Consider caam account switch",
	}

	if info.ResetsAt != "2026-01-20T18:00:00Z" {
		t.Error("WaitInfo.ResetsAt mismatch")
	}
	if info.WaitSeconds != 3600 {
		t.Error("WaitInfo.WaitSeconds mismatch")
	}
	if info.Suggestion != "Consider caam account switch" {
		t.Error("WaitInfo.Suggestion mismatch")
	}
}

// TestRestartAction tests the RestartAction structure.
func TestRestartAction(t *testing.T) {
	action := RestartAction{
		Action:  ActionRestarted,
		Reason:  "Agent is idle",
		Warning: "",
	}

	if action.Action != ActionRestarted {
		t.Error("RestartAction.Action mismatch")
	}
	if action.Reason != "Agent is idle" {
		t.Error("RestartAction.Reason mismatch")
	}
}

// TestRestartSummary tests the RestartSummary structure.
func TestRestartSummary(t *testing.T) {
	summary := RestartSummary{
		Restarted:     2,
		Skipped:       1,
		Waiting:       1,
		Failed:        0,
		WouldRestart:  0,
		PanesByAction: make(map[string][]int),
	}

	summary.PanesByAction["RESTARTED"] = []int{2, 3}
	summary.PanesByAction["SKIPPED"] = []int{4}
	summary.PanesByAction["WAITING"] = []int{5}

	if summary.Restarted != 2 {
		t.Error("RestartSummary.Restarted mismatch")
	}
	if summary.Skipped != 1 {
		t.Error("RestartSummary.Skipped mismatch")
	}
	if summary.Waiting != 1 {
		t.Error("RestartSummary.Waiting mismatch")
	}
	if summary.Failed != 0 {
		t.Error("RestartSummary.Failed mismatch")
	}
}

// TestDecisionMatrix tests the full decision matrix from the spec.
func TestDecisionMatrix(t *testing.T) {
	// Table from spec:
	// | Pre-Check State | Context | Rate Limited | Force | Action |
	// |-----------------|---------|--------------|-------|--------|
	// | Working | Any | No | No | SKIP |
	// | Working | Any | No | Yes | RESTART (with warning) |
	// | Working | Any | Yes | No | SKIP (let finish) |
	// | Idle | >20% | No | No | OPTIONAL (can restart) |
	// | Idle | <20% | No | No | RESTART recommended |
	// | Idle | Any | Yes | No | WAIT for reset |
	// | Error | Any | Any | No | RESTART |
	// | Unknown | Any | Any | No | SKIP + WARN |

	tests := []struct {
		name        string
		status      PaneWorkStatus
		force       bool
		wantRestart bool
	}{
		// Working + No rate limit + No force = SKIP
		{
			name: "working-no-limit-no-force",
			status: PaneWorkStatus{
				IsWorking:      true,
				IsRateLimited:  false,
				Recommendation: "DO_NOT_INTERRUPT",
			},
			force:       false,
			wantRestart: false,
		},
		// Working + No rate limit + Force = RESTART
		{
			name: "working-no-limit-force",
			status: PaneWorkStatus{
				IsWorking:      true,
				IsRateLimited:  false,
				Recommendation: "DO_NOT_INTERRUPT",
			},
			force:       true,
			wantRestart: true,
		},
		// Working + Rate limited + No force = SKIP (let finish)
		{
			name: "working-rate-limited-no-force",
			status: PaneWorkStatus{
				IsWorking:      true,
				IsRateLimited:  true,
				Recommendation: "RATE_LIMITED_WAIT",
			},
			force:       false,
			wantRestart: false,
		},
		// Idle + Context > 20% + No rate limit = RESTART (optional)
		{
			name: "idle-high-context-no-limit",
			status: PaneWorkStatus{
				IsWorking:        false,
				IsIdle:           true,
				IsContextLow:     false,
				ContextRemaining: float64Ptr(50.0),
				IsRateLimited:    false,
				Recommendation:   "SAFE_TO_RESTART",
			},
			force:       false,
			wantRestart: true,
		},
		// Idle + Context < 20% + No rate limit = RESTART
		{
			name: "idle-low-context-no-limit",
			status: PaneWorkStatus{
				IsWorking:        false,
				IsIdle:           true,
				IsContextLow:     true,
				ContextRemaining: float64Ptr(12.0),
				IsRateLimited:    false,
				Recommendation:   "CONTEXT_LOW_CONTINUE",
			},
			force:       false,
			wantRestart: true,
		},
		// Idle + Rate limited = WAIT (handled separately in SmartRestart)
		// Error = RESTART
		{
			name: "error-state",
			status: PaneWorkStatus{
				Recommendation: "ERROR_STATE",
			},
			force:       false,
			wantRestart: true,
		},
		// Unknown = SKIP
		{
			name: "unknown-state",
			status: PaneWorkStatus{
				Recommendation: "UNKNOWN_RECOMMENDATION",
			},
			force:       false,
			wantRestart: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, _, _ := decideRestart(&tt.status, tt.force)
			if got != tt.wantRestart {
				t.Errorf("decideRestart() = %v, want %v", got, tt.wantRestart)
			}
		})
	}
}

// Helper function for tests
func float64Ptr(v float64) *float64 {
	return &v
}

// smartContains checks if s contains substr (case-insensitive for flexibility).
func smartContains(s, substr string) bool {
	if substr == "" {
		return true
	}
	// Simple case-sensitive contains
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	// Also try lowercase
	sLower := toLower(s)
	subLower := toLower(substr)
	for i := 0; i <= len(sLower)-len(subLower); i++ {
		if sLower[i:i+len(subLower)] == subLower {
			return true
		}
	}
	return false
}

// toLower converts a string to lowercase (simple ASCII-only).
func toLower(s string) string {
	result := make([]byte, len(s))
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= 'A' && c <= 'Z' {
			result[i] = c + 32
		} else {
			result[i] = c
		}
	}
	return string(result)
}

// =============================================================================
// Hard Kill Tests (bd-bh74z)
// =============================================================================

// TestHardKillResult tests the HardKillResult structure.
func TestHardKillResult(t *testing.T) {
	result := HardKillResult{
		ShellPID:   12345,
		ChildPID:   12346,
		KillMethod: "kill_9",
		Success:    true,
	}

	if result.ShellPID != 12345 {
		t.Errorf("HardKillResult.ShellPID = %d, want 12345", result.ShellPID)
	}
	if result.ChildPID != 12346 {
		t.Errorf("HardKillResult.ChildPID = %d, want 12346", result.ChildPID)
	}
	if result.KillMethod != "kill_9" {
		t.Errorf("HardKillResult.KillMethod = %q, want 'kill_9'", result.KillMethod)
	}
	if !result.Success {
		t.Error("HardKillResult.Success should be true")
	}
}

// TestHardKillResultNoChild tests when no child process is found.
func TestHardKillResultNoChild(t *testing.T) {
	result := HardKillResult{
		ShellPID:   12345,
		ChildPID:   0,
		KillMethod: "no_child_process",
		Success:    true,
	}

	if result.KillMethod != "no_child_process" {
		t.Errorf("HardKillResult.KillMethod = %q, want 'no_child_process'", result.KillMethod)
	}
	if !result.Success {
		t.Error("no_child_process should still be success (agent already exited)")
	}
}

// TestRestartSequenceWithHardKill tests the RestartSequence with hard kill fields.
func TestRestartSequenceWithHardKill(t *testing.T) {
	seq := RestartSequence{
		ExitMethod:     "hard_kill",
		ExitDurationMs: 1000,
		ShellConfirmed: true,
		AgentLaunched:  true,
		AgentType:      "cc",
		HardKillUsed:   true,
		HardKillResult: &HardKillResult{
			ShellPID:   54321,
			ChildPID:   54322,
			KillMethod: "kill_9",
			Success:    true,
		},
	}

	if seq.ExitMethod != "hard_kill" {
		t.Errorf("RestartSequence.ExitMethod = %q, want 'hard_kill'", seq.ExitMethod)
	}
	if !seq.HardKillUsed {
		t.Error("RestartSequence.HardKillUsed should be true")
	}
	if seq.HardKillResult == nil {
		t.Fatal("RestartSequence.HardKillResult should not be nil")
	}
	if seq.HardKillResult.ShellPID != 54321 {
		t.Errorf("HardKillResult.ShellPID = %d, want 54321", seq.HardKillResult.ShellPID)
	}
}

// TestSmartRestartOptionsWithHardKill tests the options struct with hard kill flags.
func TestSmartRestartOptionsWithHardKill(t *testing.T) {
	opts := SmartRestartOptions{
		Session:      "test-session",
		Panes:        []int{2, 3, 4},
		Force:        false,
		DryRun:       false,
		HardKill:     true,
		HardKillOnly: false,
	}

	if !opts.HardKill {
		t.Error("SmartRestartOptions.HardKill should be true")
	}
	if opts.HardKillOnly {
		t.Error("SmartRestartOptions.HardKillOnly should be false")
	}
}

// TestSmartRestartOptionsHardKillOnly tests the hard kill only option.
func TestSmartRestartOptionsHardKillOnly(t *testing.T) {
	opts := SmartRestartOptions{
		Session:      "test-session",
		Panes:        []int{2},
		HardKill:     false, // Doesn't matter when HardKillOnly is true
		HardKillOnly: true,
	}

	if !opts.HardKillOnly {
		t.Error("SmartRestartOptions.HardKillOnly should be true")
	}
}

// TestDefaultOptionsNoHardKill tests that hard kill is disabled by default.
func TestDefaultOptionsNoHardKill(t *testing.T) {
	opts := DefaultSmartRestartOptions()

	if opts.HardKill {
		t.Error("DefaultSmartRestartOptions().HardKill should be false")
	}
	if opts.HardKillOnly {
		t.Error("DefaultSmartRestartOptions().HardKillOnly should be false")
	}
}

// TestSplitBySpace tests the splitBySpace helper.
func TestSplitBySpace(t *testing.T) {
	tests := []struct {
		input string
		want  []string
	}{
		{"one two three", []string{"one", "two", "three"}},
		{"  spaced   out  ", []string{"spaced", "out"}},
		{"single", []string{"single"}},
		{"", nil},
		{"\t\ttabs\t\there\t", []string{"tabs", "here"}},
		{"2 12345", []string{"2", "12345"}}, // Like tmux list-panes output
	}

	for _, tt := range tests {
		got := splitBySpace(tt.input)
		if len(got) != len(tt.want) {
			t.Errorf("splitBySpace(%q) = %v, want %v", tt.input, got, tt.want)
			continue
		}
		for i := range got {
			if got[i] != tt.want[i] {
				t.Errorf("splitBySpace(%q)[%d] = %q, want %q", tt.input, i, got[i], tt.want[i])
			}
		}
	}
}
