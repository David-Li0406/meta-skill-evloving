package panels

import (
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/components"
	"github.com/Dicklesworthstone/ntm/internal/tui/styles"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// AgentMetric represents token usage and routing info for a single agent
type AgentMetric struct {
	Name       string
	Type       string // "cc", "cod", "gmi"
	Tokens     int
	Cost       float64
	ContextPct float64

	// Routing info (from robot-route API)
	RoutingScore  float64 // 0-100 routing score (0 means not computed)
	IsRecommended bool    // True if this is the recommended agent
	State         string  // Agent state: waiting, generating, etc.
}

// MetricsData holds the data for the metrics panel
type MetricsData struct {
	TotalTokens int
	TotalCost   float64
	Agents      []AgentMetric
}

// MetricsPanel displays session token usage and costs
type MetricsPanel struct {
	PanelBase
	data  MetricsData
	theme theme.Theme
	err   error
}

// metricsConfig returns the configuration for the metrics panel
func metricsConfig() PanelConfig {
	return PanelConfig{
		ID:              "metrics",
		Title:           "Metrics & Usage",
		Priority:        PriorityNormal,
		RefreshInterval: 10 * time.Second,
		MinWidth:        30,
		MinHeight:       8,
		Collapsible:     true,
	}
}

// NewMetricsPanel creates a new metrics panel
func NewMetricsPanel() *MetricsPanel {
	return &MetricsPanel{
		PanelBase: NewPanelBase(metricsConfig()),
		theme:     theme.Current(),
	}
}

// Init implements tea.Model
func (m *MetricsPanel) Init() tea.Cmd {
	return nil
}

// Update implements tea.Model
func (m *MetricsPanel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, nil
}

// SetData updates the panel data
func (m *MetricsPanel) SetData(data MetricsData, err error) {
	m.data = data
	m.err = err
	// Only update timestamp on successful fetch
	if err == nil {
		m.SetLastUpdate(time.Now())
	}
}

// HasError returns true if there's an active error
func (m *MetricsPanel) HasError() bool {
	return m.err != nil
}

// Keybindings returns metrics panel specific shortcuts
func (m *MetricsPanel) Keybindings() []Keybinding {
	return []Keybinding{
		{
			Key:         key.NewBinding(key.WithKeys("r"), key.WithHelp("r", "refresh")),
			Description: "Refresh metrics",
			Action:      "refresh",
		},
		{
			Key:         key.NewBinding(key.WithKeys("c"), key.WithHelp("c", "copy stats")),
			Description: "Copy stats to clipboard",
			Action:      "copy",
		},
	}
}

// View renders the panel
func (m *MetricsPanel) View() string {
	t := m.theme
	w, h := m.Width(), m.Height()

	// Create border style based on focus
	borderColor := t.Surface1
	bgColor := t.Base
	if m.IsFocused() {
		borderColor = t.Primary
		bgColor = t.Surface0 // Subtle tint for focused panel
	}

	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(borderColor).
		Background(bgColor).
		Width(w-2).
		Height(h-2).
		Padding(0, 1)

	var content strings.Builder

	// Build header with stale/error badge if needed
	title := m.Config().Title
	if m.err != nil {
		errorBadge := lipgloss.NewStyle().
			Background(t.Red).
			Foreground(t.Base).
			Bold(true).
			Padding(0, 1).
			Render("⚠ Error")
		title = title + " " + errorBadge
	} else if staleBadge := components.RenderStaleBadge(m.LastUpdate(), m.Config().RefreshInterval); staleBadge != "" {
		title = title + " " + staleBadge
	}

	// Header
	headerStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(t.Lavender).
		Border(lipgloss.NormalBorder(), false, false, true, false).
		BorderForeground(t.Surface1).
		Width(w - 4).
		Align(lipgloss.Center)

	content.WriteString(headerStyle.Render(title) + "\n")

	// Show error message if present
	if m.err != nil {
		content.WriteString(components.ErrorState(m.err.Error(), "Press r to retry", w-4) + "\n")
	}

	// Empty state: no agents
	if m.data.TotalTokens == 0 && len(m.data.Agents) == 0 && m.err == nil {
		content.WriteString("\n" + components.RenderEmptyState(components.EmptyStateOptions{
			Icon:        components.IconWaiting,
			Title:       "No metrics yet",
			Description: "Data appears when agents start",
			Width:       w - 4,
			Centered:    true,
		}))
		// Ensure stable height to prevent layout jitter
		return boxStyle.Render(FitToHeight(content.String(), h-4))
	}
	content.WriteString("\n")

	// Total Usage Bar
	// Calculate total context limit (heuristic: sum of agents?)
	// Or just show total tokens.
	// For bar, we need a max. Let's assume 1M tokens as a reference scale for "heavy session".
	const refScale = 1000000.0
	totalPct := float64(m.data.TotalTokens) / refScale
	if totalPct > 1.0 {
		totalPct = 1.0
	}

	bar := styles.ProgressBar(totalPct, w-6, "█", "░", string(t.Blue), string(t.Pink))

	content.WriteString(lipgloss.NewStyle().Foreground(t.Subtext).Render("Session Total") + "\n")
	content.WriteString(bar + "\n")

	stats := fmt.Sprintf("%d tokens  •  $%.2f est.", m.data.TotalTokens, m.data.TotalCost)
	content.WriteString(lipgloss.NewStyle().Foreground(t.Text).Align(lipgloss.Right).Width(w-6).Render(stats) + "\n\n")

	// Per-Agent Bars
	// Only show top N agents if space is limited
	availHeight := h - 10 // approx header/footer usage
	if availHeight < 0 {
		availHeight = 0
	}

	for i, agent := range m.data.Agents {
		if i >= availHeight/2 { // 2 lines per agent
			content.WriteString(lipgloss.NewStyle().Foreground(t.Overlay).Render(fmt.Sprintf("...and %d more", len(m.data.Agents)-i)) + "\n")
			break
		}

		// Agent label
		valStyle := lipgloss.NewStyle().Foreground(t.Overlay)

		var typeColor lipgloss.Color
		switch agent.Type {
		case "cc":
			typeColor = t.Claude
		case "cod":
			typeColor = t.Codex
		case "gmi":
			typeColor = t.Gemini
		default:
			typeColor = t.Green
		}

		// Build name with optional recommended indicator
		nameStr := agent.Name
		if agent.IsRecommended {
			nameStr = "★ " + nameStr // Star indicates recommended agent
		}
		name := lipgloss.NewStyle().Foreground(typeColor).Bold(true).Render(nameStr)

		// Build info line with routing score if available
		var infoParts []string
		if agent.RoutingScore > 0 {
			// Show routing score as a badge
			scoreStyle := lipgloss.NewStyle().Foreground(t.Green)
			if agent.RoutingScore < 50 {
				scoreStyle = scoreStyle.Foreground(t.Yellow)
			}
			if agent.RoutingScore < 25 {
				scoreStyle = scoreStyle.Foreground(t.Red)
			}
			infoParts = append(infoParts, scoreStyle.Render(fmt.Sprintf("%.0f", agent.RoutingScore)))
		}
		infoParts = append(infoParts, fmt.Sprintf("%d tok", agent.Tokens))
		if agent.State != "" {
			stateStyle := lipgloss.NewStyle().Foreground(t.Overlay)
			infoParts = append(infoParts, stateStyle.Render(agent.State))
		}
		info := strings.Join(infoParts, " • ")

		// Space between name and info
		gap := w - 6 - lipgloss.Width(name) - lipgloss.Width(info)
		if gap < 1 {
			gap = 1
		}

		line := name + strings.Repeat(" ", gap) + valStyle.Render(info)
		content.WriteString(line + "\n")

		// Mini bar (context usage)
		miniBar := styles.ProgressBar(agent.ContextPct/100.0, w-6, "━", "┄", string(typeColor))
		content.WriteString(miniBar + "\n")
	}

	// Add freshness indicator at the bottom
	if footer := components.RenderFreshnessFooter(components.FreshnessOptions{
		LastUpdate:      m.LastUpdate(),
		RefreshInterval: m.Config().RefreshInterval,
		Width:           w - 4,
	}); footer != "" {
		content.WriteString(footer + "\n")
	}

	// Ensure stable height to prevent layout jitter
	return boxStyle.Render(FitToHeight(content.String(), h-4))
}
