package prompts

import (
	"context"
	"fmt"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// DiagnoseClusterPrompt guides systematic cluster health diagnostics
// This is the MOST IMPORTANT prompt for preventing timeouts - it teaches
// Lightspeed to use Resources (fast, cached) before Tools (slower, real-time)
type DiagnoseClusterPrompt struct{}

// NewDiagnoseClusterPrompt creates a new cluster diagnostics prompt
func NewDiagnoseClusterPrompt() *DiagnoseClusterPrompt {
	return &DiagnoseClusterPrompt{}
}

// Name returns the prompt identifier
func (p *DiagnoseClusterPrompt) Name() string {
	return "diagnose-cluster-issues"
}

// Description returns a human-readable description
func (p *DiagnoseClusterPrompt) Description() string {
	return "Systematic workflow for diagnosing OpenShift cluster health issues - teaches efficient Resource-first approach to prevent timeouts"
}

// GetPrompt returns the MCP prompt definition
func (p *DiagnoseClusterPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Diagnose Cluster Issues",
		Description: p.Description(),
		Arguments: []*mcp.PromptArgument{
			{
				Name:        "severity",
				Description: "Filter by severity level (critical, warning, all). Default: all",
				Required:    false,
			},
		},
	}
}

// Execute generates the prompt messages
func (p *DiagnoseClusterPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	// Parse severity argument (default: "all")
	severity := "all"
	if s, ok := args["severity"].(string); ok {
		severity = s
	}

	// Generate the diagnostic workflow prompt
	promptText := fmt.Sprintf(`You are diagnosing OpenShift cluster issues (severity filter: %s).

**CRITICAL: EFFICIENT WORKFLOW TO PREVENT TIMEOUTS**

Follow this exact sequence to ensure fast responses:

## Step 1: START WITH RESOURCES (Fast, Cached Data)

**Always read these Resources FIRST** - they are cached and return instantly:

1. **cluster://health** (10s cache)
   - Overall cluster status (healthy/degraded/critical)
   - Node statistics (total, ready, not_ready)
   - Pod statistics (running, pending, failed)
   - Active issues count

2. **cluster://nodes** (30s cache)
   - Detailed node information
   - Node conditions (Ready, MemoryPressure, DiskPressure)
   - Resource capacity and usage

3. **cluster://incidents** (5s cache, if Coordination Engine enabled)
   - Active incidents from self-healing system
   - Severity, status, affected resources

**WHY Resources First?** Resources are cached (10-30s TTL) and return in <100ms.
This prevents timeouts and provides immediate context.

## Step 2: ANALYZE THE DATA

Based on Resource data, identify:
- ❌ Unhealthy nodes (NotReady > 0)
- ❌ Failed/pending pods
- ❌ Resource pressure (memory/disk)
- ❌ Active incidents with high severity

## Step 3: INVESTIGATE (Tools Only When Needed)

**Only use Tools for specific investigations** after analyzing Resource data:

- **list-pods**: Get detailed pod info for specific namespaces
  - Use when you need container restart counts, detailed status
  - Provide namespace filter to limit results

- **list-incidents**: Get incident details with filters
  - Use when you need specific incident parameters

- **analyze-anomalies**: Run ML-powered anomaly detection
  - Use when cluster://health shows issues but cause is unclear
  - Requires KServe enabled

## Step 4: PROVIDE DIAGNOSIS

Based on all data, provide:
1. **Root Causes**: What's causing the issues?
2. **Severity Assessment**: Critical, high, medium, or low?
3. **Remediation Steps**: Prioritized actions to resolve issues
4. **Prevention**: How to prevent recurrence?

## Severity Filtering

Current filter: **%s**
- **critical**: Show only critical severity issues
- **warning**: Show warnings and above
- **all**: Show all issues (default)

## Example Workflow

✅ **CORRECT (Fast, <2s total):**
1. Read cluster://health → See 3 failed pods
2. Read cluster://nodes → All nodes healthy
3. Use list-pods tool with namespace filter → Get pod details
4. Diagnose: Application issue, not infrastructure

❌ **INCORRECT (Slow, may timeout):**
1. Use list-pods with no filters → Returns 1000+ pods, takes 5-10s
2. Manually analyze all pods
3. Eventually timeout or provide slow response

## Key Principles

🚀 **Speed**: Resources first (cached), Tools second (specific)
🎯 **Precision**: Use filters to limit tool results
⏱️ **Timeouts**: Stay under 10s total response time
📊 **Context**: Resources provide the big picture

Start your diagnosis now following this workflow.`, severity, severity)

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: fmt.Sprintf("Cluster diagnostic workflow (severity: %s)", severity),
		Messages:    messages,
	}, nil
}
