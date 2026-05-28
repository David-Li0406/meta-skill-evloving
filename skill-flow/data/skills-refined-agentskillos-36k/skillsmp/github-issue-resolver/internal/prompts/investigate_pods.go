package prompts

import (
	"context"
	"fmt"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// InvestigatePodsPrompt guides pod troubleshooting workflows
type InvestigatePodsPrompt struct{}

// NewInvestigatePodsPrompt creates a new pod investigation prompt
func NewInvestigatePodsPrompt() *InvestigatePodsPrompt {
	return &InvestigatePodsPrompt{}
}

// Name returns the prompt identifier
func (p *InvestigatePodsPrompt) Name() string {
	return "investigate-pods"
}

// Description returns a human-readable description
func (p *InvestigatePodsPrompt) Description() string {
	return "Guided workflow for investigating pod failures, crashes, and performance issues"
}

// GetPrompt returns the MCP prompt definition
func (p *InvestigatePodsPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Investigate Pods",
		Description: p.Description(),
		Arguments: []*mcp.PromptArgument{
			{
				Name:        "namespace",
				Description: "Kubernetes namespace to investigate (required)",
				Required:    true,
			},
			{
				Name:        "pod_name",
				Description: "Specific pod name to investigate (optional, wildcards supported)",
				Required:    false,
			},
		},
	}
}

// Execute generates the prompt messages
func (p *InvestigatePodsPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	// Parse arguments
	namespace, ok := args["namespace"].(string)
	if !ok || namespace == "" {
		return nil, fmt.Errorf("namespace argument is required")
	}

	podName := ""
	if pn, ok := args["pod_name"].(string); ok {
		podName = pn
	}

	// Generate the investigation workflow prompt
	scope := namespace
	if podName != "" {
		scope = fmt.Sprintf("%s/%s", namespace, podName)
	}

	promptText := fmt.Sprintf(`You are investigating pods in: **%s**

## Pod Investigation Workflow

### Step 1: Get Pod Overview (Resource First!)

**Use cluster://health first** to check:
- Total pods in cluster and their states
- Any failed or pending pods
- Overall cluster health context

This gives you the big picture before diving into specifics.

### Step 2: List Pods with Filters

**Use the list-pods tool** with these parameters:
- namespace: "%s"
%s- limit: 50 (to prevent timeout)

The tool provides:
- Pod status (Running, Pending, Failed, etc.)
- Restart counts (high restarts = crashloop)
- Ready status (containers ready vs total)
- Age
- Node assignment

### Step 3: Analyze Pod Patterns

Look for common issues:

**CrashLoopBackOff:**
- High restart count (>5)
- Status: Running/CrashLoopBackOff
- → Check: Application errors, missing config, resource limits

**ImagePullBackOff:**
- Status: Waiting/ImagePullBackOff
- → Check: Image name, registry auth, network

**Pending:**
- Status: Pending for >5min
- → Check: Resource requests vs available, node selectors, taints/tolerations

**OOMKilled:**
- High restart count + memory limit
- → Check: Memory limits too low, memory leaks

### Step 4: Identify Root Cause

Based on pod data:
1. **Application Issues**: Restarts, crash loops → Check logs (outside MCP scope)
2. **Resource Issues**: Pending, evicted → Check node capacity
3. **Configuration Issues**: Failed to pull image → Check manifests
4. **Infrastructure Issues**: Node problems → Read cluster://nodes resource

### Step 5: Recommend Actions

Provide specific, actionable remediation:
- **If crashloop**: Suggest checking application logs and configuration
- **If pending**: Show resource availability and scheduling constraints
- **If image issues**: Verify image registry and credentials
- **If node issues**: Point to cluster://nodes for node health

## Tips for Efficient Investigation

✅ **Filter aggressively**: Use namespace and pod_name filters
✅ **Check patterns**: Multiple pods failing = systemic issue
✅ **Use Resources**: cluster://health and cluster://nodes provide context
✅ **Be specific**: Provide namespace and pod names in recommendations

❌ **Don't**: List all pods without filters (timeout risk)
❌ **Don't**: Investigate in isolation (check cluster context first)

Start your pod investigation now.`, scope, namespace, func() string {
		if podName != "" {
			return fmt.Sprintf("- field_selector: \"metadata.name=%s\"\n", podName)
		}
		return ""
	}())

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: fmt.Sprintf("Pod investigation workflow for %s", scope),
		Messages:    messages,
	}, nil
}
