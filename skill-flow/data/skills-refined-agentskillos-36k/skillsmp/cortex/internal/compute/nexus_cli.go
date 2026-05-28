package compute

import (
	"context"
	"database/sql"
	"encoding/json"
	"path/filepath"
	"strings"
)

type terminalInvocation struct {
	EventID        string `json:"event_id"`
	Position       int    `json:"position"`
	Timestamp      int64  `json:"timestamp"`
	Command        string `json:"command"`
	RawCommand     string `json:"raw_command,omitempty"`
	Binary         string `json:"binary"`
	Subcommand     string `json:"subcommand,omitempty"`
	Args           string `json:"args,omitempty"`
	SegmentIndex   int    `json:"segment_index"`
	InvocationKind string `json:"invocation_kind,omitempty"`
}

func (e *Engine) buildNexusCLIOutput(ctx context.Context, episodeID string) (string, error) {
	return e.buildInvocationOutput(ctx, episodeID, func(inv terminalInvocation) bool {
		return inv.Binary == "nexus" || inv.Binary == "nexus-cloud"
	})
}

func (e *Engine) buildTerminalInvocationOutput(ctx context.Context, episodeID string) (string, error) {
	return e.buildInvocationOutput(ctx, episodeID, nil)
}

func (e *Engine) buildInvocationOutput(ctx context.Context, episodeID string, filter func(terminalInvocation) bool) (string, error) {
	rows, err := e.db.QueryContext(ctx, `
		SELECT
			ee.position,
			e.id,
			e.timestamp,
			e.content,
			e.source_adapter
		FROM episode_events ee
		JOIN events e ON ee.event_id = e.id
		WHERE ee.episode_id = ?
		ORDER BY ee.position
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var invocations []terminalInvocation
	var commands []string
	var subcommands []string
	var binaries []string

	for rows.Next() {
		var (
			position      int
			eventID       string
			timestamp     int64
			content       sql.NullString
			sourceAdapter string
		)
		if err := rows.Scan(&position, &eventID, &timestamp, &content, &sourceAdapter); err != nil {
			return "", err
		}
		if !content.Valid {
			continue
		}
		rawCommand := strings.TrimSpace(content.String)
		if rawCommand == "" {
			continue
		}
		if !isToolAdapter(sourceAdapter) {
			continue
		}

		extracted := extractTerminalInvocationsFromCommand(rawCommand)
		for _, inv := range extracted {
			if filter != nil && !filter(inv) {
				continue
			}
			inv.EventID = eventID
			inv.Position = position
			inv.Timestamp = timestamp
			inv.RawCommand = rawCommand

			invocations = append(invocations, inv)
			commands = append(commands, inv.Command)
			if inv.Subcommand != "" {
				subcommands = append(subcommands, inv.Subcommand)
			}
			if inv.Binary != "" {
				binaries = append(binaries, inv.Binary)
			}
		}
	}
	if err := rows.Err(); err != nil {
		return "", err
	}

	invStrings := make([]string, 0, len(invocations))
	for _, inv := range invocations {
		b, err := json.Marshal(inv)
		if err != nil {
			return "", err
		}
		invStrings = append(invStrings, string(b))
	}

	output := map[string]any{
		"invocations": invStrings,
		"commands":    commands,
		"subcommands": subcommands,
		"binaries":    binaries,
	}
	outBytes, err := json.Marshal(output)
	if err != nil {
		return "", err
	}
	return string(outBytes), nil
}

func isToolAdapter(adapter string) bool {
	return strings.HasSuffix(adapter, "_tool")
}

func extractTerminalInvocationsFromCommand(command string) []terminalInvocation {
	segments := splitShellSegments(command)
	var out []terminalInvocation
	for idx, segment := range segments {
		segment = strings.TrimSpace(segment)
		if segment == "" {
			continue
		}
		tokens := splitShellTokens(segment)
		tokens = stripShellWrappers(tokens)
		if len(tokens) == 0 {
			continue
		}

		inv, ok := parseTerminalFromTokens(tokens)
		if !ok {
			continue
		}
		inv.Command = segment
		inv.SegmentIndex = idx
		out = append(out, inv)
	}
	return out
}

func splitShellSegments(command string) []string {
	var segments []string
	var sb strings.Builder
	inSingle := false
	inDouble := false

	flush := func() {
		seg := strings.TrimSpace(sb.String())
		if seg != "" {
			segments = append(segments, seg)
		}
		sb.Reset()
	}

	for i := 0; i < len(command); i++ {
		ch := command[i]
		if ch == '\'' && !inDouble {
			inSingle = !inSingle
			sb.WriteByte(ch)
			continue
		}
		if ch == '"' && !inSingle {
			inDouble = !inDouble
			sb.WriteByte(ch)
			continue
		}
		if !inSingle && !inDouble {
			if ch == ';' {
				flush()
				continue
			}
			if ch == '|' || ch == '&' {
				// Avoid splitting on redirection operators like 2>&1 or &>file.
				prev := byte(0)
				next := byte(0)
				if i > 0 {
					prev = command[i-1]
				}
				if i+1 < len(command) {
					next = command[i+1]
				}
				if ch == '&' && (prev == '>' || next == '>') {
					sb.WriteByte(ch)
					continue
				}

				// Treat pipes and background ops as segment boundaries.
				// Skip double operators like || and &&.
				if next == ch {
					i++
				}
				flush()
				continue
			}
		}
		sb.WriteByte(ch)
	}
	flush()
	return segments
}

func splitShellTokens(segment string) []string {
	var tokens []string
	var sb strings.Builder
	inSingle := false
	inDouble := false
	escaped := false

	flush := func() {
		if sb.Len() > 0 {
			tokens = append(tokens, sb.String())
			sb.Reset()
		}
	}

	for i := 0; i < len(segment); i++ {
		ch := segment[i]
		if escaped {
			sb.WriteByte(ch)
			escaped = false
			continue
		}
		if ch == '\\' && !inSingle {
			escaped = true
			continue
		}
		if ch == '\'' && !inDouble {
			inSingle = !inSingle
			continue
		}
		if ch == '"' && !inSingle {
			inDouble = !inDouble
			continue
		}
		if !inSingle && !inDouble && (ch == ' ' || ch == '\t' || ch == '\n') {
			flush()
			continue
		}
		sb.WriteByte(ch)
	}
	flush()
	return tokens
}

func stripShellWrappers(tokens []string) []string {
	if len(tokens) == 0 {
		return tokens
	}
	first := strings.ToLower(tokens[0])
	if first == "sudo" {
		i := 1
		for i < len(tokens) && strings.HasPrefix(tokens[i], "-") {
			i++
		}
		tokens = tokens[i:]
	}
	if len(tokens) == 0 {
		return tokens
	}
	first = strings.ToLower(tokens[0])
	if first == "env" {
		i := 1
		for i < len(tokens) && strings.Contains(tokens[i], "=") {
			i++
		}
		tokens = tokens[i:]
	}
	if len(tokens) == 0 {
		return tokens
	}
	first = strings.ToLower(tokens[0])
	if first == "command" {
		tokens = tokens[1:]
	}
	for len(tokens) > 0 && isEnvAssignment(tokens[0]) {
		tokens = tokens[1:]
	}
	return tokens
}

func parseTerminalFromTokens(tokens []string) (terminalInvocation, bool) {
	if len(tokens) == 0 {
		return terminalInvocation{}, false
	}

	if inv, ok := parseCargoRunCLI(tokens); ok {
		return inv, true
	}

	if wrapper, bin, rest, ok := unwrapWrapperBinary(tokens); ok && bin != "" {
		inv := buildInvocation(bin, rest)
		inv.InvocationKind = "wrapper:" + wrapper
		return inv, true
	}

	if bin := normalizeBinary(tokens[0]); bin != "" {
		inv := buildInvocation(bin, tokens[1:])
		inv.InvocationKind = "direct"
		return inv, true
	}

	return terminalInvocation{}, false
}

func normalizeBinary(token string) string {
	base := strings.ToLower(filepath.Base(token))
	if base == "" || strings.HasPrefix(base, "-") {
		return ""
	}
	return base
}

func isEnvAssignment(token string) bool {
	if !strings.Contains(token, "=") {
		return false
	}
	parts := strings.SplitN(token, "=", 2)
	key := parts[0]
	if key == "" {
		return false
	}
	for i := 0; i < len(key); i++ {
		ch := key[i]
		if i == 0 {
			if !((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || ch == '_') {
				return false
			}
		} else {
			if !((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9') || ch == '_') {
				return false
			}
		}
	}
	return true
}

func unwrapWrapperBinary(tokens []string) (string, string, []string, bool) {
	if len(tokens) == 0 {
		return "", "", nil, false
	}
	wrapper := normalizeBinary(tokens[0])
	if wrapper == "" {
		return "", "", nil, false
	}

	switch wrapper {
	case "npx":
		idx := 1
		for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
			idx++
		}
		if idx < len(tokens) {
			return wrapper, normalizeBinary(tokens[idx]), tokens[idx+1:], true
		}
	case "pnpm":
		idx := 1
		for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
			idx++
		}
		if idx < len(tokens) && (tokens[idx] == "exec" || tokens[idx] == "dlx") {
			idx++
			for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
				idx++
			}
			if idx < len(tokens) {
				return wrapper, normalizeBinary(tokens[idx]), tokens[idx+1:], true
			}
		}
	case "npm":
		idx := 1
		for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
			idx++
		}
		if idx < len(tokens) && tokens[idx] == "exec" {
			idx++
			for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
				idx++
			}
			if idx < len(tokens) {
				return wrapper, normalizeBinary(tokens[idx]), tokens[idx+1:], true
			}
		}
	case "yarn":
		idx := 1
		for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
			idx++
		}
		if idx < len(tokens) && tokens[idx] == "dlx" {
			idx++
			for idx < len(tokens) && strings.HasPrefix(tokens[idx], "-") {
				idx++
			}
			if idx < len(tokens) {
				return wrapper, normalizeBinary(tokens[idx]), tokens[idx+1:], true
			}
		}
	}

	return "", "", nil, false
}

func buildInvocation(binary string, rest []string) terminalInvocation {
	inv := terminalInvocation{Binary: binary}
	if len(rest) > 0 {
		inv.Subcommand = rest[0]
		if len(rest) > 1 {
			inv.Args = strings.Join(rest[1:], " ")
		}
	}
	return inv
}

func parseCargoRunCLI(tokens []string) (terminalInvocation, bool) {
	if len(tokens) < 3 {
		return terminalInvocation{}, false
	}
	if normalizeBinary(tokens[0]) != "cargo" || tokens[1] != "run" {
		return terminalInvocation{}, false
	}

	pkg := ""
	argsStart := -1
	for i := 2; i < len(tokens); i++ {
		tok := tokens[i]
		switch tok {
		case "-p", "--package":
			if i+1 < len(tokens) {
				pkg = tokens[i+1]
				i++
				continue
			}
		case "--":
			argsStart = i + 1
			i = len(tokens)
		}
	}
	if pkg != "cli" || argsStart == -1 {
		return terminalInvocation{}, false
	}

	inv := terminalInvocation{Binary: "nexus-cloud"}
	if argsStart < len(tokens) {
		inv.Subcommand = tokens[argsStart]
		if argsStart+1 < len(tokens) {
			inv.Args = strings.Join(tokens[argsStart+1:], " ")
		}
	}
	inv.InvocationKind = "cargo_run"
	return inv, true
}
