# Workflow

This skill delegates all fidelity review logic to the dedicated `mcp__plugin_foundry_foundry-mcp__review action="fidelity"` MCP tool, which handles spec loading, implementation analysis, AI consultation, and report generation.

## Step 1: Validate Inputs

Ensure the user provides:
- `spec_id`: The specification to review
- Either `task_id` (for task-level review) or `phase_id` (for phase-level review)

## Step 2: Construct MCP Invocation

Build the appropriate `mcp__plugin_foundry_foundry-mcp__review action="fidelity"` command based on review scope:

**For task review:**
```bash
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id={spec-id} task_id={task-id}
```

**For phase review:**
```bash
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id={spec-id} phase_id={phase-id}
```

## Step 3: Execute the MCP Tool

Invoke the MCP tool directly:
```bash
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id={spec-id} task_id={task-id}
```

**CRITICAL:** The MCP tool handles ALL spec file operations. Do NOT:
- Read spec files with Read tool
- Parse specs with Python or jq
- Use cat/head/tail/grep on spec files
- Create temporary bash scripts (e.g., `/tmp/*.sh`)
- Use bash loops to iterate through tasks
- Use grep/sed/awk to parse JSON outputs - all commands return structured JSON

**When you need task/spec context before running fidelity review:**
- Use `mcp__plugin_foundry_foundry-mcp__task action="query" spec_id={spec-id} parent={phase-id}` to get all tasks in a phase
- Use `mcp__plugin_foundry_foundry-mcp__task action="query" spec_id={spec-id} status={status}` to filter by status
- Use `mcp__plugin_foundry_foundry-mcp__task action="info" spec_id={spec-id} task_id={task-id}` to get a single task's details
- Use `mcp__plugin_foundry_foundry-mcp__task action="list" spec_id={spec-id} include_phases=true` to see all phases

Then execute the fidelity review with the appropriate scope.

Your job is to execute the MCP tool and parse its JSON output.

The MCP tool handles:
- Loading and validating the specification
- Extracting task/phase requirements
- Analyzing implementation files
- Consulting AI tools (gemini, codex, cursor-agent) for deviation analysis
- Detecting consensus across multiple AI perspectives
- Categorizing deviations (exact match, minor, major, missing)
- Assessing impact levels
- Generating structured report

## Step 4: Parse and Present Results

The MCP tool returns JSON output with the structure:
```json
{
  "spec_id": "...",
  "review_type": "task|phase",
  "scope": {"id": "...", "title": "..."},
  "summary": {
    "tasks_reviewed": 0,
    "files_analyzed": 0,
    "deviations_found": 0,
    "fidelity_score": 0
  },
  "findings": [
    {
      "task_id": "...",
      "assessment": "exact_match|minor_deviation|major_deviation|missing",
      "deviations": [...],
      "impact": "low|medium|high",
      "ai_consensus": "..."
    }
  ],
  "recommendations": [...]
}
```

Parse this JSON, surface the structured findings directly to the invoking workflow, and include a link or path to the saved JSON report. The agent's responsibility is to faithfully relay the MCP tool's assessed deviations, recommendations, consensus signals, and metadata—perform validation/formatting as needed, but do not introduce any new analysis beyond what the tool returned. Do not open or read the saved artifact; simply point the caller to its location.
