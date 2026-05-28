package sync

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/Napageneral/aix/internal/models"
)

// ClaudeParser parses sessions from Claude Desktop
// Note: Claude Desktop stores actual messages in LevelDB (Session Storage),
// so this parser extracts session metadata from JSON files.
// Full message content would require LevelDB parsing.
type ClaudeParser struct {
	basePath   string
	exportPath string
}

// NewClaudeParser creates a parser for Claude Desktop sessions
func NewClaudeParser(basePath string) *ClaudeParser {
	if basePath == "" {
		basePath = DefaultClaudePath()
	}
	return &ClaudeParser{basePath: basePath}
}

// WithExport configures the parser to export sessions to the given path
func (p *ClaudeParser) WithExport(exportPath string) *ClaudeParser {
	p.exportPath = exportPath
	return p
}

// DefaultClaudePath returns the default path to Claude Desktop sessions
func DefaultClaudePath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "Library", "Application Support", "Claude", "claude-code-sessions")
}

// claudeSessionMeta represents the Claude Desktop session metadata
type claudeSessionMeta struct {
	SessionID      string `json:"sessionId"`
	CLISessionID   string `json:"cliSessionId"`
	CWD            string `json:"cwd"`
	OriginCWD      string `json:"originCwd"`
	CreatedAt      int64  `json:"createdAt"`
	LastActivityAt int64  `json:"lastActivityAt"`
	Model          string `json:"model"`
	IsArchived     bool   `json:"isArchived"`
	Title          string `json:"title"`
	PermissionMode string `json:"permissionMode"`
}

// ParseAll parses all Claude Desktop sessions
func (p *ClaudeParser) ParseAll() ([]*ParsedSession, []error) {
	return p.ParseAllWithStats(nil)
}

// ParseAllWithStats parses all sessions and optionally returns export stats
func (p *ClaudeParser) ParseAllWithStats(exportStats *ExportStats) ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	// Check if sessions directory exists
	if _, err := os.Stat(p.basePath); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("claude sessions directory not found: %s", p.basePath)}
	}

	// Setup export directory if exporting
	var exportDir string
	if p.exportPath != "" {
		exportDir = filepath.Join(p.exportPath, "claude")
		if err := os.MkdirAll(exportDir, 0755); err != nil {
			return nil, []error{fmt.Errorf("failed to create claude export dir: %w", err)}
		}
	}

	exportedFiles := 0

	// Walk the sessions directory (nested UUID structure)
	err := filepath.Walk(p.basePath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil // Skip files with errors
		}
		if info.IsDir() {
			return nil
		}
		if !strings.HasSuffix(path, ".json") {
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
				exportFile := filepath.Join(exportDir, session.Session.ID+".json")
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

// parseFile parses a single Claude Desktop session file
func (p *ClaudeParser) parseFile(path string) (*ParsedSession, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	var meta claudeSessionMeta
	if err := json.Unmarshal(data, &meta); err != nil {
		return nil, fmt.Errorf("failed to parse JSON: %w", err)
	}

	// Skip if no session ID
	if meta.SessionID == "" {
		return nil, nil
	}

	// Infer project from CWD
	project := inferProjectFromPath(meta.CWD)

	session := models.Session{
		ID:           meta.SessionID,
		Source:       "claude",
		Project:      project,
		Model:        meta.Model,
		CreatedAt:    meta.CreatedAt,
		MessageCount: 0, // Messages are in LevelDB, not easily accessible
		Summary:      meta.Title,
	}

	// Note: Claude Desktop stores actual messages in LevelDB (Session Storage)
	// which requires a LevelDB library to parse. For now, we only capture
	// session metadata. The MessageCount is set to 0 as messages aren't extracted.
	
	return &ParsedSession{
		Session:         session,
		Messages:        []models.Message{},
		MessageMetadata: make(map[string]string),
		Files:           []string{},
		RawJSON:         string(data),
	}, nil
}
