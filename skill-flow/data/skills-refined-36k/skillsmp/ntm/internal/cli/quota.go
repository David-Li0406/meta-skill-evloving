package cli

import (
	"context"
	"fmt"
	"os"
	"text/tabwriter"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/quota"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

func newQuotaCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "quota [session]",
		Short: "Check agent quota usage",
		Long: `Query agents for their current quota usage.
Sends /usage command to supported agents (Claude) and parses the output.

Examples:
  ntm quota myproject
  ntm quota --json`,
		Args: cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			var session string
			if len(args) > 0 {
				session = args[0]
			}

			res, err := ResolveSession(session, cmd.OutOrStdout())
			if err != nil {
				return err
			}
			if res.Session == "" {
				return nil
			}
			res.ExplainIfInferred(os.Stderr)

			session = res.Session
			return runQuota(session)
		},
	}
}

func runQuota(session string) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	panes, err := tmux.GetPanes(session)
	if err != nil {
		return err
	}

	fetcher := &quota.PTYFetcher{
		CommandTimeout: 5 * time.Second,
	}

	var results []*quota.QuotaInfo
	ctx := context.Background()

	if !IsJSONOutput() {
		fmt.Printf("Querying quota for session '%s'...\n", session)
	}

	for _, p := range panes {
		var provider quota.Provider
		switch p.Type {
		case tmux.AgentClaude:
			provider = quota.ProviderClaude
		case tmux.AgentCodex:
			provider = quota.ProviderCodex
		case tmux.AgentGemini:
			provider = quota.ProviderGemini
		default:
			continue // Skip user/unknown panes
		}

		if !IsJSONOutput() {
			fmt.Printf("  Checking pane %d (%s)...\n", p.Index, p.Type)
		}

		info, err := fetcher.FetchQuota(ctx, p.ID, provider)
		if err != nil {
			if !IsJSONOutput() {
				fmt.Printf("    Error: %v\n", err)
			}
			continue
		}
		if info.Error != "" {
			if !IsJSONOutput() {
				fmt.Printf("    Error: %s\n", info.Error)
			}
		}
		info.PaneIndex = p.Index
		results = append(results, info)
	}

	if IsJSONOutput() {
		return output.PrintJSON(results)
	}

	printQuotaTable(results)
	return nil
}

func printQuotaTable(results []*quota.QuotaInfo) {
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "Pane\tProvider\tSession\tWeekly\tReset\tAccount")
	fmt.Fprintln(w, "────\t────────\t───────\t──────\t─────\t───────")

	for _, r := range results {
		sess := "-"
		if r.SessionUsage > 0 {
			sess = fmt.Sprintf("%.1f%%", r.SessionUsage)
		}
		weekly := "-"
		if r.WeeklyUsage > 0 {
			weekly = fmt.Sprintf("%.1f%%", r.WeeklyUsage)
		}

		account := r.AccountID
		if account == "" {
			account = "-"
		}

		reset := r.ResetString
		if reset == "" {
			reset = "-"
		}

		fmt.Fprintf(w, "%d\t%s\t%s\t%s\t%s\t%s\n",
			r.PaneIndex, r.Provider, sess, weekly, reset, account)
	}
	w.Flush()
}
