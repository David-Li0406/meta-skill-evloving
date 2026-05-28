package suggestions

import (
	"fmt"
)

// State captures the current NTM system state for suggestion logic.
type State struct {
	SessionCount   int
	ActiveSessions []string
	BusyAgents     int
	IdleAgents     int
	HasBeads       bool
	RecentError    bool
	LastCommand    string
	CurrentSession string
}

// Suggestion represents a recommended next action.
type Suggestion struct {
	Command     string
	Description string
	Example     string
	Reason      string
}

// SuggestNextCommand analyzes the state and returns the best next command suggestion.
func SuggestNextCommand(s State) *Suggestion {
	// Case 1: No sessions running
	if s.SessionCount == 0 {
		return &Suggestion{
			Command:     "ntm spawn",
			Description: "Start a new session",
			Example:     "ntm spawn myproject",
			Reason:      "No active sessions found",
		}
	}

	// Case 2: Recent error
	if s.RecentError {
		session := s.CurrentSession
		if session == "" && len(s.ActiveSessions) > 0 {
			session = s.ActiveSessions[0]
		}
		if session != "" {
			return &Suggestion{
				Command:     "ntm logs",
				Description: "Check logs for errors",
				Example:     fmt.Sprintf("ntm logs %s", session),
				Reason:      "Recent command failed",
			}
		}
	}

	// Case 3: Many sessions running
	if s.SessionCount > 3 {
		return &Suggestion{
			Command:     "ntm dashboard",
			Description: "View all sessions",
			Example:     "ntm dashboard",
			Reason:      "Multiple active sessions",
		}
	}

	// Case 4: Specific session context
	if s.CurrentSession != "" {
		// If all agents busy
		if s.BusyAgents > 0 && s.IdleAgents == 0 {
			return &Suggestion{
				Command:     "ntm dashboard",
				Description: "Monitor progress",
				Example:     fmt.Sprintf("ntm dashboard %s", s.CurrentSession),
				Reason:      "Agents are busy",
			}
		}

		// If agents idle
		if s.IdleAgents > 0 {
			// If beads available
			if s.HasBeads {
				return &Suggestion{
					Command:     "ntm assign",
					Description: "Assign work",
					Example:     fmt.Sprintf("ntm assign %s", s.CurrentSession),
					Reason:      "Agents idle and beads available",
				}
			}

			// Just idle
			return &Suggestion{
				Command:     "ntm send",
				Description: "Send prompt",
				Example:     fmt.Sprintf("ntm send %s --msg='...'", s.CurrentSession),
				Reason:      "Agents ready for work",
			}
		}
	}

	// Default fallback
	if len(s.ActiveSessions) > 0 {
		return &Suggestion{
			Command:     "ntm attach",
			Description: "Connect to session",
			Example:     fmt.Sprintf("ntm attach %s", s.ActiveSessions[0]),
			Reason:      "Session active",
		}
	}

	return nil
}
