package state

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestNewTimelineLifecycle(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	tracker := NewTimelineTracker(nil)

	lifecycle, err := NewTimelineLifecycle(tracker, persister)
	if err != nil {
		t.Fatalf("NewTimelineLifecycle failed: %v", err)
	}

	if lifecycle.GetTracker() != tracker {
		t.Error("GetTracker returned wrong tracker")
	}

	if lifecycle.GetPersister() != persister {
		t.Error("GetPersister returned wrong persister")
	}

	t.Log("PASS: NewTimelineLifecycle creates lifecycle manager correctly")
}

func TestTimelineLifecycleStartSession(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{
		BaseDir:            tmpDir,
		CheckpointInterval: 100 * time.Millisecond, // Short interval for testing
	}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	tracker := NewTimelineTracker(nil)

	lifecycle, err := NewTimelineLifecycle(tracker, persister)
	if err != nil {
		t.Fatalf("NewTimelineLifecycle failed: %v", err)
	}
	defer lifecycle.Stop()

	sessionID := "test-session"

	// Start session
	lifecycle.StartSession(sessionID)

	if !lifecycle.IsSessionActive(sessionID) {
		t.Error("Session should be active after StartSession")
	}

	sessions := lifecycle.ActiveSessions()
	if len(sessions) != 1 || sessions[0] != sessionID {
		t.Errorf("Expected active sessions [%s], got %v", sessionID, sessions)
	}

	// Starting same session again should be idempotent
	lifecycle.StartSession(sessionID)
	sessions = lifecycle.ActiveSessions()
	if len(sessions) != 1 {
		t.Errorf("Expected 1 active session after duplicate start, got %d", len(sessions))
	}

	t.Log("PASS: StartSession activates timeline tracking")
}

func TestTimelineLifecycleEndSession(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	tracker := NewTimelineTracker(nil)

	lifecycle, err := NewTimelineLifecycle(tracker, persister)
	if err != nil {
		t.Fatalf("NewTimelineLifecycle failed: %v", err)
	}
	defer lifecycle.Stop()

	sessionID := "end-test-session"

	// Record some events
	tracker.RecordEvent(AgentEvent{
		AgentID:   "cc_1",
		SessionID: sessionID,
		State:     TimelineWorking,
		Timestamp: time.Now(),
	})
	tracker.RecordEvent(AgentEvent{
		AgentID:   "cc_1",
		SessionID: sessionID,
		State:     TimelineIdle,
		Timestamp: time.Now().Add(time.Second),
	})

	// Start and then end session
	lifecycle.StartSession(sessionID)
	err = lifecycle.EndSession(sessionID)
	if err != nil {
		t.Fatalf("EndSession failed: %v", err)
	}

	if lifecycle.IsSessionActive(sessionID) {
		t.Error("Session should not be active after EndSession")
	}

	// Verify timeline was saved
	path := filepath.Join(tmpDir, sessionID+".jsonl")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Error("Timeline file should exist after EndSession")
	}

	// Verify events were persisted
	events, err := persister.LoadTimeline(sessionID)
	if err != nil {
		t.Fatalf("LoadTimeline failed: %v", err)
	}

	if len(events) != 2 {
		t.Errorf("Expected 2 events, got %d", len(events))
	}

	t.Log("PASS: EndSession finalizes and persists timeline")
}

func TestTimelineLifecycleMultipleSessions(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	tracker := NewTimelineTracker(nil)

	lifecycle, err := NewTimelineLifecycle(tracker, persister)
	if err != nil {
		t.Fatalf("NewTimelineLifecycle failed: %v", err)
	}
	defer lifecycle.Stop()

	// Start multiple sessions
	sessions := []string{"session-a", "session-b", "session-c"}
	for _, s := range sessions {
		lifecycle.StartSession(s)
	}

	activeSessions := lifecycle.ActiveSessions()
	if len(activeSessions) != 3 {
		t.Errorf("Expected 3 active sessions, got %d", len(activeSessions))
	}

	// End one session
	err = lifecycle.EndSession("session-b")
	if err != nil {
		t.Fatalf("EndSession failed: %v", err)
	}

	activeSessions = lifecycle.ActiveSessions()
	if len(activeSessions) != 2 {
		t.Errorf("Expected 2 active sessions after ending one, got %d", len(activeSessions))
	}

	t.Log("PASS: Multiple sessions can be tracked concurrently")
}

func TestTimelineLifecycleStop(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	tracker := NewTimelineTracker(nil)

	lifecycle, err := NewTimelineLifecycle(tracker, persister)
	if err != nil {
		t.Fatalf("NewTimelineLifecycle failed: %v", err)
	}

	// Start sessions
	lifecycle.StartSession("session-1")
	lifecycle.StartSession("session-2")

	// Add events
	for _, s := range []string{"session-1", "session-2"} {
		tracker.RecordEvent(AgentEvent{
			AgentID:   "cc_1",
			SessionID: s,
			State:     TimelineWorking,
			Timestamp: time.Now(),
		})
	}

	// Stop should finalize all sessions
	lifecycle.Stop()

	// Verify all timelines were saved
	for _, s := range []string{"session-1", "session-2"} {
		events, err := persister.LoadTimeline(s)
		if err != nil {
			t.Errorf("LoadTimeline for %s failed: %v", s, err)
		}
		if len(events) == 0 {
			t.Errorf("Expected events for %s to be persisted", s)
		}
	}

	t.Log("PASS: Stop finalizes all active sessions")
}

func TestStartSessionTimeline(t *testing.T) {
	// This tests the convenience function
	// Note: This uses the global lifecycle, so we need to be careful about state

	sessionID := "convenience-test-" + time.Now().Format("20060102150405")

	err := StartSessionTimeline(sessionID)
	if err != nil {
		t.Fatalf("StartSessionTimeline failed: %v", err)
	}

	lifecycle, err := GetGlobalTimelineLifecycle()
	if err != nil {
		t.Fatalf("GetGlobalTimelineLifecycle failed: %v", err)
	}

	if !lifecycle.IsSessionActive(sessionID) {
		t.Error("Session should be active after StartSessionTimeline")
	}

	// Clean up
	_ = EndSessionTimeline(sessionID)

	t.Log("PASS: StartSessionTimeline convenience function works")
}

func TestEndSessionTimeline(t *testing.T) {
	sessionID := "end-convenience-test-" + time.Now().Format("20060102150405")

	// Start first
	err := StartSessionTimeline(sessionID)
	if err != nil {
		t.Fatalf("StartSessionTimeline failed: %v", err)
	}

	// End session
	err = EndSessionTimeline(sessionID)
	if err != nil {
		t.Fatalf("EndSessionTimeline failed: %v", err)
	}

	lifecycle, err := GetGlobalTimelineLifecycle()
	if err != nil {
		t.Fatalf("GetGlobalTimelineLifecycle failed: %v", err)
	}

	if lifecycle.IsSessionActive(sessionID) {
		t.Error("Session should not be active after EndSessionTimeline")
	}

	t.Log("PASS: EndSessionTimeline convenience function works")
}

func TestGetGlobalTimelineTracker(t *testing.T) {
	tracker := GetGlobalTimelineTracker()
	if tracker == nil {
		t.Fatal("GetGlobalTimelineTracker returned nil")
	}

	// Should return the same instance
	tracker2 := GetGlobalTimelineTracker()
	if tracker != tracker2 {
		t.Error("GetGlobalTimelineTracker should return singleton")
	}

	t.Log("PASS: GetGlobalTimelineTracker returns singleton")
}
