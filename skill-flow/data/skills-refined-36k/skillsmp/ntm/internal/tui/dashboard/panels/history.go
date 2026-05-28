package panels

import (
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/history"
	"github.com/Dicklesworthstone/ntm/internal/tui/components"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// historyConfig returns the configuration for the history panel
func historyConfig() PanelConfig {
	return PanelConfig{
		ID:              "history",
		Title:           "Command History",
		Priority:        PriorityNormal,
		RefreshInterval: 30 * time.Second, // Slow refresh, history doesn't change often
		MinWidth:        35,
		MinHeight:       8,
		Collapsible:     true,
	}
}

// HistoryPanel displays command history
type HistoryPanel struct {
	PanelBase
	entries []history.HistoryEntry
	cursor  int
	offset  int
	theme   theme.Theme
	err     error
}

// NewHistoryPanel creates a new history panel
func NewHistoryPanel() *HistoryPanel {
	return &HistoryPanel{
		PanelBase: NewPanelBase(historyConfig()),
		theme:     theme.Current(),
	}
}

// HasError returns true if there's an active error
func (m *HistoryPanel) HasError() bool {
	return m.err != nil
}

// Init implements tea.Model
func (m *HistoryPanel) Init() tea.Cmd {
	return nil
}

// ReplayMsg is sent when user wants to replay a history entry
type ReplayMsg struct {
	Entry history.HistoryEntry
}

// Update implements tea.Model
func (m *HistoryPanel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if !m.IsFocused() {
		return m, nil
	}

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
				if m.cursor < m.offset {
					m.offset = m.cursor
				}
			}
		case "down", "j":
			if m.cursor < len(m.entries)-1 {
				m.cursor++
				if m.cursor >= m.offset+m.contentHeight() {
					m.offset = m.cursor - m.contentHeight() + 1
				}
			}
		case "enter", "r":
			// Replay selected entry
			if len(m.entries) > 0 && m.cursor >= 0 && m.cursor < len(m.entries) {
				selectedEntry := m.entries[m.cursor]
				return m, func() tea.Msg {
					return ReplayMsg{Entry: selectedEntry}
				}
			}
		}
	}
	return m, nil
}

// SetEntries updates the history entries
func (m *HistoryPanel) SetEntries(entries []history.HistoryEntry, err error) {
	m.entries = entries
	m.err = err
	// Keep cursor within bounds
	if m.cursor >= len(m.entries) {
		m.cursor = len(m.entries) - 1
	}
	if m.cursor < 0 {
		m.cursor = 0
	}
}

// Keybindings returns history panel specific shortcuts
func (m *HistoryPanel) Keybindings() []Keybinding {
	return []Keybinding{
		{
			Key:         key.NewBinding(key.WithKeys("enter"), key.WithHelp("enter", "replay")),
			Description: "Replay selected command",
			Action:      "replay",
		},
		{
			Key:         key.NewBinding(key.WithKeys("y"), key.WithHelp("y", "copy")),
			Description: "Copy command to clipboard",
			Action:      "copy",
		},
		{
			Key:         key.NewBinding(key.WithKeys("j"), key.WithHelp("j", "down")),
			Description: "Move cursor down",
			Action:      "down",
		},
		{
			Key:         key.NewBinding(key.WithKeys("k"), key.WithHelp("k", "up")),
			Description: "Move cursor up",
			Action:      "up",
		},
	}
}

func (m *HistoryPanel) contentHeight() int {
	return m.Height() - 4 // borders + header
}

// View renders the panel
func (m *HistoryPanel) View() string {
	t := m.theme
	w, h := m.Width(), m.Height()

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

	// Build header with error badge if needed
	title := m.Config().Title
	if m.err != nil {
		errorBadge := lipgloss.NewStyle().
			Background(t.Red).
			Foreground(t.Base).
			Bold(true).
			Padding(0, 1).
			Render("⚠ Error")
		title = title + " " + errorBadge
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

	if len(m.entries) == 0 {
		content.WriteString("\n" + components.RenderEmptyState(components.EmptyStateOptions{
			Icon:        components.IconEmpty,
			Title:       "No command history",
			Description: "Send prompts to build history",
			Action:      "Press 's' to send a prompt",
			Width:       w - 4,
			Centered:    true,
		}))
		// Ensure stable height to prevent layout jitter
		return boxStyle.Render(FitToHeight(content.String(), h-4))
	}

	visibleHeight := m.contentHeight()
	end := m.offset + visibleHeight
	if end > len(m.entries) {
		end = len(m.entries)
	}

	for i := m.offset; i < end; i++ {
		entry := m.entries[i]
		selected := i == m.cursor

		var lineStyle lipgloss.Style
		if selected {
			lineStyle = lipgloss.NewStyle().Background(t.Surface0).Bold(true)
		} else {
			lineStyle = lipgloss.NewStyle()
		}

		// ID
		idText := entry.ID
		if len(idText) > 4 {
			idText = idText[:4]
		}
		id := lipgloss.NewStyle().Foreground(t.Overlay).Render(idText)

		// Targets
		targets := "all"
		if len(entry.Targets) > 0 {
			targets = strings.Join(entry.Targets, ",")
		}
		if len(targets) > 10 {
			targets = targets[:9] + "…"
		}
		targetStyle := lipgloss.NewStyle().Foreground(t.Blue).Width(10).Render(targets)

		// Prompt
		prompt := strings.ReplaceAll(entry.Prompt, "\n", " ")
		maxPrompt := w - 20
		if maxPrompt < 10 {
			maxPrompt = 10
		}
		if len(prompt) > maxPrompt {
			prompt = prompt[:maxPrompt-1] + "…"
		}
		promptStyle := lipgloss.NewStyle().Foreground(t.Text).Render(prompt)

		// Status
		status := "✓"
		statusColor := t.Green
		if !entry.Success {
			status = "✗"
			statusColor = t.Red
		}
		statusStyle := lipgloss.NewStyle().Foreground(statusColor).Render(status)

		line := fmt.Sprintf("%s %s %s %s", statusStyle, id, targetStyle, promptStyle)
		content.WriteString(lineStyle.Render(line) + "\n")
	}

	// Add scroll indicator if there's more content
	scrollState := components.ScrollState{
		FirstVisible: m.offset,
		LastVisible:  end - 1,
		TotalItems:   len(m.entries),
	}
	if footer := components.ScrollFooter(scrollState, w-4); footer != "" {
		content.WriteString(footer + "\n")
	}

	// Ensure stable height to prevent layout jitter
	return boxStyle.Render(FitToHeight(content.String(), h-4))
}
