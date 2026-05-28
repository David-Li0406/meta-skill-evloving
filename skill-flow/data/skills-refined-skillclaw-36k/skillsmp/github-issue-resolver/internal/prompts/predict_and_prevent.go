package prompts

import (
	"context"
	"fmt"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// PredictAndPreventPrompt guides proactive remediation using ML predictions
// Requires Coordination Engine to be enabled
type PredictAndPreventPrompt struct{}

// NewPredictAndPreventPrompt creates a new predictive remediation prompt
func NewPredictAndPreventPrompt() *PredictAndPreventPrompt {
	return &PredictAndPreventPrompt{}
}

// Name returns the prompt identifier
func (p *PredictAndPreventPrompt) Name() string {
	return "predict-and-prevent"
}

// Description returns a human-readable description
func (p *PredictAndPreventPrompt) Description() string {
	return "Proactive remediation workflow using ML predictions from Coordination Engine - shift from reactive to preventive cluster management"
}

// GetPrompt returns the MCP prompt definition
func (p *PredictAndPreventPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Predict and Prevent Issues",
		Description: p.Description(),
		Arguments: []*mcp.PromptArgument{
			{
				Name:        "timeframe",
				Description: "Prediction timeframe (1h, 6h, 24h). Default: 6h",
				Required:    false,
			},
			{
				Name:        "confidence_threshold",
				Description: "Minimum prediction confidence (0.0-1.0). Default: 0.7",
				Required:    false,
			},
		},
	}
}

// Execute generates the prompt messages
func (p *PredictAndPreventPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	// Parse arguments
	timeframe := "6h"
	if tf, ok := args["timeframe"].(string); ok {
		timeframe = tf
	}

	confidenceThreshold := 0.7
	if ct, ok := args["confidence_threshold"].(float64); ok {
		confidenceThreshold = ct
	}

	promptText := fmt.Sprintf(`You are performing PROACTIVE cluster management using ML predictions.

**Goal**: Prevent issues BEFORE they occur, not just react to them.

## Prerequisites

This workflow requires **Coordination Engine** to be enabled.
Check server capabilities before proceeding.

## Predictive Remediation Workflow

### Step 1: Understand Current State (Resources)

**Read Resources** to establish baseline:
1. **cluster://health** - Current cluster status
2. **cluster://remediation-history** - Past remediation success patterns
3. **cluster://incidents** - Any active issues being addressed

**Why this matters**: ML predictions are most valuable when you understand:
- What's normal vs abnormal
- What fixes worked before
- What's already being handled

### Step 2: Get ML-Powered Predictions

**Use get-remediation-recommendations tool** with:
- timeframe: "%s" (prediction window)
- include_predictions: true (CRITICAL - enables ML predictions)
- confidence_threshold: %.2f (filter noise)

**What you'll get**:
- **Predicted Issues**: Problems likely to occur within timeframe
  - Resource exhaustion (CPU, memory, disk)
  - Application failures
  - Network degradation
  - Node issues

- **Confidence Scores** (0.0-1.0):
  - >0.9: Very likely, take action now
  - 0.7-0.9: Likely, prepare preventive measures
  - <0.7: Possible, monitor

- **Recommendations**: Specific preventive actions
  - Scale deployments
  - Adjust resource limits
  - Clear caches
  - Restart services
  - Update configurations

- **Alerts with action_required flag**:
  - true: Immediate action recommended
  - false: Informational only

### Step 3: Analyze Predictions Against History

**Read cluster://remediation-history** to answer:
- Have we seen similar predictions before?
- What actions were taken?
- What was the success rate?
- How long did remediation take?

**Example Analysis**:
~~~
Prediction: "pod-xyz will run out of memory in 4h" (confidence: 0.85)
History: Similar prediction 3 times in past week
Success: scale_up action succeeded 2/3 times (67%% success rate)
Duration: Average 5 minutes to complete
Decision: High confidence + proven fix → Take preventive action
~~~

### Step 4: Prioritize Preventive Actions

Rank predictions by:
1. **Criticality**: Impact if issue occurs
2. **Confidence**: How certain is the prediction
3. **Success History**: Does the recommended fix work?
4. **Time to Impact**: How soon will issue occur?

**Priority Matrix**:
| Confidence | Impact | Action |
|------------|--------|--------|
| >0.9 | Critical | **Act now** - Prevent imminent failure |
| >0.9 | High | **Schedule soon** - Within 1 hour |
| 0.7-0.9 | Critical | **Prepare** - Have remediation ready |
| 0.7-0.9 | High/Medium | **Monitor** - Watch for escalation |
| <0.7 | Any | **Log only** - Track for pattern analysis |

### Step 5: Recommend Prevention Strategy

For each high-priority prediction:

**If action_required: true AND confidence >0.8:**
~~~
RECOMMENDED PREVENTIVE ACTION:
Problem: <predicted issue>
Confidence: <score>
Time to impact: <hours>
Action: <specific remediation>
Success rate: <%%>
Estimated duration: <minutes>

Suggest: Trigger remediation now using trigger-remediation tool
~~~

**If action_required: true BUT confidence 0.7-0.8:**
~~~
PREPARE FOR POTENTIAL ISSUE:
Problem: <predicted issue>
Confidence: <score>
Recommended: Have remediation plan ready
Watch for: <escalation indicators>
~~~

**If action_required: false:**
~~~
MONITORING RECOMMENDED:
Pattern detected: <description>
Confidence: <score>
Action: Track trend, no immediate action needed
~~~

### Step 6: Explain the Shift

Help users understand the value:

**Reactive (Traditional)**:
1. Issue occurs
2. Alerts fire
3. On-call responds
4. Debug and fix
5. Service impact: High

**Proactive (This Workflow)**:
1. ML predicts issue
2. Preventive action taken
3. Issue never occurs
4. Users unaffected
5. Service impact: None

**This is the future of cluster management!**

## Timeframe Guidance

- **1h**: Immediate predictions, urgent prevention
- **6h**: Standard prediction window (recommended)
- **24h**: Long-term planning, capacity management

## Confidence Interpretation

- **0.9-1.0**: Very high - ML has strong evidence
- **0.7-0.9**: High - Take seriously, likely accurate
- **0.5-0.7**: Medium - Monitor, may be real
- **<0.5**: Low - Noise, ignore unless pattern emerges

## Example Scenario

~~~
Current State (cluster://health):
- Status: Healthy
- Memory usage: 70%%

Prediction (get-remediation-recommendations):
- Issue: "Memory exhaustion in deployment/api-server"
- Confidence: 0.92
- Time to impact: 3 hours
- Recommendation: scale_up (add 2 replicas)
- action_required: true

History (cluster://remediation-history):
- Similar: 5 times in past month
- Action taken: scale_up
- Success rate: 100%%
- Avg duration: 3 minutes

Decision: PREVENT
- Trigger scale_up now
- No service impact
- Issue prevented before occurrence
~~~

## Performance Note

This workflow is optimized to stay under 10s:
1. Read Resources (100ms)
2. Get ML predictions (3-5s)
3. Analyze and recommend (2s)
Total: ~5-7s

Start your predictive analysis now (timeframe: %s, confidence threshold: %.2f).`, timeframe, confidenceThreshold, timeframe, confidenceThreshold)

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: fmt.Sprintf("Predictive remediation workflow (timeframe: %s, threshold: %.2f)", timeframe, confidenceThreshold),
		Messages:    messages,
	}, nil
}
