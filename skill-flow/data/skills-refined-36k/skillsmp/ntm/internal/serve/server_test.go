package serve

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/events"
	"github.com/Dicklesworthstone/ntm/internal/state"
)

func setupTestServer(t *testing.T) (*Server, *state.Store) {
	t.Helper()

	// Create temp database
	tmpDir := t.TempDir()
	dbPath := filepath.Join(tmpDir, "test.db")

	store, err := state.Open(dbPath)
	if err != nil {
		t.Fatalf("Failed to open store: %v", err)
	}

	if err := store.Migrate(); err != nil {
		t.Fatalf("Failed to migrate: %v", err)
	}

	t.Cleanup(func() {
		store.Close()
		os.Remove(dbPath)
	})

	eventBus := events.NewEventBus(100)

	srv := New(Config{
		Port:       0, // Will use default
		EventBus:   eventBus,
		StateStore: store,
	})

	return srv, store
}

func TestNew(t *testing.T) {
	srv := New(Config{})
	if srv == nil {
		t.Fatal("New returned nil")
	}
	if srv.Port() != 7337 {
		t.Errorf("Default port = %d, want 7337", srv.Port())
	}
}

func TestNewWithCustomPort(t *testing.T) {
	srv := New(Config{Port: 8080})
	if srv.Port() != 8080 {
		t.Errorf("Port = %d, want 8080", srv.Port())
	}
}

func TestHealthEndpoint(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()

	srv.handleHealth(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}

	var resp map[string]interface{}
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if resp["success"] != true {
		t.Error("Expected success=true")
	}
	if resp["status"] != "healthy" {
		t.Error("Expected status=healthy")
	}
}

func TestHealthEndpointMethodNotAllowed(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodPost, "/health", nil)
	rec := httptest.NewRecorder()

	srv.handleHealth(rec, req)

	if rec.Code != http.StatusMethodNotAllowed {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusMethodNotAllowed)
	}
}

func TestSessionsEndpoint(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/api/sessions", nil)
	rec := httptest.NewRecorder()

	srv.handleSessions(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}

	var resp map[string]interface{}
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if resp["success"] != true {
		t.Error("Expected success=true")
	}
	if _, ok := resp["sessions"]; !ok {
		t.Error("Expected sessions field")
	}
}

func TestSessionsEndpointNoStore(t *testing.T) {
	srv := New(Config{})

	req := httptest.NewRequest(http.MethodGet, "/api/sessions", nil)
	rec := httptest.NewRecorder()

	srv.handleSessions(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusServiceUnavailable)
	}
}

func TestSessionEndpointNotFound(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/api/sessions/nonexistent", nil)
	rec := httptest.NewRecorder()

	srv.handleSession(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusNotFound)
	}
}

func TestSessionEndpointMissingID(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/api/sessions/", nil)
	rec := httptest.NewRecorder()

	srv.handleSession(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusBadRequest)
	}
}

func TestRobotStatusEndpoint(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/api/robot/status", nil)
	rec := httptest.NewRecorder()

	srv.handleRobotStatus(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}

	var resp map[string]interface{}
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if resp["success"] != true {
		t.Error("Expected success=true")
	}
}

func TestRobotHealthEndpoint(t *testing.T) {
	srv, _ := setupTestServer(t)

	req := httptest.NewRequest(http.MethodGet, "/api/robot/health", nil)
	rec := httptest.NewRecorder()

	srv.handleRobotHealth(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}
}

func TestSessionEventsEndpoint(t *testing.T) {
	srv, _ := setupTestServer(t)

	// Publish an event
	srv.eventBus.Publish(events.BaseEvent{
		Type:      "test_event",
		Timestamp: time.Now().UTC(),
		Session:   "test-session",
	})

	// Give event time to be recorded
	time.Sleep(10 * time.Millisecond)

	req := httptest.NewRequest(http.MethodGet, "/api/sessions/test-session/events", nil)
	rec := httptest.NewRecorder()

	srv.handleSessionEvents(rec, req, "test-session")

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}

	var resp map[string]interface{}
	if err := json.NewDecoder(rec.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if resp["success"] != true {
		t.Error("Expected success=true")
	}
}

func TestSSEClientManagement(t *testing.T) {
	srv, _ := setupTestServer(t)

	ch := make(chan events.BusEvent, 10)
	srv.addSSEClient(ch)

	srv.sseClientsMu.RLock()
	clientCount := len(srv.sseClients)
	srv.sseClientsMu.RUnlock()

	if clientCount != 1 {
		t.Errorf("Client count = %d, want 1", clientCount)
	}

	srv.removeSSEClient(ch)

	srv.sseClientsMu.RLock()
	clientCount = len(srv.sseClients)
	srv.sseClientsMu.RUnlock()

	if clientCount != 0 {
		t.Errorf("Client count = %d, want 0 after removal", clientCount)
	}
}

func TestBroadcastEvent(t *testing.T) {
	srv, _ := setupTestServer(t)

	ch := make(chan events.BusEvent, 10)
	srv.addSSEClient(ch)
	defer srv.removeSSEClient(ch)

	testEvent := events.BaseEvent{
		Type:      "broadcast_test",
		Timestamp: time.Now().UTC(),
		Session:   "test",
	}

	srv.broadcastEvent(testEvent)

	select {
	case e := <-ch:
		if e.EventType() != "broadcast_test" {
			t.Errorf("Event type = %s, want broadcast_test", e.EventType())
		}
	case <-time.After(100 * time.Millisecond):
		t.Error("Timeout waiting for broadcast")
	}
}

func TestEventStreamSSE(t *testing.T) {
	srv, _ := setupTestServer(t)

	// Create a request with a cancelable context
	ctx, cancel := context.WithCancel(context.Background())
	req := httptest.NewRequest(http.MethodGet, "/events", nil).WithContext(ctx)
	rec := httptest.NewRecorder()

	// Start the handler in a goroutine
	done := make(chan struct{})
	go func() {
		srv.handleEventStream(rec, req)
		close(done)
	}()

	// Give time for connection setup
	time.Sleep(50 * time.Millisecond)

	// Cancel to end the request
	cancel()

	// Wait for handler to complete
	select {
	case <-done:
		// OK
	case <-time.After(1 * time.Second):
		t.Error("Handler did not complete after context cancel")
	}

	// Check headers
	contentType := rec.Header().Get("Content-Type")
	if contentType != "text/event-stream" {
		t.Errorf("Content-Type = %s, want text/event-stream", contentType)
	}

	// Check for connected event
	body, _ := io.ReadAll(rec.Body)
	if len(body) == 0 {
		t.Error("Expected some output from SSE stream")
	}
}

func TestCORSMiddleware(t *testing.T) {
	handler := corsMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))

	// Test preflight OPTIONS request
	req := httptest.NewRequest(http.MethodOptions, "/", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)

	if rec.Header().Get("Access-Control-Allow-Origin") != "*" {
		t.Error("Expected CORS header")
	}
	if rec.Code != http.StatusOK {
		t.Errorf("OPTIONS Status = %d, want %d", rec.Code, http.StatusOK)
	}
}

func TestLoggingMiddleware(t *testing.T) {
	handler := loggingMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))

	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Status = %d, want %d", rec.Code, http.StatusOK)
	}
}
