package cli

import "testing"

func TestParseAgentSpec_ModelValidation(t *testing.T) {
	tests := []struct {
		value       string
		expectError bool
	}{
		{"1:claude-3-opus", false},
		{"2:gpt-4.1", false},
		{"1:vendor/model@2025", false},
		{"1:bad model", true},
		{"1:$(touch /tmp/pwn)", true},
		{"1:;rm -rf /", true},
	}

	for _, tt := range tests {
		_, err := ParseAgentSpec(tt.value)
		if tt.expectError && err == nil {
			t.Fatalf("expected error for %q", tt.value)
		}
		if !tt.expectError && err != nil {
			t.Fatalf("unexpected error for %q: %v", tt.value, err)
		}
	}
}
