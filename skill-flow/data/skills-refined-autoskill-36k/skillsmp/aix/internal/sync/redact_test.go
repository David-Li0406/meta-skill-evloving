package sync

import (
	"strings"
	"testing"
)

func TestRedactSecrets(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		contains string // should NOT contain this after redaction
		redacted bool   // should have been redacted
	}{
		{
			name:     "google_oauth_code",
			input:    "here is my code: 4/0ASc3gC0sGJTRyIEWIP8cFvvWARiVC5Ql-OkNtnapOXJimzMfkGcKnOGD-0JEvIzTrOjVTg",
			contains: "4/0ASc3gC0sGJTRyIEWIP8cFvvWARiVC5Ql",
			redacted: true,
		},
		{
			name:     "google_access_token",
			input:    "token: ya29.a0AUMWg_JMIDQq0Gw9MoSwVVy5bA7ohdFTG4-Cmp9a1cu8PRp8KPRR6rKUXVqe3D-8TmPElZvsMeu8",
			contains: "ya29.a0AUMWg_JMIDQq0Gw9MoSwVVy5bA7ohdFTG4",
			redacted: true,
		},
		{
			name:     "gemini_api_key",
			input:    "key=AQ.Ab8RN6LWqknkGWQYJq_oTJ7LfIMQ7whPeS3uGvgK5Y8TYTiK0g",
			contains: "AQ.Ab8RN6LWqknkGWQYJq_oTJ7LfIMQ7whPeS3uGvgK5Y8TYTiK0g",
			redacted: true,
		},
		{
			name:     "openai_key",
			input:    "OPENAI_API_KEY=sk-proj-abc123xyz789defghijklmnopqrstuvwxyz",
			contains: "sk-proj-abc123xyz789defghijklmnopqrstuvwxyz",
			redacted: true,
		},
		{
			name:     "github_pat",
			input:    "export GITHUB_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz1234567890",
			contains: "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
			redacted: true,
		},
		{
			name:     "normal_uuid_not_redacted",
			input:    "session_id: 550e8400-e29b-41d4-a716-446655440000",
			contains: "550e8400-e29b-41d4-a716-446655440000",
			redacted: false,
		},
		{
			name:     "file_path_not_redacted",
			input:    "/Users/tyler/Desktop/projects/myapp/internal/config/config.go",
			contains: "/Users/tyler/Desktop/projects/myapp/internal/config/config.go",
			redacted: false,
		},
		{
			name:     "git_sha_not_redacted",
			input:    "commit: 9e5650601abcdef1234567890abcdef123456789",
			contains: "9e5650601abcdef1234567890abcdef123456789",
			redacted: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := RedactSecrets(tt.input)

			if tt.redacted {
				if strings.Contains(result, tt.contains) {
					t.Errorf("expected %q to be redacted, but found in result: %s", tt.contains, result)
				}
				if !strings.Contains(result, RedactionPlaceholder) {
					t.Errorf("expected [REDACTED] placeholder in result: %s", result)
				}
			} else {
				if !strings.Contains(result, tt.contains) {
					t.Errorf("expected %q to NOT be redacted, but it was: %s", tt.contains, result)
				}
			}
		})
	}
}

func TestShannonEntropy(t *testing.T) {
	tests := []struct {
		input    string
		minEntropy float64
		maxEntropy float64
	}{
		{"aaaaaaaaaa", 0, 0.1},                           // Very low entropy (repeated char)
		{"abcdefghij", 3.0, 3.5},                         // Medium entropy (sequential)
		{"aB3$kL9@mN", 3.0, 4.0},                         // Higher entropy (mixed)
		{"Kj8#mNp2$QrS4tUv", 3.5, 4.5},                   // High entropy (password-like)
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			entropy := shannonEntropy(tt.input)
			if entropy < tt.minEntropy || entropy > tt.maxEntropy {
				t.Errorf("entropy of %q = %.2f, expected between %.2f and %.2f",
					tt.input, entropy, tt.minEntropy, tt.maxEntropy)
			}
		})
	}
}
