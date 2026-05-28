package sync

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/Napageneral/aix/internal/models"
)

// OpenCodeParser parses sessions from OpenCode (~/.local/share/opencode/storage/)
type OpenCodeParser struct {
	basePath   string
	exportPath string
}

// NewOpenCodeParser creates a parser for OpenCode sessions
func NewOpenCodeParser(basePath string) *OpenCodeParser {
	if basePath == "" {
		basePath = DefaultOpenCodePath()
	}
	return &OpenCodeParser{basePath: basePath}
}

// WithExport configures the parser to export sessions to the given path
func (p *OpenCodeParser) WithExport(exportPath string) *OpenCodeParser {
	p.exportPath = exportPath
	return p
}

// DefaultOpenCodePath returns the default path to OpenCode storage
func DefaultOpenCodePath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".local", "share", "opencode", "storage")
}

// openCodeSession is the session metadata structure
type openCodeSession struct {
	ID        string `json:"id"`
	Version   string `json:"version"`
	ProjectID string `json:"projectID"`
	Directory string `json:"directory"`
	Title     string `json:"title"`
	Time      struct {
		Created int64 `json:"created"`
		Updated int64 `json:"updated"`
	} `json:"time"`
	Summary struct {
		Additions int `json:"additions"`
		Deletions int `json:"deletions"`
		Files     int `json:"files"`
	} `json:"summary"`
}

// openCodeMessage is the message metadata structure
type openCodeMessage struct {
	ID        string `json:"id"`
	SessionID string `json:"sessionID"`
	Role      string `json:"role"`
	Time      struct {
		Created int64 `json:"created"`
	} `json:"time"`
	Summary struct {
		Title string   `json:"title"`
		Diffs []string `json:"diffs"`
	} `json:"summary"`
	Agent string `json:"agent"`
	Model struct {
		ProviderID string `json:"providerID"`
		ModelID    string `json:"modelID"`
	} `json:"model"`
}

// openCodePart is the message part (content) structure
type openCodePart struct {
	ID        string `json:"id"`
	SessionID string `json:"sessionID"`
	MessageID string `json:"messageID"`
	Type      string `json:"type"`
	Text      string `json:"text"`
}

// ParseAll parses all OpenCode sessions
func (p *OpenCodeParser) ParseAll() ([]*ParsedSession, []error) {
	return p.ParseAllWithStats(nil)
}

// ParseAllWithStats parses all sessions and optionally returns export stats
func (p *OpenCodeParser) ParseAllWithStats(exportStats *ExportStats) ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	// Check if storage directory exists
	if _, err := os.Stat(p.basePath); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("opencode storage directory not found: %s", p.basePath)}
	}

	// Setup export directory if exporting
	var exportDir string
	if p.exportPath != "" {
		exportDir = filepath.Join(p.exportPath, "opencode")
		if err := os.MkdirAll(exportDir, 0755); err != nil {
			return nil, []error{fmt.Errorf("failed to create opencode export dir: %w", err)}
		}
	}

	exportedSessions := 0
	exportedMessages := 0

	// Find all session directories
	sessionBaseDir := filepath.Join(p.basePath, "session")
	if _, err := os.Stat(sessionBaseDir); os.IsNotExist(err) {
		return nil, []error{fmt.Errorf("opencode session directory not found: %s", sessionBaseDir)}
	}

	// Walk through project directories under session/
	projectDirs, err := os.ReadDir(sessionBaseDir)
	if err != nil {
		return nil, []error{fmt.Errorf("failed to read session directory: %w", err)}
	}

	for _, projectDir := range projectDirs {
		if !projectDir.IsDir() {
			continue
		}

		projectPath := filepath.Join(sessionBaseDir, projectDir.Name())
		sessionFiles, err := os.ReadDir(projectPath)
		if err != nil {
			errors = append(errors, fmt.Errorf("failed to read project dir %s: %w", projectDir.Name(), err))
			continue
		}

		for _, sessionFile := range sessionFiles {
			if sessionFile.IsDir() || !strings.HasSuffix(sessionFile.Name(), ".json") {
				continue
			}

			sessionPath := filepath.Join(projectPath, sessionFile.Name())
			session, parseErr := p.parseSession(sessionPath)
			if parseErr != nil {
				errors = append(errors, fmt.Errorf("%s: %w", sessionPath, parseErr))
				continue
			}
			if session != nil {
				sessions = append(sessions, session)

				// Export if configured
				if exportDir != "" {
					sessionExportDir := filepath.Join(exportDir, session.Session.ID)
					if err := os.MkdirAll(sessionExportDir, 0755); err != nil {
						errors = append(errors, fmt.Errorf("failed to create export dir for %s: %w", session.Session.ID, err))
						continue
					}

					// Export session metadata
					sessionData, _ := os.ReadFile(sessionPath)
					if err := os.WriteFile(filepath.Join(sessionExportDir, "session.json"), sessionData, 0644); err != nil {
						errors = append(errors, fmt.Errorf("failed to export session %s: %w", session.Session.ID, err))
					} else {
						exportedSessions++
					}

					// Export messages
					msgDir := filepath.Join(p.basePath, "message", session.Session.ID)
					if files, err := os.ReadDir(msgDir); err == nil {
						for _, f := range files {
							if strings.HasSuffix(f.Name(), ".json") {
								src := filepath.Join(msgDir, f.Name())
								dst := filepath.Join(sessionExportDir, "messages", f.Name())
								os.MkdirAll(filepath.Dir(dst), 0755)
								if data, err := os.ReadFile(src); err == nil {
									if err := os.WriteFile(dst, data, 0644); err == nil {
										exportedMessages++
									}
								}
							}
						}
					}
				}
			}
		}
	}

	if exportStats != nil {
		exportStats.ComposerFiles = exportedSessions
		exportStats.BubbleFiles = exportedMessages
	}

	return sessions, errors
}

// parseSession parses a single OpenCode session
func (p *OpenCodeParser) parseSession(sessionPath string) (*ParsedSession, error) {
	// Read session metadata
	data, err := os.ReadFile(sessionPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read session file: %w", err)
	}

	var sess openCodeSession
	if err := json.Unmarshal(data, &sess); err != nil {
		return nil, fmt.Errorf("failed to parse session JSON: %w", err)
	}

	if sess.ID == "" {
		return nil, nil
	}

	// Load messages for this session
	messages, msgMeta, model := p.loadMessages(sess.ID)

	// Infer project from directory
	project := inferProjectFromPath(sess.Directory)

	session := models.Session{
		ID:           sess.ID,
		Source:       "opencode",
		Project:      project,
		Model:        model,
		CreatedAt:    sess.Time.Created,
		MessageCount: len(messages),
		Summary:      sess.Title,
	}

	return &ParsedSession{
		Session:         session,
		Messages:        messages,
		MessageMetadata: msgMeta,
		Files:           []string{},
		RawJSON:         string(data),
	}, nil
}

// loadMessages loads all messages for a session
func (p *OpenCodeParser) loadMessages(sessionID string) ([]models.Message, map[string]string, string) {
	var messages []models.Message
	meta := make(map[string]string)
	model := ""

	msgDir := filepath.Join(p.basePath, "message", sessionID)
	files, err := os.ReadDir(msgDir)
	if err != nil {
		return messages, meta, model
	}

	sequence := 0
	for _, f := range files {
		if !strings.HasSuffix(f.Name(), ".json") {
			continue
		}

		msgPath := filepath.Join(msgDir, f.Name())
		msgData, err := os.ReadFile(msgPath)
		if err != nil {
			continue
		}

		var msg openCodeMessage
		if err := json.Unmarshal(msgData, &msg); err != nil {
			continue
		}

		// Get model from first message
		if model == "" && msg.Model.ModelID != "" {
			model = msg.Model.ModelID
		}

		// Load message parts (content)
		content := p.loadMessageParts(msg.ID)

		message := models.Message{
			ID:        msg.ID,
			SessionID: sessionID,
			Role:      msg.Role,
			Content:   content,
			Sequence:  sequence,
			Timestamp: msg.Time.Created,
		}

		messages = append(messages, message)
		meta[msg.ID] = string(msgData)
		sequence++
	}

	return messages, meta, model
}

// loadMessageParts loads content from message parts
func (p *OpenCodeParser) loadMessageParts(messageID string) string {
	partDir := filepath.Join(p.basePath, "part", messageID)
	files, err := os.ReadDir(partDir)
	if err != nil {
		return ""
	}

	var texts []string
	for _, f := range files {
		if !strings.HasSuffix(f.Name(), ".json") {
			continue
		}

		partPath := filepath.Join(partDir, f.Name())
		partData, err := os.ReadFile(partPath)
		if err != nil {
			continue
		}

		var part openCodePart
		if err := json.Unmarshal(partData, &part); err != nil {
			continue
		}

		if part.Type == "text" && part.Text != "" {
			texts = append(texts, part.Text)
		}
	}

	return strings.Join(texts, "\n")
}
