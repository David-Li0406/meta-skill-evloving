package ensemble

import (
	"testing"
	"time"
)

func TestContextPack_Fields(t *testing.T) {
	now := time.Now()
	pack := &ContextPack{
		Hash:        "abc123",
		GeneratedAt: now,
		ProjectBrief: &ProjectBrief{
			Name:        "test-project",
			Description: "A test project",
		},
		UserContext: &UserContext{
			ProblemStatement: "How do I fix this?",
		},
		TokenEstimate: 500,
	}

	if pack.Hash != "abc123" {
		t.Errorf("Hash = %q, want %q", pack.Hash, "abc123")
	}
	if pack.GeneratedAt != now {
		t.Errorf("GeneratedAt mismatch")
	}
	if pack.ProjectBrief == nil {
		t.Error("ProjectBrief should not be nil")
	}
	if pack.UserContext == nil {
		t.Error("UserContext should not be nil")
	}
	if pack.TokenEstimate != 500 {
		t.Errorf("TokenEstimate = %d, want 500", pack.TokenEstimate)
	}
}

func TestProjectBrief_Fields(t *testing.T) {
	brief := &ProjectBrief{
		Name:        "myproject",
		Description: "A Go project",
		Languages:   []string{"go", "python"},
		Frameworks:  []string{"gin", "cobra"},
		Structure: &ProjectStructure{
			EntryPoints:  []string{"cmd/main.go"},
			CorePackages: []string{"internal/core"},
			TestCoverage: 75.5,
			TotalFiles:   100,
			TotalLines:   5000,
		},
		RecentActivity: []CommitSummary{
			{Hash: "abc1234", Summary: "Initial commit"},
		},
		OpenIssues: 5,
	}

	if brief.Name != "myproject" {
		t.Errorf("Name = %q, want %q", brief.Name, "myproject")
	}
	if len(brief.Languages) != 2 {
		t.Errorf("Languages count = %d, want 2", len(brief.Languages))
	}
	if len(brief.Frameworks) != 2 {
		t.Errorf("Frameworks count = %d, want 2", len(brief.Frameworks))
	}
	if brief.Structure == nil {
		t.Error("Structure should not be nil")
	}
	if len(brief.RecentActivity) != 1 {
		t.Errorf("RecentActivity count = %d, want 1", len(brief.RecentActivity))
	}
	if brief.OpenIssues != 5 {
		t.Errorf("OpenIssues = %d, want 5", brief.OpenIssues)
	}
}

func TestProjectStructure_Fields(t *testing.T) {
	structure := &ProjectStructure{
		EntryPoints:  []string{"cmd/main.go", "cmd/cli.go"},
		CorePackages: []string{"internal/core", "internal/api"},
		TestCoverage: 80.5,
		TotalFiles:   150,
		TotalLines:   10000,
	}

	if len(structure.EntryPoints) != 2 {
		t.Errorf("EntryPoints count = %d, want 2", len(structure.EntryPoints))
	}
	if len(structure.CorePackages) != 2 {
		t.Errorf("CorePackages count = %d, want 2", len(structure.CorePackages))
	}
	if structure.TestCoverage != 80.5 {
		t.Errorf("TestCoverage = %f, want 80.5", structure.TestCoverage)
	}
	if structure.TotalFiles != 150 {
		t.Errorf("TotalFiles = %d, want 150", structure.TotalFiles)
	}
	if structure.TotalLines != 10000 {
		t.Errorf("TotalLines = %d, want 10000", structure.TotalLines)
	}
}

func TestCommitSummary_Fields(t *testing.T) {
	now := time.Now()
	commit := CommitSummary{
		Hash:    "abc1234",
		Author:  "Test User",
		Summary: "Fix bug in auth module",
		Date:    now,
	}

	if commit.Hash != "abc1234" {
		t.Errorf("Hash = %q, want %q", commit.Hash, "abc1234")
	}
	if commit.Author != "Test User" {
		t.Errorf("Author = %q, want %q", commit.Author, "Test User")
	}
	if commit.Summary != "Fix bug in auth module" {
		t.Errorf("Summary = %q, want %q", commit.Summary, "Fix bug in auth module")
	}
	if commit.Date != now {
		t.Error("Date mismatch")
	}
}

func TestUserContext_Fields(t *testing.T) {
	ctx := &UserContext{
		ProblemStatement: "How do I improve performance?",
		FocusAreas:       []string{"database", "caching"},
		Constraints:      []string{"must be backward compatible", "no new dependencies"},
		Stakeholders:     []string{"backend team", "devops"},
	}

	if ctx.ProblemStatement != "How do I improve performance?" {
		t.Errorf("ProblemStatement = %q", ctx.ProblemStatement)
	}
	if len(ctx.FocusAreas) != 2 {
		t.Errorf("FocusAreas count = %d, want 2", len(ctx.FocusAreas))
	}
	if len(ctx.Constraints) != 2 {
		t.Errorf("Constraints count = %d, want 2", len(ctx.Constraints))
	}
	if len(ctx.Stakeholders) != 2 {
		t.Errorf("Stakeholders count = %d, want 2", len(ctx.Stakeholders))
	}
}

func TestContextPack_NilComponents(t *testing.T) {
	// Test that nil components are handled gracefully
	pack := &ContextPack{
		Hash:          "test",
		GeneratedAt:   time.Now(),
		ProjectBrief:  nil,
		UserContext:   nil,
		TokenEstimate: 0,
	}

	if pack.ProjectBrief != nil {
		t.Error("ProjectBrief should be nil")
	}
	if pack.UserContext != nil {
		t.Error("UserContext should be nil")
	}
}

func TestProjectBrief_EmptySlices(t *testing.T) {
	brief := &ProjectBrief{
		Name:           "test",
		Languages:      nil,
		Frameworks:     nil,
		RecentActivity: nil,
	}

	if brief.Languages != nil {
		t.Error("Languages should be nil")
	}
	if brief.Frameworks != nil {
		t.Error("Frameworks should be nil")
	}
	if brief.RecentActivity != nil {
		t.Error("RecentActivity should be nil")
	}

	// Empty slices should also work
	brief.Languages = []string{}
	brief.Frameworks = []string{}
	brief.RecentActivity = []CommitSummary{}

	if len(brief.Languages) != 0 {
		t.Error("Languages should be empty")
	}
}

func TestProjectStructure_ZeroValues(t *testing.T) {
	structure := &ProjectStructure{}

	if structure.TestCoverage != 0 {
		t.Error("TestCoverage should be 0")
	}
	if structure.TotalFiles != 0 {
		t.Error("TotalFiles should be 0")
	}
	if structure.TotalLines != 0 {
		t.Error("TotalLines should be 0")
	}
}
