package prompts

import (
	"context"
	"fmt"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// CheckAnomaliesPrompt guides ML-powered anomaly detection workflows
type CheckAnomaliesPrompt struct{}

// NewCheckAnomaliesPrompt creates a new anomaly checking prompt
func NewCheckAnomaliesPrompt() *CheckAnomaliesPrompt {
	return &CheckAnomaliesPrompt{}
}

// Name returns the prompt identifier
func (p *CheckAnomaliesPrompt) Name() string {
	return "check-anomalies"
}

// Description returns a human-readable description
func (p *CheckAnomaliesPrompt) Description() string {
	return "ML-powered anomaly detection workflow using KServe models and Coordination Engine"
}

// GetPrompt returns the MCP prompt definition
func (p *CheckAnomaliesPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Check for Anomalies",
		Description: p.Description(),
		Arguments: []*mcp.PromptArgument{
			{
				Name:        "namespace",
				Description: "Limit anomaly detection to specific namespace (optional)",
				Required:    false,
			},
			{
				Name:        "timeframe",
				Description: "Time window to analyze (1h, 6h, 24h, 7d). Default: 1h",
				Required:    false,
			},
		},
	}
}

// Execute generates the prompt messages
func (p *CheckAnomaliesPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	// Parse arguments
	namespace := ""
	if ns, ok := args["namespace"].(string); ok {
		namespace = ns
	}

	timeframe := "1h"
	if tf, ok := args["timeframe"].(string); ok {
		timeframe = tf
	}

	scope := "cluster-wide"
	if namespace != "" {
		scope = fmt.Sprintf("namespace: %s", namespace)
	}

	promptText := fmt.Sprintf(`You are checking for anomalies (%s, timeframe: %s).

## Anomaly Detection Workflow

### Prerequisites

This workflow requires:
- **KServe** integration enabled (for ML models)
- **Coordination Engine** enabled (for analysis)

Check server capabilities first.

### Step 1: Context Gathering (Resources)

**Start with Resources** to understand baseline:
1. **cluster://health** - Current cluster state
2. **cluster://nodes** - Node health and resource usage
3. **cluster://incidents** - Recent self-healing actions

This provides context for detected anomalies.

### Step 2: Run Anomaly Detection

**Use the analyze-anomalies tool** with parameters:
- namespace: "%s" (empty = all namespaces)
- time_range: "%s"
- threshold: 0.7 (confidence threshold, 0.0-1.0)

The tool returns:
- Detected anomaly patterns
- Severity (low, medium, high, critical)
- Confidence scores
- Affected resources
- ML model recommendations

### Step 3: Analyze Anomaly Patterns

Group anomalies by type:

**Resource Anomalies:**
- CPU spikes above normal
- Memory usage trending up
- Disk I/O bottlenecks
- → Impact: Performance degradation

**Network Anomalies:**
- Unusual traffic patterns
- Connection failures
- Latency spikes
- → Impact: Service disruption

**Application Anomalies:**
- Error rate increases
- Request volume changes
- Response time degradation
- → Impact: User experience

**Systemic Anomalies:**
- Multiple correlated anomalies
- Cascading failures
- → Impact: Potential outage

### Step 4: Correlate with Incidents

**Read cluster://incidents** to see:
- Are anomalies already being remediated?
- Were similar issues detected before?
- What actions were taken?

This prevents duplicate remediation efforts.

### Step 5: Recommend Actions

Based on anomaly severity and patterns:

**Critical (score >0.9):**
- Immediate investigation required
- Check if remediation is already triggered
- Alert ops team

**High (score 0.7-0.9):**
- Schedule investigation
- Monitor for escalation
- Consider preventive action

**Medium/Low (score <0.7):**
- Log for trending analysis
- Monitor for patterns
- No immediate action needed

## ML Model Confidence

- **>0.9**: High confidence, likely real issue
- **0.7-0.9**: Medium confidence, investigate
- **<0.7**: Low confidence, may be noise

## Timeframe Recommendations

- **1h**: Recent issues, fast detection
- **6h**: Pattern analysis, trending
- **24h**: Daily patterns, comprehensive
- **7d**: Long-term trends, recurring issues

## Example Workflow

✅ **Efficient (3-5s total):**
1. Read cluster://health → See degraded status
2. Run analyze-anomalies with namespace filter → CPU spike detected
3. Read cluster://incidents → No remediation yet
4. Recommend: Scale up deployment or investigate cause

❌ **Inefficient:**
1. Run analyze-anomalies without context
2. Get 100+ anomalies from all namespaces
3. Can't prioritize what's important
4. Timeout or analysis paralysis

Start anomaly detection now.`, scope, timeframe, namespace, timeframe)

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: fmt.Sprintf("Anomaly detection workflow (%s, %s)", scope, timeframe),
		Messages:    messages,
	}, nil
}
