package dashboard

import (
	"errors"
	"strings"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/status"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/layout"
)

func TestStatusUpdateSetsPaneStateAndTimestamp(t *testing.T) {
	t.Parallel()

	m := New("session", "")
	m.panes = []tmux.Pane{
		{ID: "%1", Index: 0, Title: "session__cod_1", Type: tmux.AgentCodex},
	}
	m.paneStatus[0] = PaneStatus{}

	now := time.Now()
	msg := StatusUpdateMsg{
		Statuses: []status.AgentStatus{
			{PaneID: "%1", State: status.StateIdle, UpdatedAt: now},
		},
		Time: now,
	}

	updated, _ := m.Update(msg)
	m2 := updated.(Model)

	if got := m2.paneStatus[0].State; got != "idle" {
		t.Fatalf("expected pane state idle, got %q", got)
	}
	if m2.lastRefresh.IsZero() {
		t.Fatalf("expected lastRefresh to be set")
	}
}

func TestViewShowsLoadingWhenSessionFetchInFlight(t *testing.T) {
	t.Parallel()

	m := New("session", "")
	m.width = 80
	m.height = 30
	m.tier = layout.TierForWidth(m.width)

	// Simulate initial load: no panes yet, fetch in flight.
	m.panes = nil
	m.err = nil
	m.fetchingSession = true
	m.lastPaneFetch = time.Now().Add(-750 * time.Millisecond)

	plain := status.StripANSI(m.View())
	if strings.Contains(plain, "No panes found") {
		t.Fatalf("expected loading state, got empty state")
	}
	if !strings.Contains(plain, "Fetching panes") {
		t.Fatalf("expected loading copy to mention fetching panes")
	}
}

func TestViewRendersPanesEvenWhenLastSessionFetchErrored(t *testing.T) {
	t.Parallel()

	m := New("session", "")
	m.width = 120
	m.height = 30
	m.tier = layout.TierForWidth(m.width)

	m.panes = []tmux.Pane{
		{ID: "%1", Index: 0, Title: "session__cod_1", Type: tmux.AgentCodex},
	}
	m.err = errors.New("tmux refresh failed")

	plain := status.StripANSI(m.View())
	if !strings.Contains(plain, "tmux refresh failed") {
		t.Fatalf("expected error to be surfaced in view")
	}
	if !strings.Contains(plain, "session__cod_1") {
		t.Fatalf("expected panes to still render when session fetch errors")
	}
}

func TestPlanPaneCaptures_PrioritizesSelectedAndNewActivity(t *testing.T) {
	t.Parallel()

	now := time.Now()
	panes := []tmux.PaneActivity{
		{Pane: tmux.Pane{ID: "%0", Index: 0, Type: tmux.AgentUser}, LastActivity: now},
		{Pane: tmux.Pane{ID: "%1", Index: 1, Type: tmux.AgentCodex}, LastActivity: now.Add(-10 * time.Second)},
		{Pane: tmux.Pane{ID: "%2", Index: 2, Type: tmux.AgentClaude}, LastActivity: now.Add(-1 * time.Second)},
		{Pane: tmux.Pane{ID: "%3", Index: 3, Type: tmux.AgentGemini}, LastActivity: now.Add(-5 * time.Second)},
	}

	lastCaptured := map[string]time.Time{
		"%1": now,                        // no new activity
		"%2": now,                        // selected, no new activity
		"%3": now.Add(-20 * time.Second), // new activity since last capture
	}

	plan := planPaneCaptures(panes, "%2", lastCaptured, 2, 0)
	if len(plan.Targets) != 2 {
		t.Fatalf("expected 2 capture targets, got %d", len(plan.Targets))
	}
	if plan.Targets[0].Pane.ID != "%2" {
		t.Fatalf("expected selected pane first, got %s", plan.Targets[0].Pane.ID)
	}
	if plan.Targets[1].Pane.ID != "%3" {
		t.Fatalf("expected pane with new activity second, got %s", plan.Targets[1].Pane.ID)
	}
}

func TestPlanPaneCaptures_RoundRobinAdvancesCursor(t *testing.T) {
	t.Parallel()

	now := time.Now()
	panes := []tmux.PaneActivity{
		{Pane: tmux.Pane{ID: "%1", Index: 1, Type: tmux.AgentCodex}, LastActivity: now.Add(-10 * time.Second)},
		{Pane: tmux.Pane{ID: "%2", Index: 2, Type: tmux.AgentClaude}, LastActivity: now.Add(-10 * time.Second)},
		{Pane: tmux.Pane{ID: "%3", Index: 3, Type: tmux.AgentGemini}, LastActivity: now.Add(-10 * time.Second)},
	}

	lastCaptured := map[string]time.Time{
		"%1": now,
		"%2": now,
		"%3": now,
	}

	plan := planPaneCaptures(panes, "", lastCaptured, 2, 1)
	if len(plan.Targets) != 2 {
		t.Fatalf("expected 2 capture targets, got %d", len(plan.Targets))
	}
	if plan.Targets[0].Pane.ID != "%2" || plan.Targets[1].Pane.ID != "%3" {
		t.Fatalf("unexpected round-robin targets: %s, %s", plan.Targets[0].Pane.ID, plan.Targets[1].Pane.ID)
	}
	if plan.NextCursor != 0 {
		t.Fatalf("expected NextCursor=0, got %d", plan.NextCursor)
	}
}

func TestSessionDataUpdate_SortsPanesAndKeepsSelection(t *testing.T) {
	t.Parallel()

	m := New("session", "")
	m.panes = []tmux.Pane{
		{ID: "%0", Index: 0, Title: "session__user_0", Type: tmux.AgentUser},
		{ID: "%1", Index: 1, Title: "session__cod_1", Type: tmux.AgentCodex},
		{ID: "%2", Index: 2, Title: "session__cc_1", Type: tmux.AgentClaude},
	}
	m.cursor = 2

	msg := SessionDataWithOutputMsg{
		Panes: []tmux.Pane{
			{ID: "%2", Index: 2, Title: "session__cc_1", Type: tmux.AgentClaude},
			{ID: "%0", Index: 0, Title: "session__user_0", Type: tmux.AgentUser},
			{ID: "%1", Index: 1, Title: "session__cod_1", Type: tmux.AgentCodex},
		},
		Duration:          10 * time.Millisecond,
		NextCaptureCursor: 0,
	}

	updated, _ := m.Update(msg)
	m2 := updated.(Model)

	if len(m2.panes) != 3 {
		t.Fatalf("expected 3 panes, got %d", len(m2.panes))
	}
	if m2.panes[0].ID != "%0" || m2.panes[1].ID != "%1" || m2.panes[2].ID != "%2" {
		t.Fatalf("expected panes sorted by index, got %s %s %s", m2.panes[0].ID, m2.panes[1].ID, m2.panes[2].ID)
	}
	if m2.panes[m2.cursor].ID != "%2" {
		t.Fatalf("expected selection to remain on %%2, got %s", m2.panes[m2.cursor].ID)
	}
}
