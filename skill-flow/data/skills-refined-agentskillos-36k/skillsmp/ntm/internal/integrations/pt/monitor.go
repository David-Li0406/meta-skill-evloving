// Package pt provides integration with process_triage (pt) for Bayesian agent health monitoring.
// It monitors agent processes continuously and triggers alerts when agents become stuck or zombie.
package pt

import (
	"context"
	"fmt"
	"log/slog"
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/config"
	"github.com/Dicklesworthstone/ntm/internal/integrations/rano"
	"github.com/Dicklesworthstone/ntm/internal/tools"
)

var monitorLogger = slog.Default().With("component", "integrations.pt.monitor")

// Classification represents an agent's health classification.
type Classification string

const (
	ClassUseful  Classification = "useful"  // Agent is actively doing useful work
	ClassWaiting Classification = "waiting" // Agent is waiting for input/API response
	ClassIdle    Classification = "idle"    // Agent is idle but responsive
	ClassStuck   Classification = "stuck"   // Agent appears to be stuck/unresponsive
	ClassZombie  Classification = "zombie"  // Agent process is defunct
	ClassUnknown Classification = "unknown" // Unable to classify
)

// ClassificationEvent records a single classification result.
type ClassificationEvent struct {
	Classification Classification `json:"classification"`
	Confidence     float64        `json:"confidence"` // 0.0 to 1.0
	Timestamp      time.Time      `json:"timestamp"`
	Reason         string         `json:"reason,omitempty"`
	NetworkActive  bool           `json:"network_active,omitempty"` // From rano if available
}

// AgentState tracks the current state and history for an agent pane.
type AgentState struct {
	Pane             string                `json:"pane"`
	PID              int                   `json:"pid"`
	Classification   Classification        `json:"classification"`
	Confidence       float64               `json:"confidence"`
	Since            time.Time             `json:"since"` // When this classification started
	LastCheck        time.Time             `json:"last_check"`
	History          []ClassificationEvent `json:"history"`
	ConsecutiveCount int                   `json:"consecutive_count"` // How many times in a row this classification
}

// AlertType indicates the kind of alert being triggered.
type AlertType string

const (
	AlertStuck  AlertType = "stuck"
	AlertZombie AlertType = "zombie"
	AlertIdle   AlertType = "idle"
)

// Alert represents a health alert for an agent.
type Alert struct {
	Type      AlertType      `json:"type"`
	Pane      string         `json:"pane"`
	PID       int            `json:"pid"`
	State     Classification `json:"state"`
	Duration  time.Duration  `json:"duration"` // How long in this state
	Timestamp time.Time      `json:"timestamp"`
	Message   string         `json:"message"`
}

// HealthMonitor monitors agent health via process_triage.
type HealthMonitor struct {
	mu sync.RWMutex

	config      *config.ProcessTriageConfig
	pidMap      *rano.PIDMap
	ptAdapter   *tools.PTAdapter
	ranoAdapter *tools.RanoAdapter

	states  map[string]*AgentState // pane -> state
	alertCh chan Alert
	stopCh  chan struct{}
	doneCh  chan struct{}

	running bool
	session string
	useRano bool

	// Alert thresholds
	idleThreshold  time.Duration
	stuckThreshold time.Duration
	maxHistory     int // Maximum history entries to keep per agent
}

// HealthMonitorOption configures a HealthMonitor.
type HealthMonitorOption func(*HealthMonitor)

// WithSession sets the session to monitor (empty = all sessions).
func WithSession(session string) HealthMonitorOption {
	return func(m *HealthMonitor) {
		m.session = session
	}
}

// WithAlertChannel sets the channel for receiving alerts.
func WithAlertChannel(ch chan Alert) HealthMonitorOption {
	return func(m *HealthMonitor) {
		m.alertCh = ch
	}
}

// WithRano enables rano integration for improved classification.
func WithRano(enabled bool) HealthMonitorOption {
	return func(m *HealthMonitor) {
		m.useRano = enabled
	}
}

// NewHealthMonitor creates a new health monitor with the given configuration.
func NewHealthMonitor(cfg *config.ProcessTriageConfig, opts ...HealthMonitorOption) *HealthMonitor {
	m := &HealthMonitor{
		config:         cfg,
		states:         make(map[string]*AgentState),
		stopCh:         make(chan struct{}),
		doneCh:         make(chan struct{}),
		ptAdapter:      tools.NewPTAdapter(),
		ranoAdapter:    tools.NewRanoAdapter(),
		idleThreshold:  time.Duration(cfg.IdleThreshold) * time.Second,
		stuckThreshold: time.Duration(cfg.StuckThreshold) * time.Second,
		maxHistory:     100, // Keep last 100 classification events per agent
		useRano:        cfg.UseRanoData,
	}

	for _, opt := range opts {
		opt(m)
	}

	// Create PID map for the session
	m.pidMap = rano.NewPIDMap(m.session)

	// If no alert channel provided, create an internal one
	if m.alertCh == nil {
		m.alertCh = make(chan Alert, 100)
	}

	return m
}

// Start begins the monitoring loop.
// It's safe to call Start multiple times; subsequent calls are no-ops.
func (m *HealthMonitor) Start() error {
	m.mu.Lock()
	if m.running {
		m.mu.Unlock()
		return nil
	}

	// Verify pt is available
	ctx := context.Background()
	if !m.ptAdapter.IsAvailable(ctx) {
		m.mu.Unlock()
		return fmt.Errorf("process_triage (pt) is not available")
	}

	m.running = true
	m.stopCh = make(chan struct{})
	m.doneCh = make(chan struct{})
	m.mu.Unlock()

	go m.monitorLoop()

	monitorLogger.Info("health monitor started",
		"session", m.session,
		"check_interval", m.config.CheckInterval,
		"use_rano", m.useRano,
	)

	return nil
}

// Stop halts the monitoring loop.
// It blocks until the loop has fully stopped.
func (m *HealthMonitor) Stop() {
	m.mu.Lock()
	if !m.running {
		m.mu.Unlock()
		return
	}
	m.running = false
	close(m.stopCh)
	m.mu.Unlock()

	// Wait for loop to finish
	<-m.doneCh

	monitorLogger.Info("health monitor stopped")
}

// Running returns true if the monitor is currently running.
func (m *HealthMonitor) Running() bool {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return m.running
}

// Alerts returns the channel for receiving health alerts.
func (m *HealthMonitor) Alerts() <-chan Alert {
	return m.alertCh
}

// GetState returns the current state for a pane.
func (m *HealthMonitor) GetState(pane string) *AgentState {
	m.mu.RLock()
	defer m.mu.RUnlock()
	if state, ok := m.states[pane]; ok {
		// Return a copy to avoid data races
		stateCopy := *state
		return &stateCopy
	}
	return nil
}

// GetAllStates returns the current state for all monitored panes.
func (m *HealthMonitor) GetAllStates() map[string]*AgentState {
	m.mu.RLock()
	defer m.mu.RUnlock()

	result := make(map[string]*AgentState, len(m.states))
	for pane, state := range m.states {
		stateCopy := *state
		result[pane] = &stateCopy
	}
	return result
}

// monitorLoop is the main monitoring goroutine.
func (m *HealthMonitor) monitorLoop() {
	defer close(m.doneCh)

	interval := time.Duration(m.config.CheckInterval) * time.Second
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	// Do an initial check immediately
	m.checkAll()

	for {
		select {
		case <-ticker.C:
			m.checkAll()
		case <-m.stopCh:
			return
		}
	}
}

// checkAll checks the health of all agent processes.
func (m *HealthMonitor) checkAll() {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	// Refresh PID map to get current pane->PID mappings
	if err := m.pidMap.RefreshContext(ctx); err != nil {
		monitorLogger.Warn("failed to refresh PID map", "error", err)
		return
	}

	// Get all PIDs with their labels
	pidLabels := m.pidMap.GetPIDLabels()
	if len(pidLabels) == 0 {
		monitorLogger.Debug("no panes to monitor")
		return
	}

	// Collect all PIDs to classify
	pids := make([]int, 0, len(pidLabels))
	for pid := range pidLabels {
		pids = append(pids, pid)
	}

	// Classify all processes at once
	results, err := m.ptAdapter.ClassifyProcesses(ctx, pids)
	if err != nil {
		monitorLogger.Warn("failed to classify processes", "error", err)
		return
	}

	// Get rano stats if enabled
	var ranoStats map[int]*tools.RanoProcessStats
	if m.useRano && m.ranoAdapter.IsAvailable(ctx) {
		allStats, err := m.ranoAdapter.GetAllProcessStats(ctx)
		if err == nil {
			ranoStats = make(map[int]*tools.RanoProcessStats, len(allStats))
			for i := range allStats {
				ranoStats[allStats[i].PID] = &allStats[i]
			}
		}
	}

	// Process results
	m.mu.Lock()
	defer m.mu.Unlock()

	now := time.Now()
	seenPanes := make(map[string]bool)

	for _, result := range results {
		pane := pidLabels[result.PID]
		if pane == "" {
			continue
		}
		seenPanes[pane] = true

		// Convert pt classification to our classification
		classification := mapPTClassification(result.Classification)

		// Check rano for network activity
		networkActive := false
		if ranoStats != nil {
			if stats, ok := ranoStats[result.PID]; ok {
				// Consider network active if there was a request in the last check interval
				if stats.LastRequest != "" {
					if lastReq, err := time.Parse(time.RFC3339, stats.LastRequest); err == nil {
						networkActive = time.Since(lastReq) < time.Duration(m.config.CheckInterval)*time.Second
					}
				}
			}
		}

		// If network active and classified as stuck, downgrade to waiting
		if networkActive && classification == ClassStuck {
			classification = ClassWaiting
		}

		event := ClassificationEvent{
			Classification: classification,
			Confidence:     result.Confidence,
			Timestamp:      now,
			Reason:         result.Reason,
			NetworkActive:  networkActive,
		}

		m.updateState(pane, result.PID, event)
		m.checkAlerts(pane)
	}

	// Clean up states for panes that no longer exist
	for pane := range m.states {
		if !seenPanes[pane] {
			delete(m.states, pane)
			monitorLogger.Debug("removed stale pane state", "pane", pane)
		}
	}
}

// mapPTClassification converts pt classification to our classification.
func mapPTClassification(ptClass tools.PTClassification) Classification {
	switch ptClass {
	case tools.PTClassUseful:
		return ClassUseful
	case tools.PTClassAbandoned:
		return ClassStuck
	case tools.PTClassZombie:
		return ClassZombie
	default:
		return ClassUnknown
	}
}

// updateState updates the state for a pane with a new classification event.
// Must be called with m.mu held.
func (m *HealthMonitor) updateState(pane string, pid int, event ClassificationEvent) {
	state, exists := m.states[pane]
	if !exists {
		state = &AgentState{
			Pane:             pane,
			PID:              pid,
			Classification:   event.Classification,
			Confidence:       event.Confidence,
			Since:            event.Timestamp,
			LastCheck:        event.Timestamp,
			History:          make([]ClassificationEvent, 0, m.maxHistory),
			ConsecutiveCount: 1,
		}
		m.states[pane] = state
	} else {
		state.PID = pid
		state.LastCheck = event.Timestamp

		if state.Classification == event.Classification {
			state.ConsecutiveCount++
			state.Confidence = event.Confidence // Update confidence
		} else {
			// Classification changed
			state.Classification = event.Classification
			state.Confidence = event.Confidence
			state.Since = event.Timestamp
			state.ConsecutiveCount = 1
		}
	}

	// Add to history
	state.History = append(state.History, event)

	// Trim history if needed
	if len(state.History) > m.maxHistory {
		state.History = state.History[len(state.History)-m.maxHistory:]
	}
}

// checkAlerts checks if alerts should be triggered for a pane.
// Must be called with m.mu held.
func (m *HealthMonitor) checkAlerts(pane string) {
	state, ok := m.states[pane]
	if !ok {
		return
	}

	duration := time.Since(state.Since)

	switch state.Classification {
	case ClassStuck:
		if duration >= m.stuckThreshold {
			m.sendAlert(Alert{
				Type:      AlertStuck,
				Pane:      pane,
				PID:       state.PID,
				State:     state.Classification,
				Duration:  duration,
				Timestamp: time.Now(),
				Message:   fmt.Sprintf("Agent %s has been stuck for %v", pane, duration.Round(time.Second)),
			})
		}

	case ClassZombie:
		// Alert immediately for zombies
		m.sendAlert(Alert{
			Type:      AlertZombie,
			Pane:      pane,
			PID:       state.PID,
			State:     state.Classification,
			Duration:  duration,
			Timestamp: time.Now(),
			Message:   fmt.Sprintf("Agent %s is a zombie process", pane),
		})

	case ClassIdle:
		if duration >= m.idleThreshold {
			m.sendAlert(Alert{
				Type:      AlertIdle,
				Pane:      pane,
				PID:       state.PID,
				State:     state.Classification,
				Duration:  duration,
				Timestamp: time.Now(),
				Message:   fmt.Sprintf("Agent %s has been idle for %v", pane, duration.Round(time.Second)),
			})
		}
	}
}

// sendAlert sends an alert on the alert channel.
// Must be called with m.mu held.
func (m *HealthMonitor) sendAlert(alert Alert) {
	select {
	case m.alertCh <- alert:
		monitorLogger.Info("alert sent",
			"type", alert.Type,
			"pane", alert.Pane,
			"state", alert.State,
			"duration", alert.Duration,
		)
	default:
		monitorLogger.Warn("alert channel full, dropping alert",
			"type", alert.Type,
			"pane", alert.Pane,
		)
	}
}

// ForceCheck triggers an immediate health check outside the regular interval.
func (m *HealthMonitor) ForceCheck() {
	m.mu.RLock()
	running := m.running
	m.mu.RUnlock()

	if running {
		m.checkAll()
	}
}

// MonitorStats holds statistics about the health monitor.
type MonitorStats struct {
	Running        bool           `json:"running"`
	Session        string         `json:"session,omitempty"`
	CheckInterval  int            `json:"check_interval_seconds"`
	IdleThreshold  int            `json:"idle_threshold_seconds"`
	StuckThreshold int            `json:"stuck_threshold_seconds"`
	UseRano        bool           `json:"use_rano"`
	AgentCount     int            `json:"agent_count"`
	ByState        map[string]int `json:"by_state"`
	AlertsInQueue  int            `json:"alerts_in_queue"`
}

// GetStats returns statistics about the monitor.
func (m *HealthMonitor) GetStats() MonitorStats {
	m.mu.RLock()
	defer m.mu.RUnlock()

	byState := make(map[string]int)
	for _, state := range m.states {
		byState[string(state.Classification)]++
	}

	return MonitorStats{
		Running:        m.running,
		Session:        m.session,
		CheckInterval:  m.config.CheckInterval,
		IdleThreshold:  m.config.IdleThreshold,
		StuckThreshold: m.config.StuckThreshold,
		UseRano:        m.useRano,
		AgentCount:     len(m.states),
		ByState:        byState,
		AlertsInQueue:  len(m.alertCh),
	}
}

// Global singleton monitor

var (
	globalMonitor     *HealthMonitor
	globalMonitorOnce sync.Once
	globalMonitorMu   sync.RWMutex
)

// GetGlobalMonitor returns the global health monitor singleton.
// It uses the default ProcessTriageConfig from config.
func GetGlobalMonitor() *HealthMonitor {
	globalMonitorOnce.Do(func() {
		cfg := config.DefaultProcessTriageConfig()
		globalMonitor = NewHealthMonitor(&cfg)
	})
	return globalMonitor
}

// InitGlobalMonitor initializes the global monitor with the given config.
// This must be called before GetGlobalMonitor if custom config is desired.
func InitGlobalMonitor(cfg *config.ProcessTriageConfig, opts ...HealthMonitorOption) *HealthMonitor {
	globalMonitorMu.Lock()
	defer globalMonitorMu.Unlock()

	if globalMonitor != nil {
		globalMonitor.Stop()
	}

	globalMonitor = NewHealthMonitor(cfg, opts...)
	return globalMonitor
}
