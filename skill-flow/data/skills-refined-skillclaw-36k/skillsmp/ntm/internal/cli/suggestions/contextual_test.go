package suggestions

import (
	"testing"
)

func TestSuggestNextCommand(t *testing.T) {
	tests := []struct {
		name     string
		state    State
		wantCmd  string
		wantDesc string
	}{
		{
			name:     "no sessions",
			state:    State{SessionCount: 0},
			wantCmd:  "ntm spawn",
			wantDesc: "Start a new session",
		},
		{
			name:     "recent error",
			state:    State{SessionCount: 1, ActiveSessions: []string{"proj"}, RecentError: true, CurrentSession: "proj"},
			wantCmd:  "ntm logs",
			wantDesc: "Check logs for errors",
		},
		{
			name:     "many sessions",
			state:    State{SessionCount: 5},
			wantCmd:  "ntm dashboard",
			wantDesc: "View all sessions",
		},
		{
			name:     "busy session",
			state:    State{SessionCount: 1, CurrentSession: "proj", BusyAgents: 2, IdleAgents: 0},
			wantCmd:  "ntm dashboard",
			wantDesc: "Monitor progress",
		},
		{
			name:     "idle session with beads",
			state:    State{SessionCount: 1, CurrentSession: "proj", BusyAgents: 0, IdleAgents: 2, HasBeads: true},
			wantCmd:  "ntm assign",
			wantDesc: "Assign work",
		},
		{
			name:     "idle session no beads",
			state:    State{SessionCount: 1, CurrentSession: "proj", BusyAgents: 0, IdleAgents: 2, HasBeads: false},
			wantCmd:  "ntm send",
			wantDesc: "Send prompt",
		},
		{
			name:     "fallback attach",
			state:    State{SessionCount: 1, ActiveSessions: []string{"proj"}},
			wantCmd:  "ntm attach",
			wantDesc: "Connect to session",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := SuggestNextCommand(tt.state)
			if got == nil {
				t.Fatalf("expected suggestion, got nil")
			}
			if got.Command != tt.wantCmd {
				t.Errorf("expected command %q, got %q", tt.wantCmd, got.Command)
			}
			if got.Description != tt.wantDesc {
				t.Errorf("expected description %q, got %q", tt.wantDesc, got.Description)
			}
		})
	}
}
