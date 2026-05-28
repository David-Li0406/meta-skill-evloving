// Package state provides durable SQLite-backed storage for NTM orchestration state.
// This file integrates timeline tracking and persistence with the session lifecycle.
package state

import (
	"sync"
)

// TimelineLifecycle manages the integration between TimelineTracker and
// TimelinePersister for automatic persistence during session lifecycle.
type TimelineLifecycle struct {
	mu        sync.Mutex
	tracker   *TimelineTracker
	persister *TimelinePersister

	// activeSessions tracks sessions with active checkpointing
	activeSessions map[string]struct{}
}

// NewTimelineLifecycle creates a new lifecycle manager with the given tracker and persister.
// If tracker is nil, uses the global tracker. If persister is nil, uses the default persister.
func NewTimelineLifecycle(tracker *TimelineTracker, persister *TimelinePersister) (*TimelineLifecycle, error) {
	if tracker == nil {
		tracker = GetGlobalTimelineTracker()
	}

	if persister == nil {
		var err error
		persister, err = GetDefaultTimelinePersister()
		if err != nil {
			return nil, err
		}
	}

	return &TimelineLifecycle{
		tracker:        tracker,
		persister:      persister,
		activeSessions: make(map[string]struct{}),
	}, nil
}

// StartSession begins timeline tracking and periodic persistence for a session.
// This should be called when a session is spawned.
func (l *TimelineLifecycle) StartSession(sessionID string) {
	l.mu.Lock()
	defer l.mu.Unlock()

	if _, active := l.activeSessions[sessionID]; active {
		return // Already tracking
	}

	l.activeSessions[sessionID] = struct{}{}
	l.persister.StartCheckpoint(sessionID, l.tracker)
}

// EndSession finalizes timeline persistence for a session.
// This should be called when a session is killed.
func (l *TimelineLifecycle) EndSession(sessionID string) error {
	l.mu.Lock()
	defer l.mu.Unlock()

	delete(l.activeSessions, sessionID)
	return l.persister.FinalizeSession(sessionID, l.tracker)
}

// IsSessionActive returns true if the session has active timeline tracking.
func (l *TimelineLifecycle) IsSessionActive(sessionID string) bool {
	l.mu.Lock()
	defer l.mu.Unlock()
	_, active := l.activeSessions[sessionID]
	return active
}

// ActiveSessions returns the list of sessions with active tracking.
func (l *TimelineLifecycle) ActiveSessions() []string {
	l.mu.Lock()
	defer l.mu.Unlock()

	sessions := make([]string, 0, len(l.activeSessions))
	for s := range l.activeSessions {
		sessions = append(sessions, s)
	}
	return sessions
}

// GetTracker returns the TimelineTracker.
func (l *TimelineLifecycle) GetTracker() *TimelineTracker {
	return l.tracker
}

// GetPersister returns the TimelinePersister.
func (l *TimelineLifecycle) GetPersister() *TimelinePersister {
	return l.persister
}

// Stop stops all active checkpoints and cleans up resources.
func (l *TimelineLifecycle) Stop() {
	l.mu.Lock()
	sessions := make([]string, 0, len(l.activeSessions))
	for s := range l.activeSessions {
		sessions = append(sessions, s)
	}
	l.mu.Unlock()

	// Finalize all active sessions
	for _, sessionID := range sessions {
		_ = l.EndSession(sessionID)
	}

	l.persister.Stop()
	l.tracker.Stop()
}

// Global singleton lifecycle manager
var (
	globalTimelineLifecycle     *TimelineLifecycle
	globalTimelineLifecycleOnce sync.Once
	globalTimelineLifecycleErr  error
)

// GetGlobalTimelineLifecycle returns the singleton lifecycle manager.
func GetGlobalTimelineLifecycle() (*TimelineLifecycle, error) {
	globalTimelineLifecycleOnce.Do(func() {
		globalTimelineLifecycle, globalTimelineLifecycleErr = NewTimelineLifecycle(nil, nil)
	})
	return globalTimelineLifecycle, globalTimelineLifecycleErr
}

// StartSessionTimeline is a convenience function to start timeline tracking for a session.
// It uses the global lifecycle manager.
func StartSessionTimeline(sessionID string) error {
	lifecycle, err := GetGlobalTimelineLifecycle()
	if err != nil {
		return err
	}
	lifecycle.StartSession(sessionID)
	return nil
}

// EndSessionTimeline is a convenience function to finalize timeline for a session.
// It uses the global lifecycle manager.
func EndSessionTimeline(sessionID string) error {
	lifecycle, err := GetGlobalTimelineLifecycle()
	if err != nil {
		return err
	}
	return lifecycle.EndSession(sessionID)
}
