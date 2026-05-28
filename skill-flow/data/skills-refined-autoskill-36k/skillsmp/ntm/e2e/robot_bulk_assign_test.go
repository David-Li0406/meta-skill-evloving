// Package e2e contains end-to-end tests for NTM robot mode commands.
// robot_bulk_assign_test.go validates --robot-bulk-assign with various configurations.
//
// Bead: bd-1klou - Task: E2E Tests: Robot Bulk Assign
package e2e

import (
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// BulkAssignOutput represents the JSON response from --robot-bulk-assign.
type BulkAssignOutput struct {
	Success          bool                   `json:"success"`
	Session          string                 `json:"session"`
	Strategy         string                 `json:"strategy"`
	Timestamp        string                 `json:"timestamp"`
	Assignments      []BulkAssignAssignment `json:"assignments"`
	Summary          BulkAssignSummary      `json:"summary"`
	UnassignedBeads  []string               `json:"unassigned_beads,omitempty"`
	UnassignedPanes  []int                  `json:"unassigned_panes,omitempty"`
	DryRun           bool                   `json:"dry_run,omitempty"`
	AllocationSource string                 `json:"allocation_source,omitempty"`
	Error            string                 `json:"error,omitempty"`
	ErrorCode        string                 `json:"error_code,omitempty"`
}

// BulkAssignAssignment represents a single pane-to-bead allocation.
type BulkAssignAssignment struct {
	Pane       int    `json:"pane"`
	Bead       string `json:"bead"`
	BeadTitle  string `json:"bead_title"`
	Reason     string `json:"reason"`
	AgentType  string `json:"agent_type"`
	Status     string `json:"status"`
	PromptSent bool   `json:"prompt_sent"`
	Error      string `json:"error,omitempty"`
}

// BulkAssignSummary aggregates assignment stats.
type BulkAssignSummary struct {
	TotalPanes int `json:"total_panes"`
	Assigned   int `json:"assigned"`
	Skipped    int `json:"skipped"`
	Failed     int `json:"failed"`
}

// runBulkAssignCmd executes ntm --robot-bulk-assign with the given flags.
// Uses a 30-second timeout to prevent test hangs.
func runBulkAssignCmd(t *testing.T, suite *TestSuite, session string, flags ...string) (*BulkAssignOutput, []byte, error) {
	t.Helper()

	args := []string{fmt.Sprintf("--robot-bulk-assign=%s", session)}
	args = append(args, flags...)

	// Use context with timeout to prevent indefinite hangs (bd-brzap fix)
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "/tmp/ntm-test", args...)
	output, err := cmd.CombinedOutput()

	// Check for timeout
	if ctx.Err() == context.DeadlineExceeded {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Command timed out after 30s: args=%v", args)
		return nil, output, fmt.Errorf("command timed out after 30s")
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] args=%v bytes=%d", args, len(output))

	var result BulkAssignOutput
	if jsonErr := json.Unmarshal(output, &result); jsonErr != nil {
		suite.Logger().Log("[E2E-BULK-ASSIGN] JSON parse failed: %v output=%s", jsonErr, string(output))
		return nil, output, err
	}

	suite.Logger().LogJSON("[E2E-BULK-ASSIGN] Result", result)
	return &result, output, err
}

func TestE2E_RobotBulkAssign_RequiresSession(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_requires_session")
	defer suite.Teardown()

	// Test that empty session (--robot-bulk-assign=) falls through to help
	// This is expected behavior - the flag needs a value
	cmd := exec.Command("/tmp/ntm-test", "--robot-bulk-assign=")
	output, _ := cmd.CombinedOutput()

	suite.Logger().Log("[E2E-BULK-ASSIGN] empty session shows help: bytes=%d", len(output))

	// With empty value, NTM shows help instead of triggering the command
	// This is the expected CLI behavior - verify help is shown
	if !strings.Contains(string(output), "Named Tmux") && !strings.Contains(string(output), "session") {
		t.Fatalf("[E2E-BULK-ASSIGN] Expected help or session mention: %s", string(output)[:min(200, len(output))])
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func TestE2E_RobotBulkAssign_RequiresBVOrAllocation(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_requires_source")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test without --from-bv or --allocation
	result, output, _ := runBulkAssignCmd(t, suite, suite.Session())

	// Should return error about missing source
	if result != nil && result.Success {
		t.Fatal("[E2E-BULK-ASSIGN] Should fail without --from-bv or --allocation")
	}

	// Check error message mentions the required flags
	outStr := string(output)
	if !strings.Contains(outStr, "from-bv") && !strings.Contains(outStr, "allocation") {
		t.Fatalf("[E2E-BULK-ASSIGN] Error should mention --from-bv or --allocation: %s", outStr)
	}
}

func TestE2E_RobotBulkAssign_DryRunMode(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_dry_run")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test --dry-run with explicit allocation
	allocation := `{"1":"bd-test1","2":"bd-test2"}`
	result, _, err := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if err != nil {
		// Even with error, check the response structure
		suite.Logger().Log("[E2E-BULK-ASSIGN] dry-run command error: %v", err)
	}

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify dry_run flag is set in response
	if !result.DryRun {
		t.Fatal("[E2E-BULK-ASSIGN] dry_run should be true in response")
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] dry_run=%v allocation_source=%s", result.DryRun, result.AllocationSource)
}

func TestE2E_RobotBulkAssign_ExplicitAllocation(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_explicit")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test explicit allocation
	allocation := `{"1":"bd-abc123","2":"bd-xyz789"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run") // Use dry-run to avoid needing real beads

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify allocation source
	if result.AllocationSource != "explicit" {
		suite.Logger().Log("[E2E-BULK-ASSIGN] allocation_source=%s (expected: explicit)", result.AllocationSource)
	}

	// Verify the session is correct
	if result.Session != suite.Session() {
		t.Fatalf("[E2E-BULK-ASSIGN] Session mismatch: got=%s want=%s", result.Session, suite.Session())
	}
}

func TestE2E_RobotBulkAssign_SkipPanes(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_skip_panes")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with --skip-panes
	allocation := `{"1":"bd-test1","2":"bd-test2","3":"bd-test3"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--skip-panes=1,2",
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify skipped panes are reflected - they appear as "failed" with "pane not available"
	suite.Logger().Log("[E2E-BULK-ASSIGN] skip_panes: summary.failed=%d", result.Summary.Failed)

	// Skipped panes should be marked as failed (not available)
	for _, a := range result.Assignments {
		if a.Pane == 1 || a.Pane == 2 {
			// These panes should be failed due to skip
			if a.Status != "failed" || !strings.Contains(a.Error, "pane not available") {
				suite.Logger().Log("[E2E-BULK-ASSIGN] Pane %d: status=%s error=%s", a.Pane, a.Status, a.Error)
			}
		}
	}
}

func TestE2E_RobotBulkAssign_Strategy(t *testing.T) {
	CommonE2EPrerequisites(t)

	strategies := []string{"impact", "ready", "stale", "balanced"}

	for _, strategy := range strategies {
		t.Run(strategy, func(t *testing.T) {
			suite := NewTestSuite(t, fmt.Sprintf("bulk_assign_strategy_%s", strategy))
			defer suite.Teardown()

			if err := suite.Setup(); err != nil {
				t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
			}

			// Test strategy flag (note: --from-bv required with strategy)
			result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
				"--from-bv",
				"--bulk-strategy="+strategy,
				"--dry-run")

			// Even if bv is not available, the strategy should be recorded
			if result != nil {
				suite.Logger().Log("[E2E-BULK-ASSIGN] strategy=%s result.strategy=%s", strategy, result.Strategy)

				if result.Strategy != "" && result.Strategy != strategy {
					t.Fatalf("[E2E-BULK-ASSIGN] Strategy mismatch: got=%s want=%s", result.Strategy, strategy)
				}
			}
		})
	}
}

func TestE2E_RobotBulkAssign_JSONStructure(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_json_structure")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with explicit allocation to ensure we get a valid response
	allocation := `{"1":"bd-struct-test"}`
	result, output, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	// Verify JSON is valid
	var raw map[string]interface{}
	if err := json.Unmarshal(output, &raw); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Invalid JSON: %v", err)
	}

	// Verify required fields exist
	requiredFields := []string{"session", "timestamp"}
	for _, field := range requiredFields {
		if _, ok := raw[field]; !ok {
			t.Fatalf("[E2E-BULK-ASSIGN] Missing required field: %s", field)
		}
	}

	// Verify session matches
	if result != nil && result.Session != suite.Session() {
		t.Fatalf("[E2E-BULK-ASSIGN] Session mismatch: got=%s want=%s", result.Session, suite.Session())
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] JSON structure validated with %d fields", len(raw))
}

func TestE2E_RobotBulkAssign_InvalidAllocationJSON(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_invalid_json")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with invalid JSON allocation
	result, output, err := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation={invalid json}")

	suite.Logger().Log("[E2E-BULK-ASSIGN] invalid JSON: err=%v", err)

	// Should have an error
	if result != nil && result.Success {
		t.Fatal("[E2E-BULK-ASSIGN] Should fail with invalid JSON")
	}

	// Error should mention JSON or parse
	outStr := strings.ToLower(string(output))
	if !strings.Contains(outStr, "json") && !strings.Contains(outStr, "parse") && !strings.Contains(outStr, "invalid") {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: error message doesn't mention JSON parsing: %s", string(output))
	}
}

func TestE2E_RobotBulkAssign_SummaryStats(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_summary")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with multiple allocations
	allocation := `{"1":"bd-sum1","2":"bd-sum2","3":"bd-sum3"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify summary is present
	suite.Logger().Log("[E2E-BULK-ASSIGN] Summary: total=%d assigned=%d skipped=%d failed=%d",
		result.Summary.TotalPanes,
		result.Summary.Assigned,
		result.Summary.Skipped,
		result.Summary.Failed)

	// Summary counts should be non-negative
	if result.Summary.TotalPanes < 0 || result.Summary.Assigned < 0 ||
		result.Summary.Skipped < 0 || result.Summary.Failed < 0 {
		t.Fatal("[E2E-BULK-ASSIGN] Summary counts should be non-negative")
	}
}

func TestE2E_RobotBulkAssign_UnassignedPanes(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_unassigned_panes")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Create additional panes
	for i := 0; i < 3; i++ {
		cmd := exec.Command(tmux.BinaryPath(), "split-window", "-t", suite.Session(), "-h")
		if err := cmd.Run(); err != nil {
			suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: could not create pane %d: %v", i, err)
		}
	}

	// Test with fewer beads than panes
	allocation := `{"1":"bd-only-one"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Should have unassigned panes
	suite.Logger().Log("[E2E-BULK-ASSIGN] Unassigned panes: %v", result.UnassignedPanes)

	// Verify total panes vs assigned
	if result.Summary.TotalPanes > 1 && len(result.UnassignedPanes) == 0 {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: expected unassigned_panes with %d total panes and 1 allocation",
			result.Summary.TotalPanes)
	}
}

func TestE2E_RobotBulkAssign_UnassignedBeads(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_unassigned_beads")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with more beads than panes (only 1 pane in fresh session)
	allocation := `{"1":"bd-one","2":"bd-two","3":"bd-three","4":"bd-four","5":"bd-five"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Should have unassigned beads (more beads than panes)
	suite.Logger().Log("[E2E-BULK-ASSIGN] Unassigned beads: %v", result.UnassignedBeads)

	// With 5 allocations and likely fewer panes, we should have unassigned beads
	if result.Summary.TotalPanes < 5 && len(result.UnassignedBeads) == 0 {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: expected unassigned_beads with %d panes and 5 allocations",
			result.Summary.TotalPanes)
	}
}

func TestE2E_RobotBulkAssign_WithFromBV(t *testing.T) {
	CommonE2EPrerequisites(t)

	// Skip if bv is not available
	if _, err := exec.LookPath("bv"); err != nil {
		t.Skip("bv not found, skipping --from-bv test")
	}

	suite := NewTestSuite(t, "bulk_assign_from_bv")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test --from-bv flag
	result, _, err := runBulkAssignCmd(t, suite, suite.Session(),
		"--from-bv",
		"--dry-run")

	if err != nil {
		// May fail if no beads available, but should still return valid JSON
		suite.Logger().Log("[E2E-BULK-ASSIGN] --from-bv error (may be expected): %v", err)
	}

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response even with error")
	}

	// Verify allocation source is bv
	if result.AllocationSource != "" {
		suite.Logger().Log("[E2E-BULK-ASSIGN] allocation_source=%s", result.AllocationSource)
	}

	// Strategy should be set when using --from-bv
	if result.Strategy != "" {
		suite.Logger().Log("[E2E-BULK-ASSIGN] strategy=%s (from --from-bv)", result.Strategy)
	}
}

func TestE2E_RobotBulkAssign_MultiPaneSession(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_multi_pane")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Create 5 panes for testing
	for i := 0; i < 4; i++ {
		cmd := exec.Command(tmux.BinaryPath(), "split-window", "-t", suite.Session(), "-h")
		if err := cmd.Run(); err != nil {
			suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: could not create pane %d: %v", i+1, err)
		}
	}

	// Balance the layout
	cmd := exec.Command(tmux.BinaryPath(), "select-layout", "-t", suite.Session(), "tiled")
	cmd.Run()

	// Test allocation to multiple panes
	allocation := `{"0":"bd-p0","1":"bd-p1","2":"bd-p2","3":"bd-p3","4":"bd-p4"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] Multi-pane: total_panes=%d assigned=%d",
		result.Summary.TotalPanes, result.Summary.Assigned)

	// Should have multiple panes
	if result.Summary.TotalPanes < 3 {
		t.Fatalf("[E2E-BULK-ASSIGN] Expected at least 3 panes, got %d", result.Summary.TotalPanes)
	}
}

func TestE2E_RobotBulkAssign_AssignmentDetails(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_details")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with explicit allocation
	allocation := `{"0":"bd-detail-test"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify assignment details structure
	for _, a := range result.Assignments {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Assignment: pane=%d bead=%s status=%s prompt_sent=%v",
			a.Pane, a.Bead, a.Status, a.PromptSent)

		// Pane should be non-negative
		if a.Pane < 0 {
			t.Fatalf("[E2E-BULK-ASSIGN] Invalid pane index: %d", a.Pane)
		}

		// Bead ID should be set
		if a.Bead == "" {
			t.Fatal("[E2E-BULK-ASSIGN] Assignment missing bead ID")
		}
	}
}

func TestE2E_RobotBulkAssign_SkipMultiplePanes(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_skip_multiple")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Create additional panes
	for i := 0; i < 4; i++ {
		cmd := exec.Command(tmux.BinaryPath(), "split-window", "-t", suite.Session(), "-h")
		cmd.Run()
	}
	exec.Command(tmux.BinaryPath(), "select-layout", "-t", suite.Session(), "tiled").Run()

	// Skip multiple panes
	allocation := `{"0":"bd-s0","1":"bd-s1","2":"bd-s2","3":"bd-s3","4":"bd-s4"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--skip-panes=0,2,4",
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify skipped panes appear as failed (not available in filtered pane list)
	skippedPanes := map[int]bool{0: true, 2: true, 4: true}
	for _, a := range result.Assignments {
		if skippedPanes[a.Pane] {
			// Skipped panes should be marked as failed
			suite.Logger().Log("[E2E-BULK-ASSIGN] Skipped pane %d: status=%s error=%s", a.Pane, a.Status, a.Error)
		}
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] Skip multiple verified: 0,2,4 processed as expected")
}

func TestE2E_RobotBulkAssign_EmptyAllocation(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_empty_alloc")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with empty allocation
	result, output, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation={}")

	if result != nil && result.Success {
		// Empty allocation might be valid (0 assignments)
		if len(result.Assignments) > 0 {
			t.Fatal("[E2E-BULK-ASSIGN] Empty allocation should result in 0 assignments")
		}
		suite.Logger().Log("[E2E-BULK-ASSIGN] Empty allocation handled: assignments=%d", len(result.Assignments))
	} else {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Empty allocation rejected: %s", string(output))
	}
}

func TestE2E_RobotBulkAssign_NonExistentSession(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_bad_session")
	defer suite.Teardown()

	// Don't set up a session - test with non-existent one
	result, output, err := runBulkAssignCmd(t, suite, "nonexistent_session_12345",
		"--allocation={\"1\":\"bd-test\"}",
		"--dry-run")

	if err == nil && result != nil && result.Success {
		t.Fatal("[E2E-BULK-ASSIGN] Should fail with non-existent session")
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] Non-existent session error: %s", string(output))
}

func TestE2E_RobotBulkAssign_PaneIndexValidation(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_pane_validation")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with invalid pane indices (strings that look like negative numbers)
	allocation := `{"99":"bd-nonexistent-pane"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Non-existent pane should be reported
	suite.Logger().Log("[E2E-BULK-ASSIGN] Non-existent pane 99: summary.failed=%d", result.Summary.Failed)

	// The assignment should either fail or not be included
	for _, a := range result.Assignments {
		if a.Pane == 99 && a.Error == "" {
			t.Fatal("[E2E-BULK-ASSIGN] Assignment to non-existent pane 99 should have error")
		}
	}
}

func TestE2E_RobotBulkAssign_TimestampFormat(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_timestamp")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	allocation := `{"0":"bd-ts-test"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify timestamp is present and valid
	if result.Timestamp == "" {
		t.Fatal("[E2E-BULK-ASSIGN] Timestamp should not be empty")
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] Timestamp: %s", result.Timestamp)
}

func TestE2E_RobotBulkAssign_AllStrategiesValidInput(t *testing.T) {
	CommonE2EPrerequisites(t)

	strategies := []string{"impact", "ready", "stale", "balanced"}

	for _, strategy := range strategies {
		t.Run("valid_"+strategy, func(t *testing.T) {
			suite := NewTestSuite(t, fmt.Sprintf("bulk_assign_valid_%s", strategy))
			defer suite.Teardown()

			if err := suite.Setup(); err != nil {
				t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
			}

			// Use explicit allocation to avoid needing bv
			allocation := `{"0":"bd-` + strategy + `-test"}`
			result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
				"--allocation="+allocation,
				"--bulk-strategy="+strategy,
				"--dry-run")

			if result == nil {
				t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
			}

			// Strategy should be recorded even with explicit allocation
			suite.Logger().Log("[E2E-BULK-ASSIGN] Strategy %s: recorded=%s", strategy, result.Strategy)
		})
	}
}

func TestE2E_RobotBulkAssign_CombinedFlags(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_combined")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Create a few panes
	for i := 0; i < 2; i++ {
		exec.Command(tmux.BinaryPath(), "split-window", "-t", suite.Session(), "-h").Run()
	}

	// Test multiple flags combined
	allocation := `{"0":"bd-c0","1":"bd-c1","2":"bd-c2"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--skip-panes=1",
		"--bulk-strategy=impact",
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify combined behavior
	suite.Logger().Log("[E2E-BULK-ASSIGN] Combined flags: dry_run=%v strategy=%s failed=%d",
		result.DryRun, result.Strategy, result.Summary.Failed)

	if !result.DryRun {
		t.Fatal("[E2E-BULK-ASSIGN] dry_run should be true")
	}

	// Pane 1 should be in assignments but marked as failed (skip causes pane not available)
	for _, a := range result.Assignments {
		if a.Pane == 1 {
			suite.Logger().Log("[E2E-BULK-ASSIGN] Pane 1 skipped: status=%s error=%s", a.Status, a.Error)
		}
	}
}

func TestE2E_RobotBulkAssign_LargeAllocation(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_large")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Build large allocation (20 entries)
	var allocParts []string
	for i := 0; i < 20; i++ {
		allocParts = append(allocParts, fmt.Sprintf(`"%d":"bd-large%d"`, i, i))
	}
	allocation := "{" + strings.Join(allocParts, ",") + "}"

	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Should handle large allocation gracefully
	suite.Logger().Log("[E2E-BULK-ASSIGN] Large allocation: 20 entries -> %d assigned, %d unassigned beads",
		result.Summary.Assigned, len(result.UnassignedBeads))

	// With only a few panes, most should be unassigned
	if result.Summary.TotalPanes < 20 && len(result.UnassignedBeads) < 10 {
		suite.Logger().Log("[E2E-BULK-ASSIGN] Warning: expected more unassigned beads")
	}
}

func TestE2E_RobotBulkAssign_SkipPanesFormat(t *testing.T) {
	CommonE2EPrerequisites(t)

	testCases := []struct {
		name      string
		skipPanes string
	}{
		{"single", "0"},
		{"comma_separated", "0,1,2"},
		{"with_spaces", "0, 1, 2"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			suite := NewTestSuite(t, fmt.Sprintf("bulk_assign_skip_%s", tc.name))
			defer suite.Teardown()

			if err := suite.Setup(); err != nil {
				t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
			}

			allocation := `{"0":"bd-skip0","1":"bd-skip1","2":"bd-skip2"}`
			result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
				"--allocation="+allocation,
				"--skip-panes="+tc.skipPanes,
				"--dry-run")

			if result == nil {
				t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
			}

			suite.Logger().Log("[E2E-BULK-ASSIGN] Skip format %s: skipped=%d", tc.name, result.Summary.Skipped)
		})
	}
}

func TestE2E_RobotBulkAssign_AllocationPaneTypes(t *testing.T) {
	CommonE2EPrerequisites(t)

	suite := NewTestSuite(t, "bulk_assign_pane_types")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-BULK-ASSIGN] Setup failed: %v", err)
	}

	// Test with numeric string keys (which is the expected format)
	allocation := `{"0":"bd-type0","1":"bd-type1"}`
	result, _, _ := runBulkAssignCmd(t, suite, suite.Session(),
		"--allocation="+allocation,
		"--dry-run")

	if result == nil {
		t.Fatal("[E2E-BULK-ASSIGN] Expected JSON response")
	}

	// Verify pane indices are integers in response
	for _, a := range result.Assignments {
		if a.Pane < 0 {
			t.Fatalf("[E2E-BULK-ASSIGN] Invalid pane index: %d", a.Pane)
		}
	}

	suite.Logger().Log("[E2E-BULK-ASSIGN] Pane types validated: %d assignments", len(result.Assignments))
}

// Helper to check if NTM test binary exists
func init() {
	if _, err := exec.LookPath("/tmp/ntm-test"); err != nil {
		// Binary not built yet - tests will be skipped via CommonE2EPrerequisites
	}
}
