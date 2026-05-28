// Package components provides shared TUI building blocks.
package components

import (
	"fmt"

	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// ScrollState tracks scroll position within a viewport.
type ScrollState struct {
	FirstVisible int // Index of first visible item (0-indexed)
	LastVisible  int // Index of last visible item (0-indexed, inclusive)
	TotalItems   int // Total number of items
}

// HasMoreAbove returns true if there's content above the viewport.
func (s ScrollState) HasMoreAbove() bool {
	return s.FirstVisible > 0
}

// HasMoreBelow returns true if there's content below the viewport.
func (s ScrollState) HasMoreBelow() bool {
	return s.TotalItems > 0 && s.LastVisible < s.TotalItems-1
}

// AllVisible returns true if all items fit in the viewport.
func (s ScrollState) AllVisible() bool {
	return !s.HasMoreAbove() && !s.HasMoreBelow()
}

// Indicator returns the arrow indicator string based on scroll state.
// Returns "▲▼" when content above and below, "▲" for above only,
// "▼" for below only, or "" when all content is visible.
func (s ScrollState) Indicator() string {
	switch {
	case s.HasMoreAbove() && s.HasMoreBelow():
		return "▲▼"
	case s.HasMoreAbove():
		return "▲"
	case s.HasMoreBelow():
		return "▼"
	default:
		return ""
	}
}

// ScrollIndicatorOptions configures scroll indicator rendering.
type ScrollIndicatorOptions struct {
	State ScrollState // Current scroll state
	Width int         // Available width for rendering
	// ShowCount enables showing item counts (e.g., "1-5 of 20")
	ShowCount bool
}

// RenderScrollIndicator renders a scroll position indicator.
// Format depends on width:
// - Wide: "Showing 1-5 of 20 ▼"
// - Medium: "(1-5/20) ▼"
// - Narrow: "(5/20) ▼"
// Returns empty string if all items are visible.
func RenderScrollIndicator(opts ScrollIndicatorOptions) string {
	s := opts.State

	// Don't show indicator if all items are visible
	if s.AllVisible() {
		return ""
	}

	t := theme.Current()

	// Style for the indicator text
	textStyle := lipgloss.NewStyle().
		Foreground(t.Overlay)

	// Style for the arrow indicators
	arrowStyle := lipgloss.NewStyle().
		Foreground(t.Blue).
		Bold(true)

	indicator := s.Indicator()

	// Determine format based on width and ShowCount option
	if !opts.ShowCount {
		// Just show arrows
		return arrowStyle.Render(indicator)
	}

	// Calculate position strings
	first := s.FirstVisible + 1 // Convert to 1-indexed for display
	last := s.LastVisible + 1
	total := s.TotalItems

	var countStr string
	if opts.Width >= 25 {
		// Wide format: "Showing 1-5 of 20"
		countStr = fmt.Sprintf("Showing %d-%d of %d", first, last, total)
	} else if opts.Width >= 15 {
		// Medium format: "(1-5/20)"
		countStr = fmt.Sprintf("(%d-%d/%d)", first, last, total)
	} else {
		// Narrow format: "(5/20)" - just show current position
		countStr = fmt.Sprintf("(%d/%d)", last, total)
	}

	if indicator != "" {
		return textStyle.Render(countStr) + " " + arrowStyle.Render(indicator)
	}
	return textStyle.Render(countStr)
}

// ScrollFooter renders a complete footer line with scroll indicator.
// Positions the indicator on the right side of the available width.
func ScrollFooter(state ScrollState, width int) string {
	if state.AllVisible() {
		return ""
	}

	indicator := RenderScrollIndicator(ScrollIndicatorOptions{
		State:     state,
		Width:     width,
		ShowCount: width >= 15,
	})

	if indicator == "" {
		return ""
	}

	// Right-align the indicator
	indicatorWidth := lipgloss.Width(indicator)
	if indicatorWidth >= width {
		return indicator
	}

	padding := width - indicatorWidth
	return lipgloss.NewStyle().
		PaddingLeft(padding).
		Render(indicator)
}
