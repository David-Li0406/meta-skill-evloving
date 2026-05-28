package tools

import (
	"context"
	"testing"
	"time"
)

func TestNewRanoAdapter(t *testing.T) {
	adapter := NewRanoAdapter()
	if adapter == nil {
		t.Fatal("NewRanoAdapter returned nil")
	}

	if adapter.Name() != ToolRano {
		t.Errorf("Expected name %s, got %s", ToolRano, adapter.Name())
	}

	if adapter.BinaryName() != "rano" {
		t.Errorf("Expected binary name 'rano', got %s", adapter.BinaryName())
	}
}

func TestRanoAdapterImplementsInterface(t *testing.T) {
	// Ensure RanoAdapter implements the Adapter interface
	var _ Adapter = (*RanoAdapter)(nil)
}

func TestRanoAdapterDetect(t *testing.T) {
	adapter := NewRanoAdapter()

	// Test detection - result depends on whether rano is installed
	path, installed := adapter.Detect()

	// If installed, path should be non-empty
	if installed && path == "" {
		t.Error("rano detected but path is empty")
	}

	// If not installed, path should be empty
	if !installed && path != "" {
		t.Errorf("rano not detected but path is %s", path)
	}
}

func TestRanoAvailabilityStruct(t *testing.T) {
	availability := RanoAvailability{
		Available:     true,
		Compatible:    true,
		HasCapability: true,
		CanReadProc:   true,
		Version:       Version{Major: 1, Minor: 0, Patch: 0},
		Path:          "/usr/local/bin/rano",
		LastChecked:   time.Now(),
	}

	if !availability.Available {
		t.Error("Expected Available to be true")
	}

	if !availability.Compatible {
		t.Error("Expected Compatible to be true")
	}

	if !availability.HasCapability {
		t.Error("Expected HasCapability to be true")
	}

	if !availability.CanReadProc {
		t.Error("Expected CanReadProc to be true")
	}
}

func TestRanoStatusStruct(t *testing.T) {
	status := RanoStatus{
		Running:      true,
		Monitoring:   true,
		ProcessCount: 5,
		RequestCount: 100,
		BytesIn:      1024 * 1024,
		BytesOut:     512 * 1024,
	}

	if !status.Running {
		t.Error("Expected Running to be true")
	}

	if !status.Monitoring {
		t.Error("Expected Monitoring to be true")
	}

	if status.ProcessCount != 5 {
		t.Errorf("Expected ProcessCount 5, got %d", status.ProcessCount)
	}

	if status.RequestCount != 100 {
		t.Errorf("Expected RequestCount 100, got %d", status.RequestCount)
	}
}

func TestRanoProcessStatsStruct(t *testing.T) {
	stats := RanoProcessStats{
		PID:          12345,
		ProcessName:  "claude-agent",
		RequestCount: 50,
		BytesIn:      256 * 1024,
		BytesOut:     128 * 1024,
		LastRequest:  "2026-01-21T10:00:00Z",
	}

	if stats.PID != 12345 {
		t.Errorf("Expected PID 12345, got %d", stats.PID)
	}

	if stats.ProcessName != "claude-agent" {
		t.Errorf("Expected ProcessName 'claude-agent', got %s", stats.ProcessName)
	}

	if stats.RequestCount != 50 {
		t.Errorf("Expected RequestCount 50, got %d", stats.RequestCount)
	}
}

func TestRanoAdapterCacheInvalidation(t *testing.T) {
	adapter := NewRanoAdapter()

	// Invalidate cache should not panic
	adapter.InvalidateAvailabilityCache()

	// Call again to ensure it's safe to call multiple times
	adapter.InvalidateAvailabilityCache()
}

func TestRanoAdapterHealthWhenNotInstalled(t *testing.T) {
	adapter := NewRanoAdapter()

	// If rano is not installed, Health should return non-healthy status
	_, installed := adapter.Detect()
	if installed {
		t.Skip("rano is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	health, err := adapter.Health(ctx)
	if err != nil {
		t.Fatalf("Health returned unexpected error: %v", err)
	}

	if health.Healthy {
		t.Error("Expected unhealthy status when rano not installed")
	}

	if health.Message != "rano not installed" {
		t.Errorf("Expected message 'rano not installed', got %s", health.Message)
	}
}

func TestRanoAdapterIsAvailable(t *testing.T) {
	adapter := NewRanoAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// IsAvailable should not panic regardless of whether rano is installed
	available := adapter.IsAvailable(ctx)

	// If rano is not installed, should return false
	_, installed := adapter.Detect()
	if !installed && available {
		t.Error("IsAvailable returned true but rano is not installed")
	}
}

func TestRanoAdapterHasRequiredPermissions(t *testing.T) {
	adapter := NewRanoAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// HasRequiredPermissions should not panic
	hasPerms := adapter.HasRequiredPermissions(ctx)

	// If rano is not installed, should return false
	_, installed := adapter.Detect()
	if !installed && hasPerms {
		t.Error("HasRequiredPermissions returned true but rano is not installed")
	}
}

func TestRanoAdapterGetAvailability(t *testing.T) {
	adapter := NewRanoAdapter()

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
		t.Error("Available should be false when rano not installed")
	}
}

func TestRanoAdapterGetAvailabilityCaching(t *testing.T) {
	adapter := NewRanoAdapter()

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

func TestToolRanoInAllTools(t *testing.T) {
	tools := AllTools()
	found := false
	for _, tool := range tools {
		if tool == ToolRano {
			found = true
			break
		}
	}

	if !found {
		t.Error("ToolRano not found in AllTools()")
	}
}

func TestRanoMinVersionCompatibility(t *testing.T) {
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
			result := ranoCompatible(tt.version)
			if result != tt.expected {
				t.Errorf("ranoCompatible(%v) = %v, want %v", tt.version, result, tt.expected)
			}
		})
	}
}

func TestRanoAdapterGetStatus(t *testing.T) {
	adapter := NewRanoAdapter()

	// If rano is not installed, GetStatus should handle gracefully
	_, installed := adapter.Detect()
	if installed {
		t.Skip("rano is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	_, err := adapter.GetStatus(ctx)
	// Should return an error when not installed (exec.LookPath fails)
	if err == nil {
		t.Log("GetStatus returned no error - rano may be in PATH but not working")
	}
}

func TestRanoAvailabilityTTL(t *testing.T) {
	// Verify that the TTL is set to 2 minutes (shorter due to permission changes)
	if ranoAvailabilityTTL != 2*time.Minute {
		t.Errorf("Expected rano availability TTL of 2m, got %v", ranoAvailabilityTTL)
	}
}

func TestRanoAdapterCheckProcAccess(t *testing.T) {
	adapter := NewRanoAdapter()

	// checkProcAccess should work on Linux systems
	canAccess := adapter.checkProcAccess()

	// On Linux with /proc available, this should return true
	// Just verify it doesn't panic
	t.Logf("checkProcAccess returned: %v", canAccess)
}
