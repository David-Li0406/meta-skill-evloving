package cli

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/hooks"
	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

func newCreateCmd() *cobra.Command {
	var panes int

	cmd := &cobra.Command{
		Use:   "create <session-name>",
		Short: "Create a new tmux session with multiple panes",
		Long: `Create a new tmux session with the specified number of panes.
The session directory is created under PROJECTS_BASE if it doesn't exist.

Example:
  ntm create myproject           # Create with default panes
  ntm create myproject --panes=6 # Create with 6 panes`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCreate(args[0], panes)
		},
	}

	cmd.Flags().IntVarP(&panes, "panes", "p", 0, "number of panes to create (default from config)")

	return cmd
}

func runCreate(session string, panes int) error {
	if err := tmux.EnsureInstalled(); err != nil {
		if IsJSONOutput() {
			return output.PrintJSON(output.NewError(err.Error()))
		}
		return err
	}

	if err := tmux.ValidateSessionName(session); err != nil {
		if IsJSONOutput() {
			return output.PrintJSON(output.NewError(err.Error()))
		}
		return err
	}

	// Get pane count from config if not specified
	if panes <= 0 {
		panes = cfg.Tmux.DefaultPanes
	}

	dir := cfg.GetProjectDir(session)

	// Initialize hook executor
	hookExec, err := hooks.NewExecutorFromConfig()
	if err != nil {
		if !IsJSONOutput() {
			fmt.Printf("⚠ Warning: could not load hooks config: %v\n", err)
		}
		hookExec = hooks.NewExecutor(nil)
	}

	ctx := context.Background()
	hookCtx := hooks.ExecutionContext{
		SessionName: session,
		ProjectDir:  dir,
	}

	// Run pre-create hooks
	if hookExec.HasHooksForEvent(hooks.EventPreCreate) {
		if !IsJSONOutput() {
			fmt.Println("Running pre-create hooks...")
		}
		results, err := hookExec.RunHooksForEvent(ctx, hooks.EventPreCreate, hookCtx)
		if err != nil {
			if IsJSONOutput() {
				return output.PrintJSON(output.NewError(fmt.Sprintf("pre-create hooks failed: %v", err)))
			}
			return fmt.Errorf("pre-create hooks failed: %w", err)
		}
		if hooks.AnyFailed(results) {
			if IsJSONOutput() {
				return output.PrintJSON(output.NewError(hooks.AllErrors(results).Error()))
			}
			return hooks.AllErrors(results)
		}
	}

	// Check if directory exists
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		if IsJSONOutput() {
			// In JSON mode, auto-create directory without prompting
			if err := os.MkdirAll(dir, 0755); err != nil {
				return output.PrintJSON(output.NewError(fmt.Sprintf("creating directory: %v", err)))
			}
		} else {
			fmt.Printf("Directory not found: %s\n", dir)
			if !confirm("Create it?") {
				fmt.Println("Aborted.")
				return nil
			}
			if err := os.MkdirAll(dir, 0755); err != nil {
				return fmt.Errorf("creating directory: %w", err)
			}
			fmt.Printf("Created %s\n", dir)
		}
	}

	// Check if session already exists
	if tmux.SessionExists(session) {
		if IsJSONOutput() {
			// Return info about existing session
			existingPanes, _ := tmux.GetPanes(session)
			paneResponses := make([]output.PaneResponse, len(existingPanes))
			for i, p := range existingPanes {
				paneResponses[i] = output.PaneResponse{
					Index:   p.Index,
					Title:   p.Title,
					Type:    agentTypeToString(p.Type),
					Variant: p.Variant,
					Active:  p.Active,
					Width:   p.Width,
					Height:  p.Height,
					Command: p.Command,
				}
			}
			return output.PrintJSON(output.CreateResponse{
				TimestampedResponse: output.NewTimestamped(),
				Session:             session,
				Created:             false,
				AlreadyExisted:      true,
				WorkingDirectory:    dir,
				PaneCount:           len(existingPanes),
				Panes:               paneResponses,
			})
		}
		fmt.Printf("Session '%s' already exists\n", session)
		return tmux.AttachOrSwitch(session)
	}

	if !IsJSONOutput() {
		fmt.Printf("Creating session '%s' with %d pane(s)...\n", session, panes)
	}

	// Create the session
	if err := tmux.CreateSession(session, dir); err != nil {
		if IsJSONOutput() {
			return output.PrintJSON(output.NewError(fmt.Sprintf("creating session: %v", err)))
		}
		return fmt.Errorf("creating session: %w", err)
	}

	// Add additional panes
	if panes > 1 {
		for i := 1; i < panes; i++ {
			if _, err := tmux.SplitWindow(session, dir); err != nil {
				if IsJSONOutput() {
					return output.PrintJSON(output.NewError(fmt.Sprintf("creating pane %d: %v", i+1, err)))
				}
				return fmt.Errorf("creating pane %d: %w", i+1, err)
			}
		}
	}

	// Run post-create hooks
	if hookExec.HasHooksForEvent(hooks.EventPostCreate) {
		if !IsJSONOutput() {
			fmt.Println("Running post-create hooks...")
		}
		_, _ = hookExec.RunHooksForEvent(ctx, hooks.EventPostCreate, hookCtx)
	}

	// JSON output mode: return structured response
	if IsJSONOutput() {
		finalPanes, _ := tmux.GetPanes(session)
		paneResponses := make([]output.PaneResponse, len(finalPanes))
		for i, p := range finalPanes {
			paneResponses[i] = output.PaneResponse{
				Index:   p.Index,
				Title:   p.Title,
				Type:    agentTypeToString(p.Type),
				Variant: p.Variant,
				Active:  p.Active,
				Width:   p.Width,
				Height:  p.Height,
				Command: p.Command,
			}
		}
		return output.PrintJSON(output.CreateResponse{
			TimestampedResponse: output.NewTimestamped(),
			Session:             session,
			Created:             true,
			WorkingDirectory:    dir,
			PaneCount:           len(finalPanes),
			Panes:               paneResponses,
		})
	}

	fmt.Printf("Created session '%s' with %d pane(s)\n", session, panes)
	return tmux.AttachOrSwitch(session)
}

// confirm prompts the user for y/n confirmation
func confirm(prompt string) bool {
	reader := bufio.NewReader(os.Stdin)
	fmt.Printf("%s [y/N]: ", prompt)
	answer, _ := reader.ReadString('\n')
	answer = strings.TrimSpace(strings.ToLower(answer))
	return answer == "y" || answer == "yes"
}

// agentTypeToString converts a tmux.AgentType to a string for JSON output
func agentTypeToString(t tmux.AgentType) string {
	switch t {
	case tmux.AgentClaude:
		return "claude"
	case tmux.AgentCodex:
		return "codex"
	case tmux.AgentGemini:
		return "gemini"
	default:
		return "user"
	}
}
