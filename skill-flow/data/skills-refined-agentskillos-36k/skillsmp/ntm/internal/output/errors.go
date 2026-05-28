package output

import (
	"fmt"
	"os"
	"strings"

	"github.com/charmbracelet/lipgloss"
	"golang.org/x/term"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// CLIError represents a structured CLI error with remediation hints.
type CLIError struct {
	Message string // What failed
	Cause   string // Why it failed (optional)
	Hint    string // Fastest command/action to fix it (optional)
	Code    string // Error code for programmatic handling (optional)
}

// Error implements the error interface.
func (e *CLIError) Error() string {
	return e.Message
}

// NewCLIError creates a new CLI error with just a message.
func NewCLIError(msg string) *CLIError {
	return &CLIError{Message: msg}
}

// WithCause adds a cause to the error.
func (e *CLIError) WithCause(cause string) *CLIError {
	e.Cause = cause
	return e
}

// WithHint adds a remediation hint to the error.
func (e *CLIError) WithHint(hint string) *CLIError {
	e.Hint = hint
	return e
}

// WithCode adds an error code to the error.
func (e *CLIError) WithCode(code string) *CLIError {
	e.Code = code
	return e
}

// isStderrTerminal checks if stderr is a terminal (for color output).
func isStderrTerminal() bool {
	return term.IsTerminal(int(os.Stderr.Fd()))
}

// FormatCLIError formats a CLIError for terminal output with colors.
// Returns plain text if stderr is not a terminal or NO_COLOR is set.
func FormatCLIError(e *CLIError) string {
	useColor := isStderrTerminal() && os.Getenv("NO_COLOR") == ""

	var sb strings.Builder

	if useColor {
		t := theme.Current()
		errorStyle := lipgloss.NewStyle().Foreground(t.Error).Bold(true)
		causeStyle := lipgloss.NewStyle().Foreground(t.Subtext)
		hintStyle := lipgloss.NewStyle().Foreground(t.Info)
		codeStyle := lipgloss.NewStyle().Foreground(t.Overlay)

		// Error message (red, bold)
		sb.WriteString(errorStyle.Render("Error: "))
		sb.WriteString(e.Message)

		// Error code if present
		if e.Code != "" {
			sb.WriteString(" ")
			sb.WriteString(codeStyle.Render("[" + e.Code + "]"))
		}
		sb.WriteString("\n")

		// Cause if present
		if e.Cause != "" {
			sb.WriteString(causeStyle.Render("  Cause: "))
			sb.WriteString(e.Cause)
			sb.WriteString("\n")
		}

		// Hint if present
		if e.Hint != "" {
			sb.WriteString(hintStyle.Render("  Hint: "))
			sb.WriteString(e.Hint)
			sb.WriteString("\n")
		}
	} else {
		// Plain text output (no colors)
		sb.WriteString("Error: ")
		sb.WriteString(e.Message)
		if e.Code != "" {
			sb.WriteString(" [")
			sb.WriteString(e.Code)
			sb.WriteString("]")
		}
		sb.WriteString("\n")

		if e.Cause != "" {
			sb.WriteString("  Cause: ")
			sb.WriteString(e.Cause)
			sb.WriteString("\n")
		}

		if e.Hint != "" {
			sb.WriteString("  Hint: ")
			sb.WriteString(e.Hint)
			sb.WriteString("\n")
		}
	}

	return sb.String()
}

// PrintCLIError prints a CLIError to stderr with formatting.
func PrintCLIError(e *CLIError) {
	fmt.Fprint(os.Stderr, FormatCLIError(e))
}

// PrintCLIErrorOrJSON prints a CLIError to stderr (text) or stdout (JSON).
func PrintCLIErrorOrJSON(e *CLIError, jsonMode bool) error {
	if jsonMode {
		resp := ErrorResponse{
			Error:   e.Message,
			Code:    e.Code,
			Details: e.Cause,
			Hint:    e.Hint,
		}
		return WriteJSON(os.Stdout, resp, true)
	}
	PrintCLIError(e)
	return e
}

// Error outputs an error in the appropriate format
func (f *Formatter) Error(err error) error {
	if f.IsJSON() {
		return f.JSON(NewError(err.Error()))
	}
	return err
}

// ErrorMsg outputs an error message in the appropriate format
func (f *Formatter) ErrorMsg(msg string) error {
	if f.IsJSON() {
		return f.JSON(NewError(msg))
	}
	return fmt.Errorf("%s", msg)
}

// ErrorWithCode outputs an error with a code in the appropriate format
func (f *Formatter) ErrorWithCode(code, msg string) error {
	if f.IsJSON() {
		return f.JSON(NewErrorWithCode(code, msg))
	}
	return fmt.Errorf("[%s] %s", code, msg)
}

// ErrorWithHint outputs an error with a hint in the appropriate format
func (f *Formatter) ErrorWithHint(msg, hint string) error {
	if f.IsJSON() {
		return f.JSON(NewErrorWithHint(msg, hint))
	}
	cliErr := NewCLIError(msg).WithHint(hint)
	PrintCLIError(cliErr)
	return cliErr
}

// PrintError writes an error to stderr and returns an error for JSON mode
func PrintError(err error, jsonMode bool) error {
	if jsonMode {
		return WriteJSON(os.Stdout, NewError(err.Error()), true)
	}
	fmt.Fprintf(os.Stderr, "Error: %v\n", err)
	return err
}

// PrintErrorWithHint writes an error with a hint to stderr
func PrintErrorWithHint(msg, hint string, jsonMode bool) error {
	cliErr := NewCLIError(msg).WithHint(hint)
	return PrintCLIErrorOrJSON(cliErr, jsonMode)
}

// PrintErrorFull writes a full error with cause and hint
func PrintErrorFull(msg, cause, hint string, jsonMode bool) error {
	cliErr := NewCLIError(msg).WithCause(cause).WithHint(hint)
	return PrintCLIErrorOrJSON(cliErr, jsonMode)
}

// Fatal prints an error and exits
func Fatal(err error, jsonMode bool) {
	if jsonMode {
		WriteJSON(os.Stdout, NewError(err.Error()), true)
	} else {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
	}
	os.Exit(1)
}

// FatalWithHint prints an error with a hint and exits
func FatalWithHint(msg, hint string, jsonMode bool) {
	cliErr := NewCLIError(msg).WithHint(hint)
	PrintCLIErrorOrJSON(cliErr, jsonMode)
	os.Exit(1)
}

// FatalMsg prints an error message and exits
func FatalMsg(msg string, jsonMode bool) {
	Fatal(fmt.Errorf("%s", msg), jsonMode)
}

// Common error hints for frequent scenarios
var (
	// Session errors
	HintSessionNotFound  = "Run 'ntm list' to see available sessions, or 'ntm spawn <name>' to create one"
	HintSessionExists    = "Use a different name, or 'ntm kill <name>' to remove the existing session"
	HintNoSessions       = "Run 'ntm spawn <name>' to create a new session"
	HintSessionInference = "Specify a session name explicitly, e.g., 'ntm status <session>'"

	// Tmux errors
	HintTmuxNotInstalled = "Install tmux: brew install tmux (macOS) or apt install tmux (Linux)"
	HintTmuxNotRunning   = "Start tmux server with 'tmux new-session -d' or run ntm spawn"
	HintNotInTmux        = "Run this command from within a tmux session, or specify --session"

	// Config errors
	HintConfigNotFound = "Run 'ntm config init' to create a default configuration"
	HintConfigInvalid  = "Check config syntax with 'ntm config show' or edit ~/.config/ntm/config.toml"

	// Agent errors
	HintAgentNotInstalled = "Install the agent CLI tool first (claude, codex-cli, or gemini-cli)"
	HintAgentRateLimit    = "Wait a few minutes or switch to a different API key/account"

	// Pane errors
	HintPaneNotFound  = "Run 'ntm status <session>' to see available panes"
	HintNoPanes       = "Add agents with 'ntm add <session> --cc=1' or '--cod=1'"
	HintPaneIndexHelp = "Pane indices start at 0; use 'ntm status' to see valid indices"

	// Permission errors
	HintPermissionDenied = "Check file permissions or run with appropriate privileges"
)

// SessionNotFoundError creates a session not found error with hint
func SessionNotFoundError(session string) *CLIError {
	return NewCLIError(fmt.Sprintf("session '%s' not found", session)).
		WithCode("SESSION_NOT_FOUND").
		WithHint(HintSessionNotFound)
}

// SessionExistsError creates a session exists error with hint
func SessionExistsError(session string) *CLIError {
	return NewCLIError(fmt.Sprintf("session '%s' already exists", session)).
		WithCode("SESSION_EXISTS").
		WithHint(HintSessionExists)
}

// TmuxNotInstalledError creates a tmux not installed error with hint
func TmuxNotInstalledError() *CLIError {
	return NewCLIError("tmux is not installed").
		WithCode("TMUX_NOT_INSTALLED").
		WithHint(HintTmuxNotInstalled)
}

// PaneNotFoundError creates a pane not found error with hint
func PaneNotFoundError(session string, index int) *CLIError {
	return NewCLIError(fmt.Sprintf("pane %d not found in session '%s'", index, session)).
		WithCode("PANE_NOT_FOUND").
		WithHint(HintPaneNotFound)
}

// NoSessionsError creates a no sessions found error with hint
func NoSessionsError() *CLIError {
	return NewCLIError("no tmux sessions found").
		WithCode("NO_SESSIONS").
		WithHint(HintNoSessions)
}

// AgentTypeError creates an unknown agent type error with hint
func AgentTypeError(agentType string) *CLIError {
	return NewCLIError(fmt.Sprintf("unknown agent type: %s", agentType)).
		WithCode("UNKNOWN_AGENT_TYPE").
		WithHint("Valid types: claude (cc), codex (cod), gemini (gmi)")
}

// PersonaNotFoundError creates a persona not found error with hint
func PersonaNotFoundError(name string) *CLIError {
	return NewCLIError(fmt.Sprintf("persona '%s' not found", name)).
		WithCode("PERSONA_NOT_FOUND").
		WithHint("Run 'ntm personas list' to see available personas")
}

// CheckpointNotFoundError creates a checkpoint not found error with hint
func CheckpointNotFoundError(id, session string) *CLIError {
	return NewCLIError(fmt.Sprintf("checkpoint '%s' not found in session '%s'", id, session)).
		WithCode("CHECKPOINT_NOT_FOUND").
		WithHint("Run 'ntm checkpoint list <session>' to see available checkpoints")
}

// ConfigLoadError creates a config load error with hint
func ConfigLoadError(cause string) *CLIError {
	return NewCLIError("failed to load configuration").
		WithCode("CONFIG_ERROR").
		WithCause(cause).
		WithHint(HintConfigInvalid)
}

// MultipleSessions creates an ambiguous session error with hint
func MultipleSessions(sessions []string) *CLIError {
	return NewCLIError("multiple sessions found, please specify one").
		WithCode("MULTIPLE_SESSIONS").
		WithCause(fmt.Sprintf("found sessions: %s", strings.Join(sessions, ", "))).
		WithHint(HintSessionInference)
}

// InvalidFlagError creates an invalid flag value error with hint
func InvalidFlagError(flag, value, expected string) *CLIError {
	return NewCLIError(fmt.Sprintf("invalid value for --%s: %s", flag, value)).
		WithCode("INVALID_FLAG").
		WithHint(fmt.Sprintf("Expected: %s", expected))
}
