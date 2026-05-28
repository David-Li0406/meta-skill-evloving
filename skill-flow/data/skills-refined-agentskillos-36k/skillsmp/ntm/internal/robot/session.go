// Package robot provides JSON output functions for AI agent integration.
package robot

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/Dicklesworthstone/ntm/internal/session"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// SaveOptions configures the robot-save operation.
type SaveOptions struct {
	Session    string // Session name to save
	OutputFile string // Optional custom output file path
}

// RestoreOptions configures the robot-restore operation.
type RestoreOptions struct {
	SavedName string // Name of saved state to restore
	DryRun    bool   // Preview without executing
}

// SaveResult represents the JSON output for robot-save.
type SaveResult struct {
	Success  bool                  `json:"success"`
	Session  string                `json:"session"`
	SavedAs  string                `json:"saved_as"`
	FilePath string                `json:"file_path"`
	State    *session.SessionState `json:"state,omitempty"`
	Error    string                `json:"error,omitempty"`
}

// RestoreResult represents the JSON output for robot-restore.
type RestoreResult struct {
	Success    bool                  `json:"success"`
	SavedName  string                `json:"saved_name"`
	RestoredAs string                `json:"restored_as,omitempty"`
	DryRun     bool                  `json:"dry_run"`
	State      *session.SessionState `json:"state,omitempty"`
	Preview    *RestorePreview       `json:"preview,omitempty"`
	Error      string                `json:"error,omitempty"`
}

// RestorePreview describes what would happen during restore.
type RestorePreview struct {
	SessionName string   `json:"session_name"`
	WorkDir     string   `json:"work_dir"`
	PaneCount   int      `json:"pane_count"`
	AgentCount  int      `json:"agent_count"`
	Layout      string   `json:"layout"`
	Actions     []string `json:"actions"`
}

// PrintSave saves a session state and outputs JSON.
func PrintSave(opts SaveOptions) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return outputSaveError(opts.Session, err)
	}

	sessionName := opts.Session
	if sessionName == "" {
		return outputSaveError("", fmt.Errorf("session name is required"))
	}

	if !tmux.SessionExists(sessionName) {
		return outputSaveError(sessionName, fmt.Errorf("session '%s' not found", sessionName))
	}

	// Capture session state
	state, err := session.Capture(sessionName)
	if err != nil {
		return outputSaveError(sessionName, fmt.Errorf("failed to capture session state: %w", err))
	}

	// Save state
	saveOpts := session.SaveOptions{
		Overwrite: true, // Robot mode always overwrites
	}
	path, err := session.Save(state, saveOpts)
	if err != nil {
		return outputSaveError(sessionName, fmt.Errorf("failed to save session state: %w", err))
	}

	// If custom output file requested, also write there
	if opts.OutputFile != "" {
		data, err := json.MarshalIndent(state, "", "  ")
		if err != nil {
			return outputSaveError(sessionName, fmt.Errorf("failed to marshal state: %w", err))
		}
		if err := os.WriteFile(opts.OutputFile, data, 0644); err != nil {
			return outputSaveError(sessionName, fmt.Errorf("failed to write to %s: %w", opts.OutputFile, err))
		}
		path = opts.OutputFile
	}

	result := SaveResult{
		Success:  true,
		Session:  sessionName,
		SavedAs:  sessionName,
		FilePath: path,
		State:    state,
	}

	return encodeJSON(result)
}

// PrintRestore restores a session from saved state and outputs JSON.
func PrintRestore(opts RestoreOptions) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return outputRestoreError(opts.SavedName, err)
	}

	if opts.SavedName == "" {
		return outputRestoreError("", fmt.Errorf("saved state name is required"))
	}

	// Load saved state
	state, err := session.Load(opts.SavedName)
	if err != nil {
		return outputRestoreError(opts.SavedName, fmt.Errorf("failed to load saved state: %w", err))
	}

	// Dry run mode - preview what would happen
	if opts.DryRun {
		preview := buildRestorePreview(state)
		result := RestoreResult{
			Success:   true,
			SavedName: opts.SavedName,
			DryRun:    true,
			State:     state,
			Preview:   preview,
		}
		return encodeJSON(result)
	}

	// Check if session already exists
	if tmux.SessionExists(state.Name) {
		return outputRestoreError(opts.SavedName, fmt.Errorf("session '%s' already exists (use 'ntm sessions restore' with --force to overwrite)", state.Name))
	}

	// Restore session
	restoreOpts := session.RestoreOptions{
		Force: false, // Robot mode is cautious by default
	}
	if err := session.Restore(state, restoreOpts); err != nil {
		return outputRestoreError(opts.SavedName, fmt.Errorf("failed to restore session: %w", err))
	}

	result := RestoreResult{
		Success:    true,
		SavedName:  opts.SavedName,
		RestoredAs: state.Name,
		DryRun:     false,
		State:      state,
	}

	return encodeJSON(result)
}

func buildRestorePreview(state *session.SessionState) *RestorePreview {
	actions := []string{
		fmt.Sprintf("Create tmux session '%s'", state.Name),
		fmt.Sprintf("Set working directory to '%s'", state.WorkDir),
	}

	if len(state.Panes) > 1 {
		actions = append(actions, fmt.Sprintf("Create %d panes", len(state.Panes)))
	}

	if state.Layout != "" && state.Layout != "tiled" {
		actions = append(actions, fmt.Sprintf("Apply layout '%s'", state.Layout))
	}

	for _, p := range state.Panes {
		if p.Command != "" {
			actions = append(actions, fmt.Sprintf("Start '%s' in pane %d", p.Title, p.Index))
		}
	}

	return &RestorePreview{
		SessionName: state.Name,
		WorkDir:     state.WorkDir,
		PaneCount:   len(state.Panes),
		AgentCount:  state.Agents.Total(),
		Layout:      state.Layout,
		Actions:     actions,
	}
}

func outputSaveError(sessionName string, err error) error {
	result := SaveResult{
		Success: false,
		Session: sessionName,
		Error:   err.Error(),
	}
	return encodeJSON(result)
}

func outputRestoreError(savedName string, err error) error {
	result := RestoreResult{
		Success:   false,
		SavedName: savedName,
		Error:     err.Error(),
	}
	return encodeJSON(result)
}
