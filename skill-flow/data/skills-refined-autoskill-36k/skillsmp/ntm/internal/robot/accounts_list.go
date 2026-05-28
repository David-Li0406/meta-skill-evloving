package robot

import (
	"context"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tools"
)

// AccountsListOutput represents the response from --robot-accounts-list
type AccountsListOutput struct {
	RobotResponse
	Accounts []AccountInfo `json:"accounts"`
}

// AccountInfo contains detailed information about a single account
type AccountInfo struct {
	Provider     string  `json:"provider"`
	ID           string  `json:"id"`
	Email        string  `json:"email,omitempty"`
	Name         string  `json:"name,omitempty"`
	Current      bool    `json:"current"`
	UsagePercent int     `json:"usage_percent,omitempty"`
	RateLimited  bool    `json:"rate_limited,omitempty"`
	Cooldown     *string `json:"cooldown"` // nil when no cooldown, RFC3339 string when active
}

// AccountsListOptions contains options for the accounts list command
type AccountsListOptions struct {
	Provider string // Optional filter for a specific provider (claude, openai, gemini)
}

// PrintAccountsList handles the --robot-accounts-list command
// Usage:
//
//	ntm --robot-accounts-list              # List all accounts
//	ntm --robot-accounts-list --provider claude  # List only Claude accounts
func PrintAccountsList(opts AccountsListOptions) error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	adapter := tools.NewCAAMAdapter()

	// Check if CAAM is available
	if _, installed := adapter.Detect(); !installed {
		output := AccountsListOutput{
			RobotResponse: NewErrorResponse(nil, ErrCodeDependencyMissing, "Install caam to manage coding agent accounts"),
			Accounts:      []AccountInfo{}, // Empty array, not nil
		}
		output.Error = "caam not installed"
		return outputJSON(output)
	}

	// Get all accounts from CAAM
	accounts, err := adapter.GetAccounts(ctx)
	if err != nil {
		output := AccountsListOutput{
			RobotResponse: NewErrorResponse(err, ErrCodeInternalError, "Check if caam is configured correctly"),
			Accounts:      []AccountInfo{}, // Empty array, not nil
		}
		return outputJSON(output)
	}

	// Build output
	output := AccountsListOutput{
		RobotResponse: NewRobotResponse(true),
		Accounts:      []AccountInfo{}, // Initialize to empty array
	}

	for _, acc := range accounts {
		// Filter by provider if specified
		if opts.Provider != "" && acc.Provider != opts.Provider {
			continue
		}

		info := AccountInfo{
			Provider:    acc.Provider,
			ID:          acc.ID,
			Email:       acc.Email,
			Name:        acc.Name,
			Current:     acc.Active,
			RateLimited: acc.RateLimited,
		}

		// Set cooldown if present
		if !acc.CooldownUntil.IsZero() {
			cooldownStr := FormatTimestamp(acc.CooldownUntil)
			info.Cooldown = &cooldownStr
		}
		// info.Cooldown is already nil by default when no cooldown

		output.Accounts = append(output.Accounts, info)
	}

	return outputJSON(output)
}
