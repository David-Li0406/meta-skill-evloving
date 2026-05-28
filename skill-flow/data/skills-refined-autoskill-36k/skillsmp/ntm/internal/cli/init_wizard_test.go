package cli

import (
	"testing"

	tea "github.com/charmbracelet/bubbletea"
)

func TestInitWizardModel_Init(t *testing.T) {
	m := NewInitWizard()

	// Verify initial state
	if m.step != StepProjectType {
		t.Errorf("expected step %d, got %d", StepProjectType, m.step)
	}
	if m.cursor != 0 {
		t.Errorf("expected cursor 0, got %d", m.cursor)
	}

	// Verify default result values
	if m.result.AgentCount != 3 {
		t.Errorf("expected agent count 3, got %d", m.result.AgentCount)
	}
	if !m.result.EnableAgentMail {
		t.Error("expected Agent Mail enabled by default")
	}
	if !m.result.EnableCASS {
		t.Error("expected CASS enabled by default")
	}
	if !m.result.EnableCM {
		t.Error("expected CM enabled by default")
	}
}

func TestInitWizardModel_ProjectTypeNavigation(t *testing.T) {
	m := NewInitWizard()

	// Navigate down
	newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeyDown})
	m = newModel.(InitWizardModel)
	if m.cursor != 1 {
		t.Errorf("expected cursor 1 after down, got %d", m.cursor)
	}

	// Navigate up
	newModel, _ = m.Update(tea.KeyMsg{Type: tea.KeyUp})
	m = newModel.(InitWizardModel)
	if m.cursor != 0 {
		t.Errorf("expected cursor 0 after up, got %d", m.cursor)
	}

	// Select project type (enter)
	newModel, _ = m.Update(tea.KeyMsg{Type: tea.KeyEnter})
	m = newModel.(InitWizardModel)
	if m.step != StepAgentCount {
		t.Errorf("expected step %d after enter, got %d", StepAgentCount, m.step)
	}
	if m.result.ProjectType != ProjectGo {
		t.Errorf("expected project type %d, got %d", ProjectGo, m.result.ProjectType)
	}
}

func TestInitWizardModel_Cancel(t *testing.T) {
	m := NewInitWizard()

	// Cancel with q
	newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("q")})
	m = newModel.(InitWizardModel)
	if !m.result.Cancelled {
		t.Error("expected cancelled after 'q'")
	}
	if m.step != StepDone {
		t.Errorf("expected step %d after cancel, got %d", StepDone, m.step)
	}
}

func TestInitWizardModel_EscapeGoesBack(t *testing.T) {
	m := NewInitWizard()

	// Go to step 2
	newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeyEnter})
	m = newModel.(InitWizardModel)
	if m.step != StepAgentCount {
		t.Fatalf("expected step %d, got %d", StepAgentCount, m.step)
	}

	// Escape should go back
	newModel, _ = m.Update(tea.KeyMsg{Type: tea.KeyEsc})
	m = newModel.(InitWizardModel)
	if m.step != StepProjectType {
		t.Errorf("expected step %d after escape, got %d", StepProjectType, m.step)
	}
}

func TestInitWizardModel_IntegrationToggle(t *testing.T) {
	m := NewInitWizard()

	// Navigate to integrations step
	m.step = StepIntegrations
	m.cursor = 0 // Agent Mail

	// Toggle off
	newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeySpace})
	m = newModel.(InitWizardModel)
	if m.result.EnableAgentMail {
		t.Error("expected Agent Mail disabled after toggle")
	}

	// Toggle on
	newModel, _ = m.Update(tea.KeyMsg{Type: tea.KeySpace})
	m = newModel.(InitWizardModel)
	if !m.result.EnableAgentMail {
		t.Error("expected Agent Mail enabled after second toggle")
	}
}

func TestProjectTypeString(t *testing.T) {
	tests := []struct {
		pt   ProjectType
		want string
	}{
		{ProjectGo, "Go"},
		{ProjectPython, "Python"},
		{ProjectNode, "Node.js"},
		{ProjectRust, "Rust"},
		{ProjectOther, "Other"},
	}

	for _, tt := range tests {
		got := tt.pt.String()
		if got != tt.want {
			t.Errorf("ProjectType(%d).String() = %q, want %q", tt.pt, got, tt.want)
		}
	}
}

func TestInitWizardModel_View(t *testing.T) {
	m := NewInitWizard()

	// View should not panic at any step
	steps := []WizardStep{StepProjectType, StepAgentCount, StepIntegrations, StepConfirm}
	for _, step := range steps {
		m.step = step
		view := m.View()
		if view == "" {
			t.Errorf("View() returned empty for step %d", step)
		}
	}
}

func TestInitWizardModel_ClampCursor(t *testing.T) {
	m := NewInitWizard()

	// Project type step has 5 options (0-4)
	m.step = StepProjectType
	m.cursor = 10
	got := m.clampCursor()
	if got != 4 {
		t.Errorf("clampCursor() at StepProjectType with cursor 10 = %d, want 4", got)
	}

	// Confirm step has 2 options (0-1)
	m.step = StepConfirm
	m.cursor = 5
	got = m.clampCursor()
	if got != 1 {
		t.Errorf("clampCursor() at StepConfirm with cursor 5 = %d, want 1", got)
	}
}
