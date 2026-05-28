package startup

import (
	"testing"
)

func TestPhaseTransitions(t *testing.T) {
	// Reset state before test
	Reset()

	// Initially at PhaseNone
	if CurrentPhase() != PhaseNone {
		t.Errorf("Expected PhaseNone, got %v", CurrentPhase())
	}

	// Begin Phase 1
	BeginPhase1()
	if CurrentPhase() != Phase1 {
		t.Errorf("Expected Phase1, got %v", CurrentPhase())
	}

	// End Phase 1
	EndPhase1()
	if !IsPhase1Complete() {
		t.Error("Phase 1 should be complete")
	}
	if CurrentPhase() != Phase2 {
		t.Errorf("Expected Phase2 after Phase1 complete, got %v", CurrentPhase())
	}

	// Begin Phase 2
	BeginPhase2()

	// End Phase 2
	EndPhase2()
	if !IsPhase2Complete() {
		t.Error("Phase 2 should be complete")
	}
	if CurrentPhase() != PhaseComplete {
		t.Errorf("Expected PhaseComplete, got %v", CurrentPhase())
	}
}

func TestDeferredFunctions(t *testing.T) {
	Reset()

	// Track execution order
	var executed []string

	// Register deferred functions
	RegisterDeferred("func1", func() error {
		executed = append(executed, "func1")
		return nil
	})
	RegisterDeferred("func2", func() error {
		executed = append(executed, "func2")
		return nil
	})

	// Run deferred functions
	if err := RunDeferred(); err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	// Verify execution
	if len(executed) != 2 {
		t.Errorf("Expected 2 functions executed, got %d", len(executed))
	}
	if executed[0] != "func1" || executed[1] != "func2" {
		t.Errorf("Unexpected execution order: %v", executed)
	}

	// Verify initialized tracking
	if !IsInitialized("func1") {
		t.Error("func1 should be marked as initialized")
	}
	if !IsInitialized("func2") {
		t.Error("func2 should be marked as initialized")
	}
}

func TestGetStats(t *testing.T) {
	Reset()

	stats := GetStats()
	if stats.CurrentPhase != PhaseNone {
		t.Errorf("Expected PhaseNone, got %v", stats.CurrentPhase)
	}
	if stats.Phase1Done {
		t.Error("Phase1Done should be false")
	}
	if stats.Phase2Done {
		t.Error("Phase2Done should be false")
	}

	BeginPhase1()
	EndPhase1()
	BeginPhase2()
	EndPhase2()

	stats = GetStats()
	if stats.CurrentPhase != PhaseComplete {
		t.Errorf("Expected PhaseComplete, got %v", stats.CurrentPhase)
	}
	if !stats.Phase1Done {
		t.Error("Phase1Done should be true")
	}
	if !stats.Phase2Done {
		t.Error("Phase2Done should be true")
	}
}

func TestReset(t *testing.T) {
	// Setup some state
	BeginPhase1()
	EndPhase1()
	RegisterDeferred("test", func() error { return nil })

	// Reset
	Reset()

	// Verify everything is cleared
	if CurrentPhase() != PhaseNone {
		t.Errorf("Expected PhaseNone after reset, got %v", CurrentPhase())
	}
	if IsPhase1Complete() {
		t.Error("Phase 1 should not be complete after reset")
	}
	if IsPhase2Complete() {
		t.Error("Phase 2 should not be complete after reset")
	}
	if IsInitialized("test") {
		t.Error("test should not be initialized after reset")
	}
}
