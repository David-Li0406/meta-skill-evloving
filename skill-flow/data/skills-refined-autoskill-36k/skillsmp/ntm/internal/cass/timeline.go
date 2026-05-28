package cass

import (
	"context"
	"encoding/json"
	"fmt"
)

// TimelineResponse represents response from timeline query
type TimelineResponse struct {
	Period  string          `json:"period"`
	GroupBy string          `json:"group_by"`
	Entries []TimelineEntry `json:"entries"`
	Total   int             `json:"total"`
}

// Timeline fetches agent activity timeline
func (c *Client) Timeline(ctx context.Context, since, groupBy string) (*TimelineResponse, error) {
	if !c.IsInstalled() {
		return nil, ErrNotInstalled
	}

	ctx, cancel := context.WithTimeout(ctx, c.timeout)
	defer cancel()

	// Build arguments for: cass timeline --json [flags]
	args := []string{"timeline", "--json"}
	if since != "" {
		args = append(args, fmt.Sprintf("--since=%s", since))
	}
	if groupBy != "" {
		args = append(args, fmt.Sprintf("--group-by=%s", groupBy))
	}

	output, err := c.executor.Run(ctx, args...)
	if err != nil {
		return nil, err
	}

	var response TimelineResponse
	if err := json.Unmarshal(output, &response); err != nil {
		return nil, fmt.Errorf("failed to parse timeline response: %w", err)
	}

	return &response, nil
}
