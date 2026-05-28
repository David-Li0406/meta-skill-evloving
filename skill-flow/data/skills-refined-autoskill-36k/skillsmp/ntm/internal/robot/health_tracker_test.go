package robot

import (
	"testing"
	"time"
)

func TestHealthTrackerBasic(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Record initial healthy state
	tracker.RecordState("%1", "claude", HealthHealthy, "all checks passed")

	// Verify state was recorded
	metrics, ok := tracker.GetHealth("%1")
	if !ok {
		t.Fatal("expected to find agent metrics")
	}

	if metrics.CurrentState != HealthHealthy {
		t.Errorf("expected HealthHealthy, got %v", metrics.CurrentState)
	}

	if metrics.AgentType != "claude" {
		t.Errorf("expected agent type 'claude', got %s", metrics.AgentType)
	}

	if metrics.SessionID != "test-session" {
		t.Errorf("expected session 'test-session', got %s", metrics.SessionID)
	}
}

func TestHealthTrackerStateTransitions(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Record a series of state transitions
	tracker.RecordState("%1", "claude", HealthHealthy, "initial")
	tracker.RecordState("%1", "claude", HealthDegraded, "slow response")
	tracker.RecordState("%1", "claude", HealthUnhealthy, "crashed")
	tracker.RecordState("%1", "claude", HealthHealthy, "recovered")

	// Verify transition history
	history := tracker.GetTransitionHistory("%1", 10)
	if len(history) != 3 { // 3 transitions (healthy->degraded, degraded->unhealthy, unhealthy->healthy)
		t.Errorf("expected 3 transitions, got %d", len(history))
	}

	// Most recent should be unhealthy->healthy
	if len(history) > 0 {
		if history[0].From != HealthUnhealthy || history[0].To != HealthHealthy {
			t.Errorf("expected transition unhealthy->healthy, got %v->%v", history[0].From, history[0].To)
		}
	}
}

func TestHealthTrackerNoTransitionOnSameState(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Record same state multiple times
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")
	tracker.RecordState("%1", "claude", HealthHealthy, "still ok")
	tracker.RecordState("%1", "claude", HealthHealthy, "yep still ok")

	// Should have no transitions (same state)
	history := tracker.GetTransitionHistory("%1", 10)
	if len(history) != 0 {
		t.Errorf("expected 0 transitions for same state, got %d", len(history))
	}
}

func TestHealthTrackerConsecutiveFailures(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Initial healthy state
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")

	// Multiple unhealthy states
	tracker.RecordState("%1", "claude", HealthUnhealthy, "error 1")
	tracker.RecordState("%1", "claude", HealthUnhealthy, "error 2")
	tracker.RecordState("%1", "claude", HealthUnhealthy, "error 3")

	metrics, _ := tracker.GetHealth("%1")
	if metrics.ConsecutiveFailures != 3 {
		t.Errorf("expected 3 consecutive failures, got %d", metrics.ConsecutiveFailures)
	}

	// Healthy should reset
	tracker.RecordState("%1", "claude", HealthHealthy, "recovered")
	metrics, _ = tracker.GetHealth("%1")
	if metrics.ConsecutiveFailures != 0 {
		t.Errorf("expected 0 consecutive failures after recovery, got %d", metrics.ConsecutiveFailures)
	}
}

func TestHealthTrackerRestarts(t *testing.T) {
	tracker := NewHealthTracker("test-session", &HealthTrackerConfig{
		RestartWindow: time.Hour,
	})

	// First need to track the agent
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")

	// Record restarts
	tracker.RecordRestart("%1")
	tracker.RecordRestart("%1")
	tracker.RecordRestart("%1")

	metrics, _ := tracker.GetHealth("%1")
	if metrics.TotalRestarts != 3 {
		t.Errorf("expected 3 total restarts, got %d", metrics.TotalRestarts)
	}

	restartsInWindow := tracker.GetRestartsInWindow("%1")
	if restartsInWindow != 3 {
		t.Errorf("expected 3 restarts in window, got %d", restartsInWindow)
	}
}

func TestHealthTrackerErrors(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// First need to track the agent
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")

	// Record errors
	tracker.RecordError("%1", "rate_limit", "429 too many requests")
	tracker.RecordError("%1", "network", "connection refused")

	metrics, _ := tracker.GetHealth("%1")
	if metrics.TotalErrors != 2 {
		t.Errorf("expected 2 total errors, got %d", metrics.TotalErrors)
	}

	if metrics.LastError == nil {
		t.Fatal("expected last error to be set")
	}

	if metrics.LastError.Type != "network" {
		t.Errorf("expected last error type 'network', got %s", metrics.LastError.Type)
	}
}

func TestHealthTrackerRateLimits(t *testing.T) {
	tracker := NewHealthTracker("test-session", &HealthTrackerConfig{
		RateLimitWindow: time.Hour,
	})

	// Record rate limit states
	tracker.RecordState("%1", "claude", HealthRateLimited, "rate limit hit")
	tracker.RecordState("%1", "claude", HealthHealthy, "recovered")
	tracker.RecordState("%1", "claude", HealthRateLimited, "rate limit hit again")

	metrics, _ := tracker.GetHealth("%1")
	if metrics.RateLimitCount != 2 {
		t.Errorf("expected 2 rate limit count, got %d", metrics.RateLimitCount)
	}

	rateLimitsInWindow := tracker.GetRateLimitsInWindow("%1")
	if rateLimitsInWindow != 2 {
		t.Errorf("expected 2 rate limits in window, got %d", rateLimitsInWindow)
	}
}

func TestHealthTrackerUptime(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Track agent
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")

	// Sleep briefly to have measurable uptime
	time.Sleep(10 * time.Millisecond)

	uptime := tracker.GetUptime("%1")
	if uptime < 10*time.Millisecond {
		t.Errorf("expected uptime >= 10ms, got %v", uptime)
	}
}

func TestHealthTrackerClear(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Track agent
	tracker.RecordState("%1", "claude", HealthHealthy, "ok")
	tracker.RecordState("%2", "codex", HealthHealthy, "ok")

	// Clear one agent
	tracker.ClearAgent("%1")

	_, ok1 := tracker.GetHealth("%1")
	_, ok2 := tracker.GetHealth("%2")

	if ok1 {
		t.Error("expected %1 to be cleared")
	}
	if !ok2 {
		t.Error("expected %2 to still exist")
	}

	// Reset all
	tracker.Reset()
	all := tracker.GetAllHealth()
	if len(all) != 0 {
		t.Errorf("expected 0 agents after reset, got %d", len(all))
	}
}

func TestHealthTrackerTransitionHistoryLimit(t *testing.T) {
	tracker := NewHealthTracker("test-session", &HealthTrackerConfig{
		MaxTransitions: 5,
	})

	// Record more transitions than the limit
	states := []HealthState{
		HealthHealthy, HealthDegraded, HealthUnhealthy, HealthHealthy,
		HealthDegraded, HealthUnhealthy, HealthHealthy, HealthDegraded,
	}

	for i, state := range states {
		tracker.RecordState("%1", "claude", state, "transition "+string(rune('0'+i)))
	}

	history := tracker.GetTransitionHistory("%1", 100)
	if len(history) != 5 {
		t.Errorf("expected max 5 transitions, got %d", len(history))
	}
}

func TestHealthTrackerConcurrency(t *testing.T) {
	tracker := NewHealthTracker("test-session", nil)

	// Concurrent state updates
	done := make(chan bool, 10)

	for i := 0; i < 10; i++ {
		go func(idx int) {
			paneID := "%1"
			if idx%2 == 0 {
				paneID = "%2"
			}
			tracker.RecordState(paneID, "claude", HealthHealthy, "concurrent")
			tracker.RecordError(paneID, "test", "concurrent error")
			tracker.RecordRestart(paneID)
			tracker.GetHealth(paneID)
			tracker.GetAllHealth()
			done <- true
		}(i)
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	// Verify no panics occurred (if we get here, concurrency is safe)
	all := tracker.GetAllHealth()
	if len(all) != 2 {
		t.Errorf("expected 2 agents, got %d", len(all))
	}
}

func TestGlobalHealthTrackerRegistry(t *testing.T) {
	// Clean up first
	ClearHealthTracker("registry-test")

	// Get tracker (should create new)
	tracker1 := GetHealthTracker("registry-test")
	tracker1.RecordState("%1", "claude", HealthHealthy, "ok")

	// Get again (should return same)
	tracker2 := GetHealthTracker("registry-test")
	_, ok := tracker2.GetHealth("%1")
	if !ok {
		t.Error("expected same tracker to be returned from registry")
	}

	// Clear and verify
	ClearHealthTracker("registry-test")
	tracker3 := GetHealthTracker("registry-test")
	_, ok = tracker3.GetHealth("%1")
	if ok {
		t.Error("expected new tracker after clear")
	}
}
