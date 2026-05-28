// Package tests provides unit tests for assign --clear logic using the assignment store.
package tests

import (
	"os"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/assignment"
)

func setupClearTestStore(t *testing.T) *assignment.AssignmentStore {
	t.Helper()
	tmpDir := t.TempDir()
	os.Setenv("XDG_DATA_HOME", tmpDir)
	t.Cleanup(func() { os.Unsetenv("XDG_DATA_HOME") })

	return assignment.NewStore("clear-test")
}

func createAssignmentWithStatus(t *testing.T, store *assignment.AssignmentStore, beadID string, pane int, status assignment.AssignmentStatus) {
	t.Helper()
	_, err := store.Assign(beadID, "Test "+beadID, pane, "claude", "TestAgent", "Do the task")
	if err != nil {
		t.Fatalf("failed to create assignment %s: %v", beadID, err)
	}
	switch status {
	case assignment.StatusAssigned:
		return
	case assignment.StatusWorking:
		if err := store.MarkWorking(beadID); err != nil {
			t.Fatalf("failed to mark working for %s: %v", beadID, err)
		}
	case assignment.StatusCompleted:
		if err := store.MarkWorking(beadID); err != nil {
			t.Fatalf("failed to mark working for %s: %v", beadID, err)
		}
		if err := store.MarkCompleted(beadID); err != nil {
			t.Fatalf("failed to mark completed for %s: %v", beadID, err)
		}
	case assignment.StatusFailed:
		if err := store.MarkFailed(beadID, "agent crashed"); err != nil {
			t.Fatalf("failed to mark failed for %s: %v", beadID, err)
		}
	default:
		t.Fatalf("unsupported status: %s", status)
	}
}

func TestClearSingleAssignment_RemovesAssignment(t *testing.T) {
	store := setupClearTestStore(t)

	createAssignmentWithStatus(t, store, "bd-1", 1, assignment.StatusAssigned)
	if store.Get("bd-1") == nil {
		t.Fatal("expected assignment to exist before clear")
	}

	store.Remove("bd-1")
	if store.Get("bd-1") != nil {
		t.Fatal("expected assignment to be removed after clear")
	}
}

func TestClearMultipleAssignments_RemovesOnlyTargets(t *testing.T) {
	store := setupClearTestStore(t)

	createAssignmentWithStatus(t, store, "bd-1", 1, assignment.StatusAssigned)
	createAssignmentWithStatus(t, store, "bd-2", 2, assignment.StatusAssigned)
	createAssignmentWithStatus(t, store, "bd-3", 3, assignment.StatusAssigned)

	store.Remove("bd-1")
	store.Remove("bd-3")

	if store.Get("bd-1") != nil || store.Get("bd-3") != nil {
		t.Fatal("expected cleared assignments to be removed")
	}
	if store.Get("bd-2") == nil {
		t.Fatal("expected non-cleared assignment to remain")
	}
}

func TestClearByPane_RemovesOnlyPaneAssignments(t *testing.T) {
	store := setupClearTestStore(t)

	createAssignmentWithStatus(t, store, "bd-1", 1, assignment.StatusAssigned)
	createAssignmentWithStatus(t, store, "bd-2", 3, assignment.StatusAssigned)
	createAssignmentWithStatus(t, store, "bd-3", 3, assignment.StatusWorking)

	for _, a := range store.ListByPane(3) {
		store.Remove(a.BeadID)
	}

	if store.Get("bd-1") == nil {
		t.Fatal("expected assignment on other pane to remain")
	}
	if store.Get("bd-2") != nil || store.Get("bd-3") != nil {
		t.Fatal("expected pane assignments to be cleared")
	}
}

func TestClearFailed_RemovesOnlyFailedAssignments(t *testing.T) {
	store := setupClearTestStore(t)

	createAssignmentWithStatus(t, store, "bd-fail-1", 1, assignment.StatusFailed)
	createAssignmentWithStatus(t, store, "bd-fail-2", 2, assignment.StatusFailed)
	createAssignmentWithStatus(t, store, "bd-working", 3, assignment.StatusWorking)

	for _, a := range store.ListByStatus(assignment.StatusFailed) {
		store.Remove(a.BeadID)
	}

	if store.Get("bd-working") == nil {
		t.Fatal("expected non-failed assignment to remain")
	}
	if store.Get("bd-fail-1") != nil || store.Get("bd-fail-2") != nil {
		t.Fatal("expected failed assignments to be cleared")
	}
}

func TestClearCompleted_RequiresForce(t *testing.T) {
	store := setupClearTestStore(t)

	createAssignmentWithStatus(t, store, "bd-complete", 1, assignment.StatusCompleted)

	clearWithForce := func(beadID string, force bool) bool {
		a := store.Get(beadID)
		if a == nil {
			return false
		}
		if a.Status == assignment.StatusCompleted && !force {
			return false
		}
		store.Remove(beadID)
		return true
	}

	if clearWithForce("bd-complete", false) {
		t.Fatal("expected clear without force to be rejected for completed assignment")
	}
	if store.Get("bd-complete") == nil {
		t.Fatal("expected completed assignment to remain without force")
	}

	if !clearWithForce("bd-complete", true) {
		t.Fatal("expected clear with force to succeed for completed assignment")
	}
	if store.Get("bd-complete") != nil {
		t.Fatal("expected completed assignment to be removed with force")
	}
}
