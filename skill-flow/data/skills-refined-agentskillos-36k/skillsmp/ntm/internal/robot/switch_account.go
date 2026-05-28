package robot

import (
	"context"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tools"
)

// SwitchAccountOutput represents the response from --robot-switch-account
type SwitchAccountOutput struct {
	Switch SwitchAccountResult `json:"switch"`
}

// SwitchAccountResult contains the switch operation result
type SwitchAccountResult struct {
	Success         bool     `json:"success"`
	Provider        string   `json:"provider"`
	PreviousAccount string   `json:"previous_account,omitempty"`
	NewAccount      string   `json:"new_account,omitempty"`
	PanesAffected   []string `json:"panes_affected,omitempty"`
	CooldownSeconds int      `json:"cooldown_seconds,omitempty"`
	Error           string   `json:"error,omitempty"`
}

// SwitchAccountOptions contains options for the switch account command
type SwitchAccountOptions struct {
	Provider  string // claude, openai, gemini
	AccountID string // Optional specific account to switch to
	Pane      string // Optional pane filter
}

// PrintSwitchAccount handles the --robot-switch-account command
// Usage:
//
//	ntm --robot-switch-account claude         # Switch to next Claude account
//	ntm --robot-switch-account openai:acc123  # Switch to specific account
//	ntm --robot-switch-account claude --pane agent-1  # Switch for specific pane
func PrintSwitchAccount(opts SwitchAccountOptions) error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	adapter := tools.NewCAAMAdapter()

	// Check if CAAM is available
	if _, installed := adapter.Detect(); !installed {
		output := SwitchAccountOutput{
			Switch: SwitchAccountResult{
				Success:  false,
				Provider: opts.Provider,
				Error:    "caam not installed",
			},
		}
		return encodeJSON(output)
	}

	// Get current account before switch (for comparison)
	creds, _ := adapter.GetCurrentCredentials(ctx, opts.Provider)
	previousAccount := ""
	if creds != nil {
		previousAccount = creds.AccountID
	}

	var result *tools.SwitchResult
	var err error

	if opts.AccountID != "" {
		// Switch to specific account
		err = adapter.SwitchAccount(ctx, opts.AccountID)
		if err == nil {
			result = &tools.SwitchResult{
				Success:         true,
				Provider:        opts.Provider,
				PreviousAccount: previousAccount,
				NewAccount:      opts.AccountID,
			}
		}
	} else {
		// Switch to next available account
		result, err = adapter.SwitchToNextAccount(ctx, opts.Provider)
	}

	output := SwitchAccountOutput{
		Switch: SwitchAccountResult{
			Provider:        opts.Provider,
			PreviousAccount: previousAccount,
		},
	}

	if err != nil {
		output.Switch.Success = false
		output.Switch.Error = err.Error()
		return encodeJSON(output)
	}

	if result != nil {
		output.Switch.Success = result.Success
		output.Switch.NewAccount = result.NewAccount
		if result.PreviousAccount != "" {
			output.Switch.PreviousAccount = result.PreviousAccount
		}
		output.Switch.CooldownSeconds = cooldownSeconds(result.CooldownUntil)
	}

	// TODO: If pane filter specified, track which panes would be affected
	// For now, leave PanesAffected empty (would need pane tracking)
	if opts.Pane != "" {
		output.Switch.PanesAffected = []string{opts.Pane}
	}

	return encodeJSON(output)
}

// cooldownSeconds calculates seconds until cooldown expires
func cooldownSeconds(cooldownUntil time.Time) int {
	if cooldownUntil.IsZero() {
		return 0
	}
	remaining := time.Until(cooldownUntil)
	if remaining <= 0 {
		return 0
	}
	return int(remaining.Seconds())
}

// ParseSwitchAccountArg parses the argument format "provider" or "provider:account"
func ParseSwitchAccountArg(arg string) SwitchAccountOptions {
	opts := SwitchAccountOptions{}

	// Handle "provider:account" format
	for i := 0; i < len(arg); i++ {
		if arg[i] == ':' {
			opts.Provider = arg[:i]
			opts.AccountID = arg[i+1:]
			return opts
		}
	}

	// Just provider
	opts.Provider = arg
	return opts
}
