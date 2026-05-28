package auth

import "testing"

func TestClaudeAuthFlow_DetectBrowserURL(t *testing.T) {
	flow := NewClaudeAuthFlow(false)

	tests := []struct {
		name   string
		output string
		want   string
		found  bool
	}{
		{
			name:   "standard url",
			output: "Please visit https://claude.ai/login?code=123 to login",
			want:   "https://claude.ai/login?code=123",
			found:  true,
		},
		{
			name:   "no url",
			output: "Just some random text",
			want:   "",
			found:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, found := flow.DetectBrowserURL(tt.output)
			if found != tt.found {
				t.Errorf("DetectBrowserURL() found = %v, want %v", found, tt.found)
			}
			if got != tt.want {
				t.Errorf("DetectBrowserURL() got = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestClaudeAuthFlow_DetectAuthSuccess(t *testing.T) {
	flow := NewClaudeAuthFlow(false)

	tests := []struct {
		name   string
		output string
		want   bool
	}{
		{
			name:   "success message 1",
			output: "Successfully logged in as user",
			want:   true,
		},
		{
			name:   "success message 2",
			output: "Login successful",
			want:   true,
		},
		{
			name:   "failure message",
			output: "Login failed",
			want:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := flow.DetectAuthSuccess(tt.output); got != tt.want {
				t.Errorf("DetectAuthSuccess() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestClaudeAuthFlow_DetectAuthFailure(t *testing.T) {
	flow := NewClaudeAuthFlow(false)

	tests := []struct {
		name   string
		output string
		want   bool
	}{
		{
			name:   "failure message 1",
			output: "Login failed due to error",
			want:   true,
		},
		{
			name:   "failure message 2",
			output: "Authentication failed",
			want:   true,
		},
		{
			name:   "success message",
			output: "Login successful",
			want:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := flow.DetectAuthFailure(tt.output); got != tt.want {
				t.Errorf("DetectAuthFailure() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestClaudeAuthFlow_DetectChallengeCode(t *testing.T) {
	flow := NewClaudeAuthFlow(false)

	tests := []struct {
		name   string
		output string
		want   bool
	}{
		{
			name:   "challenge prompt 1",
			output: "Enter code: ",
			want:   true,
		},
		{
			name:   "challenge prompt 2",
			output: "Please Enter the code from your browser",
			want:   true,
		},
		{
			name:   "no challenge",
			output: "Waiting for browser...",
			want:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, got := flow.DetectChallengeCode(tt.output)
			if got != tt.want {
				t.Errorf("DetectChallengeCode() = %v, want %v", got, tt.want)
			}
		})
	}
}
