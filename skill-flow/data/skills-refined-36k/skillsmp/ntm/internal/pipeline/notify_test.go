package pipeline

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestNewNotifier(t *testing.T) {
	cfg := NotifierConfig{
		Channels:      []string{"desktop", "webhook", "mail"},
		WebhookURL:    "https://example.com/webhook",
		MailRecipient: "Human",
	}

	n := NewNotifier(cfg)

	if len(n.channels) != 3 {
		t.Errorf("expected 3 channels, got %d", len(n.channels))
	}
	if n.webhookURL != "https://example.com/webhook" {
		t.Errorf("expected webhook URL, got %q", n.webhookURL)
	}
	if n.mailRecipient != "Human" {
		t.Errorf("expected mail recipient 'Human', got %q", n.mailRecipient)
	}
}

func TestNewNotifierIgnoresUnknownChannels(t *testing.T) {
	cfg := NotifierConfig{
		Channels: []string{"desktop", "slack", "unknown", "webhook"},
	}

	n := NewNotifier(cfg)

	// Only desktop and webhook should be recognized
	if len(n.channels) != 2 {
		t.Errorf("expected 2 valid channels (unknown ignored), got %d", len(n.channels))
	}
}

func TestNewNotifierFromSettings(t *testing.T) {
	settings := WorkflowSettings{
		NotifyOnComplete: true,
		NotifyOnError:    true,
		NotifyChannels:   []string{"desktop", "webhook"},
		WebhookURL:       "https://example.com/hook",
		MailRecipient:    "TestAgent",
	}

	n := NewNotifierFromSettings(settings, nil, "/test/project", "Coordinator")

	if len(n.channels) != 2 {
		t.Errorf("expected 2 channels, got %d", len(n.channels))
	}
	if n.projectKey != "/test/project" {
		t.Errorf("expected projectKey, got %q", n.projectKey)
	}
	if n.agentName != "Coordinator" {
		t.Errorf("expected agentName 'Coordinator', got %q", n.agentName)
	}
}

func TestShouldNotify(t *testing.T) {
	tests := []struct {
		name     string
		settings WorkflowSettings
		event    NotificationEvent
		want     bool
	}{
		{
			name:     "complete with notify on",
			settings: WorkflowSettings{NotifyOnComplete: true},
			event:    NotifyCompleted,
			want:     true,
		},
		{
			name:     "complete with notify off",
			settings: WorkflowSettings{NotifyOnComplete: false},
			event:    NotifyCompleted,
			want:     false,
		},
		{
			name:     "failed with notify on",
			settings: WorkflowSettings{NotifyOnError: true},
			event:    NotifyFailed,
			want:     true,
		},
		{
			name:     "failed with notify off",
			settings: WorkflowSettings{NotifyOnError: false},
			event:    NotifyFailed,
			want:     false,
		},
		{
			name:     "step error with notify on",
			settings: WorkflowSettings{NotifyOnError: true},
			event:    NotifyStepError,
			want:     true,
		},
		{
			name:     "started never notifies",
			settings: WorkflowSettings{NotifyOnComplete: true, NotifyOnError: true},
			event:    NotifyStarted,
			want:     false,
		},
		{
			name:     "cancelled never notifies (no setting yet)",
			settings: WorkflowSettings{NotifyOnComplete: true, NotifyOnError: true},
			event:    NotifyCancelled,
			want:     false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := ShouldNotify(tt.settings, tt.event)
			if got != tt.want {
				t.Errorf("ShouldNotify() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestNotifyWebhook(t *testing.T) {
	var received NotificationPayload
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("expected POST, got %s", r.Method)
		}
		if ct := r.Header.Get("Content-Type"); ct != "application/json" {
			t.Errorf("expected Content-Type application/json, got %s", ct)
		}

		if err := json.NewDecoder(r.Body).Decode(&received); err != nil {
			t.Errorf("failed to decode body: %v", err)
		}

		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	n := NewNotifier(NotifierConfig{
		Channels:   []string{"webhook"},
		WebhookURL: server.URL,
	})

	payload := NotificationPayload{
		Event:        NotifyCompleted,
		WorkflowName: "test-workflow",
		RunID:        "run-123",
		Status:       StatusCompleted,
		StepsTotal:   5,
		StepsDone:    5,
		Timestamp:    time.Now(),
	}

	err := n.Notify(context.Background(), payload)
	if err != nil {
		t.Errorf("Notify() error = %v", err)
	}

	if received.Event != NotifyCompleted {
		t.Errorf("expected event NotifyCompleted, got %s", received.Event)
	}
	if received.WorkflowName != "test-workflow" {
		t.Errorf("expected workflow name 'test-workflow', got %q", received.WorkflowName)
	}
}

func TestNotifyWebhookError(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
	}))
	defer server.Close()

	n := NewNotifier(NotifierConfig{
		Channels:   []string{"webhook"},
		WebhookURL: server.URL,
	})

	payload := NotificationPayload{
		Event:        NotifyFailed,
		WorkflowName: "test-workflow",
		Timestamp:    time.Now(),
	}

	err := n.Notify(context.Background(), payload)
	if err == nil {
		t.Error("expected error for 500 response")
	}
	if !strings.Contains(err.Error(), "500") {
		t.Errorf("expected error to mention status 500, got: %v", err)
	}
}

func TestFormatDesktopTitle(t *testing.T) {
	tests := []struct {
		event NotificationEvent
		want  string
	}{
		{NotifyCompleted, "Pipeline 'test' completed"},
		{NotifyFailed, "Pipeline 'test' failed"},
		{NotifyCancelled, "Pipeline 'test' cancelled"},
		{NotifyStarted, "Pipeline 'test' started"},
		{NotifyStepError, "Pipeline 'test' step error"},
	}

	for _, tt := range tests {
		t.Run(string(tt.event), func(t *testing.T) {
			p := NotificationPayload{Event: tt.event, WorkflowName: "test"}
			got := formatDesktopTitle(p)
			if got != tt.want {
				t.Errorf("formatDesktopTitle() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestFormatDesktopBody(t *testing.T) {
	tests := []struct {
		name    string
		payload NotificationPayload
		contain string
	}{
		{
			name: "completed",
			payload: NotificationPayload{
				Event:      NotifyCompleted,
				Duration:   5 * time.Minute,
				StepsDone:  10,
				StepsTotal: 10,
			},
			contain: "Duration: 5m",
		},
		{
			name: "failed with step",
			payload: NotificationPayload{
				Event:      NotifyFailed,
				FailedStep: "build",
				Error:      "compilation error",
			},
			contain: "step 'build'",
		},
		{
			name: "cancelled",
			payload: NotificationPayload{
				Event:    NotifyCancelled,
				Duration: 2 * time.Minute,
			},
			contain: "Cancelled after",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := formatDesktopBody(tt.payload)
			if !strings.Contains(got, tt.contain) {
				t.Errorf("formatDesktopBody() = %q, want to contain %q", got, tt.contain)
			}
		})
	}
}

func TestFormatMailSubject(t *testing.T) {
	tests := []struct {
		event NotificationEvent
		want  string
	}{
		{NotifyCompleted, "Pipeline 'test' completed successfully"},
		{NotifyFailed, "Pipeline 'test' failed"},
		{NotifyCancelled, "Pipeline 'test' was cancelled"},
	}

	for _, tt := range tests {
		t.Run(string(tt.event), func(t *testing.T) {
			p := NotificationPayload{Event: tt.event, WorkflowName: "test"}
			got := formatMailSubject(p)
			if got != tt.want {
				t.Errorf("formatMailSubject() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestFormatMailBody(t *testing.T) {
	payload := NotificationPayload{
		Event:        NotifyCompleted,
		WorkflowName: "test-workflow",
		RunID:        "run-abc",
		Session:      "my-session",
		Status:       StatusCompleted,
		Duration:     3*time.Minute + 45*time.Second,
		StepsTotal:   5,
		StepsDone:    5,
		Timestamp:    time.Now(),
	}

	body := formatMailBody(payload)

	if !strings.Contains(body, "# Pipeline: test-workflow") {
		t.Error("expected markdown header")
	}
	if !strings.Contains(body, "run-abc") {
		t.Error("expected run ID")
	}
	if !strings.Contains(body, "my-session") {
		t.Error("expected session")
	}
	if !strings.Contains(body, "3m45s") {
		t.Error("expected duration")
	}
	if !strings.Contains(body, "5/5") {
		t.Error("expected step count")
	}
}

func TestFormatMailBodyFailed(t *testing.T) {
	payload := NotificationPayload{
		Event:        NotifyFailed,
		WorkflowName: "test-workflow",
		RunID:        "run-xyz",
		Status:       StatusFailed,
		FailedStep:   "deploy",
		Error:        "connection refused",
		Duration:     1 * time.Minute,
		StepsTotal:   5,
		StepsDone:    3,
		Timestamp:    time.Now(),
	}

	body := formatMailBody(payload)

	if !strings.Contains(body, "## Error") {
		t.Error("expected error section")
	}
	if !strings.Contains(body, "deploy") {
		t.Error("expected failed step name")
	}
	if !strings.Contains(body, "connection refused") {
		t.Error("expected error message")
	}
}

func TestFormatDuration(t *testing.T) {
	tests := []struct {
		d    time.Duration
		want string
	}{
		{30 * time.Second, "30s"},
		{90 * time.Second, "1m30s"},
		{3600 * time.Second, "1h0m"},
		{3661 * time.Second, "1h1m"},
	}

	for _, tt := range tests {
		t.Run(tt.want, func(t *testing.T) {
			got := formatDuration(tt.d)
			if got != tt.want {
				t.Errorf("formatDuration(%v) = %q, want %q", tt.d, got, tt.want)
			}
		})
	}
}

func TestTruncateMessage(t *testing.T) {
	tests := []struct {
		s    string
		n    int
		want string
	}{
		{"short", 10, "short"},
		{"this is a longer message", 10, "this is..."},
		{"abc", 3, "abc"},      // fits, no truncation needed
		{"ab", 2, "ab"},        // fits, no truncation needed
		{"abcdef", 3, "..."},   // doesn't fit, show ellipsis
		{"abcdef", 5, "ab..."}, // truncate with room for some content
	}

	for _, tt := range tests {
		t.Run(tt.s[:min(len(tt.s), 5)], func(t *testing.T) {
			got := truncateMessage(tt.s, tt.n)
			if got != tt.want {
				t.Errorf("truncateMessage(%q, %d) = %q, want %q", tt.s, tt.n, got, tt.want)
			}
		})
	}
}

func TestBuildPayloadFromState(t *testing.T) {
	now := time.Now()
	state := &ExecutionState{
		RunID:      "run-test",
		WorkflowID: "test-workflow",
		Session:    "test-session",
		Status:     StatusCompleted,
		StartedAt:  now.Add(-5 * time.Minute),
		FinishedAt: now,
		Steps: map[string]StepResult{
			"step1": {StepID: "step1", Status: StatusCompleted},
			"step2": {StepID: "step2", Status: StatusCompleted},
			"step3": {StepID: "step3", Status: StatusSkipped},
		},
	}

	workflow := &Workflow{
		Name: "test-workflow",
		Steps: []Step{
			{ID: "step1"},
			{ID: "step2"},
			{ID: "step3"},
		},
	}

	payload := BuildPayloadFromState(state, workflow, NotifyCompleted)

	if payload.Event != NotifyCompleted {
		t.Errorf("expected event NotifyCompleted, got %s", payload.Event)
	}
	if payload.WorkflowName != "test-workflow" {
		t.Errorf("expected workflow name, got %q", payload.WorkflowName)
	}
	if payload.RunID != "run-test" {
		t.Errorf("expected run ID, got %q", payload.RunID)
	}
	if payload.StepsTotal != 3 {
		t.Errorf("expected 3 steps total, got %d", payload.StepsTotal)
	}
	if payload.StepsDone != 3 { // 2 completed + 1 skipped
		t.Errorf("expected 3 steps done, got %d", payload.StepsDone)
	}
	if payload.Duration < 4*time.Minute || payload.Duration > 6*time.Minute {
		t.Errorf("expected duration ~5m, got %v", payload.Duration)
	}
}

func TestBuildPayloadFromStateWithFailure(t *testing.T) {
	now := time.Now()
	state := &ExecutionState{
		RunID:      "run-fail",
		WorkflowID: "fail-workflow",
		Status:     StatusFailed,
		StartedAt:  now.Add(-2 * time.Minute),
		FinishedAt: now,
		Steps: map[string]StepResult{
			"step1": {StepID: "step1", Status: StatusCompleted},
			"step2": {
				StepID: "step2",
				Status: StatusFailed,
				Error: &StepError{
					Message: "build failed",
				},
			},
		},
		Errors: []ExecutionError{
			{StepID: "step2", Message: "build failed", Fatal: true},
		},
	}

	workflow := &Workflow{
		Name: "fail-workflow",
		Steps: []Step{
			{ID: "step1"},
			{ID: "step2"},
		},
	}

	payload := BuildPayloadFromState(state, workflow, NotifyFailed)

	if payload.Event != NotifyFailed {
		t.Errorf("expected event NotifyFailed, got %s", payload.Event)
	}
	if payload.StepsFailed != 1 {
		t.Errorf("expected 1 step failed, got %d", payload.StepsFailed)
	}
	if payload.FailedStep != "step2" {
		t.Errorf("expected failed step 'step2', got %q", payload.FailedStep)
	}
	if payload.Error != "build failed" {
		t.Errorf("expected error 'build failed', got %q", payload.Error)
	}
}

func TestNotifyNoChannels(t *testing.T) {
	n := NewNotifier(NotifierConfig{
		Channels: []string{},
	})

	payload := NotificationPayload{
		Event:        NotifyCompleted,
		WorkflowName: "test",
		Timestamp:    time.Now(),
	}

	err := n.Notify(context.Background(), payload)
	if err != nil {
		t.Errorf("expected no error for empty channels, got %v", err)
	}
}
