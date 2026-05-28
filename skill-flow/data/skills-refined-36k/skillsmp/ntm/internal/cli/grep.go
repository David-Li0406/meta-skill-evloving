package cli

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// GrepMatch represents a single search match in pane output
type GrepMatch struct {
	Session string   `json:"session"`
	Pane    string   `json:"pane"`
	PaneID  string   `json:"pane_id"`
	Line    int      `json:"line"`
	Content string   `json:"content"`
	Context []string `json:"context,omitempty"`
}

// GrepResult contains all matches from a grep operation
type GrepResult struct {
	Pattern    string      `json:"pattern"`
	Session    string      `json:"session"`
	Matches    []GrepMatch `json:"matches"`
	TotalLines int         `json:"total_lines_searched"`
	MatchCount int         `json:"match_count"`
	PaneCount  int         `json:"panes_searched"`
}

// Text outputs the grep result as human-readable text
func (r *GrepResult) Text(w io.Writer) error {
	t := theme.Current()

	if len(r.Matches) == 0 {
		fmt.Fprintf(w, "%sNo matches found%s for pattern '%s'\n",
			colorize(t.Warning), colorize(t.Text), r.Pattern)
		return nil
	}

	// Group matches by pane for cleaner output
	lastKey := ""
	for i, m := range r.Matches {
		// Print pane header when pane changes
		key := m.Session + "/" + m.Pane
		if key != lastKey {
			if i > 0 {
				fmt.Fprintln(w, "--")
			}
			lastKey = key
		}

		// Print context before (if any)
		if len(m.Context) > 0 {
			contextBefore := len(m.Context) / 2
			for j := 0; j < contextBefore && j < len(m.Context); j++ {
				lineNum := m.Line - contextBefore + j
				if lineNum > 0 {
					fmt.Fprintf(w, "%s%s/%s:%d-%s %s\n",
						colorize(t.Surface1), m.Session, m.Pane, lineNum, colorize(t.Text), m.Context[j])
				}
			}
		}

		// Print matching line with highlighting
		fmt.Fprintf(w, "%s%s/%s:%d:%s %s\n",
			colorize(t.Blue), m.Session, m.Pane, m.Line, colorize(t.Text),
			highlightMatch(m.Content, r.Pattern, t))

		// Print context after (if any)
		if len(m.Context) > 0 {
			contextBefore := len(m.Context) / 2
			for j := contextBefore; j < len(m.Context); j++ {
				lineNum := m.Line + j - contextBefore + 1
				fmt.Fprintf(w, "%s%s/%s:%d-%s %s\n",
					colorize(t.Surface1), m.Session, m.Pane, lineNum, colorize(t.Text), m.Context[j])
			}
		}
	}

	fmt.Fprintf(w, "\n%s%d matches%s in %d pane(s)\n",
		colorize(t.Success), r.MatchCount, colorize(t.Text), r.PaneCount)

	return nil
}

// JSON returns the JSON-serializable data
func (r *GrepResult) JSON() interface{} {
	return r
}

func newGrepCmd() *cobra.Command {
	var (
		caseInsensitive bool
		invertMatch     bool
		contextLines    int
		afterLines      int
		beforeLines     int
		maxLines        int
		listOnly        bool
		allFlag         bool
		ccFlag          bool
		codFlag         bool
		gmiFlag         bool
	)

	cmd := &cobra.Command{
		Use:   "grep <pattern> [session-name]",
		Short: "Search pane output with regex",
		Long: `Search across all pane output buffers with regex support.

Searches the captured output from tmux panes for lines matching
the given pattern. Supports standard regex syntax.

Examples:
  ntm grep 'error' myproject          # Search all panes
  ntm grep 'error' myproject --cc     # Only Claude panes
  ntm grep 'def.*auth' myproject -i   # Case insensitive
  ntm grep 'TODO' myproject -C 3      # 3 lines context
  ntm grep 'pattern' myproject -n 100 # Search last 100 lines
  ntm grep 'pattern' --all            # Search all sessions`,
		Args: cobra.RangeArgs(1, 2),
		RunE: func(cmd *cobra.Command, args []string) error {
			pattern := args[0]
			var session string
			if len(args) > 1 {
				session = args[1]
			}

			// Determine context
			context := contextLines
			if afterLines > 0 || beforeLines > 0 {
				// Use specific before/after if set
				context = 0
			}

			filter := AgentFilter{
				Claude: ccFlag,
				Codex:  codFlag,
				Gemini: gmiFlag,
			}

			opts := GrepOptions{
				AllSessions:     allFlag,
				CaseInsensitive: caseInsensitive,
				InvertMatch:     invertMatch,
				ContextLines:    context,
				AfterLines:      afterLines,
				BeforeLines:     beforeLines,
				MaxLines:        maxLines,
				ListOnly:        listOnly,
				Filter:          filter,
			}

			return runGrep(pattern, session, opts)
		},
	}

	cmd.Flags().BoolVarP(&caseInsensitive, "ignore-case", "i", false, "Case insensitive search")
	cmd.Flags().BoolVarP(&invertMatch, "invert-match", "v", false, "Invert match (show non-matching lines)")
	cmd.Flags().IntVarP(&contextLines, "context", "C", 0, "Show N lines of context")
	cmd.Flags().IntVarP(&afterLines, "after-context", "A", 0, "Show N lines after match")
	cmd.Flags().IntVarP(&beforeLines, "before-context", "B", 0, "Show N lines before match")
	cmd.Flags().IntVarP(&maxLines, "max-lines", "n", 1000, "Search last N lines per pane")
	cmd.Flags().BoolVarP(&listOnly, "files-with-matches", "l", false, "List matching panes only")
	cmd.Flags().BoolVar(&allFlag, "all", false, "Search all sessions")
	cmd.Flags().BoolVar(&ccFlag, "cc", false, "Search Claude panes only")
	cmd.Flags().BoolVar(&codFlag, "cod", false, "Search Codex panes only")
	cmd.Flags().BoolVar(&gmiFlag, "gmi", false, "Search Gemini panes only")
	cmd.ValidArgsFunction = completeSessionSecondArg

	return cmd
}

// GrepOptions contains options for the grep operation
type GrepOptions struct {
	AllSessions     bool
	CaseInsensitive bool
	InvertMatch     bool
	ContextLines    int
	AfterLines      int
	BeforeLines     int
	MaxLines        int
	ListOnly        bool
	Filter          AgentFilter
}

func runGrep(pattern, session string, opts GrepOptions) error {
	if err := tmux.EnsureInstalled(); err != nil {
		return err
	}

	// Compile regex
	rePattern := pattern
	if opts.CaseInsensitive {
		rePattern = "(?i)" + pattern
	}
	re, err := regexp.Compile(rePattern)
	if err != nil {
		return fmt.Errorf("invalid pattern: %w", err)
	}

	// Determine target session(s)
	var sessions []string
	if opts.AllSessions {
		sessionList, err := tmux.ListSessions()
		if err != nil {
			return err
		}
		if len(sessionList) == 0 {
			return fmt.Errorf("no tmux sessions found")
		}
		for _, s := range sessionList {
			sessions = append(sessions, s.Name)
		}
	} else {
		res, err := ResolveSession(session, os.Stdout)
		if err != nil {
			return err
		}
		if res.Session == "" {
			return nil
		}
		res.ExplainIfInferred(os.Stderr)
		session = res.Session

		if !tmux.SessionExists(session) {
			return fmt.Errorf("session '%s' not found", session)
		}
		sessions = []string{session}
	}

	// Search across sessions
	var allMatches []GrepMatch
	totalLines := 0
	panesSearched := 0
	matchingPanes := make(map[string]bool)

	for _, sess := range sessions {
		panes, err := tmux.GetPanes(sess)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to get panes for %s: %v\n", sess, err)
			continue
		}

		for _, pane := range panes {
			// Apply agent filter
			if opts.Filter.IsEmpty() {
				if pane.Type == tmux.AgentUser {
					continue
				}
			} else if !opts.Filter.Matches(pane.Type) {
				continue
			}

			output, err := tmux.CapturePaneOutput(pane.ID, opts.MaxLines)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Warning: failed to capture pane %s: %v\n", pane.Title, err)
				continue
			}

			lines := strings.Split(output, "\n")
			totalLines += len(lines)
			panesSearched++

			// Search lines
			for i, line := range lines {
				matches := re.MatchString(line)
				if opts.InvertMatch {
					matches = !matches
				}

				if matches {
					matchingPanes[sess+"/"+pane.Title] = true

					if !opts.ListOnly {
						// Build context
						var context []string
						beforeCount := opts.BeforeLines
						afterCount := opts.AfterLines
						if opts.ContextLines > 0 {
							beforeCount = opts.ContextLines
							afterCount = opts.ContextLines
						}

						// Get lines before
						for j := i - beforeCount; j < i && j >= 0; j++ {
							context = append(context, lines[j])
						}
						// Get lines after
						for j := i + 1; j <= i+afterCount && j < len(lines); j++ {
							context = append(context, lines[j])
						}

						allMatches = append(allMatches, GrepMatch{
							Session: sess,
							Pane:    pane.Title,
							PaneID:  pane.ID,
							Line:    i + 1, // 1-indexed
							Content: line,
							Context: context,
						})
					}
				}
			}
		}
	}

	// Build result
	result := &GrepResult{
		Pattern:    pattern,
		Session:    session,
		Matches:    allMatches,
		TotalLines: totalLines,
		MatchCount: len(allMatches),
		PaneCount:  panesSearched,
	}
	if opts.AllSessions {
		result.Session = "<all>"
	}

	// Handle list-only mode
	if opts.ListOnly {
		result.MatchCount = len(matchingPanes)
		return outputMatchingPanes(matchingPanes)
	}

	// Output result
	formatter := output.New(output.WithJSON(jsonOutput))
	return formatter.Output(result)
}

func outputMatchingPanes(panes map[string]bool) error {
	t := theme.Current()

	if jsonOutput {
		paneList := make([]string, 0, len(panes))
		for p := range panes {
			paneList = append(paneList, p)
		}
		return output.PrintJSON(map[string]interface{}{
			"matching_panes": paneList,
			"count":          len(paneList),
		})
	}

	if len(panes) == 0 {
		fmt.Printf("%sNo matching panes found%s\n", colorize(t.Warning), colorize(t.Text))
		return nil
	}

	for p := range panes {
		fmt.Printf("%s%s%s\n", colorize(t.Blue), p, colorize(t.Text))
	}
	return nil
}

// highlightMatch highlights the matched portion in the line
func highlightMatch(line, pattern string, t theme.Theme) string {
	// Try raw pattern first (matches what the search actually uses)
	re, err := regexp.Compile("(?i)(" + pattern + ")")
	if err != nil {
		// If pattern fails to compile as regex, use escaped literal
		re, err = regexp.Compile("(?i)(" + regexp.QuoteMeta(pattern) + ")")
		if err != nil {
			return line // Can't highlight, return as-is
		}
	}

	highlighted := re.ReplaceAllStringFunc(line, func(match string) string {
		return fmt.Sprintf("%s%s%s", colorize(t.Yellow), match, colorize(t.Text))
	})

	return highlighted
}
