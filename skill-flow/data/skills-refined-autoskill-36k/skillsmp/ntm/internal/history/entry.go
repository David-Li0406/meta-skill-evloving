// Package history provides prompt history storage and retrieval.
package history

import (
	"crypto/rand"
	"fmt"
	"sync/atomic"
	"time"
)

// idCounter provides uniqueness fallback if crypto/rand fails
var idCounter uint64

// Source represents where a prompt originated
type Source string

const (
	SourceCLI     Source = "cli"
	SourcePalette Source = "palette"
	SourceReplay  Source = "replay"
)

// HistoryEntry represents a single prompt sent via ntm send.
type HistoryEntry struct {
	ID         string    `json:"id"`                    // Unique ID (timestamp-random)
	Timestamp  time.Time `json:"ts"`                    // When sent
	Session    string    `json:"session"`               // Session name
	Targets    []string  `json:"targets"`               // Pane indices sent to
	Prompt     string    `json:"prompt"`                // Full prompt text
	Source     Source    `json:"source"`                // cli, palette, replay
	Template   string    `json:"template,omitempty"`    // Template name if used
	Success    bool      `json:"success"`               // Whether send succeeded
	Error      string    `json:"error,omitempty"`       // Error message if failed
	DurationMs int       `json:"duration_ms,omitempty"` // How long the operation took
}

// NewEntry creates a new history entry with generated ID and timestamp.
func NewEntry(session string, targets []string, prompt string, source Source) *HistoryEntry {
	return &HistoryEntry{
		ID:        newID(),
		Timestamp: time.Now().UTC(),
		Session:   session,
		Targets:   targets,
		Prompt:    prompt,
		Source:    source,
	}
}

// SetSuccess marks the entry as successful.
func (e *HistoryEntry) SetSuccess() {
	e.Success = true
}

// SetError marks the entry as failed with an error message.
func (e *HistoryEntry) SetError(err error) {
	e.Success = false
	if err != nil {
		e.Error = err.Error()
	}
}

// newID generates a unique, sortable ID.
// Format: timestamp (ms) + random suffix for uniqueness.
// Falls back to an atomic counter if crypto/rand fails.
func newID() string {
	ms := time.Now().UnixMilli()
	b := make([]byte, 4)
	if _, err := rand.Read(b); err != nil {
		// Fallback: use atomic counter for uniqueness
		counter := atomic.AddUint64(&idCounter, 1)
		return fmt.Sprintf("%d-%016x", ms, counter)
	}
	return fmt.Sprintf("%d-%x", ms, b)
}
