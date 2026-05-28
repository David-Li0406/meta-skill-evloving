package pipeline

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/util"
)

const pipelineStateDirName = "pipelines"

func pipelineStateDir(projectDir string) string {
	return filepath.Join(projectDir, ".ntm", pipelineStateDirName)
}

func pipelineStatePath(projectDir, runID string) string {
	return filepath.Join(pipelineStateDir(projectDir), fmt.Sprintf("%s.json", runID))
}

// SaveState persists the execution state to .ntm/pipelines/<run-id>.json.
func SaveState(projectDir string, state *ExecutionState) error {
	if state == nil {
		return fmt.Errorf("state is nil")
	}
	if state.RunID == "" {
		return fmt.Errorf("run id is required")
	}

	dir := pipelineStateDir(projectDir)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("create pipeline state dir: %w", err)
	}

	data, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal pipeline state: %w", err)
	}

	path := pipelineStatePath(projectDir, state.RunID)

	if err := util.AtomicWriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("write pipeline state: %w", err)
	}

	return nil
}

// LoadState loads execution state from .ntm/pipelines/<run-id>.json.
func LoadState(projectDir, runID string) (*ExecutionState, error) {
	if runID == "" {
		return nil, fmt.Errorf("run id is required")
	}

	path := pipelineStatePath(projectDir, runID)
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read pipeline state: %w", err)
	}

	var state ExecutionState
	if err := json.Unmarshal(data, &state); err != nil {
		return nil, fmt.Errorf("parse pipeline state: %w", err)
	}

	if state.RunID == "" {
		state.RunID = runID
	}

	return &state, nil
}

// CleanupStates removes pipeline state files older than the provided duration.
// Returns the number of deleted state files.
func CleanupStates(projectDir string, olderThan time.Duration) (int, error) {
	if olderThan <= 0 {
		return 0, fmt.Errorf("olderThan must be greater than zero")
	}

	dir := pipelineStateDir(projectDir)
	entries, err := os.ReadDir(dir)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return 0, nil
		}
		return 0, fmt.Errorf("read pipeline state dir: %w", err)
	}

	cutoff := time.Now().Add(-olderThan)
	deleted := 0

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".json" {
			continue
		}

		info, err := entry.Info()
		if err != nil {
			continue
		}

		if info.ModTime().Before(cutoff) {
			path := filepath.Join(dir, entry.Name())
			if err := os.Remove(path); err != nil {
				return deleted, fmt.Errorf("remove pipeline state: %w", err)
			}
			deleted++
		}
	}

	return deleted, nil
}
