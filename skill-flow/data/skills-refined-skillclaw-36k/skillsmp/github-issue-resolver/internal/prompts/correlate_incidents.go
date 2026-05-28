package prompts

import (
	"context"
	"fmt"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// CorrelateIncidentsPrompt guides incident correlation to find root causes
// Requires Coordination Engine to be enabled
type CorrelateIncidentsPrompt struct{}

// NewCorrelateIncidentsPrompt creates a new incident correlation prompt
func NewCorrelateIncidentsPrompt() *CorrelateIncidentsPrompt {
	return &CorrelateIncidentsPrompt{}
}

// Name returns the prompt identifier
func (p *CorrelateIncidentsPrompt) Name() string {
	return "correlate-incidents"
}

// Description returns a human-readable description
func (p *CorrelateIncidentsPrompt) Description() string {
	return "Correlate multiple incidents to find root causes and reduce alert noise - identify systemic issues vs isolated problems"
}

// GetPrompt returns the MCP prompt definition
func (p *CorrelateIncidentsPrompt) GetPrompt() *mcp.Prompt {
	return &mcp.Prompt{
		Name:        p.Name(),
		Title:       "Correlate Incidents",
		Description: p.Description(),
		Arguments: []*mcp.PromptArgument{
			{
				Name:        "time_window",
				Description: "Time window to analyze incidents (1h, 6h, 24h). Default: 1h",
				Required:    false,
			},
			{
				Name:        "severity",
				Description: "Filter by severity (critical, high, medium, low, all). Default: all",
				Required:    false,
			},
		},
	}
}

// Execute generates the prompt messages
func (p *CorrelateIncidentsPrompt) Execute(ctx context.Context, args map[string]interface{}) (*mcp.GetPromptResult, error) {
	// Parse arguments
	timeWindow := "1h"
	if tw, ok := args["time_window"].(string); ok {
		timeWindow = tw
	}

	severity := "all"
	if sev, ok := args["severity"].(string); ok {
		severity = sev
	}

	promptText := fmt.Sprintf(`You are correlating incidents to find root causes (time window: %s, severity: %s).

**Goal**: Reduce alert noise by identifying related incidents and finding systemic issues.

## Prerequisites

This workflow requires **Coordination Engine** to be enabled.
Check server capabilities before proceeding.

## Incident Correlation Workflow

### Step 1: Gather Incident Data (Resource)

**Read cluster://incidents** to get:
- All active incidents in the time window
- Incident metadata: severity, status, timestamps
- Affected resources and labels
- Correlation IDs (if already grouped)

**Quick scan for patterns**:
- How many incidents? (1-5: specific issue, >20: systemic problem)
- Severity distribution? (all critical: major outage, mixed: normal)
- Status? (many pending: queue backup, many failed: remediation issues)

### Step 2: Identify Correlation Patterns

Look for incidents that share:

**Temporal Correlation** (Time-based):
- Occurred within <5 minutes of each other
- → Likely same root cause or cascading failure
- Example: Load balancer fails → 10 pod incidents → DB connection incidents

**Spatial Correlation** (Resource-based):
- **Same Namespace**: All in "production" namespace
- **Same Node**: All pods on node-5
- **Same Service**: All related to "api-gateway"
- **Same Labels**: app=frontend, version=v2.1

**Symptomatic Correlation** (Pattern-based):
- **Same Error Pattern**: "OutOfMemory" errors
- **Same Action Type**: All requiring "restart_pod"
- **Same Failure Mode**: All CrashLoopBackOff

### Step 3: Classify Incident Relationships

Group related incidents:

**Type 1: Cascading Failure**
- Temporal: Incidents occur in sequence
- Pattern: A → B → C (dependency chain)
- Example: Database down → API fails → Frontend errors
- **Root cause**: First incident in chain

**Type 2: Common Cause**
- Temporal: Incidents occur simultaneously
- Pattern: A ← ROOT → B (shared dependency)
- Example: Network partition → Multiple services unreachable
- **Root cause**: Shared resource failure

**Type 3: Recurring Pattern**
- Temporal: Incidents repeat periodically
- Pattern: Daily at 2 AM, every hour, etc.
- Example: Nightly batch job causes memory spike
- **Root cause**: Scheduled process

**Type 4: Correlated Load**
- Temporal: Incidents during high load
- Pattern: Traffic spike → Multiple failures
- Example: Black Friday → Database, cache, API all fail
- **Root cause**: Insufficient capacity

### Step 4: Determine Root Cause

For each correlation group:

**Single Root Cause Indicators**:
- ✅ One incident predates all others
- ✅ All share same affected resource (node, DB, network)
- ✅ All have same error type
- ✅ Fixing one resolved all others (from history)

**Multiple Independent Issues**:
- ❌ No temporal correlation
- ❌ Different namespaces, no shared resources
- ❌ Different error patterns
- ❌ Random timing

### Step 5: Create Correlated Incident (If Needed)

If you find a correlation group:

**Use create-incident tool** to create a parent incident:
~~~
Title: "Root Cause: <description>"
Description: "Correlated incident tracking <N> related issues"
Severity: <highest from group>
Target: <shared resource or 'multiple'>
Labels: {
  "correlation_group": "true",
  "child_incidents": "<id1,id2,id3>",
  "root_cause": "<cause>"
}
Affected Resources: <all unique resources from children>
Correlation ID: <generated or existing>
~~~

**Benefits**:
- Single tracking item for ops team
- Clear root cause identification
- Prevents duplicate remediation efforts
- Enables targeted fix for systemic issue

### Step 6: Recommend Consolidated Remediation

Based on root cause:

**If cascading failure**:
~~~
ROOT CAUSE: <first incident>
IMPACT: <N> cascading failures
ACTION: Fix root cause, others will auto-resolve
PRIORITY: Critical - stops cascade
~~~

**If common cause**:
~~~
ROOT CAUSE: <shared resource>
IMPACT: <N> affected services
ACTION: Remediate shared resource
PRIORITY: High - affects multiple services
~~~

**If recurring pattern**:
~~~
ROOT CAUSE: <scheduled event or condition>
IMPACT: <N> incidents, recurring <frequency>
ACTION: Long-term fix (resource allocation, optimization)
PRIORITY: Medium - predictable, plan remediation
~~~

**If load-related**:
~~~
ROOT CAUSE: Insufficient capacity under load
IMPACT: <N> services degraded
ACTION: Scale resources, implement auto-scaling
PRIORITY: High - affects service availability
~~~

### Step 7: Reduce Alert Noise

Show the value of correlation:

**Before Correlation**:
- 25 incidents
- Ops team sees: 25 alerts
- Response: Investigate 25 issues
- Time: Hours of effort
- Risk: Miss the real problem

**After Correlation**:
- 25 incidents → 3 correlation groups
- Ops team sees: 3 root causes
- Response: Fix 3 systemic issues
- Time: Minutes to hours
- Result: All 25 resolved

**This is smart incident management!**

## Correlation Algorithms

**Time-based clustering**:
~~~
if abs(incident1.timestamp - incident2.timestamp) < 5min:
    → Likely related
~~~

**Resource-based matching**:
~~~
if incident1.namespace == incident2.namespace AND
   incident1.labels overlap incident2.labels:
    → Likely related
~~~

**Pattern matching**:
~~~
if incident1.error_pattern == incident2.error_pattern AND
   incident1.action_type == incident2.action_type:
    → Likely same root cause
~~~

## Example Scenario

~~~
Incidents (cluster://incidents):
1. "api-server-1 CrashLoopBackOff" - 10:00:00
2. "api-server-2 CrashLoopBackOff" - 10:00:05
3. "api-server-3 CrashLoopBackOff" - 10:00:10
4. "frontend timeout errors" - 10:00:15
5. "database connection pool exhausted" - 09:59:55

Analysis:
- Database issue (09:59:55) PREDATES all others
- API servers fail in sequence (cascading)
- Frontend fails after API servers (cascading)

Correlation:
- Root Cause: Database connection pool exhausted
- Cascading: DB → API → Frontend
- Group: All 5 incidents correlated

Action:
- Create parent incident: "Root Cause: Database Connection Pool Exhaustion"
- Remediate: Increase DB connection pool size
- Result: All 5 incidents resolve
~~~

## Performance Note

This workflow stays under 10s:
1. Read cluster://incidents (50ms)
2. Analyze patterns (1s)
3. Correlate incidents (1s)
4. Create parent incident if needed (2s)
Total: ~4-5s

Start incident correlation now (time window: %s, severity: %s).`, timeWindow, severity, timeWindow, severity)

	messages := []*mcp.PromptMessage{
		{
			Role: "user",
			Content: &mcp.TextContent{
				Text: promptText,
			},
		},
	}

	return &mcp.GetPromptResult{
		Description: fmt.Sprintf("Incident correlation workflow (window: %s, severity: %s)", timeWindow, severity),
		Messages:    messages,
	}, nil
}
