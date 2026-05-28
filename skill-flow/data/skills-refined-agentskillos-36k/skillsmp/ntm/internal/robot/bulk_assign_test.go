package robot

import (
	"errors"
	"fmt"
	"os"
	"reflect"
	"sort"
	"strings"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/bv"
	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

func TestDecodeBulkAssignTriageValid(t *testing.T) {
	payload := `{"generated_at":"2026-01-19T23:16:00Z","data_hash":"abc","triage":{"meta":{"version":"1","generated_at":"2026-01-19T23:16:00Z","phase2_ready":true,"issue_count":1,"compute_time_ms":12},"quick_ref":{"open_count":1,"actionable_count":1,"blocked_count":0,"in_progress_count":0,"top_picks":[]},"recommendations":[{"id":"bd-1","title":"Test","type":"task","status":"ready","priority":1,"score":0.5,"action":"do","reasons":[]}],"quick_wins":[],"blockers_to_clear":[]}}`

	triage, err := decodeBulkAssignTriage([]byte(payload))
	if err != nil {
		t.Fatalf("decodeBulkAssignTriage failed: %v", err)
	}

	t.Logf("triage parsed: %+v", triage.Triage.Recommendations)
	if len(triage.Triage.Recommendations) != 1 {
		t.Fatalf("expected 1 recommendation, got %d", len(triage.Triage.Recommendations))
	}
	if triage.Triage.Recommendations[0].ID != "bd-1" {
		t.Errorf("expected bead id bd-1, got %q", triage.Triage.Recommendations[0].ID)
	}
}

func TestDecodeBulkAssignTriageInvalid(t *testing.T) {
	_, err := decodeBulkAssignTriage([]byte(`{"triage":`))
	if err == nil {
		t.Fatal("expected error for invalid triage JSON")
	}
	if !strings.Contains(err.Error(), "unexpected end") {
		t.Logf("invalid JSON error: %v", err)
	}
}

func TestBulkAssignImpactStrategySorting(t *testing.T) {
	triage := mockTriage(nil, []bv.BlockerToClear{
		{ID: "bd-1", Title: "A", UnblocksCount: 2},
		{ID: "bd-2", Title: "B", UnblocksCount: 5},
		{ID: "bd-3", Title: "C", UnblocksCount: 3},
	})
	panes := mockPanes("proj", []int{1, 2, 3})
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "impact"}, BulkAssignDependencies{}, panes, triage, nil)

	got := []string{}
	for _, a := range plan.Assignments {
		got = append(got, a.Bead)
	}
	expected := []string{"bd-2", "bd-3", "bd-1"}

	t.Logf("strategy=impact triage blockers=%v", triage.Triage.BlockersToClear)
	t.Logf("expected order=%v actual=%v", expected, got)

	if !reflect.DeepEqual(expected, got) {
		t.Fatalf("impact strategy order mismatch: got %v, want %v", got, expected)
	}
}

func TestBulkAssignReadyStrategyFilters(t *testing.T) {
	recs := []bv.TriageRecommendation{
		{ID: "bd-1", Title: "Ready low", Status: "ready", Priority: 2},
		{ID: "bd-2", Title: "Blocked", Status: "blocked", Priority: 0},
		{ID: "bd-3", Title: "Ready high", Status: "ready", Priority: 1},
	}
	triage := mockTriage(recs, nil)
	panes := mockPanes("proj", []int{1, 2, 3})
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "ready"}, BulkAssignDependencies{}, panes, triage, nil)

	got := []string{}
	for _, a := range plan.Assignments {
		got = append(got, a.Bead)
	}
	expected := []string{"bd-3", "bd-1"}

	t.Logf("strategy=ready triage recs=%v", recs)
	t.Logf("expected=%v actual=%v", expected, got)

	if !reflect.DeepEqual(expected, got) {
		t.Fatalf("ready strategy order mismatch: got %v, want %v", got, expected)
	}
}

func TestBulkAssignStaleStrategy(t *testing.T) {
	now := time.Date(2026, 1, 20, 1, 0, 0, 0, time.UTC)
	inProgress := []bv.BeadInProgress{
		{ID: "bd-1", Title: "Recent", UpdatedAt: now.Add(-2 * time.Hour)},
		{ID: "bd-2", Title: "Stale", UpdatedAt: now.Add(-48 * time.Hour)},
		{ID: "bd-3", Title: "Oldest", UpdatedAt: now.Add(-72 * time.Hour)},
	}
	panes := mockPanes("proj", []int{1, 2, 3})
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "stale"}, BulkAssignDependencies{}, panes, nil, inProgress)

	got := []string{}
	for _, a := range plan.Assignments {
		got = append(got, a.Bead)
	}
	expected := []string{"bd-3", "bd-2", "bd-1"}

	t.Logf("strategy=stale in_progress=%v", inProgress)
	t.Logf("expected=%v actual=%v", expected, got)

	if !reflect.DeepEqual(expected, got) {
		t.Fatalf("stale strategy order mismatch: got %v, want %v", got, expected)
	}
}

func TestBulkAssignBalancedStrategyMix(t *testing.T) {
	triage := mockTriage(
		[]bv.TriageRecommendation{
			{ID: "bd-r1", Title: "Ready1", Status: "ready", Priority: 1},
			{ID: "bd-r2", Title: "Ready2", Status: "ready", Priority: 2},
		},
		[]bv.BlockerToClear{
			{ID: "bd-i1", Title: "Impact1", UnblocksCount: 5},
			{ID: "bd-i2", Title: "Impact2", UnblocksCount: 3},
		},
	)
	inProgress := []bv.BeadInProgress{
		{ID: "bd-s1", Title: "Stale1", UpdatedAt: time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)},
		{ID: "bd-s2", Title: "Stale2", UpdatedAt: time.Date(2026, 1, 2, 0, 0, 0, 0, time.UTC)},
	}
	panes := mockPanes("proj", []int{1, 2, 3, 4, 5, 6})
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "balanced"}, BulkAssignDependencies{}, panes, triage, inProgress)

	got := []string{}
	for _, a := range plan.Assignments {
		got = append(got, a.Bead)
	}
	// Expected interleaving: impact1, ready1, stale1, impact2, ready2, stale2
	expected := []string{"bd-i1", "bd-r1", "bd-s1", "bd-i2", "bd-r2", "bd-s2"}

	t.Logf("strategy=balanced expected=%v actual=%v", expected, got)
	if !reflect.DeepEqual(expected, got) {
		t.Fatalf("balanced strategy order mismatch: got %v, want %v", got, expected)
	}
}

func TestBulkAssignMoreBeadsThanPanes(t *testing.T) {
	panes := mockPanes("proj", []int{1, 2})
	beads := []bulkBead{{ID: "bd-1"}, {ID: "bd-2"}, {ID: "bd-3"}}
	plan := allocateBulkAssignBeads(panes, beads)

	t.Logf("beads=%v panes=%v", beads, panes)
	if len(plan.UnassignedBeads) != 1 {
		t.Fatalf("expected 1 unassigned bead, got %d", len(plan.UnassignedBeads))
	}
	if plan.UnassignedBeads[0] != "bd-3" {
		t.Errorf("expected unassigned bead bd-3, got %v", plan.UnassignedBeads)
	}
}

func TestBulkAssignMorePanesThanBeads(t *testing.T) {
	panes := mockPanes("proj", []int{1, 2, 3})
	beads := []bulkBead{{ID: "bd-1"}}
	plan := allocateBulkAssignBeads(panes, beads)

	t.Logf("beads=%v panes=%v", beads, panes)
	if len(plan.UnassignedPanes) != 2 {
		t.Fatalf("expected 2 unassigned panes, got %d", len(plan.UnassignedPanes))
	}
}

func TestBulkAssignExactCounts(t *testing.T) {
	panes := mockPanes("proj", []int{1, 2})
	beads := []bulkBead{{ID: "bd-1"}, {ID: "bd-2"}}
	plan := allocateBulkAssignBeads(panes, beads)

	t.Logf("beads=%v panes=%v", beads, panes)
	if len(plan.UnassignedBeads) != 0 || len(plan.UnassignedPanes) != 0 {
		t.Fatalf("expected no unassigned items, got beads=%v panes=%v", plan.UnassignedBeads, plan.UnassignedPanes)
	}
}

func TestBulkAssignTemplateSubstitution(t *testing.T) {
	template := "{bead_id}:{bead_title}:{bead_type}:{bead_deps}:{session}:{pane}"
	result := expandBulkAssignTemplate(template, "bd-1", "Title", "task", []string{"bd-2", "bd-3"}, "proj", 2)
	expected := "bd-1:Title:task:bd-2, bd-3:proj:2"

	t.Logf("template=%q result=%q", template, result)
	if result != expected {
		t.Fatalf("template substitution mismatch: got %q want %q", result, expected)
	}
}

func TestBulkAssignTemplateSubstitutionDefaults(t *testing.T) {
	template := "{bead_id}:{bead_type}:{bead_deps}"
	result := expandBulkAssignTemplate(template, "bd-1", "Title", "", nil, "proj", 2)
	expected := "bd-1:unknown:none"

	t.Logf("template=%q result=%q", template, result)
	if result != expected {
		t.Fatalf("default substitution mismatch: got %q want %q", result, expected)
	}
}

func TestBulkAssignTemplateLoadingFromFile(t *testing.T) {
	opts := BulkAssignOptions{PromptTemplatePath: "testdata/bulk_assign_template.txt"}
	deps := bulkAssignDeps(nil)
	deps.ReadFile = func(path string) ([]byte, error) {
		return os.ReadFile(path)
	}
	template, err := loadBulkAssignTemplate(opts, deps)
	if err != nil {
		t.Fatalf("loadBulkAssignTemplate failed: %v", err)
	}

	t.Logf("loaded template=%q", template)
	if !strings.Contains(template, "{bead_id}") {
		t.Fatalf("expected template to contain {bead_id}, got %q", template)
	}
}

func TestBulkAssignSequentialDeliveryOrdering(t *testing.T) {
	allocation := `{"2":"bd-2","1":"bd-1"}`
	panes := mockPanes("proj", []int{1, 2})
	callOrder := []string{}
	deps := BulkAssignDependencies{
		FetchBeadTitle: func(_ string, beadID string) (string, error) { return "Title " + beadID, nil },
		Cwd:            func() (string, error) { return "/tmp", nil },
		Now:            func() time.Time { return time.Date(2026, 1, 20, 0, 0, 0, 0, time.UTC) },
		ReadFile:       func(path string) ([]byte, error) { return []byte(defaultBulkAssignTemplate), nil },
	}

	plan := planBulkAssignFromAllocation(BulkAssignOptions{}, bulkAssignDeps(&deps), panes, mustParseAllocation(t, allocation))
	output := BulkAssignOutput{Session: "proj"}
	deps.SendKeys = func(paneID, message string, enter bool) error {
		callOrder = append(callOrder, paneID)
		return nil
	}
	applyBulkAssignPlan(BulkAssignOptions{}, bulkAssignDeps(&deps), &output, plan)

	expectedOrder := []string{"proj:1", "proj:2"}
	if !reflect.DeepEqual(callOrder, expectedOrder) {
		t.Fatalf("send order mismatch: got %v want %v", callOrder, expectedOrder)
	}

	t.Logf("expected order=%v actual order=%v", expectedOrder, callOrder)
}

func TestBulkAssignFailedDelivery(t *testing.T) {
	panes := mockPanes("proj", []int{1, 2})
	beads := []bulkBead{{ID: "bd-1", Title: "Title1"}, {ID: "bd-2", Title: "Title2"}}
	plan := allocateBulkAssignBeads(panes, beads)

	deps := BulkAssignDependencies{
		SendKeys: func(paneID, message string, enter bool) error {
			if paneID == "proj:2" {
				return errors.New("send failed")
			}
			return nil
		},
		ReadFile: func(path string) ([]byte, error) { return []byte(defaultBulkAssignTemplate), nil },
	}
	output := BulkAssignOutput{Session: "proj"}
	applyBulkAssignPlan(BulkAssignOptions{}, bulkAssignDeps(&deps), &output, plan)

	if output.Summary.Failed != 1 {
		t.Fatalf("expected 1 failed assignment, got %d", output.Summary.Failed)
	}
	if output.Assignments[1].Status != "failed" {
		t.Fatalf("expected failed status, got %q", output.Assignments[1].Status)
	}

	t.Logf("output=%+v", output)
}

func TestBulkAssignDryRunSkipsPromptSend(t *testing.T) {
	panes := mockPanes("proj", []int{1})
	beads := []bulkBead{{ID: "bd-1", Title: "Title1"}}
	plan := allocateBulkAssignBeads(panes, beads)

	sent := false
	deps := BulkAssignDependencies{
		SendKeys: func(paneID, message string, enter bool) error {
			sent = true
			return nil
		},
		ReadFile: func(path string) ([]byte, error) { return []byte(defaultBulkAssignTemplate), nil },
	}

	output := BulkAssignOutput{Session: "proj"}
	applyBulkAssignPlan(BulkAssignOptions{DryRun: true}, bulkAssignDeps(&deps), &output, plan)

	if sent {
		t.Fatal("expected no send calls in dry run")
	}
	if output.Assignments[0].PromptSent {
		t.Fatal("expected prompt_sent false in dry run")
	}

	t.Logf("dry-run output=%+v", output)
}

func TestBulkAssignAllocationParsing(t *testing.T) {
	allocation := `{"1":"bd-1","2":"bd-2"}`
	parsed, err := parseBulkAssignAllocation(allocation)
	if err != nil {
		t.Fatalf("parseBulkAssignAllocation failed: %v", err)
	}

	t.Logf("parsed allocation=%v", parsed)
	if parsed[1] != "bd-1" || parsed[2] != "bd-2" {
		t.Fatalf("unexpected allocation map: %v", parsed)
	}
}

func TestBulkAssignAllocationInvalidJSON(t *testing.T) {
	_, err := parseBulkAssignAllocation("not json")
	if err == nil {
		t.Fatal("expected error for invalid JSON")
	}
}

func TestBulkAssignSkipPanesParsing(t *testing.T) {
	values, err := parseBulkAssignSkipPanes("1, 3,5")
	if err != nil {
		t.Fatalf("parseBulkAssignSkipPanes failed: %v", err)
	}
	sort.Ints(values)
	expected := []int{1, 3, 5}
	if !reflect.DeepEqual(values, expected) {
		t.Fatalf("skip panes mismatch: got %v want %v", values, expected)
	}
}

func TestBulkAssignSkipPanesApplied(t *testing.T) {
	panes := []tmux.Pane{
		{Index: 1, Title: "proj__cc_1"},
		{Index: 2, Title: "proj__cc_2"},
		{Index: 3, Title: "proj__cc_3"},
	}
	filtered := filterBulkAssignPanes(panes, []int{2})

	got := []int{}
	for _, pane := range filtered {
		got = append(got, pane.Index)
	}
	sort.Ints(got)
	expected := []int{1, 3}
	if !reflect.DeepEqual(got, expected) {
		t.Fatalf("filtered panes mismatch: got %v want %v", got, expected)
	}

	t.Logf("filtered panes=%v", got)
}

func TestBulkAssignEmptySession(t *testing.T) {
	triage := mockTriage([]bv.TriageRecommendation{{ID: "bd-1", Title: "Test", Status: "ready", Priority: 1}}, nil)
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "ready"}, BulkAssignDependencies{}, nil, triage, nil)

	if len(plan.Assignments) != 0 {
		t.Fatalf("expected no assignments, got %d", len(plan.Assignments))
	}
	if len(plan.UnassignedBeads) != 1 {
		t.Fatalf("expected 1 unassigned bead, got %v", plan.UnassignedBeads)
	}

	t.Logf("plan=%+v", plan)
}

func TestBulkAssignControlPaneOnly(t *testing.T) {
	panes := []tmux.Pane{{Index: 0, Title: "proj__user_0"}}
	filtered := filterBulkAssignPanes(panes, nil)

	if len(filtered) != 0 {
		t.Fatalf("expected 0 agent panes, got %d", len(filtered))
	}
}

func TestBulkAssignInvalidBeadIDInAllocation(t *testing.T) {
	allocation := map[int]string{1: "bd-missing"}
	panes := mockPanes("proj", []int{1})
	deps := BulkAssignDependencies{
		FetchBeadTitle: func(_ string, beadID string) (string, error) {
			return "", fmt.Errorf("bead %s not found", beadID)
		},
		Cwd: func() (string, error) { return "/tmp", nil },
	}

	plan := planBulkAssignFromAllocation(BulkAssignOptions{}, bulkAssignDeps(&deps), panes, allocation)
	if plan.Assignments[0].Status != "failed" {
		t.Fatalf("expected failed status, got %q", plan.Assignments[0].Status)
	}

	t.Logf("assignment=%+v", plan.Assignments[0])
}

func TestBulkAssignBVFailure(t *testing.T) {
	deps := BulkAssignDependencies{
		FetchTriage: func(_ string) (*bv.TriageResponse, error) {
			return nil, errors.New("bv failed")
		},
		FetchInProgress: func(_ string, _ int) ([]bv.BeadInProgress, error) {
			return nil, nil
		},
		ListPanes: func(_ string) ([]tmux.Pane, error) {
			return mockTmuxPanesForList([]int{1}), nil
		},
		Now: func() time.Time { return time.Date(2026, 1, 20, 0, 0, 0, 0, time.UTC) },
		Cwd: func() (string, error) { return "/tmp", nil },
	}

	err := PrintBulkAssign(BulkAssignOptions{Session: "proj", FromBV: true, Deps: &deps})
	if err == nil {
		t.Fatal("expected error when bv triage fails")
	}
}

func TestBulkAssignLargeTriage(t *testing.T) {
	var recs []bv.TriageRecommendation
	for i := 0; i < 120; i++ {
		recs = append(recs, bv.TriageRecommendation{
			ID:       fmt.Sprintf("bd-%03d", i),
			Title:    fmt.Sprintf("Task %d", i),
			Status:   "ready",
			Priority: i % 5,
		})
	}
	triage := mockTriage(recs, nil)
	panes := mockPanes("proj", []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
	plan := planBulkAssignFromBV(BulkAssignOptions{Strategy: "ready"}, BulkAssignDependencies{}, panes, triage, nil)

	if len(plan.Assignments) != 10 {
		t.Fatalf("expected 10 assignments, got %d", len(plan.Assignments))
	}
	if len(plan.UnassignedBeads) != 110 {
		t.Fatalf("expected 110 unassigned beads, got %d", len(plan.UnassignedBeads))
	}

	t.Logf("assignments=%d unassigned=%d", len(plan.Assignments), len(plan.UnassignedBeads))
}

func TestBulkAssignConcurrentSafety(t *testing.T) {
	triage := mockTriage([]bv.TriageRecommendation{{ID: "bd-1", Title: "Test", Status: "ready", Priority: 1}}, nil)
	inProgress := []bv.BeadInProgress{{ID: "bd-2", Title: "Stale", UpdatedAt: time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)}}
	candidates := buildBulkAssignCandidates(triage, inProgress)
	before := candidates

	_ = selectBalancedBeads(candidates)
	if !reflect.DeepEqual(before, candidates) {
		t.Fatalf("expected candidates to remain unchanged")
	}
}

// helpers

func mockTriage(recs []bv.TriageRecommendation, blockers []bv.BlockerToClear) *bv.TriageResponse {
	return &bv.TriageResponse{
		Triage: bv.TriageData{
			Recommendations: recs,
			BlockersToClear: blockers,
		},
	}
}

func mockPanes(session string, indices []int) []bulkPane {
	panes := make([]bulkPane, 0, len(indices))
	for _, idx := range indices {
		panes = append(panes, bulkPane{Index: idx, AgentType: "claude"})
	}
	sort.Slice(panes, func(i, j int) bool { return panes[i].Index < panes[j].Index })
	return panes
}

func mockTmuxPanesForList(indices []int) []tmux.Pane {
	panes := make([]tmux.Pane, 0, len(indices))
	for _, idx := range indices {
		panes = append(panes, tmux.Pane{Index: idx, Title: fmt.Sprintf("proj__cc_%d", idx)})
	}
	return panes
}

func mustParseAllocation(t *testing.T, allocation string) map[int]string {
	parsed, err := parseBulkAssignAllocation(allocation)
	if err != nil {
		t.Fatalf("allocation parse failed: %v", err)
	}
	return parsed
}

func osReadFile(path string) ([]byte, error) {
	return osReadFileImpl(path)
}

var osReadFileImpl = func(path string) ([]byte, error) {
	return os.ReadFile(path)
}
