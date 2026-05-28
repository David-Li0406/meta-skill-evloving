package integrations

import (
	"testing"
	"time"
)

func TestNewCoordinator(t *testing.T) {
	coord := NewCoordinator(nil)
	if coord == nil {
		t.Fatal("NewCoordinator returned nil")
	}

	// Verify default config was applied
	if coord.config.ProactiveThreshold != 90.0 {
		t.Errorf("Expected ProactiveThreshold 90.0, got %f", coord.config.ProactiveThreshold)
	}

	if coord.config.AutoRotate != true {
		t.Error("Expected AutoRotate to be true by default")
	}
}

func TestNewCoordinatorWithConfig(t *testing.T) {
	cfg := &CoordinatorConfig{
		CAAMEnabled:        true,
		CautEnabled:        true,
		AutoRotate:         false, // Override default
		ProactiveThreshold: 85.0,
		SwitchCooldown:     10 * time.Minute,
		CheckInterval:      1 * time.Minute,
	}

	coord := NewCoordinator(cfg)
	if coord == nil {
		t.Fatal("NewCoordinator returned nil")
	}

	if coord.config.ProactiveThreshold != 85.0 {
		t.Errorf("Expected ProactiveThreshold 85.0, got %f", coord.config.ProactiveThreshold)
	}

	if coord.config.AutoRotate != false {
		t.Error("Expected AutoRotate to be false")
	}

	if coord.switchCooldown != 10*time.Minute {
		t.Errorf("Expected SwitchCooldown 10m, got %v", coord.switchCooldown)
	}
}

func TestDefaultCoordinatorConfig(t *testing.T) {
	cfg := DefaultCoordinatorConfig()

	if cfg.ProactiveThreshold != 90.0 {
		t.Errorf("Expected ProactiveThreshold 90.0, got %f", cfg.ProactiveThreshold)
	}

	if cfg.SwitchCooldown != 5*time.Minute {
		t.Errorf("Expected SwitchCooldown 5m, got %v", cfg.SwitchCooldown)
	}

	if cfg.CheckInterval != 30*time.Second {
		t.Errorf("Expected CheckInterval 30s, got %v", cfg.CheckInterval)
	}

	if !cfg.AutoRotate {
		t.Error("Expected AutoRotate to be true")
	}
}

func TestCoordinator_InCooldown(t *testing.T) {
	cfg := &CoordinatorConfig{
		SwitchCooldown: 1 * time.Second,
	}
	coord := NewCoordinator(cfg)

	// Provider should not be in cooldown initially
	if coord.inCooldown("claude") {
		t.Error("Provider should not be in cooldown initially")
	}

	// Record a switch
	coord.recordSwitch("claude")

	// Provider should now be in cooldown
	if !coord.inCooldown("claude") {
		t.Error("Provider should be in cooldown after switch")
	}

	// Wait for cooldown to expire
	time.Sleep(1100 * time.Millisecond)

	// Provider should no longer be in cooldown
	if coord.inCooldown("claude") {
		t.Error("Provider should not be in cooldown after cooldown period")
	}
}

func TestCoordinator_ResetCooldown(t *testing.T) {
	cfg := &CoordinatorConfig{
		SwitchCooldown: 1 * time.Hour, // Long cooldown
	}
	coord := NewCoordinator(cfg)

	// Record a switch
	coord.recordSwitch("openai")

	// Should be in cooldown
	if !coord.inCooldown("openai") {
		t.Error("Provider should be in cooldown")
	}

	// Reset cooldown
	coord.ResetCooldown("openai")

	// Should no longer be in cooldown
	if coord.inCooldown("openai") {
		t.Error("Provider should not be in cooldown after reset")
	}
}

func TestCoordinator_GetLastSwitchTime(t *testing.T) {
	coord := NewCoordinator(nil)

	// No switch recorded yet
	_, ok := coord.GetLastSwitchTime("gemini")
	if ok {
		t.Error("Expected no last switch time for untracked provider")
	}

	// Record a switch
	before := time.Now()
	coord.recordSwitch("gemini")
	after := time.Now()

	// Get the switch time
	switchTime, ok := coord.GetLastSwitchTime("gemini")
	if !ok {
		t.Error("Expected last switch time to be recorded")
	}

	if switchTime.Before(before) || switchTime.After(after) {
		t.Error("Switch time should be between before and after")
	}
}

func TestCoordinator_SetSwitchCallback(t *testing.T) {
	coord := NewCoordinator(nil)

	callbackInvoked := false
	coord.SetSwitchCallback(func(event SwitchEvent) {
		callbackInvoked = true
		_ = event // Use the event
	})

	// Verify callback is set (indirectly through lock/unlock)
	coord.mu.RLock()
	hasCallback := coord.onSwitch != nil
	coord.mu.RUnlock()

	if !hasCallback {
		t.Error("Expected callback to be set")
	}

	// callbackInvoked would be set true if callback were invoked
	_ = callbackInvoked
}

func TestCoordinator_OnCautAlert_BelowThreshold(t *testing.T) {
	cfg := &CoordinatorConfig{
		CAAMEnabled:        true,
		CautEnabled:        true,
		AutoRotate:         true,
		ProactiveThreshold: 90.0,
		SwitchCooldown:     5 * time.Minute,
	}
	coord := NewCoordinator(cfg)

	// Track if switch was attempted
	switchAttempted := false
	coord.SetSwitchCallback(func(event SwitchEvent) {
		switchAttempted = true
	})

	// Call with usage below threshold - should not trigger switch
	coord.OnCautAlert("claude", 85.0)

	if switchAttempted {
		t.Error("Should not attempt switch below threshold")
	}
}

func TestCoordinator_OnCautAlert_AutoRotateDisabled(t *testing.T) {
	cfg := &CoordinatorConfig{
		CAAMEnabled:        true,
		CautEnabled:        true,
		AutoRotate:         false, // Disabled
		ProactiveThreshold: 90.0,
	}
	coord := NewCoordinator(cfg)

	switchAttempted := false
	coord.SetSwitchCallback(func(event SwitchEvent) {
		switchAttempted = true
	})

	// Call with high usage but auto-rotate disabled
	coord.OnCautAlert("claude", 95.0)

	if switchAttempted {
		t.Error("Should not attempt switch when auto-rotate disabled")
	}
}

func TestCoordinator_IsRunning(t *testing.T) {
	coord := NewCoordinator(nil)

	if coord.IsRunning() {
		t.Error("Coordinator should not be running initially")
	}
}

func TestSwitchEvent_Fields(t *testing.T) {
	event := SwitchEvent{
		Provider:          "claude",
		UsagePercent:      92.5,
		Reason:            "proactive",
		PreviousAccount:   "account1",
		NewAccount:        "account2",
		Success:           true,
		Timestamp:         time.Now(),
		AccountsRemaining: 3,
	}

	if event.Provider != "claude" {
		t.Errorf("Expected Provider 'claude', got %q", event.Provider)
	}

	if event.UsagePercent != 92.5 {
		t.Errorf("Expected UsagePercent 92.5, got %f", event.UsagePercent)
	}

	if event.Reason != "proactive" {
		t.Errorf("Expected Reason 'proactive', got %q", event.Reason)
	}

	if !event.Success {
		t.Error("Expected Success to be true")
	}

	if event.AccountsRemaining != 3 {
		t.Errorf("Expected AccountsRemaining 3, got %d", event.AccountsRemaining)
	}
}

func TestCoordinatorConfig_Validation(t *testing.T) {
	// Test that config values are reasonable
	cfg := DefaultCoordinatorConfig()

	if cfg.ProactiveThreshold < 0 || cfg.ProactiveThreshold > 100 {
		t.Errorf("ProactiveThreshold should be 0-100, got %f", cfg.ProactiveThreshold)
	}

	if cfg.SwitchCooldown <= 0 {
		t.Error("SwitchCooldown should be positive")
	}

	if cfg.CheckInterval <= 0 {
		t.Error("CheckInterval should be positive")
	}
}

func TestGetGlobalCoordinator(t *testing.T) {
	coord := GetGlobalCoordinator()
	if coord == nil {
		t.Fatal("GetGlobalCoordinator returned nil")
	}

	// Should return the same instance
	coord2 := GetGlobalCoordinator()
	if coord != coord2 {
		t.Error("GetGlobalCoordinator should return same instance")
	}
}
