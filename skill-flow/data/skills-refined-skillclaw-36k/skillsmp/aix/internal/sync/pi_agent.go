package sync

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/Napageneral/aix/internal/models"
)

// PiAgentParser parses sessions from pi-coding-agent based tools (clawdbot, nexus)
type PiAgentParser struct {
	basePath       string
	source         string // "clawdbot" or "nexus"
	exportPath     string
	includeBackups bool // whether to scan .bak.* files for compaction history
}

// NewClawdbotParser creates a parser for clawdbot sessions (~/.clawdbot/sessions/)
func NewClawdbotParser(basePath string) *PiAgentParser {
	if basePath == "" {
		basePath = DefaultClawdbotPath()
	}
	return &PiAgentParser{basePath: basePath, source: "clawdbot"}
}

// NewNexusParser creates a parser for nexus sessions (~/nexus/state/sessions/)
func NewNexusParser(basePath string) *PiAgentParser {
	if basePath == "" {
		basePath = DefaultNexusPath()
	}
	return &PiAgentParser{basePath: basePath, source: "nexus"}
}

// DefaultClawdbotPath returns the default path to clawdbot sessions
func DefaultClawdbotPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".clawdbot", "sessions")
}

// DefaultNexusPath returns the default path to nexus sessions
func DefaultNexusPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "nexus", "state", "sessions")
}

// WithExport configures the parser to export sessions to the given path
func (p *PiAgentParser) WithExport(exportPath string) *PiAgentParser {
	p.exportPath = exportPath
	return p
}

// WithBackups configures the parser to include .bak.* files from compaction
func (p *PiAgentParser) WithBackups(include bool) *PiAgentParser {
	p.includeBackups = include
	return p
}

// piAgentEvent represents a single line in a pi-coding-agent JSONL file
type piAgentEvent struct {
	Type      string          `json:"type"`
	Timestamp string          `json:"timestamp"`
	SessionID string          `json:"sessionId"`
	UUID      string          `json:"uuid"`
	CWD       string          `json:"cwd"`
	Version   string          `json:"version"`
	ID        string          `json:"id"`      // for session header
	Message   json.RawMessage `json:"message"` // for user/assistant events
}

// piAgentMessage represents a message payload in pi-coding-agent
type piAgentMessage struct {
	Role    string `json:"role"`
	Content any    `json:"content"` // can be string or array of content blocks
	Model   string `json:"model"`
	API     string `json:"api"`
}

// SessionEntry represents the rich metadata from sessions.json
type SessionEntry struct {
	SessionID        string           `json:"sessionId"`
	UpdatedAt        int64            `json:"updatedAt"`
	SessionFile      string           `json:"sessionFile,omitempty"`
	InputTokens      int64            `json:"inputTokens,omitempty"`
	OutputTokens     int64            `json:"outputTokens,omitempty"`
	TotalTokens      int64            `json:"totalTokens,omitempty"`
	ContextTokens    int64            `json:"contextTokens,omitempty"`
	CompactionCount  int              `json:"compactionCount,omitempty"`
	Model            string           `json:"model,omitempty"`
	ModelProvider    string           `json:"modelProvider,omitempty"`
	Origin           *SessionOrigin   `json:"origin,omitempty"`
	QueueMode        string           `json:"queueMode,omitempty"`
}

// SessionOrigin tracks where a session originated from
type SessionOrigin struct {
	Label     string `json:"label,omitempty"`
	Provider  string `json:"provider,omitempty"`  // telegram, whatsapp, discord, etc.
	Surface   string `json:"surface,omitempty"`   // dm, group, channel
	ChatType  string `json:"chatType,omitempty"`
	From      string `json:"from,omitempty"`
	To        string `json:"to,omitempty"`
	AccountID string `json:"accountId,omitempty"`
	ThreadID  string `json:"threadId,omitempty"`
}

// ParseAll parses all pi-agent sessions
func (p *PiAgentParser) ParseAll() ([]*ParsedSession, []error) {
	return p.ParseAllWithStats(nil)
}

// ParseAllWithStats parses all sessions and optionally returns export stats
func (p *PiAgentParser) ParseAllWithStats(exportStats *ExportStats) ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	// Check if sessions directory exists
	if _, err := os.Stat(p.basePath); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("%s sessions directory not found: %s", p.source, p.basePath)}
	}

	// Load sessions.json for rich metadata
	sessionsStore := p.loadSessionsStore()

	// Setup export directory if exporting
	var exportDir string
	if p.exportPath != "" {
		exportDir = filepath.Join(p.exportPath, p.source)
		if err := os.MkdirAll(exportDir, 0755); err != nil {
			return nil, []error{fmt.Errorf("failed to create %s export dir: %w", p.source, err)}
		}
	}

	exportedFiles := 0

	// Read all JSONL files in the sessions directory
	entries, err := os.ReadDir(p.basePath)
	if err != nil {
		return nil, []error{fmt.Errorf("failed to read sessions directory: %w", err)}
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}

		name := entry.Name()

		// Parse main session files
		if strings.HasSuffix(name, ".jsonl") && !strings.Contains(name, ".bak.") {
			filePath := filepath.Join(p.basePath, name)
			sessionID := strings.TrimSuffix(name, ".jsonl")

			// Get rich metadata from sessions.json
			var storeEntry *SessionEntry
			if sessionsStore != nil {
				if e, ok := sessionsStore[sessionID]; ok {
					storeEntry = &e
				}
			}

			session, parseErr := p.parseFile(filePath, storeEntry)
			if parseErr != nil {
				errors = append(errors, fmt.Errorf("%s: %w", filePath, parseErr))
				continue
			}
			if session != nil {
				sessions = append(sessions, session)

				// Export if configured
				if exportDir != "" {
					exportFile := filepath.Join(exportDir, session.Session.ID+".jsonl")
					data, _ := os.ReadFile(filePath)
					if err := os.WriteFile(exportFile, data, 0644); err != nil {
						errors = append(errors, fmt.Errorf("failed to export %s: %w", session.Session.ID, err))
					} else {
						exportedFiles++
					}
				}
			}
		}

		// Optionally parse backup files from compaction
		if p.includeBackups && strings.Contains(name, ".jsonl.bak.") {
			filePath := filepath.Join(p.basePath, name)
			// Extract session ID from backup filename (e.g., "abc123.jsonl.bak.2026-01-21T12-00-00.000Z")
			parts := strings.Split(name, ".jsonl.bak.")
			if len(parts) >= 1 {
				sessionID := parts[0]
				backupSession, parseErr := p.parseBackupFile(filePath, sessionID)
				if parseErr != nil {
					errors = append(errors, fmt.Errorf("%s: %w", filePath, parseErr))
					continue
				}
				if backupSession != nil {
					// Mark as backup in the session ID to avoid collisions
					backupSession.Session.ID = fmt.Sprintf("%s-bak-%s", sessionID, parts[1])
					sessions = append(sessions, backupSession)
				}
			}
		}
	}

	if exportStats != nil {
		exportStats.ComposerFiles = exportedFiles
	}

	return sessions, errors
}

// loadSessionsStore loads the sessions.json metadata file
func (p *PiAgentParser) loadSessionsStore() map[string]SessionEntry {
	storePath := filepath.Join(p.basePath, "sessions.json")
	data, err := os.ReadFile(storePath)
	if err != nil {
		return nil
	}

	var store map[string]SessionEntry
	if err := json.Unmarshal(data, &store); err != nil {
		return nil
	}

	return store
}

// parseFile parses a single pi-agent JSONL session file
func (p *PiAgentParser) parseFile(path string, storeEntry *SessionEntry) (*ParsedSession, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	var sessionID string
	var cwd string
	var model string
	var firstTimestamp time.Time
	var messages []models.Message
	rawLines := []string{}
	sequence := 0

	scanner := bufio.NewScanner(file)
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 10*1024*1024) // 10MB max line

	for scanner.Scan() {
		line := scanner.Text()
		rawLines = append(rawLines, line)

		var event piAgentEvent
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			continue // Skip malformed lines
		}

		// Parse timestamp
		ts, _ := time.Parse(time.RFC3339, event.Timestamp)
		if firstTimestamp.IsZero() && !ts.IsZero() {
			firstTimestamp = ts
		}

		switch event.Type {
		case "session":
			// Session header event
			if sessionID == "" {
				sessionID = event.ID
				if sessionID == "" {
					sessionID = event.SessionID
				}
			}
			if cwd == "" && event.CWD != "" {
				cwd = event.CWD
			}

		case "user":
			if sessionID == "" && event.SessionID != "" {
				sessionID = event.SessionID
			}

			var msg piAgentMessage
			if err := json.Unmarshal(event.Message, &msg); err == nil {
				content := extractPiAgentContent(msg.Content)
				if content != "" {
					messages = append(messages, models.Message{
						ID:        event.UUID,
						SessionID: sessionID,
						Role:      "user",
						Content:   content,
						Sequence:  sequence,
						Timestamp: ts.UnixMilli(),
					})
					sequence++
				}
			}

		case "assistant":
			if sessionID == "" && event.SessionID != "" {
				sessionID = event.SessionID
			}

			var msg piAgentMessage
			if err := json.Unmarshal(event.Message, &msg); err == nil {
				// Extract model from assistant messages
				if model == "" && msg.Model != "" {
					model = msg.Model
				}

				content := extractPiAgentContent(msg.Content)
				if content != "" {
					messages = append(messages, models.Message{
						ID:        event.UUID,
						SessionID: sessionID,
						Role:      "assistant",
						Content:   content,
						Sequence:  sequence,
						Timestamp: ts.UnixMilli(),
					})
					sequence++
				}
			}
		}
	}

	if sessionID == "" {
		return nil, nil // No valid session found
	}

	// Infer project from CWD
	project := ""
	if cwd != "" {
		project = inferProjectFromPath(cwd)
	}

	// Use model from store entry if not found in transcript
	if model == "" && storeEntry != nil && storeEntry.Model != "" {
		model = storeEntry.Model
	}

	session := models.Session{
		ID:           sessionID,
		Source:       p.source,
		Project:      project,
		Model:        model,
		CreatedAt:    firstTimestamp.UnixMilli(),
		MessageCount: len(messages),
	}

	// Build metadata JSON with rich session entry data
	metadataJSON := ""
	if storeEntry != nil {
		if data, err := json.Marshal(storeEntry); err == nil {
			metadataJSON = string(data)
		}
	}

	return &ParsedSession{
		Session:         session,
		Messages:        messages,
		MessageMetadata: map[string]string{"session_entry": metadataJSON},
		Files:           []string{},
		RawJSON:         strings.Join(rawLines, "\n"),
	}, nil
}

// parseBackupFile parses a compaction backup file
func (p *PiAgentParser) parseBackupFile(path, originalSessionID string) (*ParsedSession, error) {
	// Backup files have the same format, just parse normally
	session, err := p.parseFile(path, nil)
	if err != nil {
		return nil, err
	}
	if session == nil {
		return nil, nil
	}

	// Mark as archive source
	session.MessageMetadata["archive_source"] = path
	session.MessageMetadata["original_session_id"] = originalSessionID

	return session, nil
}

// extractPiAgentContent extracts text content from pi-agent message content
func extractPiAgentContent(content any) string {
	switch v := content.(type) {
	case string:
		return v
	case []interface{}:
		var texts []string
		for _, item := range v {
			if m, ok := item.(map[string]interface{}); ok {
				if t, ok := m["type"].(string); ok && t == "text" {
					if text, ok := m["text"].(string); ok {
						texts = append(texts, text)
					}
				}
			}
		}
		return strings.Join(texts, "\n")
	default:
		return ""
	}
}
