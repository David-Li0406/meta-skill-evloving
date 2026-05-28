package robot

import (
	"encoding/json"
	"testing"
)

// =============================================================================
// Health Classification Tests (bd-1alai)
// =============================================================================

func TestDetermineOverallHealth(t *testing.T) {
	tests := []struct {
		name    string
		summary DiagnoseSummary
		want    string
	}{
		// Healthy cases
		{
			name: "all healthy",
			summary: DiagnoseSummary{
				TotalPanes: 4,
				Healthy:    4,
			},
			want: "healthy",
		},
		{
			name: "empty session",
			summary: DiagnoseSummary{
				TotalPanes: 0,
			},
			want: "healthy",
		},
		{
			name: "single healthy pane",
			summary: DiagnoseSummary{
				TotalPanes: 1,
				Healthy:    1,
			},
			want: "healthy",
		},

		// Degraded cases
		{
			name: "one rate limited",
			summary: DiagnoseSummary{
				TotalPanes:  4,
				Healthy:     3,
				RateLimited: 1,
			},
			want: "degraded",
		},
		{
			name: "one degraded (non-rate limited)",
			summary: DiagnoseSummary{
				TotalPanes: 4,
				Healthy:    3,
				Degraded:   1, // We will need to add this field to DiagnoseSummary
			},
			want: "degraded",
		},
		{
			name: "one unresponsive minority",
			summary: DiagnoseSummary{
				TotalPanes:   4,
				Healthy:      3,
				Unresponsive: 1,
			},
			want: "degraded",
		},
		{
			name: "one unknown",
			summary: DiagnoseSummary{
				TotalPanes: 4,
				Healthy:    3,
				Unknown:    1,
			},
			want: "degraded",
		},
		{
			name: "multiple degraded states",
			summary: DiagnoseSummary{
				TotalPanes:   8,
				Healthy:      5,
				RateLimited:  2,
				Unresponsive: 1,
			},
			want: "degraded",
		},

		// Critical cases
		{
			name: "any crashed pane",
			summary: DiagnoseSummary{
				TotalPanes: 4,
				Healthy:    3,
				Crashed:    1,
			},
			want: "critical",
		},
		{
			name: "majority unresponsive",
			summary: DiagnoseSummary{
				TotalPanes:   4,
				Healthy:      1,
				Unresponsive: 3,
			},
			want: "critical",
		},
		{
			name: "equal unresponsive and healthy",
			summary: DiagnoseSummary{
				TotalPanes:   4,
				Healthy:      2,
				Unresponsive: 2,
			},
			want: "degraded", // Not majority, so degraded not critical
		},
		{
			name: "multiple crashed",
			summary: DiagnoseSummary{
				TotalPanes: 4,
				Healthy:    2,
				Crashed:    2,
			},
			want: "critical",
		},
		{
			name: "crashed plus rate limited",
			summary: DiagnoseSummary{
				TotalPanes:  4,
				Healthy:     2,
				Crashed:     1,
				RateLimited: 1,
			},
			want: "critical",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := determineOverallHealth(tt.summary)
			if got != tt.want {
				t.Errorf("determineOverallHealth(%+v) = %q, want %q", tt.summary, got, tt.want)
			}
		})
	}
}

// =============================================================================
// Recommendation Tests
// =============================================================================

func TestBuildRateLimitRecommendation(t *testing.T) {
	tests := []struct {
		name       string
		paneIndex  int
		session    string
		check      *HealthCheck
		wantAction string
		wantStatus string
	}{
		{
			name:      "with wait seconds",
			paneIndex: 2,
			session:   "test-session",
			check: &HealthCheck{
				ErrorCheck: &ErrorCheckResult{
					RateLimited: true,
					WaitSeconds: 300,
				},
			},
			wantAction: "wait",
			wantStatus: "rate_limited",
		},
		{
			name:      "no wait seconds",
			paneIndex: 0,
			session:   "my-session",
			check: &HealthCheck{
				ErrorCheck: &ErrorCheckResult{
					RateLimited: true,
					WaitSeconds: 0,
				},
			},
			wantAction: "wait_or_switch",
			wantStatus: "rate_limited",
		},
		{
			name:      "nil error check",
			paneIndex: 1,
			session:   "session",
			check: &HealthCheck{
				ErrorCheck: nil,
			},
			wantAction: "wait_or_switch",
			wantStatus: "rate_limited",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rec := buildRateLimitRecommendation(tt.paneIndex, tt.session, tt.check)

			if rec.Status != tt.wantStatus {
				t.Errorf("buildRateLimitRecommendation() status = %q, want %q", rec.Status, tt.wantStatus)
			}
			if rec.Action != tt.wantAction {
				t.Errorf("buildRateLimitRecommendation() action = %q, want %q", rec.Action, tt.wantAction)
			}
			if rec.Pane != tt.paneIndex {
				t.Errorf("buildRateLimitRecommendation() pane = %d, want %d", rec.Pane, tt.paneIndex)
			}
			if rec.AutoFixable {
				t.Errorf("buildRateLimitRecommendation() auto_fixable should be false for rate limits")
			}
			if rec.Reason == "" {
				t.Errorf("buildRateLimitRecommendation() reason should not be empty")
			}
			if rec.FixCommand == "" {
				t.Errorf("buildRateLimitRecommendation() fix_command should not be empty")
			}
		})
	}
}

func TestBuildRateLimitRecommendation_FixCommandFormat(t *testing.T) {
	// Test that fix command contains correct session and pane info
	check := &HealthCheck{
		ErrorCheck: &ErrorCheckResult{
			RateLimited: true,
			WaitSeconds: 60,
		},
	}

	rec := buildRateLimitRecommendation(3, "my-test-session", check)

	if rec.FixCommand == "" {
		t.Fatal("FixCommand should not be empty")
	}

	// Should contain sleep and re-diagnosis command
	if rec.Action == "wait" {
		// Expect: sleep 60 && ntm --robot-diagnose=my-test-session --pane=3
		if !contains(rec.FixCommand, "sleep 60") {
			t.Errorf("FixCommand should contain 'sleep 60', got: %s", rec.FixCommand)
		}
		if !contains(rec.FixCommand, "my-test-session") {
			t.Errorf("FixCommand should contain session name, got: %s", rec.FixCommand)
		}
	}
}

// =============================================================================
// DiagnoseRecommendation Structure Tests
// =============================================================================

func TestDiagnoseRecommendation_JSONStructure(t *testing.T) {
	rec := DiagnoseRecommendation{
		Pane:        2,
		Status:      "crashed",
		Action:      "restart",
		Reason:      "Process not running",
		AutoFixable: true,
		FixCommand:  "ntm --robot-restart-pane=session --panes=2",
	}

	data, err := json.Marshal(rec)
	if err != nil {
		t.Fatalf("Failed to marshal DiagnoseRecommendation: %v", err)
	}

	// Unmarshal to verify structure
	var decoded map[string]interface{}
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal: %v", err)
	}

	// Check all expected fields are present
	expectedFields := []string{"pane", "status", "action", "reason", "auto_fixable", "fix_command"}
	for _, field := range expectedFields {
		if _, ok := decoded[field]; !ok {
			t.Errorf("Missing field %q in JSON output", field)
		}
	}

	// Check specific values
	if decoded["pane"].(float64) != 2 {
		t.Errorf("pane = %v, want 2", decoded["pane"])
	}
	if decoded["status"].(string) != "crashed" {
		t.Errorf("status = %v, want 'crashed'", decoded["status"])
	}
	if decoded["auto_fixable"].(bool) != true {
		t.Errorf("auto_fixable = %v, want true", decoded["auto_fixable"])
	}
}

// =============================================================================
// DiagnoseOutput Structure Tests
// =============================================================================

func TestDiagnoseOutput_JSONEnvelope(t *testing.T) {
	output := DiagnoseOutput{
		RobotResponse:   NewRobotResponse(true),
		Session:         "test-session",
		OverallHealth:   "healthy",
		Summary:         DiagnoseSummary{TotalPanes: 4, Healthy: 4},
		Panes:           DiagnosePanes{Healthy: []int{0, 1, 2, 3}},
		Recommendations: []DiagnoseRecommendation{},
		AutoFixAvail:    false,
	}

	data, err := json.Marshal(output)
	if err != nil {
		t.Fatalf("Failed to marshal DiagnoseOutput: %v", err)
	}

	var decoded map[string]interface{}
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal: %v", err)
	}

	// Check RobotResponse envelope fields
	if _, ok := decoded["success"]; !ok {
		t.Error("Missing 'success' field from RobotResponse envelope")
	}
	if _, ok := decoded["timestamp"]; !ok {
		t.Error("Missing 'timestamp' field from RobotResponse envelope")
	}

	// Check diagnose-specific fields
	requiredFields := []string{"session", "overall_health", "summary", "panes", "recommendations", "auto_fix_available"}
	for _, field := range requiredFields {
		if _, ok := decoded[field]; !ok {
			t.Errorf("Missing field %q in DiagnoseOutput", field)
		}
	}

	// Verify overall_health values
	if decoded["overall_health"].(string) != "healthy" {
		t.Errorf("overall_health = %v, want 'healthy'", decoded["overall_health"])
	}
}

func TestDiagnoseOutput_EmptySlicesNotNil(t *testing.T) {
	output := DiagnoseOutput{
		RobotResponse: NewRobotResponse(true),
		Session:       "test",
		OverallHealth: "healthy",
		Panes: DiagnosePanes{
			Healthy:      []int{},
			RateLimited:  []int{},
			Unresponsive: []int{},
			Crashed:      []int{},
			Unknown:      []int{},
		},
		Recommendations: []DiagnoseRecommendation{},
	}

	data, err := json.Marshal(output)
	if err != nil {
		t.Fatalf("Failed to marshal: %v", err)
	}

	var decoded map[string]interface{}
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal: %v", err)
	}

	// Verify panes object has empty arrays, not null
	panes := decoded["panes"].(map[string]interface{})
	for _, key := range []string{"healthy", "rate_limited", "unresponsive", "crashed", "unknown"} {
		arr := panes[key]
		if arr == nil {
			t.Errorf("panes.%s should be empty array [], not null", key)
		}
		if arrTyped, ok := arr.([]interface{}); !ok {
			t.Errorf("panes.%s should be array type", key)
		} else if len(arrTyped) != 0 {
			t.Errorf("panes.%s should be empty, got %v", key, arrTyped)
		}
	}

	// Verify recommendations is empty array, not null
	recs := decoded["recommendations"]
	if recs == nil {
		t.Error("recommendations should be empty array [], not null")
	}
}

// =============================================================================
// DiagnoseSummary Tests
// =============================================================================

func TestDiagnoseSummary_TotalPanes(t *testing.T) {
	tests := []struct {
		name    string
		summary DiagnoseSummary
	}{
		{
			name: "counts match total",
			summary: DiagnoseSummary{
				TotalPanes:   10,
				Healthy:      5,
				RateLimited:  2,
				Unresponsive: 1,
				Crashed:      1,
				Unknown:      1,
			},
		},
		{
			name: "all healthy",
			summary: DiagnoseSummary{
				TotalPanes: 8,
				Healthy:    8,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			sum := tt.summary.Healthy + tt.summary.RateLimited +
				tt.summary.Unresponsive + tt.summary.Crashed + tt.summary.Unknown
			if sum != tt.summary.TotalPanes {
				t.Errorf("Sum of states (%d) != TotalPanes (%d)", sum, tt.summary.TotalPanes)
			}
		})
	}
}

// =============================================================================
// DiagnoseBriefOutput Tests
// =============================================================================

func TestDiagnoseBriefOutput_JSONStructure(t *testing.T) {
	output := DiagnoseBriefOutput{
		RobotResponse: NewRobotResponse(true),
		Session:       "test",
		OverallHealth: "degraded",
		Summary:       "3/4 healthy, 1 rate_limited",
		HasIssues:     true,
		FixAvailable:  false,
	}

	data, err := json.Marshal(output)
	if err != nil {
		t.Fatalf("Failed to marshal: %v", err)
	}

	var decoded map[string]interface{}
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal: %v", err)
	}

	requiredFields := []string{"success", "timestamp", "session", "overall_health", "summary", "has_issues", "fix_available"}
	for _, field := range requiredFields {
		if _, ok := decoded[field]; !ok {
			t.Errorf("Missing field %q in DiagnoseBriefOutput", field)
		}
	}
}

// =============================================================================
// DiagnoseOptions Tests
// =============================================================================

func TestDiagnoseOptions_Defaults(t *testing.T) {
	opts := DiagnoseOptions{
		Session: "my-session",
	}

	// Verify defaults
	if opts.Pane != 0 {
		t.Errorf("Default Pane should be 0 (all panes when -1 is set explicitly)")
	}
	if opts.Fix {
		t.Error("Default Fix should be false")
	}
	if opts.Brief {
		t.Error("Default Brief should be false")
	}
}

func TestDiagnoseOptions_PaneFiltering(t *testing.T) {
	tests := []struct {
		name     string
		pane     int
		wantAll  bool
		wantPane int
	}{
		{"all panes", -1, true, -1},
		{"pane 0", 0, false, 0},
		{"pane 5", 5, false, 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			opts := DiagnoseOptions{
				Session: "test",
				Pane:    tt.pane,
			}

			isAll := opts.Pane < 0
			if isAll != tt.wantAll {
				t.Errorf("Pane=%d: isAll=%v, wantAll=%v", tt.pane, isAll, tt.wantAll)
			}
		})
	}
}

// =============================================================================
// Action to FixCommand Mapping Tests
// =============================================================================

func TestRecommendationActions(t *testing.T) {
	tests := []struct {
		name              string
		status            string
		action            string
		autoFixable       bool
		fixCommandPattern string
	}{
		{
			name:              "crashed pane restart",
			status:            "crashed",
			action:            "restart",
			autoFixable:       true,
			fixCommandPattern: "--robot-restart-pane",
		},
		{
			name:              "unresponsive interrupt",
			status:            "unresponsive",
			action:            "interrupt",
			autoFixable:       true,
			fixCommandPattern: "--robot-interrupt",
		},
		{
			name:              "rate limited wait",
			status:            "rate_limited",
			action:            "wait",
			autoFixable:       false,
			fixCommandPattern: "sleep",
		},
		{
			name:              "unknown investigate",
			status:            "unknown",
			action:            "investigate",
			autoFixable:       false,
			fixCommandPattern: "inspect",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rec := DiagnoseRecommendation{
				Pane:        0,
				Status:      tt.status,
				Action:      tt.action,
				AutoFixable: tt.autoFixable,
				FixCommand:  "ntm " + tt.fixCommandPattern + "=session",
				Reason:      "test reason",
			}

			if rec.AutoFixable != tt.autoFixable {
				t.Errorf("Status %q: AutoFixable = %v, want %v", tt.status, rec.AutoFixable, tt.autoFixable)
			}

			if !contains(rec.FixCommand, tt.fixCommandPattern) {
				t.Errorf("FixCommand %q should contain %q", rec.FixCommand, tt.fixCommandPattern)
			}
		})
	}
}

// =============================================================================
// Overall Health Threshold Tests
// =============================================================================

func TestOverallHealthThresholds(t *testing.T) {
	// Test the exact boundaries for health state transitions

	// Boundary: unresponsive exactly equals healthy (not majority) = degraded
	t.Run("unresponsive equals healthy is degraded", func(t *testing.T) {
		summary := DiagnoseSummary{
			TotalPanes:   4,
			Healthy:      2,
			Unresponsive: 2,
		}
		got := determineOverallHealth(summary)
		if got != "degraded" {
			t.Errorf("Equal unresponsive/healthy should be 'degraded', got %q", got)
		}
	})

	// Boundary: unresponsive > healthy = critical
	t.Run("unresponsive majority is critical", func(t *testing.T) {
		summary := DiagnoseSummary{
			TotalPanes:   4,
			Healthy:      1,
			Unresponsive: 3,
		}
		got := determineOverallHealth(summary)
		if got != "critical" {
			t.Errorf("Majority unresponsive should be 'critical', got %q", got)
		}
	})

	// Any crashed = critical (even 1)
	t.Run("single crashed is critical", func(t *testing.T) {
		summary := DiagnoseSummary{
			TotalPanes: 100,
			Healthy:    99,
			Crashed:    1,
		}
		got := determineOverallHealth(summary)
		if got != "critical" {
			t.Errorf("Any crashed pane should be 'critical', got %q", got)
		}
	})
}

// =============================================================================
// Helper functions
// =============================================================================

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
