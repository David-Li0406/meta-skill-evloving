package dcg

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// ClaudeHookConfig represents the Claude Code hooks configuration format.
// See: https://docs.anthropic.com/en/docs/claude-code/hooks
type ClaudeHookConfig struct {
	Hooks HooksSection `json:"hooks"`
}

// HooksSection contains the different hook types.
type HooksSection struct {
	PreToolUse []HookEntry `json:"PreToolUse,omitempty"`
}

// HookEntry represents a single hook configuration.
type HookEntry struct {
	Matcher string `json:"matcher"`           // Tool name to match (e.g., "Bash")
	Command string `json:"command"`           // Command to run
	Timeout int    `json:"timeout,omitempty"` // Optional timeout in ms
}

// DCGHookOptions configures how DCG hooks are generated.
type DCGHookOptions struct {
	// BinaryPath is the path to the dcg binary. If empty, "dcg" is used (PATH lookup).
	BinaryPath string

	// AuditLog is an optional path to write audit logs.
	AuditLog string

	// Timeout is the hook timeout in milliseconds. Default is 5000ms.
	Timeout int

	// CustomBlocklist adds additional patterns to block.
	CustomBlocklist []string

	// CustomWhitelist adds patterns to always allow.
	CustomWhitelist []string
}

// DefaultDCGHookOptions returns sensible defaults for DCG hook configuration.
func DefaultDCGHookOptions() DCGHookOptions {
	return DCGHookOptions{
		Timeout: 5000, // 5 seconds
	}
}

// GenerateHookConfig creates a Claude Code hook configuration for DCG.
// The generated hook intercepts Bash tool calls and validates them against DCG.
func GenerateHookConfig(opts DCGHookOptions) (*ClaudeHookConfig, error) {
	dcgBinary := opts.BinaryPath
	if dcgBinary == "" {
		dcgBinary = "dcg"
	}

	// Build the check command
	// DCG check command format: dcg check [options] "<command>"
	// The command placeholder will be filled by Claude Code via $CLAUDE_TOOL_INPUT_command
	var cmdParts []string
	cmdParts = append(cmdParts, dcgBinary, "check")

	// Add audit log option if specified
	if opts.AuditLog != "" {
		cmdParts = append(cmdParts, "--audit-log", opts.AuditLog)
	}

	// Add custom blocklist patterns
	for _, pattern := range opts.CustomBlocklist {
		cmdParts = append(cmdParts, "--block", pattern)
	}

	// Add custom whitelist patterns
	for _, pattern := range opts.CustomWhitelist {
		cmdParts = append(cmdParts, "--allow", pattern)
	}

	// The command argument - use shell variable that Claude Code sets
	cmdParts = append(cmdParts, "--", "$CLAUDE_TOOL_INPUT_command")

	checkCmd := strings.Join(cmdParts, " ")

	config := &ClaudeHookConfig{
		Hooks: HooksSection{
			PreToolUse: []HookEntry{
				{
					Matcher: "Bash",
					Command: checkCmd,
					Timeout: opts.Timeout,
				},
			},
		},
	}

	return config, nil
}

// GenerateHookJSON creates the JSON string for Claude Code hook configuration.
func GenerateHookJSON(opts DCGHookOptions) (string, error) {
	config, err := GenerateHookConfig(opts)
	if err != nil {
		return "", err
	}

	data, err := json.MarshalIndent(config, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal hook config: %w", err)
	}

	return string(data), nil
}

// DCGAvailability tracks whether DCG is available and can be used for hooks.
type DCGAvailability struct {
	Available   bool
	BinaryPath  string
	Version     string
	LastChecked time.Time
	Error       string
}

var (
	dcgAvailabilityCache DCGAvailability
	dcgAvailabilityMutex sync.RWMutex
	dcgCacheTTL          = 5 * time.Minute
)

// CheckDCGAvailable checks if dcg is installed and available.
func CheckDCGAvailable(binaryPath string) DCGAvailability {
	dcgAvailabilityMutex.RLock()
	if time.Since(dcgAvailabilityCache.LastChecked) < dcgCacheTTL {
		cached := dcgAvailabilityCache
		dcgAvailabilityMutex.RUnlock()
		return cached
	}
	dcgAvailabilityMutex.RUnlock()

	result := checkDCGAvailabilityUncached(binaryPath)

	dcgAvailabilityMutex.Lock()
	dcgAvailabilityCache = result
	dcgAvailabilityMutex.Unlock()

	return result
}

func checkDCGAvailabilityUncached(binaryPath string) DCGAvailability {
	result := DCGAvailability{
		LastChecked: time.Now(),
	}

	binary := binaryPath
	if binary == "" {
		binary = "dcg"
	}

	// Check if binary exists
	path, err := exec.LookPath(binary)
	if err != nil {
		result.Error = fmt.Sprintf("dcg not found: %v", err)
		return result
	}

	result.BinaryPath = path
	result.Available = true

	// Try to get version
	cmd := exec.Command(path, "--version")
	output, err := cmd.Output()
	if err == nil {
		result.Version = strings.TrimSpace(string(output))
	}

	return result
}

// InvalidateDCGCache clears the DCG availability cache.
func InvalidateDCGCache() {
	dcgAvailabilityMutex.Lock()
	dcgAvailabilityCache = DCGAvailability{}
	dcgAvailabilityMutex.Unlock()
}

// WriteHookConfigFile writes the DCG hook configuration to a file.
// This can be used to persist the hook configuration for Claude Code.
func WriteHookConfigFile(opts DCGHookOptions, configPath string) error {
	jsonConfig, err := GenerateHookJSON(opts)
	if err != nil {
		return err
	}

	// Ensure parent directory exists
	dir := filepath.Dir(configPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create config directory: %w", err)
	}

	return os.WriteFile(configPath, []byte(jsonConfig), 0644)
}

// HookEnvVars returns environment variables that can be set to configure
// Claude Code hooks for DCG. These can be passed to the agent process.
func HookEnvVars(opts DCGHookOptions) (map[string]string, error) {
	jsonConfig, err := GenerateHookJSON(opts)
	if err != nil {
		return nil, err
	}

	// Claude Code reads hooks from CLAUDE_CODE_HOOKS env var
	return map[string]string{
		"CLAUDE_CODE_HOOKS": jsonConfig,
	}, nil
}

// ShouldConfigureHooks determines if DCG hooks should be configured
// for an agent spawn based on DCG availability and configuration.
func ShouldConfigureHooks(dcgEnabled bool, binaryPath string) bool {
	if !dcgEnabled {
		return false
	}

	availability := CheckDCGAvailable(binaryPath)
	return availability.Available
}
