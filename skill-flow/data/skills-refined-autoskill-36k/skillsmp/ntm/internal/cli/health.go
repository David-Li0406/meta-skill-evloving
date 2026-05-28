package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/charmbracelet/lipgloss"
	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/health"
	"github.com/Dicklesworthstone/ntm/internal/robot"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

var (
	healthWatch    bool
	healthInterval int
	healthVerbose  bool
	healthPane     int
	healthStatus   string
)

func newHealthCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "health [session]",
		Short: "Check health status of agents in a session",
		Long: `Check health status of all agents in a session.

Reports:
  - Process status (running/exited)
  - Activity level (active/idle/stale)
  - Uptime and restart counts
  - Detected issues (rate limits, crashes, errors)

Examples:
  ntm health myproject              # Check health of all agents
  ntm health myproject --json       # Output as JSON
  ntm health myproject --watch      # Auto-refresh every 5s
  ntm health myproject --watch -i 2 # Auto-refresh every 2s
  ntm health myproject --verbose    # Show full error details
  ntm health myproject --pane 1     # Filter to specific pane
  ntm health myproject --status ok  # Filter by status (ok/warning/error)`,
		Args: cobra.MaximumNArgs(1),
		RunE: runHealth,
	}

	cmd.Flags().BoolVarP(&healthWatch, "watch", "w", false, "Auto-refresh health display")
	cmd.Flags().IntVarP(&healthInterval, "interval", "i", 5, "Refresh interval in seconds (with --watch)")
	cmd.Flags().BoolVarP(&healthVerbose, "verbose", "v", false, "Show full error details")
	cmd.Flags().IntVar(&healthPane, "pane", -1, "Filter to specific pane index")
	cmd.Flags().StringVar(&healthStatus, "status", "", "Filter by status (ok, warning, error)")
	cmd.ValidArgsFunction = completeSessionArgs
	_ = cmd.RegisterFlagCompletionFunc("pane", completePaneIndexes)

	return cmd
}

func runHealth(cmd *cobra.Command, args []string) error {
	var session string

	if len(args) > 0 {
		session = args[0]
	}

	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	res, err := ResolveSession(session, cmd.OutOrStdout())
	if err != nil {
		return err
	}
	if res.Session == "" {
		return nil
	}
	res.ExplainIfInferred(cmd.ErrOrStderr())
	session = res.Session

	// Validate interval
	if healthInterval < 1 {
		healthInterval = 1
	}

	// Validate status filter
	if healthStatus != "" {
		healthStatus = strings.ToLower(healthStatus)
		if healthStatus != "ok" && healthStatus != "warning" && healthStatus != "error" {
			return fmt.Errorf("invalid status filter '%s': must be ok, warning, or error", healthStatus)
		}
	}

	// Watch mode - continuous refresh
	if healthWatch {
		return runHealthWatch(session)
	}

	// Single check
	return runHealthOnce(session)
}

// runHealthOnce performs a single health check and outputs the result
func runHealthOnce(session string) error {
	result, err := health.CheckSession(session)
	if err != nil {
		if _, ok := err.(*health.SessionNotFoundError); ok {
			if jsonOutput {
				return outputHealthJSON(&health.SessionHealth{
					Session: session,
					Summary: health.HealthSummary{},
					Agents:  []health.AgentHealth{},
				}, fmt.Errorf("session '%s' not found", session))
			}
			return fmt.Errorf("session '%s' not found", session)
		}
		return err
	}

	// Apply filters
	result = filterHealthResult(result)

	// Enrich with tracker data (uptime, restarts)
	enrichHealthResult(session, result)

	if jsonOutput {
		return outputHealthJSON(result, nil)
	}

	return renderHealthTUI(result)
}

// runHealthWatch continuously refreshes health display
func runHealthWatch(session string) error {
	// Set up signal handling for clean exit
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	ticker := time.NewTicker(time.Duration(healthInterval) * time.Second)
	defer ticker.Stop()

	// Initial display
	clearScreen()
	if err := runHealthOnce(session); err != nil {
		return err
	}

	for {
		select {
		case <-sigChan:
			fmt.Println("\nStopping health watch...")
			return nil
		case <-ticker.C:
			clearScreen()
			if err := runHealthOnce(session); err != nil {
				// Don't exit on transient errors in watch mode
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			}
		}
	}
}

// clearScreen clears the terminal screen for watch mode
func clearScreen() {
	fmt.Print("\033[H\033[2J")
}

// filterHealthResult applies pane and status filters to the result
func filterHealthResult(result *health.SessionHealth) *health.SessionHealth {
	if healthPane < 0 && healthStatus == "" {
		return result // No filters
	}

	filtered := &health.SessionHealth{
		Session:       result.Session,
		CheckedAt:     result.CheckedAt,
		Agents:        make([]health.AgentHealth, 0),
		Summary:       health.HealthSummary{},
		OverallStatus: health.StatusOK,
	}

	for _, agent := range result.Agents {
		// Pane filter
		if healthPane >= 0 && agent.Pane != healthPane {
			continue
		}

		// Status filter
		if healthStatus != "" {
			statusStr := strings.ToLower(string(agent.Status))
			if statusStr != healthStatus {
				continue
			}
		}

		filtered.Agents = append(filtered.Agents, agent)

		// Update summary
		filtered.Summary.Total++
		switch agent.Status {
		case health.StatusOK:
			filtered.Summary.Healthy++
		case health.StatusWarning:
			filtered.Summary.Warning++
		case health.StatusError:
			filtered.Summary.Error++
		default:
			filtered.Summary.Unknown++
		}

		// Update overall status
		if statusSeverity(agent.Status) > statusSeverity(filtered.OverallStatus) {
			filtered.OverallStatus = agent.Status
		}
	}

	return filtered
}

// statusSeverity returns numeric severity for status comparison
func statusSeverity(s health.Status) int {
	switch s {
	case health.StatusOK:
		return 0
	case health.StatusWarning:
		return 1
	case health.StatusError:
		return 2
	default:
		return 0
	}
}

// enrichHealthResult adds uptime and restart data from the health tracker
func enrichHealthResult(session string, result *health.SessionHealth) {
	tracker := robot.GetHealthTracker(session)

	for i := range result.Agents {
		agent := &result.Agents[i]
		metrics, ok := tracker.GetHealth(agent.PaneID)
		if !ok {
			continue
		}

		// Add uptime info to issues for display
		uptime := tracker.GetUptime(agent.PaneID)
		restarts := tracker.GetRestartsInWindow(agent.PaneID)

		if restarts > 0 {
			agent.Issues = append(agent.Issues, health.Issue{
				Type:    "restart_count",
				Message: fmt.Sprintf("%d restarts in last hour", restarts),
			})
		}

		// Store uptime in IdleSeconds as a secondary metric if not already set
		if agent.IdleSeconds == 0 && uptime > 0 {
			// Use a special indicator - this is a bit of a hack but keeps compatibility
			agent.IdleSeconds = -int(uptime.Seconds()) // Negative = uptime, positive = idle
		}

		// Add last error info if verbose and there's an error
		if healthVerbose && metrics.LastError != nil {
			agent.Issues = append(agent.Issues, health.Issue{
				Type:    metrics.LastError.Type,
				Message: metrics.LastError.Message,
			})
		}
	}
}

func outputHealthJSON(result *health.SessionHealth, err error) error {
	type jsonOutput struct {
		*health.SessionHealth
		Error string `json:"error,omitempty"`
	}

	output := jsonOutput{SessionHealth: result}
	if err != nil {
		output.Error = err.Error()
	}

	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	return encoder.Encode(output)
}

func renderHealthTUI(result *health.SessionHealth) error {
	// Define styles
	titleStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("99"))

	okStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("42"))     // Green
	warnStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("214"))  // Orange
	errorStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("196")) // Red
	mutedStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("240")) // Gray

	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("240")).
		Padding(0, 1)

	// Status icon helper
	statusIcon := func(s health.Status) string {
		switch s {
		case health.StatusOK:
			return okStyle.Render("✓ OK")
		case health.StatusWarning:
			return warnStyle.Render("⚠ WARN")
		case health.StatusError:
			return errorStyle.Render("✗ ERROR")
		default:
			return mutedStyle.Render("? UNKNOWN")
		}
	}

	// Activity indicator
	activityStr := func(a health.ActivityLevel) string {
		switch a {
		case health.ActivityActive:
			return okStyle.Render("active")
		case health.ActivityIdle:
			return mutedStyle.Render("idle")
		case health.ActivityStale:
			return warnStyle.Render("stale")
		default:
			return mutedStyle.Render("unknown")
		}
	}

	// Format uptime/idle duration
	formatDuration := func(seconds int) string {
		if seconds == 0 {
			return "-"
		}
		// Negative means uptime (encoded in enrichHealthResult)
		if seconds < 0 {
			seconds = -seconds
			hours := seconds / 3600
			mins := (seconds % 3600) / 60
			if hours > 0 {
				return fmt.Sprintf("up %dh%dm", hours, mins)
			}
			return fmt.Sprintf("up %dm", mins)
		}
		// Positive means idle time
		mins := seconds / 60
		if mins > 0 {
			return fmt.Sprintf("idle %dm", mins)
		}
		return fmt.Sprintf("idle %ds", seconds)
	}

	// Build header
	fmt.Println()
	fmt.Printf("%s %s\n", titleStyle.Render("Session:"), result.Session)
	if healthWatch {
		fmt.Printf("%s %s (refreshing every %ds)\n",
			mutedStyle.Render("Checked:"),
			result.CheckedAt.Format("15:04:05"),
			healthInterval)
	}
	fmt.Println()

	// Build table header - include Uptime column
	header := fmt.Sprintf("%-6s │ %-10s │ %-10s │ %-10s │ %-12s │ %s",
		"Pane", "Agent", "Status", "Activity", "Uptime", "Issues")
	fmt.Println(mutedStyle.Render(header))
	fmt.Println(mutedStyle.Render(strings.Repeat("─", 85)))

	// Build table rows
	for _, agent := range result.Agents {
		// Format issues
		issueStr := "-"
		if len(agent.Issues) > 0 {
			var issueStrs []string
			for _, issue := range agent.Issues {
				// Skip restart_count in issues display (shown separately in uptime)
				if issue.Type == "restart_count" {
					continue
				}
				issueStrs = append(issueStrs, issue.Message)
			}
			if len(issueStrs) > 0 {
				issueStr = strings.Join(issueStrs, ", ")
			}
		}

		// Add stale timing if relevant and not already showing issues
		if agent.Activity == health.ActivityStale && agent.IdleSeconds > 0 && issueStr == "-" {
			mins := agent.IdleSeconds / 60
			if mins > 0 {
				issueStr = fmt.Sprintf("no output %dm", mins)
			}
		}

		// Format uptime/idle
		uptimeStr := formatDuration(agent.IdleSeconds)

		// Check for restart count in issues
		for _, issue := range agent.Issues {
			if issue.Type == "restart_count" {
				uptimeStr = fmt.Sprintf("%s (%s)", uptimeStr, issue.Message)
				break
			}
		}

		row := fmt.Sprintf("%-6d │ %-10s │ %-10s │ %-10s │ %-12s │ %s",
			agent.Pane,
			truncateString(agent.AgentType, 10),
			statusIcon(agent.Status),
			activityStr(agent.Activity),
			truncateString(uptimeStr, 12),
			issueStr)
		fmt.Println(row)

		// In verbose mode, show additional details
		if healthVerbose && len(agent.Issues) > 0 {
			for _, issue := range agent.Issues {
				if issue.Type == "restart_count" {
					continue // Already shown in uptime column
				}
				fmt.Printf("       │ %s: %s\n",
					mutedStyle.Render(issue.Type),
					issue.Message)
			}
		}
	}

	fmt.Println()

	// Summary box
	summary := fmt.Sprintf("Overall: %d healthy, %d warning, %d error",
		result.Summary.Healthy,
		result.Summary.Warning,
		result.Summary.Error)
	fmt.Println(boxStyle.Render(summary))
	fmt.Println()

	// Don't exit in watch mode - only set exit code on final display
	if !healthWatch {
		if result.OverallStatus == health.StatusError {
			os.Exit(2)
		} else if result.OverallStatus == health.StatusWarning {
			os.Exit(1)
		}
	}

	return nil
}

// truncateString truncates a string to maxLen runes with ellipsis if needed
func truncateString(s string, maxLen int) string {
	runes := []rune(s)
	if len(runes) <= maxLen {
		return s
	}
	if maxLen <= 1 {
		return string(runes[:maxLen])
	}
	return string(runes[:maxLen-1]) + "…"
}
