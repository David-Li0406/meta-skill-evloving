# Multi-Agent Supervisors (MAS)

Multi-Agent Supervisors orchestrate multiple specialized agents, routing user queries to the most appropriate agent based on the query content.

## What is a Multi-Agent Supervisor?

A MAS acts as a traffic controller for multiple AI agents. When a user asks a question:

1. **Analyzes** the query to understand the intent
2. **Routes** to the most appropriate specialized agent
3. **Returns** the agent's response to the user

This allows you to combine multiple specialized agents into a single unified interface.

## When to Use

Use a Multi-Agent Supervisor when:
- You have multiple specialized agents (billing, technical support, HR, etc.)
- Users shouldn't need to know which agent to ask
- You want to provide a unified conversational experience

## Prerequisites

Before creating a MAS, you need:

**Model Serving Endpoints**: Each agent must be deployed as a model serving endpoint in Databricks.

These could be:
- Custom agents built with LangChain, LlamaIndex, etc.
- Fine-tuned models
- RAG applications
- External API integrations

## Creating a Multi-Agent Supervisor

Use the `create_or_update_mas` tool:

- `name`: "Customer Support MAS"
- `agents`:
  ```json
  [
    {
      "name": "billing_agent",
      "endpoint_name": "billing-assistant-endpoint",
      "description": "Handles billing, payments, invoices, and subscription questions"
    },
    {
      "name": "technical_agent",
      "endpoint_name": "tech-support-endpoint",
      "description": "Handles technical issues, bugs, and product features"
    },
    {
      "name": "hr_agent",
      "endpoint_name": "hr-assistant-endpoint",
      "description": "Handles HR policies, benefits, and employee questions"
    }
  ]
  ```
- `description`: "Routes customer queries to specialized support agents"
- `instructions`: "Analyze the user's question and route to the most appropriate agent. If unclear, ask for clarification."

## Agent Configuration

Each agent in the `agents` list needs:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Internal identifier for the agent |
| `endpoint_name` | Yes | Model serving endpoint name |
| `description` | Yes | What this agent handles (used for routing) |

### Writing Good Descriptions

The `description` field is critical for routing. Make it specific:

**Good descriptions:**
- "Handles billing questions including invoices, payments, refunds, and subscription changes"
- "Answers technical questions about API errors, integration issues, and product bugs"
- "Provides information about HR policies, PTO, benefits, and employee handbook"

**Bad descriptions:**
- "Billing agent" (too vague)
- "Handles stuff" (not helpful)
- "Technical" (not specific)

## Provisioning Timeline

After creation, the MAS endpoint needs to provision:

| Status | Meaning | Duration |
|--------|---------|----------|
| `PROVISIONING` | Creating the supervisor | 2-5 minutes |
| `ONLINE` | Ready to route queries | - |
| `OFFLINE` | Not currently running | - |

Use `get_mas` to check the status.

## Adding Example Questions

Example questions help with evaluation and can guide routing optimization:

```json
{
  "examples": [
    {
      "question": "I haven't received my invoice for this month",
      "guideline": "Should be routed to billing_agent"
    },
    {
      "question": "The API is returning a 500 error",
      "guideline": "Should be routed to technical_agent"
    },
    {
      "question": "How many vacation days do I have?",
      "guideline": "Should be routed to hr_agent"
    }
  ]
}
```

If the MAS is not yet `ONLINE`, examples are queued and added automatically when ready.

## Best Practices

### Agent Design

1. **Specialized agents**: Each agent should have a clear, distinct purpose
2. **Non-overlapping domains**: Avoid agents with similar descriptions
3. **Clear boundaries**: Define what each agent does and doesn't handle

### Instructions

Provide routing instructions:

```
You are a customer support supervisor. Your job is to route user queries to the right specialist:

1. For billing, payments, or subscription questions → billing_agent
2. For technical issues, bugs, or API problems → technical_agent
3. For HR, benefits, or policy questions → hr_agent

If the query is unclear or spans multiple domains, ask the user to clarify.
```

### Fallback Handling

Consider adding a general-purpose agent for queries that don't fit elsewhere:

```json
{
  "name": "general_agent",
  "endpoint_name": "general-support-endpoint",
  "description": "Handles general inquiries that don't fit other categories, provides navigation help"
}
```

## Example Workflow

1. **Deploy specialized agents** as model serving endpoints:
   - `billing-assistant-endpoint`
   - `tech-support-endpoint`
   - `hr-assistant-endpoint`

2. **Create the MAS**:
   - Configure agents with clear descriptions
   - Add routing instructions

3. **Wait for ONLINE status** (2-5 minutes)

4. **Add example questions** for evaluation

5. **Test routing** with various query types

## Updating a Multi-Agent Supervisor

To update an existing MAS:

1. **Add/remove agents**: Call `create_or_update_mas` with updated `agents` list
2. **Update descriptions**: Change agent descriptions to improve routing
3. **Modify instructions**: Update routing rules

The tool finds the existing MAS by name and updates it.

## Troubleshooting

### Queries routed to wrong agent

- Review and improve agent descriptions
- Make descriptions more specific and distinct
- Add examples that demonstrate correct routing

### Endpoint not responding

- Verify each underlying model serving endpoint is running
- Check endpoint logs for errors
- Ensure endpoints accept the expected input format

### Slow responses

- Check latency of underlying endpoints
- Consider endpoint scaling settings
- Monitor for cold start issues

## Advanced: Hierarchical Routing

For complex scenarios, you can create multiple levels of MAS:

```
Top-level MAS
├── Customer Support MAS
│   ├── billing_agent
│   ├── technical_agent
│   └── general_agent
├── Sales MAS
│   ├── pricing_agent
│   ├── demo_agent
│   └── contract_agent
└── Internal MAS
    ├── hr_agent
    └── it_helpdesk_agent
```

Each sub-MAS is deployed as an endpoint and configured as an agent in the top-level MAS.
