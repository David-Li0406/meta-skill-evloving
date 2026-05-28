package panels

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/key"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tools"
	"github.com/Dicklesworthstone/ntm/internal/tui/components"
	"github.com/Dicklesworthstone/ntm/internal/tui/styles"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// AccountsData holds the data for the accounts panel
type AccountsData struct {
	Status    *tools.CAAMStatus
	Available bool
	Error     error
}

// AccountsPanel displays CAAM account status and switching information
type AccountsPanel struct {
	PanelBase
	data    AccountsData
	theme   theme.Theme
	adapter *tools.CAAMAdapter
}

// accountsConfig returns the configuration for the accounts panel
func accountsConfig() PanelConfig {
	return PanelConfig{
		ID:              "accounts",
		Title:           "Accounts",
		Priority:        PriorityNormal,
		RefreshInterval: 30 * time.Second,
		MinWidth:        30,
		MinHeight:       6,
		Collapsible:     true,
	}
}

// NewAccountsPanel creates a new accounts panel
func NewAccountsPanel() *AccountsPanel {
	return &AccountsPanel{
		PanelBase: NewPanelBase(accountsConfig()),
		theme:     theme.Current(),
		adapter:   tools.NewCAAMAdapter(),
	}
}

// Init implements tea.Model
func (a *AccountsPanel) Init() tea.Cmd {
	return nil
}

// Update implements tea.Model
func (a *AccountsPanel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return a, nil
}

// Refresh fetches the latest data from CAAM
func (a *AccountsPanel) Refresh() {
	if a.adapter == nil {
		a.data = AccountsData{Available: false}
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := a.adapter.GetStatus(ctx)
	if err != nil {
		a.data = AccountsData{
			Available: false,
			Error:     err,
		}
		return
	}

	a.data = AccountsData{
		Status:    status,
		Available: status != nil && status.Available,
		Error:     nil,
	}

	a.SetLastUpdate(time.Now())
}

// SetData updates the panel data directly
func (a *AccountsPanel) SetData(data AccountsData) {
	a.data = data
	if data.Error == nil {
		a.SetLastUpdate(time.Now())
	}
}

// HasError returns true if there's an active error
func (a *AccountsPanel) HasError() bool {
	return a.data.Error != nil
}

// Keybindings returns accounts panel specific shortcuts
func (a *AccountsPanel) Keybindings() []Keybinding {
	return []Keybinding{
		{
			Key:         key.NewBinding(key.WithKeys("r"), key.WithHelp("r", "refresh")),
			Description: "Refresh account data",
			Action:      "refresh",
		},
	}
}

// View renders the panel
func (a *AccountsPanel) View() string {
	t := a.theme
	w, h := a.Width(), a.Height()

	// Create border style based on focus
	borderColor := t.Surface1
	bgColor := t.Base
	if a.IsFocused() {
		borderColor = t.Primary
		bgColor = t.Surface0
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
	title := a.Config().Title
	if a.data.Error != nil {
		errorBadge := lipgloss.NewStyle().
			Background(t.Red).
			Foreground(t.Base).
			Bold(true).
			Padding(0, 1).
			Render("!")
		title = title + " " + errorBadge
	} else if staleBadge := components.RenderStaleBadge(a.LastUpdate(), a.Config().RefreshInterval); staleBadge != "" {
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
	if a.data.Error != nil {
		content.WriteString(components.ErrorState(a.data.Error.Error(), "Press r to retry", w-4) + "\n")
		return boxStyle.Render(FitToHeight(content.String(), h-4))
	}

	// Empty state: CAAM not available
	if !a.data.Available || a.data.Status == nil {
		content.WriteString("\n" + components.RenderEmptyState(components.EmptyStateOptions{
			Icon:        components.IconWaiting,
			Title:       "No accounts",
			Description: "CAAM not available",
			Width:       w - 4,
			Centered:    true,
		}))
		return boxStyle.Render(FitToHeight(content.String(), h-4))
	}

	content.WriteString("\n")

	status := a.data.Status

	// Summary line
	countLabel := fmt.Sprintf("%d account", status.AccountsCount)
	if status.AccountsCount != 1 {
		countLabel += "s"
	}
	if len(status.Providers) > 0 {
		countLabel += fmt.Sprintf(" (%d providers)", len(status.Providers))
	}
	content.WriteString(lipgloss.NewStyle().Foreground(t.Subtext).Render(countLabel) + "\n")
	content.WriteString("\n")

	// Per-provider account display
	availHeight := h - 10
	if availHeight < 2 {
		availHeight = 2
	}

	// Group accounts by provider
	providerAccounts := make(map[string][]tools.CAAMAccount)
	for _, acc := range status.Accounts {
		providerAccounts[acc.Provider] = append(providerAccounts[acc.Provider], acc)
	}

	providerCount := 0
	for _, provider := range status.Providers {
		if providerCount >= availHeight {
			remaining := len(status.Providers) - providerCount
			if remaining > 0 {
				content.WriteString(lipgloss.NewStyle().Foreground(t.Overlay).Render(fmt.Sprintf("+%d more", remaining)) + "\n")
			}
			break
		}

		accounts := providerAccounts[provider]
		if len(accounts) == 0 {
			continue
		}

		// Provider color
		var providerColor lipgloss.Color
		switch strings.ToLower(provider) {
		case "claude", "anthropic":
			providerColor = t.Claude
		case "openai", "gpt", "codex":
			providerColor = t.Codex
		case "gemini", "google":
			providerColor = t.Gemini
		default:
			providerColor = t.Green
		}

		providerName := lipgloss.NewStyle().Foreground(providerColor).Bold(true).Render(provider)

		// Find active account for this provider
		var activeAcc *tools.CAAMAccount
		var cooldownCount int
		for i := range accounts {
			if accounts[i].Active {
				activeAcc = &accounts[i]
			}
			if accounts[i].RateLimited {
				cooldownCount++
			}
		}

		// Account info
		var accountInfo string
		if activeAcc != nil {
			email := activeAcc.Email
			if email == "" {
				email = activeAcc.Name
			}
			if email == "" {
				email = activeAcc.ID
			}
			// Truncate email if too long
			maxEmailLen := w - 15 - lipgloss.Width(provider)
			if maxEmailLen > 0 && len(email) > maxEmailLen {
				email = email[:maxEmailLen-3] + "..."
			}
			accountInfo = lipgloss.NewStyle().Foreground(t.Text).Render(email)
		} else {
			accountInfo = lipgloss.NewStyle().Foreground(t.Overlay).Render("(none active)")
		}

		// Status indicator
		statusStr := ""
		if cooldownCount > 0 {
			statusStr = lipgloss.NewStyle().Foreground(t.Yellow).Render(fmt.Sprintf(" [%d cooldown]", cooldownCount))
		}

		// Build the line
		gap := w - 6 - lipgloss.Width(providerName) - lipgloss.Width(accountInfo) - lipgloss.Width(statusStr)
		if gap < 1 {
			gap = 1
		}

		line := providerName + strings.Repeat(" ", gap) + accountInfo + statusStr
		content.WriteString(line + "\n")

		// Show usage bar if we have usage info
		if activeAcc != nil && !activeAcc.RateLimited {
			// Calculate a simple "health" indicator based on whether rate limited
			barColor := string(t.Green)
			barLabel := "ready"
			barPct := 0.1 // Small bar to show account is available

			bar := styles.ProgressBar(barPct, w-8, "█", "░", barColor)
			barLine := lipgloss.NewStyle().Foreground(t.Overlay).Render("  " + barLabel + " ")
			content.WriteString(barLine + bar + "\n")
		} else if activeAcc != nil && activeAcc.RateLimited {
			// Rate limited indicator
			barColor := string(t.Yellow)
			bar := styles.ProgressBar(0.0, w-8, "█", "░", barColor)
			cooldownLabel := "cooldown"
			if !activeAcc.CooldownUntil.IsZero() {
				remaining := time.Until(activeAcc.CooldownUntil)
				if remaining > 0 {
					cooldownLabel = fmt.Sprintf("~%dm", int(remaining.Minutes())+1)
				}
			}
			barLine := lipgloss.NewStyle().Foreground(t.Yellow).Render("  " + cooldownLabel + " ")
			content.WriteString(barLine + bar + "\n")
		}

		providerCount++
	}

	// Add freshness indicator at the bottom
	if footer := components.RenderFreshnessFooter(components.FreshnessOptions{
		LastUpdate:      a.LastUpdate(),
		RefreshInterval: a.Config().RefreshInterval,
		Width:           w - 4,
	}); footer != "" {
		content.WriteString(footer + "\n")
	}

	return boxStyle.Render(FitToHeight(content.String(), h-4))
}
