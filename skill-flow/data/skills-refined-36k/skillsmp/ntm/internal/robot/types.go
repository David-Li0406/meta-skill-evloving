// Package robot provides machine-readable output for AI agents.
// types.go defines the standardized response structures for robot commands.
//
// # Robot Output Envelope Specification
//
// All robot command responses MUST follow the envelope specification to ensure
// consistent, parseable output for AI agents. This spec is authoritative.
//
// ## Required Fields (All Responses)
//
// Every robot response MUST include:
//   - success (bool): Whether the operation completed successfully. Check this FIRST.
//   - timestamp (string): RFC3339 UTC timestamp when response was generated.
//
// ## Error Response Fields
//
// When success=false, responses SHOULD include:
//   - error (string): Human-readable error message.
//   - error_code (string): Machine-readable code for programmatic handling.
//     See ErrCode* constants for defined values.
//   - hint (string, optional): Actionable guidance for resolving the error.
//
// ## Array Fields
//
// Critical arrays MUST always be present, even when empty:
//   - Use `[]` not `null` for empty arrays that agents will iterate.
//   - This allows safe iteration without null checks.
//   - Use `omitempty` only for truly optional arrays (like _agent_hints).
//
// ## Creating New Output Types
//
// New robot commands MUST:
//  1. Embed RobotResponse as the first field (anonymous embed).
//  2. Use NewRobotResponse(true) for success responses.
//  3. Use NewErrorResponse() or RobotError() for errors.
//  4. Initialize all critical arrays to empty slices, not nil.
//  5. Use FormatTimestamp() for any additional timestamp fields.
//
// Example:
//
//	type MyOutput struct {
//	    RobotResponse           // Embed for success/timestamp/error fields
//	    Items []ItemInfo `json:"items"` // Always present, even if empty
//	}
//
//	func PrintMyCommand() error {
//	    output := MyOutput{
//	        RobotResponse: NewRobotResponse(true),
//	        Items:         []ItemInfo{}, // Empty, not nil
//	    }
//	    return outputJSON(output)
//	}
//
// ## Compliance Status
//
// Compliant types (embed RobotResponse): TailOutput, SendOutput, ContextOutput,
// ActivityOutput, DiffOutput, AssignOutput, FilesOutput, InspectPaneOutput,
// MetricsOutput, ReplayOutput, PaletteOutput, TUIAlertsOutput, DismissAlertOutput,
// BeadsListOutput, BeadClaimOutput, BeadCreateOutput, BeadShowOutput, BeadCloseOutput,
// TokensOutput, SchemaOutput, RouteOutput, HistoryOutput.
//
// Non-compliant types (need migration): CASSStatusOutput, CASSSearchOutput,
// CASSInsightsOutput, CASSContextOutput, StatusOutput, PlanOutput, SnapshotOutput,
// SnapshotDeltaOutput, GraphOutput, AlertsOutput, RecipesOutput, TriageOutput,
// AckOutput, SpawnOutput, HealthOutput, SessionHealthOutput, InterruptOutput,
// DashboardOutput.
//
// See envelope_test.go for test coverage ensuring compliance.
package robot

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// Error codes for programmatic handling by AI agents.
// These codes allow agents to handle specific error types without parsing error messages.
const (
	// ErrCodeSessionNotFound indicates the requested session doesn't exist.
	ErrCodeSessionNotFound = "SESSION_NOT_FOUND"

	// ErrCodePaneNotFound indicates the requested pane doesn't exist.
	ErrCodePaneNotFound = "PANE_NOT_FOUND"

	// ErrCodeInvalidFlag indicates a flag value is invalid or malformed.
	ErrCodeInvalidFlag = "INVALID_FLAG"

	// ErrCodeTimeout indicates the operation timed out.
	ErrCodeTimeout = "TIMEOUT"

	// ErrCodeNotImplemented indicates a feature is planned but not yet available.
	ErrCodeNotImplemented = "NOT_IMPLEMENTED"

	// ErrCodeDependencyMissing indicates a required external tool is not installed.
	ErrCodeDependencyMissing = "DEPENDENCY_MISSING"

	// ErrCodeInternalError indicates an unexpected internal error.
	ErrCodeInternalError = "INTERNAL_ERROR"

	// ErrCodePermissionDenied indicates insufficient permissions.
	ErrCodePermissionDenied = "PERMISSION_DENIED"

	// ErrCodeResourceBusy indicates a resource is locked or in use.
	ErrCodeResourceBusy = "RESOURCE_BUSY"

	// =============================================================================
	// Restart/Exit Error Codes (bd-3vc3s)
	// =============================================================================

	// ErrCodeSoftExitFailed indicates Ctrl-C didn't work within timeout.
	ErrCodeSoftExitFailed = "SOFT_EXIT_FAILED"

	// ErrCodeHardKillFailed indicates kill -9 didn't work.
	ErrCodeHardKillFailed = "HARD_KILL_FAILED"

	// ErrCodeShellNotReturned indicates no shell prompt after exit.
	ErrCodeShellNotReturned = "SHELL_NOT_RETURNED"

	// ErrCodeCCLaunchFailed indicates the cc command failed.
	ErrCodeCCLaunchFailed = "CC_LAUNCH_FAILED"

	// ErrCodeCCInitTimeout indicates cc didn't initialize in time.
	ErrCodeCCInitTimeout = "CC_INIT_TIMEOUT"

	// ErrCodeBeadNotFound indicates the bead ID doesn't exist.
	ErrCodeBeadNotFound = "BEAD_NOT_FOUND"

	// ErrCodePromptSendFailed indicates failed to send prompt.
	ErrCodePromptSendFailed = "PROMPT_SEND_FAILED"
)

// RobotResponse is the base structure for all robot command outputs.
// All robot commands should embed this or include these fields.
//
// Design Philosophy:
// AI coding agents consume this output. They don't read external documentation
// before using commands - they parse JSON and make decisions based on what
// they see. Every response must be understandable WITHOUT external docs.
type RobotResponse struct {
	// Success indicates whether the operation completed successfully.
	// This is the first field agents should check.
	Success bool `json:"success"`

	// Timestamp is when this response was generated (RFC3339 format, UTC).
	Timestamp string `json:"timestamp"`

	// Error contains the human-readable error message when success=false.
	Error string `json:"error,omitempty"`

	// ErrorCode is a machine-readable error code for programmatic handling.
	// See ErrCode* constants for defined codes.
	ErrorCode string `json:"error_code,omitempty"`

	// Hint provides actionable guidance for resolving errors.
	// Example: "Use 'ntm list' to see available sessions"
	Hint string `json:"hint,omitempty"`

	// StructuredError provides detailed error information when simple error fields
	// are not sufficient. This is used for complex failure modes that require
	// debugging context. When set, this takes precedence over Error/ErrorCode/Hint.
	StructuredError *StructuredError `json:"structured_error,omitempty"`
}

// =============================================================================
// Structured Error Types (bd-3vc3s)
// =============================================================================
// These types provide detailed error information for complex failure modes.
// AI agents can use these to make informed recovery decisions.

// StructuredError provides comprehensive error information for complex failures.
// This enables AI agents to diagnose and recover from errors without manual inspection.
//
// Example JSON output:
//
//	{
//	  "code": "SOFT_EXIT_FAILED",
//	  "message": "Agent did not respond to Ctrl-C within 3s",
//	  "phase": "soft_exit",
//	  "pane": 4,
//	  "details": {
//	    "child_pid": 12345,
//	    "process_state": "running",
//	    "last_output": "... truncated ...",
//	    "attempted_actions": ["ctrl-c-1", "ctrl-c-2", "wait-3s"]
//	  },
//	  "recovery_hint": "Try --robot-restart-pane with automatic kill -9 fallback"
//	}
type StructuredError struct {
	// Code is a machine-readable error code (e.g., SOFT_EXIT_FAILED).
	Code string `json:"code"`

	// Message is a human-readable error description.
	Message string `json:"message"`

	// Phase identifies which operation step failed.
	// Common phases: init, soft_exit, hard_kill, post_exit, launch, prompt
	Phase string `json:"phase,omitempty"`

	// Pane is the affected pane index (if applicable).
	Pane int `json:"pane,omitempty"`

	// Details provides debugging context for the error.
	Details *ErrorDetails `json:"details,omitempty"`

	// RecoveryHint suggests how to resolve the error.
	RecoveryHint string `json:"recovery_hint,omitempty"`
}

// ErrorDetails provides debugging context for structured errors.
// Fields are populated based on error type and availability.
type ErrorDetails struct {
	// ChildPID is the process ID of the child process (if known).
	ChildPID int `json:"child_pid,omitempty"`

	// ProcessState describes the current process state (running, zombie, etc).
	ProcessState string `json:"process_state,omitempty"`

	// LastOutput is truncated recent terminal output for debugging.
	LastOutput string `json:"last_output,omitempty"`

	// AttemptedActions lists actions taken before failure.
	AttemptedActions []string `json:"attempted_actions,omitempty"`

	// AgentType is the type of agent (cc, cod, gmi).
	AgentType string `json:"agent_type,omitempty"`

	// ExitMethod describes how exit was attempted.
	ExitMethod string `json:"exit_method,omitempty"`

	// DurationMs is how long the operation took before failing.
	DurationMs int `json:"duration_ms,omitempty"`

	// ExpectedOutput describes what we expected to see.
	ExpectedOutput string `json:"expected_output,omitempty"`

	// ActualOutput describes what we actually saw.
	ActualOutput string `json:"actual_output,omitempty"`

	// Extra allows additional context not covered by standard fields.
	Extra map[string]interface{} `json:"extra,omitempty"`
}

// NewStructuredError creates a new StructuredError with the given code and message.
func NewStructuredError(code, message string) *StructuredError {
	return &StructuredError{
		Code:    code,
		Message: message,
	}
}

// WithPhase adds the phase field to a StructuredError.
func (e *StructuredError) WithPhase(phase string) *StructuredError {
	e.Phase = phase
	return e
}

// WithPane adds the pane field to a StructuredError.
func (e *StructuredError) WithPane(pane int) *StructuredError {
	e.Pane = pane
	return e
}

// WithDetails adds details to a StructuredError.
func (e *StructuredError) WithDetails(details *ErrorDetails) *StructuredError {
	e.Details = details
	return e
}

// WithRecoveryHint adds a recovery hint to a StructuredError.
func (e *StructuredError) WithRecoveryHint(hint string) *StructuredError {
	e.RecoveryHint = hint
	return e
}

// Error implements the error interface for StructuredError.
func (e *StructuredError) Error() string {
	if e.Phase != "" {
		return e.Phase + ": " + e.Message
	}
	return e.Message
}

// NewErrorDetails creates a new ErrorDetails instance.
func NewErrorDetails() *ErrorDetails {
	return &ErrorDetails{}
}

// WithChildPID sets the child PID on ErrorDetails.
func (d *ErrorDetails) WithChildPID(pid int) *ErrorDetails {
	d.ChildPID = pid
	return d
}

// WithProcessState sets the process state on ErrorDetails.
func (d *ErrorDetails) WithProcessState(state string) *ErrorDetails {
	d.ProcessState = state
	return d
}

// WithLastOutput sets truncated last output on ErrorDetails.
func (d *ErrorDetails) WithLastOutput(output string, maxLen int) *ErrorDetails {
	if len(output) > maxLen {
		d.LastOutput = output[:maxLen] + "... [truncated]"
	} else {
		d.LastOutput = output
	}
	return d
}

// WithAttemptedActions sets the list of attempted actions on ErrorDetails.
func (d *ErrorDetails) WithAttemptedActions(actions ...string) *ErrorDetails {
	d.AttemptedActions = actions
	return d
}

// WithAgentType sets the agent type on ErrorDetails.
func (d *ErrorDetails) WithAgentType(agentType string) *ErrorDetails {
	d.AgentType = agentType
	return d
}

// WithExitMethod sets the exit method on ErrorDetails.
func (d *ErrorDetails) WithExitMethod(method string) *ErrorDetails {
	d.ExitMethod = method
	return d
}

// WithDuration sets the duration in milliseconds on ErrorDetails.
func (d *ErrorDetails) WithDuration(ms int) *ErrorDetails {
	d.DurationMs = ms
	return d
}

// SetExtra adds an extra field to ErrorDetails.
func (d *ErrorDetails) SetExtra(key string, value interface{}) *ErrorDetails {
	if d.Extra == nil {
		d.Extra = make(map[string]interface{})
	}
	d.Extra[key] = value
	return d
}

// NewStructuredErrorResponse creates a RobotResponse with a structured error.
func NewStructuredErrorResponse(structErr *StructuredError) RobotResponse {
	resp := NewRobotResponse(false)
	resp.StructuredError = structErr
	// Also set the simple fields for backward compatibility
	resp.Error = structErr.Message
	resp.ErrorCode = structErr.Code
	resp.Hint = structErr.RecoveryHint
	return resp
}

// AgentHints provides optional guidance for AI agents consuming robot output.
// This is included in complex responses (status, snapshot, dashboard) to help
// agents make decisions without needing to implement complex logic themselves.
//
// The underscore prefix in JSON (_agent_hints) indicates this is meta-information
// that agents can safely ignore if they just want the raw data.
type AgentHints struct {
	// Summary is a human-readable one-liner describing the response.
	// Example: "2 sessions, 6 agents total (4 working, 2 idle)"
	Summary string `json:"summary,omitempty"`

	// SuggestedActions are actions the agent might want to take.
	SuggestedActions []RobotAction `json:"suggested_actions,omitempty"`

	// Warnings are non-fatal issues the agent should be aware of.
	// Example: "Agent in pane 3 approaching context limit (85%)"
	Warnings []string `json:"warnings,omitempty"`

	// Notes are informational messages that may be useful.
	Notes []string `json:"notes,omitempty"`
}

// RobotAction represents a recommended action for an AI agent in JSON output.
// This is different from SuggestedAction in markdown.go which is for markdown rendering.
type RobotAction struct {
	// Action is the type of action (e.g., "send_prompt", "wait", "spawn").
	Action string `json:"action"`

	// Target describes what the action should be applied to.
	// Example: "idle agents", "pane 2", "session myproject"
	Target string `json:"target,omitempty"`

	// Reason explains why this action is suggested.
	// Example: "2 agents available", "context at 95%"
	Reason string `json:"reason,omitempty"`

	// Priority indicates relative importance (higher = more important).
	Priority int `json:"priority,omitempty"`
}

// TerseKeyMap defines the short-key mapping for --robot-verbosity=terse JSON/TOON output.
// This is NOT used by --robot-terse (single-line encoded state).
//
// Mapping rules:
// - Only keys listed here are shortened.
// - Values must be unique to keep the mapping reversible.
// - Keep the mapping stable; add new keys only when needed by terse profile outputs.
//
// Agents can reverse the mapping using TerseKeyReverseMap().
var TerseKeyMap = map[string]string{
	// Envelope fields
	"success":    "ok",
	"timestamp":  "ts",
	"error":      "err",
	"error_code": "ec",
	"hint":       "h",

	// Optional agent guidance (only if included by profile)
	"_agent_hints": "ah",

	// Critical top-level arrays (always present per envelope spec)
	"sessions": "s",
	"panes":    "p",
	"targets":  "t",
	"agents":   "a",

	// Common top-level collections
	"alerts":   "al",
	"beads":    "b",
	"messages": "m",

	// Common meta fields
	"count":        "n",
	"generated_at": "ga",
	"summary":      "sum",

	// Structured error fields (bd-3vc3s)
	"structured_error": "se",
	"phase":            "ph",
	"details":          "d",
	"recovery_hint":    "rh",
}

// TerseKeyFor returns the short key for a long field name.
// If no mapping exists, ok is false and key is empty.
func TerseKeyFor(field string) (key string, ok bool) {
	key, ok = TerseKeyMap[field]
	return key, ok
}

// TerseKeyReverseMap returns the reverse mapping for short keys.
// It panics if the mapping is not reversible (duplicate short keys).
func TerseKeyReverseMap() map[string]string {
	reverse := make(map[string]string, len(TerseKeyMap))
	for longKey, shortKey := range TerseKeyMap {
		if existing, ok := reverse[shortKey]; ok {
			panic(fmt.Sprintf("terse key map collision: %q and %q both map to %q", existing, longKey, shortKey))
		}
		reverse[shortKey] = longKey
	}
	return reverse
}

// ExpandTerseKey converts a short key back to its long form.
// If the short key is unknown, ok is false and long is empty.
func ExpandTerseKey(short string) (long string, ok bool) {
	reverse := TerseKeyReverseMap()
	long, ok = reverse[short]
	return long, ok
}

// NewRobotResponse creates a new RobotResponse with current timestamp.
func NewRobotResponse(success bool) RobotResponse {
	return RobotResponse{
		Success:   success,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
	}
}

// NewErrorResponse creates an error RobotResponse with the given details.
func NewErrorResponse(err error, code, hint string) RobotResponse {
	resp := NewRobotResponse(false)
	if err != nil {
		resp.Error = err.Error()
	}
	resp.ErrorCode = code
	resp.Hint = hint
	return resp
}

// RobotError outputs a standardized error response as JSON and returns the original error.
// Use this when you want structured JSON output but need to return an error to the caller.
// This is useful for testing and for callers that want to handle errors themselves.
//
// Example usage:
//
//	if !tmux.SessionExists(session) {
//	    return RobotError(
//	        fmt.Errorf("session '%s' not found", session),
//	        ErrCodeSessionNotFound,
//	        "Use 'ntm list' to see available sessions",
//	    )
//	}
func RobotError(err error, code, hint string) error {
	resp := NewErrorResponse(err, code, hint)
	outputJSON(resp)
	return err
}

// PrintRobotError outputs a standardized error response and exits with code 1.
// Use this for actual errors that indicate something went wrong when you want
// to exit immediately. For testable code, prefer RobotError instead.
//
// Example usage:
//
//	if !tmux.SessionExists(session) {
//	    PrintRobotError(
//	        fmt.Errorf("session '%s' not found", session),
//	        ErrCodeSessionNotFound,
//	        "Use 'ntm list' to see available sessions",
//	    )
//	    return
//	}
func PrintRobotError(err error, code, hint string) {
	resp := NewErrorResponse(err, code, hint)
	outputJSON(resp)
	os.Exit(1)
}

// NotImplementedResponse is the structured output for unavailable features.
type NotImplementedResponse struct {
	RobotResponse
	Feature        string `json:"feature"`                   // The unavailable feature name
	PlannedVersion string `json:"planned_version,omitempty"` // Version where feature is planned
}

// PrintRobotUnavailable outputs a response for unavailable/unimplemented features
// and exits with code 2. Use this when a feature doesn't exist yet or a
// dependency is missing - it's not an error, just unavailable.
//
// Exit code 2 signals "unavailable" to agents, distinct from error (1) or success (0).
//
// Example usage:
//
//	robot.PrintRobotUnavailable(
//	    "robot-assign",
//	    "Work assignment is planned for a future release",
//	    "v1.3",
//	    "Use manual work distribution in the meantime",
//	)
func PrintRobotUnavailable(feature, message, plannedVersion, hint string) {
	resp := NotImplementedResponse{
		RobotResponse: RobotResponse{
			Success:   false,
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Error:     message,
			ErrorCode: ErrCodeNotImplemented,
			Hint:      hint,
		},
		Feature:        feature,
		PlannedVersion: plannedVersion,
	}
	outputJSON(resp)
	os.Exit(2)
}

// ErrorResponse is a complete error output structure that can be embedded
// in more specific response types or used standalone.
type ErrorResponse struct {
	RobotResponse
}

// SuccessResponse is a minimal success response.
type SuccessResponse struct {
	RobotResponse
}

// outputJSON encodes the value to stdout using the current robot output settings.
// It honors OutputFormat and OutputVerbosity (including terse key mapping).
// This is the internal helper used by Print* functions.
func outputJSON(v interface{}) error {
	return encodeJSON(v)
}

// WithAgentHints is a wrapper that adds _agent_hints to any response.
// Use this to add agent guidance to existing response types.
type WithAgentHints struct {
	// Embed the original response data
	Data interface{} `json:"-"`

	// AgentHints provides guidance for AI agents
	AgentHints *AgentHints `json:"_agent_hints,omitempty"`
}

// MarshalJSON implements custom JSON marshaling to flatten the Data field.
func (w WithAgentHints) MarshalJSON() ([]byte, error) {
	// First marshal the data
	dataBytes, err := json.Marshal(w.Data)
	if err != nil {
		return nil, err
	}

	// If no hints, just return the data
	if w.AgentHints == nil {
		return dataBytes, nil
	}

	// Parse data as a map
	var dataMap map[string]interface{}
	if err := json.Unmarshal(dataBytes, &dataMap); err != nil {
		return nil, fmt.Errorf("data must be a JSON object: %w", err)
	}

	// Add agent hints
	dataMap["_agent_hints"] = w.AgentHints

	return json.Marshal(dataMap)
}

// AddAgentHints wraps a response with agent hints.
func AddAgentHints(data interface{}, hints *AgentHints) WithAgentHints {
	return WithAgentHints{
		Data:       data,
		AgentHints: hints,
	}
}

// =============================================================================
// Timestamp Helpers - RFC3339 Standardization
// =============================================================================
// All robot command timestamps use RFC3339 format (ISO8601) in UTC.
// These helpers ensure consistency across all output types.

// FormatTimestamp returns an RFC3339 string for any time.Time in UTC.
// Use this for all timestamp fields in robot output.
func FormatTimestamp(t time.Time) string {
	return t.UTC().Format(time.RFC3339)
}

// FormatTimestampPtr handles nil time pointers, returning empty string for nil.
func FormatTimestampPtr(t *time.Time) string {
	if t == nil {
		return ""
	}
	return FormatTimestamp(*t)
}

// FormatUnixMillis converts Unix milliseconds to RFC3339 string.
// Use this when converting from external APIs that return Unix timestamps.
func FormatUnixMillis(ms int64) string {
	if ms == 0 {
		return ""
	}
	return FormatTimestamp(time.UnixMilli(ms))
}

// FormatUnixSeconds converts Unix seconds to RFC3339 string.
func FormatUnixSeconds(sec int64) string {
	if sec == 0 {
		return ""
	}
	return FormatTimestamp(time.Unix(sec, 0))
}
