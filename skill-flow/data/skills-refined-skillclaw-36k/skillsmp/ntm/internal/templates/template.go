// Package templates provides prompt template loading, parsing, and variable substitution.
package templates

import (
	"fmt"
	"os"
	"time"
)

// Template represents a loaded prompt template with metadata.
type Template struct {
	Name        string         `yaml:"name"`
	Description string         `yaml:"description"`
	Variables   []VariableSpec `yaml:"variables"`
	Tags        []string       `yaml:"tags,omitempty"`
	Body        string         `yaml:"-"` // The template body (not in frontmatter)
	Source      TemplateSource `yaml:"-"` // Where this template came from
	SourcePath  string         `yaml:"-"` // File path if from file
}

// VariableSpec describes a template variable.
type VariableSpec struct {
	Name        string `yaml:"name"`
	Description string `yaml:"description,omitempty"`
	Required    bool   `yaml:"required,omitempty"`
	Default     string `yaml:"default,omitempty"`
}

// TemplateSource indicates where a template was loaded from.
type TemplateSource int

const (
	SourceBuiltin TemplateSource = iota
	SourceUser
	SourceProject
)

func (s TemplateSource) String() string {
	switch s {
	case SourceBuiltin:
		return "builtin"
	case SourceUser:
		return "user"
	case SourceProject:
		return "project"
	default:
		return "unknown"
	}
}

// BuiltinVariables returns the built-in variables available in all templates.
func BuiltinVariables() map[string]string {
	now := time.Now()
	cwd, _ := os.Getwd()

	return map[string]string{
		"cwd":  cwd,
		"date": now.Format("2006-01-02"),
		"time": now.Format("15:04:05"),
	}
}

// ExecutionContext holds variables for template execution.
type ExecutionContext struct {
	// User-provided variables via --var flags
	Variables map[string]string

	// File content injection via --file flag
	FileContent string

	// Session name for {{session}} variable
	Session string

	// Clipboard content for {{clipboard}} variable
	Clipboard string

	// Bead context for {{bead_id}}, {{bead_title}}, {{bead_priority}}, {{bead_description}}
	BeadID          string
	BeadTitle       string
	BeadPriority    string // e.g., "P0", "P1"
	BeadDescription string
	BeadStatus      string // e.g., "open", "in_progress"
	BeadType        string // e.g., "feature", "bug", "task"

	// Agent context for {{agent_num}}, {{agent_type}}, {{agent_variant}}, {{agent_pane}}
	AgentNum     int    // 1-indexed agent number
	AgentType    string // "claude", "codex", "gemini"
	AgentVariant string // e.g., "opus", "sonnet"
	AgentPane    string // pane ID like "%123"

	// Index in a multi-send operation for {{send_index}}, {{send_total}}
	SendIndex int // 0-indexed position in send batch
	SendTotal int // total number of targets in send batch
}

// WithBead sets bead context on an ExecutionContext and returns the modified context.
// This is a convenience method for chaining.
func (ctx ExecutionContext) WithBead(id, title, priority, description, status, issueType string) ExecutionContext {
	ctx.BeadID = id
	ctx.BeadTitle = title
	ctx.BeadPriority = priority
	ctx.BeadDescription = description
	ctx.BeadStatus = status
	ctx.BeadType = issueType
	return ctx
}

// WithAgent sets agent context on an ExecutionContext and returns the modified context.
// agentNum should be 1-indexed (first agent is 1, not 0).
func (ctx ExecutionContext) WithAgent(agentNum int, agentType, variant, paneID string) ExecutionContext {
	ctx.AgentNum = agentNum
	ctx.AgentType = agentType
	ctx.AgentVariant = variant
	ctx.AgentPane = paneID
	return ctx
}

// WithSendBatch sets send batch context (for multi-target sends).
// index is 0-indexed, total is the count of all targets.
func (ctx ExecutionContext) WithSendBatch(index, total int) ExecutionContext {
	ctx.SendIndex = index
	ctx.SendTotal = total
	return ctx
}

// Validate checks that all required variables are provided.
func (t *Template) Validate(ctx ExecutionContext) error {
	for _, v := range t.Variables {
		if !v.Required {
			continue
		}

		// Check if variable is provided via Variables map
		if _, ok := ctx.Variables[v.Name]; ok {
			continue
		}

		// Check if "file" variable is provided via FileContent
		if v.Name == "file" && ctx.FileContent != "" {
			continue
		}

		// Check if "session" variable is provided via Session
		if v.Name == "session" && ctx.Session != "" {
			continue
		}

		// Check if variable has a default value
		if v.Default != "" {
			continue
		}

		return fmt.Errorf("missing required variable: %s", v.Name)
	}
	return nil
}

// HasVariable checks if a variable is defined in the template.
func (t *Template) HasVariable(name string) bool {
	for _, v := range t.Variables {
		if v.Name == name {
			return true
		}
	}
	return false
}
