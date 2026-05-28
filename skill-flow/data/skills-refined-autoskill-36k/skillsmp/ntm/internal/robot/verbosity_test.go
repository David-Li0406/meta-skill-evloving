package robot

import "testing"

func TestParseRobotVerbosity(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    RobotVerbosity
		wantErr bool
	}{
		{name: "empty defaults", input: "", want: VerbosityDefault},
		{name: "default", input: "default", want: VerbosityDefault},
		{name: "terse", input: "terse", want: VerbosityTerse},
		{name: "debug", input: "debug", want: VerbosityDebug},
		{name: "invalid", input: "loud", wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseRobotVerbosity(tt.input)
			if (err != nil) != tt.wantErr {
				t.Fatalf("ParseRobotVerbosity(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
			}
			if tt.wantErr {
				return
			}
			if got != tt.want {
				t.Fatalf("ParseRobotVerbosity(%q) = %q, want %q", tt.input, got, tt.want)
			}
		})
	}
}

func TestApplyVerbosity_TerseShortensKeysAndDropsHints(t *testing.T) {
	payload := map[string]any{
		"success":   true,
		"timestamp": "2026-01-01T00:00:00Z",
		"_agent_hints": map[string]any{
			"summary": "ok",
		},
	}

	typed, ok := applyVerbosity(payload, VerbosityTerse).(map[string]any)
	if !ok {
		t.Fatalf("applyVerbosity() returned %T, want map[string]any", typed)
	}

	if _, exists := typed["_agent_hints"]; exists {
		t.Fatal("expected _agent_hints to be removed in terse profile")
	}
	if _, exists := typed["success"]; exists {
		t.Fatal("expected success key to be shortened in terse profile")
	}
	if _, exists := typed["ok"]; !exists {
		t.Fatal("expected ok key in terse profile output")
	}
	if _, exists := typed["ts"]; !exists {
		t.Fatal("expected ts key in terse profile output")
	}
}

func TestApplyVerbosity_DebugAddsMetadata(t *testing.T) {
	payload := map[string]any{
		"success": true,
	}

	typed, ok := applyVerbosity(payload, VerbosityDebug).(map[string]any)
	if !ok {
		t.Fatalf("applyVerbosity() returned %T, want map[string]any", typed)
	}
	debug, ok := typed["_debug"].(map[string]any)
	if !ok {
		t.Fatalf("expected _debug map, got %T", typed["_debug"])
	}
	if debug["verbosity"] != "debug" {
		t.Fatalf("expected debug verbosity, got %v", debug["verbosity"])
	}
	if debug["payload_type"] == "" {
		t.Fatalf("expected payload_type to be populated")
	}
}

func TestApplyVerbosity_DebugWrapsSlices(t *testing.T) {
	payload := []map[string]any{
		{"success": true},
	}

	typed, ok := applyVerbosity(payload, VerbosityDebug).(map[string]any)
	if !ok {
		t.Fatalf("applyVerbosity() returned %T, want map[string]any", typed)
	}
	if _, ok := typed["_debug"].(map[string]any); !ok {
		t.Fatalf("expected _debug map for slice payload")
	}
	if _, ok := typed["items"].([]any); !ok {
		t.Fatalf("expected items array for slice payload")
	}
}
