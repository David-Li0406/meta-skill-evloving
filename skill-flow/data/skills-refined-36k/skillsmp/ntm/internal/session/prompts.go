package session

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/util"
)

const (
	promptsDirName  = "prompts"
	promptExtension = ".json"
)

// PromptEntry represents a saved prompt that was sent to agents.
type PromptEntry struct {
	ID        string    `json:"id"`
	Timestamp time.Time `json:"timestamp"`
	Session   string    `json:"session"`
	Content   string    `json:"content"`
	Targets   []string  `json:"targets"` // Pane IDs or "all"
	Source    string    `json:"source"`  // "cli", "template", "file"
	Template  string    `json:"template,omitempty"`
	FilePath  string    `json:"file_path,omitempty"`
}

// PromptHistory contains all prompts for a session.
type PromptHistory struct {
	Session  string        `json:"session"`
	Prompts  []PromptEntry `json:"prompts"`
	UpdateAt time.Time     `json:"updated_at"`
}

// SessionDir returns the path to the session-specific directory.
// Creates the directory if it doesn't exist.
func SessionDir(sessionName string) (string, error) {
	ntmDir, err := util.NTMDir()
	if err != nil {
		return "", err
	}

	dir := filepath.Join(ntmDir, "sessions", sanitizeFilename(sessionName))
	if err := os.MkdirAll(dir, 0700); err != nil {
		return "", fmt.Errorf("failed to create session directory: %w", err)
	}

	return dir, nil
}

// promptsFilePath returns the path to the prompts file for a session.
func promptsFilePath(sessionName string) (string, error) {
	dir, err := SessionDir(sessionName)
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, "prompts.json"), nil
}

// SavePrompt saves a prompt to the session's prompt history.
func SavePrompt(entry PromptEntry) error {
	if entry.Session == "" {
		return fmt.Errorf("session name is required")
	}

	// Generate ID if not set
	if entry.ID == "" {
		entry.ID = fmt.Sprintf("%d", time.Now().UnixNano())
	}

	// Set timestamp if not set
	if entry.Timestamp.IsZero() {
		entry.Timestamp = time.Now()
	}

	// Load existing history
	history, err := LoadPromptHistory(entry.Session)
	if err != nil && !os.IsNotExist(err) {
		return err
	}
	if history == nil {
		history = &PromptHistory{
			Session: entry.Session,
			Prompts: []PromptEntry{},
		}
	}

	// Append new entry
	history.Prompts = append(history.Prompts, entry)
	history.UpdateAt = time.Now()

	// Save history
	return savePromptHistory(history)
}

// LoadPromptHistory loads the prompt history for a session.
func LoadPromptHistory(sessionName string) (*PromptHistory, error) {
	path, err := promptsFilePath(sessionName)
	if err != nil {
		return nil, err
	}

	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return &PromptHistory{
				Session: sessionName,
				Prompts: []PromptEntry{},
			}, nil
		}
		return nil, fmt.Errorf("failed to read prompts file: %w", err)
	}

	var history PromptHistory
	if err := json.Unmarshal(data, &history); err != nil {
		return nil, fmt.Errorf("failed to parse prompts file: %w", err)
	}

	return &history, nil
}

// savePromptHistory writes the prompt history to disk.
func savePromptHistory(history *PromptHistory) error {
	path, err := promptsFilePath(history.Session)
	if err != nil {
		return err
	}

	data, err := json.MarshalIndent(history, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to serialize prompt history: %w", err)
	}

	if err := util.AtomicWriteFile(path, data, 0600); err != nil {
		return fmt.Errorf("writing prompts file: %w", err)
	}

	return nil
}

// GetLatestPrompts returns the N most recent prompts for a session.
func GetLatestPrompts(sessionName string, limit int) ([]PromptEntry, error) {
	history, err := LoadPromptHistory(sessionName)
	if err != nil {
		return nil, err
	}

	// Sort by timestamp (newest first)
	sort.Slice(history.Prompts, func(i, j int) bool {
		return history.Prompts[i].Timestamp.After(history.Prompts[j].Timestamp)
	})

	// Limit results
	if limit > 0 && len(history.Prompts) > limit {
		return history.Prompts[:limit], nil
	}

	return history.Prompts, nil
}

// ClearPromptHistory removes all prompts for a session.
func ClearPromptHistory(sessionName string) error {
	path, err := promptsFilePath(sessionName)
	if err != nil {
		return err
	}

	err = os.Remove(path)
	if os.IsNotExist(err) {
		return nil // Already cleared
	}
	return err
}

// ListSessionDirs returns all sessions that have prompt history.
func ListSessionDirs() ([]string, error) {
	ntmDir, err := util.NTMDir()
	if err != nil {
		return nil, err
	}

	sessionsDir := filepath.Join(ntmDir, "sessions")
	entries, err := os.ReadDir(sessionsDir)
	if err != nil {
		if os.IsNotExist(err) {
			return []string{}, nil
		}
		return nil, err
	}

	var sessions []string
	for _, entry := range entries {
		if entry.IsDir() {
			// Check if it has a prompts.json file
			promptsPath := filepath.Join(sessionsDir, entry.Name(), "prompts.json")
			if _, err := os.Stat(promptsPath); err == nil {
				sessions = append(sessions, entry.Name())
			}
		}
	}

	return sessions, nil
}
