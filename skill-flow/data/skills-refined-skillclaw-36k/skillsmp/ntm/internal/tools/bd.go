package tools

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

// BDAdapter provides integration with the beads (bd) tool
type BDAdapter struct {
	*BaseAdapter
}

// NewBDAdapter creates a new BD adapter
func NewBDAdapter() *BDAdapter {
	return &BDAdapter{
		BaseAdapter: NewBaseAdapter(ToolBD, "bd"),
	}
}

// Detect checks if bd is installed
func (a *BDAdapter) Detect() (string, bool) {
	path, err := exec.LookPath(a.BinaryName())
	if err != nil {
		return "", false
	}
	return path, true
}

// Version returns the installed bd version
func (a *BDAdapter) Version(ctx context.Context) (Version, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, a.BinaryName(), "--version")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout

	if err := cmd.Run(); err != nil {
		return Version{}, fmt.Errorf("failed to get bd version: %w", err)
	}

	return parseVersion(stdout.String())
}

// Capabilities returns the list of bd capabilities
func (a *BDAdapter) Capabilities(ctx context.Context) ([]Capability, error) {
	caps := []Capability{CapRobotMode}

	version, err := a.Version(ctx)
	if err != nil {
		return caps, nil
	}

	// bd 0.20+ has daemon mode
	if version.AtLeast(Version{Major: 0, Minor: 20, Patch: 0}) {
		caps = append(caps, CapDaemonMode)
	}

	return caps, nil
}

// Health checks if bd is functioning correctly
func (a *BDAdapter) Health(ctx context.Context) (*HealthStatus, error) {
	start := time.Now()

	path, installed := a.Detect()
	if !installed {
		return &HealthStatus{
			Healthy:     false,
			Message:     "bd not installed",
			LastChecked: time.Now(),
		}, nil
	}

	// Try to get version as a health check
	_, err := a.Version(ctx)
	latency := time.Since(start)

	if err != nil {
		return &HealthStatus{
			Healthy:     false,
			Message:     fmt.Sprintf("bd at %s not responding", path),
			Error:       err.Error(),
			LastChecked: time.Now(),
			Latency:     latency,
		}, nil
	}

	return &HealthStatus{
		Healthy:     true,
		Message:     "bd is healthy",
		LastChecked: time.Now(),
		Latency:     latency,
	}, nil
}

// HasCapability checks if bd has a specific capability
func (a *BDAdapter) HasCapability(ctx context.Context, cap Capability) bool {
	caps, err := a.Capabilities(ctx)
	if err != nil {
		return false
	}
	for _, c := range caps {
		if c == cap {
			return true
		}
	}
	return false
}

// Info returns complete bd tool information
func (a *BDAdapter) Info(ctx context.Context) (*ToolInfo, error) {
	return a.BaseAdapter.Info(ctx, a)
}

// BD-specific methods

// GetStats returns bd stats output
func (a *BDAdapter) GetStats(ctx context.Context, dir string) (json.RawMessage, error) {
	return a.runCommand(ctx, dir, "stats", "--json")
}

// GetReady returns ready issues
func (a *BDAdapter) GetReady(ctx context.Context, dir string) (json.RawMessage, error) {
	return a.runCommand(ctx, dir, "ready", "--json")
}

// GetBlocked returns blocked issues
func (a *BDAdapter) GetBlocked(ctx context.Context, dir string) (json.RawMessage, error) {
	return a.runCommand(ctx, dir, "blocked", "--json")
}

// GetList returns issues matching filter
func (a *BDAdapter) GetList(ctx context.Context, dir string, status string) (json.RawMessage, error) {
	args := []string{"list", "--json"}
	if status != "" {
		args = append(args, "--status="+status)
	}
	return a.runCommand(ctx, dir, args...)
}

// Show returns details for a specific issue
func (a *BDAdapter) Show(ctx context.Context, dir, issueID string) (json.RawMessage, error) {
	return a.runCommand(ctx, dir, "show", issueID, "--json")
}

// runCommand executes a bd command and returns raw JSON
func (a *BDAdapter) runCommand(ctx context.Context, dir string, args ...string) (json.RawMessage, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, a.BinaryName(), args...)
	if dir != "" {
		cmd.Dir = dir
	}

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return nil, ErrTimeout
		}
		return nil, fmt.Errorf("bd %s failed: %w: %s", strings.Join(args, " "), err, stderr.String())
	}

	// Validate JSON
	output := stdout.Bytes()
	if len(output) > 0 && !json.Valid(output) {
		return nil, fmt.Errorf("%w: invalid JSON from bd", ErrSchemaValidation)
	}

	return output, nil
}
