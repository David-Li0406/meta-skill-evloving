package cli

import "testing"

func TestTruncateCassText(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		maxLen   int
		expected string
	}{
		{
			name:     "short string unchanged",
			input:    "hello world",
			maxLen:   20,
			expected: "hello world",
		},
		{
			name:     "long string truncated",
			input:    "this is a very long string that exceeds the limit",
			maxLen:   20,
			expected: "this is a very lo...",
		},
		{
			name:     "exact length unchanged",
			input:    "exactly twenty chars",
			maxLen:   20,
			expected: "exactly twenty chars",
		},
		{
			name:     "newlines replaced with spaces",
			input:    "line one\nline two",
			maxLen:   30,
			expected: "line one line two",
		},
		{
			name:     "whitespace trimmed",
			input:    "  hello world  ",
			maxLen:   20,
			expected: "hello world",
		},
		{
			name:     "newlines and truncation combined",
			input:    "first\nsecond\nthird\nfourth line here",
			maxLen:   20,
			expected: "first second thir...",
		},
		{
			name:     "maxLen zero returns empty",
			input:    "hello",
			maxLen:   0,
			expected: "",
		},
		{
			name:     "maxLen negative returns empty",
			input:    "hello",
			maxLen:   -5,
			expected: "",
		},
		{
			name:     "maxLen 1 truncates without ellipsis",
			input:    "hello",
			maxLen:   1,
			expected: "h",
		},
		{
			name:     "maxLen 3 truncates without ellipsis",
			input:    "hello",
			maxLen:   3,
			expected: "hel",
		},
		{
			name:     "maxLen 3 with short string unchanged",
			input:    "hi",
			maxLen:   3,
			expected: "hi",
		},
		{
			name:     "maxLen 4 uses ellipsis",
			input:    "hello world",
			maxLen:   4,
			expected: "h...",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := truncateCassText(tt.input, tt.maxLen)
			if result != tt.expected {
				t.Errorf("truncateCassText(%q, %d) = %q; want %q",
					tt.input, tt.maxLen, result, tt.expected)
			}
		})
	}
}

func TestExtractSessionNameFromPath(t *testing.T) {
	tests := []struct {
		name     string
		path     string
		expected string
	}{
		{
			name:     "empty path",
			path:     "",
			expected: "unknown",
		},
		{
			name:     "simple filename",
			path:     "/path/to/session.jsonl",
			expected: "session",
		},
		{
			name:     "json extension",
			path:     "/path/to/session.json",
			expected: "session",
		},
		{
			name:     "no extension",
			path:     "/path/to/session_name",
			expected: "session_name",
		},
		{
			name:     "path ending with slash",
			path:     "/path/to/dir/",
			expected: "unknown",
		},
		{
			name:     "long filename truncated",
			path:     "/path/to/this_is_a_very_long_session_name_that_exceeds_forty_chars.jsonl",
			expected: "this_is_a_very_long_session_name_that...",
		},
		{
			name:     "date-based path",
			path:     "/sessions/2025/01/05/claude-ntm-project.jsonl",
			expected: "claude-ntm-project",
		},
		{
			name:     "windows-style path",
			path:     "C:/Users/test/sessions/session.jsonl",
			expected: "session",
		},
		{
			name:     "filename is just extension jsonl",
			path:     "/path/to/.jsonl",
			expected: "unknown",
		},
		{
			name:     "filename is just extension json",
			path:     "/path/to/.json",
			expected: "unknown",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := extractSessionNameFromPath(tt.path)
			if result != tt.expected {
				t.Errorf("extractSessionNameFromPath(%q) = %q; want %q",
					tt.path, result, tt.expected)
			}
		})
	}
}

func TestNewCassPreviewCmd(t *testing.T) {
	cmd := newCassPreviewCmd()

	// Verify command structure
	if cmd.Use != "preview <prompt>" {
		t.Errorf("Use = %q; want %q", cmd.Use, "preview <prompt>")
	}
	if cmd.Short == "" {
		t.Error("Short description is empty")
	}
	if cmd.Long == "" {
		t.Error("Long description is empty")
	}

	// Verify flags exist
	flags := []string{"max-results", "max-age", "format", "max-tokens"}
	for _, flag := range flags {
		if cmd.Flags().Lookup(flag) == nil {
			t.Errorf("Flag %q not found", flag)
		}
	}

	// Verify default values
	maxResults, _ := cmd.Flags().GetInt("max-results")
	if maxResults != 5 {
		t.Errorf("max-results default = %d; want 5", maxResults)
	}

	maxAge, _ := cmd.Flags().GetInt("max-age")
	if maxAge != 30 {
		t.Errorf("max-age default = %d; want 30", maxAge)
	}

	format, _ := cmd.Flags().GetString("format")
	if format != "markdown" {
		t.Errorf("format default = %q; want %q", format, "markdown")
	}

	maxTokens, _ := cmd.Flags().GetInt("max-tokens")
	if maxTokens != 500 {
		t.Errorf("max-tokens default = %d; want 500", maxTokens)
	}
}

func TestCassPreviewCmdAddedToParent(t *testing.T) {
	cmd := newCassCmd()

	// Find preview subcommand
	var found bool
	for _, sub := range cmd.Commands() {
		if sub.Name() == "preview" {
			found = true
			break
		}
	}

	if !found {
		t.Error("preview subcommand not found in cass command")
	}
}
