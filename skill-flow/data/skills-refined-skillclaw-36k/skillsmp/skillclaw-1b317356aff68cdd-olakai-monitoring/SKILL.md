---
name: olakai-monitoring
description: Use this skill when you want to integrate Olakai monitoring into an AI agent, whether creating a new agent from scratch or adding monitoring to an existing one.
---

# Olakai Monitoring Integration

This skill guides you through creating a new AI agent with Olakai monitoring or adding monitoring to an existing AI agent or LLM-powered application.

## Prerequisites

Before starting, ensure:
1. Olakai CLI installed: `npm install -g olakai-cli`
2. CLI authenticated: `olakai login`
3. API key for SDK (generated per-agent via CLI - see Step 2.1)
4. For existing agents, ensure you have access to the agent's API key (get via CLI: `olakai agents get AGENT_ID --json | jq '.apiKey'`)

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

### How It Works

1. **customData** (SDK): Raw JSON you send with each event
2. **CustomDataConfig** (Platform): Schema defining which fields are processed
3. **Context Variables**: CustomDataConfig fields become available for formulas
4. **KPI Formula**: Expression that computes KPI values based on context variables

## Creating a New AI Agent with Monitoring

1. **Initialize a New Agent**:
   - Use the command: `olakai agents create --name "YourAgentName" --with-api-key`
   
2. **Configure KPIs**:
   - Define 2-4 KPIs relevant to your agent's purpose.

3. **Implement Monitoring**:
   - Follow the steps to integrate the SDK and set up the custom data flow.

## Adding Monitoring to an Existing Agent

1. **Identify the Existing Agent**:
   - Ensure you have the agent's API key.

2. **Integrate Monitoring**:
   - Use the command: `olakai agents add-monitoring AGENT_ID`

3. **Configure KPIs**:
   - Similar to new agents, define KPIs that reflect the performance and business value of the existing agent.

By following these steps, you can effectively integrate Olakai monitoring into both new and existing AI agents, ensuring you gain valuable insights into their performance and impact.