package robot

import (
	"context"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/integrations/caut"
	"github.com/Dicklesworthstone/ntm/internal/tools"
)

// QuotaStatusOutput represents the response from --robot-quota-status
type QuotaStatusOutput struct {
	RobotResponse
	Quota QuotaInfo `json:"quota"`
}

// QuotaInfo contains quota and usage information from caut
type QuotaInfo struct {
	LastUpdated    string                   `json:"last_updated"`
	CautAvailable  bool                     `json:"caut_available"`
	Providers      map[string]ProviderQuota `json:"providers"`
	TotalCostToday float64                  `json:"total_cost_today_usd"`
	TotalCostMonth float64                  `json:"total_cost_month_usd,omitempty"`
	HasWarning     bool                     `json:"has_warning"`
	HasCritical    bool                     `json:"has_critical"`
}

// ProviderQuota contains quota information for a single provider
type ProviderQuota struct {
	UsagePercent  float64 `json:"usage_percent"`
	RequestsUsed  int     `json:"requests_used,omitempty"`
	RequestsLimit int     `json:"requests_limit,omitempty"`
	TokensUsed    int64   `json:"tokens_used,omitempty"`
	TokensLimit   int64   `json:"tokens_limit,omitempty"`
	CostUSD       float64 `json:"cost_usd"`
	ResetAt       string  `json:"reset_at,omitempty"`
	Status        string  `json:"status"` // "ok", "warning", "critical"
}

// QuotaCheckOutput represents the response from --robot-quota-check
type QuotaCheckOutput struct {
	RobotResponse
	Provider string        `json:"provider"`
	Quota    ProviderQuota `json:"quota"`
}

// PrintQuotaStatus handles the --robot-quota-status command
// Usage:
//
//	ntm --robot-quota-status
func PrintQuotaStatus() error {
	poller := caut.GetGlobalPoller()
	cache := poller.GetCache()

	// Check if caut is available
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	adapter := tools.NewCautAdapter()
	available := adapter.IsAvailable(ctx)

	quotaInfo := QuotaInfo{
		LastUpdated:   FormatTimestamp(cache.GetLastUpdated()),
		CautAvailable: available,
		Providers:     make(map[string]ProviderQuota),
	}

	// Get cached status
	status := cache.GetStatus()
	if status != nil {
		quotaInfo.TotalCostToday = status.TotalSpend

		// Check for warnings/critical based on overall quota
		if status.QuotaPercent >= 95.0 {
			quotaInfo.HasCritical = true
		} else if status.QuotaPercent >= 80.0 {
			quotaInfo.HasWarning = true
		}

		// Add per-provider quota info from status
		for _, p := range status.Providers {
			if !p.Enabled {
				continue
			}

			providerQuota := ProviderQuota{
				UsagePercent: p.QuotaUsed,
				Status:       getQuotaStatus(p.QuotaUsed),
			}

			quotaInfo.Providers[p.Name] = providerQuota

			// Track warning/critical at provider level
			if p.QuotaUsed >= 95.0 {
				quotaInfo.HasCritical = true
			} else if p.QuotaUsed >= 80.0 {
				quotaInfo.HasWarning = true
			}
		}
	}

	// Add usage data from cache
	usages := cache.GetAllUsage()
	for _, usage := range usages {
		providerQuota, exists := quotaInfo.Providers[usage.Provider]
		if !exists {
			providerQuota = ProviderQuota{
				Status: "ok",
			}
		}

		providerQuota.RequestsUsed = usage.RequestCount
		providerQuota.TokensUsed = usage.TokensIn + usage.TokensOut
		providerQuota.CostUSD = usage.Cost

		quotaInfo.Providers[usage.Provider] = providerQuota
	}

	// Check for cache errors
	if err, errTime := cache.GetLastError(); err != nil && !errTime.IsZero() {
		output := QuotaStatusOutput{
			RobotResponse: NewErrorResponse(err, ErrCodeInternalError, "caut polling error - data may be stale"),
			Quota:         quotaInfo,
		}
		// Still include the data even with error
		output.Success = true // Partial success
		return outputJSON(output)
	}

	output := QuotaStatusOutput{
		RobotResponse: NewRobotResponse(true),
		Quota:         quotaInfo,
	}

	return outputJSON(output)
}

// PrintQuotaCheck handles the --robot-quota-check command
// Usage:
//
//	ntm --robot-quota-check claude
func PrintQuotaCheck(provider string) error {
	if provider == "" {
		return RobotError(
			nil,
			ErrCodeInvalidFlag,
			"Specify a provider with --quota-check-provider=<name>",
		)
	}

	poller := caut.GetGlobalPoller()
	cache := poller.GetCache()

	// Get provider-specific usage
	usage := cache.GetUsage(provider)
	if usage == nil {
		// Try to get from status providers
		status := cache.GetStatus()
		if status != nil {
			for _, p := range status.Providers {
				if p.Name == provider {
					output := QuotaCheckOutput{
						RobotResponse: NewRobotResponse(true),
						Provider:      provider,
						Quota: ProviderQuota{
							UsagePercent: p.QuotaUsed,
							Status:       getQuotaStatus(p.QuotaUsed),
						},
					}
					return outputJSON(output)
				}
			}
		}

		return RobotError(
			nil,
			ErrCodePaneNotFound, // Reusing as "not found"
			"Provider '"+provider+"' not found. Use --robot-quota-status to see available providers.",
		)
	}

	// Build provider quota from usage data
	providerQuota := ProviderQuota{
		RequestsUsed: usage.RequestCount,
		TokensUsed:   usage.TokensIn + usage.TokensOut,
		CostUSD:      usage.Cost,
		Status:       "ok",
	}

	// Check status for quota percentage
	status := cache.GetStatus()
	if status != nil {
		for _, p := range status.Providers {
			if p.Name == provider {
				providerQuota.UsagePercent = p.QuotaUsed
				providerQuota.Status = getQuotaStatus(p.QuotaUsed)
				break
			}
		}
	}

	output := QuotaCheckOutput{
		RobotResponse: NewRobotResponse(true),
		Provider:      provider,
		Quota:         providerQuota,
	}

	return outputJSON(output)
}

// getQuotaStatus returns the status string based on usage percentage
func getQuotaStatus(usagePercent float64) string {
	switch {
	case usagePercent >= 95.0:
		return "critical"
	case usagePercent >= 80.0:
		return "warning"
	default:
		return "ok"
	}
}
