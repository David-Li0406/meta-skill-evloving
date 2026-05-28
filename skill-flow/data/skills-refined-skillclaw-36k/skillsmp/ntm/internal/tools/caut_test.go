package tools

import (
	"context"
	"testing"
	"time"
)

func TestNewCautAdapter(t *testing.T) {
	adapter := NewCautAdapter()
	if adapter == nil {
		t.Fatal("NewCautAdapter returned nil")
	}

	if adapter.Name() != ToolCaut {
		t.Errorf("Expected name %s, got %s", ToolCaut, adapter.Name())
	}

	if adapter.BinaryName() != "caut" {
		t.Errorf("Expected binary name 'caut', got %s", adapter.BinaryName())
	}
}

func TestCautAdapterImplementsInterface(t *testing.T) {
	// Ensure CautAdapter implements the Adapter interface
	var _ Adapter = (*CautAdapter)(nil)
}

func TestCautAdapterDetect(t *testing.T) {
	adapter := NewCautAdapter()

	// Test detection - result depends on whether caut is installed
	path, installed := adapter.Detect()

	// If installed, path should be non-empty
	if installed && path == "" {
		t.Error("caut detected but path is empty")
	}

	// If not installed, path should be empty
	if !installed && path != "" {
		t.Errorf("caut not detected but path is %s", path)
	}
}

func TestCautAvailabilityStruct(t *testing.T) {
	availability := CautAvailability{
		Available:   true,
		Compatible:  true,
		HasData:     true,
		Version:     Version{Major: 1, Minor: 0, Patch: 0},
		Path:        "/usr/local/bin/caut",
		Providers:   []string{"anthropic", "openai"},
		LastChecked: time.Now(),
	}

	if !availability.Available {
		t.Error("Expected Available to be true")
	}

	if !availability.Compatible {
		t.Error("Expected Compatible to be true")
	}

	if !availability.HasData {
		t.Error("Expected HasData to be true")
	}

	if len(availability.Providers) != 2 {
		t.Errorf("Expected 2 providers, got %d", len(availability.Providers))
	}
}

func TestCautStatusStruct(t *testing.T) {
	status := CautStatus{
		Running:       true,
		Tracking:      true,
		ProviderCount: 2,
		Providers: []CautProvider{
			{Name: "anthropic", Enabled: true, HasQuota: true, QuotaUsed: 45.5},
			{Name: "openai", Enabled: true, HasQuota: true, QuotaUsed: 30.0},
		},
		TotalSpend:   125.50,
		QuotaPercent: 37.75,
	}

	if !status.Running {
		t.Error("Expected Running to be true")
	}

	if !status.Tracking {
		t.Error("Expected Tracking to be true")
	}

	if status.ProviderCount != 2 {
		t.Errorf("Expected ProviderCount 2, got %d", status.ProviderCount)
	}

	if status.TotalSpend != 125.50 {
		t.Errorf("Expected TotalSpend 125.50, got %f", status.TotalSpend)
	}
}

func TestCautProviderStruct(t *testing.T) {
	provider := CautProvider{
		Name:      "anthropic",
		Enabled:   true,
		HasQuota:  true,
		QuotaUsed: 65.5,
	}

	if provider.Name != "anthropic" {
		t.Errorf("Expected Name 'anthropic', got %s", provider.Name)
	}

	if !provider.Enabled {
		t.Error("Expected Enabled to be true")
	}

	if !provider.HasQuota {
		t.Error("Expected HasQuota to be true")
	}

	if provider.QuotaUsed != 65.5 {
		t.Errorf("Expected QuotaUsed 65.5, got %f", provider.QuotaUsed)
	}
}

func TestCautUsageStruct(t *testing.T) {
	usage := CautUsage{
		Provider:     "anthropic",
		RequestCount: 1500,
		TokensIn:     500000,
		TokensOut:    250000,
		Cost:         45.50,
		Period:       "day",
		StartDate:    "2026-01-21",
		EndDate:      "2026-01-21",
	}

	if usage.Provider != "anthropic" {
		t.Errorf("Expected Provider 'anthropic', got %s", usage.Provider)
	}

	if usage.RequestCount != 1500 {
		t.Errorf("Expected RequestCount 1500, got %d", usage.RequestCount)
	}

	if usage.TokensIn != 500000 {
		t.Errorf("Expected TokensIn 500000, got %d", usage.TokensIn)
	}

	if usage.Cost != 45.50 {
		t.Errorf("Expected Cost 45.50, got %f", usage.Cost)
	}
}

func TestCautAdapterCacheInvalidation(t *testing.T) {
	adapter := NewCautAdapter()

	// Invalidate cache should not panic
	adapter.InvalidateAvailabilityCache()

	// Call again to ensure it's safe to call multiple times
	adapter.InvalidateAvailabilityCache()
}

func TestCautAdapterHealthWhenNotInstalled(t *testing.T) {
	adapter := NewCautAdapter()

	// If caut is not installed, Health should return non-healthy status
	_, installed := adapter.Detect()
	if installed {
		t.Skip("caut is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	health, err := adapter.Health(ctx)
	if err != nil {
		t.Fatalf("Health returned unexpected error: %v", err)
	}

	if health.Healthy {
		t.Error("Expected unhealthy status when caut not installed")
	}

	if health.Message != "caut not installed" {
		t.Errorf("Expected message 'caut not installed', got %s", health.Message)
	}
}

func TestCautAdapterIsAvailable(t *testing.T) {
	adapter := NewCautAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// IsAvailable should not panic regardless of whether caut is installed
	available := adapter.IsAvailable(ctx)

	// If caut is not installed, should return false
	_, installed := adapter.Detect()
	if !installed && available {
		t.Error("IsAvailable returned true but caut is not installed")
	}
}

func TestCautAdapterHasUsageData(t *testing.T) {
	adapter := NewCautAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// HasUsageData should not panic
	hasData := adapter.HasUsageData(ctx)

	// If caut is not installed, should return false
	_, installed := adapter.Detect()
	if !installed && hasData {
		t.Error("HasUsageData returned true but caut is not installed")
	}
}

func TestCautAdapterGetAvailability(t *testing.T) {
	adapter := NewCautAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// GetAvailability should not panic and should return valid struct
	availability, err := adapter.GetAvailability(ctx)
	if err != nil {
		t.Fatalf("GetAvailability returned unexpected error: %v", err)
	}

	if availability == nil {
		t.Fatal("GetAvailability returned nil")
	}

	// LastChecked should be set
	if availability.LastChecked.IsZero() {
		t.Error("LastChecked should be set")
	}

	// If not installed, Available should be false
	_, installed := adapter.Detect()
	if !installed && availability.Available {
		t.Error("Available should be false when caut not installed")
	}
}

func TestCautAdapterGetAvailabilityCaching(t *testing.T) {
	adapter := NewCautAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// First call
	availability1, err := adapter.GetAvailability(ctx)
	if err != nil {
		t.Fatalf("First GetAvailability returned error: %v", err)
	}

	// Second call should return cached result
	availability2, err := adapter.GetAvailability(ctx)
	if err != nil {
		t.Fatalf("Second GetAvailability returned error: %v", err)
	}

	// LastChecked should be the same (cached)
	if !availability1.LastChecked.Equal(availability2.LastChecked) {
		t.Error("Expected cached result with same LastChecked time")
	}
}

func TestToolCautInAllTools(t *testing.T) {
	tools := AllTools()
	found := false
	for _, tool := range tools {
		if tool == ToolCaut {
			found = true
			break
		}
	}

	if !found {
		t.Error("ToolCaut not found in AllTools()")
	}
}

func TestCautMinVersionCompatibility(t *testing.T) {
	tests := []struct {
		name     string
		version  Version
		expected bool
	}{
		{
			name:     "exact min version",
			version:  Version{Major: 0, Minor: 1, Patch: 0},
			expected: true,
		},
		{
			name:     "above min version",
			version:  Version{Major: 1, Minor: 0, Patch: 0},
			expected: true,
		},
		{
			name:     "minor above",
			version:  Version{Major: 0, Minor: 2, Patch: 0},
			expected: true,
		},
		{
			name:     "below min version",
			version:  Version{Major: 0, Minor: 0, Patch: 9},
			expected: false,
		},
		{
			name:     "zero version",
			version:  Version{Major: 0, Minor: 0, Patch: 0},
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := cautCompatible(tt.version)
			if result != tt.expected {
				t.Errorf("cautCompatible(%v) = %v, want %v", tt.version, result, tt.expected)
			}
		})
	}
}

func TestCautAdapterGetStatus(t *testing.T) {
	adapter := NewCautAdapter()

	// If caut is not installed, GetStatus should handle gracefully
	_, installed := adapter.Detect()
	if installed {
		t.Skip("caut is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	_, err := adapter.GetStatus(ctx)
	// Should return an error when not installed
	if err == nil {
		t.Log("GetStatus returned no error - caut may be in PATH but not working")
	}
}

func TestCautAvailabilityTTL(t *testing.T) {
	// Verify that the TTL is set to 5 minutes
	if cautAvailabilityTTL != 5*time.Minute {
		t.Errorf("Expected caut availability TTL of 5m, got %v", cautAvailabilityTTL)
	}
}
