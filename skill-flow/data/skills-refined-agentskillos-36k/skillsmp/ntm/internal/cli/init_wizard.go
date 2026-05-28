package cli

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// WizardStep represents the current step in the init wizard
type WizardStep int

const (
	StepProjectType WizardStep = iota
	StepAgentCount
	StepIntegrations
	StepConfirm
	StepDone
)

// ProjectType represents the type of project being initialized
type ProjectType int

const (
	ProjectGo ProjectType = iota
	ProjectPython
	ProjectNode
	ProjectRust
	ProjectOther
)

func (p ProjectType) String() string {
	switch p {
	case ProjectGo:
		return "Go"
	case ProjectPython:
		return "Python"
	case ProjectNode:
		return "Node.js"
	case ProjectRust:
		return "Rust"
	default:
		return "Other"
	}
}

// WizardResult contains the wizard configuration choices
type WizardResult struct {
	ProjectType     ProjectType
	AgentCount      int
	EnableAgentMail bool
	EnableCASS      bool
	EnableCM        bool
	AutoFileReserve bool
	Cancelled       bool
}

// InitWizardModel is the Bubble Tea model for the init wizard
type InitWizardModel struct {
	step       WizardStep
	width      int
	height     int
	cursor     int
	result     WizardResult
	agentInput textinput.Model
	theme      theme.Theme
	err        error
}

// NewInitWizard creates a new init wizard model
func NewInitWizard() InitWizardModel {
	ti := textinput.New()
	ti.Placeholder = "3"
	ti.Focus()
	ti.CharLimit = 2
	ti.Width = 5
	ti.SetValue("3")

	return InitWizardModel{
		step:       StepProjectType,
		cursor:     0,
		agentInput: ti,
		theme:      theme.Current(),
		result: WizardResult{
			ProjectType:     ProjectGo,
			AgentCount:      3,
			EnableAgentMail: true,
			EnableCASS:      true,
			EnableCM:        true,
			AutoFileReserve: true,
		},
	}
}

// Init initializes the wizard model
func (m InitWizardModel) Init() tea.Cmd {
	return textinput.Blink
}

// Update handles messages for the wizard
func (m InitWizardModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			m.result.Cancelled = true
			m.step = StepDone
			return m, tea.Quit

		case "esc":
			if m.step > StepProjectType {
				m.step--
				m.cursor = 0
			} else {
				m.result.Cancelled = true
				m.step = StepDone
				return m, tea.Quit
			}

		case "enter":
			return m.handleEnter()

		case "up", "k":
			if m.step != StepAgentCount {
				if m.cursor > 0 {
					m.cursor--
				}
			}

		case "down", "j":
			if m.step != StepAgentCount {
				m.cursor++
				m.cursor = m.clampCursor()
			}

		case "tab", " ":
			if m.step == StepIntegrations {
				m.toggleIntegration()
			}
		}
	}

	// Update text input for agent count step
	if m.step == StepAgentCount {
		var cmd tea.Cmd
		m.agentInput, cmd = m.agentInput.Update(msg)
		return m, cmd
	}

	return m, nil
}

func (m InitWizardModel) handleEnter() (tea.Model, tea.Cmd) {
	switch m.step {
	case StepProjectType:
		m.result.ProjectType = ProjectType(m.cursor)
		m.step = StepAgentCount
		m.cursor = 0
		return m, textinput.Blink

	case StepAgentCount:
		count := 3
		if val := m.agentInput.Value(); val != "" {
			fmt.Sscanf(val, "%d", &count)
		}
		if count < 1 {
			count = 1
		}
		if count > 10 {
			count = 10
		}
		m.result.AgentCount = count
		m.step = StepIntegrations
		m.cursor = 0

	case StepIntegrations:
		if m.cursor == 4 { // "Continue" option
			m.step = StepConfirm
			m.cursor = 0
		} else {
			m.toggleIntegration()
		}

	case StepConfirm:
		if m.cursor == 0 { // Confirm
			m.step = StepDone
			return m, tea.Quit
		} else { // Go back
			m.step = StepProjectType
			m.cursor = 0
		}
	}
	return m, nil
}

func (m *InitWizardModel) toggleIntegration() {
	switch m.cursor {
	case 0:
		m.result.EnableAgentMail = !m.result.EnableAgentMail
	case 1:
		m.result.EnableCASS = !m.result.EnableCASS
	case 2:
		m.result.EnableCM = !m.result.EnableCM
	case 3:
		m.result.AutoFileReserve = !m.result.AutoFileReserve
	}
}

func (m InitWizardModel) clampCursor() int {
	var max int
	switch m.step {
	case StepProjectType:
		max = 4 // 5 project types
	case StepIntegrations:
		max = 4 // 4 toggles + continue
	case StepConfirm:
		max = 1 // confirm or go back
	default:
		max = 0
	}
	if m.cursor > max {
		return max
	}
	return m.cursor
}

// View renders the wizard
func (m InitWizardModel) View() string {
	t := m.theme

	// Styles
	titleStyle := lipgloss.NewStyle().
		Bold(true).
		Foreground(t.Blue).
		MarginBottom(1)

	subtitleStyle := lipgloss.NewStyle().
		Foreground(t.Subtext).
		MarginBottom(1)

	selectedStyle := lipgloss.NewStyle().
		Foreground(t.Green).
		Bold(true)

	normalStyle := lipgloss.NewStyle().
		Foreground(t.Text)

	checkStyle := lipgloss.NewStyle().
		Foreground(t.Green)

	uncheckStyle := lipgloss.NewStyle().
		Foreground(t.Surface1)

	hintStyle := lipgloss.NewStyle().
		Foreground(t.Subtext).
		Italic(true).
		MarginTop(1)

	// Build view
	var b strings.Builder

	// Header
	b.WriteString(titleStyle.Render("🚀 NTM Project Initialization"))
	b.WriteString("\n")
	b.WriteString(subtitleStyle.Render(m.stepDescription()))
	b.WriteString("\n\n")

	// Progress indicator
	b.WriteString(m.renderProgress())
	b.WriteString("\n\n")

	switch m.step {
	case StepProjectType:
		types := []string{"Go", "Python", "Node.js", "Rust", "Other"}
		for i, pt := range types {
			prefix := "  "
			style := normalStyle
			if i == m.cursor {
				prefix = "▶ "
				style = selectedStyle
			}
			b.WriteString(prefix + style.Render(pt) + "\n")
		}

	case StepAgentCount:
		b.WriteString("Number of agents: ")
		b.WriteString(m.agentInput.View())
		b.WriteString("\n\n")
		b.WriteString(hintStyle.Render("Enter a number between 1-10"))

	case StepIntegrations:
		integrations := []struct {
			name    string
			desc    string
			enabled bool
		}{
			{"Agent Mail", "Multi-agent coordination", m.result.EnableAgentMail},
			{"CASS", "Session memory & context", m.result.EnableCASS},
			{"CM", "Cognitive memory system", m.result.EnableCM},
			{"Auto File Reserve", "Prevent edit conflicts", m.result.AutoFileReserve},
		}

		for i, integ := range integrations {
			prefix := "  "
			style := normalStyle
			if i == m.cursor {
				prefix = "▶ "
				style = selectedStyle
			}
			check := uncheckStyle.Render("[ ]")
			if integ.enabled {
				check = checkStyle.Render("[✓]")
			}
			b.WriteString(fmt.Sprintf("%s%s %s  %s\n",
				prefix,
				check,
				style.Render(integ.name),
				lipgloss.NewStyle().Foreground(t.Subtext).Render(integ.desc),
			))
		}

		// Continue option
		prefix := "  "
		style := normalStyle
		if m.cursor == 4 {
			prefix = "▶ "
			style = selectedStyle
		}
		b.WriteString("\n" + prefix + style.Render("Continue →") + "\n")

	case StepConfirm:
		b.WriteString(m.renderSummary())
		b.WriteString("\n\n")

		options := []string{"✓ Confirm and Initialize", "← Go Back"}
		for i, opt := range options {
			prefix := "  "
			style := normalStyle
			if i == m.cursor {
				prefix = "▶ "
				style = selectedStyle
			}
			b.WriteString(prefix + style.Render(opt) + "\n")
		}
	}

	// Footer hints
	b.WriteString("\n")
	b.WriteString(hintStyle.Render(m.stepHint()))

	return lipgloss.NewStyle().Padding(1, 2).Render(b.String())
}

func (m InitWizardModel) stepDescription() string {
	switch m.step {
	case StepProjectType:
		return "Step 1/4: Select your project type"
	case StepAgentCount:
		return "Step 2/4: Configure agent count"
	case StepIntegrations:
		return "Step 3/4: Enable integrations (space to toggle)"
	case StepConfirm:
		return "Step 4/4: Review and confirm"
	default:
		return ""
	}
}

func (m InitWizardModel) stepHint() string {
	switch m.step {
	case StepProjectType:
		return "↑/↓ to move • enter to select • esc to cancel"
	case StepAgentCount:
		return "Type a number • enter to continue • esc to go back"
	case StepIntegrations:
		return "↑/↓ to move • space to toggle • enter on Continue • esc to go back"
	case StepConfirm:
		return "↑/↓ to move • enter to select • esc to go back"
	default:
		return ""
	}
}

func (m InitWizardModel) renderProgress() string {
	t := m.theme
	active := lipgloss.NewStyle().Foreground(t.Green).Render("●")
	inactive := lipgloss.NewStyle().Foreground(t.Surface1).Render("○")
	done := lipgloss.NewStyle().Foreground(t.Blue).Render("●")

	steps := []string{}
	for i := 0; i < 4; i++ {
		if i < int(m.step) {
			steps = append(steps, done)
		} else if i == int(m.step) {
			steps = append(steps, active)
		} else {
			steps = append(steps, inactive)
		}
	}
	return strings.Join(steps, " ─ ")
}

func (m InitWizardModel) renderSummary() string {
	t := m.theme

	labelStyle := lipgloss.NewStyle().Foreground(t.Subtext).Width(16)
	valueStyle := lipgloss.NewStyle().Foreground(t.Text).Bold(true)
	enabledStyle := lipgloss.NewStyle().Foreground(t.Green)
	disabledStyle := lipgloss.NewStyle().Foreground(t.Surface1)

	var b strings.Builder
	b.WriteString(lipgloss.NewStyle().Bold(true).Foreground(t.Blue).Render("Configuration Summary"))
	b.WriteString("\n\n")

	b.WriteString(labelStyle.Render("Project Type:"))
	b.WriteString(valueStyle.Render(m.result.ProjectType.String()))
	b.WriteString("\n")

	b.WriteString(labelStyle.Render("Agent Count:"))
	b.WriteString(valueStyle.Render(fmt.Sprintf("%d", m.result.AgentCount)))
	b.WriteString("\n\n")

	b.WriteString(labelStyle.Render("Integrations:"))
	b.WriteString("\n")

	integrations := []struct {
		name    string
		enabled bool
	}{
		{"  Agent Mail", m.result.EnableAgentMail},
		{"  CASS", m.result.EnableCASS},
		{"  CM", m.result.EnableCM},
		{"  Auto File Reserve", m.result.AutoFileReserve},
	}

	for _, integ := range integrations {
		style := disabledStyle
		status := "✗"
		if integ.enabled {
			style = enabledStyle
			status = "✓"
		}
		b.WriteString(style.Render(fmt.Sprintf("  %s %s", status, integ.name)))
		b.WriteString("\n")
	}

	return b.String()
}

// Result returns the wizard result
func (m InitWizardModel) Result() WizardResult {
	return m.result
}

// RunInitWizard runs the init wizard and returns the result
func RunInitWizard() (WizardResult, error) {
	model := NewInitWizard()
	p := tea.NewProgram(model)

	finalModel, err := p.Run()
	if err != nil {
		return WizardResult{Cancelled: true}, err
	}

	wizardModel, ok := finalModel.(InitWizardModel)
	if !ok {
		return WizardResult{Cancelled: true}, fmt.Errorf("unexpected model type")
	}

	return wizardModel.Result(), nil
}
