package ensemble

import "time"

// ContextPack captures the structured context assembled for an ensemble run.
// It is intentionally compact and meant to be serialized or cached.
type ContextPack struct {
	Hash          string        `json:"hash"`
	GeneratedAt   time.Time     `json:"generated_at"`
	ProjectBrief  *ProjectBrief `json:"project_brief,omitempty"`
	UserContext   *UserContext  `json:"user_context,omitempty"`
	TokenEstimate int           `json:"token_estimate"`
}

// ProjectBrief summarizes repository facts and recent activity.
type ProjectBrief struct {
	Name           string            `json:"name"`
	Description    string            `json:"description"`
	Languages      []string          `json:"languages,omitempty"`
	Frameworks     []string          `json:"frameworks,omitempty"`
	Structure      *ProjectStructure `json:"structure,omitempty"`
	RecentActivity []CommitSummary   `json:"recent_activity,omitempty"`
	OpenIssues     int               `json:"open_issues"`
}

// ProjectStructure captures coarse structural metrics about the codebase.
type ProjectStructure struct {
	EntryPoints  []string `json:"entry_points,omitempty"`
	CorePackages []string `json:"core_packages,omitempty"`
	TestCoverage float64  `json:"test_coverage"`
	TotalFiles   int      `json:"total_files"`
	TotalLines   int      `json:"total_lines"`
}

// CommitSummary captures high-level info about a recent commit.
type CommitSummary struct {
	Hash    string    `json:"hash"`
	Author  string    `json:"author,omitempty"`
	Summary string    `json:"summary,omitempty"`
	Date    time.Time `json:"date"`
}

// UserContext captures user-provided framing for the ensemble run.
type UserContext struct {
	ProblemStatement string   `json:"problem_statement"`
	FocusAreas       []string `json:"focus_areas,omitempty"`
	Constraints      []string `json:"constraints,omitempty"`
	Stakeholders     []string `json:"stakeholders,omitempty"`
}
