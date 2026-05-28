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

// ClaudeCodeParser parses sessions from Claude Code CLI (~/.claude/projects/)
type ClaudeCodeParser struct {
	basePath   string
	exportPath string
}

// NewClaudeCodeParser creates a parser for Claude Code CLI sessions
func NewClaudeCodeParser(basePath string) *ClaudeCodeParser {
	if basePath == "" {
		basePath = DefaultClaudeCodePath()
	}
	return &ClaudeCodeParser{basePath: basePath}
}

// WithExport configures the parser to export sessions to the given path
func (p *ClaudeCodeParser) WithExport(exportPath string) *ClaudeCodeParser {
	p.exportPath = exportPath
	return p
}

// DefaultClaudeCodePath returns the default path to Claude Code CLI projects
func DefaultClaudeCodePath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".claude", "projects")
}

// claudeCodeEvent represents a single line in a Claude Code JSONL file
type claudeCodeEvent struct {
	Type       string          `json:"type"`
	Timestamp  string          `json:"timestamp"`
	SessionID  string          `json:"sessionId"`
	UUID       string          `json:"uuid"`
	ParentUUID string          `json:"parentUuid"`
	CWD        string          `json:"cwd"`
	Version    string          `json:"version"`
	GitBranch  string          `json:"gitBranch"`
	Message    json.RawMessage `json:"message"`
}

// claudeCodeMessage represents a message in Claude Code
type claudeCodeMessage struct {
	Role    string `json:"role"`
	Content any    `json:"content"` // can be string or array
	Model   string `json:"model"`
	ID      string `json:"id"`
}

// ParseAll parses all Claude Code CLI sessions
func (p *ClaudeCodeParser) ParseAll() ([]*ParsedSession, []error) {
	return p.ParseAllWithStats(nil)
}

// ParseAllWithStats parses all sessions and optionally returns export stats
func (p *ClaudeCodeParser) ParseAllWithStats(exportStats *ExportStats) ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	// Check if projects directory exists
	if _, err := os.Stat(p.basePath); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("claude code projects directory not found: %s", p.basePath)}
	}

	// Setup export directory if exporting
	var exportDir string
	if p.exportPath != "" {
		exportDir = filepath.Join(p.exportPath, "claude-code")
		if err := os.MkdirAll(exportDir, 0755); err != nil {
			return nil, []error{fmt.Errorf("failed to create claude-code export dir: %w", err)}
		}
	}

	exportedFiles := 0

	// Walk through project directories
	projectDirs, err := os.ReadDir(p.basePath)
	if err != nil {
		return nil, []error{fmt.Errorf("failed to read projects directory: %w", err)}
	}

	for _, projectDir := range projectDirs {
		if !projectDir.IsDir() {
			continue
		}

		projectPath := filepath.Join(p.basePath, projectDir.Name())
		files, err := os.ReadDir(projectPath)
		if err != nil {
			errors = append(errors, fmt.Errorf("failed to read project dir %s: %w", projectDir.Name(), err))
			continue
		}

		for _, file := range files {
			// Only parse top-level JSONL files (not subagent files in subdirs)
			if file.IsDir() || !strings.HasSuffix(file.Name(), ".jsonl") {
				continue
			}

			// Skip agent-*.jsonl files (subagents) at top level
			if strings.HasPrefix(file.Name(), "agent-") {
				continue
			}

			filePath := filepath.Join(projectPath, file.Name())
			session, parseErr := p.parseFile(filePath, projectDir.Name())
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
	}

	if exportStats != nil {
		exportStats.ComposerFiles = exportedFiles
	}

	return sessions, errors
}

// parseFile parses a single Claude Code JSONL session file
func (p *ClaudeCodeParser) parseFile(path, projectDirName string) (*ParsedSession, error) {
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

		var event claudeCodeEvent
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			continue // Skip malformed lines
		}

		// Extract session ID from first event
		if sessionID == "" && event.SessionID != "" {
			sessionID = event.SessionID
		}

		// Extract CWD from first event that has it
		if cwd == "" && event.CWD != "" {
			cwd = event.CWD
		}

		// Parse timestamp
		ts, _ := time.Parse(time.RFC3339, event.Timestamp)
		if firstTimestamp.IsZero() && !ts.IsZero() {
			firstTimestamp = ts
		}

		// Parse messages
		switch event.Type {
		case "user":
			var msg claudeCodeMessage
			if err := json.Unmarshal(event.Message, &msg); err == nil {
				content := extractClaudeCodeContent(msg.Content)
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
			var msg claudeCodeMessage
			if err := json.Unmarshal(event.Message, &msg); err == nil {
				// Extract model from assistant messages
				if model == "" && msg.Model != "" {
					model = msg.Model
				}

				content := extractClaudeCodeContent(msg.Content)
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

	// Infer project from directory name or CWD
	project := ""
	if cwd != "" {
		project = inferProjectFromPath(cwd)
	}
	if project == "" {
		// Try to extract from directory name (format: -Users-tyler-path-to-project)
		parts := strings.Split(projectDirName, "-")
		if len(parts) > 3 {
			project = parts[len(parts)-1]
		}
	}

	session := models.Session{
		ID:           sessionID,
		Source:       "claude-code",
		Project:      project,
		Model:        model,
		CreatedAt:    firstTimestamp.UnixMilli(),
		MessageCount: len(messages),
	}

	return &ParsedSession{
		Session:         session,
		Messages:        messages,
		MessageMetadata: make(map[string]string),
		Files:           []string{},
		RawJSON:         strings.Join(rawLines, "\n"),
	}, nil
}

// extractClaudeCodeContent extracts text content from Claude Code message content
func extractClaudeCodeContent(content any) string {
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
