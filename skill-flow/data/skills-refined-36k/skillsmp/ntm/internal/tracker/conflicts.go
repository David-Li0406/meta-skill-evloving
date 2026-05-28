package tracker

import (
	"time"
)

// Conflict represents a detected file conflict
type Conflict struct {
	Path     string               `json:"path"`
	Changes  []RecordedFileChange `json:"changes,omitempty"`
	Severity string               `json:"severity,omitempty"` // "warning", "critical"
	Agents   []string             `json:"agents,omitempty"`
	LastAt   time.Time            `json:"last_at,omitempty"`
}

// DetectConflicts analyzes a set of changes for conflicts.
func DetectConflicts(changes []RecordedFileChange) []Conflict {
	// Group by file path
	byPath := make(map[string][]RecordedFileChange)
	for _, change := range changes {
		// Only care about modifications for now
		if change.Change.Type == FileModified {
			byPath[change.Change.Path] = append(byPath[change.Change.Path], change)
		}
	}

	var conflicts []Conflict
	for path, pathChanges := range byPath {
		if len(pathChanges) > 1 {
			allAgents := make(map[string]bool)
			for _, pc := range pathChanges {
				for _, agent := range pc.Agents {
					allAgents[agent] = true
				}
			}

			if len(allAgents) <= 1 {
				continue
			}

			agentList := make([]string, 0, len(allAgents))
			var last time.Time
			for agent := range allAgents {
				agentList = append(agentList, agent)
			}
			for _, pc := range pathChanges {
				if pc.Timestamp.After(last) {
					last = pc.Timestamp
				}
			}

			conflicts = append(conflicts, Conflict{
				Path:     path,
				Changes:  pathChanges,
				Severity: conflictSeverity(pathChanges, len(allAgents)),
				Agents:   agentList,
				LastAt:   last,
			})
		}
	}
	return conflicts
}

// DetectConflictsRecent analyzes global file changes within the given window.
func DetectConflictsRecent(window time.Duration) []Conflict {
	changes := GlobalFileChanges.Since(time.Now().Add(-window))
	return DetectConflicts(changes)
}

// ConflictsSince returns files changed by more than one agent since the timestamp.
func ConflictsSince(ts time.Time, session string) []Conflict {
	changes := GlobalFileChanges.Since(ts)
	var filtered []RecordedFileChange
	for _, c := range changes {
		if session != "" && c.Session != session {
			continue
		}
		filtered = append(filtered, c)
	}
	return DetectConflicts(filtered)
}

// conflictSeverity classifies severity using simple heuristics:
// - critical if three or more agents touched the file
// - critical if edits occurred within a 10-minute window
// otherwise warning.
func conflictSeverity(pathChanges []RecordedFileChange, agentCount int) string {
	if agentCount >= 3 {
		return "critical"
	}
	var minT, maxT time.Time
	for i, c := range pathChanges {
		if i == 0 || c.Timestamp.Before(minT) {
			minT = c.Timestamp
		}
		if c.Timestamp.After(maxT) {
			maxT = c.Timestamp
		}
	}
	if maxT.Sub(minT) <= 10*time.Minute {
		return "critical"
	}
	return "warning"
}
