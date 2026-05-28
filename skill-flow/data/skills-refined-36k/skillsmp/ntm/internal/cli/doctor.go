package cli

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/charmbracelet/lipgloss"
	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/invariants"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tools"
)

var (
	doctorVerbose bool
	doctorJSON    bool
)

func newDoctorCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "doctor",
		Short: "Validate the NTM ecosystem health",
		Long: `Validates that all ecosystem tools and dependencies are properly installed
and configured. Checks:

  - Tool detection (bv, bd, am, cm, cass, s2p)
  - Version compatibility
  - Daemon health and port availability
  - Configuration files

This command helps diagnose issues before spawning sessions.`,
		RunE: runDoctor,
	}

	cmd.Flags().BoolVarP(&doctorVerbose, "verbose", "v", false, "Show detailed output")
	cmd.Flags().BoolVar(&doctorJSON, "json", false, "Output as JSON")

	return cmd
}

// DoctorReport contains the full health check report
type DoctorReport struct {
	Timestamp     time.Time        `json:"timestamp"`
	Overall       string           `json:"overall"` // "healthy", "warning", "unhealthy"
	Tools         []ToolCheck      `json:"tools"`
	Dependencies  []DepCheck       `json:"dependencies"`
	Daemons       []DaemonCheck    `json:"daemons"`
	Configuration []ConfigCheck    `json:"configuration"`
	Invariants    []InvariantCheck `json:"invariants"`
	Warnings      int              `json:"warnings"`
	Errors        int              `json:"errors"`
}

// InvariantCheck represents a design invariant check result
type InvariantCheck struct {
	ID      string   `json:"id"`
	Name    string   `json:"name"`
	Status  string   `json:"status"` // "ok", "warning", "error"
	Message string   `json:"message,omitempty"`
	Details []string `json:"details,omitempty"`
}

// ToolCheck represents a tool health check result
type ToolCheck struct {
	Name         string   `json:"name"`
	Installed    bool     `json:"installed"`
	Version      string   `json:"version,omitempty"`
	Path         string   `json:"path,omitempty"`
	Capabilities []string `json:"capabilities,omitempty"`
	Required     bool     `json:"required"`
	Status       string   `json:"status"` // "ok", "warning", "error"
	Message      string   `json:"message,omitempty"`
}

// DepCheck represents a dependency check result
type DepCheck struct {
	Name       string `json:"name"`
	Installed  bool   `json:"installed"`
	Version    string `json:"version,omitempty"`
	MinVersion string `json:"min_version,omitempty"`
	Status     string `json:"status"`
	Message    string `json:"message,omitempty"`
}

// DaemonCheck represents a daemon health check result
type DaemonCheck struct {
	Name    string `json:"name"`
	Running bool   `json:"running"`
	Port    int    `json:"port,omitempty"`
	PID     int    `json:"pid,omitempty"`
	Status  string `json:"status"`
	Message string `json:"message,omitempty"`
}

// ConfigCheck represents a configuration check result
type ConfigCheck struct {
	Name    string `json:"name"`
	Valid   bool   `json:"valid"`
	Status  string `json:"status"`
	Message string `json:"message,omitempty"`
}

func runDoctor(cmd *cobra.Command, args []string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	report := performDoctorCheck(ctx)

	if doctorJSON {
		return outputDoctorJSON(report)
	}

	return renderDoctorTUI(report)
}

func performDoctorCheck(ctx context.Context) *DoctorReport {
	report := &DoctorReport{
		Timestamp: time.Now(),
		Overall:   "healthy",
	}

	// Check tools using the adapter framework
	report.Tools = checkTools(ctx)

	// Check dependencies (tmux, Go)
	report.Dependencies = checkDependencies(ctx)

	// Check daemons
	report.Daemons = checkDaemons(ctx)

	// Check configuration
	report.Configuration = checkConfiguration()

	// Check design invariants
	report.Invariants = checkInvariants(ctx)

	// Calculate overall status
	for _, t := range report.Tools {
		switch t.Status {
		case "error":
			report.Errors++
		case "warning":
			report.Warnings++
		}
	}
	for _, d := range report.Dependencies {
		switch d.Status {
		case "error":
			report.Errors++
		case "warning":
			report.Warnings++
		}
	}
	for _, d := range report.Daemons {
		switch d.Status {
		case "error":
			report.Errors++
		case "warning":
			report.Warnings++
		}
	}
	for _, c := range report.Configuration {
		switch c.Status {
		case "error":
			report.Errors++
		case "warning":
			report.Warnings++
		}
	}
	for _, i := range report.Invariants {
		switch i.Status {
		case "error":
			report.Errors++
		case "warning":
			report.Warnings++
		}
	}

	if report.Errors > 0 {
		report.Overall = "unhealthy"
	} else if report.Warnings > 0 {
		report.Overall = "warning"
	}

	return report
}

func checkTools(ctx context.Context) []ToolCheck {
	var checks []ToolCheck

	// Required tools
	requiredTools := map[tools.ToolName]bool{
		tools.ToolBV: true, // Required for priority/insights
		tools.ToolBD: true, // Required for beads tracking
	}

	// Optional tools
	optionalTools := []tools.ToolName{
		tools.ToolAM,
		tools.ToolCM,
		tools.ToolCASS,
		tools.ToolS2P,
	}

	// Check each registered tool
	for _, toolName := range tools.AllTools() {
		adapter, ok := tools.Get(toolName)
		if !ok {
			continue
		}

		check := ToolCheck{
			Name:     string(toolName),
			Required: requiredTools[toolName],
		}

		path, installed := adapter.Detect()
		check.Installed = installed
		check.Path = path

		if installed {
			// Get version
			if version, err := adapter.Version(ctx); err == nil {
				check.Version = version.String()
			}

			// Get capabilities
			if caps, err := adapter.Capabilities(ctx); err == nil {
				for _, c := range caps {
					check.Capabilities = append(check.Capabilities, string(c))
				}
			}

			// Health check
			if health, err := adapter.Health(ctx); err == nil && health.Healthy {
				check.Status = "ok"
				check.Message = check.Version
			} else {
				check.Status = "warning"
				check.Message = "health check failed"
			}
		} else {
			if check.Required {
				check.Status = "error"
				check.Message = "required tool not found"
			} else {
				check.Status = "warning"
				check.Message = "optional tool not found"
			}
		}

		checks = append(checks, check)
	}

	// Add any optional tools not in registry
	for _, name := range optionalTools {
		found := false
		for _, c := range checks {
			if c.Name == string(name) {
				found = true
				break
			}
		}
		if !found {
			checks = append(checks, ToolCheck{
				Name:     string(name),
				Required: false,
				Status:   "warning",
				Message:  "adapter not registered",
			})
		}
	}

	return checks
}

func checkDependencies(ctx context.Context) []DepCheck {
	var checks []DepCheck

	// Check tmux
	tmuxCheck := DepCheck{
		Name:       "tmux",
		MinVersion: "3.0",
	}
	if tmux.DefaultClient.IsInstalled() {
		path := tmux.BinaryPath()
		tmuxCheck.Installed = true
		cmd := exec.CommandContext(ctx, path, "-V")
		if out, err := cmd.Output(); err == nil {
			tmuxCheck.Version = strings.TrimSpace(string(out))
		}
		tmuxCheck.Status = "ok"
	} else {
		tmuxCheck.Status = "error"
		tmuxCheck.Message = "tmux is required for NTM"
	}
	checks = append(checks, tmuxCheck)

	// Check Go version (for building)
	goCheck := DepCheck{
		Name:       "go",
		MinVersion: "1.25",
	}
	goCheck.Version = runtime.Version()
	goCheck.Installed = true
	goCheck.Status = "ok"
	checks = append(checks, goCheck)

	return checks
}

func checkDaemons(ctx context.Context) []DaemonCheck {
	var checks []DaemonCheck

	// Check common daemon ports in deterministic order
	type daemonPort struct {
		name string
		port int
	}
	daemons := []daemonPort{
		{"agent-mail", 8765},
		{"cm-server", 8766},
		{"bd-daemon", 8767},
	}

	dialer := &net.Dialer{Timeout: time.Second}

	for _, dp := range daemons {
		check := DaemonCheck{
			Name: dp.name,
			Port: dp.port,
		}

		// Check if port is in use (use context for cancellation)
		conn, err := dialer.DialContext(ctx, "tcp", fmt.Sprintf("127.0.0.1:%d", dp.port))
		if err == nil {
			conn.Close()
			check.Running = true
			check.Status = "ok"
			check.Message = fmt.Sprintf("listening on port %d", dp.port)
		} else {
			check.Running = false
			check.Status = "ok"
			check.Message = fmt.Sprintf("port %d available", dp.port)
		}

		checks = append(checks, check)
	}

	return checks
}

func checkConfiguration() []ConfigCheck {
	var checks []ConfigCheck

	// Check .ntm directory
	homeDir, err := os.UserHomeDir()
	if err != nil {
		checks = append(checks, ConfigCheck{
			Name:    ".ntm directory",
			Status:  "error",
			Message: "cannot determine home directory",
		})
	} else {
		ntmDir := filepath.Join(homeDir, ".ntm")
		if info, err := os.Stat(ntmDir); err == nil && info.IsDir() {
			// Check if writable
			testFile := filepath.Join(ntmDir, ".doctor_test")
			if f, err := os.Create(testFile); err == nil {
				f.Close()
				os.Remove(testFile)
				checks = append(checks, ConfigCheck{
					Name:    ".ntm directory",
					Valid:   true,
					Status:  "ok",
					Message: "exists and writable",
				})
			} else {
				checks = append(checks, ConfigCheck{
					Name:    ".ntm directory",
					Valid:   false,
					Status:  "error",
					Message: "not writable",
				})
			}
		} else {
			checks = append(checks, ConfigCheck{
				Name:    ".ntm directory",
				Valid:   false,
				Status:  "warning",
				Message: "does not exist (will be created)",
			})
		}
	}

	// Check for .beads directory in current directory
	if _, err := os.Stat(".beads"); err == nil {
		checks = append(checks, ConfigCheck{
			Name:    ".beads directory",
			Valid:   true,
			Status:  "ok",
			Message: "project has beads initialized",
		})
	} else {
		checks = append(checks, ConfigCheck{
			Name:    ".beads directory",
			Valid:   false,
			Status:  "warning",
			Message: "no beads in current directory",
		})
	}

	return checks
}

func checkInvariants(ctx context.Context) []InvariantCheck {
	var checks []InvariantCheck

	// Get current working directory for the checker
	cwd, err := os.Getwd()
	if err != nil {
		cwd = "."
	}

	checker := invariants.NewChecker(cwd)
	report := checker.CheckAll(ctx)

	// Convert invariant results to InvariantCheck format
	defs := invariants.Definitions()
	for _, id := range invariants.AllInvariants() {
		result, ok := report.Results[id]
		if !ok {
			continue
		}

		def := defs[id]
		checks = append(checks, InvariantCheck{
			ID:      string(id),
			Name:    def.Name,
			Status:  result.Status,
			Message: result.Message,
			Details: result.Details,
		})
	}

	return checks
}

func outputDoctorJSON(report *DoctorReport) error {
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	return encoder.Encode(report)
}

func renderDoctorTUI(report *DoctorReport) error {
	// Define styles
	titleStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("99"))

	sectionStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("75")).
		MarginTop(1)

	okStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("42"))     // Green
	warnStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("214"))  // Orange
	errorStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("196")) // Red
	mutedStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("240")) // Gray

	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("240")).
		Padding(0, 1).
		MarginTop(1)

	// Status icon helper
	statusIcon := func(s string) string {
		switch s {
		case "ok":
			return okStyle.Render("✓")
		case "warning":
			return warnStyle.Render("⚠")
		case "error":
			return errorStyle.Render("✗")
		default:
			return mutedStyle.Render("?")
		}
	}

	// Title
	fmt.Println()
	fmt.Println(titleStyle.Render("NTM Doctor"))
	fmt.Println()

	// Tools section
	fmt.Println(sectionStyle.Render("Tools:"))
	for _, t := range report.Tools {
		icon := statusIcon(t.Status)
		if t.Installed {
			caps := ""
			if len(t.Capabilities) > 0 && doctorVerbose {
				caps = fmt.Sprintf(" (%v)", t.Capabilities)
			}
			fmt.Printf("  %s %s %s%s\n", icon, t.Name, mutedStyle.Render(t.Message), caps)
		} else {
			msg := t.Message
			if t.Required {
				msg = errorStyle.Render(msg)
			} else {
				msg = mutedStyle.Render(msg)
			}
			fmt.Printf("  %s %s %s\n", icon, t.Name, msg)
		}
	}

	// Dependencies section
	fmt.Println(sectionStyle.Render("Dependencies:"))
	for _, d := range report.Dependencies {
		icon := statusIcon(d.Status)
		version := ""
		if d.Version != "" {
			version = mutedStyle.Render(fmt.Sprintf(" (%s)", d.Version))
		}
		fmt.Printf("  %s %s%s\n", icon, d.Name, version)
	}

	// Daemons section
	fmt.Println(sectionStyle.Render("Daemons:"))
	for _, d := range report.Daemons {
		icon := statusIcon(d.Status)
		fmt.Printf("  %s %s %s\n", icon, d.Name, mutedStyle.Render(d.Message))
	}

	// Configuration section
	fmt.Println(sectionStyle.Render("Configuration:"))
	for _, c := range report.Configuration {
		icon := statusIcon(c.Status)
		fmt.Printf("  %s %s %s\n", icon, c.Name, mutedStyle.Render(c.Message))
	}

	// Invariants section
	fmt.Println(sectionStyle.Render("Design Invariants:"))
	for _, i := range report.Invariants {
		icon := statusIcon(i.Status)
		fmt.Printf("  %s %s %s\n", icon, i.Name, mutedStyle.Render(i.Message))
		if doctorVerbose && len(i.Details) > 0 {
			for _, detail := range i.Details {
				fmt.Printf("      %s\n", mutedStyle.Render(detail))
			}
		}
	}

	// Overall status box
	var statusMsg string
	var statusStyle lipgloss.Style
	switch report.Overall {
	case "healthy":
		statusMsg = "Overall: HEALTHY"
		statusStyle = okStyle
	case "warning":
		statusMsg = fmt.Sprintf("Overall: HEALTHY (%d warnings)", report.Warnings)
		statusStyle = warnStyle
	case "unhealthy":
		statusMsg = fmt.Sprintf("Overall: UNHEALTHY (%d errors, %d warnings)", report.Errors, report.Warnings)
		statusStyle = errorStyle
	}
	fmt.Println(boxStyle.Render(statusStyle.Render(statusMsg)))
	fmt.Println()

	// Return error to indicate non-healthy status (Cobra will set appropriate exit code)
	if report.Overall == "unhealthy" {
		return errors.New("ecosystem is unhealthy")
	} else if report.Overall == "warning" {
		// Warnings are informational, don't fail
		return nil
	}

	return nil
}
