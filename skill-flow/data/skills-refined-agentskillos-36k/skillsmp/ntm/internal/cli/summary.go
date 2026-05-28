package cli

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/summary"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/util"
)

func newSummaryCmd() *cobra.Command {
	var (
		since   string
		format  string
		listAll bool
	)

	cmd := &cobra.Command{
		Use:   "summary [session]",
		Short: "Show activity summary for agents in a session",
		Long: `Display a summary of what each agent accomplished in a session.

Shows per-agent:
  - Active time and output volume
  - Files modified
  - Key actions (created, fixed, added, etc.)
  - Error counts

The summary is useful after parallel agent work to understand
what each agent did and identify potential conflicts.

Examples:
  ntm summary                      # Auto-detect session
  ntm summary myproject            # Specific session
  ntm summary --since 1h           # Look back 1 hour
  ntm summary --json               # Output as JSON
  ntm summary --all                # List all available sessions`,
		Args: cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			if listAll {
				return runSummaryList(format)
			}
			return runSummary(args, since, format)
		},
	}

	cmd.Flags().StringVar(&since, "since", "30m", "Duration to look back (e.g., 30m, 1h)")
	cmd.Flags().StringVar(&format, "format", "text", "Output format: text, json, detailed, or handoff")
	cmd.Flags().BoolVar(&listAll, "all", false, "List all available sessions")

	return cmd
}

func runSummary(args []string, sinceStr, format string) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	var session string
	if len(args) > 0 {
		session = args[0]
	}

	res, err := ResolveSession(session, os.Stdout)
	if err != nil {
		return err
	}
	if res.Session == "" {
		return nil
	}
	res.ExplainIfInferred(os.Stderr)
	session = res.Session

	if !tmux.SessionExists(session) {
		return fmt.Errorf("session '%s' not found", session)
	}

	// We'll use the since duration to potentially filter logs (if we enhanced capture)
	// For now, it's just validated.
	_, err = util.ParseDurationWithDefault(sinceStr, 30*time.Minute, "since")
	if err != nil {
		return fmt.Errorf("invalid --since: %w", err)
	}

	// Get panes
	panes, err := tmux.GetPanes(session)
	if err != nil {
		return fmt.Errorf("failed to get panes: %w", err)
	}

	// Build agent outputs
	var outputs []summary.AgentOutput
	for _, pane := range panes {
		agentType := string(pane.Type)
		if agentType == "" || agentType == "unknown" {
			continue // Skip non-agent panes
		}

		// Capture output (500 lines)
		out, _ := tmux.CapturePaneOutput(pane.ID, 500)

		outputs = append(outputs, summary.AgentOutput{
			AgentID:   pane.ID,
			AgentType: agentType,
			Output:    out,
		})
	}

	// Determine format
	sumFormat := summary.FormatBrief
	if format == "detailed" {
		sumFormat = summary.FormatDetailed
	} else if format == "handoff" {
		sumFormat = summary.FormatHandoff
	}

	wd, _ := os.Getwd()

	opts := summary.Options{
		Session:    session,
		Outputs:    outputs,
		Format:     sumFormat,
		ProjectKey: wd,
	}

	s, err := summary.SummarizeSession(context.Background(), opts)
	if err != nil {
		return err
	}

	// Output
	if IsJSONOutput() || format == "json" {
		return output.PrintJSON(s)
	}

	// Human-readable output
	fmt.Println(s.Text)
	return nil
}

func runSummaryList(format string) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	sessions, err := tmux.ListSessions()
	if err != nil {
		return fmt.Errorf("failed to list sessions: %w", err)
	}

	if len(sessions) == 0 {
		fmt.Println("No tmux sessions found.")
		return nil
	}

	// Output as JSON if requested
	if IsJSONOutput() || format == "json" {
		return output.PrintJSON(sessions)
	}

	// Human-readable output
	fmt.Println("Available sessions:")
	for _, s := range sessions {
		attached := ""
		if s.Attached {
			attached = " (attached)"
		}
		fmt.Printf("  %s - %d window(s), created %s%s\n", s.Name, s.Windows, s.Created, attached)
	}
	return nil
}
