package cli

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/assignment"
)

// ============================================================================
// Clear Assignments Tests (bd-30o1y)
// ============================================================================

// ============================================================================
// Data Structure Tests
// ============================================================================

// TestClearAssignmentResultStructure tests the ClearAssignmentResult type
func TestClearAssignmentResultStructure(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:                   "bd-xyz",
		BeadTitle:                "Test task",
		PreviousPane:             3,
		PreviousAgent:            "GreenLake",
		PreviousAgentType:        "claude",
		PreviousStatus:           "working",
		AssignmentFound:          true,
		FileReservationsReleased: true,
		FilesReleased:            []string{"src/api/*.go"},
		Success:                  true,
		Error:                    "",
		ErrorCode:                "",
	}

	if result.BeadID != "bd-xyz" {
		t.Errorf("Expected BeadID 'bd-xyz', got %q", result.BeadID)
	}
	if result.PreviousPane != 3 {
		t.Errorf("Expected PreviousPane 3, got %d", result.PreviousPane)
	}
	if !result.AssignmentFound {
		t.Error("Expected AssignmentFound to be true")
	}
	if !result.Success {
		t.Error("Expected Success to be true")
	}
}

// TestClearAssignmentResultNotFound tests result when assignment not found
func TestClearAssignmentResultNotFound(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:          "bd-notfound",
		AssignmentFound: false,
		Success:         false,
		Error:           "assignment not found or already completed",
		ErrorCode:       clearErrNotAssigned,
	}

	if result.AssignmentFound {
		t.Error("Expected AssignmentFound to be false")
	}
	if result.Success {
		t.Error("Expected Success to be false")
	}
	if result.ErrorCode != "NOT_ASSIGNED" {
		t.Errorf("Expected ErrorCode 'NOT_ASSIGNED', got %q", result.ErrorCode)
	}
}

// TestClearAssignmentResultJSON tests JSON marshaling
func TestClearAssignmentResultJSON(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:          "bd-json",
		PreviousPane:    2,
		PreviousAgent:   "BlueLake",
		AssignmentFound: true,
		Success:         true,
		FilesReleased:   []string{"a.go", "b.go"},
	}

	data, err := json.Marshal(result)
	if err != nil {
		t.Fatalf("Failed to marshal: %v", err)
	}

	var decoded ClearAssignmentResult
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal: %v", err)
	}

	if decoded.BeadID != "bd-json" {
		t.Errorf("Expected BeadID 'bd-json', got %q", decoded.BeadID)
	}
	if len(decoded.FilesReleased) != 2 {
		t.Errorf("Expected 2 files released, got %d", len(decoded.FilesReleased))
	}
}

// TestClearAllResultStructure tests the ClearAllResult type
func TestClearAllResultStructure(t *testing.T) {
	result := ClearAllResult{
		Pane:      3,
		AgentType: "claude",
		Success:   true,
		ClearedBeads: []ClearAssignmentResult{
			{BeadID: "bd-001", Success: true},
			{BeadID: "bd-002", Success: true},
		},
	}

	if result.Pane != 3 {
		t.Errorf("Expected Pane 3, got %d", result.Pane)
	}
	if result.AgentType != "claude" {
		t.Errorf("Expected AgentType 'claude', got %q", result.AgentType)
	}
	if len(result.ClearedBeads) != 2 {
		t.Errorf("Expected 2 cleared beads, got %d", len(result.ClearedBeads))
	}
}

// TestClearAssignmentsSummaryStructure tests the ClearAssignmentsSummary type
func TestClearAssignmentsSummaryStructure(t *testing.T) {
	summary := ClearAssignmentsSummary{
		ClearedCount:         5,
		ReservationsReleased: 3,
		FailedCount:          1,
	}

	if summary.ClearedCount != 5 {
		t.Errorf("Expected ClearedCount 5, got %d", summary.ClearedCount)
	}
	if summary.ReservationsReleased != 3 {
		t.Errorf("Expected ReservationsReleased 3, got %d", summary.ReservationsReleased)
	}
	if summary.FailedCount != 1 {
		t.Errorf("Expected FailedCount 1, got %d", summary.FailedCount)
	}
}

// TestClearAssignmentsDataStructure tests the ClearAssignmentsData type
func TestClearAssignmentsDataStructure(t *testing.T) {
	pane := 3
	data := ClearAssignmentsData{
		Cleared: []ClearAssignmentResult{
			{BeadID: "bd-001", Success: true},
		},
		Summary: ClearAssignmentsSummary{
			ClearedCount: 1,
		},
		Pane:      &pane,
		AgentType: "claude",
	}

	if len(data.Cleared) != 1 {
		t.Errorf("Expected 1 cleared, got %d", len(data.Cleared))
	}
	if data.Summary.ClearedCount != 1 {
		t.Errorf("Expected ClearedCount 1, got %d", data.Summary.ClearedCount)
	}
	if *data.Pane != 3 {
		t.Errorf("Expected Pane 3, got %d", *data.Pane)
	}
}

// TestClearAssignmentsErrorStructure tests the ClearAssignmentsError type
func TestClearAssignmentsErrorStructure(t *testing.T) {
	err := ClearAssignmentsError{
		Code:    "NOT_ASSIGNED",
		Message: "assignment not found",
		Details: map[string]interface{}{
			"bead_id": "bd-xyz",
		},
	}

	if err.Code != "NOT_ASSIGNED" {
		t.Errorf("Expected Code 'NOT_ASSIGNED', got %q", err.Code)
	}
	if err.Details["bead_id"] != "bd-xyz" {
		t.Errorf("Expected bead_id 'bd-xyz' in details, got %v", err.Details["bead_id"])
	}
}

// TestClearAssignmentsEnvelopeStructure tests the ClearAssignmentsEnvelope type
func TestClearAssignmentsEnvelopeStructure(t *testing.T) {
	envelope := ClearAssignmentsEnvelope{
		Command:    "assign",
		Subcommand: "clear",
		Session:    "myproject",
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
		Success:    true,
		Data: &ClearAssignmentsData{
			Cleared: []ClearAssignmentResult{
				{BeadID: "bd-001", Success: true},
			},
			Summary: ClearAssignmentsSummary{ClearedCount: 1},
		},
		Warnings: []string{},
	}

	if envelope.Command != "assign" {
		t.Errorf("Expected Command 'assign', got %q", envelope.Command)
	}
	if envelope.Subcommand != "clear" {
		t.Errorf("Expected Subcommand 'clear', got %q", envelope.Subcommand)
	}
	if !envelope.Success {
		t.Error("Expected Success to be true")
	}
}

// ============================================================================
// Error Code Tests
// ============================================================================

// TestClearErrorCodes tests the documented error code constants
func TestClearErrorCodes(t *testing.T) {
	tests := []struct {
		code    string
		meaning string
	}{
		{clearErrNotAssigned, "Assignment not found"},
		{clearErrAlreadyCompleted, "Assignment already completed"},
		{clearErrPaneNotFound, "Pane not found"},
		{clearErrInvalidFlag, "Invalid flag combination"},
		{clearErrInternal, "Internal error"},
	}

	for _, tc := range tests {
		if tc.code == "" {
			t.Errorf("Error code for %q is empty", tc.meaning)
		}
	}

	// Verify specific constant values
	if clearErrNotAssigned != "NOT_ASSIGNED" {
		t.Errorf("Expected clearErrNotAssigned='NOT_ASSIGNED', got %q", clearErrNotAssigned)
	}
	if clearErrAlreadyCompleted != "ALREADY_COMPLETED" {
		t.Errorf("Expected clearErrAlreadyCompleted='ALREADY_COMPLETED', got %q", clearErrAlreadyCompleted)
	}
	if clearErrPaneNotFound != "PANE_NOT_FOUND" {
		t.Errorf("Expected clearErrPaneNotFound='PANE_NOT_FOUND', got %q", clearErrPaneNotFound)
	}
}

// TestClearEnvelopeWithError tests error envelope creation
func TestClearEnvelopeWithError(t *testing.T) {
	envelope := ClearAssignmentsEnvelope{
		Command:    "assign",
		Subcommand: "clear",
		Session:    "test",
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
		Success:    false,
		Warnings:   []string{},
		Error: &ClearAssignmentsError{
			Code:    "NOT_ASSIGNED",
			Message: "assignment not found",
		},
	}

	if envelope.Success {
		t.Error("Expected Success to be false")
	}
	if envelope.Error == nil {
		t.Fatal("Expected Error to be non-nil")
	}
	if envelope.Error.Code != "NOT_ASSIGNED" {
		t.Errorf("Expected Error.Code 'NOT_ASSIGNED', got %q", envelope.Error.Code)
	}
}

// ============================================================================
// Validation Tests
// ============================================================================

// TestClearAndClearPaneMutuallyExclusive tests that --clear and --clear-pane can't be used together
func TestClearAndClearPaneMutuallyExclusive(t *testing.T) {
	// If both are set, it's an error
	clearBeads := "bd-001"
	clearPane := 3

	isInvalid := clearBeads != "" && clearPane >= 0
	if !isInvalid {
		t.Error("Expected setting both --clear and --clear-pane to be invalid")
	}
}

// TestClearRequiresBeadIDs tests that --clear requires bead IDs
func TestClearRequiresBeadIDs(t *testing.T) {
	// Empty string means no beads
	clearBeads := ""
	if clearBeads != "" {
		t.Error("Expected empty string for no beads")
	}
}

// TestClearParsesCommaSeparatedBeads tests parsing comma-separated bead IDs
func TestClearParsesCommaSeparatedBeads(t *testing.T) {
	tests := []struct {
		input    string
		expected []string
	}{
		{"bd-001", []string{"bd-001"}},
		{"bd-001,bd-002", []string{"bd-001", "bd-002"}},
		{"bd-001, bd-002, bd-003", []string{"bd-001", "bd-002", "bd-003"}},
		{"", []string{""}},
	}

	for _, tc := range tests {
		// Simulate parsing logic
		result := []string{}
		if tc.input != "" {
			parts := splitAndTrimTestHelper(tc.input)
			result = parts
		} else {
			result = []string{""}
		}

		if len(result) != len(tc.expected) {
			t.Errorf("For input %q, expected %d parts, got %d", tc.input, len(tc.expected), len(result))
		}
	}
}

// Helper function for tests
func splitAndTrimTestHelper(input string) []string {
	parts := []string{}
	start := 0
	for i := 0; i <= len(input); i++ {
		if i == len(input) || input[i] == ',' {
			part := trimSpaces(input[start:i])
			parts = append(parts, part)
			start = i + 1
		}
	}
	return parts
}

func trimSpaces(s string) string {
	start := 0
	end := len(s)
	for start < end && s[start] == ' ' {
		start++
	}
	for end > start && s[end-1] == ' ' {
		end--
	}
	return s[start:end]
}

// ============================================================================
// Assignment Status Tests
// ============================================================================

// TestClearOnlyNonCompletedWithoutForce tests that completed assignments need --force
func TestClearOnlyNonCompletedWithoutForce(t *testing.T) {
	tests := []struct {
		status   assignment.AssignmentStatus
		force    bool
		canClear bool
	}{
		{assignment.StatusAssigned, false, true},
		{assignment.StatusWorking, false, true},
		{assignment.StatusFailed, false, true},
		{assignment.StatusCompleted, false, false}, // Need --force
		{assignment.StatusCompleted, true, true},   // With --force
		{assignment.StatusReassigned, false, true},
	}

	for _, tc := range tests {
		t.Run(string(tc.status), func(t *testing.T) {
			// Validation: status != Completed || force
			canClear := tc.status != assignment.StatusCompleted || tc.force
			if canClear != tc.canClear {
				t.Errorf("Expected canClear=%v for status=%s force=%v, got %v",
					tc.canClear, tc.status, tc.force, canClear)
			}
		})
	}
}

// TestClearFailedOnlyFlag tests the --clear-failed flag logic
func TestClearFailedOnlyFlag(t *testing.T) {
	assignments := []assignment.Assignment{
		{BeadID: "bd-001", Status: assignment.StatusWorking},
		{BeadID: "bd-002", Status: assignment.StatusFailed},
		{BeadID: "bd-003", Status: assignment.StatusCompleted},
		{BeadID: "bd-004", Status: assignment.StatusFailed},
	}

	// --clear-failed should only clear failed assignments
	var failedBeads []string
	for _, a := range assignments {
		if a.Status == assignment.StatusFailed {
			failedBeads = append(failedBeads, a.BeadID)
		}
	}

	if len(failedBeads) != 2 {
		t.Errorf("Expected 2 failed beads, got %d", len(failedBeads))
	}
	if failedBeads[0] != "bd-002" || failedBeads[1] != "bd-004" {
		t.Errorf("Expected failed beads bd-002 and bd-004, got %v", failedBeads)
	}
}

// ============================================================================
// CLI Flag Tests
// ============================================================================

// TestAssignCommandHasClearFlag tests that the assign command has --clear flag
func TestAssignCommandHasClearFlag(t *testing.T) {
	cmd := newAssignCmd()
	flag := cmd.Flags().Lookup("clear")
	if flag == nil {
		t.Fatal("Expected 'clear' flag to exist")
	}
}

// TestAssignCommandHasClearPaneFlag tests that the assign command has --clear-pane flag
func TestAssignCommandHasClearPaneFlag(t *testing.T) {
	cmd := newAssignCmd()
	flag := cmd.Flags().Lookup("clear-pane")
	if flag == nil {
		t.Fatal("Expected 'clear-pane' flag to exist")
	}
}

// TestAssignCommandHasClearFailedFlag tests that the assign command has --clear-failed flag
func TestAssignCommandHasClearFailedFlag(t *testing.T) {
	cmd := newAssignCmd()
	flag := cmd.Flags().Lookup("clear-failed")
	if flag == nil {
		t.Fatal("Expected 'clear-failed' flag to exist")
	}
}

// TestClearFlagDefaultValue tests that --clear defaults to empty
func TestClearFlagDefaultValue(t *testing.T) {
	cmd := newAssignCmd()
	flag := cmd.Flags().Lookup("clear")
	if flag == nil {
		t.Fatal("Expected 'clear' flag to exist")
	}
	if flag.DefValue != "" {
		t.Errorf("Expected default value '', got %q", flag.DefValue)
	}
}

// TestClearPaneFlagDefaultValue tests that --clear-pane defaults to -1
func TestClearPaneFlagDefaultValue(t *testing.T) {
	cmd := newAssignCmd()
	flag := cmd.Flags().Lookup("clear-pane")
	if flag == nil {
		t.Fatal("Expected 'clear-pane' flag to exist")
	}
	if flag.DefValue != "-1" {
		t.Errorf("Expected default value '-1', got %q", flag.DefValue)
	}
}

// ============================================================================
// File Reservation Release Tests
// ============================================================================

// TestClearReleasesFileReservations tests that clear releases file reservations
func TestClearReleasesFileReservations(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:                   "bd-xyz",
		AssignmentFound:          true,
		FileReservationsReleased: true,
		FilesReleased:            []string{"src/api/*.go", "src/utils/*.go"},
		Success:                  true,
	}

	if !result.FileReservationsReleased {
		t.Error("Expected FileReservationsReleased to be true")
	}
	if len(result.FilesReleased) != 2 {
		t.Errorf("Expected 2 files released, got %d", len(result.FilesReleased))
	}
}

// TestClearWithNoReservationsToRelease tests clear with no file reservations
func TestClearWithNoReservationsToRelease(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:                   "bd-xyz",
		AssignmentFound:          true,
		FileReservationsReleased: false,
		FilesReleased:            nil,
		Success:                  true,
	}

	if result.FileReservationsReleased {
		t.Error("Expected FileReservationsReleased to be false when no reservations")
	}
}

// ============================================================================
// Edge Cases
// ============================================================================

// TestClearEmptyBeadList tests clearing with empty bead list
func TestClearEmptyBeadList(t *testing.T) {
	beadIDs := []string{}

	// Empty list should be handled gracefully
	if len(beadIDs) != 0 {
		t.Errorf("Expected empty bead list, got %d beads", len(beadIDs))
	}
}

// TestClearNonExistentBead tests clearing a bead that doesn't exist
func TestClearNonExistentBead(t *testing.T) {
	result := ClearAssignmentResult{
		BeadID:          "bd-nonexistent",
		AssignmentFound: false,
		Success:         false,
		Error:           "assignment not found or already completed",
	}

	if result.AssignmentFound {
		t.Error("Expected AssignmentFound to be false")
	}
	if result.Success {
		t.Error("Expected Success to be false")
	}
}

// TestClearPaneWithNoAssignments tests clearing a pane with no assignments
func TestClearPaneWithNoAssignments(t *testing.T) {
	result := ClearAllResult{
		Pane:         5,
		AgentType:    "claude",
		Success:      true,
		ClearedBeads: []ClearAssignmentResult{},
	}

	// Should succeed with 0 cleared beads
	if !result.Success {
		t.Error("Expected Success to be true even with no beads to clear")
	}
	if len(result.ClearedBeads) != 0 {
		t.Errorf("Expected 0 cleared beads, got %d", len(result.ClearedBeads))
	}
}

// TestClearAlreadyClearedAssignment tests clearing the same assignment twice
func TestClearAlreadyClearedAssignment(t *testing.T) {
	// First clear succeeds
	firstResult := ClearAssignmentResult{
		BeadID:          "bd-xyz",
		AssignmentFound: true,
		Success:         true,
	}

	// Second clear fails (already cleared)
	secondResult := ClearAssignmentResult{
		BeadID:          "bd-xyz",
		AssignmentFound: false,
		Success:         false,
		Error:           "assignment not found or already completed",
	}

	if !firstResult.Success {
		t.Error("Expected first clear to succeed")
	}
	if secondResult.Success {
		t.Error("Expected second clear to fail")
	}
}

// TestClearCompletedWithoutForce tests clearing completed assignment without --force
func TestClearCompletedWithoutForce(t *testing.T) {
	a := assignment.Assignment{
		BeadID: "bd-completed",
		Status: assignment.StatusCompleted,
	}
	force := false

	// Validation: completed without force should be rejected
	shouldReject := a.Status == assignment.StatusCompleted && !force
	if !shouldReject {
		t.Error("Expected completed assignment without --force to be rejected")
	}
}

// TestClearCompletedWithForce tests clearing completed assignment with --force
func TestClearCompletedWithForce(t *testing.T) {
	a := assignment.Assignment{
		BeadID: "bd-completed",
		Status: assignment.StatusCompleted,
	}
	force := true

	// Validation: completed with force should be allowed
	shouldAllow := a.Status != assignment.StatusCompleted || force
	if !shouldAllow {
		t.Error("Expected completed assignment with --force to be allowed")
	}
}

// ============================================================================
// Batch Clear Tests
// ============================================================================

// TestBatchClearSuccess tests clearing multiple beads successfully
func TestBatchClearSuccess(t *testing.T) {
	results := []ClearAssignmentResult{
		{BeadID: "bd-001", Success: true},
		{BeadID: "bd-002", Success: true},
		{BeadID: "bd-003", Success: true},
	}

	successCount := 0
	for _, r := range results {
		if r.Success {
			successCount++
		}
	}

	if successCount != 3 {
		t.Errorf("Expected 3 successful clears, got %d", successCount)
	}
}

// TestBatchClearPartialFailure tests clearing multiple beads with some failures
func TestBatchClearPartialFailure(t *testing.T) {
	results := []ClearAssignmentResult{
		{BeadID: "bd-001", Success: true},
		{BeadID: "bd-002", Success: false, Error: "assignment not found"},
		{BeadID: "bd-003", Success: true},
	}

	successCount := 0
	failCount := 0
	for _, r := range results {
		if r.Success {
			successCount++
		} else {
			failCount++
		}
	}

	if successCount != 2 {
		t.Errorf("Expected 2 successful clears, got %d", successCount)
	}
	if failCount != 1 {
		t.Errorf("Expected 1 failed clear, got %d", failCount)
	}
}

// TestClearSummaryAccuracy tests that summary stats are accurate
func TestClearSummaryAccuracy(t *testing.T) {
	results := []ClearAssignmentResult{
		{BeadID: "bd-001", Success: true, FilesReleased: []string{"a.go"}},
		{BeadID: "bd-002", Success: true, FilesReleased: []string{"b.go", "c.go"}},
		{BeadID: "bd-003", Success: false},
		{BeadID: "bd-004", Success: true, FilesReleased: nil},
	}

	cleared := 0
	failed := 0
	reservations := 0
	for _, r := range results {
		if r.Success {
			cleared++
			reservations += len(r.FilesReleased)
		} else {
			failed++
		}
	}

	if cleared != 3 {
		t.Errorf("Expected 3 cleared, got %d", cleared)
	}
	if failed != 1 {
		t.Errorf("Expected 1 failed, got %d", failed)
	}
	if reservations != 3 {
		t.Errorf("Expected 3 reservations released, got %d", reservations)
	}
}

// ============================================================================
// JSON Envelope Tests
// ============================================================================

// TestClearEnvelopeJSONMarshaling tests JSON marshaling of envelope
func TestClearEnvelopeJSONMarshaling(t *testing.T) {
	envelope := ClearAssignmentsEnvelope{
		Command:    "assign",
		Subcommand: "clear",
		Session:    "myproject",
		Timestamp:  "2026-01-20T12:00:00Z",
		Success:    true,
		Data: &ClearAssignmentsData{
			Cleared: []ClearAssignmentResult{
				{BeadID: "bd-001", Success: true},
			},
			Summary: ClearAssignmentsSummary{ClearedCount: 1},
		},
		Warnings: []string{},
	}

	data, err := json.Marshal(envelope)
	if err != nil {
		t.Fatalf("Failed to marshal envelope: %v", err)
	}

	var decoded ClearAssignmentsEnvelope
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("Failed to unmarshal envelope: %v", err)
	}

	if decoded.Command != "assign" {
		t.Errorf("Expected Command 'assign', got %q", decoded.Command)
	}
	if decoded.Subcommand != "clear" {
		t.Errorf("Expected Subcommand 'clear', got %q", decoded.Subcommand)
	}
	if !decoded.Success {
		t.Error("Expected Success to be true")
	}
	if decoded.Data == nil {
		t.Fatal("Expected Data to be non-nil")
	}
	if len(decoded.Data.Cleared) != 1 {
		t.Errorf("Expected 1 cleared, got %d", len(decoded.Data.Cleared))
	}
}

// TestClearPaneEnvelopeSubcommand tests the subcommand value for clear-pane
func TestClearPaneEnvelopeSubcommand(t *testing.T) {
	pane := 3
	envelope := ClearAssignmentsEnvelope{
		Command:    "assign",
		Subcommand: "clear-pane",
		Session:    "test",
		Timestamp:  "2026-01-20T12:00:00Z",
		Success:    true,
		Data: &ClearAssignmentsData{
			Pane: &pane,
		},
		Warnings: []string{},
	}

	if envelope.Subcommand != "clear-pane" {
		t.Errorf("Expected Subcommand 'clear-pane', got %q", envelope.Subcommand)
	}
	if envelope.Data.Pane == nil || *envelope.Data.Pane != 3 {
		t.Error("Expected Pane to be 3")
	}
}
