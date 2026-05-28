package cli

import (
	"fmt"
	"io"
	"strconv"
	"strings"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

func newAdoptCmd() *cobra.Command {
	var (
		ccPanes   string
		codPanes  string
		gmiPanes  string
		userPanes string
		autoName  bool
		dryRun    bool
	)

	cmd := &cobra.Command{
		Use:   "adopt <session-name>",
		Short: "Adopt an external tmux session for NTM management",
		Long: `Adopt an existing tmux session that was created outside of NTM.

This command takes an externally-created tmux session and configures it
for use with NTM by setting appropriate pane titles and registering
agent types. After adoption, all NTM commands (send, status, list, etc.)
will work with the session.

Panes are specified by their pane index (0-based from tmux).
Use commas to specify multiple panes per agent type.

Examples:
  # Adopt session with panes 0-5 as Claude agents
  ntm adopt my_session --cc=0,1,2,3,4,5

  # Adopt with mixed agent types
  ntm adopt my_session --cc=0,1,2 --cod=3,4 --gmi=5

  # Preview what would be changed
  ntm adopt my_session --cc=0,1 --dry-run

  # Auto-rename panes based on agent type
  ntm adopt my_session --cc=0,1 --auto-name`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			sessionName := args[0]

			opts := AdoptOptions{
				Session:   sessionName,
				AutoName:  autoName,
				DryRun:    dryRun,
				CCPanes:   parsePaneList(ccPanes),
				CodPanes:  parsePaneList(codPanes),
				GmiPanes:  parsePaneList(gmiPanes),
				UserPanes: parsePaneList(userPanes),
			}

			return runAdopt(opts)
		},
	}

	cmd.Flags().StringVar(&ccPanes, "cc", "", "Comma-separated pane indices for Claude agents (e.g., 0,1,2)")
	cmd.Flags().StringVar(&codPanes, "cod", "", "Comma-separated pane indices for Codex agents (e.g., 3,4)")
	cmd.Flags().StringVar(&gmiPanes, "gmi", "", "Comma-separated pane indices for Gemini agents (e.g., 5)")
	cmd.Flags().StringVar(&userPanes, "user", "", "Comma-separated pane indices for user panes (e.g., 6)")
	cmd.Flags().BoolVar(&autoName, "auto-name", true, "Automatically rename panes to NTM convention")
	cmd.Flags().BoolVar(&dryRun, "dry-run", false, "Preview changes without applying them")

	return cmd
}

// AdoptOptions configures session adoption
type AdoptOptions struct {
	Session   string
	AutoName  bool
	DryRun    bool
	CCPanes   []int
	CodPanes  []int
	GmiPanes  []int
	UserPanes []int
}

// AdoptResult represents the result of an adopt operation
type AdoptResult struct {
	Success      bool               `json:"success"`
	Session      string             `json:"session"`
	AdoptedPanes []AdoptedPaneInfo  `json:"adopted_panes"`
	TotalPanes   int                `json:"total_panes"`
	Agents       AdoptedAgentCounts `json:"agents"`
	DryRun       bool               `json:"dry_run"`
	Error        string             `json:"error,omitempty"`
}

// AdoptedPaneInfo describes a pane that was adopted
type AdoptedPaneInfo struct {
	PaneID    string `json:"pane_id"`
	PaneIndex int    `json:"pane_index"`
	AgentType string `json:"agent_type"`
	OldTitle  string `json:"old_title,omitempty"`
	NewTitle  string `json:"new_title"`
	NTMIndex  int    `json:"ntm_index"`
}

// AdoptedAgentCounts tracks agent counts by type
type AdoptedAgentCounts struct {
	Claude int `json:"cc"`
	Codex  int `json:"cod"`
	Gemini int `json:"gmi"`
	User   int `json:"user"`
}

func (a AdoptedAgentCounts) Total() int {
	return a.Claude + a.Codex + a.Gemini + a.User
}

func (r *AdoptResult) Text(w io.Writer) error {
	t := theme.Current()

	if !r.Success {
		fmt.Fprintf(w, "%s✗%s Failed to adopt session: %s\n",
			colorize(t.Red), colorize(t.Text), r.Error)
		return nil
	}

	if r.DryRun {
		fmt.Fprintf(w, "%s[DRY RUN]%s Would adopt session '%s'\n",
			colorize(t.Warning), colorize(t.Text), r.Session)
	} else {
		fmt.Fprintf(w, "%s✓%s Adopted session '%s'\n",
			colorize(t.Success), colorize(t.Text), r.Session)
	}

	fmt.Fprintf(w, "  Total panes: %d\n", r.TotalPanes)
	fmt.Fprintf(w, "  Adopted: %d (cc:%d, cod:%d, gmi:%d, user:%d)\n",
		r.Agents.Total(), r.Agents.Claude, r.Agents.Codex, r.Agents.Gemini, r.Agents.User)

	if len(r.AdoptedPanes) > 0 {
		fmt.Fprintf(w, "\n%sPanes:%s\n", colorize(t.Blue), colorize(t.Text))
		for _, p := range r.AdoptedPanes {
			fmt.Fprintf(w, "  [%d] %s → %s\n", p.PaneIndex, p.OldTitle, p.NewTitle)
		}
	}

	if r.DryRun {
		fmt.Fprintf(w, "\n%sNote:%s Use without --dry-run to apply changes.\n",
			colorize(t.Warning), colorize(t.Text))
	}

	return nil
}

func (r *AdoptResult) JSON() interface{} {
	return r
}

func runAdopt(opts AdoptOptions) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	// Check session exists
	if !tmux.SessionExists(opts.Session) {
		result := &AdoptResult{
			Success: false,
			Session: opts.Session,
			Error:   fmt.Sprintf("session '%s' not found", opts.Session),
		}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}

	// Get existing panes
	panes, err := tmux.GetPanes(opts.Session)
	if err != nil {
		result := &AdoptResult{
			Success: false,
			Session: opts.Session,
			Error:   fmt.Sprintf("failed to get panes: %v", err),
		}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}

	// Build pane index lookup
	paneByIndex := make(map[int]*tmux.Pane)
	for i := range panes {
		paneByIndex[panes[i].Index] = &panes[i]
	}

	// Build adoption plan
	adoptedPanes := []AdoptedPaneInfo{}
	counts := AdoptedAgentCounts{}

	// Track NTM index per agent type
	ntmIndex := map[string]int{
		"cc":   1,
		"cod":  1,
		"gmi":  1,
		"user": 1,
	}

	// Helper to adopt panes for a type
	adoptType := func(paneIndices []int, agentType string, counter *int) error {
		for _, idx := range paneIndices {
			pane, ok := paneByIndex[idx]
			if !ok {
				return fmt.Errorf("pane index %d not found in session", idx)
			}

			newTitle := tmux.FormatPaneName(opts.Session, agentType, ntmIndex[agentType], "")
			info := AdoptedPaneInfo{
				PaneID:    pane.ID,
				PaneIndex: pane.Index,
				AgentType: agentType,
				OldTitle:  pane.Title,
				NewTitle:  newTitle,
				NTMIndex:  ntmIndex[agentType],
			}

			if opts.AutoName && !opts.DryRun {
				if err := tmux.SetPaneTitle(pane.ID, newTitle); err != nil {
					return fmt.Errorf("failed to set title for pane %d: %v", idx, err)
				}
			}

			adoptedPanes = append(adoptedPanes, info)
			ntmIndex[agentType]++
			*counter++
		}
		return nil
	}

	// Adopt each type
	if err := adoptType(opts.CCPanes, "cc", &counts.Claude); err != nil {
		result := &AdoptResult{Success: false, Session: opts.Session, Error: err.Error()}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}
	if err := adoptType(opts.CodPanes, "cod", &counts.Codex); err != nil {
		result := &AdoptResult{Success: false, Session: opts.Session, Error: err.Error()}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}
	if err := adoptType(opts.GmiPanes, "gmi", &counts.Gemini); err != nil {
		result := &AdoptResult{Success: false, Session: opts.Session, Error: err.Error()}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}
	if err := adoptType(opts.UserPanes, "user", &counts.User); err != nil {
		result := &AdoptResult{Success: false, Session: opts.Session, Error: err.Error()}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}

	// Check if any panes were specified
	if counts.Total() == 0 {
		result := &AdoptResult{
			Success: false,
			Session: opts.Session,
			Error:   "no panes specified for adoption; use --cc, --cod, --gmi, or --user flags",
		}
		return output.New(output.WithJSON(jsonOutput)).Output(result)
	}

	result := &AdoptResult{
		Success:      true,
		Session:      opts.Session,
		AdoptedPanes: adoptedPanes,
		TotalPanes:   len(panes),
		Agents:       counts,
		DryRun:       opts.DryRun,
	}

	return output.New(output.WithJSON(jsonOutput)).Output(result)
}

// parsePaneList parses a comma-separated list of pane indices
func parsePaneList(s string) []int {
	if s == "" {
		return nil
	}

	var result []int
	parts := strings.Split(s, ",")
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p == "" {
			continue
		}

		// Support ranges like "0-5"
		if strings.Contains(p, "-") {
			rangeParts := strings.Split(p, "-")
			if len(rangeParts) == 2 {
				start, err1 := strconv.Atoi(strings.TrimSpace(rangeParts[0]))
				end, err2 := strconv.Atoi(strings.TrimSpace(rangeParts[1]))
				if err1 == nil && err2 == nil && start <= end {
					for i := start; i <= end; i++ {
						result = append(result, i)
					}
					continue
				}
			}
		}

		// Single index
		if idx, err := strconv.Atoi(p); err == nil {
			result = append(result, idx)
		}
	}

	return result
}
