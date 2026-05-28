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

// CodexParser parses sessions from Codex CLI (~/.codex/sessions/)
type CodexParser struct {
	basePath   string
	exportPath string
}

// NewCodexParser creates a parser for Codex sessions
func NewCodexParser(basePath string) *CodexParser {
	if basePath == "" {
		basePath = DefaultCodexPath()
	}
	return &CodexParser{basePath: basePath}
}

// WithExport configures the parser to export sessions to the given path
func (p *CodexParser) WithExport(exportPath string) *CodexParser {
	p.exportPath = exportPath
	return p
}

// DefaultCodexPath returns the default path to Codex sessions
func DefaultCodexPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".codex", "sessions")
}

// codexEvent represents a single line in a Codex JSONL file
type codexEvent struct {
	Timestamp string          `json:"timestamp"`
	Type      string          `json:"type"`
	Payload   json.RawMessage `json:"payload"`
}

// codexSessionMeta is the payload for session_meta events
type codexSessionMeta struct {
	ID            string `json:"id"`
	Timestamp     string `json:"timestamp"`
	CWD           string `json:"cwd"`
	Originator    string `json:"originator"`
	CLIVersion    string `json:"cli_version"`
	Instructions  string `json:"instructions"`
	Source        string `json:"source"`
	ModelProvider string `json:"model_provider"`
	Git           struct {
		CommitHash    string `json:"commit_hash"`
		Branch        string `json:"branch"`
		RepositoryURL string `json:"repository_url"`
	} `json:"git"`
}

// codexResponseItem is the payload for response_item events
type codexResponseItem struct {
	Type    string `json:"type"`
	Role    string `json:"role"`
	Content []struct {
		Type string `json:"type"`
		Text string `json:"text"`
	} `json:"content"`
}

// ParseAll parses all Codex sessions
func (p *CodexParser) ParseAll() ([]*ParsedSession, []error) {
	return p.ParseAllWithStats(nil)
}

// ParseAllWithStats parses all sessions and optionally returns export stats
func (p *CodexParser) ParseAllWithStats(exportStats *ExportStats) ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	// Check if sessions directory exists
	if _, err := os.Stat(p.basePath); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("codex sessions directory not found: %s", p.basePath)}
	}

	// Setup export directory if exporting
	var exportDir string
	if p.exportPath != "" {
		exportDir = filepath.Join(p.exportPath, "codex")
		if err := os.MkdirAll(exportDir, 0755); err != nil {
			return nil, []error{fmt.Errorf("failed to create codex export dir: %w", err)}
		}
	}

	exportedFiles := 0

	// Walk the sessions directory (YYYY/MM/DD/*.jsonl structure)
	err := filepath.Walk(p.basePath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil // Skip files with errors
		}
		if info.IsDir() {
			return nil
		}
		if !strings.HasSuffix(path, ".jsonl") {
			return nil
		}

		session, parseErr := p.parseFile(path)
		if parseErr != nil {
			errors = append(errors, fmt.Errorf("%s: %w", path, parseErr))
			return nil
		}
		if session != nil {
			sessions = append(sessions, session)

			// Export if configured
			if exportDir != "" {
				exportFile := filepath.Join(exportDir, session.Session.ID+".jsonl")
				data, _ := os.ReadFile(path)
				if err := os.WriteFile(exportFile, data, 0644); err != nil {
					errors = append(errors, fmt.Errorf("failed to export %s: %w", session.Session.ID, err))
				} else {
					exportedFiles++
				}
			}
		}
		return nil
	})

	if err != nil {
		errors = append(errors, fmt.Errorf("failed to walk sessions directory: %w", err))
	}

	if exportStats != nil {
		exportStats.ComposerFiles = exportedFiles
	}

	return sessions, errors
}

// parseFile parses a single Codex JSONL session file
func (p *CodexParser) parseFile(path string) (*ParsedSession, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	var meta *codexSessionMeta
	var messages []models.Message
	rawLines := []string{}
	sequence := 0

	scanner := bufio.NewScanner(file)
	// Increase buffer size for potentially long lines
	buf := make([]byte, 0, 64*1024)
	scanner.Buffer(buf, 10*1024*1024) // 10MB max line

	for scanner.Scan() {
		line := scanner.Text()
		rawLines = append(rawLines, line)

		var event codexEvent
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			continue // Skip malformed lines
		}

		switch event.Type {
		case "session_meta":
			var sm codexSessionMeta
			if err := json.Unmarshal(event.Payload, &sm); err == nil {
				meta = &sm
			}

		case "response_item":
			var ri codexResponseItem
			if err := json.Unmarshal(event.Payload, &ri); err == nil {
				if ri.Type == "message" && ri.Role != "" {
					// Extract text content
					var content strings.Builder
					for _, c := range ri.Content {
						if c.Type == "input_text" || c.Type == "text" {
							if content.Len() > 0 {
								content.WriteString("\n")
							}
							content.WriteString(c.Text)
						}
					}

					// Parse timestamp
					ts, _ := time.Parse(time.RFC3339, event.Timestamp)

					msg := models.Message{
						ID:        fmt.Sprintf("%s-%d", meta.ID, sequence),
						SessionID: meta.ID,
						Role:      ri.Role,
						Content:   content.String(),
						Sequence:  sequence,
						Timestamp: ts.UnixMilli(),
					}

					// Only add messages with content
					if msg.Content != "" {
						messages = append(messages, msg)
						sequence++
					}
				}
			}
		}
	}

	if meta == nil {
		return nil, nil // No valid session metadata found
	}

	// Parse session timestamp
	ts, _ := time.Parse(time.RFC3339, meta.Timestamp)

	// Infer project from CWD
	project := inferProjectFromPath(meta.CWD)

	// Determine model - Codex uses model_provider (e.g., "openai", "anthropic")
	model := meta.ModelProvider

	session := models.Session{
		ID:           meta.ID,
		Source:       "codex",
		Project:      project,
		Model:        model,
		CreatedAt:    ts.UnixMilli(),
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
