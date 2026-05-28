package status

// Detector detects agent status from tmux pane state.
// Implementations analyze pane activity timestamps, output content,
// and pattern matching to determine the current state.
type Detector interface {
	// Detect returns the current status of a single pane.
	// The paneID can be a tmux pane ID (e.g., "%0") or a target
	// specification (e.g., "mysession:0.1").
	Detect(paneID string) (AgentStatus, error)

	// DetectAll returns status for all panes in a session.
	// Returns a slice of AgentStatus, one for each pane in the session.
	DetectAll(session string) ([]AgentStatus, error)
}

// DetectorConfig holds configuration for status detection
type DetectorConfig struct {
	// ActivityThreshold is how long since last activity before considering idle
	ActivityThreshold int `json:"activity_threshold_secs"`
	// OutputPreviewLength is max characters to include in LastOutput
	OutputPreviewLength int `json:"output_preview_length"`
	// ScanLines is how many lines of output to scan for patterns
	ScanLines int `json:"scan_lines"`
}

// DefaultConfig returns the default detector configuration
func DefaultConfig() DetectorConfig {
	return DetectorConfig{
		ActivityThreshold:   5,   // 5 seconds
		OutputPreviewLength: 200, // 200 characters
		ScanLines:           50,  // Last 50 lines
	}
}
