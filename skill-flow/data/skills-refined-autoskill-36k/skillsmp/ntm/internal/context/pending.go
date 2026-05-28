// Package context provides context window monitoring for AI agent orchestration.
// pending.go implements persistent storage for pending rotation confirmations.
package context

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/util"
)

const (
	pendingRotationDir  = "rotation_history"
	pendingRotationFile = "pending.jsonl"
)

var (
	// pendingMu provides goroutine safety for pending operations
	pendingMu sync.Mutex
)

// StoredPendingRotation is the serialized form of PendingRotation for persistence.
type StoredPendingRotation struct {
	AgentID        string        `json:"agent_id"`
	SessionName    string        `json:"session_name"`
	PaneID         string        `json:"pane_id"`
	ContextPercent float64       `json:"context_percent"`
	CreatedAt      time.Time     `json:"created_at"`
	TimeoutAt      time.Time     `json:"timeout_at"`
	DefaultAction  ConfirmAction `json:"default_action"`
	WorkDir        string        `json:"work_dir"`
}

// ToPendingRotation converts a StoredPendingRotation to PendingRotation.
func (s *StoredPendingRotation) ToPendingRotation() *PendingRotation {
	return &PendingRotation{
		AgentID:        s.AgentID,
		SessionName:    s.SessionName,
		PaneID:         s.PaneID,
		ContextPercent: s.ContextPercent,
		CreatedAt:      s.CreatedAt,
		TimeoutAt:      s.TimeoutAt,
		DefaultAction:  s.DefaultAction,
		WorkDir:        s.WorkDir,
	}
}

// FromPendingRotation creates a StoredPendingRotation from PendingRotation.
func FromPendingRotation(p *PendingRotation) *StoredPendingRotation {
	return &StoredPendingRotation{
		AgentID:        p.AgentID,
		SessionName:    p.SessionName,
		PaneID:         p.PaneID,
		ContextPercent: p.ContextPercent,
		CreatedAt:      p.CreatedAt,
		TimeoutAt:      p.TimeoutAt,
		DefaultAction:  p.DefaultAction,
		WorkDir:        p.WorkDir,
	}
}

// PendingRotationStore provides persistent storage for pending rotations.
type PendingRotationStore struct {
	storagePath string
}

// NewPendingRotationStore creates a new pending rotation store with default path.
func NewPendingRotationStore() *PendingRotationStore {
	return &PendingRotationStore{
		storagePath: defaultPendingRotationPath(),
	}
}

// NewPendingRotationStoreWithPath creates a store with a custom path.
func NewPendingRotationStoreWithPath(path string) *PendingRotationStore {
	return &PendingRotationStore{
		storagePath: path,
	}
}

// defaultPendingRotationPath returns the path to the pending rotation file.
func defaultPendingRotationPath() string {
	ntmDir, err := util.NTMDir()
	if err != nil {
		return filepath.Join(os.TempDir(), "ntm", pendingRotationDir, pendingRotationFile)
	}
	return filepath.Join(ntmDir, pendingRotationDir, pendingRotationFile)
}

// StoragePath returns the path to the pending rotation file.
func (s *PendingRotationStore) StoragePath() string {
	return s.storagePath
}

// Add adds or updates a pending rotation in the store.
func (s *PendingRotationStore) Add(pending *PendingRotation) error {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	// Read existing entries (excluding expired and matching agent)
	entries, _ := s.readAllLocked()
	var newEntries []StoredPendingRotation

	now := time.Now()
	for _, e := range entries {
		// Skip expired and skip existing entry for same agent
		if e.TimeoutAt.After(now) && e.AgentID != pending.AgentID {
			newEntries = append(newEntries, e)
		}
	}

	// Add the new/updated entry
	newEntries = append(newEntries, *FromPendingRotation(pending))

	return s.writeAllLocked(newEntries)
}

// Remove removes a pending rotation by agent ID.
func (s *PendingRotationStore) Remove(agentID string) error {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, _ := s.readAllLocked()
	var newEntries []StoredPendingRotation

	now := time.Now()
	for _, e := range entries {
		// Keep non-expired, non-matching entries
		if e.TimeoutAt.After(now) && e.AgentID != agentID {
			newEntries = append(newEntries, e)
		}
	}

	return s.writeAllLocked(newEntries)
}

// Get retrieves a pending rotation by agent ID.
func (s *PendingRotationStore) Get(agentID string) (*PendingRotation, error) {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, err := s.readAllLocked()
	if err != nil {
		return nil, err
	}

	now := time.Now()
	for _, e := range entries {
		if e.AgentID == agentID && e.TimeoutAt.After(now) {
			return e.ToPendingRotation(), nil
		}
	}

	return nil, nil
}

// GetAll retrieves all non-expired pending rotations.
func (s *PendingRotationStore) GetAll() ([]*PendingRotation, error) {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, err := s.readAllLocked()
	if err != nil {
		return nil, err
	}

	var result []*PendingRotation
	now := time.Now()
	for _, e := range entries {
		if e.TimeoutAt.After(now) {
			result = append(result, e.ToPendingRotation())
		}
	}

	return result, nil
}

// GetForSession retrieves pending rotations for a specific session.
func (s *PendingRotationStore) GetForSession(session string) ([]*PendingRotation, error) {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, err := s.readAllLocked()
	if err != nil {
		return nil, err
	}

	var result []*PendingRotation
	now := time.Now()
	for _, e := range entries {
		if e.SessionName == session && e.TimeoutAt.After(now) {
			result = append(result, e.ToPendingRotation())
		}
	}

	return result, nil
}

// GetExpired retrieves all expired pending rotations.
func (s *PendingRotationStore) GetExpired() ([]*PendingRotation, error) {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, err := s.readAllLocked()
	if err != nil {
		return nil, err
	}

	var result []*PendingRotation
	now := time.Now()
	for _, e := range entries {
		if e.TimeoutAt.Before(now) || e.TimeoutAt.Equal(now) {
			result = append(result, e.ToPendingRotation())
		}
	}

	return result, nil
}

// CleanExpired removes all expired entries.
func (s *PendingRotationStore) CleanExpired() (int, error) {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	entries, err := s.readAllLocked()
	if err != nil {
		return 0, err
	}

	var newEntries []StoredPendingRotation
	now := time.Now()
	for _, e := range entries {
		if e.TimeoutAt.After(now) {
			newEntries = append(newEntries, e)
		}
	}

	removed := len(entries) - len(newEntries)
	if removed > 0 {
		if err := s.writeAllLocked(newEntries); err != nil {
			return 0, err
		}
	}

	return removed, nil
}

// Count returns the number of pending rotations.
func (s *PendingRotationStore) Count() (int, error) {
	entries, err := s.GetAll()
	if err != nil {
		return 0, err
	}
	return len(entries), nil
}

// Clear removes all pending rotations.
func (s *PendingRotationStore) Clear() error {
	pendingMu.Lock()
	defer pendingMu.Unlock()

	err := os.Remove(s.storagePath)
	if os.IsNotExist(err) {
		return nil
	}
	return err
}

// readAllLocked reads all entries (caller must hold lock).
func (s *PendingRotationStore) readAllLocked() ([]StoredPendingRotation, error) {
	f, err := os.Open(s.storagePath)
	if err != nil {
		if os.IsNotExist(err) {
			return []StoredPendingRotation{}, nil
		}
		return nil, err
	}
	defer f.Close()

	var entries []StoredPendingRotation
	scanner := bufio.NewScanner(f)
	scanner.Buffer(make([]byte, 64*1024), 1024*1024)

	for scanner.Scan() {
		var entry StoredPendingRotation
		if err := json.Unmarshal(scanner.Bytes(), &entry); err != nil {
			continue // Skip malformed lines
		}
		entries = append(entries, entry)
	}

	if err := scanner.Err(); err != nil {
		return entries, err
	}

	return entries, nil
}

// writeAllLocked writes all entries atomically (caller must hold lock).
func (s *PendingRotationStore) writeAllLocked(entries []StoredPendingRotation) error {
	// Ensure directory exists
	if err := os.MkdirAll(filepath.Dir(s.storagePath), 0755); err != nil {
		return fmt.Errorf("creating directory: %w", err)
	}

	// Write to temp file first
	tmpFile, err := os.CreateTemp(filepath.Dir(s.storagePath), "pending-*.tmp")
	if err != nil {
		return err
	}
	defer func() { _ = os.Remove(tmpFile.Name()) }()

	writer := bufio.NewWriter(tmpFile)
	for _, entry := range entries {
		data, err := json.Marshal(entry)
		if err != nil {
			continue
		}
		if _, err := writer.Write(data); err != nil {
			return err
		}
		if err := writer.WriteByte('\n'); err != nil {
			return err
		}
	}

	if err := writer.Flush(); err != nil {
		return err
	}
	if err := tmpFile.Close(); err != nil {
		return err
	}

	if err := os.Chmod(tmpFile.Name(), 0600); err != nil {
		return err
	}

	return os.Rename(tmpFile.Name(), s.storagePath)
}

// DefaultPendingRotationStore is the default global pending rotation store.
var DefaultPendingRotationStore = NewPendingRotationStore()

// AddPendingRotation adds a pending rotation to the default store.
func AddPendingRotation(pending *PendingRotation) error {
	return DefaultPendingRotationStore.Add(pending)
}

// RemovePendingRotation removes a pending rotation from the default store.
func RemovePendingRotation(agentID string) error {
	return DefaultPendingRotationStore.Remove(agentID)
}

// GetPendingRotationByID retrieves a pending rotation from the default store.
func GetPendingRotationByID(agentID string) (*PendingRotation, error) {
	return DefaultPendingRotationStore.Get(agentID)
}

// GetAllPendingRotations retrieves all pending rotations from the default store.
func GetAllPendingRotations() ([]*PendingRotation, error) {
	return DefaultPendingRotationStore.GetAll()
}

// GetPendingRotationsForSession retrieves pending rotations for a session.
func GetPendingRotationsForSession(session string) ([]*PendingRotation, error) {
	return DefaultPendingRotationStore.GetForSession(session)
}

// PendingRotationStoragePath returns the path to the pending rotation file.
func PendingRotationStoragePath() string {
	return DefaultPendingRotationStore.StoragePath()
}
