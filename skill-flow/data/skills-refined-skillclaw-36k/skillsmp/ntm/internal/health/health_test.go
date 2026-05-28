package health

import (
	"testing"
	"time"
)

func TestParseWaitTime(t *testing.T) {
	tests := []struct {
		input string
		want  int
	}{
		{"try again in 60s", 60},
		{"wait 30 seconds", 30},
		{"retry after 120s", 120},
		{"Rate limit exceeded, 45s cooldown", 45},
		{"no wait time here", 0},
	}

	for _, tt := range tests {
		got := parseWaitTime(tt.input)
		if got != tt.want {
			t.Errorf("parseWaitTime(%q) = %d, want %d", tt.input, got, tt.want)
		}
	}
}

func TestDetectErrors(t *testing.T) {
	tests := []struct {
		input    string
		wantType string
	}{
		{"Rate limit exceeded", "rate_limit"},
		{"HTTP 429 Too Many Requests", "rate_limit"},
		{"Authentication failed", "auth_error"},
		{"panic: runtime error", "crash"},
		{"connection refused", "network_error"},
		{"everything is fine", ""},
	}

	for _, tt := range tests {
		issues := detectErrors(tt.input)
		if tt.wantType == "" {
			if len(issues) > 0 {
				t.Errorf("detectErrors(%q) returned issues, want none", tt.input)
			}
		} else {
			found := false
			for _, issue := range issues {
				if issue.Type == tt.wantType {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("detectErrors(%q) did not return type %q", tt.input, tt.wantType)
			}
		}
	}
}

func TestDetectProgress(t *testing.T) {
	tests := []struct {
		output   string
		activity ActivityLevel
		want     ProgressStage
	}{
		{"Let me analyze this...", ActivityActive, StageStarting},
		{"Editing file main.go...", ActivityActive, StageWorking},
		{"All tests passed.", ActivityActive, StageFinishing},
		{"Error: unable to compile.", ActivityActive, StageStuck},
		{"", ActivityIdle, StageIdle},
	}

	for _, tt := range tests {
		p := detectProgress(tt.output, tt.activity, nil)
		if p.Stage != tt.want {
			t.Errorf("detectProgress(%q) = %v, want %v", tt.output, p.Stage, tt.want)
		}
	}
}

func TestDetectActivity(t *testing.T) {
	// With timestamp
	now := time.Now()
	active := detectActivity("output", now.Add(-10*time.Second), "user")
	if active != ActivityActive {
		t.Errorf("Expected Active for recent output, got %v", active)
	}

	stale := detectActivity("output", now.Add(-10*time.Minute), "user")
	if stale != ActivityStale {
		t.Errorf("Expected Stale for old output, got %v", stale)
	}

	// Without timestamp (rely on prompt)
	// Use ">" which is a generic prompt pattern
	idle := detectActivity("> ", time.Time{}, "user")
	if idle != ActivityIdle {
		t.Errorf("Expected Idle for prompt without timestamp, got %v", idle)
	}

	// Recent timestamp but prompt visible -> Idle (new behavior)
	// Use "cc" agent type for claude prompt
	idleWithTime := detectActivity("claude>", now.Add(-5*time.Second), "cc")
	if idleWithTime != ActivityIdle {
		t.Errorf("Expected Idle for prompt with recent timestamp, got %v", idleWithTime)
	}
}

func TestCalculateStatus(t *testing.T) {
	// Healthy
	h := AgentHealth{
		ProcessStatus: ProcessRunning,
		Activity:      ActivityActive,
	}
	if s := calculateStatus(h); s != StatusOK {
		t.Errorf("Expected OK, got %v", s)
	}

	// Error
	h.ProcessStatus = ProcessExited
	if s := calculateStatus(h); s != StatusError {
		t.Errorf("Expected Error for exited process, got %v", s)
	}

	// Warning
	h.ProcessStatus = ProcessRunning
	h.Activity = ActivityStale
	if s := calculateStatus(h); s != StatusWarning {
		t.Errorf("Expected Warning for stale activity, got %v", s)
	}
}
