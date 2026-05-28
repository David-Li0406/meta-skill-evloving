package approval

import (
	"context"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/events"
	"github.com/Dicklesworthstone/ntm/internal/state"
)

func setupTestStore(t *testing.T) *state.Store {
	t.Helper()
	tmpDir := t.TempDir()
	dbPath := filepath.Join(tmpDir, "test.db")

	store, err := state.Open(dbPath)
	if err != nil {
		t.Fatalf("Failed to open store: %v", err)
	}

	// Run migrations to create tables
	if err := store.Migrate(); err != nil {
		t.Fatalf("Failed to migrate store: %v", err)
	}

	t.Cleanup(func() {
		store.Close()
		os.Remove(dbPath)
	})

	return store
}

func TestNewEngine(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())
	if engine == nil {
		t.Fatal("New returned nil")
	}
}

func TestRequest(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, err := engine.Request(ctx, RequestParams{
		Action:      "force_release",
		Resource:    "internal/auth/**",
		Reason:      "Agent crashed",
		RequestedBy: "system",
	})

	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}

	if approval.ID == "" {
		t.Error("Approval ID should be set")
	}
	if approval.Status != state.ApprovalPending {
		t.Errorf("Status should be pending, got %s", approval.Status)
	}
	if approval.Action != "force_release" {
		t.Errorf("Action should be force_release, got %s", approval.Action)
	}
}

func TestCheck(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	created, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "tester",
	})

	checked, err := engine.Check(ctx, created.ID)
	if err != nil {
		t.Fatalf("Check failed: %v", err)
	}

	if checked.ID != created.ID {
		t.Error("Checked ID doesn't match created ID")
	}
	if checked.Status != state.ApprovalPending {
		t.Errorf("Status should be pending, got %s", checked.Status)
	}
}

func TestApprove(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
	})

	err := engine.Approve(ctx, approval.ID, "approver")
	if err != nil {
		t.Fatalf("Approve failed: %v", err)
	}

	checked, _ := engine.Check(ctx, approval.ID)
	if checked.Status != state.ApprovalApproved {
		t.Errorf("Status should be approved, got %s", checked.Status)
	}
	if checked.ApprovedBy != "approver" {
		t.Errorf("ApprovedBy should be approver, got %s", checked.ApprovedBy)
	}
}

func TestDeny(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
	})

	err := engine.Deny(ctx, approval.ID, "denier", "Too risky")
	if err != nil {
		t.Fatalf("Deny failed: %v", err)
	}

	checked, _ := engine.Check(ctx, approval.ID)
	if checked.Status != state.ApprovalDenied {
		t.Errorf("Status should be denied, got %s", checked.Status)
	}
	if checked.DeniedReason != "Too risky" {
		t.Errorf("DeniedReason should be 'Too risky', got %s", checked.DeniedReason)
	}
}

func TestSLBEnforcement(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "force_release",
		Resource:    "sensitive_file",
		RequestedBy: "alice",
		RequiresSLB: true,
	})

	// Same person should not be able to approve
	err := engine.Approve(ctx, approval.ID, "alice")
	if err == nil {
		t.Error("SLB should prevent self-approval")
	}

	// Different person should be able to approve
	err = engine.Approve(ctx, approval.ID, "bob")
	if err != nil {
		t.Errorf("Different person should be able to approve: %v", err)
	}
}

func TestSLBApproverList(t *testing.T) {
	store := setupTestStore(t)
	cfg := DefaultConfig()
	cfg.ApproverList = []string{"admin", "manager"}
	engine := New(store, nil, nil, cfg)

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "force_release",
		Resource:    "sensitive_file",
		RequestedBy: "alice",
		RequiresSLB: true,
	})

	// Non-admin should not be able to approve
	err := engine.Approve(ctx, approval.ID, "bob")
	if err == nil {
		t.Error("Non-admin should not be able to approve when ApproverList is set")
	}

	// Admin should be able to approve
	err = engine.Approve(ctx, approval.ID, "admin")
	if err != nil {
		t.Errorf("Admin should be able to approve: %v", err)
	}
}

func TestExpiry(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
		ExpiresIn:   1 * time.Millisecond, // Very short expiry
	})

	// Wait for expiry
	time.Sleep(10 * time.Millisecond)

	// Check should mark it as expired
	checked, err := engine.Check(ctx, approval.ID)
	if err != nil {
		t.Fatalf("Check failed: %v", err)
	}
	if checked.Status != state.ApprovalExpired {
		t.Errorf("Status should be expired, got %s", checked.Status)
	}

	// Should not be able to approve expired request
	err = engine.Approve(ctx, approval.ID, "approver")
	if err == nil {
		t.Error("Should not be able to approve expired request")
	}
}

func TestListPending(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()

	// Create some approvals
	engine.Request(ctx, RequestParams{
		Action:      "action1",
		Resource:    "resource1",
		RequestedBy: "requester1",
	})
	engine.Request(ctx, RequestParams{
		Action:      "action2",
		Resource:    "resource2",
		RequestedBy: "requester2",
	})

	pending, err := engine.ListPending(ctx)
	if err != nil {
		t.Fatalf("ListPending failed: %v", err)
	}

	if len(pending) != 2 {
		t.Errorf("Expected 2 pending approvals, got %d", len(pending))
	}
}

func TestExpireStale(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()

	// Create an approval with short expiry
	// Use 500ms expiry to be robust across CI environments with heavy load
	engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
		ExpiresIn:   500 * time.Millisecond,
	})

	// Wait for expiry - use 1s to ensure expiry even with CI scheduling delays
	time.Sleep(1 * time.Second)

	// Expire stale
	count, err := engine.ExpireStale(ctx)
	if err != nil {
		t.Fatalf("ExpireStale failed: %v", err)
	}

	if count != 1 {
		t.Errorf("Expected 1 expired, got %d", count)
	}
}

func TestWaitForApproval(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
	})

	// Approve in background
	go func() {
		time.Sleep(50 * time.Millisecond)
		engine.Approve(ctx, approval.ID, "approver")
	}()

	// Wait for approval
	result, err := engine.WaitForApproval(ctx, approval.ID, 1*time.Second)
	if err != nil {
		t.Fatalf("WaitForApproval failed: %v", err)
	}

	if result.Status != state.ApprovalApproved {
		t.Errorf("Status should be approved, got %s", result.Status)
	}
}

func TestWaitForApprovalTimeout(t *testing.T) {
	store := setupTestStore(t)
	engine := New(store, nil, nil, DefaultConfig())

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
	})

	// Wait with short timeout (no approval will come)
	result, err := engine.WaitForApproval(ctx, approval.ID, 50*time.Millisecond)
	if err != nil {
		t.Fatalf("WaitForApproval failed: %v", err)
	}

	// Should still be pending after timeout
	if result.Status != state.ApprovalPending {
		t.Errorf("Status should be pending after timeout, got %s", result.Status)
	}
}

func TestEventEmission(t *testing.T) {
	store := setupTestStore(t)
	eventBus := events.NewEventBus(100)
	engine := New(store, nil, eventBus, DefaultConfig())

	// Subscribe to events
	received := make([]string, 0)
	var mu sync.Mutex
	eventBus.SubscribeAll(func(e events.BusEvent) {
		mu.Lock()
		received = append(received, e.EventType())
		mu.Unlock()
	})

	ctx := context.Background()
	approval, _ := engine.Request(ctx, RequestParams{
		Action:      "test_action",
		Resource:    "test_resource",
		RequestedBy: "requester",
	})

	engine.Approve(ctx, approval.ID, "approver")

	// Wait for events to be processed
	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	defer mu.Unlock()

	if len(received) < 2 {
		t.Errorf("Expected at least 2 events, got %d", len(received))
	}
}
