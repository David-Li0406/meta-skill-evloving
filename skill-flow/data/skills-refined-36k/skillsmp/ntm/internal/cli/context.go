package cli

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"

	ntmctx "github.com/Dicklesworthstone/ntm/internal/context"
	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/state"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

func newContextCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "context",
		Short: "Manage context packs for agent tasks",
	}

	cmd.AddCommand(
		newContextBuildCmd(),
		newContextShowCmd(),
		newContextStatsCmd(),
		newContextClearCmd(),
	)

	return cmd
}

func newContextBuildCmd() *cobra.Command {
	var (
		beadID    string
		agentType string
		task      string
		files     []string
	)

	cmd := &cobra.Command{
		Use:   "build",
		Short: "Build a context pack for a task",
		Long: `Build a context pack containing:
- BV triage data (priority and planning)
- CM rules (learned guidelines)
- CASS history (prior solutions)
- S2P file context

The context is rendered in agent-appropriate format:
- Claude (cc): XML format
- Codex (cod), Gemini (gmi): Markdown format`,
		RunE: func(cmd *cobra.Command, args []string) error {
			dir, _ := os.Getwd()

			// Get repo revision
			repoRev := getRepoRev(dir)

			// Get session info
			session := tmux.GetCurrentSession()
			if session == "" {
				session = filepath.Base(dir)
			}

			// Open state store
			store, err := state.Open("")
			if err != nil {
				return fmt.Errorf("open state store: %w", err)
			}
			defer store.Close()

			if err := store.Migrate(); err != nil {
				return fmt.Errorf("migrate state store: %w", err)
			}

			// Build context pack
			builder := ntmctx.NewContextPackBuilder(store)

			opts := ntmctx.BuildOptions{
				BeadID:     beadID,
				AgentType:  agentType,
				RepoRev:    repoRev,
				Task:       task,
				Files:      files,
				ProjectDir: dir,
				SessionID:  session,
			}

			pack, err := builder.Build(cmd.Context(), opts)
			if err != nil {
				return err
			}

			if IsJSONOutput() {
				return output.PrintJSON(pack)
			}

			// Print summary
			fmt.Printf("Context Pack: %s\n", pack.ID)
			fmt.Printf("Agent Type:   %s\n", pack.AgentType)
			fmt.Printf("Token Count:  %d\n", pack.TokenCount)
			fmt.Println()

			for name, comp := range pack.Components {
				status := "✓"
				if comp.Error != "" {
					status = "✗ " + comp.Error
				}
				fmt.Printf("  %s: %s (%d tokens)\n", name, status, comp.TokenCount)
			}
			fmt.Println()

			// Print rendered prompt if verbose
			verbose, _ := cmd.Flags().GetBool("verbose")
			if verbose {
				fmt.Println("--- Rendered Prompt ---")
				fmt.Println(pack.RenderedPrompt)
			}

			return nil
		},
	}

	cmd.Flags().StringVar(&beadID, "bead", "", "Bead ID for context")
	cmd.Flags().StringVar(&agentType, "agent", "cc", "Agent type (cc, cod, gmi)")
	cmd.Flags().StringVar(&task, "task", "", "Task description for CM context")
	cmd.Flags().StringSliceVar(&files, "files", nil, "Files to include in S2P context")
	cmd.Flags().Bool("verbose", false, "Show full rendered prompt")

	return cmd
}

func newContextShowCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "show <pack-id>",
		Short: "Show a stored context pack",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			packID := args[0]

			store, err := state.Open("")
			if err != nil {
				return fmt.Errorf("open state store: %w", err)
			}
			defer store.Close()

			pack, err := store.GetContextPack(packID)
			if err != nil {
				return fmt.Errorf("get context pack: %w", err)
			}

			if pack == nil {
				return fmt.Errorf("context pack not found: %s", packID)
			}

			if IsJSONOutput() {
				return output.PrintJSON(pack)
			}

			fmt.Printf("ID:           %s\n", pack.ID)
			fmt.Printf("Bead ID:      %s\n", pack.BeadID)
			fmt.Printf("Agent Type:   %s\n", pack.AgentType)
			fmt.Printf("Repo Rev:     %s\n", pack.RepoRev)
			fmt.Printf("Created:      %s\n", pack.CreatedAt.Format("2006-01-02 15:04:05"))
			fmt.Printf("Token Count:  %d\n", pack.TokenCount)

			if pack.RenderedPrompt != "" {
				fmt.Println()
				fmt.Println("--- Rendered Prompt ---")
				fmt.Println(pack.RenderedPrompt)
			}

			return nil
		},
	}
}

func newContextStatsCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "stats",
		Short: "Show context pack cache statistics",
		RunE: func(cmd *cobra.Command, args []string) error {
			// Create builder to check cache stats
			builder := ntmctx.NewContextPackBuilder(nil)
			size, keys := builder.CacheStats()

			if IsJSONOutput() {
				return output.PrintJSON(map[string]interface{}{
					"cache_size": size,
					"cache_keys": keys,
				})
			}

			fmt.Printf("Cache Size: %d entries\n", size)
			if size > 0 {
				fmt.Println("Cache Keys:")
				for _, k := range keys {
					fmt.Printf("  - %s\n", k)
				}
			}

			return nil
		},
	}
}

func newContextClearCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "clear",
		Short: "Clear the context pack cache",
		RunE: func(cmd *cobra.Command, args []string) error {
			builder := ntmctx.NewContextPackBuilder(nil)
			builder.ClearCache()

			fmt.Println("Context pack cache cleared.")
			return nil
		},
	}
}

// getRepoRev returns the current git HEAD revision
func getRepoRev(dir string) string {
	// Try to get git HEAD
	headPath := filepath.Join(dir, ".git", "HEAD")
	data, err := os.ReadFile(headPath)
	if err != nil {
		return "unknown"
	}

	head := strings.TrimSpace(string(data))
	if strings.HasPrefix(head, "ref: ") {
		// Symbolic ref - read the actual ref
		refPath := filepath.Join(dir, ".git", head[5:])
		refData, err := os.ReadFile(refPath)
		if err == nil {
			rev := strings.TrimSpace(string(refData))
			if len(rev) > 40 {
				rev = rev[:40]
			}
			return rev
		}
	}

	// Direct SHA
	if len(head) >= 40 {
		return head[:40]
	}

	return "unknown"
}
