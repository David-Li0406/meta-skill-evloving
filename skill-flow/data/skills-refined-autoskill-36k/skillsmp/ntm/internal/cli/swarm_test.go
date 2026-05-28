package cli

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/swarm"
)

func TestWritePlanToFile(t *testing.T) {
	tmpDir := t.TempDir()
	path := filepath.Join(tmpDir, "plans", "swarm_plan.json")

	createdAt := time.Now().UTC().Truncate(time.Second)
	plan := &swarm.SwarmPlan{
		CreatedAt:       createdAt,
		ScanDir:         "/tmp/projects",
		TotalCC:         1,
		TotalCod:        2,
		TotalGmi:        0,
		TotalAgents:     3,
		SessionsPerType: 2,
		PanesPerSession: 2,
	}

	if err := writePlanToFile(plan, path); err != nil {
		t.Fatalf("writePlanToFile error: %v", err)
	}

	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read plan file: %v", err)
	}

	var got swarm.SwarmPlan
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("unmarshal plan: %v", err)
	}

	if got.ScanDir != plan.ScanDir {
		t.Errorf("ScanDir = %q, want %q", got.ScanDir, plan.ScanDir)
	}
	if got.TotalAgents != plan.TotalAgents {
		t.Errorf("TotalAgents = %d, want %d", got.TotalAgents, plan.TotalAgents)
	}
	if got.SessionsPerType != plan.SessionsPerType {
		t.Errorf("SessionsPerType = %d, want %d", got.SessionsPerType, plan.SessionsPerType)
	}
	if !got.CreatedAt.Equal(createdAt) {
		t.Errorf("CreatedAt = %v, want %v", got.CreatedAt, createdAt)
	}
}

func TestWritePlanToFileNilPlan(t *testing.T) {
	tmpDir := t.TempDir()
	path := filepath.Join(tmpDir, "plan.json")

	if err := writePlanToFile(nil, path); err == nil {
		t.Fatal("expected error for nil plan, got nil")
	}
}
