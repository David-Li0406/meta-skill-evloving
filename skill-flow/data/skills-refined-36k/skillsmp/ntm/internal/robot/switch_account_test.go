package robot

import (
	"testing"
	"time"
)

// =============================================================================
// Unit Tests for --robot-switch-account (bd-1tmw5)
// =============================================================================

// TestParseSwitchAccountArg tests parsing of provider and provider:account formats.
func TestParseSwitchAccountArg(t *testing.T) {
	tests := []struct {
		name         string
		arg          string
		wantProvider string
		wantAccount  string
	}{
		{
			name:         "provider only - claude",
			arg:          "claude",
			wantProvider: "claude",
			wantAccount:  "",
		},
		{
			name:         "provider only - openai",
			arg:          "openai",
			wantProvider: "openai",
			wantAccount:  "",
		},
		{
			name:         "provider only - gemini",
			arg:          "gemini",
			wantProvider: "gemini",
			wantAccount:  "",
		},
		{
			name:         "provider:account format",
			arg:          "claude:account-123",
			wantProvider: "claude",
			wantAccount:  "account-123",
		},
		{
			name:         "provider:account with special chars",
			arg:          "openai:my-org_team@123",
			wantProvider: "openai",
			wantAccount:  "my-org_team@123",
		},
		{
			name:         "empty string",
			arg:          "",
			wantProvider: "",
			wantAccount:  "",
		},
		{
			name:         "account with colons",
			arg:          "gemini:acc:with:colons",
			wantProvider: "gemini",
			wantAccount:  "acc:with:colons",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			opts := ParseSwitchAccountArg(tt.arg)
			if opts.Provider != tt.wantProvider {
				t.Errorf("Provider = %q, want %q", opts.Provider, tt.wantProvider)
			}
			if opts.AccountID != tt.wantAccount {
				t.Errorf("AccountID = %q, want %q", opts.AccountID, tt.wantAccount)
			}
		})
	}
}

// TestCooldownSeconds tests cooldown calculation from expiry time.
func TestCooldownSeconds(t *testing.T) {
	tests := []struct {
		name          string
		cooldownUntil time.Time
		wantZero      bool
		wantPositive  bool
	}{
		{
			name:          "zero time - returns 0",
			cooldownUntil: time.Time{},
			wantZero:      true,
		},
		{
			name:          "past time - returns 0",
			cooldownUntil: time.Now().Add(-1 * time.Hour),
			wantZero:      true,
		},
		{
			name:          "future time - returns positive",
			cooldownUntil: time.Now().Add(30 * time.Second),
			wantPositive:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := cooldownSeconds(tt.cooldownUntil)
			if tt.wantZero && result != 0 {
				t.Errorf("cooldownSeconds() = %d, want 0", result)
			}
			if tt.wantPositive && result <= 0 {
				t.Errorf("cooldownSeconds() = %d, want > 0", result)
			}
		})
	}
}

// TestSwitchAccountResultStruct tests JSON struct fields.
func TestSwitchAccountResultStruct(t *testing.T) {
	result := SwitchAccountResult{
		Success:         true,
		Provider:        "claude",
		PreviousAccount: "old-account",
		NewAccount:      "new-account",
		PanesAffected:   []string{"agent-1", "agent-2"},
		CooldownSeconds: 300,
	}

	if !result.Success {
		t.Error("Success should be true")
	}
	if result.Provider != "claude" {
		t.Errorf("Provider = %q, want %q", result.Provider, "claude")
	}
	if len(result.PanesAffected) != 2 {
		t.Errorf("PanesAffected len = %d, want 2", len(result.PanesAffected))
	}
}

// TestSwitchAccountResultWithError tests error field usage.
func TestSwitchAccountResultWithError(t *testing.T) {
	result := SwitchAccountResult{
		Success:  false,
		Provider: "openai",
		Error:    "rate limited",
	}

	if result.Success {
		t.Error("Success should be false")
	}
	if result.Error != "rate limited" {
		t.Errorf("Error = %q, want %q", result.Error, "rate limited")
	}
}

// TestSwitchAccountOptions tests options struct.
func TestSwitchAccountOptions(t *testing.T) {
	opts := SwitchAccountOptions{
		Provider:  "claude",
		AccountID: "acc-123",
		Pane:      "agent-1",
	}

	if opts.Provider != "claude" {
		t.Errorf("Provider = %q, want %q", opts.Provider, "claude")
	}
	if opts.AccountID != "acc-123" {
		t.Errorf("AccountID = %q, want %q", opts.AccountID, "acc-123")
	}
	if opts.Pane != "agent-1" {
		t.Errorf("Pane = %q, want %q", opts.Pane, "agent-1")
	}
}

// TestSwitchAccountOutputStruct tests JSON wrapper struct.
func TestSwitchAccountOutputStruct(t *testing.T) {
	output := SwitchAccountOutput{
		Switch: SwitchAccountResult{
			Success:    true,
			Provider:   "gemini",
			NewAccount: "my-new-account",
		},
	}

	if !output.Switch.Success {
		t.Error("Switch.Success should be true")
	}
	if output.Switch.Provider != "gemini" {
		t.Errorf("Switch.Provider = %q, want %q", output.Switch.Provider, "gemini")
	}
}
