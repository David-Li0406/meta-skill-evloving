package profiler

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"
	"time"
)

func TestEnableDisable(t *testing.T) {
	// Start disabled
	Disable()
	Reset()

	if IsEnabled() {
		t.Error("expected profiler to be disabled initially")
	}

	Enable()
	if !IsEnabled() {
		t.Error("expected profiler to be enabled after Enable()")
	}

	Disable()
	if IsEnabled() {
		t.Error("expected profiler to be disabled after Disable()")
	}
}

func TestSpanCreation(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	span := Start("test-operation")
	if span == nil {
		t.Fatal("expected non-nil span")
	}
	if span.Name != "test-operation" {
		t.Errorf("expected name 'test-operation', got %q", span.Name)
	}

	time.Sleep(10 * time.Millisecond)
	span.End()

	if span.Duration < 10*time.Millisecond {
		t.Errorf("expected duration >= 10ms, got %v", span.Duration)
	}
}

func TestSpanWithPhase(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	span := StartWithPhase("init-config", "startup")
	span.End()

	if span.Phase != "startup" {
		t.Errorf("expected phase 'startup', got %q", span.Phase)
	}

	startupSpans := GetSpansByPhase("startup")
	if len(startupSpans) != 1 {
		t.Errorf("expected 1 startup span, got %d", len(startupSpans))
	}
}

func TestChildSpan(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	parent := StartWithPhase("parent-op", "command")
	child := StartChild(parent, "child-op")

	if child.Parent != "parent-op" {
		t.Errorf("expected parent 'parent-op', got %q", child.Parent)
	}
	if child.Phase != "command" {
		t.Errorf("expected inherited phase 'command', got %q", child.Phase)
	}

	child.End()
	parent.End()
}

func TestSpanTags(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	span := Start("tagged-op")
	span.Tag("session", "myproject")
	span.Tag("count", 42)
	span.End()

	if span.Tags["session"] != "myproject" {
		t.Errorf("expected tag session='myproject', got %v", span.Tags["session"])
	}
	if span.Tags["count"] != 42 {
		t.Errorf("expected tag count=42, got %v", span.Tags["count"])
	}
}

func TestDisabledProfilingNoOps(t *testing.T) {
	Reset()
	Disable()

	// Should not panic and return no-op spans
	span := Start("should-not-record")
	span.Tag("key", "value")
	span.End()

	spans := GetSpans()
	if len(spans) != 0 {
		t.Errorf("expected no spans when disabled, got %d", len(spans))
	}
}

func TestGetProfile(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	// Create some spans
	s1 := StartWithPhase("op1", "startup")
	time.Sleep(5 * time.Millisecond)
	s1.End()

	s2 := StartWithPhase("op2", "startup")
	time.Sleep(5 * time.Millisecond)
	s2.End()

	s3 := StartWithPhase("op3", "command")
	time.Sleep(5 * time.Millisecond)
	s3.End()

	profile := GetProfile()

	if profile.SpanCount != 3 {
		t.Errorf("expected 3 spans, got %d", profile.SpanCount)
	}

	if len(profile.Phases) < 2 {
		t.Errorf("expected at least 2 phases, got %d", len(profile.Phases))
	}

	// Find startup phase
	var startupPhase *PhaseReport
	for i := range profile.Phases {
		if profile.Phases[i].Phase == "startup" {
			startupPhase = &profile.Phases[i]
			break
		}
	}
	if startupPhase == nil {
		t.Fatal("expected to find startup phase")
	}
	if startupPhase.SpanCount != 2 {
		t.Errorf("expected 2 startup spans, got %d", startupPhase.SpanCount)
	}
}

func TestWriteJSON(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	span := Start("json-test")
	span.Tag("test", true)
	span.End()

	var buf bytes.Buffer
	if err := WriteJSON(&buf); err != nil {
		t.Fatalf("WriteJSON failed: %v", err)
	}

	// Verify it's valid JSON
	var profile Profile
	if err := json.Unmarshal(buf.Bytes(), &profile); err != nil {
		t.Fatalf("invalid JSON output: %v", err)
	}

	if profile.SpanCount != 1 {
		t.Errorf("expected span_count=1, got %d", profile.SpanCount)
	}
}

func TestWriteText(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	s := StartWithPhase("text-test", "startup")
	time.Sleep(5 * time.Millisecond)
	s.End()

	var buf bytes.Buffer
	if err := WriteText(&buf); err != nil {
		t.Fatalf("WriteText failed: %v", err)
	}

	output := buf.String()
	if !strings.Contains(output, "Performance Profile") {
		t.Error("expected output to contain 'Performance Profile'")
	}
	if !strings.Contains(output, "text-test") {
		t.Error("expected output to contain span name 'text-test'")
	}
}

func TestTimeHelper(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	called := false
	Time("helper-test", func() {
		called = true
		time.Sleep(5 * time.Millisecond)
	})

	if !called {
		t.Error("expected function to be called")
	}

	spans := GetSpans()
	if len(spans) != 1 {
		t.Errorf("expected 1 span, got %d", len(spans))
	}
	if spans[0].Name != "helper-test" {
		t.Errorf("expected name 'helper-test', got %q", spans[0].Name)
	}
}

func TestTimeWithError(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	err := TimeWithError("error-test", func() error {
		return nil
	})
	if err != nil {
		t.Errorf("expected no error, got %v", err)
	}

	spans := GetSpans()
	if len(spans) != 1 {
		t.Fatal("expected 1 span")
	}
	if _, ok := spans[0].Tags["error"]; ok {
		t.Error("expected no error tag for successful operation")
	}
}

func TestDoubleEnd(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	span := Start("double-end")
	time.Sleep(5 * time.Millisecond)
	span.End()

	firstDuration := span.Duration

	time.Sleep(10 * time.Millisecond)
	span.End() // Should be no-op

	if span.Duration != firstDuration {
		t.Error("expected duration to not change after second End()")
	}
}

func TestReset(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	Start("span1").End()
	Start("span2").End()

	if len(GetSpans()) != 2 {
		t.Error("expected 2 spans before reset")
	}

	Reset()

	if len(GetSpans()) != 0 {
		t.Error("expected 0 spans after reset")
	}
}

func TestWriteJSONIncludesRecommendations(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	// Create some spans to generate recommendations
	span := Start("json-rec-test")
	span.End()

	var buf bytes.Buffer
	if err := WriteJSON(&buf); err != nil {
		t.Fatalf("WriteJSON failed: %v", err)
	}

	// Verify JSON contains recommendations field
	var profile Profile
	if err := json.Unmarshal(buf.Bytes(), &profile); err != nil {
		t.Fatalf("invalid JSON output: %v", err)
	}

	// Should have at least the "performance looks good" recommendation
	if len(profile.Recommendations) == 0 {
		t.Error("expected recommendations in JSON output")
	}

	// Verify recommendation structure
	rec := profile.Recommendations[0]
	if rec.Category == "" {
		t.Error("expected recommendation to have category")
	}
	if rec.Message == "" {
		t.Error("expected recommendation to have message")
	}
	if rec.Suggestion == "" {
		t.Error("expected recommendation to have suggestion")
	}
}

func TestWriteTextIncludesRecommendations(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	s := StartWithPhase("text-rec-test", "startup")
	s.End()

	var buf bytes.Buffer
	if err := WriteText(&buf); err != nil {
		t.Fatalf("WriteText failed: %v", err)
	}

	output := buf.String()
	if !strings.Contains(output, "Recommendations:") {
		t.Error("expected output to contain 'Recommendations:'")
	}
	// Should contain a suggestion (marked with →)
	if !strings.Contains(output, "→") {
		t.Error("expected output to contain recommendation suggestions")
	}
}

func TestWriteTextRecommendationSeverityIcons(t *testing.T) {
	Reset()
	Enable()
	defer Disable()

	// Create slow spans to trigger warnings
	span := StartWithPhase("very-slow-op", "startup")
	time.Sleep(150 * time.Millisecond) // Slow enough to trigger warning (>100ms)
	span.End()

	var buf bytes.Buffer
	if err := WriteText(&buf); err != nil {
		t.Fatalf("WriteText failed: %v", err)
	}

	output := buf.String()
	// Should contain warning icon for slow span
	if !strings.Contains(output, "⚠") && !strings.Contains(output, "❌") {
		t.Error("expected output to contain warning or critical icons for slow operation")
	}
}
