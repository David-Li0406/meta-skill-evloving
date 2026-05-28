package cli

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/agentmail"
	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/tools"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

func newDepsCmd() *cobra.Command {
	var verbose bool

	cmd := &cobra.Command{
		Use:     "deps",
		Aliases: []string{"check"},
		Short:   "Check for required dependencies and agent CLIs",
		Long: `Check that all required tools and AI agent CLIs are installed:

Required:
  - tmux (terminal multiplexer)

Optional agents:
  - claude (Claude Code CLI)
  - codex (OpenAI Codex CLI)
  - gemini (Google Gemini CLI)

Also checks for recommended tools like fzf.

Examples:
  ntm deps           # Quick check
  ntm deps -v        # Verbose output with versions
  ntm deps --json    # JSON output for scripts`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDeps(verbose)
		},
	}

	cmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "Show detailed version info")

	return cmd
}

type depCheck struct {
	Name        string
	Command     string
	VersionArgs []string
	Required    bool
	Category    string
	InstallHint string
}

func runDeps(verbose bool) error {
	deps := []depCheck{
		// Required
		{
			Name:        "tmux",
			Command:     "tmux",
			VersionArgs: []string{"-V"},
			Required:    true,
			Category:    "Required",
			InstallHint: "brew install tmux (macOS) / apt install tmux (Linux)",
		},

		// Agents
		{
			Name:        "Claude Code",
			Command:     "claude",
			VersionArgs: []string{"--version"},
			Required:    false,
			Category:    "AI Agents",
			InstallHint: "npm install -g @anthropic-ai/claude-code",
		},
		{
			Name:        "OpenAI Codex",
			Command:     "codex",
			VersionArgs: []string{"--version"},
			Required:    false,
			Category:    "AI Agents",
			InstallHint: "npm install -g @openai/codex",
		},
		{
			Name:        "Gemini CLI",
			Command:     "gemini",
			VersionArgs: []string{"--version"},
			Required:    false,
			Category:    "AI Agents",
			InstallHint: "npm install -g @google/gemini-cli",
		},

		// Recommended
		{
			Name:        "fzf",
			Command:     "fzf",
			VersionArgs: []string{"--version"},
			Required:    false,
			Category:    "Recommended",
			InstallHint: "brew install fzf (macOS) / apt install fzf (Linux)",
		},
		{
			Name:        "git",
			Command:     "git",
			VersionArgs: []string{"--version"},
			Required:    false,
			Category:    "Recommended",
			InstallHint: "brew install git (macOS) / apt install git (Linux)",
		},
	}

	// Collect all dependency statuses
	var depResults []output.DependencyCheck
	missingRequired := false
	agentsAvailable := 0

	for _, dep := range deps {
		status, version, path := checkDepWithPath(dep)
		installed := status == "found"

		if !installed && dep.Required {
			missingRequired = true
		}
		if installed && dep.Category == "AI Agents" {
			agentsAvailable++
		}

		depResults = append(depResults, output.DependencyCheck{
			Name:      dep.Name,
			Required:  dep.Required,
			Installed: installed,
			Version:   version,
			Path:      path,
		})
	}

	// Add Agent Mail as a service check
	client := newAgentMailClient("")
	agentMailAvailable := client.IsAvailable()
	depResults = append(depResults, output.DependencyCheck{
		Name:      "Agent Mail",
		Required:  false,
		Installed: agentMailAvailable,
		Path:      agentmail.DefaultBaseURL,
	})

	// JSON output mode
	if IsJSONOutput() {
		response := output.DepsResponse{
			TimestampedResponse: output.NewTimestamped(),
			AllInstalled:        !missingRequired,
			Dependencies:        depResults,
		}
		return output.PrintJSON(response)
	}

	// Text output mode
	t := theme.Current()

	// Group by category
	categories := []string{"Required", "AI Agents", "Recommended"}
	byCategory := make(map[string][]depCheck)
	for _, d := range deps {
		byCategory[d.Category] = append(byCategory[d.Category], d)
	}

	fmt.Println()
	fmt.Printf("%s NTM Dependency Check%s\n", "\033[1m", "\033[0m")
	fmt.Printf("%s═══════════════════════════════════════════════════%s\n\n", "\033[2m", "\033[0m")

	for _, cat := range categories {
		items := byCategory[cat]
		if len(items) == 0 {
			continue
		}

		fmt.Printf("%s%s:%s\n\n", "\033[1m", cat, "\033[0m")

		for _, dep := range items {
			status, version, _ := checkDepWithPath(dep)

			var statusIcon, statusColor string
			switch status {
			case "found":
				statusIcon = "✓"
				statusColor = colorize(t.Success)
			case "not found":
				statusIcon = "✗"
				if dep.Required {
					statusColor = colorize(t.Error)
				} else {
					statusColor = colorize(t.Warning)
				}
			case "error":
				statusIcon = "?"
				statusColor = colorize(t.Overlay)
			}

			fmt.Printf("  %s%s%s %-15s", statusColor, statusIcon, "\033[0m", dep.Name)

			if verbose && version != "" {
				// Clean up version output
				version = strings.TrimSpace(version)
				if len(version) > 40 {
					version = version[:40] + "..."
				}
				fmt.Printf(" %s%s%s", "\033[2m", version, "\033[0m")
			}

			fmt.Println()

			if status == "not found" && verbose {
				fmt.Printf("      %sInstall: %s%s\n", "\033[2m", dep.InstallHint, "\033[0m")
			}
		}

		fmt.Println()
	}

	// Services section
	fmt.Printf("%sServices:%s\n\n", "\033[1m", "\033[0m")
	checkAgentMail(t, verbose)
	fmt.Println()

	// Flywheel Tools section
	fmt.Printf("%sFlywheel Tools:%s\n\n", "\033[1m", "\033[0m")
	flywheelCount := checkFlywheelTools(t, verbose)
	fmt.Println()

	// Summary
	fmt.Printf("%s───────────────────────────────────────────────────%s\n", "\033[2m", "\033[0m")

	if missingRequired {
		fmt.Printf("%s✗%s Missing required dependencies!\n", colorize(t.Error), "\033[0m")
		os.Exit(1)
	} else if agentsAvailable == 0 {
		fmt.Printf("%s⚠%s No AI agents installed. Install at least one to use ntm spawn.\n",
			colorize(t.Warning), "\033[0m")
	} else {
		fmt.Printf("%s✓%s All required dependencies installed. %d agent(s), %d flywheel tool(s) available.\n",
			colorize(t.Success), "\033[0m", agentsAvailable, flywheelCount)
	}

	fmt.Println()
	return nil
}

// checkAgentMail checks Agent Mail server availability
func checkAgentMail(t theme.Theme, verbose bool) {
	client := newAgentMailClient("")

	if client.IsAvailable() {
		fmt.Printf("  %s✓%s %-15s", colorize(t.Success), "\033[0m", "Agent Mail")
		if verbose {
			fmt.Printf(" %srunning (%s)%s", "\033[2m", agentmail.DefaultBaseURL, "\033[0m")
		}
		fmt.Println()
	} else {
		fmt.Printf("  %s○%s %-15s", colorize(t.Overlay), "\033[0m", "Agent Mail")
		if verbose {
			fmt.Printf(" %snot detected (optional)%s", "\033[2m", "\033[0m")
		}
		fmt.Println()
	}
}

// checkFlywheelTools checks and displays flywheel ecosystem tools (bv, bd, caam, etc.)
func checkFlywheelTools(t theme.Theme, verbose bool) int {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	allInfo := tools.GetAllInfo(ctx)
	installedCount := 0

	// Key flywheel tools to display (in priority order)
	keyTools := []tools.ToolName{
		tools.ToolBV,   // Required for triage
		tools.ToolBD,   // Beads issue tracker
		tools.ToolCAAM, // Multi-account management
		tools.ToolCaut, // Quota monitoring
		tools.ToolDCG,  // Destructive command guard
		tools.ToolUBS,  // Bug scanner
		tools.ToolCASS, // Cross-agent search
		tools.ToolCM,   // CASS memory
	}

	// Build a map for quick lookup
	infoMap := make(map[tools.ToolName]*tools.ToolInfo)
	for _, info := range allInfo {
		if info != nil {
			infoMap[info.Name] = info
		}
	}

	for _, toolName := range keyTools {
		info, exists := infoMap[toolName]
		if !exists {
			// Tool not in registry, show as unavailable
			fmt.Printf("  %s○%s %-15s", colorize(t.Overlay), "\033[0m", string(toolName))
			if verbose {
				fmt.Printf(" %snot in registry%s", "\033[2m", "\033[0m")
			}
			fmt.Println()
			continue
		}

		var statusIcon, statusColor string
		if info.Installed {
			installedCount++
			if info.Health.Healthy {
				statusIcon = "✓"
				statusColor = colorize(t.Success)
			} else {
				statusIcon = "⚠"
				statusColor = colorize(t.Warning)
			}
		} else {
			statusIcon = "○"
			statusColor = colorize(t.Overlay)
		}

		// Format tool name with required indicator
		displayName := string(info.Name)
		if toolName == tools.ToolBV {
			displayName += " *" // Mark BV as required
		}

		fmt.Printf("  %s%s%s %-15s", statusColor, statusIcon, "\033[0m", displayName)

		if verbose && info.Installed {
			versionStr := info.Version.String()
			if versionStr == "" {
				versionStr = "installed"
			}
			if len(versionStr) > 30 {
				versionStr = versionStr[:30] + "..."
			}
			fmt.Printf(" %s%s%s", "\033[2m", versionStr, "\033[0m")

			// Show health status for unhealthy tools
			if !info.Health.Healthy && info.Health.Message != "" {
				fmt.Printf(" %s(%s)%s", "\033[33m", info.Health.Message, "\033[0m")
			}
		}

		fmt.Println()
	}

	return installedCount
}

// checkDepWithPath checks if a dependency is installed and returns its status, version, and path
func checkDepWithPath(dep depCheck) (status string, version string, path string) {
	// Check if command exists
	foundPath, err := exec.LookPath(dep.Command)
	if err != nil {
		return "not found", "", ""
	}

	path = foundPath

	// Get version if possible
	if len(dep.VersionArgs) > 0 {
		cmd := exec.Command(dep.Command, dep.VersionArgs...)
		out, err := cmd.CombinedOutput()
		if err != nil {
			return "found", "", path
		}
		return "found", strings.TrimSpace(string(out)), path
	}

	return "found", "", path
}
