// Package policy provides destructive command protection through pattern matching.
package policy

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"gopkg.in/yaml.v3"
)

// DefaultPolicyPath is the default location for the policy file.
const DefaultPolicyPath = ".ntm/policy.yaml"

// Action represents what should happen when a command matches a pattern.
type Action string

const (
	ActionBlock   Action = "block"
	ActionApprove Action = "approve" // requires approval
	ActionAllow   Action = "allow"
)

// Rule represents a single policy rule.
type Rule struct {
	Pattern string `yaml:"pattern"`
	Reason  string `yaml:"reason,omitempty"`
	SLB     bool   `yaml:"slb,omitempty"` // Requires SLB two-person approval
	regex   *regexp.Regexp
}

// AutomationConfig controls automatic operations.
type AutomationConfig struct {
	AutoPush     bool   `yaml:"auto_push"`     // Allow automatic git push
	AutoCommit   bool   `yaml:"auto_commit"`   // Allow automatic git commit
	ForceRelease string `yaml:"force_release"` // "never", "approval", "auto"
}

// Policy represents the complete policy configuration.
type Policy struct {
	Version          int              `yaml:"version"`
	Blocked          []Rule           `yaml:"blocked"`
	ApprovalRequired []Rule           `yaml:"approval_required"`
	Allowed          []Rule           `yaml:"allowed"`
	Automation       AutomationConfig `yaml:"automation"`
}

// Match represents a matched policy rule.
type Match struct {
	Action  Action
	Pattern string
	Reason  string
	Command string
	SLB     bool // Whether this match requires SLB approval
}

// Load reads and parses a policy file from the given path.
func Load(path string) (*Policy, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading policy file: %w", err)
	}

	var p Policy
	if err := yaml.Unmarshal(data, &p); err != nil {
		return nil, fmt.Errorf("parsing policy file: %w", err)
	}

	// Compile all regex patterns
	if err := p.compile(); err != nil {
		return nil, err
	}

	return &p, nil
}

// LoadOrDefault loads the policy from the default path, or returns an empty policy if not found.
func LoadOrDefault() (*Policy, error) {
	path := DefaultPolicyPath

	// Try home directory first, then current directory
	if home, err := os.UserHomeDir(); err == nil {
		homePath := filepath.Join(home, DefaultPolicyPath)
		if _, err := os.Stat(homePath); err == nil {
			path = homePath
		}
	}

	// Check current directory
	if _, err := os.Stat(path); os.IsNotExist(err) {
		// Return default policy with common dangerous patterns
		return DefaultPolicy(), nil
	}

	return Load(path)
}

// DefaultPolicy returns a sensible default policy for destructive command protection.
func DefaultPolicy() *Policy {
	p := &Policy{
		Version: 1,
		// Automation defaults
		Automation: AutomationConfig{
			AutoPush:     false,      // Require explicit push
			AutoCommit:   true,       // Allow auto-commit
			ForceRelease: "approval", // Require approval for force release
		},
		// Allowed patterns checked FIRST - explicitly safe commands
		Allowed: []Rule{
			{Pattern: `git\s+push\s+.*--force-with-lease`, Reason: "Force with lease is safer than force push"},
			{Pattern: `git\s+reset\s+--soft`, Reason: "Soft reset preserves changes"},
			{Pattern: `git\s+reset\s+HEAD~?\d*$`, Reason: "Mixed reset preserves working directory"},
		},
		// Blocked patterns - dangerous commands (checked after allowed)
		Blocked: []Rule{
			{Pattern: `git\s+reset\s+--hard`, Reason: "Hard reset loses uncommitted changes"},
			{Pattern: `git\s+clean\s+-fd`, Reason: "Removes untracked files permanently"},
			// Match --force followed by space or end-of-string (not --force-with-lease)
			// The allowed pattern for --force-with-lease takes precedence
			{Pattern: `git\s+push\s+.*--force(\s|$)`, Reason: "Force push can overwrite remote history"},
			{Pattern: `git\s+push\s+(.*\s)?-f(\s|$)`, Reason: "Force push can overwrite remote history"},
			{Pattern: `rm\s+-rf\s+/$`, Reason: "Recursive delete of root is catastrophic"},
			{Pattern: `rm\s+-rf\s+~`, Reason: "Recursive delete of home directory"},
			{Pattern: `rm\s+-rf\s+\*`, Reason: "Recursive delete of everything in current directory"},
			{Pattern: `git\s+branch\s+-D`, Reason: "Force delete branch loses unmerged work"},
			{Pattern: `git\s+stash\s+drop`, Reason: "Dropping stash loses saved work"},
			{Pattern: `git\s+stash\s+clear`, Reason: "Clearing all stashes loses saved work"},
		},
		// Approval required - potentially dangerous commands
		ApprovalRequired: []Rule{
			{Pattern: `git\s+rebase\s+-i`, Reason: "Interactive rebase rewrites history"},
			{Pattern: `git\s+commit\s+--amend`, Reason: "Amending rewrites history"},
			{Pattern: `rm\s+-rf\s+\S`, Reason: "Recursive force delete"},
			{Pattern: `force_release`, Reason: "Force release another agent's reservation", SLB: true},
		},
	}
	// Compile patterns; ignore errors for default policy as these are hardcoded
	// and should always be valid. Any patterns that fail will just not match.
	_ = p.compile()
	return p
}

// compile compiles all regex patterns in the policy.
func (p *Policy) compile() error {
	for i := range p.Blocked {
		re, err := regexp.Compile(p.Blocked[i].Pattern)
		if err != nil {
			return fmt.Errorf("invalid blocked pattern %q: %w", p.Blocked[i].Pattern, err)
		}
		p.Blocked[i].regex = re
	}

	for i := range p.ApprovalRequired {
		re, err := regexp.Compile(p.ApprovalRequired[i].Pattern)
		if err != nil {
			return fmt.Errorf("invalid approval_required pattern %q: %w", p.ApprovalRequired[i].Pattern, err)
		}
		p.ApprovalRequired[i].regex = re
	}

	for i := range p.Allowed {
		re, err := regexp.Compile(p.Allowed[i].Pattern)
		if err != nil {
			return fmt.Errorf("invalid allowed pattern %q: %w", p.Allowed[i].Pattern, err)
		}
		p.Allowed[i].regex = re
	}

	return nil
}

// Check evaluates a command against the policy and returns a match if found.
// Returns nil if the command is not matched by any rule (implicitly allowed).
// Order of precedence: allowed > blocked > approval_required
func (p *Policy) Check(command string) *Match {
	// Normalize command for matching
	cmd := strings.TrimSpace(command)

	// Check allowed first (explicit allowlist takes precedence)
	for _, rule := range p.Allowed {
		if rule.regex != nil && rule.regex.MatchString(cmd) {
			return &Match{
				Action:  ActionAllow,
				Pattern: rule.Pattern,
				Reason:  rule.Reason,
				Command: cmd,
			}
		}
	}

	// Check blocked patterns
	for _, rule := range p.Blocked {
		if rule.regex != nil && rule.regex.MatchString(cmd) {
			return &Match{
				Action:  ActionBlock,
				Pattern: rule.Pattern,
				Reason:  rule.Reason,
				Command: cmd,
			}
		}
	}

	// Check approval required patterns
	for _, rule := range p.ApprovalRequired {
		if rule.regex != nil && rule.regex.MatchString(cmd) {
			return &Match{
				Action:  ActionApprove,
				Pattern: rule.Pattern,
				Reason:  rule.Reason,
				Command: cmd,
				SLB:     rule.SLB,
			}
		}
	}

	// No match - implicitly allowed
	return nil
}

// IsBlocked returns true if the command matches a blocked pattern.
func (p *Policy) IsBlocked(command string) bool {
	match := p.Check(command)
	return match != nil && match.Action == ActionBlock
}

// NeedsApproval returns true if the command requires approval.
func (p *Policy) NeedsApproval(command string) bool {
	match := p.Check(command)
	return match != nil && match.Action == ActionApprove
}

// Stats returns counts of rules by type.
func (p *Policy) Stats() (blocked, approval, allowed int) {
	return len(p.Blocked), len(p.ApprovalRequired), len(p.Allowed)
}

// NeedsSLBApproval returns true if the action requires SLB two-person approval.
func (p *Policy) NeedsSLBApproval(action string) bool {
	match := p.Check(action)
	return match != nil && match.Action == ActionApprove && match.SLB
}

// AutomationEnabled checks if a specific automation feature is enabled.
func (p *Policy) AutomationEnabled(feature string) bool {
	switch feature {
	case "auto_push":
		return p.Automation.AutoPush
	case "auto_commit":
		return p.Automation.AutoCommit
	default:
		return false
	}
}

// ForceReleasePolicy returns the force release policy: "never", "approval", or "auto".
func (p *Policy) ForceReleasePolicy() string {
	if p.Automation.ForceRelease == "" {
		return "approval" // Default to requiring approval
	}
	return p.Automation.ForceRelease
}

// Validate checks the policy for errors.
func (p *Policy) Validate() error {
	// Validate version
	if p.Version < 1 {
		p.Version = 1 // Default to version 1
	}

	// Validate force_release value
	switch p.Automation.ForceRelease {
	case "", "never", "approval", "auto":
		// Valid values
	default:
		return fmt.Errorf("invalid force_release value: %q (must be never, approval, or auto)", p.Automation.ForceRelease)
	}

	// Compile patterns to validate them
	return p.compile()
}
