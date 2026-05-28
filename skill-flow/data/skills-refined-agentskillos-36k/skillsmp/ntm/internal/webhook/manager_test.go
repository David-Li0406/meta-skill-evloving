package webhook

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestNewManager(t *testing.T) {
	t.Parallel()

	// Test with zero config (should use defaults)
	m := NewManager(ManagerConfig{})
	if m.config.QueueSize != DefaultQueueSize {
		t.Errorf("expected queue size %d, got %d", DefaultQueueSize, m.config.QueueSize)
	}
	if m.config.WorkerCount != DefaultWorkerCount {
		t.Errorf("expected worker count %d, got %d", DefaultWorkerCount, m.config.WorkerCount)
	}

	// Test with custom config
	m2 := NewManager(ManagerConfig{
		QueueSize:   100,
		WorkerCount: 5,
	})
	if m2.config.QueueSize != 100 {
		t.Errorf("expected queue size 100, got %d", m2.config.QueueSize)
	}
	if m2.config.WorkerCount != 5 {
		t.Errorf("expected worker count 5, got %d", m2.config.WorkerCount)
	}
}

func TestRegisterWebhook(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	// Test valid registration
	err := m.Register(WebhookConfig{
		ID:      "test-webhook",
		URL:     "https://example.com/webhook",
		Enabled: true,
	})
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	// Verify webhook was registered
	m.webhooksMu.RLock()
	wh, ok := m.webhooks["test-webhook"]
	m.webhooksMu.RUnlock()
	if !ok {
		t.Error("webhook not found after registration")
	}
	if wh.Method != "POST" {
		t.Errorf("expected method POST, got %s", wh.Method)
	}

	// Test registration without URL
	err = m.Register(WebhookConfig{
		ID:      "no-url",
		Enabled: true,
	})
	if err == nil {
		t.Error("expected error for webhook without URL")
	}

	// Test auto-generated ID
	err = m.Register(WebhookConfig{
		URL:     "https://example.com/webhook2",
		Enabled: true,
	})
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
}

func TestUnregisterWebhook(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	// Register and then unregister
	err := m.Register(WebhookConfig{
		ID:      "test-webhook",
		URL:     "https://example.com/webhook",
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	err = m.Unregister("test-webhook")
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	// Verify webhook was removed
	m.webhooksMu.RLock()
	_, ok := m.webhooks["test-webhook"]
	m.webhooksMu.RUnlock()
	if ok {
		t.Error("webhook still exists after unregistration")
	}

	// Test unregistering non-existent webhook
	err = m.Unregister("non-existent")
	if err == nil {
		t.Error("expected error for non-existent webhook")
	}
}

func TestDispatchWithoutStart(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	err := m.Dispatch(Event{Type: "test"})
	if err == nil {
		t.Error("expected error when dispatching before start")
	}
}

func TestBasicDispatch(t *testing.T) {
	t.Parallel()

	var received atomic.Int32
	var mu sync.Mutex
	var receivedPayload Event

	// Create test server
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received.Add(1)

		// Verify headers
		if r.Header.Get("Content-Type") != "application/json" {
			t.Errorf("expected Content-Type application/json, got %s", r.Header.Get("Content-Type"))
		}
		if r.Header.Get("X-NTM-Event-Type") == "" {
			t.Error("missing X-NTM-Event-Type header")
		}

		// Parse payload
		body, _ := io.ReadAll(r.Body)
		mu.Lock()
		json.Unmarshal(body, &receivedPayload)
		mu.Unlock()

		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	// Create and start manager
	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "test",
		URL:     ts.URL,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event
	err = m.Dispatch(Event{
		Type:    "test.event",
		Message: "Hello webhook",
		Session: "test-session",
	})
	if err != nil {
		t.Errorf("dispatch failed: %v", err)
	}

	// Wait for delivery
	time.Sleep(100 * time.Millisecond)

	if received.Load() != 1 {
		t.Errorf("expected 1 delivery, got %d", received.Load())
	}

	mu.Lock()
	if receivedPayload.Type != "test.event" {
		t.Errorf("expected event type test.event, got %s", receivedPayload.Type)
	}
	if receivedPayload.Message != "Hello webhook" {
		t.Errorf("expected message 'Hello webhook', got %s", receivedPayload.Message)
	}
	mu.Unlock()
}

func TestRetryLogic(t *testing.T) {
	t.Parallel()

	var attempts atomic.Int32

	// Create test server that fails first 2 attempts
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempt := attempts.Add(1)
		if attempt <= 2 {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	// Create manager with fast retry for testing
	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "retry-test",
		URL:     ts.URL,
		Enabled: true,
		Retry: RetryConfig{
			Enabled:    true,
			MaxRetries: 5,
			BaseDelay:  10 * time.Millisecond,
			MaxDelay:   50 * time.Millisecond,
		},
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event
	err = m.Dispatch(Event{Type: "test.retry"})
	if err != nil {
		t.Errorf("dispatch failed: %v", err)
	}

	// Wait for retries
	time.Sleep(500 * time.Millisecond)

	if attempts.Load() != 3 {
		t.Errorf("expected 3 attempts (2 failures + 1 success), got %d", attempts.Load())
	}

	stats := m.Stats()
	if stats.Deliveries != 1 {
		t.Errorf("expected 1 successful delivery, got %d", stats.Deliveries)
	}
}

func TestNoRetryOn4xx(t *testing.T) {
	t.Parallel()

	var attempts atomic.Int32

	// Create test server that returns 400 Bad Request
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempts.Add(1)
		w.WriteHeader(http.StatusBadRequest)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "no-retry-test",
		URL:     ts.URL,
		Enabled: true,
		Retry: RetryConfig{
			Enabled:    true,
			MaxRetries: 5,
			BaseDelay:  10 * time.Millisecond,
		},
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event
	err = m.Dispatch(Event{Type: "test.no-retry"})
	if err != nil {
		t.Errorf("dispatch failed: %v", err)
	}

	// Wait for processing
	time.Sleep(200 * time.Millisecond)

	// Should only attempt once (no retry on 4xx)
	if attempts.Load() != 1 {
		t.Errorf("expected 1 attempt (no retry on 4xx), got %d", attempts.Load())
	}

	stats := m.Stats()
	if stats.Failures != 1 {
		t.Errorf("expected 1 failure, got %d", stats.Failures)
	}
	if stats.DeadLetterCount != 1 {
		t.Errorf("expected 1 dead letter, got %d", stats.DeadLetterCount)
	}
}

func TestRetryOn429(t *testing.T) {
	t.Parallel()

	var attempts atomic.Int32

	// Create test server that returns 429 then succeeds
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempt := attempts.Add(1)
		if attempt == 1 {
			w.WriteHeader(http.StatusTooManyRequests)
			return
		}
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "retry-429-test",
		URL:     ts.URL,
		Enabled: true,
		Retry: RetryConfig{
			Enabled:    true,
			MaxRetries: 5,
			BaseDelay:  10 * time.Millisecond,
		},
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event
	err = m.Dispatch(Event{Type: "test.rate-limit"})
	if err != nil {
		t.Errorf("dispatch failed: %v", err)
	}

	// Wait for retry
	time.Sleep(200 * time.Millisecond)

	// Should retry on 429
	if attempts.Load() != 2 {
		t.Errorf("expected 2 attempts (retry on 429), got %d", attempts.Load())
	}
}

func TestDeadLetterQueue(t *testing.T) {
	t.Parallel()

	// Create test server that always fails
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:       10,
		WorkerCount:     2,
		DeadLetterLimit: 5,
	})

	err := m.Register(WebhookConfig{
		ID:      "dead-letter-test",
		URL:     ts.URL,
		Enabled: true,
		Retry: RetryConfig{
			Enabled:    true,
			MaxRetries: 2,
			BaseDelay:  5 * time.Millisecond,
			MaxDelay:   10 * time.Millisecond,
		},
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event that will fail all retries
	err = m.Dispatch(Event{Type: "test.fail"})
	if err != nil {
		t.Errorf("dispatch failed: %v", err)
	}

	// Wait for all retries to exhaust
	time.Sleep(500 * time.Millisecond)

	deadLetters := m.DeadLetters()
	if len(deadLetters) != 1 {
		t.Errorf("expected 1 dead letter, got %d", len(deadLetters))
	}

	if len(deadLetters) > 0 && deadLetters[0].LastError == "" {
		t.Error("dead letter should have last error")
	}

	// Test clearing dead letters
	cleared := m.ClearDeadLetters()
	if cleared != 1 {
		t.Errorf("expected to clear 1 dead letter, cleared %d", cleared)
	}

	deadLetters = m.DeadLetters()
	if len(deadLetters) != 0 {
		t.Errorf("expected 0 dead letters after clear, got %d", len(deadLetters))
	}
}

func TestEventFiltering(t *testing.T) {
	t.Parallel()

	var received atomic.Int32

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received.Add(1)
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	// Register webhook that only receives "event.a" events
	err := m.Register(WebhookConfig{
		ID:      "filtered-webhook",
		URL:     ts.URL,
		Enabled: true,
		Events:  []string{"event.a"},
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch matching event
	m.Dispatch(Event{Type: "event.a"})
	// Dispatch non-matching event
	m.Dispatch(Event{Type: "event.b"})

	time.Sleep(100 * time.Millisecond)

	// Should only receive the matching event
	if received.Load() != 1 {
		t.Errorf("expected 1 delivery (filtered), got %d", received.Load())
	}
}

func TestHMACSignature(t *testing.T) {
	t.Parallel()

	var receivedSignature string
	var mu sync.Mutex

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		receivedSignature = r.Header.Get("X-NTM-Signature")
		mu.Unlock()
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "signed-webhook",
		URL:     ts.URL,
		Enabled: true,
		Secret:  "test-secret-key",
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event
	m.Dispatch(Event{Type: "test.signed"})

	time.Sleep(100 * time.Millisecond)

	mu.Lock()
	sig := receivedSignature
	mu.Unlock()

	if sig == "" {
		t.Error("expected X-NTM-Signature header")
	}
	if len(sig) < 10 || sig[:7] != "sha256=" {
		t.Errorf("expected sha256= prefix in signature, got %s", sig)
	}
}

func TestCustomTemplate(t *testing.T) {
	t.Parallel()

	var receivedBody string
	var mu sync.Mutex

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		mu.Lock()
		receivedBody = string(body)
		mu.Unlock()
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   10,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:       "templated-webhook",
		URL:      ts.URL,
		Enabled:  true,
		Template: `{"text": "Event: {{.Type}}, Message: {{jsonEscape .Message}}"}`,
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch event with special characters
	m.Dispatch(Event{
		Type:    "test.template",
		Message: `Hello "world"`,
	})

	time.Sleep(100 * time.Millisecond)

	mu.Lock()
	body := receivedBody
	mu.Unlock()

	expected := `{"text": "Event: test.template, Message: Hello \"world\""}`
	if body != expected {
		t.Errorf("expected %s, got %s", expected, body)
	}
}

func TestStats(t *testing.T) {
	t.Parallel()

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   100,
		WorkerCount: 2,
	})

	err := m.Register(WebhookConfig{
		ID:      "stats-test",
		URL:     ts.URL,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch multiple events
	for i := 0; i < 5; i++ {
		m.Dispatch(Event{Type: "test.stats"})
	}

	time.Sleep(200 * time.Millisecond)

	stats := m.Stats()
	if stats.Deliveries != 5 {
		t.Errorf("expected 5 deliveries, got %d", stats.Deliveries)
	}
	if stats.WebhookCount != 1 {
		t.Errorf("expected 1 webhook, got %d", stats.WebhookCount)
	}
	if stats.QueueCapacity != 100 {
		t.Errorf("expected queue capacity 100, got %d", stats.QueueCapacity)
	}
}

func TestStartStop(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	// Start
	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}

	// Double start should fail
	if err := m.Start(); err == nil {
		t.Error("expected error on double start")
	}

	// Stop
	if err := m.Stop(); err != nil {
		t.Fatalf("stop failed: %v", err)
	}

	// Dispatch after stop should fail
	if err := m.Dispatch(Event{Type: "test"}); err == nil {
		t.Error("expected error dispatching after stop")
	}
}

func TestConcurrentDispatch(t *testing.T) {
	t.Parallel()

	var received atomic.Int32

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received.Add(1)
		time.Sleep(10 * time.Millisecond) // Simulate some processing
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	m := NewManager(ManagerConfig{
		QueueSize:   1000,
		WorkerCount: 10,
	})

	err := m.Register(WebhookConfig{
		ID:      "concurrent-test",
		URL:     ts.URL,
		Enabled: true,
	})
	if err != nil {
		t.Fatalf("registration failed: %v", err)
	}

	if err := m.Start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	defer m.Stop()

	// Dispatch many events concurrently
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			m.Dispatch(Event{
				Type:    "test.concurrent",
				Message: "Event " + string(rune('0'+n%10)),
			})
		}(i)
	}
	wg.Wait()

	// Wait for all deliveries
	time.Sleep(2 * time.Second)

	if received.Load() != 100 {
		t.Errorf("expected 100 deliveries, got %d", received.Load())
	}
}

func TestExponentialBackoff(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	// Create a delivery with custom retry config
	wh := &WebhookConfig{
		Retry: RetryConfig{
			Enabled:    true,
			MaxRetries: 5,
			BaseDelay:  1 * time.Second,
			MaxDelay:   30 * time.Second,
		},
	}

	testCases := []struct {
		attempt  int
		expected time.Duration
	}{
		{1, 1 * time.Second},  // 1s
		{2, 2 * time.Second},  // 2s
		{3, 4 * time.Second},  // 4s
		{4, 8 * time.Second},  // 8s
		{5, 16 * time.Second}, // 16s
		{6, 30 * time.Second}, // Capped at max
	}

	for _, tc := range testCases {
		d := &Delivery{Webhook: wh, Attempt: tc.attempt}
		nextRetry := m.calculateNextRetry(d)
		delay := time.Until(nextRetry)

		// Allow some tolerance for timing
		minExpected := tc.expected - 100*time.Millisecond
		maxExpected := tc.expected + 100*time.Millisecond

		if delay < minExpected || delay > maxExpected {
			t.Errorf("attempt %d: expected delay ~%v, got %v", tc.attempt, tc.expected, delay)
		}
	}
}

func TestMatchesEvent(t *testing.T) {
	t.Parallel()

	m := NewManager(DefaultManagerConfig())

	tests := []struct {
		events   []string
		event    string
		expected bool
	}{
		{nil, "any.event", true},              // Empty = all events
		{[]string{}, "any.event", true},       // Empty = all events
		{[]string{"*"}, "any.event", true},    // Wildcard
		{[]string{"a.b"}, "a.b", true},        // Exact match
		{[]string{"a.b"}, "a.c", false},       // No match
		{[]string{"a.b", "a.c"}, "a.c", true}, // One of multiple
	}

	for _, tt := range tests {
		wh := &WebhookConfig{Events: tt.events}
		result := m.matchesEvent(wh, tt.event)
		if result != tt.expected {
			t.Errorf("matchesEvent(%v, %s) = %v, expected %v",
				tt.events, tt.event, result, tt.expected)
		}
	}
}
