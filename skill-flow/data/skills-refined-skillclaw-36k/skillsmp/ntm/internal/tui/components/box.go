package components

import (
	"strings"

	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/x/ansi"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// BoxStyle defines the visual style of a box
type BoxStyle int

const (
	BoxRounded BoxStyle = iota
	BoxDouble
	BoxThick
	BoxNormal
	BoxHidden
)

// Box creates styled box containers
type Box struct {
	Title       string
	TitleAlign  lipgloss.Position
	Content     string
	Width       int
	Height      int
	Style       BoxStyle
	BorderColor lipgloss.Color
	TitleColor  lipgloss.Color
	Padding     int
}

// NewBox creates a new box with defaults
func NewBox() *Box {
	t := theme.Current()
	return &Box{
		TitleAlign:  lipgloss.Left,
		Style:       BoxRounded,
		BorderColor: t.Blue,
		TitleColor:  t.Primary,
		Padding:     1,
	}
}

// WithTitle sets the box title
func (b *Box) WithTitle(title string) *Box {
	b.Title = title
	return b
}

// WithContent sets the box content
func (b *Box) WithContent(content string) *Box {
	b.Content = content
	return b
}

// WithSize sets the box dimensions
func (b *Box) WithSize(width, height int) *Box {
	b.Width = width
	b.Height = height
	return b
}

// WithStyle sets the border style
func (b *Box) WithStyle(style BoxStyle) *Box {
	b.Style = style
	return b
}

// WithBorderColor sets the border color
func (b *Box) WithBorderColor(color lipgloss.Color) *Box {
	b.BorderColor = color
	return b
}

// WithTitleColor sets the title color
func (b *Box) WithTitleColor(color lipgloss.Color) *Box {
	b.TitleColor = color
	return b
}

// WithPadding sets internal padding
func (b *Box) WithPadding(padding int) *Box {
	b.Padding = padding
	return b
}

// getBorder returns the lipgloss border for the style
func (b *Box) getBorder() lipgloss.Border {
	switch b.Style {
	case BoxDouble:
		return lipgloss.DoubleBorder()
	case BoxThick:
		return lipgloss.ThickBorder()
	case BoxNormal:
		return lipgloss.NormalBorder()
	case BoxHidden:
		return lipgloss.HiddenBorder()
	default:
		return lipgloss.RoundedBorder()
	}
}

// Render renders the box to a string
func (b *Box) Render() string {
	border := b.getBorder()

	style := lipgloss.NewStyle().
		Border(border).
		BorderForeground(b.BorderColor).
		Padding(b.Padding)

	if b.Width > 0 {
		style = style.Width(b.Width - 2) // Account for border
	}

	if b.Height > 0 {
		style = style.Height(b.Height - 2) // Account for border
	}

	content := b.Content

	// Add title if present
	if b.Title != "" {
		titleStyle := lipgloss.NewStyle().
			Bold(true).
			Foreground(b.TitleColor)

		renderedTitle := titleStyle.Render(" " + b.Title + " ")

		// The title is rendered as part of the border
		// We use a custom approach with BorderLabel
		style = style.BorderTop(true).BorderBottom(true).BorderLeft(true).BorderRight(true)

		// Create a styled box with the content
		boxContent := style.Render(content)

		// Insert title into top border
		lines := strings.Split(boxContent, "\n")
		if len(lines) > 0 {
			topBorder := lines[0]
			// Calculate position for title (visible width, ANSI-aware)
			titlePos := 2 // After corner and one border char
			borderWidth := lipgloss.Width(topBorder)
			titleWidth := lipgloss.Width(renderedTitle)

			if borderWidth > titlePos+titleWidth {
				// Calculate insertion point based on alignment
				insertPos := titlePos
				switch b.TitleAlign {
				case lipgloss.Center:
					insertPos = (borderWidth - titleWidth) / 2
				case lipgloss.Right:
					insertPos = borderWidth - titleWidth - 2
				}

				if insertPos < titlePos {
					insertPos = titlePos
				}

				lines[0] = insertTitleIntoBorder(topBorder, renderedTitle, insertPos)
			}
			return strings.Join(lines, "\n")
		}

		return boxContent
	}

	return style.Render(content)
}

// insertTitleIntoBorder replaces a visible-width slice of a border line with a title,
// preserving ANSI escape sequences.
func insertTitleIntoBorder(line, title string, insertPos int) string {
	totalWidth := lipgloss.Width(line)
	titleWidth := lipgloss.Width(title)
	if totalWidth == 0 || titleWidth == 0 {
		return line
	}
	if insertPos < 0 {
		insertPos = 0
	}
	if insertPos+titleWidth > totalWidth {
		return line
	}

	left := ansi.Cut(line, 0, insertPos)
	right := ansi.Cut(line, insertPos+titleWidth, totalWidth)
	return left + title + right
}

// String implements fmt.Stringer
func (b *Box) String() string {
	return b.Render()
}

// SimpleBox creates a simple box with title and content
func SimpleBox(title, content string, width int) string {
	t := theme.Current()
	return NewBox().
		WithTitle(title).
		WithContent(content).
		WithSize(width, 0).
		WithBorderColor(t.Blue).
		WithTitleColor(t.Primary).
		Render()
}

// InfoBox creates an info-styled box
func InfoBox(title, content string, width int) string {
	t := theme.Current()
	return NewBox().
		WithTitle(title).
		WithContent(content).
		WithSize(width, 0).
		WithBorderColor(t.Info).
		WithTitleColor(t.Info).
		Render()
}

// SuccessBox creates a success-styled box
func SuccessBox(title, content string, width int) string {
	t := theme.Current()
	return NewBox().
		WithTitle(title).
		WithContent(content).
		WithSize(width, 0).
		WithBorderColor(t.Success).
		WithTitleColor(t.Success).
		Render()
}

// ErrorBox creates an error-styled box
func ErrorBox(title, content string, width int) string {
	t := theme.Current()
	return NewBox().
		WithTitle(title).
		WithContent(content).
		WithSize(width, 0).
		WithBorderColor(t.Error).
		WithTitleColor(t.Error).
		Render()
}

// WarningBox creates a warning-styled box
func WarningBox(title, content string, width int) string {
	t := theme.Current()
	return NewBox().
		WithTitle(title).
		WithContent(content).
		WithSize(width, 0).
		WithBorderColor(t.Warning).
		WithTitleColor(t.Warning).
		Render()
}

// Divider creates a horizontal divider line
func Divider(width int) string {
	t := theme.Current()
	style := lipgloss.NewStyle().Foreground(t.Surface2)
	return style.Render(strings.Repeat("─", width))
}

// DoubleDivider creates a double-line divider
func DoubleDivider(width int) string {
	t := theme.Current()
	style := lipgloss.NewStyle().Foreground(t.Surface2)
	return style.Render(strings.Repeat("═", width))
}

// ThinDivider creates a thin divider with dots
func ThinDivider(width int) string {
	t := theme.Current()
	style := lipgloss.NewStyle().Foreground(t.Overlay)
	return style.Render(strings.Repeat("·", width))
}

// LabeledDivider creates a divider with a centered label
func LabeledDivider(label string, width int) string {
	t := theme.Current()
	lineStyle := lipgloss.NewStyle().Foreground(t.Surface2)
	labelStyle := lipgloss.NewStyle().Foreground(t.Subtext)

	labelLen := lipgloss.Width(label) + 2 // Add padding
	if width <= labelLen+4 {
		return labelStyle.Render(label)
	}

	sideLen := (width - labelLen) / 2
	leftLine := lineStyle.Render(strings.Repeat("─", sideLen))
	rightLine := lineStyle.Render(strings.Repeat("─", width-sideLen-labelLen))
	renderedLabel := labelStyle.Render(" " + label + " ")

	return leftLine + renderedLabel + rightLine
}
