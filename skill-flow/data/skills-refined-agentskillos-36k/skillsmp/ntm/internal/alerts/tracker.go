package alerts

import (
	"sync"
	"time"
)

// Tracker manages the lifecycle of alerts
type Tracker struct {
	mu         sync.RWMutex
	active     map[string]*Alert // keyed by alert ID
	resolved   []*Alert          // recently resolved alerts
	config     Config
	pruneAfter time.Duration
}

// NewTracker creates a new alert tracker
func NewTracker(cfg Config) *Tracker {
	return &Tracker{
		active:     make(map[string]*Alert),
		resolved:   make([]*Alert, 0),
		config:     cfg,
		pruneAfter: time.Duration(cfg.ResolvedPruneMinutes) * time.Minute,
	}
}

// Update processes new alerts and manages lifecycle.
// It adds new alerts, refreshes existing ones, and resolves alerts
// that are no longer detected.
// failedChecks is a list of sources that failed to report; alerts from these sources will be preserved.
func (t *Tracker) Update(detected []Alert, failedChecks []string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	now := time.Now()
	seenIDs := make(map[string]bool)
	failedSet := make(map[string]bool)
	for _, s := range failedChecks {
		failedSet[s] = true
	}

	// Process detected alerts
	for _, alert := range detected {
		seenIDs[alert.ID] = true

		if existing, ok := t.active[alert.ID]; ok {
			// Refresh existing alert
			existing.LastSeenAt = now
			existing.Count++
			// Update severity if it increased
			if severityRank(alert.Severity) > severityRank(existing.Severity) {
				existing.Severity = alert.Severity
			}
			// Update context if present
			if alert.Context != nil {
				existing.Context = alert.Context
			}
		} else {
			// Add new alert
			alertCopy := alert
			alertCopy.CreatedAt = now
			alertCopy.LastSeenAt = now
			alertCopy.Count = 1
			t.active[alert.ID] = &alertCopy
		}
	}

	// Resolve alerts that weren't detected this cycle
	for id, alert := range t.active {
		if !seenIDs[id] {
			// If the check for this source failed, assume the alert might still be active
			if failedSet[alert.Source] {
				continue
			}

			resolved := now
			alert.ResolvedAt = &resolved
			t.resolved = append(t.resolved, alert)
			delete(t.active, id)
		}
	}

	// Prune old resolved alerts
	t.pruneResolved(now)
}

// GetActive returns all currently active alerts
func (t *Tracker) GetActive() []Alert {
	t.mu.RLock()
	defer t.mu.RUnlock()

	alerts := make([]Alert, 0, len(t.active))
	for _, alert := range t.active {
		alerts = append(alerts, *alert)
	}
	return alerts
}

// GetActiveFiltered returns active alerts filtered by type or severity
func (t *Tracker) GetActiveFiltered(alertType *AlertType, minSeverity *Severity) []Alert {
	t.mu.RLock()
	defer t.mu.RUnlock()

	var alerts []Alert
	for _, alert := range t.active {
		// Filter by type if specified
		if alertType != nil && alert.Type != *alertType {
			continue
		}
		// Filter by minimum severity if specified
		if minSeverity != nil && severityRank(alert.Severity) < severityRank(*minSeverity) {
			continue
		}
		alerts = append(alerts, *alert)
	}
	return alerts
}

// GetResolved returns recently resolved alerts
func (t *Tracker) GetResolved() []Alert {
	t.mu.RLock()
	defer t.mu.RUnlock()

	alerts := make([]Alert, len(t.resolved))
	for i, alert := range t.resolved {
		alerts[i] = *alert
	}
	return alerts
}

// GetAll returns both active and resolved alerts
func (t *Tracker) GetAll() (active []Alert, resolved []Alert) {
	t.mu.RLock()
	defer t.mu.RUnlock()

	active = make([]Alert, 0, len(t.active))
	for _, alert := range t.active {
		active = append(active, *alert)
	}

	resolved = make([]Alert, len(t.resolved))
	for i, alert := range t.resolved {
		resolved[i] = *alert
	}

	return active, resolved
}

// GetByID returns a specific alert by ID, checking both active and resolved
func (t *Tracker) GetByID(id string) (*Alert, bool) {
	t.mu.RLock()
	defer t.mu.RUnlock()

	if alert, ok := t.active[id]; ok {
		alertCopy := *alert
		return &alertCopy, true
	}

	for _, alert := range t.resolved {
		if alert.ID == id {
			alertCopy := *alert
			return &alertCopy, true
		}
	}

	return nil, false
}

// Summary returns aggregate statistics about alerts
func (t *Tracker) Summary() AlertSummary {
	t.mu.RLock()
	defer t.mu.RUnlock()

	summary := AlertSummary{
		TotalActive:   len(t.active),
		TotalResolved: len(t.resolved),
		BySeverity:    make(map[string]int),
		ByType:        make(map[string]int),
	}

	for _, alert := range t.active {
		summary.BySeverity[string(alert.Severity)]++
		summary.ByType[string(alert.Type)]++
	}

	return summary
}

// Clear removes all alerts (useful for testing or reset)
func (t *Tracker) Clear() {
	t.mu.Lock()
	defer t.mu.Unlock()

	t.active = make(map[string]*Alert)
	t.resolved = make([]*Alert, 0)
}

// ManualResolve marks a specific alert as resolved
func (t *Tracker) ManualResolve(id string) bool {
	t.mu.Lock()
	defer t.mu.Unlock()

	if alert, ok := t.active[id]; ok {
		now := time.Now()
		alert.ResolvedAt = &now
		t.resolved = append(t.resolved, alert)
		delete(t.active, id)
		return true
	}

	return false
}

// AddAlert adds a single alert without affecting other active alerts.
// Unlike Update(), this does not auto-resolve alerts not in the update batch.
// Use this for event-based alerts (like rotation events) that shouldn't
// interfere with other active alerts.
func (t *Tracker) AddAlert(alert Alert) {
	t.mu.Lock()
	defer t.mu.Unlock()

	now := time.Now()

	if existing, ok := t.active[alert.ID]; ok {
		// Refresh existing alert
		existing.LastSeenAt = now
		existing.Count++
		// Update severity if it increased
		if severityRank(alert.Severity) > severityRank(existing.Severity) {
			existing.Severity = alert.Severity
		}
		// Update context if present
		if alert.Context != nil {
			existing.Context = alert.Context
		}
	} else {
		// Add new alert
		alertCopy := alert
		alertCopy.CreatedAt = now
		alertCopy.LastSeenAt = now
		alertCopy.Count = 1
		t.active[alert.ID] = &alertCopy
	}
}

// pruneResolved removes old resolved alerts
func (t *Tracker) pruneResolved(now time.Time) {
	cutoff := now.Add(-t.pruneAfter)

	kept := make([]*Alert, 0, len(t.resolved))
	for _, alert := range t.resolved {
		if alert.ResolvedAt != nil && alert.ResolvedAt.After(cutoff) {
			kept = append(kept, alert)
		}
	}
	t.resolved = kept
}

// severityRank returns numeric rank for severity comparison
func severityRank(s Severity) int {
	switch s {
	case SeverityInfo:
		return 1
	case SeverityWarning:
		return 2
	case SeverityError:
		return 3
	case SeverityCritical:
		return 4
	default:
		return 0
	}
}

// Global tracker instance for convenience
var globalTracker *Tracker
var globalTrackerOnce sync.Once

// GetGlobalTracker returns the global alert tracker singleton
func GetGlobalTracker() *Tracker {
	globalTrackerOnce.Do(func() {
		globalTracker = NewTracker(DefaultConfig())
	})
	return globalTracker
}

// SetGlobalTrackerConfig updates the global tracker's configuration
func SetGlobalTrackerConfig(cfg Config) {
	tracker := GetGlobalTracker()
	tracker.mu.Lock()
	defer tracker.mu.Unlock()
	tracker.config = cfg
	tracker.pruneAfter = time.Duration(cfg.ResolvedPruneMinutes) * time.Minute
}
