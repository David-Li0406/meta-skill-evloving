package prompts

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// Prompt interface defines the contract for all MCP prompts
// Prompts are pre-written templates that guide LLM clients (like OpenShift Lightspeed)
// in how to effectively use the MCP server's capabilities.
type Prompt interface {
	// Name returns the unique identifier for this prompt
	Name() string

	// Description returns a human-readable description of what this prompt does
	Description() string

	// GetPrompt returns the MCP prompt definition including arguments and metadata
	GetPrompt() *mcp.Prompt

	// Execute generates the prompt messages based on the provided arguments
	// This is called when Lightspeed wants to use this prompt template
	Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error)
}
