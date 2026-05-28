package cass

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
)

// Health performs a quick health check
func (c *Client) Health(ctx context.Context) (*StatusResponse, error) {
	if !c.IsInstalled() {
		return nil, ErrNotInstalled
	}
	// Use "status" as health check for now, unless "health" is distinct in CASS
	return c.runStatusCmd(ctx, "status")
}

// Status returns full index status
func (c *Client) Status(ctx context.Context) (*StatusResponse, error) {
	if !c.IsInstalled() {
		return nil, ErrNotInstalled
	}
	return c.runStatusCmd(ctx, "status")
}

func (c *Client) runStatusCmd(ctx context.Context, cmd string) (*StatusResponse, error) {
	ctx, cancel := context.WithTimeout(ctx, c.timeout)
	defer cancel()

	// Call: cass <cmd> --json (e.g., cass status --json)
	output, err := c.executor.Run(ctx, cmd, "--json")
	if err != nil {
		return nil, err
	}

	var response StatusResponse
	if err := json.Unmarshal(output, &response); err != nil {
		return nil, fmt.Errorf("failed to parse %s response: %w", cmd, err)
	}

	return &response, nil
}

// Capabilities returns CASS feature discovery
func (c *Client) Capabilities(ctx context.Context) (*Capabilities, error) {
	if !c.IsInstalled() {
		return nil, ErrNotInstalled
	}

	ctx, cancel := context.WithTimeout(ctx, c.timeout)
	defer cancel()

	// Call: cass capabilities --json
	output, err := c.executor.Run(ctx, "capabilities", "--json")
	if err != nil {
		return nil, err
	}

	var response Capabilities
	if err := json.Unmarshal(output, &response); err != nil {
		return nil, fmt.Errorf("failed to parse capabilities response: %w", err)
	}

	return &response, nil
}

// IsHealthy returns true if CASS is healthy and index is fresh
func (c *Client) IsHealthy(ctx context.Context) bool {
	status, err := c.Health(ctx)
	if err != nil {
		return false
	}
	return status.IsHealthy()
}

// NeedsReindex returns true if index is stale or missing
func (c *Client) NeedsReindex(ctx context.Context) (bool, string) {
	status, err := c.Status(ctx)
	if err != nil {
		return true, "CASS unavailable"
	}

	if status.Index.DocCount == 0 {
		return true, "Index empty"
	}

	if !status.Index.LastUpdated.IsZero() {
		if time.Since(status.Index.LastUpdated.Time) > 24*time.Hour {
			return true, fmt.Sprintf("Index stale (last updated %s)",
				time.Since(status.Index.LastUpdated.Time).Round(time.Minute))
		}
	}

	return false, ""
}
