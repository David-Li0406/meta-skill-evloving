package metrics

import (
	"testing"
	"time"
)

func TestCollectorBasicOperations(t *testing.T) {
	// Create collector without store
	c := NewCollector(nil, "test-session")
	defer c.Close()

	// Test RecordAPICall
	c.RecordAPICall("bv", "triage")
	c.RecordAPICall("bv", "triage")
	c.RecordAPICall("bd", "create")

	// Test RecordLatency
	c.RecordLatency("cm_query", 50*time.Millisecond)
	c.RecordLatency("cm_query", 100*time.Millisecond)
	c.RecordLatency("cm_query", 75*time.Millisecond)

	// Test RecordBlockedCommand
	c.RecordBlockedCommand("agent-1", "rm -rf /", "destructive")

	// Test RecordFileConflict
	c.RecordFileConflict("agent-1", "agent-2", "*.go")

	// Generate report
	report, err := c.GenerateReport()
	if err != nil {
		t.Fatalf("GenerateReport failed: %v", err)
	}

	// Verify API calls
	if report.APICallCounts["bv:triage"] != 2 {
		t.Errorf("expected bv:triage=2, got %d", report.APICallCounts["bv:triage"])
	}
	if report.APICallCounts["bd:create"] != 1 {
		t.Errorf("expected bd:create=1, got %d", report.APICallCounts["bd:create"])
	}

	// Verify latency stats
	stats, ok := report.LatencyStats["cm_query"]
	if !ok {
		t.Fatal("expected cm_query latency stats")
	}
	if stats.Count != 3 {
		t.Errorf("expected count=3, got %d", stats.Count)
	}
	if stats.MinMs != 50 {
		t.Errorf("expected min=50, got %.1f", stats.MinMs)
	}
	if stats.MaxMs != 100 {
		t.Errorf("expected max=100, got %.1f", stats.MaxMs)
	}

	// Verify incidents
	if report.BlockedCommands != 1 {
		t.Errorf("expected blocked_commands=1, got %d", report.BlockedCommands)
	}
	if report.FileConflicts != 1 {
		t.Errorf("expected file_conflicts=1, got %d", report.FileConflicts)
	}
}

func TestLatencyStatistics(t *testing.T) {
	samples := []float64{10, 20, 30, 40, 50, 60, 70, 80, 90, 100}
	stats := calculateLatencyStats(samples)

	if stats.Count != 10 {
		t.Errorf("expected count=10, got %d", stats.Count)
	}
	if stats.MinMs != 10 {
		t.Errorf("expected min=10, got %.1f", stats.MinMs)
	}
	if stats.MaxMs != 100 {
		t.Errorf("expected max=100, got %.1f", stats.MaxMs)
	}
	if stats.AvgMs != 55 {
		t.Errorf("expected avg=55, got %.1f", stats.AvgMs)
	}
	// P50 should be around 50-60
	if stats.P50Ms < 50 || stats.P50Ms > 60 {
		t.Errorf("expected p50 around 50-60, got %.1f", stats.P50Ms)
	}
}

func TestTargetComparison(t *testing.T) {
	c := NewCollector(nil, "test-session")
	defer c.Close()

	// Should start meeting targets (no incidents)
	report, _ := c.GenerateReport()

	for _, tc := range report.TargetComparison {
		if tc.Metric == "destructive_cmd_incidents" && tc.Status != "met" {
			t.Errorf("expected destructive_cmd_incidents to be met with 0 incidents")
		}
		if tc.Metric == "file_conflicts" && tc.Status != "met" {
			t.Errorf("expected file_conflicts to be met with 0 conflicts")
		}
	}

	// Add an incident
	c.RecordBlockedCommand("agent", "rm", "policy")

	report, _ = c.GenerateReport()
	// Now should show regressing (if target is 0)
	// Note: The target is 0, so 1 incident means regressing
	found := false
	for _, tc := range report.TargetComparison {
		if tc.Metric == "destructive_cmd_incidents" {
			found = true
			if tc.Current != 1 {
				t.Errorf("expected current=1, got %.1f", tc.Current)
			}
		}
	}
	if !found {
		t.Error("expected destructive_cmd_incidents in target comparison")
	}
}

func TestCompareSnapshots(t *testing.T) {
	c := NewCollector(nil, "test-session")
	defer c.Close()

	// Baseline: latency 500ms
	baseline := &MetricsReport{
		SessionID: "baseline",
		LatencyStats: map[string]LatencyStats{
			"cm_query": {Count: 10, AvgMs: 500},
		},
		BlockedCommands: 0,
		FileConflicts:   0,
	}

	// Current: latency improved to 50ms
	c.RecordLatency("cm_query", 50*time.Millisecond)
	current, _ := c.GenerateReport()

	result := c.CompareSnapshots(baseline, current)

	// Should detect improvement in latency
	if len(result.Improvements) == 0 {
		t.Error("expected latency improvement to be detected")
	}

	// Should have no regressions
	if len(result.Regressions) != 0 {
		t.Errorf("expected no regressions, got %v", result.Regressions)
	}
}

func TestExportFormats(t *testing.T) {
	c := NewCollector(nil, "test-session")
	defer c.Close()

	c.RecordLatency("test_op", 100*time.Millisecond)

	report, err := c.GenerateReport()
	if err != nil {
		t.Fatalf("GenerateReport failed: %v", err)
	}

	// Test JSON export
	jsonData, err := report.ExportJSON()
	if err != nil {
		t.Fatalf("ExportJSON failed: %v", err)
	}
	if len(jsonData) == 0 {
		t.Error("JSON export should not be empty")
	}

	// Test CSV export
	csvData := report.ExportCSV()
	if csvData == "" {
		t.Error("CSV export should not be empty")
	}
	if !contains(csvData, "operation") || !contains(csvData, "test_op") {
		t.Error("CSV should contain header and test_op data")
	}
}

func TestSortFloat64s(t *testing.T) {
	input := []float64{5, 2, 8, 1, 9, 3}
	sortFloat64s(input)

	expected := []float64{1, 2, 3, 5, 8, 9}
	for i, v := range input {
		if v != expected[i] {
			t.Errorf("expected sorted[%d]=%f, got %f", i, expected[i], v)
		}
	}
}

func TestPercentile(t *testing.T) {
	sorted := []float64{10, 20, 30, 40, 50, 60, 70, 80, 90, 100}

	p50 := percentile(sorted, 50)
	if p50 != 50 && p50 != 60 { // P50 should be around 50-60
		t.Errorf("expected p50 around 50-60, got %.1f", p50)
	}

	p95 := percentile(sorted, 95)
	if p95 < 90 {
		t.Errorf("expected p95 >= 90, got %.1f", p95)
	}
}

func TestAverage(t *testing.T) {
	samples := []float64{10, 20, 30}
	avg := average(samples)
	if avg != 20 {
		t.Errorf("expected avg=20, got %.1f", avg)
	}

	// Empty slice
	emptyAvg := average([]float64{})
	if emptyAvg != 0 {
		t.Errorf("expected empty avg=0, got %.1f", emptyAvg)
	}
}

func TestGetTargetStatus(t *testing.T) {
	// Lower is better
	if getTargetStatus(0, 0, true) != "met" {
		t.Error("0 vs target 0 should be met")
	}
	if getTargetStatus(5, 0, true) != "regressing" {
		t.Error("5 vs target 0 should be regressing")
	}
	if getTargetStatus(10, 50, true) != "met" {
		t.Error("10 vs target 50 should be met (lower is better)")
	}

	// Higher is better
	if getTargetStatus(100, 50, false) != "met" {
		t.Error("100 vs target 50 should be met (higher is better)")
	}
	if getTargetStatus(30, 50, false) != "regressing" {
		t.Error("30 vs target 50 should be regressing (higher is better)")
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsHelper(s, substr))
}

func containsHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
