package models

// Session represents a parsed AI conversation session
type Session struct {
	ID           string `json:"id"`            // composerId UUID
	Source       string `json:"source"`        // 'cursor', 'claude', etc.
	Project      string `json:"project"`       // inferred from file paths
	Model        string `json:"model"`         // AI model used (e.g. 'claude-4.5-opus-high-thinking')
	CreatedAt    int64  `json:"created_at"`    // unix timestamp (ms)
	MessageCount int    `json:"message_count"` // number of messages
	Summary      string `json:"summary"`       // optional generated summary
}

// Message represents a single message in a conversation
type Message struct {
	ID        string `json:"id"`         // bubbleId
	SessionID string `json:"session_id"` // references Session.ID
	Role      string `json:"role"`       // 'user', 'assistant', 'tool'
	Content   string `json:"content"`    // text content
	Sequence  int    `json:"sequence"`   // order in conversation
	Timestamp int64  `json:"timestamp"`  // optional timestamp
}

// FileReference represents a file referenced in a session
type FileReference struct {
	SessionID string `json:"session_id"`
	FilePath  string `json:"file_path"`
}

// SyncResult contains stats from a sync operation
type SyncResult struct {
	Source     string `json:"source"`
	Synced     int    `json:"synced"`
	New        int    `json:"new"`
	Updated    int    `json:"updated"`
	Errors     int    `json:"errors"`
	DurationMs int64  `json:"duration_ms"`
}

// SessionWithMessages is a session with its messages for display
type SessionWithMessages struct {
	Session  Session   `json:"session"`
	Messages []Message `json:"messages"`
	Files    []string  `json:"files"`
}
