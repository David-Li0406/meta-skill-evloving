package tools

import (
	"context"
	"testing"
	"time"
)

func TestNewPTAdapter(t *testing.T) {
	adapter := NewPTAdapter()
	if adapter == nil {
		t.Fatal("NewPTAdapter returned nil")
	}

	if adapter.Name() != ToolPT {
		t.Errorf("Expected name %s, got %s", ToolPT, adapter.Name())
	}

	if adapter.BinaryName() != "pt" {
		t.Errorf("Expected binary name 'pt', got %s", adapter.BinaryName())
	}
}

func TestPTAdapterImplementsInterface(t *testing.T) {
	// Ensure PTAdapter implements the Adapter interface
	var _ Adapter = (*PTAdapter)(nil)
}

func TestPTAdapterDetect(t *testing.T) {
	adapter := NewPTAdapter()

	// Test detection - result depends on whether pt is installed
	path, installed := adapter.Detect()

	// If installed, path should be non-empty
	if installed && path == "" {
		t.Error("pt detected but path is empty")
	}

	// If not installed, path should be empty
	if !installed && path != "" {
		t.Errorf("pt not detected but path is %s", path)
	}
}

func TestPTStatusStruct(t *testing.T) {
	status := PTStatus{
		Available:   true,
		Compatible:  true,
		Version:     Version{Major: 1, Minor: 0, Patch: 0},
		Path:        "/usr/local/bin/pt",
		LastChecked: time.Now(),
	}

	if !status.Available {
		t.Error("Expected Available to be true")
	}

	if !status.Compatible {
		t.Error("Expected Compatible to be true")
	}

	if status.Path != "/usr/local/bin/pt" {
		t.Errorf("Expected Path '/usr/local/bin/pt', got %s", status.Path)
	}
}

func TestPTClassificationConstants(t *testing.T) {
	tests := []struct {
		class    PTClassification
		expected string
	}{
		{PTClassUseful, "useful"},
		{PTClassAbandoned, "abandoned"},
		{PTClassZombie, "zombie"},
		{PTClassUnknown, "unknown"},
	}

	for _, tt := range tests {
		if string(tt.class) != tt.expected {
			t.Errorf("Expected classification %s, got %s", tt.expected, tt.class)
		}
	}
}

func TestPTProcessResultStruct(t *testing.T) {
	result := PTProcessResult{
		PID:            12345,
		Name:           "claude-agent",
		Classification: PTClassUseful,
		Confidence:     0.95,
		Reason:         "Active process with recent I/O",
	}

	if result.PID != 12345 {
		t.Errorf("Expected PID 12345, got %d", result.PID)
	}

	if result.Name != "claude-agent" {
		t.Errorf("Expected Name 'claude-agent', got %s", result.Name)
	}

	if result.Classification != PTClassUseful {
		t.Errorf("Expected Classification 'useful', got %s", result.Classification)
	}

	if result.Confidence != 0.95 {
		t.Errorf("Expected Confidence 0.95, got %f", result.Confidence)
	}

	if result.Reason != "Active process with recent I/O" {
		t.Errorf("Expected Reason 'Active process with recent I/O', got %s", result.Reason)
	}
}

func TestPTAdapterCacheInvalidation(t *testing.T) {
	adapter := NewPTAdapter()

	// Invalidate cache should not panic
	adapter.InvalidateStatusCache()

	// Call again to ensure it's safe to call multiple times
	adapter.InvalidateStatusCache()
}

func TestPTAdapterHealthWhenNotInstalled(t *testing.T) {
	adapter := NewPTAdapter()

	// If pt is not installed, Health should return non-healthy status
	_, installed := adapter.Detect()
	if installed {
		t.Skip("pt is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	health, err := adapter.Health(ctx)
	if err != nil {
		t.Fatalf("Health returned unexpected error: %v", err)
	}

	if health.Healthy {
		t.Error("Expected unhealthy status when pt not installed")
	}

	if health.Message != "pt not installed" {
		t.Errorf("Expected message 'pt not installed', got %s", health.Message)
	}
}

func TestPTAdapterIsAvailable(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// IsAvailable should not panic regardless of whether pt is installed
	available := adapter.IsAvailable(ctx)

	// If pt is not installed, should return false
	_, installed := adapter.Detect()
	if !installed && available {
		t.Error("IsAvailable returned true but pt is not installed")
	}
}

func TestPTAdapterGetStatus(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// GetStatus should not panic and should return valid struct
	status, err := adapter.GetStatus(ctx)
	if err != nil {
		t.Fatalf("GetStatus returned unexpected error: %v", err)
	}

	if status == nil {
		t.Fatal("GetStatus returned nil")
	}

	// LastChecked should be set
	if status.LastChecked.IsZero() {
		t.Error("LastChecked should be set")
	}

	// If not installed, Available should be false
	_, installed := adapter.Detect()
	if !installed && status.Available {
		t.Error("Available should be false when pt not installed")
	}
}

func TestPTAdapterGetStatusCaching(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// First call
	status1, err := adapter.GetStatus(ctx)
	if err != nil {
		t.Fatalf("First GetStatus returned error: %v", err)
	}

	// Second call should return cached result
	status2, err := adapter.GetStatus(ctx)
	if err != nil {
		t.Fatalf("Second GetStatus returned error: %v", err)
	}

	// LastChecked should be the same (cached)
	if !status1.LastChecked.Equal(status2.LastChecked) {
		t.Error("Expected cached result with same LastChecked time")
	}
}

func TestToolPTInAllTools(t *testing.T) {
	tools := AllTools()
	found := false
	for _, tool := range tools {
		if tool == ToolPT {
			found = true
			break
		}
	}

	if !found {
		t.Error("ToolPT not found in AllTools()")
	}
}

func TestPTMinVersionCompatibility(t *testing.T) {
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
			result := ptCompatible(tt.version)
			if result != tt.expected {
				t.Errorf("ptCompatible(%v) = %v, want %v", tt.version, result, tt.expected)
			}
		})
	}
}

func TestPTStatusTTL(t *testing.T) {
	// Verify that the TTL is set to 5 minutes
	if ptStatusTTL != 5*time.Minute {
		t.Errorf("Expected pt status TTL of 5m, got %v", ptStatusTTL)
	}
}

func TestPTAdapterInfo(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	info, err := adapter.Info(ctx)
	if err != nil {
		t.Fatalf("Info returned unexpected error: %v", err)
	}

	if info == nil {
		t.Fatal("Info returned nil")
	}

	if info.Name != ToolPT {
		t.Errorf("Expected name %s, got %s", ToolPT, info.Name)
	}

	// If not installed, Installed should be false
	_, installed := adapter.Detect()
	if !installed && info.Installed {
		t.Error("Installed should be false when pt not installed")
	}
}

func TestPTAdapterCapabilities(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	caps, err := adapter.Capabilities(ctx)
	if err != nil {
		t.Fatalf("Capabilities returned unexpected error: %v", err)
	}

	// If not installed, should return empty capabilities
	_, installed := adapter.Detect()
	if !installed && len(caps) > 0 {
		t.Error("Expected empty capabilities when pt not installed")
	}
}

func TestPTAdapterHasCapability(t *testing.T) {
	adapter := NewPTAdapter()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// HasCapability should not panic
	hasCap := adapter.HasCapability(ctx, CapRobotMode)

	// If not installed, should return false
	_, installed := adapter.Detect()
	if !installed && hasCap {
		t.Error("HasCapability returned true but pt is not installed")
	}
}

func TestPTClassifyProcessWhenNotInstalled(t *testing.T) {
	adapter := NewPTAdapter()

	_, installed := adapter.Detect()
	if installed {
		t.Skip("pt is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// ClassifyProcess should return error when pt is not installed
	_, err := adapter.ClassifyProcess(ctx, 1)
	if err == nil {
		t.Error("Expected error when pt is not installed")
	}
}

func TestPTClassifyProcessesWhenNotInstalled(t *testing.T) {
	adapter := NewPTAdapter()

	_, installed := adapter.Detect()
	if installed {
		t.Skip("pt is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// ClassifyProcesses should return error when pt is not installed
	_, err := adapter.ClassifyProcesses(ctx, []int{1, 2, 3})
	if err == nil {
		t.Error("Expected error when pt is not installed")
	}
}

func TestPTWatchSessionWhenNotInstalled(t *testing.T) {
	adapter := NewPTAdapter()

	_, installed := adapter.Detect()
	if installed {
		t.Skip("pt is installed, skipping not-installed test")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// WatchSession should return error when pt is not installed
	_, err := adapter.WatchSession(ctx, "test-session")
	if err == nil {
		t.Error("Expected error when pt is not installed")
	}
}

func TestPTToolNameConstant(t *testing.T) {
	if ToolPT != "pt" {
		t.Errorf("Expected ToolPT to be 'pt', got %s", ToolPT)
	}
}
