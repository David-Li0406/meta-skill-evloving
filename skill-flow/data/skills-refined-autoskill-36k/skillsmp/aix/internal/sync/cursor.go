package sync

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/Napageneral/aix/internal/models"
)

// CursorComposerData represents the raw Cursor composer JSON structure
type CursorComposerData struct {
	ComposerID   string                   `json:"composerId"`
	Text         string                   `json:"text"`
	RichText     string                   `json:"richText"`
	CreatedAt    int64                    `json:"createdAt"`
	Conversation []map[string]interface{} `json:"conversation"`
	Context      struct {
		FileSelections []struct {
			URI struct {
				FsPath string `json:"fsPath"`
			} `json:"uri"`
		} `json:"fileSelections"`
	} `json:"context"`
}

// CursorParser handles parsing Cursor session files
type CursorParser struct {
	sourcePath string
}

// NewCursorParser creates a new Cursor parser
func NewCursorParser(sourcePath string) *CursorParser {
	return &CursorParser{sourcePath: sourcePath}
}

// ParseAll parses all JSON files in the source directory
func (p *CursorParser) ParseAll() ([]*ParsedSession, []error) {
	var sessions []*ParsedSession
	var errors []error

	entries, err := os.ReadDir(p.sourcePath)
	if err != nil {
		return nil, []error{fmt.Errorf("failed to read directory: %w", err)}
	}

	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".json") {
			continue
		}

		filePath := filepath.Join(p.sourcePath, entry.Name())
		session, err := p.ParseFile(filePath)
		if err != nil {
			errors = append(errors, fmt.Errorf("%s: %w", entry.Name(), err))
			continue
		}

		if session != nil {
			sessions = append(sessions, session)
		}
	}

	return sessions, errors
}

// ParsedSession contains a parsed session with its messages and files
type ParsedSession struct {
	Session  models.Session
	Messages []models.Message
	// MessageMetadata maps message_id -> JSON metadata blob (Cursor-specific fields).
	MessageMetadata map[string]string
	Capabilities    []MessageCapability
	Lints           []MessageLint
	MessageFiles    []MessageFileRef
	Codeblocks      []MessageCodeblock
	Files           []string
	RawJSON         string
}

type MessageCapability struct {
	MessageID  string
	SessionID  string
	Phase      string
	Capability int
}

type MessageLint struct {
	MessageID string
	SessionID string

	FilePath  string
	Message   string
	Source    string
	StartLine int
	StartCol  int
	EndLine   int
	EndCol    int
}

type MessageFileRef struct {
	MessageID  string
	SessionID  string
	Kind       string
	FilePath   string
	LineNumber int
}

type MessageCodeblock struct {
	MessageID string
	SessionID string
	Idx       int
	RawJSON   string
}

// ParseFile parses a single Cursor session file
func (p *CursorParser) ParseFile(filePath string) (*ParsedSession, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	// First try standard JSON parsing
	var composer CursorComposerData
	err = json.Unmarshal(data, &composer)
	if err != nil {
		// Try with preprocessed JSON to handle embedded newlines
		cleanedData := preprocessJSON(data)
		err = json.Unmarshal(cleanedData, &composer)
		if err != nil {
			// Last resort: scrub known-problematic fields (symbolLinks/codeBlocks/diffHistories)
			scrubbed := scrubKnownBadFields(cleanedData)
			if err2 := json.Unmarshal(scrubbed, &composer); err2 != nil {
				// Final fallback: salvage minimal session metadata so sync can proceed without errors.
				if ps := salvageSession(filePath, data); ps != nil {
					return ps, nil
				}
				return nil, fmt.Errorf("failed to parse JSON: %w", err)
			}
		}
	}

	// Skip empty sessions (no conversations)
	if len(composer.Conversation) == 0 && composer.Text == "" {
		return nil, nil
	}

	// Extract project from file paths
	project := extractProject(composer)

	// Build session
	session := models.Session{
		ID:           composer.ComposerID,
		Source:       "cursor",
		Project:      project,
		CreatedAt:    composer.CreatedAt,
		MessageCount: len(composer.Conversation),
	}

	// If no createdAt, try to infer from file mod time
	if session.CreatedAt == 0 {
		// Try UUIDv7 timestamp from composerId first (if applicable)
		if ts, ok := uuidV7TimestampMillis(composer.ComposerID); ok {
			session.CreatedAt = ts
		}
	}
	if session.CreatedAt == 0 {
		if info, err := os.Stat(filePath); err == nil {
			session.CreatedAt = info.ModTime().UnixMilli()
		}
	}

	// Parse messages
	messages, meta, caps, lints, mfiles, cbs := parseMessages(composer.ComposerID, session.CreatedAt, composer.Conversation)
	session.MessageCount = len(messages)

	// Collect file references
	files := collectFiles(composer)

	return &ParsedSession{
		Session:         session,
		Messages:        messages,
		MessageMetadata: meta,
		Capabilities:    caps,
		Lints:           lints,
		MessageFiles:    mfiles,
		Codeblocks:      cbs,
		Files:           files,
		RawJSON:         string(data),
	}, nil
}

var (
	reComposerID = regexp.MustCompile(`"composerId"\s*:\s*"([^"]+)"`)
	reCreatedAt  = regexp.MustCompile(`"createdAt"\s*:\s*([0-9]{10,})`)
	reAnyPath    = regexp.MustCompile(`(/Users/[^"]+|/home/[^"]+)`)
)

// salvageSession attempts to extract minimal session metadata from malformed JSON.
// It intentionally drops conversation parsing and returns a session-only record.
func salvageSession(filePath string, raw []byte) *ParsedSession {
	m := reComposerID.FindSubmatch(raw)
	if len(m) < 2 {
		return nil
	}
	id := string(m[1])
	if id == "" {
		return nil
	}

	var createdAt int64
	if mm := reCreatedAt.FindSubmatch(raw); len(mm) >= 2 {
		if ts, err := strconv.ParseInt(string(mm[1]), 10, 64); err == nil {
			createdAt = ts
		}
	}
	if createdAt == 0 {
		if ts, ok := uuidV7TimestampMillis(id); ok {
			createdAt = ts
		}
	}
	if createdAt == 0 {
		if info, err := os.Stat(filePath); err == nil {
			createdAt = info.ModTime().UnixMilli()
		}
	}

	// Best-effort project inference from any embedded absolute path
	project := ""
	if pm := reAnyPath.FindSubmatch(raw); len(pm) >= 2 {
		project = inferProjectFromPath(string(pm[1]))
	}

	s := models.Session{
		ID:           id,
		Source:       "cursor",
		Project:      project,
		CreatedAt:    createdAt,
		MessageCount: 0,
	}

	return &ParsedSession{
		Session:         s,
		Messages:        nil,
		MessageMetadata: map[string]string{},
		Capabilities:    nil,
		Lints:           nil,
		MessageFiles:    nil,
		Codeblocks:      nil,
		Files:           nil,
		RawJSON:         string(raw),
	}
}

// preprocessJSON cleans JSON that has embedded newlines in strings
// Note: Some Cursor exports have double-escaped quotes in nested JSON which
// can't be reliably fixed without understanding the nesting structure.
// This preprocessor handles the simpler case of literal control characters.
func preprocessJSON(data []byte) []byte {
	result := make([]byte, 0, len(data))
	inString := false
	i := 0

	for i < len(data) {
		b := data[i]

		// Handle escape sequences inside strings.
		// Cursor exports sometimes contain invalid JSON where a string includes the byte
		// sequence \\\" (two backslashes then quote). In JSON this terminates the string
		// because \\ becomes a literal backslash and the quote is then unescaped.
		// We repair this by inserting one extra backslash to make the quote escaped.
		if inString && b == '\\' && i+1 < len(data) {
			// Repair pattern: \\\" -> \\\"
			if data[i+1] == '\\' && i+2 < len(data) && data[i+2] == '"' {
				result = append(result, '\\', '\\', '\\', '"')
				i += 3
				continue
			}
			// Normal JSON escape sequences we should preserve.
			switch data[i+1] {
			case '"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u':
				// Validate \\uXXXX escapes; Cursor sometimes emits invalid sequences.
				if data[i+1] == 'u' {
					if i+6 > len(data) || !isHex(data[i+2]) || !isHex(data[i+3]) || !isHex(data[i+4]) || !isHex(data[i+5]) {
						// Treat as literal backslash; re-process next byte.
						result = append(result, '\\', '\\')
						i++
						continue
					}
				}
				result = append(result, b, data[i+1])
				i += 2
				continue
			default:
				// Invalid escape (e.g. \s, \%, \', or backslash + newline).
				// Treat the backslash as a literal by escaping it, and re-process the next byte.
				result = append(result, '\\', '\\')
				i++
				continue
			}
		}

		// Toggle string state on quote
		if b == '"' {
			inString = !inString
			result = append(result, b)
			i++
			continue
		}

		// Escape literal control characters inside strings
		if inString {
			switch b {
			case '\n':
				result = append(result, '\\', 'n')
			case '\r':
				result = append(result, '\\', 'r')
			case '\t':
				result = append(result, '\\', 't')
			case '\b':
				result = append(result, '\\', 'b')
			case '\f':
				result = append(result, '\\', 'f')
			default:
				if b < 32 && b != 0 {
					// Escape other control characters as unicode
					result = append(result, fmt.Sprintf("\\u%04x", b)...)
				} else {
					result = append(result, b)
				}
			}
		} else {
			result = append(result, b)
		}
		i++
	}

	return result
}

func isHex(b byte) bool {
	return (b >= '0' && b <= '9') || (b >= 'a' && b <= 'f') || (b >= 'A' && b <= 'F')
}

// scrubKnownBadFields replaces values for certain large/problematic keys with safe defaults.
// Only used as a last resort on files that still fail JSON parsing after preprocessing.
func scrubKnownBadFields(src []byte) []byte {
	// Regex-based scrubs: designed to survive malformed inner JSON by removing whole fields.
	// Only used as last resort when normal parsing fails.
	s := string(src)
	rules := []struct {
		re   *regexp.Regexp
		repl string
	}{
		{regexp.MustCompile(`(?s)("symbolLinks"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("codeBlocks"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("diffHistories"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("newTextDiffWrtV0"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("newTextDiffWrtV1"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("oldTextDiffWrtV0"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		{regexp.MustCompile(`(?s)("oldTextDiffWrtV1"\s*:\s*)\[[\s\S]*?\]`), `$1[]`},
		// Extremely heavy / frequently broken nested objects (we don't need them for session intelligence).
		{regexp.MustCompile(`(?s)("codeBlockData"\s*:\s*)\{[\s\S]*?\}`), `$1{}`},
		{regexp.MustCompile(`(?s)("originalModelLines"\s*:\s*)\{[\s\S]*?\}`), `$1{}`},
		{regexp.MustCompile(`(?s)("inlineDiffNewlyCreatedResources"\s*:\s*)\{[\s\S]*?\}`), `$1{}`},
		{regexp.MustCompile(`(?s)("cachedConversationSummary"\s*:\s*)\{[\s\S]*?\}`), `$1{}`},
	}
	for _, r := range rules {
		s = r.re.ReplaceAllString(s, r.repl)
	}
	return []byte(s)
}

func scrubJSONKey(src []byte, key string, replacement []byte) []byte {
	pat := []byte(`"` + key + `":`)
	idx := 0
	for {
		i := bytes.Index(src[idx:], pat)
		if i == -1 {
			return src
		}
		i += idx
		// Find start of value
		j := i + len(pat)
		for j < len(src) && (src[j] == ' ' || src[j] == '\n' || src[j] == '\r' || src[j] == '\t') {
			j++
		}
		if j >= len(src) {
			return src
		}
		end := scanJSONValueEnd(src, j)
		if end <= j {
			idx = j + 1
			continue
		}
		// Replace value range [j:end)
		var b bytes.Buffer
		b.Grow(len(src) - (end - j) + len(replacement))
		b.Write(src[:j])
		b.Write(replacement)
		b.Write(src[end:])
		src = b.Bytes()
		idx = j + len(replacement)
	}
}

func scanJSONValueEnd(src []byte, start int) int {
	if start >= len(src) {
		return start
	}
	switch src[start] {
	case '{':
		return scanBalanced(src, start, '{', '}')
	case '[':
		return scanBalanced(src, start, '[', ']')
	case '"':
		return scanString(src, start)
	default:
		// literal: true/false/null/number
		i := start
		for i < len(src) {
			switch src[i] {
			case ',', '}', ']':
				return i
			default:
				i++
			}
		}
		return i
	}
}

func scanString(src []byte, start int) int {
	i := start + 1
	for i < len(src) {
		if src[i] == '\\' {
			i += 2
			continue
		}
		if src[i] == '"' {
			return i + 1
		}
		i++
	}
	return i
}

func scanBalanced(src []byte, start int, open, close byte) int {
	depth := 0
	inString := false
	escaped := false
	for i := start; i < len(src); i++ {
		c := src[i]
		if inString {
			if escaped {
				escaped = false
				continue
			}
			if c == '\\' {
				escaped = true
				continue
			}
			if c == '"' {
				inString = false
			}
			continue
		}
		if c == '"' {
			inString = true
			continue
		}
		if c == open {
			depth++
		} else if c == close {
			depth--
			if depth == 0 {
				return i + 1
			}
		}
	}
	return len(src)
}

// extractProject tries to infer the project name from file paths
func extractProject(composer CursorComposerData) string {
	// Collect all file paths
	var paths []string

	// From context file selections
	for _, fs := range composer.Context.FileSelections {
		if fs.URI.FsPath != "" {
			paths = append(paths, fs.URI.FsPath)
		}
	}

	// From conversation items (relevantFiles)
	for _, item := range composer.Conversation {
		if files, ok := item["relevantFiles"].([]interface{}); ok {
			for _, f := range files {
				if path, ok := f.(string); ok {
					paths = append(paths, path)
				}
			}
		}
	}

	if len(paths) == 0 {
		return ""
	}

	// Find common project directory
	// Look for patterns like /Users/tyler/Desktop/projects/ProjectName/ or /path/to/project/
	projectCounts := make(map[string]int)

	for _, p := range paths {
		project := inferProjectFromPath(p)
		if project != "" {
			projectCounts[project]++
		}
	}

	// Return most common project
	var bestProject string
	var bestCount int
	for project, count := range projectCounts {
		if count > bestCount {
			bestProject = project
			bestCount = count
		}
	}

	return bestProject
}

// inferProjectFromPath extracts a project name from a file path
func inferProjectFromPath(path string) string {
	// Common project directory patterns
	patterns := []string{
		`/Users/[^/]+/Desktop/projects/([^/]+)`,
		`/Users/[^/]+/Projects/([^/]+)`,
		`/Users/[^/]+/([^/]+)/`, // fallback: first directory under home
		`/home/[^/]+/projects/([^/]+)`,
		`/home/[^/]+/([^/]+)/`,
	}

	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		if matches := re.FindStringSubmatch(path); len(matches) > 1 {
			return matches[1]
		}
	}

	// Fallback: get the first meaningful directory
	parts := strings.Split(path, "/")
	for i, part := range parts {
		if part == "src" || part == "lib" || part == "app" || part == "internal" {
			if i > 0 {
				return parts[i-1]
			}
		}
	}

	return ""
}

// parseMessages extracts messages from conversation items
func parseMessages(sessionID string, sessionCreatedAt int64, conversation []map[string]interface{}) ([]models.Message, map[string]string, []MessageCapability, []MessageLint, []MessageFileRef, []MessageCodeblock) {
	var messages []models.Message
	meta := make(map[string]string)
	var caps []MessageCapability
	var lints []MessageLint
	var files []MessageFileRef
	var codeblocks []MessageCodeblock

	for i, item := range conversation {
		msg := models.Message{
			SessionID: sessionID,
			Sequence:  i,
		}

		// Get bubble ID
		if bubbleID, ok := item["bubbleId"].(string); ok {
			msg.ID = bubbleID
		} else {
			msg.ID = fmt.Sprintf("%s-%d", sessionID, i)
		}

		// Determine role from type
		// Type 1 = user, Type 2 = assistant (based on observed patterns)
		if typeVal, ok := item["type"].(float64); ok {
			switch int(typeVal) {
			case 1:
				msg.Role = "user"
			case 2:
				msg.Role = "assistant"
			default:
				msg.Role = "unknown"
			}
		}

		// Timestamp inference
		// 1) Prefer UUIDv7 timestamps from bubbleId (if bubbleId is v7)
		if msg.ID != "" {
			if ts, ok := uuidV7TimestampMillis(msg.ID); ok {
				msg.Timestamp = ts
			}
		}
		// 2) Fallback: use session created_at if we have it
		if msg.Timestamp == 0 && sessionCreatedAt > 0 {
			msg.Timestamp = sessionCreatedAt
		}

		// Extract text content
		msg.Content = extractMessageContent(item)

		// Always persist the bubble, even if content is empty.
		// Cursor bubbles can carry important metadata (tools, files, lints) even when
		// the rendered text is empty. Persisting all bubbles also prevents FK errors
		// for per-message tables keyed by message_id.
		messages = append(messages, msg)

		// Capture raw-ish metadata for later analysis.
		// Keep it intentionally lossy and JSON-friendly.
		m := map[string]interface{}{}
		if v, ok := item["type"]; ok {
			m["type"] = v
		}
		if v, ok := item["relevantFiles"]; ok {
			m["relevantFiles"] = v
		}
		if v, ok := item["capabilitiesRan"]; ok {
			m["capabilitiesRan"] = v
		}
		if v, ok := item["capabilityStatuses"]; ok {
			m["capabilityStatuses"] = v
		}
		if v, ok := item["multiFileLinterErrors"]; ok {
			m["multiFileLinterErrors"] = v
		}
		if v, ok := item["diffHistories"]; ok {
			m["diffHistories"] = v
		}
		if v, ok := item["recentLocationsHistory"]; ok {
			m["recentLocationsHistory"] = v
		}
		if v, ok := item["suggestedCodeBlocks"]; ok {
			m["suggestedCodeBlocks"] = v
		}
		if v, ok := item["codeBlocks"]; ok {
			m["codeBlocks"] = v
		}
		if v, ok := item["context"]; ok {
			m["context"] = v
		}
		if len(m) > 0 && msg.ID != "" {
			if b, err := json.Marshal(m); err == nil {
				meta[msg.ID] = string(b)
			}
		}

		// Flatten capabilitiesRan into message_capabilities
		if msg.ID != "" {
			if cr, ok := item["capabilitiesRan"].(map[string]interface{}); ok {
				for phase, raw := range cr {
					arr, ok := raw.([]interface{})
					if !ok {
						continue
					}
					for _, v := range arr {
						switch n := v.(type) {
						case float64:
							caps = append(caps, MessageCapability{
								MessageID:  msg.ID,
								SessionID:  sessionID,
								Phase:      phase,
								Capability: int(n),
							})
						}
					}
				}
			}
		}

		// Flatten multiFileLinterErrors into message_lints
		if msg.ID != "" {
			if mfe, ok := item["multiFileLinterErrors"].([]interface{}); ok {
				for _, fileEntry := range mfe {
					fm, ok := fileEntry.(map[string]interface{})
					if !ok {
						continue
					}
					filePath, _ := fm["relativeWorkspacePath"].(string)
					errs, ok := fm["errors"].([]interface{})
					if !ok {
						continue
					}
					for _, e := range errs {
						em, ok := e.(map[string]interface{})
						if !ok {
							continue
						}
						msgText, _ := em["message"].(string)
						src, _ := em["source"].(string)

						var sl, sc, el, ec int
						if r, ok := em["range"].(map[string]interface{}); ok {
							if sp, ok := r["startPosition"].(map[string]interface{}); ok {
								sl = int(getFloat(sp["line"]))
								sc = int(getFloat(sp["column"]))
							}
							if ep, ok := r["endPosition"].(map[string]interface{}); ok {
								el = int(getFloat(ep["line"]))
								ec = int(getFloat(ep["column"]))
							}
						}

						lints = append(lints, MessageLint{
							MessageID: msg.ID,
							SessionID: sessionID,
							FilePath:  filePath,
							Message:   msgText,
							Source:    src,
							StartLine: sl,
							StartCol:  sc,
							EndLine:   el,
							EndCol:    ec,
						})
					}
				}
			}
		}

		// Per-message file references
		if msg.ID != "" {
			if rf, ok := item["relevantFiles"].([]interface{}); ok {
				for _, v := range rf {
					if p, ok := v.(string); ok && p != "" {
						files = append(files, MessageFileRef{
							MessageID: msg.ID, SessionID: sessionID, Kind: "relevant", FilePath: p,
						})
					}
				}
			}
			if rh, ok := item["recentLocationsHistory"].([]interface{}); ok {
				for _, v := range rh {
					mm, ok := v.(map[string]interface{})
					if !ok {
						continue
					}
					p, _ := mm["relativeWorkspacePath"].(string)
					if p == "" {
						continue
					}
					ln := int(getFloat(mm["lineNumber"]))
					files = append(files, MessageFileRef{
						MessageID: msg.ID, SessionID: sessionID, Kind: "recent_location", FilePath: p, LineNumber: ln,
					})
				}
			}
			// Context file selections (often absolute fsPath)
			if ctx, ok := item["context"].(map[string]interface{}); ok {
				if fs, ok := ctx["fileSelections"].([]interface{}); ok {
					for _, v := range fs {
						fm, ok := v.(map[string]interface{})
						if !ok {
							continue
						}
						uri, ok := fm["uri"].(map[string]interface{})
						if !ok {
							continue
						}
						fsPath, _ := uri["fsPath"].(string)
						if fsPath == "" {
							continue
						}
						files = append(files, MessageFileRef{
							MessageID: msg.ID, SessionID: sessionID, Kind: "context_file_selection", FilePath: fsPath,
						})
					}
				}
			}
		}

		// Suggested code blocks
		if msg.ID != "" {
			if scb, ok := item["suggestedCodeBlocks"].([]interface{}); ok {
				for idx, v := range scb {
					if b, err := json.Marshal(v); err == nil {
						codeblocks = append(codeblocks, MessageCodeblock{
							MessageID: msg.ID, SessionID: sessionID, Idx: idx, RawJSON: string(b),
						})
					}
				}
			}
			if cb, ok := item["codeBlocks"].([]interface{}); ok {
				baseIdx := len(codeblocks)
				for idx, v := range cb {
					if b, err := json.Marshal(v); err == nil {
						codeblocks = append(codeblocks, MessageCodeblock{
							MessageID: msg.ID, SessionID: sessionID, Idx: baseIdx + idx, RawJSON: string(b),
						})
					}
				}
			}
		}
	}

	return messages, meta, caps, lints, files, codeblocks
}

func getFloat(v interface{}) float64 {
	if v == nil {
		return 0
	}
	if f, ok := v.(float64); ok {
		return f
	}
	return 0
}

// extractMessageContent extracts the text content from a conversation item
func extractMessageContent(item map[string]interface{}) string {
	// Try direct text field first
	if text, ok := item["text"].(string); ok && text != "" {
		return text
	}

	// Try to parse richText (Lexical editor format)
	if richText, ok := item["richText"].(string); ok && richText != "" {
		return extractFromRichText(richText)
	}

	// For assistant messages, try modelResponse or other fields
	if response, ok := item["modelResponse"].(map[string]interface{}); ok {
		if text, ok := response["text"].(string); ok {
			return text
		}
	}

	// Try message field
	if msg, ok := item["message"].(string); ok {
		return msg
	}

	return ""
}

// extractFromRichText parses Lexical JSON format to extract plain text
func extractFromRichText(richText string) string {
	var doc map[string]interface{}
	if err := json.Unmarshal([]byte(richText), &doc); err != nil {
		return ""
	}

	var texts []string
	extractTextsFromNode(doc, &texts)
	return strings.Join(texts, "\n")
}

// extractTextsFromNode recursively extracts text from Lexical nodes
func extractTextsFromNode(node map[string]interface{}, texts *[]string) {
	// Handle text nodes
	if text, ok := node["text"].(string); ok {
		*texts = append(*texts, text)
	}

	// Handle children
	if children, ok := node["children"].([]interface{}); ok {
		for _, child := range children {
			if childMap, ok := child.(map[string]interface{}); ok {
				extractTextsFromNode(childMap, texts)
			}
		}
	}

	// Handle root node
	if root, ok := node["root"].(map[string]interface{}); ok {
		extractTextsFromNode(root, texts)
	}
}

// collectFiles gathers all file references from a session
func collectFiles(composer CursorComposerData) []string {
	seen := make(map[string]bool)
	var files []string

	// From context
	for _, fs := range composer.Context.FileSelections {
		if fs.URI.FsPath != "" && !seen[fs.URI.FsPath] {
			seen[fs.URI.FsPath] = true
			files = append(files, fs.URI.FsPath)
		}
	}

	// From conversation
	for _, item := range composer.Conversation {
		if relevantFiles, ok := item["relevantFiles"].([]interface{}); ok {
			for _, f := range relevantFiles {
				if path, ok := f.(string); ok && !seen[path] {
					seen[path] = true
					files = append(files, path)
				}
			}
		}
	}

	return files
}

// DefaultCursorPath returns the default path for exported Cursor sessions
func DefaultCursorPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "nexus", "home", "sessions", "composer")
}

// DefaultCursorDBPath returns the path to Cursor's internal SQLite database
func DefaultCursorDBPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "Library", "Application Support", "Cursor", "User", "globalStorage", "state.vscdb")
}

// uuidV7TimestampMillis extracts Unix epoch milliseconds from a UUIDv7 string.
// Spec: first 48 bits are unix_ms; version nibble is 7 (e.g. xxxxxxxx-xxxx-7xxx-....).
func uuidV7TimestampMillis(id string) (int64, bool) {
	parts := strings.Split(id, "-")
	if len(parts) != 5 {
		return 0, false
	}
	if len(parts[0]) != 8 || len(parts[1]) != 4 || len(parts[2]) != 4 {
		return 0, false
	}
	if len(parts[3]) != 4 || len(parts[4]) != 12 {
		return 0, false
	}
	// Version nibble is the first char of the 3rd group.
	if parts[2][0] != '7' {
		return 0, false
	}

	hexTS := parts[0] + parts[1] // 12 hex chars => 48-bit unix ms
	v, err := strconv.ParseUint(hexTS, 16, 64)
	if err != nil {
		return 0, false
	}
	return int64(v), true
}
