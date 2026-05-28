package panels

import (
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tools"
)

func TestNewQuotaPanel(t *testing.T) {
	panel := NewQuotaPanel()
	if panel == nil {
		t.Fatal("NewQuotaPanel returned nil")
	}

	config := panel.Config()
	if config.ID != "quota" {
		t.Errorf("Expected ID 'quota', got %q", config.ID)
	}

	if config.Title != "Usage & Costs" {
		t.Errorf("Expected Title 'Usage & Costs', got %q", config.Title)
	}
}

func TestQuotaPanel_SetSize(t *testing.T) {
	panel := NewQuotaPanel()
	panel.SetSize(80, 24)

	if panel.Width() != 80 {
		t.Errorf("Expected Width 80, got %d", panel.Width())
	}

	if panel.Height() != 24 {
		t.Errorf("Expected Height 24, got %d", panel.Height())
	}
}

func TestQuotaPanel_FocusBlur(t *testing.T) {
	panel := NewQuotaPanel()

	if panel.IsFocused() {
		t.Error("Panel should not be focused initially")
	}

	panel.Focus()
	if !panel.IsFocused() {
		t.Error("Panel should be focused after Focus()")
	}

	panel.Blur()
	if panel.IsFocused() {
		t.Error("Panel should not be focused after Blur()")
	}
}

func TestQuotaPanel_SetData(t *testing.T) {
	panel := NewQuotaPanel()

	data := QuotaData{
		Status: &tools.CautStatus{
			Running:       true,
			ProviderCount: 2,
			TotalSpend:    50.00,
			QuotaPercent:  45.0,
		},
		Usages: []tools.CautUsage{
			{Provider: "claude", Cost: 30.00, TokensIn: 100000, TokensOut: 50000},
			{Provider: "openai", Cost: 20.00, TokensIn: 80000, TokensOut: 40000},
		},
		Available: true,
	}

	panel.SetData(data)

	if panel.data.Status == nil {
		t.Fatal("Expected Status to be set")
	}

	if panel.data.Status.QuotaPercent != 45.0 {
		t.Errorf("Expected QuotaPercent 45.0, got %f", panel.data.Status.QuotaPercent)
	}

	if len(panel.data.Usages) != 2 {
		t.Errorf("Expected 2 usages, got %d", len(panel.data.Usages))
	}
}

func TestQuotaPanel_HasError(t *testing.T) {
	panel := NewQuotaPanel()

	if panel.HasError() {
		t.Error("Panel should not have error initially")
	}

	panel.SetData(QuotaData{
		Error: &testError{msg: "test error"},
	})

	if !panel.HasError() {
		t.Error("Panel should have error after SetData with error")
	}
}

type testError struct {
	msg string
}

func (e *testError) Error() string {
	return e.msg
}

func TestQuotaPanel_Keybindings(t *testing.T) {
	panel := NewQuotaPanel()
	bindings := panel.Keybindings()

	if len(bindings) != 1 {
		t.Errorf("Expected 1 keybinding, got %d", len(bindings))
	}

	if bindings[0].Action != "refresh" {
		t.Errorf("Expected action 'refresh', got %q", bindings[0].Action)
	}
}

func TestQuotaPanel_View(t *testing.T) {
	panel := NewQuotaPanel()
	panel.SetSize(60, 20)

	// Test empty view
	view := panel.View()
	if view == "" {
		t.Error("View should not be empty")
	}

	// Test view with data
	panel.SetData(QuotaData{
		Status: &tools.CautStatus{
			Running:       true,
			ProviderCount: 1,
			TotalSpend:    25.00,
			QuotaPercent:  75.0,
		},
		Usages: []tools.CautUsage{
			{Provider: "claude", Cost: 25.00, TokensIn: 50000, TokensOut: 25000},
		},
		Available: true,
	})

	viewWithData := panel.View()
	if viewWithData == "" {
		t.Error("View with data should not be empty")
	}

	// View with data should be different from empty view
	if view == viewWithData {
		t.Error("View with data should differ from empty view")
	}
}

func TestQuotaPanel_ViewWarning(t *testing.T) {
	panel := NewQuotaPanel()
	panel.SetSize(60, 20)

	// Test warning state (80-95%)
	panel.SetData(QuotaData{
		Status: &tools.CautStatus{
			QuotaPercent: 85.0,
		},
		Available: true,
	})

	view := panel.View()
	// Should contain warning indicator (yellow styling would be applied)
	if view == "" {
		t.Error("View should not be empty for warning state")
	}
}

func TestQuotaPanel_ViewCritical(t *testing.T) {
	panel := NewQuotaPanel()
	panel.SetSize(60, 20)

	// Test critical state (>=95%)
	panel.SetData(QuotaData{
		Status: &tools.CautStatus{
			QuotaPercent: 97.0,
		},
		Available: true,
	})

	view := panel.View()
	// Should contain critical indicator (red styling would be applied)
	if view == "" {
		t.Error("View should not be empty for critical state")
	}
}

func TestQuotaPanel_Init(t *testing.T) {
	panel := NewQuotaPanel()
	cmd := panel.Init()

	// Init should return nil (no initial command)
	if cmd != nil {
		t.Error("Init should return nil")
	}
}

func TestQuotaPanel_Update(t *testing.T) {
	panel := NewQuotaPanel()
	model, cmd := panel.Update(nil)

	if model != panel {
		t.Error("Update should return same panel")
	}

	if cmd != nil {
		t.Error("Update should return nil command")
	}
}
