// Package startup provides two-phase initialization for NTM.
//
// Two-Phase Architecture:
//   - Phase 1 (Critical): Minimal startup for instant response
//     CLI argument parsing, simple flags (--version, --help, robot-version)
//   - Phase 2 (Deferred): Lazy loading of heavy resources
//     Config, tmux state, Agent Mail, bv/beads integration
//
// This architecture ensures NTM feels responsive even with complex initialization.
package startup

import (
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/profiler"
)

// Phase represents a startup phase
type Phase int

const (
	// PhaseNone indicates startup hasn't begun
	PhaseNone Phase = iota
	// Phase1 is critical/minimal startup
	Phase1
	// Phase2 is deferred/lazy loading
	Phase2
	// PhaseComplete indicates all initialization is done
	PhaseComplete
)

// Manager coordinates two-phase startup
type Manager struct {
	mu            sync.RWMutex
	currentPhase  Phase
	phase1Done    bool
	phase2Done    bool
	phase1Start   time.Time
	phase2Start   time.Time
	phase1Time    time.Duration
	phase2Time    time.Duration
	deferredFuncs []DeferredFunc
	initialized   map[string]bool
}

// DeferredFunc is a function to run during Phase 2
type DeferredFunc struct {
	Name string
	Fn   func() error
}

// global manager instance
var global = &Manager{
	initialized: make(map[string]bool),
}

// BeginPhase1 marks the start of Phase 1 (critical startup)
func BeginPhase1() {
	global.mu.Lock()
	defer global.mu.Unlock()
	global.currentPhase = Phase1
	global.phase1Start = time.Now()
	global.phase1Time = 0
	if profiler.IsEnabled() {
		// Create an instant marker span for phase1 start
		span := profiler.StartWithPhase("phase1_start", "startup")
		span.End()
	}
}

// EndPhase1 marks the completion of Phase 1
func EndPhase1() time.Duration {
	global.mu.Lock()
	defer global.mu.Unlock()
	if !global.phase1Start.IsZero() {
		global.phase1Time = time.Since(global.phase1Start)
	}
	global.phase1Done = true
	global.currentPhase = Phase2
	if profiler.IsEnabled() {
		span := profiler.Start("phase1_complete")
		span.Tag("phase", "startup")
		span.End()
	}
	return global.phase1Time
}

// BeginPhase2 marks the start of Phase 2 (deferred loading)
func BeginPhase2() {
	global.mu.Lock()
	defer global.mu.Unlock()
	global.currentPhase = Phase2
	global.phase2Start = time.Now()
	global.phase2Time = 0
	if profiler.IsEnabled() {
		// Create an instant marker span for phase2 start
		span := profiler.StartWithPhase("phase2_start", "deferred")
		span.End()
	}
}

// EndPhase2 marks the completion of Phase 2
func EndPhase2() time.Duration {
	global.mu.Lock()
	defer global.mu.Unlock()
	if !global.phase2Start.IsZero() {
		global.phase2Time = time.Since(global.phase2Start)
	}
	global.phase2Done = true
	global.currentPhase = PhaseComplete
	if profiler.IsEnabled() {
		span := profiler.Start("phase2_complete")
		span.Tag("phase", "deferred")
		span.End()
	}
	return global.phase2Time
}

// CurrentPhase returns the current startup phase
func CurrentPhase() Phase {
	global.mu.RLock()
	defer global.mu.RUnlock()
	return global.currentPhase
}

// IsPhase1Complete returns true if Phase 1 is done
func IsPhase1Complete() bool {
	global.mu.RLock()
	defer global.mu.RUnlock()
	return global.phase1Done
}

// IsPhase2Complete returns true if Phase 2 is done
func IsPhase2Complete() bool {
	global.mu.RLock()
	defer global.mu.RUnlock()
	return global.phase2Done
}

// RegisterDeferred adds a function to be run during Phase 2
func RegisterDeferred(name string, fn func() error) {
	global.mu.Lock()
	defer global.mu.Unlock()
	global.deferredFuncs = append(global.deferredFuncs, DeferredFunc{
		Name: name,
		Fn:   fn,
	})
}

// RunDeferred executes all registered deferred functions
func RunDeferred() error {
	global.mu.Lock()
	funcs := make([]DeferredFunc, len(global.deferredFuncs))
	copy(funcs, global.deferredFuncs)
	global.mu.Unlock()

	for _, df := range funcs {
		span := profiler.StartWithPhase(df.Name, "deferred")
		if err := df.Fn(); err != nil {
			span.Tag("error", err.Error())
			span.End()
			return err
		}
		span.End()
		markInitialized(df.Name)
	}
	return nil
}

// IsInitialized checks if a subsystem has been initialized
func IsInitialized(name string) bool {
	global.mu.RLock()
	defer global.mu.RUnlock()
	return global.initialized[name]
}

// markInitialized marks a subsystem as initialized
func markInitialized(name string) {
	global.mu.Lock()
	defer global.mu.Unlock()
	global.initialized[name] = true
}

// Reset clears all startup state (useful for testing)
func Reset() {
	global.mu.Lock()
	defer global.mu.Unlock()
	global.currentPhase = PhaseNone
	global.phase1Done = false
	global.phase2Done = false
	global.phase1Start = time.Time{}
	global.phase2Start = time.Time{}
	global.phase1Time = 0
	global.phase2Time = 0
	global.deferredFuncs = nil
	global.initialized = make(map[string]bool)
}

// Stats returns startup timing statistics
type Stats struct {
	CurrentPhase  Phase    `json:"current_phase"`
	Phase1Done    bool     `json:"phase1_done"`
	Phase2Done    bool     `json:"phase2_done"`
	Phase1TimeMs  float64  `json:"phase1_time_ms,omitempty"`
	Phase2TimeMs  float64  `json:"phase2_time_ms,omitempty"`
	DeferredCount int      `json:"deferred_count"`
	Initialized   []string `json:"initialized,omitempty"`
}

// GetStats returns current startup statistics
func GetStats() Stats {
	global.mu.RLock()
	defer global.mu.RUnlock()

	stats := Stats{
		CurrentPhase:  global.currentPhase,
		Phase1Done:    global.phase1Done,
		Phase2Done:    global.phase2Done,
		Phase1TimeMs:  float64(global.phase1Time.Nanoseconds()) / 1e6,
		Phase2TimeMs:  float64(global.phase2Time.Nanoseconds()) / 1e6,
		DeferredCount: len(global.deferredFuncs),
	}

	for name := range global.initialized {
		stats.Initialized = append(stats.Initialized, name)
	}

	return stats
}
