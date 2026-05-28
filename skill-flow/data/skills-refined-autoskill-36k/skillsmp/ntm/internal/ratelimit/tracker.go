// Package ratelimit provides rate limit tracking and adaptive delay management for AI agents.
package ratelimit

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// Default delays per provider (initial values before learning).
const (
	DefaultDelayAnthropic = 15 * time.Second
	DefaultDelayOpenAI    = 10 * time.Second
	DefaultDelayGoogle    = 8 * time.Second

	MinDelayAnthropic = 5 * time.Second
	MinDelayOpenAI    = 3 * time.Second
	MinDelayGoogle    = 2 * time.Second

	// Learning parameters
	delayIncreaseRate       = 1.5 // Increase by 50% on rate limit
	delayDecreaseRate       = 0.9 // Decrease by 10% on consecutive successes
	successesBeforeDecrease = 10  // Number of consecutive successes before decreasing delay
)

// RateLimitEvent represents a rate limit occurrence.
type RateLimitEvent struct {
	Time     time.Time `json:"time"`
	Provider string    `json:"provider"`
	Action   string    `json:"action"` // "spawn" or "send"
}

// ProviderState tracks the current state for a provider.
type ProviderState struct {
	CurrentDelay       time.Duration `json:"current_delay"`
	ConsecutiveSuccess int           `json:"consecutive_success"`
	LastRateLimit      time.Time     `json:"last_rate_limit,omitempty"`
	TotalRateLimits    int           `json:"total_rate_limits"`
	TotalSuccesses     int           `json:"total_successes"`
}

// RateLimitTracker tracks rate limit events and learns optimal spawn/send timing.
type RateLimitTracker struct {
	mu      sync.RWMutex
	history map[string][]RateLimitEvent // provider -> recent events
	state   map[string]*ProviderState   // provider -> current state
	dataDir string
}

// persistedData is the JSON structure for persistence.
type persistedData struct {
	State   map[string]*ProviderState   `json:"state"`
	History map[string][]RateLimitEvent `json:"history,omitempty"`
}

// NewRateLimitTracker creates a new RateLimitTracker instance.
// If dataDir is empty, persistence is disabled.
func NewRateLimitTracker(dataDir string) *RateLimitTracker {
	return &RateLimitTracker{
		history: make(map[string][]RateLimitEvent),
		state:   make(map[string]*ProviderState),
		dataDir: dataDir,
	}
}

// getDefaultDelay returns the default delay for a provider.
func getDefaultDelay(provider string) time.Duration {
	switch provider {
	case "anthropic", "claude":
		return DefaultDelayAnthropic
	case "openai", "gpt":
		return DefaultDelayOpenAI
	case "google", "gemini":
		return DefaultDelayGoogle
	default:
		return DefaultDelayOpenAI // Default to OpenAI timing
	}
}

// getMinDelay returns the minimum delay for a provider.
func getMinDelay(provider string) time.Duration {
	switch provider {
	case "anthropic", "claude":
		return MinDelayAnthropic
	case "openai", "gpt":
		return MinDelayOpenAI
	case "google", "gemini":
		return MinDelayGoogle
	default:
		return MinDelayOpenAI
	}
}

// getOrCreateState returns the provider state, creating it if needed.
func (t *RateLimitTracker) getOrCreateState(provider string) *ProviderState {
	if s, ok := t.state[provider]; ok {
		return s
	}
	s := &ProviderState{
		CurrentDelay: getDefaultDelay(provider),
	}
	t.state[provider] = s
	return s
}

// RecordRateLimit records a rate limit event and adjusts delays.
func (t *RateLimitTracker) RecordRateLimit(provider, action string) {
	provider = NormalizeProvider(provider)
	t.mu.Lock()
	defer t.mu.Unlock()

	now := time.Now()
	event := RateLimitEvent{
		Time:     now,
		Provider: provider,
		Action:   action,
	}

	// Add to history (keep last 100 events per provider)
	t.history[provider] = append(t.history[provider], event)
	if len(t.history[provider]) > 100 {
		t.history[provider] = t.history[provider][len(t.history[provider])-100:]
	}

	// Update state
	state := t.getOrCreateState(provider)
	state.LastRateLimit = now
	state.TotalRateLimits++
	state.ConsecutiveSuccess = 0 // Reset consecutive successes

	// Increase delay by 50%
	newDelay := time.Duration(float64(state.CurrentDelay) * delayIncreaseRate)
	state.CurrentDelay = newDelay
}

// RecordSuccess records a successful request.
func (t *RateLimitTracker) RecordSuccess(provider string) {
	provider = NormalizeProvider(provider)
	t.mu.Lock()
	defer t.mu.Unlock()

	state := t.getOrCreateState(provider)
	state.TotalSuccesses++
	state.ConsecutiveSuccess++

	// After 10 consecutive successes, decrease delay by 10%
	if state.ConsecutiveSuccess >= successesBeforeDecrease {
		minDelay := getMinDelay(provider)
		newDelay := time.Duration(float64(state.CurrentDelay) * delayDecreaseRate)
		if newDelay < minDelay {
			newDelay = minDelay
		}
		state.CurrentDelay = newDelay
		state.ConsecutiveSuccess = 0 // Reset counter
	}
}

// GetOptimalDelay returns the current optimal delay for a provider.
func (t *RateLimitTracker) GetOptimalDelay(provider string) time.Duration {
	provider = NormalizeProvider(provider)
	t.mu.RLock()
	defer t.mu.RUnlock()

	if state, ok := t.state[provider]; ok {
		return state.CurrentDelay
	}
	return getDefaultDelay(provider)
}

// GetProviderState returns a copy of the state for a provider.
func (t *RateLimitTracker) GetProviderState(provider string) *ProviderState {
	provider = NormalizeProvider(provider)
	t.mu.RLock()
	defer t.mu.RUnlock()

	state, ok := t.state[provider]
	if !ok {
		return nil
	}
	// Return a copy
	copy := *state
	return &copy
}

// GetAllProviders returns all tracked providers.
func (t *RateLimitTracker) GetAllProviders() []string {
	t.mu.RLock()
	defer t.mu.RUnlock()

	providers := make([]string, 0, len(t.state))
	for p := range t.state {
		providers = append(providers, p)
	}
	return providers
}

// GetRecentEvents returns recent rate limit events for a provider.
func (t *RateLimitTracker) GetRecentEvents(provider string, limit int) []RateLimitEvent {
	provider = NormalizeProvider(provider)
	t.mu.RLock()
	defer t.mu.RUnlock()

	events := t.history[provider]
	if len(events) == 0 {
		return nil
	}

	if limit <= 0 || limit > len(events) {
		limit = len(events)
	}

	// Return the most recent events
	result := make([]RateLimitEvent, limit)
	copy(result, events[len(events)-limit:])
	return result
}

// Reset resets the state for a provider to defaults.
func (t *RateLimitTracker) Reset(provider string) {
	provider = NormalizeProvider(provider)
	t.mu.Lock()
	defer t.mu.Unlock()

	delete(t.state, provider)
	delete(t.history, provider)
}

// ResetAll resets all provider states.
func (t *RateLimitTracker) ResetAll() {
	t.mu.Lock()
	defer t.mu.Unlock()

	t.state = make(map[string]*ProviderState)
	t.history = make(map[string][]RateLimitEvent)
}

// LoadFromDir loads rate limit data from the .ntm directory.
func (t *RateLimitTracker) LoadFromDir(dir string) error {
	if dir == "" {
		dir = t.dataDir
	}
	if dir == "" {
		return nil // persistence disabled
	}

	path := filepath.Join(dir, ".ntm", "rate_limits.json")
	// Read without lock (IO)
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // No file yet, that's fine
		}
		return fmt.Errorf("read rate limits file: %w", err)
	}

	var pd persistedData
	if err := json.Unmarshal(data, &pd); err != nil {
		return fmt.Errorf("parse rate limits file: %w", err)
	}

	t.mu.Lock()
	defer t.mu.Unlock()

	if pd.State != nil {
		t.state = pd.State
	}
	if pd.History != nil {
		t.history = pd.History
	}

	return nil
}

// SaveToDir saves rate limit data to the .ntm directory.
func (t *RateLimitTracker) SaveToDir(dir string) error {
	if dir == "" {
		dir = t.dataDir
	}
	if dir == "" {
		return nil // persistence disabled
	}

	t.mu.RLock()
	pd := persistedData{
		State:   make(map[string]*ProviderState),
		History: make(map[string][]RateLimitEvent),
	}
	// Deep copy to release lock early
	for k, v := range t.state {
		val := *v
		pd.State[k] = &val
	}
	for k, v := range t.history {
		pd.History[k] = append([]RateLimitEvent(nil), v...)
	}
	t.mu.RUnlock()

	ntmDir := filepath.Join(dir, ".ntm")
	if err := os.MkdirAll(ntmDir, 0755); err != nil {
		return fmt.Errorf("create .ntm dir: %w", err)
	}

	data, err := json.MarshalIndent(pd, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal rate limits: %w", err)
	}

	path := filepath.Join(ntmDir, "rate_limits.json")
	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("write rate limits file: %w", err)
	}

	return nil
}

// FormatDelay formats a duration as a human-readable string.
func FormatDelay(d time.Duration) string {
	if d < time.Second {
		return fmt.Sprintf("%dms", d.Milliseconds())
	}
	if d < time.Minute {
		return fmt.Sprintf("%.1fs", d.Seconds())
	}
	return fmt.Sprintf("%.1fm", d.Minutes())
}

// NormalizeProvider normalizes provider names to canonical forms.
func NormalizeProvider(provider string) string {
	switch provider {
	case "anthropic", "claude", "claude-code", "cc":
		return "anthropic"
	case "openai", "gpt", "chatgpt", "codex", "cod":
		return "openai"
	case "google", "gemini", "gmi":
		return "google"
	default:
		return provider
	}
}
