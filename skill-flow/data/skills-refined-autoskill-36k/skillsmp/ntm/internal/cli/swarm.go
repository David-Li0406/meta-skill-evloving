package cli

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/swarm"
)

func newSwarmCmd() *cobra.Command {
	var (
		scanDir         string
		projects        []string
		dryRun          bool
		remote          string
		jsonOutput      bool
		sessionsPerType int
		panesPerSession int
		outputPath      string
	)

	cmd := &cobra.Command{
		Use:   "swarm",
		Short: "Orchestrate weighted multi-project agent swarm",
		Long: `Create and manage a weighted swarm of AI agents across multiple projects.

The swarm system allocates agents based on each project's open bead count:
  - Tier 1 (≥400 beads): Heavy allocation (e.g., 4 CC, 4 Codex, 2 Gemini)
  - Tier 2 (≥100 beads): Medium allocation (e.g., 3 CC, 3 Codex, 2 Gemini)
  - Tier 3 (<100 beads): Light allocation (e.g., 1 CC, 1 Codex, 1 Gemini)

Examples:
  ntm swarm                           # Scan /dp and create swarm
  ntm swarm --scan-dir=/projects      # Scan custom directory
  ntm swarm --dry-run                 # Preview plan without executing
  ntm swarm --projects=foo,bar        # Only include specific projects
  ntm swarm --remote=user@host        # Execute on remote host via SSH`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runSwarm(swarmOptions{
				ScanDir:         scanDir,
				Projects:        projects,
				DryRun:          dryRun,
				Remote:          remote,
				JSONOutput:      jsonOutput,
				SessionsPerType: sessionsPerType,
				PanesPerSession: panesPerSession,
				OutputPath:      outputPath,
			})
		},
	}

	// Set default scan dir from config or /dp
	defaultScanDir := "/dp"
	if cfg != nil && cfg.Swarm.DefaultScanDir != "" {
		defaultScanDir = cfg.Swarm.DefaultScanDir
	}
	defaultSessionsPerType := 3
	if cfg != nil && cfg.Swarm.SessionsPerType > 0 {
		defaultSessionsPerType = cfg.Swarm.SessionsPerType
	}

	cmd.Flags().StringVar(&scanDir, "scan-dir", defaultScanDir, "Directory to scan for projects")
	cmd.Flags().StringSliceVar(&projects, "projects", nil, "Explicit list of project paths (comma-separated)")
	cmd.Flags().BoolVar(&dryRun, "dry-run", false, "Preview plan without creating sessions")
	cmd.Flags().StringVar(&remote, "remote", "", "Remote host for SSH execution (user@host)")
	cmd.Flags().BoolVar(&jsonOutput, "json", false, "Output plan as JSON")
	cmd.Flags().IntVar(&sessionsPerType, "sessions-per-type", defaultSessionsPerType, "Number of tmux sessions per agent type (default: 3)")
	cmd.Flags().IntVar(&panesPerSession, "panes-per-session", 0, "Max panes per session (0 = auto-calculate from total agents)")
	cmd.Flags().StringVar(&outputPath, "output", "", "Write swarm plan to JSON file (optional)")

	// Add subcommands
	cmd.AddCommand(newSwarmPlanCmd())
	cmd.AddCommand(newSwarmStatusCmd())
	cmd.AddCommand(newSwarmStopCmd())

	return cmd
}

type swarmOptions struct {
	ScanDir         string
	Projects        []string
	DryRun          bool
	Remote          string
	JSONOutput      bool
	SessionsPerType int
	PanesPerSession int
	OutputPath      string
}

// SwarmPlanOutput is the JSON output format for swarm plan
type SwarmPlanOutput struct {
	ScanDir         string             `json:"scan_dir"`
	TotalCC         int                `json:"total_cc"`
	TotalCod        int                `json:"total_cod"`
	TotalGmi        int                `json:"total_gmi"`
	TotalAgents     int                `json:"total_agents"`
	SessionsPerType int                `json:"sessions_per_type"`
	PanesPerSession int                `json:"panes_per_session"`
	Allocations     []AllocationOutput `json:"allocations"`
	Sessions        []SessionOutput    `json:"sessions"`
	DryRun          bool               `json:"dry_run"`
	Error           string             `json:"error,omitempty"`
}

type AllocationOutput struct {
	Project     string `json:"project"`
	Path        string `json:"path"`
	OpenBeads   int    `json:"open_beads"`
	Tier        int    `json:"tier"`
	CCAgents    int    `json:"cc_agents"`
	CodAgents   int    `json:"cod_agents"`
	GmiAgents   int    `json:"gmi_agents"`
	TotalAgents int    `json:"total_agents"`
}

type SessionOutput struct {
	Name      string       `json:"name"`
	AgentType string       `json:"agent_type"`
	PaneCount int          `json:"pane_count"`
	Panes     []PaneOutput `json:"panes"`
}

type PaneOutput struct {
	Index     int    `json:"index"`
	Project   string `json:"project"`
	AgentType string `json:"agent_type"`
}

func runSwarm(opts swarmOptions) error {
	logger := slog.Default()

	// Get swarm config
	swarmCfg := cfg.Swarm
	if !swarmCfg.Enabled && !opts.DryRun {
		return fmt.Errorf("swarm orchestration is disabled in config; set swarm.enabled=true or use --dry-run")
	}

	if opts.SessionsPerType < 1 {
		return fmt.Errorf("--sessions-per-type must be at least 1, got %d", opts.SessionsPerType)
	}
	if opts.SessionsPerType > 10 {
		logger.Warn("high sessions-per-type may impact performance", "value", opts.SessionsPerType)
	}
	swarmCfg.SessionsPerType = opts.SessionsPerType

	if opts.PanesPerSession < 0 {
		return fmt.Errorf("--panes-per-session cannot be negative, got %d", opts.PanesPerSession)
	}
	if opts.PanesPerSession > 20 {
		logger.Warn("high panes-per-session may impact performance", "value", opts.PanesPerSession)
	}
	swarmCfg.PanesPerSession = opts.PanesPerSession
	if opts.PanesPerSession > 0 {
		logger.Info("session configuration", "sessions_per_type", opts.SessionsPerType, "panes_per_session", opts.PanesPerSession, "mode", "manual")
	} else {
		logger.Info("session configuration", "sessions_per_type", opts.SessionsPerType, "panes_per_session", "auto", "mode", "auto-calculate")
	}

	// Discover projects
	projects, err := discoverProjects(opts.ScanDir, opts.Projects)
	if err != nil {
		return fmt.Errorf("failed to discover projects: %w", err)
	}

	if len(projects) == 0 {
		if opts.JSONOutput {
			return printSwarmJSON(SwarmPlanOutput{
				ScanDir: opts.ScanDir,
				DryRun:  opts.DryRun,
				Error:   "no projects found",
			})
		}
		return fmt.Errorf("no projects found in %s", opts.ScanDir)
	}

	// Calculate allocations
	calc := swarm.NewAllocationCalculator(&swarmCfg)
	plan := calc.GenerateSwarmPlan(opts.ScanDir, projects)
	logger.Info("calculated panes per session",
		"sessions_per_type", plan.SessionsPerType,
		"panes_per_session", plan.PanesPerSession,
	)

	if opts.OutputPath != "" {
		if err := writePlanToFile(plan, opts.OutputPath); err != nil {
			return fmt.Errorf("write plan: %w", err)
		}
		logger.Info("swarm plan written", "path", opts.OutputPath)
	}

	// Build output
	out := buildSwarmPlanOutput(plan, opts.DryRun)

	if opts.JSONOutput {
		return printSwarmJSON(out)
	}

	// Pretty print plan
	printSwarmPlan(out)

	if opts.DryRun {
		output.PrintInfo("Dry run - no sessions created")
		return nil
	}

	// Create the orchestrator
	var orch *swarm.SessionOrchestrator
	if opts.Remote != "" {
		orch = swarm.NewRemoteSessionOrchestrator(opts.Remote)
		output.PrintInfof("Creating swarm on remote host: %s", opts.Remote)
	} else {
		orch = swarm.NewSessionOrchestrator()
	}

	// Execute the plan
	result, err := orch.CreateSessions(plan)
	if err != nil {
		return fmt.Errorf("failed to create sessions: %w", err)
	}

	// Report results
	output.PrintSuccessf("Created %d sessions with %d/%d panes",
		len(result.Sessions), result.SuccessfulPanes, result.TotalPanes)

	if result.FailedPanes > 0 {
		output.PrintWarningf("%d panes failed to create", result.FailedPanes)
		for _, err := range result.Errors {
			fmt.Fprintf(os.Stderr, "  %v\n", err)
		}
	}

	return nil
}

// discoverProjects finds projects with bead counts using BeadScanner
func discoverProjects(scanDir string, explicitProjects []string) ([]swarm.ProjectBeadCount, error) {
	var opts []swarm.BeadScannerOption

	if len(explicitProjects) > 0 {
		opts = append(opts, swarm.WithExplicitProjects(explicitProjects))
	}

	scanner := swarm.NewBeadScanner(scanDir, opts...)
	result, err := scanner.Scan(context.Background())
	if err != nil {
		return nil, fmt.Errorf("scan projects: %w", err)
	}

	return result.Projects, nil
}

func buildSwarmPlanOutput(plan *swarm.SwarmPlan, dryRun bool) SwarmPlanOutput {
	out := SwarmPlanOutput{
		ScanDir:         plan.ScanDir,
		TotalCC:         plan.TotalCC,
		TotalCod:        plan.TotalCod,
		TotalGmi:        plan.TotalGmi,
		TotalAgents:     plan.TotalAgents,
		SessionsPerType: plan.SessionsPerType,
		PanesPerSession: plan.PanesPerSession,
		Allocations:     make([]AllocationOutput, 0, len(plan.Allocations)),
		Sessions:        make([]SessionOutput, 0, len(plan.Sessions)),
		DryRun:          dryRun,
	}

	for _, alloc := range plan.Allocations {
		out.Allocations = append(out.Allocations, AllocationOutput{
			Project:     alloc.Project.Name,
			Path:        alloc.Project.Path,
			OpenBeads:   alloc.Project.OpenBeads,
			Tier:        alloc.Project.Tier,
			CCAgents:    alloc.CCAgents,
			CodAgents:   alloc.CodAgents,
			GmiAgents:   alloc.GmiAgents,
			TotalAgents: alloc.TotalAgents,
		})
	}

	for _, sess := range plan.Sessions {
		sessOut := SessionOutput{
			Name:      sess.Name,
			AgentType: sess.AgentType,
			PaneCount: sess.PaneCount,
			Panes:     make([]PaneOutput, 0, len(sess.Panes)),
		}
		for _, pane := range sess.Panes {
			sessOut.Panes = append(sessOut.Panes, PaneOutput{
				Index:     pane.Index,
				Project:   pane.Project,
				AgentType: pane.AgentType,
			})
		}
		out.Sessions = append(out.Sessions, sessOut)
	}

	return out
}

func printSwarmPlan(out SwarmPlanOutput) {
	printSwarmHeader("Swarm Plan")
	fmt.Printf("  Scan Directory: %s\n", out.ScanDir)
	fmt.Printf("  Total Agents:   %d (CC: %d, Codex: %d, Gemini: %d)\n",
		out.TotalAgents, out.TotalCC, out.TotalCod, out.TotalGmi)
	fmt.Printf("  Sessions:       %d per type, %d panes max each\n",
		out.SessionsPerType, out.PanesPerSession)
	fmt.Println()

	printSwarmHeader("Project Allocations")
	for _, alloc := range out.Allocations {
		tierStr := fmt.Sprintf("T%d", alloc.Tier)
		fmt.Printf("  %-20s [%s] %d beads → CC:%d Cod:%d Gmi:%d\n",
			alloc.Project, tierStr, alloc.OpenBeads,
			alloc.CCAgents, alloc.CodAgents, alloc.GmiAgents)
	}
	fmt.Println()

	printSwarmHeader("Sessions")
	for _, sess := range out.Sessions {
		fmt.Printf("  %s (%d panes)\n", sess.Name, sess.PaneCount)
	}
}

func printSwarmHeader(title string) {
	fmt.Printf("\n\033[1m%s\033[0m\n", title)
}

func printSwarmJSON(v interface{}) error {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	return enc.Encode(v)
}

func writePlanToFile(plan *swarm.SwarmPlan, path string) error {
	if plan == nil {
		return fmt.Errorf("plan cannot be nil")
	}
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("create directory: %w", err)
	}

	data, err := json.MarshalIndent(plan, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal plan: %w", err)
	}

	tmpPath := path + ".tmp"
	if err := os.WriteFile(tmpPath, data, 0644); err != nil {
		return err
	}
	if err := os.Rename(tmpPath, path); err != nil {
		return err
	}
	return nil
}

// Subcommand: swarm plan
func newSwarmPlanCmd() *cobra.Command {
	var (
		scanDir  string
		projects []string
	)

	cmd := &cobra.Command{
		Use:   "plan",
		Short: "Preview swarm allocation plan without executing",
		RunE: func(cmd *cobra.Command, args []string) error {
			return runSwarm(swarmOptions{
				ScanDir:    scanDir,
				Projects:   projects,
				DryRun:     true,
				JSONOutput: jsonOutput,
			})
		},
	}

	defaultScanDir := "/dp"
	if cfg != nil && cfg.Swarm.DefaultScanDir != "" {
		defaultScanDir = cfg.Swarm.DefaultScanDir
	}

	cmd.Flags().StringVar(&scanDir, "scan-dir", defaultScanDir, "Directory to scan for projects")
	cmd.Flags().StringSliceVar(&projects, "projects", nil, "Explicit list of project paths")

	return cmd
}

// Subcommand: swarm status
func newSwarmStatusCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "status",
		Short: "Show current swarm status",
		RunE: func(cmd *cobra.Command, args []string) error {
			// TODO: Implement swarm status
			output.PrintInfo("Swarm status not yet implemented")
			return nil
		},
	}
	return cmd
}

// Subcommand: swarm stop
func newSwarmStopCmd() *cobra.Command {
	var (
		force bool
	)

	cmd := &cobra.Command{
		Use:   "stop",
		Short: "Stop the swarm and destroy all sessions",
		RunE: func(cmd *cobra.Command, args []string) error {
			// TODO: Implement swarm stop
			output.PrintInfo("Swarm stop not yet implemented")
			return nil
		},
	}

	cmd.Flags().BoolVar(&force, "force", false, "Force stop without confirmation")

	return cmd
}
