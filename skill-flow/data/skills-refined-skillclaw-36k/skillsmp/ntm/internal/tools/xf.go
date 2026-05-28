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

// XFAdapter provides integration with the XF (X Find) tool.
// XF is a CLI for indexing and searching X/Twitter data archives,
// supporting full-text search with BM25 ranking via Tantivy.
type XFAdapter struct {
	*BaseAdapter
}

// NewXFAdapter creates a new XF adapter
func NewXFAdapter() *XFAdapter {
	return &XFAdapter{
		BaseAdapter: NewBaseAdapter(ToolXF, "xf"),
	}
}

// Detect checks if xf is installed
func (a *XFAdapter) Detect() (string, bool) {
	path, err := exec.LookPath(a.BinaryName())
	if err != nil {
		return "", false
	}
	return path, true
}

// Version returns the installed xf version
func (a *XFAdapter) Version(ctx context.Context) (Version, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, a.BinaryName(), "--version")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout

	if err := cmd.Run(); err != nil {
		return Version{}, fmt.Errorf("failed to get xf version: %w", err)
	}

	return parseVersion(stdout.String())
}

// Capabilities returns the list of xf capabilities
func (a *XFAdapter) Capabilities(ctx context.Context) ([]Capability, error) {
	caps := []Capability{}

	// Check if xf has specific capabilities by examining help output
	path, installed := a.Detect()
	if !installed {
		return caps, nil
	}

	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, path, "--help")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	_ = cmd.Run() // Ignore error, just check output

	output := stdout.String()

	// Check for known capabilities
	if strings.Contains(output, "search") {
		caps = append(caps, CapSearch)
	}
	// XF supports JSON output via --output json
	if strings.Contains(output, "output") || strings.Contains(output, "json") {
		caps = append(caps, CapRobotMode)
	}

	return caps, nil
}

// Health checks if xf is functioning correctly
func (a *XFAdapter) Health(ctx context.Context) (*HealthStatus, error) {
	start := time.Now()

	path, installed := a.Detect()
	if !installed {
		return &HealthStatus{
			Healthy:     false,
			Message:     "xf not installed",
			LastChecked: time.Now(),
		}, nil
	}

	// Try to get version as a basic health check
	_, err := a.Version(ctx)
	latency := time.Since(start)

	if err != nil {
		return &HealthStatus{
			Healthy:     false,
			Message:     fmt.Sprintf("xf at %s not responding", path),
			Error:       err.Error(),
			LastChecked: time.Now(),
			Latency:     latency,
		}, nil
	}

	return &HealthStatus{
		Healthy:     true,
		Message:     "xf is healthy",
		LastChecked: time.Now(),
		Latency:     latency,
	}, nil
}

// HasCapability checks if xf has a specific capability
func (a *XFAdapter) HasCapability(ctx context.Context, cap Capability) bool {
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

// Info returns complete xf tool information
func (a *XFAdapter) Info(ctx context.Context) (*ToolInfo, error) {
	return a.BaseAdapter.Info(ctx, a)
}

// XF-specific methods

// XFStats represents archive statistics
type XFStats struct {
	TweetCount   int    `json:"tweet_count,omitempty"`
	LikeCount    int    `json:"like_count,omitempty"`
	DMCount      int    `json:"dm_count,omitempty"`
	GrokCount    int    `json:"grok_count,omitempty"`
	IndexStatus  string `json:"index_status,omitempty"`
	LastIndexed  string `json:"last_indexed,omitempty"`
	DatabasePath string `json:"database_path,omitempty"`
}

// XFSearchResult represents a search result
type XFSearchResult struct {
	ID        string  `json:"id"`
	Content   string  `json:"content"`
	CreatedAt string  `json:"created_at,omitempty"`
	Type      string  `json:"type,omitempty"` // tweet, like, dm, grok
	Score     float64 `json:"score,omitempty"`
}

// GetStats returns archive statistics
func (a *XFAdapter) GetStats(ctx context.Context) (*XFStats, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, a.BinaryName(), "stats", "--output", "json")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return nil, ErrTimeout
		}
		// Return empty stats if command fails (no archive indexed)
		return &XFStats{}, nil
	}

	output := stdout.Bytes()
	if !json.Valid(output) {
		return &XFStats{}, nil
	}

	var stats XFStats
	if err := json.Unmarshal(output, &stats); err != nil {
		return nil, fmt.Errorf("failed to parse xf stats: %w", err)
	}

	return &stats, nil
}

// Search performs a full-text search on the indexed archive
func (a *XFAdapter) Search(ctx context.Context, query string, limit int) ([]XFSearchResult, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	args := []string{"search", query, "--output", "json"}
	if limit > 0 {
		args = append(args, "--limit", fmt.Sprintf("%d", limit))
	}

	cmd := exec.CommandContext(ctx, a.BinaryName(), args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return nil, ErrTimeout
		}
		return nil, fmt.Errorf("xf search failed: %w: %s", err, stderr.String())
	}

	output := stdout.Bytes()
	if !json.Valid(output) {
		return []XFSearchResult{}, nil
	}

	var results []XFSearchResult
	if err := json.Unmarshal(output, &results); err != nil {
		return nil, fmt.Errorf("failed to parse xf search results: %w", err)
	}

	return results, nil
}

// Doctor runs xf doctor diagnostics
func (a *XFAdapter) Doctor(ctx context.Context) (string, error) {
	ctx, cancel := context.WithTimeout(ctx, a.Timeout())
	defer cancel()

	cmd := exec.CommandContext(ctx, a.BinaryName(), "doctor")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return "", ErrTimeout
		}
		return "", fmt.Errorf("xf doctor failed: %w: %s", err, stderr.String())
	}

	return stdout.String(), nil
}
