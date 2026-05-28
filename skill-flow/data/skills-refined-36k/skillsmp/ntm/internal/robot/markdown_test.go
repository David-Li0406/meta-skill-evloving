package robot

import (
	"strings"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/alerts"
)

func TestRenderAgentTable(t *testing.T) {
	rows := []AgentTableRow{
		{Agent: "cc_1", Type: "claude", Status: "active"},
		{Agent: "cod_1", Type: "codex", Status: "idle"},
	}

	out := RenderAgentTable(rows)

	if !strings.HasPrefix(out, "| Agent | Type | Status |") {
		t.Fatalf("missing table header, got:\n%s", out)
	}
	if !strings.Contains(out, "| cc_1 | claude | active |") {
		t.Errorf("missing first row: %s", out)
	}
	if !strings.Contains(out, "| cod_1 | codex | idle |") {
		t.Errorf("missing second row: %s", out)
	}
}

func TestRenderAlertsList(t *testing.T) {
	alerts := []AlertInfo{
		{Severity: "critical", Type: "tmux", Message: "Session dropped", Session: "s1", Pane: "cc_1"},
		{Severity: "warning", Type: "disk", Message: "Low space"},
		{Severity: "info", Type: "beads", Message: "Ready: 5"},
		{Severity: "other", Type: "custom", Message: "Note"},
	}

	out := RenderAlertsList(alerts)

	// Order: Critical before Warning before Info
	critIdx := strings.Index(out, "### Critical")
	warnIdx := strings.Index(out, "### Warning")
	infoIdx := strings.Index(out, "### Info")
	if critIdx == -1 || warnIdx == -1 || infoIdx == -1 {
		t.Fatalf("missing severity headings:\n%s", out)
	}
	if !(critIdx < warnIdx && warnIdx < infoIdx) {
		t.Errorf("severity order wrong: crit=%d warn=%d info=%d", critIdx, warnIdx, infoIdx)
	}

	if !strings.Contains(out, "- [tmux] Session dropped (s1 cc_1)") {
		t.Errorf("missing critical item formatting: %s", out)
	}
	if !strings.Contains(out, "- [disk] Low space") {
		t.Errorf("missing warning item: %s", out)
	}
	if !strings.Contains(out, "### Other") || !strings.Contains(out, "[custom] Note") {
		t.Errorf("missing other bucket: %s", out)
	}
}

func TestRenderSuggestedActions(t *testing.T) {
	actions := []SuggestedAction{
		{Title: "Fix tmux", Reason: "session drops"},
		{Title: "Trim logs", Reason: ""},
	}
	out := RenderSuggestedActions(actions)

	if !strings.HasPrefix(out, "1. Fix tmux — session drops") {
		t.Fatalf("unexpected first line: %s", out)
	}
	if !strings.Contains(out, "2. Trim logs") {
		t.Errorf("second action missing: %s", out)
	}
}

func TestDefaultMarkdownOptions(t *testing.T) {
	opts := DefaultMarkdownOptions()

	if opts.MaxBeads != 5 {
		t.Errorf("expected MaxBeads=5, got %d", opts.MaxBeads)
	}
	if opts.MaxAlerts != 10 {
		t.Errorf("expected MaxAlerts=10, got %d", opts.MaxAlerts)
	}
	if opts.Compact {
		t.Error("expected Compact=false by default")
	}
	if opts.Session != "" {
		t.Errorf("expected empty Session, got %q", opts.Session)
	}
}

func TestTruncateStr(t *testing.T) {
	tests := []struct {
		input  string
		maxLen int
		want   string
	}{
		{"hello", 10, "hello"},
		{"hello world", 5, "he..."},
		{"ab", 3, "ab"},
		{"abcd", 3, "abc"},
		{"", 5, ""},
	}

	for _, tc := range tests {
		got := truncateStr(tc.input, tc.maxLen)
		if got != tc.want {
			t.Errorf("truncateStr(%q, %d) = %q, want %q", tc.input, tc.maxLen, got, tc.want)
		}
	}
}

func TestAlertSeverityOrder(t *testing.T) {
	tests := []struct {
		severity alerts.Severity
		want     int
	}{
		{alerts.SeverityCritical, 0},
		{alerts.SeverityWarning, 1},
		{alerts.SeverityInfo, 2},
		{alerts.Severity("unknown"), 2},
	}

	for _, tc := range tests {
		got := alertSeverityOrder(tc.severity)
		if got != tc.want {
			t.Errorf("alertSeverityOrder(%v) = %d, want %d", tc.severity, got, tc.want)
		}
	}
}

func TestAlertSeverityIcon(t *testing.T) {
	tests := []struct {
		severity alerts.Severity
		want     string
	}{
		{alerts.SeverityCritical, "🔴"},
		{alerts.SeverityWarning, "⚠️"},
		{alerts.SeverityInfo, "ℹ️"},
		{alerts.Severity("other"), "ℹ️"},
	}

	for _, tc := range tests {
		got := alertSeverityIcon(tc.severity)
		if got != tc.want {
			t.Errorf("alertSeverityIcon(%v) = %q, want %q", tc.severity, got, tc.want)
		}
	}
}
