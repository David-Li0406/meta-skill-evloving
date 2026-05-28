---
name: olakai-monitoring
description: Use this skill to create a new AI agent or add monitoring to an existing AI agent with Olakai for observability and KPI tracking.
---

# Olakai Monitoring for AI Agents

This skill guides you through creating a new AI agent or adding Olakai monitoring to an existing AI agent or LLM-powered application, enabling analytics and governance.

## Prerequisites

Before starting, ensure:
1. Olakai CLI installed: `npm install -g olakai-cli`
2. CLI authenticated: `olakai login`
3. API key for SDK (generated per-agent via CLI - see Step 2.1)

## Why Custom KPIs Are Essential

Olakai's core value is **tracking business-specific KPIs for your AI agents**. Without KPIs, you're just logging events - not gaining actionable insights.

**What you can measure with KPIs:**
- Business outcomes (items processed, success rates, revenue impact)
- Operational metrics (step counts, retry rates, execution time)
- Quality indicators (error rates, user satisfaction signals)

**Without KPIs configured:**
- ❌ No dashboard metrics beyond basic token counts
- ❌ No aggregated performance views
- ❌ No alerting thresholds
- ❌ No ROI calculations

> ⚠️ **Every agent should have 2-4 KPIs that answer: "How do I know this agent is performing well?"**

## Understanding the customData → KPI Pipeline

Before diving into implementation, understand how data flows through Olakai:

```
SDK customData → CustomDataConfig (Schema) → Context Variable → KPI Formula → kpiData
```

### Critical Rules

| Rule | Consequence |
|------|-------------|
| Only CustomDataConfig fields become variables | Unregistered customData fields are NOT usable in KPIs |
| Formula evaluation is case-insensitive | `stepCount`, `STEPCOUNT`, `StepCount` all work in formulas |
| NUMBER configs need numeric values | Don't send `"5"` (string), send `5` (number) |

### Built-in Context Variables (Always Available)

| Variable | Type | Description |
|----------|------|-------------|
| `Prompt` | string | The prompt text sent to the LLM |
| `Response` | string | The LLM response text |
| `Documents count` | number | Number of attached documents |
| `PII detected` | boolean | Whether PII was detected |
| `PHI detected` | boolean | Whether PHI was detected |
| `CODE detected` | boolean | Whether code was detected |
| `SECRET detected` | boolean | Whether secrets were detected |

## Step 1: Create a New AI Agent

### 1.1 Determine Agent Type

**Agentic AI** (Multi-step autonomous workflows):
- Research agents, document processors, data pipelines
- Track as SINGLE events aggregating all internal LLM calls
- Focus on workflow-level metrics (total tokens, total time, success/failure)

**Assistive AI** (Interactive chatbots/copilots):
- Customer support bots, coding assistants, Q&A systems
- Track EACH interaction as separate events
- Focus on conversation-level metrics (per-message tokens, response quality)

### 1.2 Design Your Metrics Schema (CRITICAL)

**Design your metrics BEFORE writing any SDK code.** This ensures only meaningful data is sent and tracked.

#### Step A: Identify Business Questions

What do stakeholders need to know about this agent?
- "How many items does it process per run?"
- "What's the success/failure rate?"
- "How efficient is each execution?"

#### Step B: Map Questions to Metrics

| Business Question | Field Name | Type | KPI Formula | Aggregation |
|-------------------|------------|------|-------------|-------------|
| Throughput | ItemsProcessed | NUMBER | `ItemsProcessed` | SUM |
| Reliability | SuccessRate | NUMBER | `SuccessRate * 100` | AVERAGE |
| Error count | SuccessRate | NUMBER | `IF(SuccessRate < 1, 1, 0)` | SUM |
| Workflow ID | ExecutionId | STRING | (for filtering only) | - |

#### Step C: Plan Your customData Structure

```typescript
// ONLY include fields you'll register as CustomDataConfigs
customData: {
  // Business metrics (will become KPIs)
  ItemsProcessed: number,  // Count of items handled
  SuccessRate: number,     // 0-1 success ratio

  // Performance metrics (will become KPIs)
  StepCount: number,       // Number of workflow steps

  // Identification (for filtering, not KPIs)
  ExecutionId: string,     // Correlation ID
}
```

> ⚠️ **IMPORTANT**: Only include fields you will register as CustomDataConfigs.
> Unregistered fields are stored but **cannot be used in KPIs** - they're effectively wasted data.

### 1.3 Create the Agent in Olakai

```bash
# Create the agent associated with the workflow
olakai agents create \
  --name "Your Agent Name" \
  --description "What this agent does" \
  --workflow WORKFLOW_ID \
  --with-api-key \
  --json
```

## Step 2: Add Monitoring to an Existing AI Agent

### 2.1 Install the SDK

For TypeScript/JavaScript:
```bash
npm install @olakai/sdk
```

For Python:
```bash
pip install olakai-sdk
```

### 2.2 Wrap Your Existing Client

#### TypeScript Example:
```typescript
import OpenAI from "openai";
import { OlakaiSDK } from "@olakai/sdk";

const olakai = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY! });
await olakai.init();

const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  { provider: "openai" }
);
```

#### Python Example:
```python
from openai import OpenAI
from olakaisdk import olakai_config, instrument_openai

olakai_config(os.getenv("OLAKAI_API_KEY"))
instrument_openai()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### 2.3 Add Context to Calls

#### TypeScript:
```typescript
const response = await openai.chat.completions.create(
  { model: "gpt-4o", messages: [{ role: "user", content: userMessage }] },
  { userEmail: user.email, task: "Customer Experience" }
);
```

#### Python:
```python
with olakai_context(userEmail=user.email, task="Customer Experience"):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
```

### 2.4 Handle Agentic Workflows

If your agent makes multiple LLM calls per task, aggregate them into a single event:

```typescript
async function processDocument(doc: Document): Promise<ProcessingResult> {
  const startTime = Date.now();
  let totalTokens = 0;

  // Step 1: Extract
  const extraction = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Extract from: ${doc.content}` }],
  });
  totalTokens += extraction.usage?.total_tokens ?? 0;

  // Step 2: Analyze
  const analysis = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Analyze: ${extraction.choices[0].message.content}` }],
  });
  totalTokens += analysis.usage?.total_tokens ?? 0;

  // Step 3: Summarize
  const summary = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Summarize: ${analysis.choices[0].message.content}` }],
  });
  totalTokens += summary.usage?.total_tokens ?? 0;

  const result = summary.choices[0].message.content ?? "";

  // Track the complete workflow as ONE event
  olakai.event({
    prompt: `Process document: ${doc.title}`,
    response: result,
    tokens: totalTokens,
    requestTime: Date.now() - startTime,
    task: "Data Processing & Analysis",
    customData: {
      DocumentId: doc.id,
      DocumentType: doc.type,
      StepCount: 3,
      Success: 1,
    },
  });

  return { summary: result, tokens: totalTokens };
}
```

## Step 3: Configure Custom Metrics

### 3.1 Create Custom Data Configurations

```bash
# For each field in your customData, create a config
olakai custom-data create --name "DocumentId" --type STRING
olakai custom-data create --name "DocumentType" --type STRING
olakai custom-data create --name "StepCount" --type NUMBER
olakai custom-data create --name "Success" --type NUMBER  # Use 1/0 for boolean
```

### 3.2 Create KPIs

```bash
olakai kpis create \
  --name "Documents Processed" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "IF(Success = 1, 1, 0)" \
  --aggregation SUM

olakai kpis create \
  --name "Avg Steps per Document" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "StepCount" \
  --aggregation AVERAGE
```

## Step 4: Test-Validate-Iterate Cycle

**CRITICAL:** Always validate your implementation by running a test and inspecting the actual event data. Do not assume configuration is correct - verify it.

### 4.1 Run Your Agent (Generate Test Event)

Execute your agent with test data to generate at least one monitoring event.

### 4.2 Fetch and Inspect the Event

```bash
# List recent activity for your agent
olakai activity list --agent-id YOUR_AGENT_ID --limit 1 --json

# Get the full event details including customData and kpiData
olakai activity get EVENT_ID --json
```

### 4.3 Validate Each Component

**Check customData is present and correct:**
```bash
olakai activity get EVENT_ID --json | jq '.customData'
```

**Check KPIs are numeric (not strings):**
```bash
olakai activity get EVENT_ID --json | jq '.kpiData'
```

### 4.4 Iterate Until Correct

Repeat the cycle until all validations pass.

## Quick Reference

```bash
# CLI Commands
olakai login                           # Authenticate
olakai agents create --name "Name"     # Create agent
olakai custom-data create --name X --type NUMBER  # Create custom field
olakai kpis create --formula "X" --agent-id ID    # Create KPI
olakai activity list --agent-id ID     # View events
```

## KPI Formula Reference

### Supported Operators

| Category | Operators |
|----------|-----------|
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `<`, `<=`, `=`, `<>`, `>=`, `>` |
| Logical | `AND`, `OR`, `NOT` |
| Conditional | `IF(condition, true_val, false_val)` |
| Null handling | `ISNA(value)`, `ISDEFINED(value)` |

### Common Formula Patterns

```bash
# Simple variable passthrough
--formula "ItemsProcessed"

# Percentage conversion (0-1 to 0-100)
--formula "SuccessRate * 100"

# Conditional counting (count failures)
--formula "IF(SuccessRate < 1, 1, 0)"
```

### Aggregation Types

| Aggregation | Use For |
|-------------|---------|
| `SUM` | Totals, counts |
| `AVERAGE` | Rates, percentages |