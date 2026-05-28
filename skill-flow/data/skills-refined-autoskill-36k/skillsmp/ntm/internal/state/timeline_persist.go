// Package state provides durable SQLite-backed storage for NTM orchestration state.
// This file implements timeline persistence for post-session analysis.
package state

import (
	"bufio"
	"compress/gzip"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"time"
)

// TimelineInfo contains metadata about a persisted timeline.
type TimelineInfo struct {
	SessionID  string    `json:"session_id"`
	Path       string    `json:"path"`
	EventCount int       `json:"event_count"`
	FirstEvent time.Time `json:"first_event,omitempty"`
	LastEvent  time.Time `json:"last_event,omitempty"`
	AgentCount int       `json:"agent_count"`
	Size       int64     `json:"size_bytes"`
	Compressed bool      `json:"compressed"`
	CreatedAt  time.Time `json:"created_at"`
	ModifiedAt time.Time `json:"modified_at"`
}

// TimelineHeader contains metadata stored at the beginning of a timeline file.
type TimelineHeader struct {
	Version    string    `json:"version"`
	SessionID  string    `json:"session_id"`
	CreatedAt  time.Time `json:"created_at"`
	AgentCount int       `json:"agent_count"`
	EventCount int       `json:"event_count"`
	FirstEvent time.Time `json:"first_event,omitempty"`
	LastEvent  time.Time `json:"last_event,omitempty"`
}

// TimelinePersistConfig configures timeline persistence behavior.
type TimelinePersistConfig struct {
	// BaseDir is the directory where timelines are stored.
	// Default: ~/.local/share/ntm/timelines
	BaseDir string

	// MaxTimelines is the maximum number of timelines to retain.
	// Older timelines are automatically deleted when this is exceeded.
	// Default: 30
	MaxTimelines int

	// CompressOlderThan compresses timelines older than this duration.
	// Set to 0 to disable compression.
	// Default: 24 hours
	CompressOlderThan time.Duration

	// CheckpointInterval is how often to save checkpoints during active sessions.
	// Default: 5 minutes
	CheckpointInterval time.Duration
}

// DefaultTimelinePersistConfig returns sensible defaults.
func DefaultTimelinePersistConfig() TimelinePersistConfig {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		homeDir = "."
	}

	return TimelinePersistConfig{
		BaseDir:            filepath.Join(homeDir, ".local", "share", "ntm", "timelines"),
		MaxTimelines:       30,
		CompressOlderThan:  24 * time.Hour,
		CheckpointInterval: 5 * time.Minute,
	}
}

// TimelinePersister handles saving and loading timeline data.
type TimelinePersister struct {
	mu     sync.RWMutex
	config TimelinePersistConfig

	// activeCheckpoints tracks checkpoint timers for active sessions
	activeCheckpoints map[string]*time.Ticker
	checkpointStop    map[string]chan struct{}
}

// NewTimelinePersister creates a new persister with the given configuration.
func NewTimelinePersister(config *TimelinePersistConfig) (*TimelinePersister, error) {
	cfg := DefaultTimelinePersistConfig()
	if config != nil {
		if config.BaseDir != "" {
			cfg.BaseDir = config.BaseDir
		}
		if config.MaxTimelines > 0 {
			cfg.MaxTimelines = config.MaxTimelines
		}
		if config.CompressOlderThan > 0 {
			cfg.CompressOlderThan = config.CompressOlderThan
		}
		if config.CheckpointInterval > 0 {
			cfg.CheckpointInterval = config.CheckpointInterval
		}
	}

	// Ensure base directory exists
	if err := os.MkdirAll(cfg.BaseDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create timeline directory: %w", err)
	}

	return &TimelinePersister{
		config:            cfg,
		activeCheckpoints: make(map[string]*time.Ticker),
		checkpointStop:    make(map[string]chan struct{}),
	}, nil
}

// SaveTimeline persists timeline events for a session to disk.
// The events are stored in JSONL format (one JSON object per line).
func (p *TimelinePersister) SaveTimeline(sessionID string, events []AgentEvent) error {
	if sessionID == "" {
		return errors.New("session ID cannot be empty")
	}

	p.mu.Lock()
	defer p.mu.Unlock()

	path := p.getTimelinePath(sessionID, false)

	// Ensure parent directory exists
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	file, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("failed to create timeline file: %w", err)
	}
	defer file.Close()

	// Write header
	header := TimelineHeader{
		Version:    "1.0",
		SessionID:  sessionID,
		CreatedAt:  time.Now(),
		AgentCount: countUniqueAgents(events),
		EventCount: len(events),
	}
	if len(events) > 0 {
		header.FirstEvent = events[0].Timestamp
		header.LastEvent = events[len(events)-1].Timestamp
	}

	encoder := json.NewEncoder(file)
	if err := encoder.Encode(header); err != nil {
		return fmt.Errorf("failed to write header: %w", err)
	}

	// Write events
	for _, event := range events {
		if err := encoder.Encode(event); err != nil {
			return fmt.Errorf("failed to write event: %w", err)
		}
	}

	return nil
}

// LoadTimeline reads timeline events for a session from disk.
func (p *TimelinePersister) LoadTimeline(sessionID string) ([]AgentEvent, error) {
	if sessionID == "" {
		return nil, errors.New("session ID cannot be empty")
	}

	p.mu.RLock()
	defer p.mu.RUnlock()

	// Try uncompressed first, then compressed
	path := p.getTimelinePath(sessionID, false)
	compressed := false
	if _, err := os.Stat(path); os.IsNotExist(err) {
		path = p.getTimelinePath(sessionID, true)
		compressed = true
	}

	file, err := os.Open(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil // No timeline exists
		}
		return nil, fmt.Errorf("failed to open timeline: %w", err)
	}
	defer file.Close()

	var reader io.Reader = file
	if compressed {
		gzReader, err := gzip.NewReader(file)
		if err != nil {
			return nil, fmt.Errorf("failed to create gzip reader: %w", err)
		}
		defer gzReader.Close()
		reader = gzReader
	}

	scanner := bufio.NewScanner(reader)
	// Increase buffer size for large lines
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 1024*1024)

	events := make([]AgentEvent, 0, 100)
	lineNum := 0

	for scanner.Scan() {
		lineNum++
		line := scanner.Bytes()

		// Skip empty lines
		if len(line) == 0 {
			continue
		}

		// First line is header - skip it
		if lineNum == 1 {
			continue
		}

		var event AgentEvent
		if err := json.Unmarshal(line, &event); err != nil {
			// Log and skip malformed lines
			continue
		}
		events = append(events, event)
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading timeline: %w", err)
	}

	return events, nil
}

// ListTimelines returns information about all persisted timelines.
func (p *TimelinePersister) ListTimelines() ([]TimelineInfo, error) {
	p.mu.RLock()
	defer p.mu.RUnlock()

	entries, err := os.ReadDir(p.config.BaseDir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to read timelines directory: %w", err)
	}

	timelines := make([]TimelineInfo, 0, len(entries))

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}

		name := entry.Name()
		if !strings.HasSuffix(name, ".jsonl") && !strings.HasSuffix(name, ".jsonl.gz") {
			continue
		}

		info, err := entry.Info()
		if err != nil {
			continue
		}

		// Extract session ID from filename
		sessionID := strings.TrimSuffix(strings.TrimSuffix(name, ".gz"), ".jsonl")
		compressed := strings.HasSuffix(name, ".gz")

		// Read header for event count and timestamps
		path := filepath.Join(p.config.BaseDir, name)
		header, err := p.readHeader(path, compressed)

		ti := TimelineInfo{
			SessionID:  sessionID,
			Path:       path,
			Size:       info.Size(),
			Compressed: compressed,
			CreatedAt:  info.ModTime(),
			ModifiedAt: info.ModTime(),
		}

		if err == nil && header != nil {
			ti.EventCount = header.EventCount
			ti.FirstEvent = header.FirstEvent
			ti.LastEvent = header.LastEvent
			ti.AgentCount = header.AgentCount
		}

		timelines = append(timelines, ti)
	}

	// Sort by modification time (newest first)
	sort.Slice(timelines, func(i, j int) bool {
		return timelines[i].ModifiedAt.After(timelines[j].ModifiedAt)
	})

	return timelines, nil
}

// DeleteTimeline removes a persisted timeline.
func (p *TimelinePersister) DeleteTimeline(sessionID string) error {
	if sessionID == "" {
		return errors.New("session ID cannot be empty")
	}

	p.mu.Lock()
	defer p.mu.Unlock()

	// Try to delete both compressed and uncompressed versions
	pathUncompressed := p.getTimelinePath(sessionID, false)
	pathCompressed := p.getTimelinePath(sessionID, true)

	var lastErr error
	if err := os.Remove(pathUncompressed); err != nil && !os.IsNotExist(err) {
		lastErr = err
	}
	if err := os.Remove(pathCompressed); err != nil && !os.IsNotExist(err) {
		lastErr = err
	}

	return lastErr
}

// Cleanup removes old timelines exceeding the configured maximum.
func (p *TimelinePersister) Cleanup() (int, error) {
	timelines, err := p.ListTimelines()
	if err != nil {
		return 0, err
	}

	if len(timelines) <= p.config.MaxTimelines {
		return 0, nil
	}

	// Sort by modification time (oldest first)
	sort.Slice(timelines, func(i, j int) bool {
		return timelines[i].ModifiedAt.Before(timelines[j].ModifiedAt)
	})

	// Delete excess timelines
	toDelete := len(timelines) - p.config.MaxTimelines
	deleted := 0

	for i := 0; i < toDelete; i++ {
		if err := p.DeleteTimeline(timelines[i].SessionID); err == nil {
			deleted++
		}
	}

	return deleted, nil
}

// CompressOldTimelines compresses timelines older than the configured threshold.
func (p *TimelinePersister) CompressOldTimelines() (int, error) {
	if p.config.CompressOlderThan <= 0 {
		return 0, nil
	}

	timelines, err := p.ListTimelines()
	if err != nil {
		return 0, err
	}

	cutoff := time.Now().Add(-p.config.CompressOlderThan)
	compressed := 0

	for _, ti := range timelines {
		if ti.Compressed || ti.ModifiedAt.After(cutoff) {
			continue
		}

		if err := p.compressTimeline(ti.SessionID); err == nil {
			compressed++
		}
	}

	return compressed, nil
}

// StartCheckpoint starts periodic checkpointing for a session.
func (p *TimelinePersister) StartCheckpoint(sessionID string, tracker *TimelineTracker) {
	p.mu.Lock()
	defer p.mu.Unlock()

	// Stop existing checkpoint if any
	if stop, exists := p.checkpointStop[sessionID]; exists {
		close(stop)
		delete(p.checkpointStop, sessionID)
	}
	if ticker, exists := p.activeCheckpoints[sessionID]; exists {
		ticker.Stop()
		delete(p.activeCheckpoints, sessionID)
	}

	ticker := time.NewTicker(p.config.CheckpointInterval)
	stop := make(chan struct{})

	p.activeCheckpoints[sessionID] = ticker
	p.checkpointStop[sessionID] = stop

	go func() {
		for {
			select {
			case <-ticker.C:
				events := tracker.GetEventsForSession(sessionID, time.Time{})
				if len(events) > 0 {
					_ = p.SaveTimeline(sessionID, events)
				}
			case <-stop:
				return
			}
		}
	}()
}

// StopCheckpoint stops periodic checkpointing for a session.
func (p *TimelinePersister) StopCheckpoint(sessionID string) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if stop, exists := p.checkpointStop[sessionID]; exists {
		close(stop)
		delete(p.checkpointStop, sessionID)
	}
	if ticker, exists := p.activeCheckpoints[sessionID]; exists {
		ticker.Stop()
		delete(p.activeCheckpoints, sessionID)
	}
}

// FinalizeSession saves the final state of a session's timeline and stops checkpointing.
func (p *TimelinePersister) FinalizeSession(sessionID string, tracker *TimelineTracker) error {
	p.StopCheckpoint(sessionID)

	events := tracker.GetEventsForSession(sessionID, time.Time{})
	if len(events) == 0 {
		return nil
	}

	return p.SaveTimeline(sessionID, events)
}

// GetTimelineInfo returns information about a specific timeline.
func (p *TimelinePersister) GetTimelineInfo(sessionID string) (*TimelineInfo, error) {
	timelines, err := p.ListTimelines()
	if err != nil {
		return nil, err
	}

	for _, ti := range timelines {
		if ti.SessionID == sessionID {
			return &ti, nil
		}
	}

	return nil, nil
}

// Stop stops all active checkpoints and cleans up resources.
func (p *TimelinePersister) Stop() {
	p.mu.Lock()
	defer p.mu.Unlock()

	for sessionID, stop := range p.checkpointStop {
		close(stop)
		delete(p.checkpointStop, sessionID)
	}

	for sessionID, ticker := range p.activeCheckpoints {
		ticker.Stop()
		delete(p.activeCheckpoints, sessionID)
	}
}

// Private helpers

func (p *TimelinePersister) getTimelinePath(sessionID string, compressed bool) string {
	filename := sessionID + ".jsonl"
	if compressed {
		filename += ".gz"
	}
	return filepath.Join(p.config.BaseDir, filename)
}

func (p *TimelinePersister) readHeader(path string, compressed bool) (*TimelineHeader, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var reader io.Reader = file
	if compressed {
		gzReader, err := gzip.NewReader(file)
		if err != nil {
			return nil, err
		}
		defer gzReader.Close()
		reader = gzReader
	}

	scanner := bufio.NewScanner(reader)
	if !scanner.Scan() {
		return nil, errors.New("empty file")
	}

	var header TimelineHeader
	if err := json.Unmarshal(scanner.Bytes(), &header); err != nil {
		return nil, err
	}

	return &header, nil
}

func (p *TimelinePersister) compressTimeline(sessionID string) error {
	srcPath := p.getTimelinePath(sessionID, false)
	dstPath := p.getTimelinePath(sessionID, true)

	// Read original file
	src, err := os.Open(srcPath)
	if err != nil {
		return err
	}
	defer src.Close()

	// Create compressed file
	dst, err := os.Create(dstPath)
	if err != nil {
		return err
	}
	defer dst.Close()

	gzWriter := gzip.NewWriter(dst)
	defer gzWriter.Close()

	if _, err := io.Copy(gzWriter, src); err != nil {
		os.Remove(dstPath)
		return err
	}

	// Close gzip writer to flush
	if err := gzWriter.Close(); err != nil {
		os.Remove(dstPath)
		return err
	}

	// Remove original after successful compression
	return os.Remove(srcPath)
}

func countUniqueAgents(events []AgentEvent) int {
	agents := make(map[string]struct{})
	for _, e := range events {
		agents[e.AgentID] = struct{}{}
	}
	return len(agents)
}

// DefaultTimelinePersister is the global timeline persister instance.
var (
	defaultTimelinePersister     *TimelinePersister
	defaultTimelinePersisterOnce sync.Once
)

// GetDefaultTimelinePersister returns the singleton timeline persister.
func GetDefaultTimelinePersister() (*TimelinePersister, error) {
	var initErr error
	defaultTimelinePersisterOnce.Do(func() {
		defaultTimelinePersister, initErr = NewTimelinePersister(nil)
	})
	if initErr != nil {
		return nil, initErr
	}
	return defaultTimelinePersister, nil
}
