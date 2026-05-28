package cli

import (
	"fmt"
	"io"
	"os"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

func newViewCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:     "view [session-name]",
		Aliases: []string{"v", "tile"},
		Short:   "View all panes in a session (unzoom, tile, attach)",
		Long: `View all panes in a tmux session by:
1. Unzooming any zoomed panes
2. Applying tiled layout to all windows
3. Attaching/switching to the session

If no session is specified:
- If inside tmux, operates on the current session
- Otherwise, shows a session selector

Examples:
  ntm view myproject
  ntm view                 # Select session or use current
  ntm tile myproject       # Alias`,
		Args: cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			var session string
			if len(args) > 0 {
				session = args[0]
			}
			return runView(cmd.OutOrStdout(), session)
		},
	}

	cmd.ValidArgsFunction = completeSessionArgs

	return cmd
}

func runView(w io.Writer, session string) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	t := theme.Current()

	res, err := ResolveSession(session, w)
	if err != nil {
		return err
	}
	if res.Session == "" {
		return nil
	}
	res.ExplainIfInferred(os.Stderr)
	session = res.Session

	if !tmux.SessionExists(session) {
		cliErr := output.SessionNotFoundError(session)
		output.PrintCLIError(cliErr)
		return cliErr
	}

	// Apply tiled layout (includes unzoom)
	if err := tmux.ApplyTiledLayout(session); err != nil {
		return fmt.Errorf("failed to apply layout: %w", err)
	}

	fmt.Printf("%s✓%s Tiled layout applied to '%s'\n",
		colorize(t.Success), colorize(t.Text), session)

	// Attach or switch to session
	return tmux.AttachOrSwitch(session)
}
