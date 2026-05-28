// Package components provides shared TUI building blocks.
package components

import (
	"fmt"
	"time"

	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// FreshnessOptions configures freshness indicator rendering.
type FreshnessOptions struct {
	LastUpdate      time.Time     // When data was last fetched
	RefreshInterval time.Duration // Expected refresh interval (for staleness detection)
	Width           int           // Available width for rendering
	ShowBadge       bool          // Show "STALE" badge when data is stale
}

// IsStale returns true if data is older than 2x the refresh interval.
func IsStale(lastUpdate time.Time, refreshInterval time.Duration) bool {
	if lastUpdate.IsZero() || refreshInterval <= 0 {
		return false
	}
	return time.Since(lastUpdate) > 2*refreshInterval
}

// RenderFreshnessIndicator renders a "Updated Xs ago" indicator.
// Returns empty string if lastUpdate is zero.
func RenderFreshnessIndicator(opts FreshnessOptions) string {
	if opts.LastUpdate.IsZero() {
		return ""
	}

	t := theme.Current()
	elapsed := time.Since(opts.LastUpdate)

	// Format the age string
	ageStr := formatDuration(elapsed)

	// Determine style based on staleness
	stale := IsStale(opts.LastUpdate, opts.RefreshInterval)

	textStyle := lipgloss.NewStyle().Foreground(t.Overlay)
	if stale {
		textStyle = lipgloss.NewStyle().Foreground(t.Yellow)
	}

	return textStyle.Render(fmt.Sprintf("Updated %s ago", ageStr))
}

// RenderStaleBadge renders a "STALE" warning badge if data is stale.
// Returns empty string if not stale.
func RenderStaleBadge(lastUpdate time.Time, refreshInterval time.Duration) string {
	if !IsStale(lastUpdate, refreshInterval) {
		return ""
	}

	t := theme.Current()
	return lipgloss.NewStyle().
		Background(t.Yellow).
		Foreground(t.Base).
		Bold(true).
		Padding(0, 1).
		Render("STALE")
}

// RenderFreshnessFooter renders a right-aligned freshness footer.
func RenderFreshnessFooter(opts FreshnessOptions) string {
	indicator := RenderFreshnessIndicator(opts)
	if indicator == "" {
		return ""
	}

	indicatorWidth := lipgloss.Width(indicator)
	if indicatorWidth >= opts.Width {
		return indicator
	}

	// Right-align
	padding := opts.Width - indicatorWidth
	return lipgloss.NewStyle().
		PaddingLeft(padding).
		Render(indicator)
}

// formatDuration returns a human-readable duration string.
func formatDuration(d time.Duration) string {
	switch {
	case d < time.Second:
		return "now"
	case d < time.Minute:
		return fmt.Sprintf("%ds", int(d.Seconds()))
	case d < time.Hour:
		return fmt.Sprintf("%dm", int(d.Minutes()))
	case d < 24*time.Hour:
		return fmt.Sprintf("%dh", int(d.Hours()))
	default:
		return fmt.Sprintf("%dd", int(d.Hours()/24))
	}
}
