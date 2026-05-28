package components

import (
	"strings"

	"github.com/charmbracelet/lipgloss"
	"github.com/muesli/reflow/wordwrap"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// Preview is a content preview pane component
type Preview struct {
	Title       string
	Content     string
	Width       int
	Height      int
	BorderColor lipgloss.Color
	TitleColor  lipgloss.Color
	ShowBorder  bool
	Wrap        bool
}

// NewPreview creates a new preview pane
func NewPreview() *Preview {
	t := theme.Current()
	return &Preview{
		Width:       40,
		Height:      10,
		BorderColor: t.Surface2,
		TitleColor:  t.Primary,
		ShowBorder:  true,
		Wrap:        true,
	}
}

// WithTitle sets the preview title
func (p *Preview) WithTitle(title string) *Preview {
	p.Title = title
	return p
}

// WithContent sets the preview content
func (p *Preview) WithContent(content string) *Preview {
	p.Content = content
	return p
}

// WithSize sets the preview dimensions
func (p *Preview) WithSize(width, height int) *Preview {
	p.Width = width
	p.Height = height
	return p
}

// WithBorder enables/disables the border
func (p *Preview) WithBorder(show bool) *Preview {
	p.ShowBorder = show
	return p
}

// Render renders the preview pane
func (p *Preview) Render() string {
	t := theme.Current()

	// Wrap content if needed
	content := p.Content
	contentWidth := p.Width - 4 // Account for padding and border
	if contentWidth < 10 {
		contentWidth = 10
	}

	if p.Wrap && content != "" {
		content = wordwrap.String(content, contentWidth)
	}

	// Split into lines and limit height
	lines := strings.Split(content, "\n")
	maxLines := p.Height - 3 // Account for title and borders
	if maxLines < 1 {
		maxLines = 1
	}

	if len(lines) > maxLines {
		lines = lines[:maxLines]
		lines = append(lines, "...")
	}

	// Style content
	contentStyle := lipgloss.NewStyle().
		Foreground(t.Text).
		Width(contentWidth)

	styledContent := contentStyle.Render(strings.Join(lines, "\n"))

	if !p.ShowBorder {
		// No border, just title + content
		if p.Title != "" {
			titleStyle := lipgloss.NewStyle().
				Bold(true).
				Foreground(p.TitleColor)
			dividerStyle := lipgloss.NewStyle().Foreground(t.Surface2)

			return titleStyle.Render(p.Title) + "\n" +
				dividerStyle.Render(strings.Repeat("─", contentWidth)) + "\n" +
				styledContent
		}
		return styledContent
	}

	// With border
	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(p.BorderColor).
		Width(p.Width-2).
		Padding(0, 1)

	boxContent := boxStyle.Render(styledContent)

	// Add title to border
	if p.Title != "" {
		titleStyle := lipgloss.NewStyle().
			Bold(true).
			Foreground(p.TitleColor)

		renderedTitle := titleStyle.Render(" " + p.Title + " ")

		// Insert title into top border
		lines := strings.Split(boxContent, "\n")
		if len(lines) > 0 {
			topBorder := lines[0]
			if lipgloss.Width(topBorder) > 4 {
				lines[0] = insertTitleIntoBorder(topBorder, renderedTitle, 2)
			}

			return strings.Join(lines, "\n")
		}
	}

	return boxContent
}

// String implements fmt.Stringer
func (p *Preview) String() string {
	return p.Render()
}

// StatusBar is a bottom status/help bar
type StatusBar struct {
	Left   string
	Center string
	Right  string
	Width  int
}

// NewStatusBar creates a new status bar
func NewStatusBar(width int) *StatusBar {
	return &StatusBar{
		Width: width,
	}
}

// WithLeft sets left-aligned content
func (s *StatusBar) WithLeft(text string) *StatusBar {
	s.Left = text
	return s
}

// WithCenter sets center-aligned content
func (s *StatusBar) WithCenter(text string) *StatusBar {
	s.Center = text
	return s
}

// WithRight sets right-aligned content
func (s *StatusBar) WithRight(text string) *StatusBar {
	s.Right = text
	return s
}

// Render renders the status bar
func (s *StatusBar) Render() string {
	t := theme.Current()

	barStyle := lipgloss.NewStyle().
		Foreground(t.Subtext).
		Background(t.Surface0).
		Width(s.Width)

	leftStyle := lipgloss.NewStyle().
		Foreground(t.Subtext).
		Padding(0, 1)

	centerStyle := lipgloss.NewStyle().
		Foreground(t.Overlay)

	rightStyle := lipgloss.NewStyle().
		Foreground(t.Subtext).
		Padding(0, 1)

	// Calculate widths
	leftLen := lipgloss.Width(s.Left) + 2
	rightLen := lipgloss.Width(s.Right) + 2
	centerSpace := s.Width - leftLen - rightLen

	if centerSpace < 0 {
		centerSpace = 0
	}

	// Build content
	left := leftStyle.Render(s.Left)
	right := rightStyle.Render(s.Right)

	// Center content with padding
	centerPadded := centerStyle.Width(centerSpace).Align(lipgloss.Center).Render(s.Center)

	content := left + centerPadded + right

	return barStyle.Render(content)
}

// HelpBar creates a help text bar with key hints
type HelpBar struct {
	Items []HelpItem
	Width int
}

// HelpItem is a key binding hint
type HelpItem struct {
	Key  string
	Desc string
}

// NewHelpBar creates a help bar
func NewHelpBar(width int) *HelpBar {
	return &HelpBar{
		Width: width,
	}
}

// Add adds a help item
func (h *HelpBar) Add(key, desc string) *HelpBar {
	h.Items = append(h.Items, HelpItem{Key: key, Desc: desc})
	return h
}

// Render renders the help bar
func (h *HelpBar) Render() string {
	t := theme.Current()

	keyStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(t.Primary)

	descStyle := lipgloss.NewStyle().
		Foreground(t.Overlay)

	sepStyle := lipgloss.NewStyle().
		Foreground(t.Surface2)

	var parts []string
	for _, item := range h.Items {
		parts = append(parts, keyStyle.Render(item.Key)+" "+descStyle.Render(item.Desc))
	}

	content := strings.Join(parts, sepStyle.Render(" • "))

	// Center it
	return lipgloss.NewStyle().
		Width(h.Width).
		Align(lipgloss.Center).
		Foreground(t.Overlay).
		Render(content)
}

// String implements fmt.Stringer
func (h *HelpBar) String() string {
	return h.Render()
}

// Header creates a styled header
type Header struct {
	Title    string
	Subtitle string
	Icon     string
	Width    int
}

// NewHeader creates a new header
func NewHeader(title string, width int) *Header {
	return &Header{
		Title: title,
		Width: width,
	}
}

// WithSubtitle adds a subtitle
func (h *Header) WithSubtitle(subtitle string) *Header {
	h.Subtitle = subtitle
	return h
}

// WithIcon adds an icon
func (h *Header) WithIcon(icon string) *Header {
	h.Icon = icon
	return h
}

// Render renders the header
func (h *Header) Render() string {
	t := theme.Current()

	titleStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(t.Primary)

	subtitleStyle := lipgloss.NewStyle().
		Foreground(t.Subtext)

	iconStyle := lipgloss.NewStyle().
		Foreground(t.Secondary)

	var title string
	if h.Icon != "" {
		title = iconStyle.Render(h.Icon) + " " + titleStyle.Render(h.Title)
	} else {
		title = titleStyle.Render(h.Title)
	}

	if h.Subtitle != "" {
		sepStyle := lipgloss.NewStyle().Foreground(t.Surface2)
		title += sepStyle.Render(" │ ") + subtitleStyle.Render(h.Subtitle)
	}

	return title
}

// String implements fmt.Stringer
func (h *Header) String() string {
	return h.Render()
}
