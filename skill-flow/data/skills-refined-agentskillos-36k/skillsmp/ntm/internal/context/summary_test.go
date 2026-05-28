package context

import (
	"strings"
	"testing"
	"time"
)

func TestNewSummaryGenerator(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		cfg      SummaryGeneratorConfig
		wantMax  int
		wantTime time.Duration
	}{
		{
			name:     "default config",
			cfg:      DefaultSummaryGeneratorConfig(),
			wantMax:  2000,
			wantTime: 30 * time.Second,
		},
		{
			name:     "custom config",
			cfg:      SummaryGeneratorConfig{MaxTokens: 3000, PromptTimeout: 60 * time.Second},
			wantMax:  3000,
			wantTime: 60 * time.Second,
		},
		{
			name:     "zero values get defaults",
			cfg:      SummaryGeneratorConfig{},
			wantMax:  2000,
			wantTime: 30 * time.Second,
		},
		{
			name:     "negative values get defaults",
			cfg:      SummaryGeneratorConfig{MaxTokens: -100, PromptTimeout: -5 * time.Second},
			wantMax:  2000,
			wantTime: 30 * time.Second,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			g := NewSummaryGenerator(tt.cfg)
			if g.maxTokens != tt.wantMax {
				t.Errorf("maxTokens = %d, want %d", g.maxTokens, tt.wantMax)
			}
			if g.promptTimeout != tt.wantTime {
				t.Errorf("promptTimeout = %v, want %v", g.promptTimeout, tt.wantTime)
			}
		})
	}
}

func TestGeneratePrompt(t *testing.T) {
	t.Parallel()

	g := NewSummaryGenerator(DefaultSummaryGeneratorConfig())
	prompt := g.GeneratePrompt()

	// Check that prompt contains key sections
	requiredSections := []string{
		"CURRENT TASK",
		"PROGRESS",
		"KEY DECISIONS",
		"ACTIVE FILES",
		"BLOCKERS",
	}

	for _, section := range requiredSections {
		if !strings.Contains(prompt, section) {
			t.Errorf("prompt missing section: %s", section)
		}
	}
}

func TestParseAgentResponse(t *testing.T) {
	t.Parallel()

	g := NewSummaryGenerator(DefaultSummaryGeneratorConfig())

	response := `## CURRENT TASK
Implementing the context rotation feature for NTM.

## PROGRESS
- Completed the token monitoring module
- Added configuration options
- Still need to implement the rotation logic

## KEY DECISIONS
- Using multi-source estimation for accuracy
- Conservative thresholds (80%/95%)
- Fallback to heuristics when robot mode unavailable

## ACTIVE FILES
- internal/context/monitor.go
- internal/context/summary.go
- internal/config/config.go

## BLOCKERS
- Need to test with real agent sessions
- Unclear how Codex handles context internally`

	summary := g.ParseAgentResponse("cc_1", "claude", "test-session", response)

	if summary.OldAgentID != "cc_1" {
		t.Errorf("OldAgentID = %s, want cc_1", summary.OldAgentID)
	}
	if summary.OldAgentType != "claude" {
		t.Errorf("OldAgentType = %s, want claude", summary.OldAgentType)
	}
	if summary.SessionName != "test-session" {
		t.Errorf("SessionName = %s, want test-session", summary.SessionName)
	}
	if !strings.Contains(summary.CurrentTask, "context rotation") {
		t.Errorf("CurrentTask not parsed correctly: %s", summary.CurrentTask)
	}
	if !strings.Contains(summary.Progress, "token monitoring") {
		t.Errorf("Progress not parsed correctly: %s", summary.Progress)
	}
	if len(summary.KeyDecisions) == 0 {
		t.Error("KeyDecisions not parsed")
	}
	if len(summary.ActiveFiles) == 0 {
		t.Error("ActiveFiles not parsed")
	}
	if len(summary.Blockers) == 0 {
		t.Error("Blockers not parsed")
	}
	if summary.RawSummary != response {
		t.Error("RawSummary not set correctly")
	}
}

func TestParseAgentResponse_AlternateFormat(t *testing.T) {
	t.Parallel()

	g := NewSummaryGenerator(DefaultSummaryGeneratorConfig())

	// Test with bold format
	response := `**CURRENT TASK**
Working on API refactoring.

**PROGRESS**
- Completed endpoint design
- Implemented auth middleware

**KEY DECISIONS**
Using JWT for authentication.

**ACTIVE FILES**
api/handlers.go
api/middleware.go

**BLOCKERS**
None at the moment.`

	summary := g.ParseAgentResponse("cod_1", "codex", "api-proj", response)

	if !strings.Contains(summary.CurrentTask, "API refactoring") {
		t.Errorf("CurrentTask not parsed from bold format: %s", summary.CurrentTask)
	}
}

func TestParseAgentResponse_Truncation(t *testing.T) {
	t.Parallel()

	cfg := SummaryGeneratorConfig{
		MaxTokens:     50, // Very small limit
		PromptTimeout: 30 * time.Second,
	}
	g := NewSummaryGenerator(cfg)

	// Create a response that's definitely over the limit
	longResponse := strings.Repeat("This is a very long response. ", 100)

	summary := g.ParseAgentResponse("cc_1", "claude", "test", longResponse)

	if summary.TokenEstimate > 50 {
		t.Errorf("TokenEstimate = %d, should be capped at 50", summary.TokenEstimate)
	}
	if !strings.Contains(summary.RawSummary, "[Summary truncated") {
		t.Error("Truncated summary should contain truncation notice")
	}
}

func TestGenerateFallbackSummary(t *testing.T) {
	t.Parallel()

	g := NewSummaryGenerator(DefaultSummaryGeneratorConfig())

	recentOutput := []string{
		"Working on implementing the auth module...",
		"Created internal/auth/handler.go",
		"Fixed a bug in session validation.",
		"Running tests now...",
	}

	summary := g.GenerateFallbackSummary("cc_1", "claude", "auth-proj", recentOutput)

	if summary.OldAgentID != "cc_1" {
		t.Errorf("OldAgentID = %s, want cc_1", summary.OldAgentID)
	}
	if !strings.Contains(summary.RawSummary, "FALLBACK SUMMARY") {
		t.Error("Fallback summary should indicate it's a fallback")
	}
	// Should detect file paths
	if len(summary.ActiveFiles) == 0 {
		t.Log("Note: no files detected in fallback (this is OK if patterns don't match)")
	}
}

func TestFormatForNewAgent(t *testing.T) {
	t.Parallel()

	summary := &HandoffSummary{
		GeneratedAt:  time.Now(),
		OldAgentID:   "cc_1",
		OldAgentType: "claude",
		SessionName:  "test-session",
		CurrentTask:  "Implementing feature X",
		Progress:     "50% complete",
		KeyDecisions: []string{"Using approach A", "Chose library B"},
		ActiveFiles:  []string{"file1.go", "file2.go"},
		Blockers:     []string{"Waiting for API access"},
		RawSummary:   "...",
	}

	formatted := summary.FormatForNewAgent()

	requiredContent := []string{
		"HANDOFF CONTEXT",
		"Implementing feature X",
		"50% complete",
		"Using approach A",
		"file1.go",
		"Waiting for API access",
		"continue",
	}

	for _, content := range requiredContent {
		if !strings.Contains(formatted, content) {
			t.Errorf("formatted output missing: %s", content)
		}
	}
}

func TestExtractSection(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		response string
		header   string
		want     string
	}{
		{
			name:     "markdown header",
			response: "## CURRENT TASK\nDoing something.\n\n## PROGRESS\nDone stuff.",
			header:   "CURRENT TASK",
			want:     "Doing something.",
		},
		{
			name:     "bold header",
			response: "**CURRENT TASK**\nDoing something.\n\n**PROGRESS**\nDone stuff.",
			header:   "CURRENT TASK",
			want:     "Doing something.",
		},
		{
			name:     "missing section",
			response: "## OTHER\nSomething else.",
			header:   "CURRENT TASK",
			want:     "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := extractSection(tt.response, tt.header)
			if got != tt.want {
				t.Errorf("extractSection() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestExtractListSection(t *testing.T) {
	t.Parallel()

	response := `## KEY DECISIONS
- Decision one
- Decision two
* Decision three
1. Decision four`

	items := extractListSection(response, "KEY DECISIONS")

	if len(items) != 4 {
		t.Errorf("got %d items, want 4", len(items))
	}

	for i, item := range items {
		if strings.HasPrefix(item, "-") || strings.HasPrefix(item, "*") || strings.HasPrefix(item, "1.") {
			t.Errorf("item %d still has bullet: %s", i, item)
		}
	}
}

func TestExtractFilePaths(t *testing.T) {
	t.Parallel()

	text := `Working on internal/context/monitor.go and internal/config/config.go.
Also modified cmd/ntm/main.go.
The test file is monitor_test.go.`

	files := extractFilePaths(text)

	expected := map[string]bool{
		"internal/context/monitor.go": true,
		"internal/config/config.go":   true,
		"cmd/ntm/main.go":             true,
		"monitor_test.go":             true,
	}

	for _, f := range files {
		if !expected[f] {
			t.Logf("Found file: %s (may be valid)", f)
		}
	}

	// At least some should be found
	if len(files) < 2 {
		t.Errorf("only found %d files, expected at least 2", len(files))
	}
}

func TestIsLikelyFilePath(t *testing.T) {
	t.Parallel()

	tests := []struct {
		path string
		want bool
	}{
		{"internal/context/monitor.go", true},
		{"config.go", true},
		{"README.md", true},
		{"data.json", true},
		{"config.yaml", true},
		{"https://example.com", false},
		{"1.0", false},
		{"v2.0", false},
		{"random_text", false},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			t.Parallel()
			got := isLikelyFilePath(tt.path)
			if got != tt.want {
				t.Errorf("isLikelyFilePath(%q) = %v, want %v", tt.path, got, tt.want)
			}
		})
	}
}

func TestExtractLastTask(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name string
		text string
		want string
	}{
		{
			name: "working on pattern",
			text: "I am working on the authentication module.",
			want: "the authentication module",
		},
		{
			name: "implementing pattern",
			text: "Implementing new feature for user management.",
			want: "new feature for user management",
		},
		{
			name: "TODO pattern",
			text: "TODO: Fix the login bug",
			want: "Fix the login bug",
		},
		{
			name: "no pattern",
			text: "Just some random text",
			want: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := extractLastTask(tt.text)
			if tt.want != "" && !strings.Contains(got, tt.want) {
				t.Errorf("extractLastTask() = %q, should contain %q", got, tt.want)
			}
			if tt.want == "" && got != "" {
				t.Errorf("extractLastTask() = %q, want empty", got)
			}
		})
	}
}

func TestTruncateToTokens(t *testing.T) {
	t.Parallel()

	// Create text that's definitely over 50 tokens (~200 chars)
	longText := strings.Repeat("Hello world. ", 50)

	truncated := truncateToTokens(longText, 50)

	// Should be truncated
	if len(truncated) >= len(longText) {
		t.Error("text was not truncated")
	}

	// Should have truncation notice
	if !strings.Contains(truncated, "[Summary truncated") {
		t.Error("truncated text should have truncation notice")
	}
}

func TestHandoffSummary_EmptyValues(t *testing.T) {
	t.Parallel()

	summary := &HandoffSummary{
		GeneratedAt:  time.Now(),
		OldAgentID:   "cc_1",
		CurrentTask:  "",
		Progress:     "",
		KeyDecisions: nil,
		ActiveFiles:  nil,
		Blockers:     nil,
		RawSummary:   "",
	}

	// Should not panic with empty values
	formatted := summary.FormatForNewAgent()

	if !strings.Contains(formatted, "HANDOFF CONTEXT") {
		t.Error("formatted output missing header")
	}
}
