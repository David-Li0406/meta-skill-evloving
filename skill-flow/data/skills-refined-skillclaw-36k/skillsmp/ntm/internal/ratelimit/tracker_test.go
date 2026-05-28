// Package ratelimit provides rate limit tracking and adaptive delay management for AI agents.
package ratelimit

import (
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func TestNewRateLimitTracker(t *testing.T) {
	tracker := NewRateLimitTracker("/tmp/test")
	if tracker == nil {
		t.Fatal("NewRateLimitTracker returned nil")
	}
	if tracker.dataDir != "/tmp/test" {
		t.Errorf("dataDir = %q, want %q", tracker.dataDir, "/tmp/test")
	}
	if tracker.state == nil {
		t.Error("state map should not be nil")
	}
	if tracker.history == nil {
		t.Error("history map should not be nil")
	}
}

func TestGetDefaultDelay(t *testing.T) {
	tests := []struct {
		provider string
		want     time.Duration
	}{
		{"anthropic", DefaultDelayAnthropic},
		{"claude", DefaultDelayAnthropic},
		{"openai", DefaultDelayOpenAI},
		{"gpt", DefaultDelayOpenAI},
		{"google", DefaultDelayGoogle},
		{"gemini", DefaultDelayGoogle},
		{"unknown", DefaultDelayOpenAI},
	}

	for _, tt := range tests {
		t.Run(tt.provider, func(t *testing.T) {
			got := getDefaultDelay(tt.provider)
			if got != tt.want {
				t.Errorf("getDefaultDelay(%q) = %v, want %v", tt.provider, got, tt.want)
			}
		})
	}
}

func TestGetMinDelay(t *testing.T) {
	tests := []struct {
		provider string
		want     time.Duration
	}{
		{"anthropic", MinDelayAnthropic},
		{"openai", MinDelayOpenAI},
		{"google", MinDelayGoogle},
		{"unknown", MinDelayOpenAI},
	}

	for _, tt := range tests {
		t.Run(tt.provider, func(t *testing.T) {
			got := getMinDelay(tt.provider)
			if got != tt.want {
				t.Errorf("getMinDelay(%q) = %v, want %v", tt.provider, got, tt.want)
			}
		})
	}
}

func TestGetOptimalDelay_Default(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Should return default for unknown provider
	delay := tracker.GetOptimalDelay("anthropic")
	if delay != DefaultDelayAnthropic {
		t.Errorf("GetOptimalDelay() = %v, want %v", delay, DefaultDelayAnthropic)
	}
}

func TestRecordRateLimit(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Record a rate limit
	tracker.RecordRateLimit("anthropic", "spawn")

	// Check that delay increased by 50%
	state := tracker.GetProviderState("anthropic")
	if state == nil {
		t.Fatal("state should not be nil")
	}

	expectedDelay := time.Duration(float64(DefaultDelayAnthropic) * delayIncreaseRate)
	if state.CurrentDelay != expectedDelay {
		t.Errorf("CurrentDelay = %v, want %v", state.CurrentDelay, expectedDelay)
	}
	if state.TotalRateLimits != 1 {
		t.Errorf("TotalRateLimits = %d, want 1", state.TotalRateLimits)
	}
	if state.ConsecutiveSuccess != 0 {
		t.Errorf("ConsecutiveSuccess = %d, want 0", state.ConsecutiveSuccess)
	}
}

func TestRecordSuccess(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Record 9 successes - should not decrease yet
	for i := 0; i < 9; i++ {
		tracker.RecordSuccess("anthropic")
	}

	state := tracker.GetProviderState("anthropic")
	if state.CurrentDelay != DefaultDelayAnthropic {
		t.Errorf("Delay should not change before %d successes, got %v", successesBeforeDecrease, state.CurrentDelay)
	}

	// 10th success should trigger decrease
	tracker.RecordSuccess("anthropic")

	state = tracker.GetProviderState("anthropic")
	expectedDelay := time.Duration(float64(DefaultDelayAnthropic) * delayDecreaseRate)
	if state.CurrentDelay != expectedDelay {
		t.Errorf("CurrentDelay = %v, want %v after 10 successes", state.CurrentDelay, expectedDelay)
	}
	if state.TotalSuccesses != 10 {
		t.Errorf("TotalSuccesses = %d, want 10", state.TotalSuccesses)
	}
}

func TestRecordSuccess_RespectMinDelay(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Manually set delay to just above minimum
	tracker.mu.Lock()
	tracker.state["anthropic"] = &ProviderState{
		CurrentDelay: MinDelayAnthropic + time.Second,
	}
	tracker.mu.Unlock()

	// Record 10 successes - should not go below min
	for i := 0; i < 10; i++ {
		tracker.RecordSuccess("anthropic")
	}

	state := tracker.GetProviderState("anthropic")
	if state.CurrentDelay < MinDelayAnthropic {
		t.Errorf("Delay should not go below min %v, got %v", MinDelayAnthropic, state.CurrentDelay)
	}
}

func TestRecordRateLimit_ResetsConsecutiveSuccess(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Build up some successes
	for i := 0; i < 5; i++ {
		tracker.RecordSuccess("anthropic")
	}

	state := tracker.GetProviderState("anthropic")
	if state.ConsecutiveSuccess != 5 {
		t.Errorf("ConsecutiveSuccess = %d, want 5", state.ConsecutiveSuccess)
	}

	// Rate limit should reset consecutive successes
	tracker.RecordRateLimit("anthropic", "send")

	state = tracker.GetProviderState("anthropic")
	if state.ConsecutiveSuccess != 0 {
		t.Errorf("ConsecutiveSuccess should reset to 0 after rate limit, got %d", state.ConsecutiveSuccess)
	}
}

func TestGetRecentEvents(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Record some events
	tracker.RecordRateLimit("anthropic", "spawn")
	tracker.RecordRateLimit("anthropic", "send")
	tracker.RecordRateLimit("anthropic", "spawn")

	events := tracker.GetRecentEvents("anthropic", 2)
	if len(events) != 2 {
		t.Errorf("GetRecentEvents() returned %d events, want 2", len(events))
	}

	// Should be most recent events
	if events[1].Action != "spawn" {
		t.Errorf("Most recent event action = %q, want 'spawn'", events[1].Action)
	}
}

func TestGetRecentEvents_Empty(t *testing.T) {
	tracker := NewRateLimitTracker("")

	events := tracker.GetRecentEvents("anthropic", 5)
	if events != nil {
		t.Error("GetRecentEvents should return nil for empty history")
	}
}

func TestGetAllProviders(t *testing.T) {
	tracker := NewRateLimitTracker("")

	tracker.RecordSuccess("anthropic")
	tracker.RecordSuccess("openai")
	tracker.RecordSuccess("google")

	providers := tracker.GetAllProviders()
	if len(providers) != 3 {
		t.Errorf("GetAllProviders() returned %d providers, want 3", len(providers))
	}
}

func TestReset(t *testing.T) {
	tracker := NewRateLimitTracker("")

	tracker.RecordRateLimit("anthropic", "spawn")
	tracker.RecordSuccess("anthropic")

	tracker.Reset("anthropic")

	state := tracker.GetProviderState("anthropic")
	if state != nil {
		t.Error("state should be nil after Reset")
	}

	events := tracker.GetRecentEvents("anthropic", 10)
	if events != nil {
		t.Error("events should be nil after Reset")
	}
}

func TestResetAll(t *testing.T) {
	tracker := NewRateLimitTracker("")

	tracker.RecordRateLimit("anthropic", "spawn")
	tracker.RecordRateLimit("openai", "send")

	tracker.ResetAll()

	providers := tracker.GetAllProviders()
	if len(providers) != 0 {
		t.Errorf("GetAllProviders() should return empty after ResetAll, got %d", len(providers))
	}
}

func TestPersistence(t *testing.T) {
	tmpDir := t.TempDir()

	// Create tracker and record data
	tracker1 := NewRateLimitTracker(tmpDir)
	tracker1.RecordRateLimit("anthropic", "spawn")
	tracker1.RecordSuccess("anthropic")
	tracker1.RecordSuccess("openai")

	// Save
	if err := tracker1.SaveToDir(tmpDir); err != nil {
		t.Fatalf("SaveToDir failed: %v", err)
	}

	// Verify file exists
	path := filepath.Join(tmpDir, ".ntm", "rate_limits.json")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Fatal("rate_limits.json not created")
	}

	// Create new tracker and load
	tracker2 := NewRateLimitTracker(tmpDir)
	if err := tracker2.LoadFromDir(tmpDir); err != nil {
		t.Fatalf("LoadFromDir failed: %v", err)
	}

	// Verify data was loaded correctly
	state := tracker2.GetProviderState("anthropic")
	if state == nil {
		t.Fatal("anthropic state not loaded")
	}
	if state.TotalRateLimits != 1 {
		t.Errorf("TotalRateLimits = %d, want 1", state.TotalRateLimits)
	}
	if state.TotalSuccesses != 1 {
		t.Errorf("TotalSuccesses = %d, want 1", state.TotalSuccesses)
	}

	// Check openai was also loaded
	openaiState := tracker2.GetProviderState("openai")
	if openaiState == nil {
		t.Fatal("openai state not loaded")
	}
}

func TestLoadFromDir_NoFile(t *testing.T) {
	tmpDir := t.TempDir()
	tracker := NewRateLimitTracker(tmpDir)

	// Should not error when file doesn't exist
	if err := tracker.LoadFromDir(tmpDir); err != nil {
		t.Errorf("LoadFromDir should not error for missing file: %v", err)
	}
}

func TestConcurrent(t *testing.T) {
	tracker := NewRateLimitTracker("")
	var wg sync.WaitGroup

	// Simulate concurrent access from multiple goroutines
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			provider := "anthropic"
			if id%2 == 0 {
				provider = "openai"
			}
			for j := 0; j < 100; j++ {
				if j%10 == 0 {
					tracker.RecordRateLimit(provider, "spawn")
				} else {
					tracker.RecordSuccess(provider)
				}
				_ = tracker.GetOptimalDelay(provider)
			}
		}(i)
	}

	wg.Wait()

	// Should have tracked both providers without panic
	providers := tracker.GetAllProviders()
	if len(providers) != 2 {
		t.Errorf("Expected 2 providers, got %d", len(providers))
	}
}

func TestFormatDelay(t *testing.T) {
	tests := []struct {
		delay time.Duration
		want  string
	}{
		{500 * time.Millisecond, "500ms"},
		{1 * time.Second, "1.0s"},
		{5500 * time.Millisecond, "5.5s"},
		{90 * time.Second, "1.5m"},
	}

	for _, tt := range tests {
		t.Run(tt.want, func(t *testing.T) {
			got := FormatDelay(tt.delay)
			if got != tt.want {
				t.Errorf("FormatDelay(%v) = %q, want %q", tt.delay, got, tt.want)
			}
		})
	}
}

func TestNormalizeProvider(t *testing.T) {
	tests := []struct {
		input string
		want  string
	}{
		{"anthropic", "anthropic"},
		{"claude", "anthropic"},
		{"claude-code", "anthropic"},
		{"cc", "anthropic"},
		{"openai", "openai"},
		{"gpt", "openai"},
		{"chatgpt", "openai"},
		{"codex", "openai"},
		{"cod", "openai"},
		{"google", "google"},
		{"gemini", "google"},
		{"gmi", "google"},
		{"unknown", "unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := NormalizeProvider(tt.input)
			if got != tt.want {
				t.Errorf("NormalizeProvider(%q) = %q, want %q", tt.input, got, tt.want)
			}
		})
	}
}

func TestHistoryTruncation(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Record more than 100 events
	for i := 0; i < 150; i++ {
		tracker.RecordRateLimit("anthropic", "spawn")
	}

	events := tracker.GetRecentEvents("anthropic", 200)
	if len(events) > 100 {
		t.Errorf("History should be truncated to 100, got %d", len(events))
	}
}

func TestGetProviderState_ReturnsCopy(t *testing.T) {
	tracker := NewRateLimitTracker("")
	tracker.RecordSuccess("anthropic")

	// Get state
	state1 := tracker.GetProviderState("anthropic")

	// Modify the returned state
	state1.TotalSuccesses = 999

	// Get state again - should not reflect the modification
	state2 := tracker.GetProviderState("anthropic")
	if state2.TotalSuccesses == 999 {
		t.Error("GetProviderState should return a copy, not the original")
	}
}

func TestAdaptiveLearning_MultipleRateLimits(t *testing.T) {
	tracker := NewRateLimitTracker("")

	// Record 3 consecutive rate limits
	tracker.RecordRateLimit("anthropic", "spawn")
	tracker.RecordRateLimit("anthropic", "spawn")
	tracker.RecordRateLimit("anthropic", "spawn")

	state := tracker.GetProviderState("anthropic")

	// Delay should be: 15s * 1.5 * 1.5 * 1.5 = 50.625s
	expectedDelay := time.Duration(float64(DefaultDelayAnthropic) * delayIncreaseRate * delayIncreaseRate * delayIncreaseRate)
	if state.CurrentDelay != expectedDelay {
		t.Errorf("CurrentDelay = %v, want %v after 3 rate limits", state.CurrentDelay, expectedDelay)
	}
}
