package state

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestNewTimelinePersister(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{
		BaseDir:      tmpDir,
		MaxTimelines: 10,
	}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	if persister.config.BaseDir != tmpDir {
		t.Errorf("Expected BaseDir %q, got %q", tmpDir, persister.config.BaseDir)
	}

	if persister.config.MaxTimelines != 10 {
		t.Errorf("Expected MaxTimelines 10, got %d", persister.config.MaxTimelines)
	}

	// Verify directory was created
	if _, err := os.Stat(tmpDir); os.IsNotExist(err) {
		t.Error("Expected base directory to be created")
	}
}

func TestSaveAndLoadTimeline(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	sessionID := "test-session-1"
	now := time.Now()

	events := []AgentEvent{
		{
			AgentID:   "cc_1",
			AgentType: AgentTypeClaude,
			SessionID: sessionID,
			State:     TimelineWorking,
			Timestamp: now.Add(-5 * time.Minute),
			Details:   map[string]string{"task": "implementing feature"},
		},
		{
			AgentID:       "cc_1",
			AgentType:     AgentTypeClaude,
			SessionID:     sessionID,
			State:         TimelineIdle,
			PreviousState: TimelineWorking,
			Timestamp:     now.Add(-2 * time.Minute),
			Duration:      3 * time.Minute,
		},
		{
			AgentID:       "cc_1",
			AgentType:     AgentTypeClaude,
			SessionID:     sessionID,
			State:         TimelineWorking,
			PreviousState: TimelineIdle,
			Timestamp:     now,
			Duration:      2 * time.Minute,
		},
	}

	// Save
	t.Log("Saving timeline...")
	if err := persister.SaveTimeline(sessionID, events); err != nil {
		t.Fatalf("SaveTimeline failed: %v", err)
	}

	// Verify file exists
	path := filepath.Join(tmpDir, sessionID+".jsonl")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Fatal("Timeline file was not created")
	}

	// Load
	t.Log("Loading timeline...")
	loaded, err := persister.LoadTimeline(sessionID)
	if err != nil {
		t.Fatalf("LoadTimeline failed: %v", err)
	}

	if len(loaded) != len(events) {
		t.Fatalf("Expected %d events, got %d", len(events), len(loaded))
	}

	// Verify first event
	if loaded[0].AgentID != events[0].AgentID {
		t.Errorf("Expected AgentID %q, got %q", events[0].AgentID, loaded[0].AgentID)
	}
	if loaded[0].State != events[0].State {
		t.Errorf("Expected State %q, got %q", events[0].State, loaded[0].State)
	}

	t.Logf("PASS: Saved and loaded %d events successfully", len(loaded))
}

func TestLoadNonExistentTimeline(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	events, err := persister.LoadTimeline("nonexistent")
	if err != nil {
		t.Fatalf("LoadTimeline should not error for nonexistent: %v", err)
	}

	if events != nil {
		t.Error("Expected nil events for nonexistent timeline")
	}

	t.Log("PASS: Correctly returned nil for nonexistent timeline")
}

func TestListTimelines(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	// Create multiple timelines
	sessions := []string{"session-a", "session-b", "session-c"}
	for _, sessionID := range sessions {
		events := []AgentEvent{
			{
				AgentID:   "cc_1",
				SessionID: sessionID,
				State:     TimelineWorking,
				Timestamp: time.Now(),
			},
		}
		if err := persister.SaveTimeline(sessionID, events); err != nil {
			t.Fatalf("SaveTimeline failed for %s: %v", sessionID, err)
		}
	}

	// List
	timelines, err := persister.ListTimelines()
	if err != nil {
		t.Fatalf("ListTimelines failed: %v", err)
	}

	if len(timelines) != len(sessions) {
		t.Errorf("Expected %d timelines, got %d", len(sessions), len(timelines))
	}

	for _, ti := range timelines {
		t.Logf("Found timeline: %s (events=%d, size=%d bytes)",
			ti.SessionID, ti.EventCount, ti.Size)
	}

	t.Log("PASS: Listed all timelines correctly")
}

func TestDeleteTimeline(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	sessionID := "to-delete"
	events := []AgentEvent{
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
	}

	// Save
	if err := persister.SaveTimeline(sessionID, events); err != nil {
		t.Fatalf("SaveTimeline failed: %v", err)
	}

	// Verify exists
	loaded, err := persister.LoadTimeline(sessionID)
	if err != nil || len(loaded) == 0 {
		t.Fatal("Timeline should exist after save")
	}

	// Delete
	if err := persister.DeleteTimeline(sessionID); err != nil {
		t.Fatalf("DeleteTimeline failed: %v", err)
	}

	// Verify deleted
	loaded, err = persister.LoadTimeline(sessionID)
	if err != nil {
		t.Fatalf("LoadTimeline error after delete: %v", err)
	}
	if loaded != nil {
		t.Error("Timeline should be nil after deletion")
	}

	t.Log("PASS: Deleted timeline successfully")
}

func TestCleanupOldTimelines(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{
		BaseDir:      tmpDir,
		MaxTimelines: 3,
	}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	// Create 5 timelines
	for i := 0; i < 5; i++ {
		sessionID := "session-" + string(rune('a'+i))
		events := []AgentEvent{
			{AgentID: "cc_1", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
		}
		if err := persister.SaveTimeline(sessionID, events); err != nil {
			t.Fatalf("SaveTimeline failed: %v", err)
		}
		// Small delay to ensure different mod times
		time.Sleep(10 * time.Millisecond)
	}

	// Verify 5 exist
	timelines, _ := persister.ListTimelines()
	if len(timelines) != 5 {
		t.Fatalf("Expected 5 timelines before cleanup, got %d", len(timelines))
	}

	// Cleanup
	deleted, err := persister.Cleanup()
	if err != nil {
		t.Fatalf("Cleanup failed: %v", err)
	}

	t.Logf("Cleaned up %d timelines", deleted)

	// Verify only MaxTimelines remain
	timelines, _ = persister.ListTimelines()
	if len(timelines) > config.MaxTimelines {
		t.Errorf("Expected at most %d timelines after cleanup, got %d",
			config.MaxTimelines, len(timelines))
	}

	t.Log("PASS: Cleanup removed old timelines")
}

func TestEmptySessionIDError(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	// SaveTimeline with empty ID
	err = persister.SaveTimeline("", []AgentEvent{})
	if err == nil {
		t.Error("Expected error for empty session ID on save")
	}

	// LoadTimeline with empty ID
	_, err = persister.LoadTimeline("")
	if err == nil {
		t.Error("Expected error for empty session ID on load")
	}

	// DeleteTimeline with empty ID
	err = persister.DeleteTimeline("")
	if err == nil {
		t.Error("Expected error for empty session ID on delete")
	}

	t.Log("PASS: Empty session ID errors correctly")
}

func TestSaveTimelineOverwrite(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	sessionID := "overwrite-test"

	// First save with 2 events
	events1 := []AgentEvent{
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineIdle, Timestamp: time.Now()},
	}
	if err := persister.SaveTimeline(sessionID, events1); err != nil {
		t.Fatalf("First save failed: %v", err)
	}

	// Second save with 3 events (should overwrite)
	events2 := []AgentEvent{
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineIdle, Timestamp: time.Now()},
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineError, Timestamp: time.Now()},
	}
	if err := persister.SaveTimeline(sessionID, events2); err != nil {
		t.Fatalf("Second save failed: %v", err)
	}

	// Load and verify
	loaded, err := persister.LoadTimeline(sessionID)
	if err != nil {
		t.Fatalf("Load failed: %v", err)
	}

	if len(loaded) != 3 {
		t.Errorf("Expected 3 events after overwrite, got %d", len(loaded))
	}

	t.Log("PASS: Overwrite works correctly")
}

func TestTimelineWithMultipleAgents(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	sessionID := "multi-agent-session"
	now := time.Now()

	events := []AgentEvent{
		{AgentID: "cc_1", AgentType: AgentTypeClaude, SessionID: sessionID, State: TimelineWorking, Timestamp: now},
		{AgentID: "cod_1", AgentType: AgentTypeCodex, SessionID: sessionID, State: TimelineWorking, Timestamp: now.Add(1 * time.Second)},
		{AgentID: "gmi_1", AgentType: AgentTypeGemini, SessionID: sessionID, State: TimelineWorking, Timestamp: now.Add(2 * time.Second)},
		{AgentID: "cc_1", AgentType: AgentTypeClaude, SessionID: sessionID, State: TimelineIdle, Timestamp: now.Add(3 * time.Second)},
	}

	if err := persister.SaveTimeline(sessionID, events); err != nil {
		t.Fatalf("SaveTimeline failed: %v", err)
	}

	loaded, err := persister.LoadTimeline(sessionID)
	if err != nil {
		t.Fatalf("LoadTimeline failed: %v", err)
	}

	if len(loaded) != 4 {
		t.Errorf("Expected 4 events, got %d", len(loaded))
	}

	// Check agent diversity
	agents := make(map[string]bool)
	for _, e := range loaded {
		agents[e.AgentID] = true
	}

	if len(agents) != 3 {
		t.Errorf("Expected 3 unique agents, got %d", len(agents))
	}

	t.Logf("PASS: Multi-agent timeline with %d unique agents", len(agents))
}

func TestGetTimelineInfo(t *testing.T) {
	tmpDir := t.TempDir()
	config := &TimelinePersistConfig{BaseDir: tmpDir}

	persister, err := NewTimelinePersister(config)
	if err != nil {
		t.Fatalf("NewTimelinePersister failed: %v", err)
	}

	sessionID := "info-test"
	events := []AgentEvent{
		{AgentID: "cc_1", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
		{AgentID: "cc_2", SessionID: sessionID, State: TimelineWorking, Timestamp: time.Now()},
	}

	if err := persister.SaveTimeline(sessionID, events); err != nil {
		t.Fatalf("SaveTimeline failed: %v", err)
	}

	info, err := persister.GetTimelineInfo(sessionID)
	if err != nil {
		t.Fatalf("GetTimelineInfo failed: %v", err)
	}

	if info == nil {
		t.Fatal("Expected non-nil info")
	}

	if info.SessionID != sessionID {
		t.Errorf("Expected SessionID %q, got %q", sessionID, info.SessionID)
	}

	t.Logf("Timeline info: session=%s events=%d agents=%d size=%d",
		info.SessionID, info.EventCount, info.AgentCount, info.Size)

	t.Log("PASS: GetTimelineInfo works correctly")
}

func TestDefaultTimelinePersistConfig(t *testing.T) {
	config := DefaultTimelinePersistConfig()

	if config.MaxTimelines != 30 {
		t.Errorf("Expected MaxTimelines 30, got %d", config.MaxTimelines)
	}

	if config.CompressOlderThan != 24*time.Hour {
		t.Errorf("Expected CompressOlderThan 24h, got %v", config.CompressOlderThan)
	}

	if config.CheckpointInterval != 5*time.Minute {
		t.Errorf("Expected CheckpointInterval 5m, got %v", config.CheckpointInterval)
	}

	if config.BaseDir == "" {
		t.Error("Expected non-empty BaseDir")
	}

	t.Logf("Default config: BaseDir=%s MaxTimelines=%d CompressOlderThan=%v",
		config.BaseDir, config.MaxTimelines, config.CompressOlderThan)

	t.Log("PASS: Default config has sensible values")
}
