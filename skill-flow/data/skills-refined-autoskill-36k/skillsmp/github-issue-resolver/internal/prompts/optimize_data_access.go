package prompts

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// OptimizeDataAccessPrompt educates about efficient Resource vs Tool usage
type OptimizeDataAccessPrompt struct{}

// NewOptimizeDataAccessPrompt creates a new data access optimization prompt
func NewOptimizeDataAccessPrompt() *OptimizeDataAccessPrompt {
	return &OptimizeDataAccessPrompt{}
}

// Name returns the prompt identifier
func (p *OptimizeDataAccessPrompt) Name() string {
	return "optimize-data-access"
}

// Description returns a human-readable description
func (p *OptimizeDataAccessPrompt) Description() string {
	return "Educational guide on when to use Resources vs Tools for optimal performance and timeout prevention"
}

// GetPrompt returns the MCP prompt definition
func (p *OptimizeDataAccessPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Optimize Data Access",
		Description: p.Description(),
		Arguments:   []*mcp.PromptArgument{}, // No arguments needed
	}
}

// Execute generates the educational prompt messages
func (p *OptimizeDataAccessPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	promptText := `# MCP Server Performance Guide: Resources vs Tools

This guide helps you use the MCP server efficiently and avoid timeouts.

## The Golden Rule

**ALWAYS START WITH RESOURCES, USE TOOLS SPARINGLY**

## Understanding Resources

**Resources** are like reading a file - fast, cached data:

| Resource URI | Cache TTL | Response Time | Use For |
|--------------|-----------|---------------|---------|
| cluster://health | 10s | <100ms | Overall health check |
| cluster://nodes | 30s | <100ms | Node status and capacity |
| cluster://incidents | 5s | <50ms | Active remediation actions |
| cluster://remediation-history | 15s | <100ms | Past remediation success rates |

**Why Resources are Fast:**
- Data is cached in memory
- No live Kubernetes API calls
- Returns immediately
- Perfect for overview and context

**When to Use Resources:**
1. Starting any investigation (get context first!)
2. Checking overall status
3. Finding patterns (multiple resources together)
4. When speed matters (user-facing queries)

## Understanding Tools

**Tools** are like running a command - slower, real-time execution:

| Tool | Response Time | Use For |
|------|---------------|---------|
| get-cluster-health | 1-3s | Fresh cluster snapshot |
| list-pods | 2-5s | Detailed pod filtering |
| list-incidents | 1-2s | Filtered incident search |
| analyze-anomalies | 3-8s | ML-powered analysis |
| trigger-remediation | 2-5s | Initiate fixes |
| get-remediation-recommendations | 3-6s | ML predictions |

**Why Tools are Slower:**
- Make live Kubernetes API calls
- Execute ML models
- Communicate with external services
- Process and filter data

**When to Use Tools:**
1. After Resources show an issue
2. Need specific, filtered data
3. Want fresh, real-time information
4. Taking actions (remediation)

## Timeout Prevention Strategy

The MCP server has a **10-second timeout** for requests.

### ✅ Good Pattern (2-3s total):
~~~
1. Read cluster://health (100ms)
   → See 10 failed pods in "production" namespace
2. Use list-pods tool with namespace filter (2s)
   → Get details on those 10 pods
3. Analyze and respond
~~~

### ❌ Bad Pattern (10-15s, TIMEOUT):
~~~
1. Use list-pods with no filters (8s)
   → Returns 1000+ pods across all namespaces
2. Try to analyze in LLM
3. Timeout or very slow response
~~~

## Cache Awareness

Understanding cache TTLs helps you balance freshness vs speed:

**Short TTL (5s) - cluster://incidents:**
- Very fresh data
- Use when investigating active issues
- Still faster than tools

**Medium TTL (10s) - cluster://health:**
- Good balance
- Perfect for most queries
- Refresh every 10s

**Long TTL (30s) - cluster://nodes:**
- Nodes don't change often
- Acceptable staleness
- Maximum performance

## Combining Resources

**Most powerful pattern**: Read multiple Resources together

~~~
Parallel reads (all cached):
- cluster://health → Overall status
- cluster://nodes → Infrastructure health
- cluster://incidents → Active fixes

Total time: <100ms (served from cache)
Total insight: Complete picture of cluster
~~~

## Tool Usage Best Practices

When you must use Tools:

1. **Always filter**: namespace, labels, fields
2. **Limit results**: Use limit parameter (default: 100, max: 1000)
3. **Be specific**: Target exactly what you need
4. **Check Resources first**: Understand context before diving deep

## Performance Metrics

Target response times for Lightspeed queries:

- **Simple queries** (<1s): Use only Resources
- **Medium queries** (1-3s): Resources + 1 Tool
- **Complex queries** (3-7s): Resources + 2-3 Tools
- **Very complex** (7-10s): Resources + multiple Tools with heavy filters

**NEVER exceed 10s** - this is the hard timeout limit.

## Real-World Examples

### Example 1: "What's wrong with my cluster?"
~~~
✅ Fast approach (1s):
- Read cluster://health
- Read cluster://incidents
- Summarize

❌ Slow approach (10s+):
- Use get-cluster-health tool (fresh but slow)
- Use list-pods with no filter
- Timeout risk
~~~

### Example 2: "Are there any crashlooping pods?"
~~~
✅ Fast approach (2s):
- Read cluster://health (check if any failed pods exist)
- If yes, use list-pods with appropriate filter

❌ Slow approach (8s+):
- Immediately use list-pods without filter
- Get all pods, manually search
~~~

### Example 3: "Predict upcoming issues"
~~~
✅ Fast approach (4s):
- Read cluster://remediation-history (past patterns)
- Read cluster://health (current state)
- Use get-remediation-recommendations (ML predictions)
- Correlate and predict

❌ Slow approach (12s+):
- Use analyze-anomalies without context
- Use list-incidents with no filter
- Timeout
~~~

## Key Takeaways

1. 🚀 **Resources First**: Always start with cached data
2. 🎯 **Filter Tools**: Never use tools without filters
3. ⏱️ **Watch Time**: Stay under 10s total
4. 📊 **Context Matters**: Resources provide the big picture
5. 🔄 **Cache Aware**: Know TTLs, balance fresh vs fast
6. 🛡️ **Prevent Timeouts**: Plan your data access strategy

## Questions?

When in doubt, ask yourself:
- "Do I need real-time data, or is 10-30s old data OK?"
- If OK → Use Resources
- If real-time needed → Use Tools with filters

This approach ensures fast, reliable responses and happy users!`

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: "Guide to optimizing MCP data access for performance",
		Messages:    messages,
	}, nil
}
