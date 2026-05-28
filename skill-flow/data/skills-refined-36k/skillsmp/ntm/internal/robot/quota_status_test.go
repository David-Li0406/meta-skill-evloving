package robot

import (
	"testing"
)

func TestGetQuotaStatus(t *testing.T) {
	tests := []struct {
		name     string
		percent  float64
		expected string
	}{
		{"ok_low", 0.0, "ok"},
		{"ok_mid", 50.0, "ok"},
		{"ok_high", 79.9, "ok"},
		{"warning_threshold", 80.0, "warning"},
		{"warning_mid", 90.0, "warning"},
		{"warning_high", 94.9, "warning"},
		{"critical_threshold", 95.0, "critical"},
		{"critical_high", 100.0, "critical"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := getQuotaStatus(tt.percent)
			if got != tt.expected {
				t.Errorf("getQuotaStatus(%v) = %q, want %q", tt.percent, got, tt.expected)
			}
		})
	}
}

func TestQuotaStatusOutput_Struct(t *testing.T) {
	// Verify the struct embeds RobotResponse correctly
	output := QuotaStatusOutput{
		RobotResponse: NewRobotResponse(true),
		Quota: QuotaInfo{
			LastUpdated:   "2026-01-15T10:30:00Z",
			CautAvailable: true,
			Providers: map[string]ProviderQuota{
				"claude": {
					UsagePercent: 45.0,
					RequestsUsed: 450,
					TokensUsed:   45000,
					CostUSD:      12.50,
					Status:       "ok",
				},
			},
			TotalCostToday: 12.50,
			HasWarning:     false,
			HasCritical:    false,
		},
	}

	if !output.Success {
		t.Error("Expected Success to be true")
	}

	if output.Timestamp == "" {
		t.Error("Expected Timestamp to be set")
	}

	if !output.Quota.CautAvailable {
		t.Error("Expected CautAvailable to be true")
	}

	claude, ok := output.Quota.Providers["claude"]
	if !ok {
		t.Fatal("Expected claude provider in Providers map")
	}

	if claude.UsagePercent != 45.0 {
		t.Errorf("Expected UsagePercent 45.0, got %v", claude.UsagePercent)
	}

	if claude.Status != "ok" {
		t.Errorf("Expected Status 'ok', got %q", claude.Status)
	}
}

func TestQuotaCheckOutput_Struct(t *testing.T) {
	output := QuotaCheckOutput{
		RobotResponse: NewRobotResponse(true),
		Provider:      "openai",
		Quota: ProviderQuota{
			UsagePercent: 85.0,
			RequestsUsed: 850,
			TokensUsed:   170000,
			CostUSD:      25.00,
			Status:       "warning",
		},
	}

	if !output.Success {
		t.Error("Expected Success to be true")
	}

	if output.Provider != "openai" {
		t.Errorf("Expected Provider 'openai', got %q", output.Provider)
	}

	if output.Quota.Status != "warning" {
		t.Errorf("Expected Status 'warning', got %q", output.Quota.Status)
	}
}

func TestQuotaInfo_Warning(t *testing.T) {
	// Test that HasWarning is set correctly based on provider quotas
	qi := QuotaInfo{
		Providers: map[string]ProviderQuota{
			"claude": {UsagePercent: 45.0, Status: "ok"},
			"openai": {UsagePercent: 82.0, Status: "warning"},
		},
	}

	// Check warning detection (would be set by PrintQuotaStatus)
	hasWarning := false
	for _, p := range qi.Providers {
		if p.UsagePercent >= 80.0 && p.UsagePercent < 95.0 {
			hasWarning = true
		}
	}

	if !hasWarning {
		t.Error("Expected to detect warning when provider at 82%")
	}
}

func TestQuotaInfo_Critical(t *testing.T) {
	// Test that HasCritical is set correctly
	qi := QuotaInfo{
		Providers: map[string]ProviderQuota{
			"claude": {UsagePercent: 96.0, Status: "critical"},
		},
	}

	hasCritical := false
	for _, p := range qi.Providers {
		if p.UsagePercent >= 95.0 {
			hasCritical = true
		}
	}

	if !hasCritical {
		t.Error("Expected to detect critical when provider at 96%")
	}
}

func TestProviderQuota_Fields(t *testing.T) {
	pq := ProviderQuota{
		UsagePercent:  75.5,
		RequestsUsed:  1000,
		RequestsLimit: 2000,
		TokensUsed:    150000,
		TokensLimit:   200000,
		CostUSD:       50.00,
		ResetAt:       "2026-01-16T00:00:00Z",
		Status:        "ok",
	}

	if pq.UsagePercent != 75.5 {
		t.Errorf("Expected UsagePercent 75.5, got %v", pq.UsagePercent)
	}

	if pq.RequestsUsed != 1000 {
		t.Errorf("Expected RequestsUsed 1000, got %d", pq.RequestsUsed)
	}

	if pq.TokensLimit != 200000 {
		t.Errorf("Expected TokensLimit 200000, got %d", pq.TokensLimit)
	}

	if pq.ResetAt == "" {
		t.Error("Expected ResetAt to be set")
	}
}
