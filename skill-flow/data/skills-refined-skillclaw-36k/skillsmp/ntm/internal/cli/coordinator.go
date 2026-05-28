package cli

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"slices"
	"strings"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/agentmail"
	"github.com/Dicklesworthstone/ntm/internal/bv"
	"github.com/Dicklesworthstone/ntm/internal/coordinator"
	"github.com/Dicklesworthstone/ntm/internal/robot"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

func newCoordinatorCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:     "coordinator",
		Aliases: []string{"coord"},
		Short:   "Manage session coordination for multi-agent workflows",
		Long: `Manage session coordination for multi-agent workflows.

The coordinator monitors agents, detects file conflicts, sends periodic
digests, and can automatically assign work to idle agents based on bv
triage recommendations.

Examples:
  ntm coordinator status myproject        # Show coordinator status
  ntm coordinator digest myproject        # Generate and display digest
  ntm coordinator conflicts myproject     # List current file conflicts
  ntm coordinator assign myproject        # Trigger work assignment

  # Enable/disable features (global config)
  ntm coordinator enable auto-assign
  ntm coordinator enable digest --interval=30m
  ntm coordinator disable conflict-negotiate`,
	}

	cmd.AddCommand(newCoordinatorStatusCmd())
	cmd.AddCommand(newCoordinatorDigestCmd())
	cmd.AddCommand(newCoordinatorConflictsCmd())
	cmd.AddCommand(newCoordinatorAssignCmd())
	cmd.AddCommand(newCoordinatorEnableCmd())
	cmd.AddCommand(newCoordinatorDisableCmd())

	return cmd
}

// newCoordinatorStatusCmd shows coordinator and agent status
func newCoordinatorStatusCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "status [session]",
		Short: "Show coordinator status for a session",
		Long: `Show the current coordinator status including:
- Agent states (idle, active, error)
- Context usage per agent
- Active file reservations
- Configuration settings

Examples:
  ntm coordinator status myproject
  ntm coordinator status myproject --json`,
		Args: cobra.MaximumNArgs(1),
		RunE: runCoordinatorStatus,
	}

	return cmd
}

func runCoordinatorStatus(cmd *cobra.Command, args []string) error {
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

	// Get working directory for project key
	projectKey, _ := os.Getwd()
	if cfg != nil {
		projectKey = cfg.GetProjectDir(session)
	}

	// Create coordinator to get status
	mailClient := agentmail.NewClient(agentmail.WithProjectKey(projectKey))
	coord := coordinator.New(session, projectKey, mailClient, "NTM-Coordinator")

	// Get agent states
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Start coordinator briefly to get current state
	if err := coord.Start(ctx); err != nil {
		return fmt.Errorf("starting coordinator: %w", err)
	}
	defer coord.Stop()

	// Give it a moment to poll
	time.Sleep(500 * time.Millisecond)

	agents := coord.GetAgents()
	idleAgents := coord.GetIdleAgents()

	// Use default coordinator config
	coordConfig := coordinator.DefaultCoordinatorConfig()

	if jsonOutput {
		return outputCoordinatorStatusJSON(session, agents, idleAgents, coordConfig)
	}

	return renderCoordinatorStatus(session, agents, idleAgents, coordConfig)
}

func outputCoordinatorStatusJSON(session string, agents map[string]*coordinator.AgentState, idleAgents []*coordinator.AgentState, coordCfg coordinator.CoordinatorConfig) error {
	result := map[string]interface{}{
		"session":     session,
		"timestamp":   time.Now().Format(time.RFC3339),
		"agent_count": len(agents),
		"idle_count":  len(idleAgents),
		"agents":      agents,
		"config": map[string]interface{}{
			"auto_assign":        coordCfg.AutoAssign,
			"send_digests":       coordCfg.SendDigests,
			"conflict_notify":    coordCfg.ConflictNotify,
			"conflict_negotiate": coordCfg.ConflictNegotiate,
			"poll_interval":      coordCfg.PollInterval.String(),
			"digest_interval":    coordCfg.DigestInterval.String(),
			"idle_threshold":     coordCfg.IdleThreshold,
		},
	}
	return json.NewEncoder(os.Stdout).Encode(result)
}

func renderCoordinatorStatus(session string, agents map[string]*coordinator.AgentState, idleAgents []*coordinator.AgentState, coordCfg coordinator.CoordinatorConfig) error {
	t := theme.Current()

	fmt.Printf("\n%s Coordinator Status: %s%s\n\n",
		colorize(t.Primary), session, "\033[0m")

	// Summary
	fmt.Printf("  %sAgents:%s %d total, %d idle\n",
		"\033[1m", "\033[0m", len(agents), len(idleAgents))
	fmt.Println()

	// Agent table
	if len(agents) > 0 {
		// Sort agents by PaneIndex for deterministic output
		sortedAgents := make([]*coordinator.AgentState, 0, len(agents))
		for _, agent := range agents {
			sortedAgents = append(sortedAgents, agent)
		}
		slices.SortFunc(sortedAgents, func(a, b *coordinator.AgentState) int {
			return a.PaneIndex - b.PaneIndex
		})

		fmt.Printf("  %sAgent Status%s\n", "\033[1m", "\033[0m")
		fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 60), "\033[0m")
		fmt.Printf("  %-12s %-8s %-12s %-8s %s\n",
			"Pane", "Type", "Status", "Context", "Idle For")
		fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 60), "\033[0m")

		for _, agent := range sortedAgents {
			statusColor := "\033[32m" // green
			switch agent.Status {
			case robot.StateError:
				statusColor = "\033[31m" // red
			case robot.StateGenerating, robot.StateThinking:
				statusColor = "\033[33m" // yellow
			}

			idleFor := "-"
			if !agent.LastActivity.IsZero() && agent.Status == robot.StateWaiting {
				idleFor = formatIdleDuration(time.Since(agent.LastActivity))
			}

			fmt.Printf("  %-12d %-8s %s%-12s%s %-8.0f%% %s\n",
				agent.PaneIndex, agent.AgentType,
				statusColor, string(agent.Status), "\033[0m",
				agent.ContextUsage, idleFor)
		}
		fmt.Println()
	}

	// Configuration
	fmt.Printf("  %sConfiguration%s\n", "\033[1m", "\033[0m")
	fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 60), "\033[0m")

	printConfigBool("  Auto-assign:         ", coordCfg.AutoAssign)
	printConfigBool("  Send digests:        ", coordCfg.SendDigests)
	printConfigBool("  Conflict notify:     ", coordCfg.ConflictNotify)
	printConfigBool("  Conflict negotiate:  ", coordCfg.ConflictNegotiate)
	fmt.Printf("  Poll interval:       %s\n", coordCfg.PollInterval)
	fmt.Printf("  Digest interval:     %s\n", coordCfg.DigestInterval)
	fmt.Printf("  Idle threshold:      %.0fs\n", coordCfg.IdleThreshold)
	fmt.Println()

	return nil
}

func printConfigBool(label string, value bool) {
	status := "\033[31m✗ disabled\033[0m"
	if value {
		status = "\033[32m✓ enabled\033[0m"
	}
	fmt.Printf("%s%s\n", label, status)
}

func formatIdleDuration(d time.Duration) string {
	if d < time.Minute {
		return fmt.Sprintf("%ds", int(d.Seconds()))
	}
	if d < time.Hour {
		return fmt.Sprintf("%dm", int(d.Minutes()))
	}
	return fmt.Sprintf("%dh%dm", int(d.Hours()), int(d.Minutes())%60)
}

// newCoordinatorDigestCmd generates a session digest
func newCoordinatorDigestCmd() *cobra.Command {
	var sendMail bool

	cmd := &cobra.Command{
		Use:   "digest [session]",
		Short: "Generate and display a session digest",
		Long: `Generate a summary digest of the current session state.

The digest includes:
- Agent counts and status breakdown
- Active/idle/error agent counts
- Context usage alerts
- Work summary (if beads available)

Examples:
  ntm coordinator digest myproject
  ntm coordinator digest myproject --send   # Also send via Agent Mail
  ntm coordinator digest myproject --json`,
		Args: cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCoordinatorDigest(cmd, args, sendMail)
		},
	}

	cmd.Flags().BoolVar(&sendMail, "send", false, "Send digest via Agent Mail")

	return cmd
}

func runCoordinatorDigest(cmd *cobra.Command, args []string, sendMail bool) error {
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

	projectKey, _ := os.Getwd()
	if cfg != nil {
		projectKey = cfg.GetProjectDir(session)
	}

	mailClient := agentmail.NewClient(agentmail.WithProjectKey(projectKey))
	coord := coordinator.New(session, projectKey, mailClient, "NTM-Coordinator")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := coord.Start(ctx); err != nil {
		return fmt.Errorf("starting coordinator: %w", err)
	}
	defer coord.Stop()

	time.Sleep(500 * time.Millisecond)

	digest := coord.GenerateDigest()

	if sendMail {
		if err := coord.SendDigest(ctx); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to send digest: %v\n", err)
		} else {
			fmt.Fprintf(os.Stderr, "Digest sent via Agent Mail\n")
		}
	}

	if jsonOutput {
		return json.NewEncoder(os.Stdout).Encode(digest)
	}

	return renderDigest(digest)
}

func renderDigest(digest coordinator.DigestSummary) error {
	t := theme.Current()

	fmt.Printf("\n%s Session Digest: %s%s\n",
		colorize(t.Primary), digest.Session, "\033[0m")
	fmt.Printf("  Generated: %s\n\n", digest.GeneratedAt.Format(time.RFC3339))

	// Summary
	fmt.Printf("  %sSummary%s\n", "\033[1m", "\033[0m")
	fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 40), "\033[0m")
	fmt.Printf("  Total Agents: %d\n", digest.AgentCount)
	fmt.Printf("  Active:       %d\n", digest.ActiveCount)
	fmt.Printf("  Idle:         %d\n", digest.IdleCount)
	if digest.ErrorCount > 0 {
		fmt.Printf("  %sErrors:       %d%s ⚠️\n", "\033[31m", digest.ErrorCount, "\033[0m")
	}
	fmt.Println()

	// Alerts
	if len(digest.Alerts) > 0 {
		fmt.Printf("  %sAlerts%s\n", "\033[1m", "\033[0m")
		fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 40), "\033[0m")
		for _, alert := range digest.Alerts {
			fmt.Printf("  %s⚠️  %s%s\n", "\033[33m", alert, "\033[0m")
		}
		fmt.Println()
	}

	// Agent table
	if len(digest.AgentStatuses) > 0 {
		fmt.Printf("  %sAgent Status%s\n", "\033[1m", "\033[0m")
		fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 50), "\033[0m")
		fmt.Printf("  %-6s %-8s %-12s %-8s %s\n",
			"Pane", "Type", "Status", "Context", "Idle")
		fmt.Printf("  %s%s%s\n", "\033[2m", strings.Repeat("─", 50), "\033[0m")

		for _, agent := range digest.AgentStatuses {
			idleFor := "-"
			if agent.IdleFor != "" {
				idleFor = agent.IdleFor
			}
			fmt.Printf("  %-6d %-8s %-12s %-8.0f%% %s\n",
				agent.PaneIndex, agent.AgentType, agent.Status,
				agent.ContextUsage, idleFor)
		}
		fmt.Println()
	}

	return nil
}

// newCoordinatorConflictsCmd lists file reservation conflicts
func newCoordinatorConflictsCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "conflicts [session]",
		Short: "List current file reservation conflicts",
		Long: `List any active file reservation conflicts between agents.

Conflicts occur when multiple agents hold overlapping file reservations.
The coordinator can notify holders or attempt automatic resolution.

Examples:
  ntm coordinator conflicts myproject
  ntm coordinator conflicts myproject --json`,
		Args: cobra.MaximumNArgs(1),
		RunE: runCoordinatorConflicts,
	}

	return cmd
}

func runCoordinatorConflicts(cmd *cobra.Command, args []string) error {
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

	projectKey, _ := os.Getwd()
	if cfg != nil {
		projectKey = cfg.GetProjectDir(session)
	}

	mailClient := agentmail.NewClient(agentmail.WithProjectKey(projectKey))

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	detector := coordinator.NewConflictDetector(mailClient, projectKey)
	conflicts, err := detector.DetectConflicts(ctx)
	if err != nil {
		return fmt.Errorf("detecting conflicts: %w", err)
	}

	if jsonOutput {
		return json.NewEncoder(os.Stdout).Encode(map[string]interface{}{
			"session":   session,
			"conflicts": conflicts,
			"count":     len(conflicts),
		})
	}

	t := theme.Current()
	fmt.Printf("\n%s File Conflicts: %s%s\n\n",
		colorize(t.Primary), session, "\033[0m")

	if len(conflicts) == 0 {
		fmt.Println("  No active conflicts detected.")
		fmt.Println()
		return nil
	}

	for _, c := range conflicts {
		fmt.Printf("  %s⚠️  %s%s\n", "\033[33m", c.Pattern, "\033[0m")
		fmt.Printf("     Detected: %s\n", c.DetectedAt.Format(time.RFC3339))
		fmt.Printf("     Holders:\n")
		for _, h := range c.Holders {
			fmt.Printf("       - %s (reserved %s, expires %s)\n",
				h.AgentName,
				h.ReservedAt.Format("15:04:05"),
				h.ExpiresAt.Format("15:04:05"))
			if h.Reason != "" {
				fmt.Printf("         Reason: %s\n", h.Reason)
			}
		}
		fmt.Println()
	}

	return nil
}

// newCoordinatorAssignCmd triggers work assignment
func newCoordinatorAssignCmd() *cobra.Command {
	var dryRun bool

	cmd := &cobra.Command{
		Use:   "assign [session]",
		Short: "Trigger work assignment to idle agents",
		Long: `Assign work to idle agents based on bv triage recommendations.

Uses the bv graph analysis to find the highest-impact unblocked work
and assigns it to available idle agents.

Examples:
  ntm coordinator assign myproject
  ntm coordinator assign myproject --dry-run   # Preview without sending
  ntm coordinator assign myproject --json`,
		Args: cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCoordinatorAssign(cmd, args, dryRun)
		},
	}

	cmd.Flags().BoolVar(&dryRun, "dry-run", false, "Preview assignments without executing")

	return cmd
}

func runCoordinatorAssign(cmd *cobra.Command, args []string, dryRun bool) error {
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

	projectKey, _ := os.Getwd()
	if cfg != nil {
		projectKey = cfg.GetProjectDir(session)
	}

	mailClient := agentmail.NewClient(agentmail.WithProjectKey(projectKey))
	coord := coordinator.New(session, projectKey, mailClient, "NTM-Coordinator")

	// Enable auto-assign for this call
	coordCfg := coordinator.DefaultCoordinatorConfig()
	coordCfg.AutoAssign = true
	coord.WithConfig(coordCfg)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := coord.Start(ctx); err != nil {
		return fmt.Errorf("starting coordinator: %w", err)
	}
	defer coord.Stop()

	time.Sleep(500 * time.Millisecond)

	// Get idle agents and assignable work
	idleAgents := coord.GetIdleAgents()
	work, err := coord.GetAssignableWork(ctx)
	if err != nil {
		return fmt.Errorf("getting assignable work: %w", err)
	}

	if dryRun {
		return outputAssignmentPreview(session, idleAgents, work)
	}

	// Perform actual assignment
	results, err := coord.AssignWork(ctx)
	if err != nil {
		return fmt.Errorf("assigning work: %w", err)
	}

	if jsonOutput {
		return json.NewEncoder(os.Stdout).Encode(map[string]interface{}{
			"session":     session,
			"assignments": results,
			"count":       len(results),
		})
	}

	t := theme.Current()
	fmt.Printf("\n%s Work Assignment: %s%s\n\n",
		colorize(t.Primary), session, "\033[0m")

	if len(results) == 0 {
		fmt.Println("  No assignments made.")
		if len(idleAgents) == 0 {
			fmt.Println("  (No idle agents available)")
		} else if len(work) == 0 {
			fmt.Println("  (No assignable work found)")
		}
		fmt.Println()
		return nil
	}

	for _, r := range results {
		if r.Success && r.Assignment != nil {
			fmt.Printf("  %s✓%s Assigned %s to pane %s\n",
				"\033[32m", "\033[0m",
				r.Assignment.BeadID, r.Assignment.AgentPaneID)
			if r.MessageSent {
				fmt.Println("    (Message sent via Agent Mail)")
			}
		} else if !r.Success {
			fmt.Printf("  %s✗%s Failed: %s\n",
				"\033[31m", "\033[0m", r.Error)
		}
	}
	fmt.Println()

	return nil
}

func outputAssignmentPreview(session string, idleAgents []*coordinator.AgentState, work []bv.TriageRecommendation) error {
	if jsonOutput {
		return json.NewEncoder(os.Stdout).Encode(map[string]interface{}{
			"session":         session,
			"dry_run":         true,
			"idle_agents":     idleAgents,
			"assignable_work": work,
			"would_assign":    min(len(idleAgents), len(work)),
		})
	}

	fmt.Printf("\n  Dry Run - Assignment Preview\n")
	fmt.Printf("  %s%s%s\n\n", "\033[2m", strings.Repeat("─", 40), "\033[0m")

	fmt.Printf("  Idle agents: %d\n", len(idleAgents))
	for _, a := range idleAgents {
		fmt.Printf("    - Pane %d (%s)\n", a.PaneIndex, a.AgentType)
	}
	fmt.Println()

	fmt.Printf("  Assignable work: %d items\n", len(work))
	for i, w := range work {
		if i >= 5 {
			fmt.Printf("    ... and %d more\n", len(work)-5)
			break
		}
		fmt.Printf("    - %s: %s (score: %.2f)\n", w.ID, w.Title, w.Score)
	}
	fmt.Println()

	wouldAssign := min(len(idleAgents), len(work))
	fmt.Printf("  Would assign: %d items\n\n", wouldAssign)

	return nil
}

// newCoordinatorEnableCmd enables coordinator features
func newCoordinatorEnableCmd() *cobra.Command {
	var interval string

	cmd := &cobra.Command{
		Use:   "enable <feature>",
		Short: "Enable a coordinator feature",
		Long: `Enable a coordinator feature globally.

Available features:
  auto-assign         - Automatically assign work to idle agents
  digest              - Send periodic digest summaries
  conflict-notify     - Notify when conflicts are detected
  conflict-negotiate  - Attempt automatic conflict resolution

Note: These settings are configured globally in ~/.config/ntm/config.toml.

Examples:
  ntm coordinator enable auto-assign
  ntm coordinator enable digest --interval=30m
  ntm coordinator enable conflict-notify`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCoordinatorToggle(cmd, args, true, interval)
		},
	}

	cmd.Flags().StringVar(&interval, "interval", "", "Interval for digest (e.g., 5m, 30m, 1h)")

	return cmd
}

// newCoordinatorDisableCmd disables coordinator features
func newCoordinatorDisableCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "disable <feature>",
		Short: "Disable a coordinator feature",
		Long: `Disable a coordinator feature globally.

Available features:
  auto-assign         - Automatic work assignment
  digest              - Periodic digest summaries
  conflict-notify     - Conflict notifications
  conflict-negotiate  - Automatic conflict resolution

Note: These settings are configured globally in ~/.config/ntm/config.toml.

Examples:
  ntm coordinator disable auto-assign
  ntm coordinator disable digest`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCoordinatorToggle(cmd, args, false, "")
		},
	}

	return cmd
}

func runCoordinatorToggle(cmd *cobra.Command, args []string, enable bool, interval string) error {
	feature := args[0]

	// Validate feature name
	validFeatures := []string{"auto-assign", "digest", "conflict-notify", "conflict-negotiate"}
	valid := false
	for _, f := range validFeatures {
		if f == feature {
			valid = true
			break
		}
	}

	if !valid {
		return fmt.Errorf("unknown feature '%s'. Valid features: %s",
			feature, strings.Join(validFeatures, ", "))
	}

	action := "disabled"
	if enable {
		action = "enabled"
	}

	// Show configuration instructions
	if jsonOutput {
		return json.NewEncoder(os.Stdout).Encode(map[string]interface{}{
			"feature":     feature,
			"enabled":     enable,
			"config_hint": fmt.Sprintf("Add to ~/.config/ntm/config.toml under [coordinator] section"),
		})
	}

	status := "\033[31m✗ " + action + "\033[0m"
	if enable {
		status = "\033[32m✓ " + action + "\033[0m"
	}

	fmt.Printf("Coordinator feature '%s': %s\n\n", feature, status)

	// Show config instructions
	fmt.Printf("To persist this setting, add to ~/.config/ntm/config.toml:\n\n")
	fmt.Printf("  [coordinator]\n")

	switch feature {
	case "auto-assign":
		fmt.Printf("  auto_assign = %t\n", enable)
	case "digest":
		fmt.Printf("  send_digests = %t\n", enable)
		if enable && interval != "" {
			fmt.Printf("  digest_interval = \"%s\"\n", interval)
		}
	case "conflict-notify":
		fmt.Printf("  conflict_notify = %t\n", enable)
	case "conflict-negotiate":
		fmt.Printf("  conflict_negotiate = %t\n", enable)
	}
	fmt.Println()

	return nil
}
