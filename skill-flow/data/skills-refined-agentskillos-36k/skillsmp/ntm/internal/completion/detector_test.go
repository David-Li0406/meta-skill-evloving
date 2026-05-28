package completion

import (
	"context"
	"fmt"
	"sync"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/assignment"
)

func TestDefaultConfig(t *testing.T) {
	cfg := DefaultConfig()

	if cfg.PollInterval != 5*time.Second {
		t.Errorf("PollInterval = %v, want %v", cfg.PollInterval, 5*time.Second)
	}
	if cfg.IdleThreshold != 120*time.Second {
		t.Errorf("IdleThreshold = %v, want %v", cfg.IdleThreshold, 120*time.Second)
	}
	if !cfg.RetryOnError {
		t.Error("RetryOnError should be true by default")
	}
	if !cfg.GracefulDegrading {
		t.Error("GracefulDegrading should be true by default")
	}
	if cfg.CaptureLines != 50 {
		t.Errorf("CaptureLines = %d, want 50", cfg.CaptureLines)
	}
}

func TestNew(t *testing.T) {
	store := assignment.NewStore("test-session")
	d := New("test-session", store)

	if d.Session != "test-session" {
		t.Errorf("Session = %q, want %q", d.Session, "test-session")
	}
	if d.Store != store {
		t.Error("Store not set correctly")
	}
	if len(d.Patterns) == 0 {
		t.Error("Default completion patterns not loaded")
	}
	if len(d.FailPattern) == 0 {
		t.Error("Default failure patterns not loaded")
	}
}

func TestAddPattern(t *testing.T) {
	d := New("test-session", nil)
	initialCount := len(d.Patterns)

	err := d.AddPattern(`(?i)custom\s+complete`)
	if err != nil {
		t.Fatalf("AddPattern failed: %v", err)
	}

	if len(d.Patterns) != initialCount+1 {
		t.Errorf("Pattern count = %d, want %d", len(d.Patterns), initialCount+1)
	}
}

func TestAddPatternInvalid(t *testing.T) {
	d := New("test-session", nil)

	err := d.AddPattern(`[invalid`)
	if err == nil {
		t.Error("AddPattern should fail for invalid regex")
	}
}

func TestAddFailurePattern(t *testing.T) {
	d := New("test-session", nil)
	initialCount := len(d.FailPattern)

	err := d.AddFailurePattern(`(?i)custom\s+failure`)
	if err != nil {
		t.Fatalf("AddFailurePattern failed: %v", err)
	}

	if len(d.FailPattern) != initialCount+1 {
		t.Errorf("Pattern count = %d, want %d", len(d.FailPattern), initialCount+1)
	}
}

func TestMatchCompletionPatterns(t *testing.T) {
	d := New("test-session", nil)

	tests := []struct {
		name   string
		output string
		want   bool
	}{
		{"bead complete", "I've finished the bead bd-1234 complete", true},
		{"task done", "The task bd-1234 done successfully", true},
		{"task finished", "task xyz finished successfully", true},
		{"closing bead", "closing bead bd-5678", true},
		{"br close", "Running br close bd-1234", true},
		{"marked complete", "The work was marked as complete", true},
		{"successfully completed", "Task successfully completed!", true},
		{"work complete", "My work complete for this bead", true},
		{"no match", "Just regular output without keywords", false},
		{"partial match", "The bead is still in progress", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := d.matchCompletionPatterns(tt.output)
			if got != tt.want {
				t.Errorf("matchCompletionPatterns(%q) = %v, want %v", tt.output, got, tt.want)
			}
		})
	}
}

func TestMatchFailurePatterns(t *testing.T) {
	d := New("test-session", nil)

	tests := []struct {
		name      string
		output    string
		wantMatch bool
	}{
		{"unable to complete", "I'm unable to complete this task", true},
		{"cannot proceed", "Cannot proceed due to missing dependencies", true},
		{"blocked by", "This is blocked by another issue", true},
		{"giving up", "I'm giving up on this approach", true},
		{"need help", "I need help with this problem", true},
		{"failed to", "Failed to compile the code", true},
		{"error fatal", "Error: fatal exception occurred", true},
		{"aborting", "Aborting the operation", true},
		{"no match", "Everything is working fine", false},
		{"success message", "Successfully deployed the feature", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := d.matchFailurePatterns(tt.output)
			if (got != "") != tt.wantMatch {
				t.Errorf("matchFailurePatterns(%q) = %q, wantMatch=%v", tt.output, got, tt.wantMatch)
			}
		})
	}
}

func TestTruncateOutput(t *testing.T) {
	tests := []struct {
		name   string
		output string
		maxLen int
		want   string
	}{
		{"short", "hello", 10, "hello"},
		{"exact", "hello", 5, "hello"},
		{"truncate", "hello world", 5, "...world"},
		{"empty", "", 10, ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := truncateOutput(tt.output, tt.maxLen)
			if got != tt.want {
				t.Errorf("truncateOutput(%q, %d) = %q, want %q", tt.output, tt.maxLen, got, tt.want)
			}
		})
	}
}

func TestCompletionEventFields(t *testing.T) {
	event := CompletionEvent{
		Pane:       2,
		AgentType:  "claude",
		BeadID:     "bd-1234",
		Method:     MethodPatternMatch,
		Timestamp:  time.Now(),
		Duration:   5 * time.Minute,
		Output:     "task complete",
		IsFailed:   false,
		FailReason: "",
	}

	if event.Pane != 2 {
		t.Errorf("Pane = %d, want 2", event.Pane)
	}
	if event.AgentType != "claude" {
		t.Errorf("AgentType = %q, want %q", event.AgentType, "claude")
	}
	if event.Method != MethodPatternMatch {
		t.Errorf("Method = %v, want %v", event.Method, MethodPatternMatch)
	}
}

func TestDetectionMethods(t *testing.T) {
	tests := []struct {
		method DetectionMethod
		want   string
	}{
		{MethodBeadClosed, "bead_closed"},
		{MethodPatternMatch, "pattern_match"},
		{MethodIdle, "idle"},
		{MethodAgentMail, "agent_mail"},
		{MethodPaneLost, "pane_lost"},
	}

	for _, tt := range tests {
		t.Run(string(tt.method), func(t *testing.T) {
			if string(tt.method) != tt.want {
				t.Errorf("DetectionMethod = %q, want %q", tt.method, tt.want)
			}
		})
	}
}

func TestCheckNowNoStore(t *testing.T) {
	d := New("test-session", nil)

	_, err := d.CheckNow(0)
	if err == nil {
		t.Error("CheckNow should fail without assignment store")
	}
}

func TestCheckNowNoAssignment(t *testing.T) {
	store := assignment.NewStore("test-session")
	d := New("test-session", store)

	_, err := d.CheckNow(99)
	if err == nil {
		t.Error("CheckNow should fail for pane with no assignment")
	}
}

func TestIdleDetection(t *testing.T) {
	store := assignment.NewStore("test-session")
	cfg := DefaultConfig()
	cfg.IdleThreshold = 10 * time.Millisecond // Very short for testing
	d := NewWithConfig("test-session", store, cfg)

	now := time.Now()
	a := &assignment.Assignment{
		BeadID:     "bd-test",
		Pane:       0,
		AgentType:  "claude",
		AssignedAt: now,
	}

	// First check - initialize activity state
	event := d.checkIdle(a, "initial output", now)
	if event != nil {
		t.Error("First checkIdle should return nil (initializing)")
	}

	// Same output - should trigger burst detection but not complete yet
	event = d.checkIdle(a, "initial output", now)
	if event != nil {
		t.Error("Second checkIdle should return nil (no burst started)")
	}

	// Change output to start burst
	event = d.checkIdle(a, "new output", now)
	if event != nil {
		t.Error("After output change, checkIdle should return nil")
	}

	// Wait for idle threshold
	time.Sleep(15 * time.Millisecond)

	// Same output after threshold - should detect idle completion
	event = d.checkIdle(a, "new output", now)
	if event == nil {
		t.Error("After idle threshold, checkIdle should return completion event")
	}
	if event != nil && event.Method != MethodIdle {
		t.Errorf("Method = %v, want %v", event.Method, MethodIdle)
	}
}

func TestWatchCancellation(t *testing.T) {
	store := assignment.NewStore("test-session")
	cfg := DefaultConfig()
	cfg.PollInterval = 10 * time.Millisecond
	d := NewWithConfig("test-session", store, cfg)

	ctx, cancel := context.WithCancel(context.Background())
	events := d.Watch(ctx)

	// Cancel immediately
	cancel()

	// Channel should close
	select {
	case _, ok := <-events:
		if ok {
			// May receive events before close, that's fine
		}
	case <-time.After(100 * time.Millisecond):
		t.Error("Events channel should close after context cancellation")
	}
}

func TestDeduplication(t *testing.T) {
	d := New("test-session", nil)
	d.Config.DedupWindow = 100 * time.Millisecond

	// Record an event
	d.mu.Lock()
	d.recentEvents["bd-test"] = time.Now()
	d.mu.Unlock()

	// Check if within dedup window
	d.mu.RLock()
	lastEvent, exists := d.recentEvents["bd-test"]
	d.mu.RUnlock()

	if !exists {
		t.Error("Event should exist in recentEvents")
	}
	if time.Since(lastEvent) >= d.Config.DedupWindow {
		t.Error("Event should be within dedup window")
	}
}

func TestBrAvailableCaching(t *testing.T) {
	d := New("test-session", nil)

	// First call checks availability
	result1 := d.isBrAvailable()

	// Second call should use cache
	result2 := d.isBrAvailable()

	if result1 != result2 {
		t.Error("isBrAvailable should return consistent results")
	}

	// Verify cache is set
	d.mu.RLock()
	defer d.mu.RUnlock()
	if d.brAvailable == nil {
		t.Error("brAvailable cache should be set after first call")
	}
}

// TestConcurrentDedup tests concurrent access to the deduplication mechanism
// to verify thread-safety under race conditions. Run with: go test -race
func TestConcurrentDedup(t *testing.T) {
	d := New("test-session", nil)
	d.Config.DedupWindow = 100 * time.Millisecond

	var wg sync.WaitGroup
	numGoroutines := 10
	eventsPerGoroutine := 20

	// Concurrent writes to recentEvents
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func(goroutineID int) {
			defer wg.Done()
			for j := 0; j < eventsPerGoroutine; j++ {
				beadID := fmt.Sprintf("bd-%d-%d", goroutineID, j)
				d.mu.Lock()
				d.recentEvents[beadID] = time.Now()
				d.mu.Unlock()

				// Also do some concurrent reads
				d.mu.RLock()
				_ = d.recentEvents[beadID]
				d.mu.RUnlock()
			}
		}(i)
	}

	// Concurrent reads
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < eventsPerGoroutine; j++ {
				d.mu.RLock()
				_ = len(d.recentEvents)
				d.mu.RUnlock()
			}
		}()
	}

	wg.Wait()

	// Verify all events were recorded
	d.mu.RLock()
	expectedCount := numGoroutines * eventsPerGoroutine
	actualCount := len(d.recentEvents)
	d.mu.RUnlock()

	if actualCount != expectedCount {
		t.Errorf("expected %d events, got %d", expectedCount, actualCount)
	}
}

// TestConcurrentActivityTracking tests concurrent access to activity tracker
func TestConcurrentActivityTracking(t *testing.T) {
	d := New("test-session", nil)

	var wg sync.WaitGroup
	numGoroutines := 10
	operationsPerGoroutine := 20

	// Concurrent activity tracker updates
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func(pane int) {
			defer wg.Done()
			for j := 0; j < operationsPerGoroutine; j++ {
				d.mu.Lock()
				if d.activityTracker[pane] == nil {
					d.activityTracker[pane] = &activityState{}
				}
				d.activityTracker[pane].lastOutputTime = time.Now()
				d.activityTracker[pane].lastOutput = fmt.Sprintf("output-%d", j)
				d.mu.Unlock()

				// Concurrent read
				d.mu.RLock()
				_ = d.activityTracker[pane]
				d.mu.RUnlock()
			}
		}(i)
	}

	wg.Wait()

	// Verify all panes were tracked
	d.mu.RLock()
	actualPanes := len(d.activityTracker)
	d.mu.RUnlock()

	if actualPanes != numGoroutines {
		t.Errorf("expected %d panes tracked, got %d", numGoroutines, actualPanes)
	}
}
