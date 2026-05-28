// Package status provides agent status detection for NTM.
// It enables monitoring whether agents are idle, working, or in error state
// by analyzing tmux pane activity and output patterns.
package status

import "time"

// AgentState represents the current state of an agent
type AgentState string

const (
	// StateIdle indicates the agent is waiting for input at a prompt
	StateIdle AgentState = "idle"
	// StateWorking indicates the agent is actively producing output
	StateWorking AgentState = "working"
	// StateError indicates the agent encountered a problem
	StateError AgentState = "error"
	// StateUnknown indicates the state cannot be determined
	StateUnknown AgentState = "unknown"
)

// Icon returns the visual indicator for a state
func (s AgentState) Icon() string {
	switch s {
	case StateIdle:
		return "\u26aa" // white circle
	case StateWorking:
		return "\U0001f7e2" // green circle
	case StateError:
		return "\U0001f534" // red circle
	default:
		return "\u26ab" // black circle
	}
}

// String returns the string representation of the state
func (s AgentState) String() string {
	return string(s)
}

// ErrorType categorizes detected errors
type ErrorType string

const (
	// ErrorNone indicates no error detected
	ErrorNone ErrorType = ""
	// ErrorRateLimit indicates API rate limiting
	ErrorRateLimit ErrorType = "rate_limit"
	// ErrorCrash indicates the agent process crashed
	ErrorCrash ErrorType = "crash"
	// ErrorAuth indicates authentication failure
	ErrorAuth ErrorType = "auth"
	// ErrorConnection indicates network/connection issues
	ErrorConnection ErrorType = "connection"
	// ErrorGeneric indicates an unspecified error
	ErrorGeneric ErrorType = "error"
)

// Message returns a human-readable description of the error
func (e ErrorType) Message() string {
	switch e {
	case ErrorRateLimit:
		return "Rate limited - too many requests"
	case ErrorCrash:
		return "Agent crashed"
	case ErrorAuth:
		return "Authentication error"
	case ErrorConnection:
		return "Connection error"
	case ErrorGeneric:
		return "Error detected"
	default:
		return ""
	}
}

// String returns the string representation of the error type
func (e ErrorType) String() string {
	return string(e)
}

// AgentStatus represents the full status of an agent pane
type AgentStatus struct {
	// PaneID is the tmux pane identifier (e.g., "%0")
	PaneID string `json:"pane_id"`
	// PaneName is the custom pane title (e.g., "myproject__cc_1")
	PaneName string `json:"pane_name"`
	// AgentType identifies the agent type ("cc", "cod", "gmi", "user")
	AgentType string `json:"agent_type"`
	// State is the current agent state
	State AgentState `json:"state"`
	// ErrorType categorizes the error if State == StateError
	ErrorType ErrorType `json:"error_type,omitempty"`
	// LastActive is when the pane last had output activity
	LastActive time.Time `json:"last_active"`
	// LastOutput contains the last N characters of output (for preview)
	LastOutput string `json:"last_output,omitempty"`
	// UpdatedAt is when this status was computed
	UpdatedAt time.Time `json:"updated_at"`
}

// IsHealthy returns true if the agent is in a healthy state (idle or working)
func (s *AgentStatus) IsHealthy() bool {
	return s.State == StateIdle || s.State == StateWorking
}

// IdleDuration returns how long the agent has been idle since LastActive
func (s *AgentStatus) IdleDuration() time.Duration {
	return time.Since(s.LastActive)
}
