package cass

import (
	"context"
)

type DuplicateCheckResult struct {
	Query           string      `json:"query"`
	DuplicatesFound bool        `json:"duplicates_found"`
	SimilarSessions []SearchHit `json:"similar_sessions"`
	Recommendation  string      `json:"recommendation"` // "proceed", "review", "skip"
}

type DuplicateCheckOptions struct {
	Query     string
	Workspace string
	Since     string
	Threshold float64
	Limit     int
}

func (c *Client) CheckDuplicates(ctx context.Context, opts DuplicateCheckOptions) (*DuplicateCheckResult, error) {
	if opts.Threshold <= 0 {
		opts.Threshold = 0.7
	}
	if opts.Since == "" {
		opts.Since = "7d"
	}
	if opts.Limit <= 0 {
		opts.Limit = 5
	}

	// Search for similar sessions
	// Note: CASS search score is usually relevant for similarity
	resp, err := c.Search(ctx, SearchOptions{
		Query:     opts.Query,
		Workspace: opts.Workspace,
		Since:     opts.Since,
		Limit:     opts.Limit,
	})
	if err != nil {
		return nil, err
	}

	result := &DuplicateCheckResult{
		Query:           opts.Query,
		SimilarSessions: []SearchHit{},
		Recommendation:  "proceed",
	}

	for _, hit := range resp.Hits {
		if hit.Score >= opts.Threshold {
			result.SimilarSessions = append(result.SimilarSessions, hit)
		}
	}

	if len(result.SimilarSessions) > 0 {
		result.DuplicatesFound = true
		result.Recommendation = "review_before_proceeding"
	}

	return result, nil
}
