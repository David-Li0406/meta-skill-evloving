package panels

import (
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tools"
)

func TestNewAccountsPanel(t *testing.T) {
	panel := NewAccountsPanel()
	if panel == nil {
		t.Fatal("NewAccountsPanel returned nil")
	}

	config := panel.Config()
	if config.ID != "accounts" {
		t.Errorf("Expected ID 'accounts', got %q", config.ID)
	}

	if config.Title != "Accounts" {
		t.Errorf("Expected Title 'Accounts', got %q", config.Title)
	}
}

func TestAccountsPanel_SetSize(t *testing.T) {
	panel := NewAccountsPanel()
	panel.SetSize(80, 24)

	if panel.Width() != 80 {
		t.Errorf("Expected Width 80, got %d", panel.Width())
	}

	if panel.Height() != 24 {
		t.Errorf("Expected Height 24, got %d", panel.Height())
	}
}

func TestAccountsPanel_FocusBlur(t *testing.T) {
	panel := NewAccountsPanel()

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

func TestAccountsPanel_SetData(t *testing.T) {
	panel := NewAccountsPanel()

	data := AccountsData{
		Status: &tools.CAAMStatus{
			Available:     true,
			Version:       "1.0.0",
			AccountsCount: 2,
			Providers:     []string{"claude", "openai"},
			Accounts: []tools.CAAMAccount{
				{ID: "acc1", Provider: "claude", Email: "user@example.com", Active: true},
				{ID: "acc2", Provider: "openai", Email: "other@example.com", Active: true},
			},
		},
		Available: true,
	}

	panel.SetData(data)

	if panel.data.Status == nil {
		t.Fatal("Expected Status to be set")
	}

	if panel.data.Status.AccountsCount != 2 {
		t.Errorf("Expected AccountsCount 2, got %d", panel.data.Status.AccountsCount)
	}

	if len(panel.data.Status.Accounts) != 2 {
		t.Errorf("Expected 2 accounts, got %d", len(panel.data.Status.Accounts))
	}
}

func TestAccountsPanel_HasError(t *testing.T) {
	panel := NewAccountsPanel()

	if panel.HasError() {
		t.Error("Panel should not have error initially")
	}

	panel.SetData(AccountsData{
		Error: &testError{msg: "test error"},
	})

	if !panel.HasError() {
		t.Error("Panel should have error after SetData with error")
	}
}

func TestAccountsPanel_Keybindings(t *testing.T) {
	panel := NewAccountsPanel()
	bindings := panel.Keybindings()

	if len(bindings) != 1 {
		t.Errorf("Expected 1 keybinding, got %d", len(bindings))
	}

	if bindings[0].Action != "refresh" {
		t.Errorf("Expected action 'refresh', got %q", bindings[0].Action)
	}
}

func TestAccountsPanel_View(t *testing.T) {
	panel := NewAccountsPanel()
	panel.SetSize(60, 20)

	// Test empty view
	view := panel.View()
	if view == "" {
		t.Error("View should not be empty")
	}

	// Test view with data
	panel.SetData(AccountsData{
		Status: &tools.CAAMStatus{
			Available:     true,
			AccountsCount: 1,
			Providers:     []string{"claude"},
			Accounts: []tools.CAAMAccount{
				{ID: "acc1", Provider: "claude", Email: "user@example.com", Active: true},
			},
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

func TestAccountsPanel_ViewWithCooldown(t *testing.T) {
	panel := NewAccountsPanel()
	panel.SetSize(60, 20)

	// Test with rate-limited account
	panel.SetData(AccountsData{
		Status: &tools.CAAMStatus{
			Available:     true,
			AccountsCount: 2,
			Providers:     []string{"claude"},
			Accounts: []tools.CAAMAccount{
				{ID: "acc1", Provider: "claude", Email: "user1@example.com", Active: false, RateLimited: true, CooldownUntil: time.Now().Add(5 * time.Minute)},
				{ID: "acc2", Provider: "claude", Email: "user2@example.com", Active: true},
			},
		},
		Available: true,
	})

	view := panel.View()
	if view == "" {
		t.Error("View should not be empty for cooldown state")
	}
}

func TestAccountsPanel_ViewMultipleProviders(t *testing.T) {
	panel := NewAccountsPanel()
	panel.SetSize(60, 25)

	panel.SetData(AccountsData{
		Status: &tools.CAAMStatus{
			Available:     true,
			AccountsCount: 3,
			Providers:     []string{"claude", "openai", "gemini"},
			Accounts: []tools.CAAMAccount{
				{ID: "acc1", Provider: "claude", Email: "claude@example.com", Active: true},
				{ID: "acc2", Provider: "openai", Email: "openai@example.com", Active: true},
				{ID: "acc3", Provider: "gemini", Email: "gemini@example.com", Active: true},
			},
		},
		Available: true,
	})

	view := panel.View()
	if view == "" {
		t.Error("View should not be empty for multiple providers")
	}
}

func TestAccountsPanel_Init(t *testing.T) {
	panel := NewAccountsPanel()
	cmd := panel.Init()

	// Init should return nil (no initial command)
	if cmd != nil {
		t.Error("Init should return nil")
	}
}

func TestAccountsPanel_Update(t *testing.T) {
	panel := NewAccountsPanel()
	model, cmd := panel.Update(nil)

	if model != panel {
		t.Error("Update should return same panel")
	}

	if cmd != nil {
		t.Error("Update should return nil command")
	}
}

func TestAccountsData_Fields(t *testing.T) {
	data := AccountsData{
		Status: &tools.CAAMStatus{
			Available:     true,
			Version:       "2.0.0",
			AccountsCount: 5,
			Providers:     []string{"claude", "openai"},
		},
		Available: true,
		Error:     nil,
	}

	if !data.Available {
		t.Error("Expected Available to be true")
	}

	if data.Status.Version != "2.0.0" {
		t.Errorf("Expected Version '2.0.0', got %q", data.Status.Version)
	}

	if data.Status.AccountsCount != 5 {
		t.Errorf("Expected AccountsCount 5, got %d", data.Status.AccountsCount)
	}
}

func TestAccountsPanel_ViewErrorState(t *testing.T) {
	panel := NewAccountsPanel()
	panel.SetSize(60, 20)

	panel.SetData(AccountsData{
		Error: &testError{msg: "connection failed"},
	})

	view := panel.View()
	if view == "" {
		t.Error("View should not be empty for error state")
	}
}
