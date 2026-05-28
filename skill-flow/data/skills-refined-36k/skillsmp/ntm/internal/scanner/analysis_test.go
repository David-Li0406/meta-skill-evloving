package scanner

import (
	"strings"
	"testing"
)

func TestSeverityToScore(t *testing.T) {
	tests := []struct {
		severity Severity
		want     float64
	}{
		{SeverityCritical, 10.0},
		{SeverityWarning, 5.0},
		{SeverityInfo, 1.0},
		{"unknown", 2.0},
	}

	for _, tt := range tests {
		got := severityToScore(tt.severity)
		if got != tt.want {
			t.Errorf("severityToScore(%s) = %v, want %v", tt.severity, got, tt.want)
		}
	}
}

func TestComputeHotspotsBasic(t *testing.T) {
	findings := []Finding{
		{File: "file1.go", Severity: SeverityCritical, Message: "Critical issue"},
		{File: "file1.go", Severity: SeverityWarning, Message: "Warning issue"},
		{File: "file2.go", Severity: SeverityInfo, Message: "Info issue"},
	}

	hotspots := computeHotspots(findings, nil)

	if len(hotspots) != 2 {
		t.Errorf("Expected 2 hotspots, got %d", len(hotspots))
	}

	// First hotspot should be file1.go (higher score)
	if len(hotspots) > 0 && hotspots[0].File != "file1.go" {
		t.Errorf("Expected file1.go as top hotspot, got %s", hotspots[0].File)
	}

	// Check counts
	for _, h := range hotspots {
		if h.File == "file1.go" {
			if h.Critical != 1 || h.Warning != 1 || h.FindingCount != 2 {
				t.Errorf("file1.go: got critical=%d warning=%d count=%d, want 1,1,2",
					h.Critical, h.Warning, h.FindingCount)
			}
		}
	}
}

func TestAnalyzeImpactWithoutBv(t *testing.T) {
	result := &ScanResult{
		Findings: []Finding{
			{File: "test.go", Line: 10, Severity: SeverityCritical, Message: "Critical bug"},
			{File: "test.go", Line: 20, Severity: SeverityWarning, Message: "Warning"},
		},
	}

	analysis, err := AnalyzeImpact(result, nil)
	if err != nil {
		t.Fatalf("AnalyzeImpact error: %v", err)
	}

	if analysis.TotalFindings != 2 {
		t.Errorf("Expected 2 total findings, got %d", analysis.TotalFindings)
	}

	// Should be sorted by impact (critical first)
	if len(analysis.HighImpactFindings) > 0 {
		first := analysis.HighImpactFindings[0]
		if first.Finding.Severity != SeverityCritical {
			t.Errorf("Expected critical finding first, got %s", first.Finding.Severity)
		}
	}
}

func TestFormatImpactReport(t *testing.T) {
	result := &AnalysisResult{
		TotalFindings:  2,
		GraphAvailable: false,
		HighImpactFindings: []ImpactAnalysis{
			{
				Finding: Finding{
					File:     "test.go",
					Line:     10,
					Severity: SeverityCritical,
					Message:  "Critical issue",
				},
				ImpactScore: 10.0,
			},
		},
		RecommendedOrder: []ImpactAnalysis{
			{
				Finding: Finding{
					File:     "test.go",
					Line:     10,
					Severity: SeverityCritical,
					Message:  "Critical issue",
				},
				ImpactScore: 10.0,
			},
		},
		Hotspots: []Hotspot{
			{File: "test.go", FindingCount: 2, ImpactScore: 15.0},
		},
	}

	report := FormatImpactReport(result)

	if !strings.Contains(report, "Scan Impact Analysis") {
		t.Error("Report should contain 'Scan Impact Analysis' header")
	}

	if !strings.Contains(report, "bv not available") {
		t.Error("Report should note bv is unavailable")
	}

	if !strings.Contains(report, "test.go") {
		t.Error("Report should contain the file name")
	}
}

func TestTruncate(t *testing.T) {
	tests := []struct {
		input  string
		maxLen int
		want   string
	}{
		{"short", 10, "short"},
		{"this is a long message", 10, "this is..."},
		{"exactly10!", 10, "exactly10!"},
	}

	for _, tt := range tests {
		got := truncate(tt.input, tt.maxLen)
		if got != tt.want {
			t.Errorf("truncate(%q, %d) = %q, want %q", tt.input, tt.maxLen, got, tt.want)
		}
	}
}

func TestFormatPriority(t *testing.T) {
	tests := []struct {
		severity Severity
		want     string
	}{
		{SeverityCritical, "P0"},
		{SeverityWarning, "P1"},
		{SeverityInfo, "P3"},
		{"unknown", "P2"},
	}

	for _, tt := range tests {
		got := formatPriority(tt.severity)
		if got != tt.want {
			t.Errorf("formatPriority(%s) = %s, want %s", tt.severity, got, tt.want)
		}
	}
}

func TestSortByImpact(t *testing.T) {
	findings := []ImpactAnalysis{
		{Finding: Finding{Message: "low"}, ImpactScore: 1.0},
		{Finding: Finding{Message: "high"}, ImpactScore: 10.0},
		{Finding: Finding{Message: "medium"}, ImpactScore: 5.0},
	}

	sortByImpact(findings)

	if findings[0].Finding.Message != "high" {
		t.Errorf("First finding should be 'high', got %s", findings[0].Finding.Message)
	}
	if findings[1].Finding.Message != "medium" {
		t.Errorf("Second finding should be 'medium', got %s", findings[1].Finding.Message)
	}
	if findings[2].Finding.Message != "low" {
		t.Errorf("Third finding should be 'low', got %s", findings[2].Finding.Message)
	}
}
