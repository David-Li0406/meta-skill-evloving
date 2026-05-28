package swarm

import (
	"encoding/json"
	"testing"
	"time"
)

func TestProjectBeadCountJSON(t *testing.T) {
	pbc := ProjectBeadCount{
		Path:      "/data/projects/example",
		Name:      "example",
		OpenBeads: 42,
		Tier:      1,
	}

	data, err := json.Marshal(pbc)
	if err != nil {
		t.Fatalf("failed to marshal ProjectBeadCount: %v", err)
	}

	var decoded ProjectBeadCount
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal ProjectBeadCount: %v", err)
	}

	if decoded.Path != pbc.Path {
		t.Errorf("path mismatch: got %q, want %q", decoded.Path, pbc.Path)
	}
	if decoded.Name != pbc.Name {
		t.Errorf("name mismatch: got %q, want %q", decoded.Name, pbc.Name)
	}
	if decoded.OpenBeads != pbc.OpenBeads {
		t.Errorf("open_beads mismatch: got %d, want %d", decoded.OpenBeads, pbc.OpenBeads)
	}
	if decoded.Tier != pbc.Tier {
		t.Errorf("tier mismatch: got %d, want %d", decoded.Tier, pbc.Tier)
	}
}

func TestProjectAllocationJSON(t *testing.T) {
	pa := ProjectAllocation{
		Project: ProjectBeadCount{
			Path:      "/dp/test",
			Name:      "test",
			OpenBeads: 150,
			Tier:      2,
		},
		CCAgents:    3,
		CodAgents:   3,
		GmiAgents:   2,
		TotalAgents: 8,
	}

	data, err := json.Marshal(pa)
	if err != nil {
		t.Fatalf("failed to marshal ProjectAllocation: %v", err)
	}

	var decoded ProjectAllocation
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal ProjectAllocation: %v", err)
	}

	if decoded.CCAgents != pa.CCAgents {
		t.Errorf("cc_agents mismatch: got %d, want %d", decoded.CCAgents, pa.CCAgents)
	}
	if decoded.CodAgents != pa.CodAgents {
		t.Errorf("cod_agents mismatch: got %d, want %d", decoded.CodAgents, pa.CodAgents)
	}
	if decoded.TotalAgents != pa.TotalAgents {
		t.Errorf("total_agents mismatch: got %d, want %d", decoded.TotalAgents, pa.TotalAgents)
	}
}

func TestSwarmPlanJSON(t *testing.T) {
	now := time.Now().UTC().Truncate(time.Second)
	plan := SwarmPlan{
		CreatedAt: now,
		ScanDir:   "/dp",
		Allocations: []ProjectAllocation{
			{
				Project: ProjectBeadCount{
					Path:      "/dp/project1",
					Name:      "project1",
					OpenBeads: 500,
					Tier:      1,
				},
				CCAgents:    4,
				CodAgents:   4,
				GmiAgents:   2,
				TotalAgents: 10,
			},
		},
		TotalCC:         4,
		TotalCod:        4,
		TotalGmi:        2,
		TotalAgents:     10,
		SessionsPerType: 3,
		PanesPerSession: 4,
		Sessions: []SessionSpec{
			{
				Name:      "cc_agents_1",
				AgentType: "cc",
				PaneCount: 4,
				Panes: []PaneSpec{
					{Index: 1, Project: "project1", AgentType: "cc", AgentIndex: 1, LaunchCmd: "cc"},
				},
			},
		},
	}

	data, err := json.Marshal(plan)
	if err != nil {
		t.Fatalf("failed to marshal SwarmPlan: %v", err)
	}

	var decoded SwarmPlan
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal SwarmPlan: %v", err)
	}

	if decoded.ScanDir != plan.ScanDir {
		t.Errorf("scan_dir mismatch: got %q, want %q", decoded.ScanDir, plan.ScanDir)
	}
	if decoded.TotalAgents != plan.TotalAgents {
		t.Errorf("total_agents mismatch: got %d, want %d", decoded.TotalAgents, plan.TotalAgents)
	}
	if len(decoded.Sessions) != len(plan.Sessions) {
		t.Errorf("sessions length mismatch: got %d, want %d", len(decoded.Sessions), len(plan.Sessions))
	}
	if len(decoded.Allocations) != len(plan.Allocations) {
		t.Errorf("allocations length mismatch: got %d, want %d", len(decoded.Allocations), len(plan.Allocations))
	}
}

func TestSessionSpecJSON(t *testing.T) {
	ss := SessionSpec{
		Name:      "cod_agents_2",
		AgentType: "cod",
		PaneCount: 3,
		Panes: []PaneSpec{
			{Index: 1, Project: "proj1", AgentType: "cod", AgentIndex: 1, LaunchCmd: "cod"},
			{Index: 2, Project: "proj2", AgentType: "cod", AgentIndex: 1, LaunchCmd: "cod"},
			{Index: 3, Project: "proj1", AgentType: "cod", AgentIndex: 2, LaunchCmd: "cod"},
		},
	}

	data, err := json.Marshal(ss)
	if err != nil {
		t.Fatalf("failed to marshal SessionSpec: %v", err)
	}

	var decoded SessionSpec
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal SessionSpec: %v", err)
	}

	if decoded.Name != ss.Name {
		t.Errorf("name mismatch: got %q, want %q", decoded.Name, ss.Name)
	}
	if decoded.PaneCount != ss.PaneCount {
		t.Errorf("pane_count mismatch: got %d, want %d", decoded.PaneCount, ss.PaneCount)
	}
	if len(decoded.Panes) != len(ss.Panes) {
		t.Errorf("panes length mismatch: got %d, want %d", len(decoded.Panes), len(ss.Panes))
	}
}

func TestPaneSpecJSON(t *testing.T) {
	ps := PaneSpec{
		Index:      5,
		Project:    "my_project",
		AgentType:  "gmi",
		AgentIndex: 3,
		LaunchCmd:  "gmi",
	}

	data, err := json.Marshal(ps)
	if err != nil {
		t.Fatalf("failed to marshal PaneSpec: %v", err)
	}

	var decoded PaneSpec
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal PaneSpec: %v", err)
	}

	if decoded.Index != ps.Index {
		t.Errorf("index mismatch: got %d, want %d", decoded.Index, ps.Index)
	}
	if decoded.Project != ps.Project {
		t.Errorf("project mismatch: got %q, want %q", decoded.Project, ps.Project)
	}
	if decoded.AgentIndex != ps.AgentIndex {
		t.Errorf("agent_index mismatch: got %d, want %d", decoded.AgentIndex, ps.AgentIndex)
	}
}

func TestSwarmStateJSON(t *testing.T) {
	now := time.Now().UTC().Truncate(time.Second)
	limitTime := now.Add(-5 * time.Minute)

	state := SwarmState{
		Plan: &SwarmPlan{
			CreatedAt:   now,
			ScanDir:     "/dp",
			TotalAgents: 5,
		},
		StartedAt: now,
		PaneStates: map[string]PaneState{
			"cc_agents_1:1.1": {
				SessionPane:  "cc_agents_1:1.1",
				AgentType:    "cc",
				Project:      "proj1",
				Status:       "running",
				LastActivity: now,
				RespawnCount: 0,
			},
			"cc_agents_1:1.2": {
				SessionPane:  "cc_agents_1:1.2",
				AgentType:    "cc",
				Project:      "proj2",
				Status:       "limit_hit",
				LastActivity: limitTime,
				LimitHitAt:   &limitTime,
				RespawnCount: 1,
			},
		},
		LimitHits: []LimitHitEvent{
			{
				SessionPane: "cc_agents_1:1.2",
				AgentType:   "cc",
				Project:     "proj2",
				DetectedAt:  limitTime,
				Pattern:     "usage limit",
			},
		},
		Respawns: []RespawnEvent{
			{
				SessionPane:     "cc_agents_1:1.2",
				AgentType:       "cc",
				RespawnedAt:     now,
				AccountRotated:  true,
				PreviousAccount: "account1",
				NewAccount:      "account2",
			},
		},
	}

	data, err := json.Marshal(state)
	if err != nil {
		t.Fatalf("failed to marshal SwarmState: %v", err)
	}

	var decoded SwarmState
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal SwarmState: %v", err)
	}

	if len(decoded.PaneStates) != len(state.PaneStates) {
		t.Errorf("pane_states length mismatch: got %d, want %d", len(decoded.PaneStates), len(state.PaneStates))
	}
	if len(decoded.LimitHits) != len(state.LimitHits) {
		t.Errorf("limit_hits length mismatch: got %d, want %d", len(decoded.LimitHits), len(state.LimitHits))
	}
	if len(decoded.Respawns) != len(state.Respawns) {
		t.Errorf("respawns length mismatch: got %d, want %d", len(decoded.Respawns), len(state.Respawns))
	}
}

func TestPaneStateJSON(t *testing.T) {
	now := time.Now().UTC().Truncate(time.Second)

	t.Run("without limit hit", func(t *testing.T) {
		ps := PaneState{
			SessionPane:  "gmi_agents_1:1.3",
			AgentType:    "gmi",
			Project:      "test_proj",
			Status:       "running",
			LastActivity: now,
			LimitHitAt:   nil,
			RespawnCount: 0,
		}

		data, err := json.Marshal(ps)
		if err != nil {
			t.Fatalf("failed to marshal PaneState: %v", err)
		}

		var decoded PaneState
		if err := json.Unmarshal(data, &decoded); err != nil {
			t.Fatalf("failed to unmarshal PaneState: %v", err)
		}

		if decoded.LimitHitAt != nil {
			t.Error("expected limit_hit_at to be nil")
		}
	})

	t.Run("with limit hit", func(t *testing.T) {
		limitTime := now.Add(-2 * time.Minute)
		ps := PaneState{
			SessionPane:  "cc_agents_2:1.1",
			AgentType:    "cc",
			Project:      "proj",
			Status:       "limit_hit",
			LastActivity: limitTime,
			LimitHitAt:   &limitTime,
			RespawnCount: 2,
		}

		data, err := json.Marshal(ps)
		if err != nil {
			t.Fatalf("failed to marshal PaneState: %v", err)
		}

		var decoded PaneState
		if err := json.Unmarshal(data, &decoded); err != nil {
			t.Fatalf("failed to unmarshal PaneState: %v", err)
		}

		if decoded.LimitHitAt == nil {
			t.Error("expected limit_hit_at to be non-nil")
		}
		if decoded.RespawnCount != ps.RespawnCount {
			t.Errorf("respawn_count mismatch: got %d, want %d", decoded.RespawnCount, ps.RespawnCount)
		}
	})
}

func TestLimitHitEventJSON(t *testing.T) {
	now := time.Now().UTC().Truncate(time.Second)
	event := LimitHitEvent{
		SessionPane: "cod_agents_1:1.5",
		AgentType:   "cod",
		Project:     "myproject",
		DetectedAt:  now,
		Pattern:     "rate limit exceeded",
	}

	data, err := json.Marshal(event)
	if err != nil {
		t.Fatalf("failed to marshal LimitHitEvent: %v", err)
	}

	var decoded LimitHitEvent
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("failed to unmarshal LimitHitEvent: %v", err)
	}

	if decoded.Pattern != event.Pattern {
		t.Errorf("pattern mismatch: got %q, want %q", decoded.Pattern, event.Pattern)
	}
}

func TestRespawnEventJSON(t *testing.T) {
	now := time.Now().UTC().Truncate(time.Second)

	t.Run("without account rotation", func(t *testing.T) {
		event := RespawnEvent{
			SessionPane:    "cc_agents_1:1.1",
			AgentType:      "cc",
			RespawnedAt:    now,
			AccountRotated: false,
		}

		data, err := json.Marshal(event)
		if err != nil {
			t.Fatalf("failed to marshal RespawnEvent: %v", err)
		}

		var decoded RespawnEvent
		if err := json.Unmarshal(data, &decoded); err != nil {
			t.Fatalf("failed to unmarshal RespawnEvent: %v", err)
		}

		if decoded.AccountRotated {
			t.Error("expected account_rotated to be false")
		}
	})

	t.Run("with account rotation", func(t *testing.T) {
		event := RespawnEvent{
			SessionPane:     "cc_agents_1:1.2",
			AgentType:       "cc",
			RespawnedAt:     now,
			AccountRotated:  true,
			PreviousAccount: "user1@example.com",
			NewAccount:      "user2@example.com",
		}

		data, err := json.Marshal(event)
		if err != nil {
			t.Fatalf("failed to marshal RespawnEvent: %v", err)
		}

		var decoded RespawnEvent
		if err := json.Unmarshal(data, &decoded); err != nil {
			t.Fatalf("failed to unmarshal RespawnEvent: %v", err)
		}

		if !decoded.AccountRotated {
			t.Error("expected account_rotated to be true")
		}
		if decoded.PreviousAccount != event.PreviousAccount {
			t.Errorf("previous_account mismatch: got %q, want %q", decoded.PreviousAccount, event.PreviousAccount)
		}
		if decoded.NewAccount != event.NewAccount {
			t.Errorf("new_account mismatch: got %q, want %q", decoded.NewAccount, event.NewAccount)
		}
	})
}
