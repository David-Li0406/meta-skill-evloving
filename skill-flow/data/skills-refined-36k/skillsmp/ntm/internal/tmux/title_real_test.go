//go:build integration

package tmux

import (
	"fmt"
	"testing"
	"time"
)

// =============================================================================
// Title Real Integration Tests (ntm-s219)
//
// These tests verify title parsing and agent detection using real tmux panes.
// Run with: go test -tags=integration ./internal/tmux/...
// =============================================================================

// createTestSessionForTitle creates a unique test session for title tests
func createTestSessionForTitle(t *testing.T) string {
	t.Helper()
	name := uniqueSessionName("title")
	t.Cleanup(func() { cleanupSession(t, name) })

	err := CreateSession(name, t.TempDir())
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)
	return name
}

// =============================================================================
// Title Parsing Tests
// =============================================================================

func TestRealTitleParsingAgentFormat(t *testing.T) {
	skipIfNoTmux(t)

	// Test parsing of various agent title formats
	testCases := []struct {
		title       string
		wantType    AgentType
		wantVariant string
	}{
		{"myproject__cc_1", AgentClaude, ""},
		{"myproject__cc_2", AgentClaude, ""},
		{"myproject__cod_1", AgentCodex, ""},
		{"myproject__gmi_1", AgentGemini, ""},
		{"myproject__cc_1_opus", AgentClaude, "opus"},
		{"myproject__cc_2_sonnet", AgentClaude, "sonnet"},
		{"myproject__cod_1_o1", AgentCodex, "o1"},
		{"myproject__gmi_1_flash", AgentGemini, "flash"},
		{"myproject__user_1", AgentUser, ""},
		{"zsh", AgentUser, ""},
		{"bash", AgentUser, ""},
	}

	for _, tc := range testCases {
		t.Run(tc.title, func(t *testing.T) {
			gotType, gotVariant, _ := parseAgentFromTitle(tc.title)
			if gotType != tc.wantType {
				t.Errorf("parseAgentFromTitle(%q) type = %v, want %v", tc.title, gotType, tc.wantType)
			}
			if gotVariant != tc.wantVariant {
				t.Errorf("parseAgentFromTitle(%q) variant = %q, want %q", tc.title, gotVariant, tc.wantVariant)
			}
		})
	}
}

func TestRealTitleParsingWithTags(t *testing.T) {
	skipIfNoTmux(t)

	testCases := []struct {
		title    string
		wantTags []string
	}{
		{"myproject__cc_1[tag1,tag2]", []string{"tag1", "tag2"}},
		{"myproject__cc_1_opus[arch,review]", []string{"arch", "review"}},
		{"myproject__cc_1[]", nil},
		{"myproject__cc_1", nil},
	}

	for _, tc := range testCases {
		t.Run(tc.title, func(t *testing.T) {
			_, _, gotTags := parseAgentFromTitle(tc.title)
			if len(gotTags) != len(tc.wantTags) {
				t.Errorf("parseAgentFromTitle(%q) tags len = %d, want %d", tc.title, len(gotTags), len(tc.wantTags))
				return
			}
			for i, tag := range tc.wantTags {
				if gotTags[i] != tag {
					t.Errorf("parseAgentFromTitle(%q) tag[%d] = %q, want %q", tc.title, i, gotTags[i], tag)
				}
			}
		})
	}
}

// =============================================================================
// Title Setting Tests (Real tmux)
// =============================================================================

func TestRealTitleSetAndGet(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Set title
	title := "test__cc_1_opus"
	if err := SetPaneTitle(paneID, title); err != nil {
		t.Fatalf("SetPaneTitle failed: %v", err)
	}
	time.Sleep(100 * time.Millisecond)

	// Get panes and verify title
	panes, err := GetPanes(session)
	if err != nil {
		t.Fatalf("GetPanes failed: %v", err)
	}

	var foundTitle string
	for _, p := range panes {
		if p.ID == paneID {
			foundTitle = p.Title
			break
		}
	}

	if foundTitle != title {
		t.Errorf("pane title = %q, want %q", foundTitle, title)
	}
}

func TestRealTitlePersistsAfterOperations(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Set initial title
	title := "persistent__cc_1"
	SetPaneTitle(paneID, title)
	time.Sleep(100 * time.Millisecond)

	// Perform some operations
	SendKeys(paneID, "echo test1", true)
	time.Sleep(200 * time.Millisecond)
	SendKeys(paneID, "echo test2", true)
	time.Sleep(200 * time.Millisecond)

	// Verify title still set
	panes, _ = GetPanes(session)
	for _, p := range panes {
		if p.ID == paneID {
			if p.Title != title {
				t.Errorf("title changed after operations: got %q, want %q", p.Title, title)
			}
			break
		}
	}
}

func TestRealTitleWithVariants(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Test various variant suffixes
	variants := []string{
		"proj__cc_1_opus",
		"proj__cc_1_sonnet",
		"proj__cod_1_gpt4",
		"proj__gmi_1_pro",
	}

	for _, title := range variants {
		t.Run(title, func(t *testing.T) {
			SetPaneTitle(paneID, title)
			time.Sleep(100 * time.Millisecond)

			panes, _ := GetPanes(session)
			for _, p := range panes {
				if p.ID == paneID {
					if p.Title != title {
						t.Errorf("title = %q, want %q", p.Title, title)
					}
					// Verify variant is parsed correctly
					if p.Variant == "" && title != "proj__cc_1" {
						// Check parseAgentFromTitle
						_, variant, _ := parseAgentFromTitle(title)
						if variant == "" {
							t.Errorf("variant should be parsed from %q", title)
						}
					}
					break
				}
			}
		})
	}
}

// =============================================================================
// Agent Detection Tests (Real tmux)
// =============================================================================

func TestRealAgentDetectionFromTitle(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Set various titles and verify agent type detection
	testCases := []struct {
		title    string
		wantType AgentType
	}{
		{"myproj__cc_1", AgentClaude},
		{"myproj__cod_1", AgentCodex},
		{"myproj__gmi_1", AgentGemini},
		{"bash", AgentUser},
		{"zsh", AgentUser},
	}

	for _, tc := range testCases {
		t.Run(tc.title, func(t *testing.T) {
			SetPaneTitle(paneID, tc.title)
			time.Sleep(100 * time.Millisecond)

			panes, _ := GetPanes(session)
			for _, p := range panes {
				if p.ID == paneID {
					if p.Type != tc.wantType {
						t.Errorf("agent type = %v, want %v for title %q", p.Type, tc.wantType, tc.title)
					}
					break
				}
			}
		})
	}
}

func TestRealAgentDetectionWithVariants(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Test detection with variant suffixes
	testCases := []struct {
		title       string
		wantType    AgentType
		wantVariant string
	}{
		{"proj__cc_1_opus", AgentClaude, "opus"},
		{"proj__cc_2_sonnet", AgentClaude, "sonnet"},
		{"proj__cod_1_gpt4", AgentCodex, "gpt4"},
		{"proj__gmi_1_flash", AgentGemini, "flash"},
	}

	for _, tc := range testCases {
		t.Run(tc.title, func(t *testing.T) {
			SetPaneTitle(paneID, tc.title)
			time.Sleep(100 * time.Millisecond)

			panes, _ := GetPanes(session)
			for _, p := range panes {
				if p.ID == paneID {
					if p.Type != tc.wantType {
						t.Errorf("type = %v, want %v", p.Type, tc.wantType)
					}
					if p.Variant != tc.wantVariant {
						t.Errorf("variant = %q, want %q", p.Variant, tc.wantVariant)
					}
					break
				}
			}
		})
	}
}

// =============================================================================
// Edge Cases
// =============================================================================

func TestRealTitleExtraUnderscores(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Test titles with extra underscores
	testCases := []struct {
		title    string
		wantType AgentType
	}{
		{"my_project__cc_1", AgentClaude},
		{"my__project__cc_1", AgentClaude},
		{"a_b_c__cc_1", AgentClaude},
	}

	for _, tc := range testCases {
		t.Run(tc.title, func(t *testing.T) {
			SetPaneTitle(paneID, tc.title)
			time.Sleep(100 * time.Millisecond)

			panes, _ := GetPanes(session)
			for _, p := range panes {
				if p.ID == paneID {
					if p.Type != tc.wantType {
						t.Errorf("type = %v, want %v for title %q", p.Type, tc.wantType, tc.title)
					}
					break
				}
			}
		})
	}
}

func TestRealTitleManuallySet(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Set a non-agent title
	title := "my custom title"
	SetPaneTitle(paneID, title)
	time.Sleep(100 * time.Millisecond)

	panes, _ = GetPanes(session)
	for _, p := range panes {
		if p.ID == paneID {
			// Should be treated as user pane
			if p.Type != AgentUser {
				t.Errorf("custom title should result in AgentUser, got %v", p.Type)
			}
			if p.Title != title {
				t.Errorf("title = %q, want %q", p.Title, title)
			}
			break
		}
	}
}

func TestRealTitleMultiplePanes(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	// Create additional panes
	for i := 0; i < 3; i++ {
		_, err := SplitWindow(session, t.TempDir())
		if err != nil {
			t.Fatalf("SplitWindow %d failed: %v", i, err)
		}
	}
	time.Sleep(200 * time.Millisecond)

	panes, _ := GetPanes(session)
	if len(panes) != 4 {
		t.Fatalf("expected 4 panes, got %d", len(panes))
	}

	// Set different agent titles for each pane
	titles := []struct {
		title    string
		wantType AgentType
	}{
		{"session__cc_1_opus", AgentClaude},
		{"session__cc_2_sonnet", AgentClaude},
		{"session__cod_1", AgentCodex},
		{"session__gmi_1", AgentGemini},
	}

	for i, p := range panes {
		SetPaneTitle(p.ID, titles[i].title)
	}
	time.Sleep(200 * time.Millisecond)

	// Verify each pane has correct type
	panes, _ = GetPanes(session)
	for i, p := range panes {
		if p.Type != titles[i].wantType {
			t.Errorf("pane %d: type = %v, want %v", i, p.Type, titles[i].wantType)
		}
	}

	// Count agent types
	counts := make(map[AgentType]int)
	for _, p := range panes {
		counts[p.Type]++
	}

	if counts[AgentClaude] != 2 {
		t.Errorf("claude count = %d, want 2", counts[AgentClaude])
	}
	if counts[AgentCodex] != 1 {
		t.Errorf("codex count = %d, want 1", counts[AgentCodex])
	}
	if counts[AgentGemini] != 1 {
		t.Errorf("gemini count = %d, want 1", counts[AgentGemini])
	}
}

func TestRealTitleEmpty(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	panes, _ := GetPanes(session)
	paneID := panes[0].ID

	// Try to set empty title
	SetPaneTitle(paneID, "")
	time.Sleep(100 * time.Millisecond)

	panes, _ = GetPanes(session)
	for _, p := range panes {
		if p.ID == paneID {
			// Empty title should result in AgentUser (fallback)
			if p.Type != AgentUser {
				t.Errorf("empty title should result in AgentUser, got %v", p.Type)
			}
			break
		}
	}
}

func TestRealTitleAgentTypeConstants(t *testing.T) {
	// Verify AgentType constants are distinct
	types := []AgentType{AgentClaude, AgentCodex, AgentGemini, AgentUser}
	seen := make(map[AgentType]bool)
	for _, at := range types {
		if seen[at] {
			t.Errorf("duplicate AgentType value")
		}
		seen[at] = true
	}
}

func TestRealTitleIndexParsing(t *testing.T) {
	skipIfNoTmux(t)

	session := createTestSessionForTitle(t)

	// Create 3 panes and set sequential titles
	for i := 0; i < 2; i++ {
		_, err := SplitWindow(session, t.TempDir())
		if err != nil {
			t.Fatalf("SplitWindow %d failed: %v", i, err)
		}
	}
	time.Sleep(200 * time.Millisecond)

	panes, _ := GetPanes(session)
	for i, p := range panes {
		title := fmt.Sprintf("proj__cc_%d", i+1)
		SetPaneTitle(p.ID, title)
	}
	time.Sleep(200 * time.Millisecond)

	// Verify all are detected as Claude
	panes, _ = GetPanes(session)
	for _, p := range panes {
		if p.Type != AgentClaude {
			t.Errorf("pane with cc title should be AgentClaude, got %v", p.Type)
		}
	}
}
