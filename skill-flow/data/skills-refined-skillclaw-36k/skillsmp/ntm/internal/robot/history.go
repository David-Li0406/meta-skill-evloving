package robot

import (
	"fmt"
	"strings"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/history"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/util"
)

// HistoryOptions configures history queries
type HistoryOptions struct {
	Session   string // tmux session name
	Pane      string // filter by pane ID
	AgentType string // filter by agent type
	Last      int    // last N entries
	Since     string // time-based filter (e.g., "1h", "30m", "2025-12-15")
	Stats     bool   // show statistics instead of entries
}

// HistoryOutput is the structured output for --robot-history
type HistoryOutput struct {
	RobotResponse
	Session     string                 `json:"session"`
	GeneratedAt time.Time              `json:"generated_at"`
	Entries     []history.HistoryEntry `json:"entries,omitempty"`
	Stats       *history.Stats         `json:"stats,omitempty"`
	Total       int                    `json:"total"`
	Filtered    int                    `json:"filtered"`
	AgentHints  *HistoryAgentHints     `json:"_agent_hints,omitempty"`
}

// HistoryAgentHints provides actionable suggestions for AI agents
type HistoryAgentHints struct {
	Summary           string   `json:"summary,omitempty"`
	SuggestedCommands []string `json:"suggested_commands,omitempty"`
	Warnings          []string `json:"warnings,omitempty"`
}

// PrintHistory outputs command history as JSON
func PrintHistory(opts HistoryOptions) error {
	if opts.Session == "" {
		return RobotError(
			fmt.Errorf("session name is required"),
			ErrCodeInvalidFlag,
			"Provide session name: ntm --robot-history=myproject",
		)
	}

	// Verify session exists
	if !tmux.SessionExists(opts.Session) {
		// Session doesn't exist, but we might still have history
		// history.Exists() checks for global history file
		if !history.Exists() {
			return RobotError(
				fmt.Errorf("session '%s' not found and no history exists", opts.Session),
				ErrCodeSessionNotFound,
				"Use 'ntm list' to see available sessions",
			)
		}
	}

	output := HistoryOutput{
		RobotResponse: NewRobotResponse(true),
		Session:       opts.Session,
		GeneratedAt:   time.Now().UTC(),
	}

	// Stats mode
	if opts.Stats {
		stats, err := history.GetStats()
		if err != nil {
			return RobotError(
				fmt.Errorf("failed to get stats: %w", err),
				ErrCodeInternalError,
				"History file may be corrupted",
			)
		}
		// Filter stats for session if needed?
		// history.GetStats() returns global stats.
		// If we want session stats, we have to compute them.
		// Let's compute session stats manually for accuracy.
		entries, err := history.ReadForSession(opts.Session)
		if err == nil {
			sessionStats := &history.Stats{
				TotalEntries: len(entries),
			}
			for _, e := range entries {
				if e.Success {
					sessionStats.SuccessCount++
				} else {
					sessionStats.FailureCount++
				}
			}
			sessionStats.UniqueSessions = 1
			output.Stats = sessionStats
		} else {
			output.Stats = stats // Fallback to global
		}
		output.AgentHints = generateHistoryHints(output, opts)
		return encodeJSON(output)
	}

	// Get entries for the session
	// Note: opts.Session is guaranteed non-empty (checked at line 44)
	entries, err := history.ReadForSession(opts.Session)

	if err != nil {
		return RobotError(
			fmt.Errorf("failed to read history: %w", err),
			ErrCodeInternalError,
			"Check permissions on history file",
		)
	}

	output.Total = len(entries)

	// Filter entries
	var filtered []history.HistoryEntry
	var sinceTime time.Time

	if opts.Since != "" {
		var err error
		sinceTime, err = parseSinceTime(opts.Since)
		if err != nil {
			return RobotError(
				fmt.Errorf("invalid --since value: %w", err),
				ErrCodeInvalidFlag,
				"Use duration (1h, 30m, 2d) or ISO8601 date",
			)
		}
	}

	for _, e := range entries {
		// Filter by time
		if !sinceTime.IsZero() && e.Timestamp.Before(sinceTime) {
			continue
		}

		// Filter by pane/targets
		if opts.Pane != "" {
			// e.Targets contains pane indices or names
			found := false
			for _, t := range e.Targets {
				if t == opts.Pane {
					found = true
					break
				}
			}
			if !found {
				continue
			}
		}

		// Filter by AgentType (not directly stored, approximate via targets?)
		// We skip this for now as JSONL history doesn't store AgentType directly
		// unless we parse the targets or look up pane state.

		filtered = append(filtered, e)
	}

	// Apply limit (Last N)
	if opts.Last > 0 && len(filtered) > opts.Last {
		filtered = filtered[len(filtered)-opts.Last:]
	}

	output.Entries = filtered
	output.Filtered = len(filtered)
	output.AgentHints = generateHistoryHints(output, opts)

	return encodeJSON(output)
}

// parseSinceTime parses various time formats
func parseSinceTime(s string) (time.Time, error) {
	// Try duration format first (e.g., "1h", "30m", "2d")
	if dur, err := util.ParseDuration(s); err == nil {
		return time.Now().Add(-dur), nil
	}

	// Try RFC3339
	if t, err := time.Parse(time.RFC3339, s); err == nil {
		return t, nil
	}

	// Try date only
	if t, err := time.Parse("2006-01-02", s); err == nil {
		return t, nil
	}

	// Try relative formats
	s = strings.ToLower(strings.TrimSpace(s))
	if strings.HasSuffix(s, " ago") {
		s = strings.TrimSuffix(s, " ago")
		if dur, err := util.ParseDuration(s); err == nil {
			return time.Now().Add(-dur), nil
		}
	}

	return time.Time{}, fmt.Errorf("unrecognized time format: %s", s)
}

// generateHistoryHints creates actionable hints for AI agents
func generateHistoryHints(output HistoryOutput, opts HistoryOptions) *HistoryAgentHints {
	hints := &HistoryAgentHints{}

	// Build summary
	if output.Stats != nil {
		s := output.Stats
		hints.Summary = fmt.Sprintf("%d total commands", s.TotalEntries)
	} else if output.Total == 0 {
		hints.Summary = "No command history for this session"
	} else {
		hints.Summary = fmt.Sprintf("Showing %d of %d commands", output.Filtered, output.Total)
		if opts.Pane != "" {
			hints.Summary += fmt.Sprintf(" (pane %s)", opts.Pane)
		}
	}

	// Suggested commands
	hints.SuggestedCommands = []string{
		fmt.Sprintf("ntm --robot-history=%s --stats", opts.Session),
		fmt.Sprintf("ntm --robot-history=%s --last=10", opts.Session),
		fmt.Sprintf("ntm --robot-history=%s --since=1h", opts.Session),
	}

	if output.Total > 1000 {
		hints.Warnings = append(hints.Warnings,
			"Large history - consider using --prune or filtering")
	}

	return hints
}
