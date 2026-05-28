---
name: machina-agent
description: Debug and trace MachinaMed medical agent errors in GKE environments. Use for investigating agent failures, tracing invocations, analyzing MALFORMED_FUNCTION_CALL errors, and generating comprehensive error reports from agent-trace.log files.
---

# Machina Agent Skill

Debug and trace errors in the MachinaMed medical agent system. This skill provides procedures for investigating agent failures, analyzing logs, and generating comprehensive error reports.

## When to Use This Skill

Use this skill when you need to:
- Investigate why user queries return empty responses
- Trace agent invocations from start to completion
- Analyze MALFORMED_FUNCTION_CALL or other LLM errors
- Generate comprehensive error reports from agent logs
- Debug agent routing issues (TriageAgent → HealthConsultantAgent)
- Investigate intermittent agent failures

## Agent Architecture Overview

### Agent Hierarchy

```
TusdiAI (ParallelAgent)
├── TriageAgent (LlmAgent) ← Routes user queries
│   ├── URLHandlerAgent (tool)
│   └── HealthConsultantAgent (SafeAgentTool)
│       └── query_graph, search_patient_data (tools)
└── ParallelDataExtractor (LlmAgent) ← Extracts health data from statements
```

### Key Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| TriageAgent | gemini-3-flash-preview | Routes queries to appropriate specialist |
| HealthConsultantAgent | gemini-3-pro-preview | Answers health questions using patient data |
| ParallelDataExtractor | gemini-3-flash-preview | Extracts symptoms, conditions from user statements |

### Agent Configuration Files

- `services/medical-agent/src/machina/medical_agent/agents/TriageAgent/config.yml`
- `services/medical-agent/src/machina/medical_agent/agents/HealthConsultantAgent/config.yml`
- `services/medical-agent/src/machina/medical_agent/agents/factory.py` - Agent creation logic

## GKE Log Access

### Prerequisites

Access to GKE clusters is through the **gcloud-admin** container. See `gcloud-admin/CLAUDE.md` for setup.

### Environment Mapping

| Environment | Namespace | Pod Pattern |
|-------------|-----------|-------------|
| tusdi-dev | tusdi-dev | tusdi-api-* |
| tusdi-staging | tusdi-staging | tusdi-api-* |
| tusdi-prod | tusdi-prod | tusdi-api-* |

### Accessing Agent Logs

Agent logs are written to files inside the pod, NOT to stdout. The primary log file is:

```
/app/logs/agent-trace.log
```

Older logs are compressed with timestamps:
```
/app/logs/agent-trace.log.2026-01-17.gz
/app/logs/agent-trace.log.2026-01-16.gz
```

### Step 1: Find the API Pod

```bash
# List pods in target namespace
just gcloud-admin::kubectl get pods -n tusdi-dev | grep tusdi-api

# Example output:
# tusdi-api-bc58677b8-fwxcd   1/1     Running   0          2d
```

### Step 2: Read Agent Trace Log

```bash
# Read current agent-trace.log
just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- cat /app/logs/agent-trace.log

# Read last 100 lines
just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- tail -100 /app/logs/agent-trace.log

# Search for specific error
just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- grep "MALFORMED_FUNCTION_CALL" /app/logs/agent-trace.log

# Read compressed historical logs
just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- zcat /app/logs/agent-trace.log.2026-01-17.gz | grep "ERROR"
```

### Step 3: Copy Logs Locally (for extensive analysis)

```bash
# Copy current log
just gcloud-admin::kubectl cp tusdi-dev/tusdi-api-bc58677b8-fwxcd:/app/logs/agent-trace.log ./agent-trace.log

# Copy compressed logs
just gcloud-admin::kubectl cp tusdi-dev/tusdi-api-bc58677b8-fwxcd:/app/logs/agent-trace.log.2026-01-17.gz ./agent-trace.log.2026-01-17.gz
```

## Log Format Reference

### Invocation Start

```
[timestamp] [INFO] invocation_started invocation_id="e-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### User Message

```
[timestamp] [INFO] user_message event_type="user_message" content="tell me about my cholesterol"
```

### Agent Lifecycle

```
[timestamp] [INFO] agent_starting agent_name="TriageAgent"
[timestamp] [INFO] agent_completed agent_name="TriageAgent"
```

### LLM Errors

```
[timestamp] [ERROR] LLM error response event_type="llm_response" agent="TriageAgent" error_code="MALFORMED_FUNCTION_CALL" error_message=""
```

### Response Yielded

```
[timestamp] [INFO] event_yielded author="TriageAgent" content_summary="..." content_length=1234 is_final_response=True
```

### Invocation End

```
[timestamp] [INFO] invocation_completed invocation_id="e-xxxxxxxx" duration_ms=6807
```

## Common Error Patterns

### MALFORMED_FUNCTION_CALL

**Symptoms:**
- User receives empty response
- HealthConsultantAgent never called
- `content_length=0` in final response

**Log Pattern:**
```
[ERROR] LLM error response agent="TriageAgent" error_code="MALFORMED_FUNCTION_CALL" error_message=""
[INFO] event_yielded author="TriageAgent" content_summary="None" content_length=0 is_final_response=True
```

**Root Cause:**
- `MALFORMED_FUNCTION_CALL` is a Gemini API FinishReason (NOT an ADK parsing error)
- TriageAgent lacks `tool_config` with constrained decoding mode
- In default/AUTO mode, model generates free-form text that can be syntactically invalid

**Investigation:**
1. Check if agent has `tool_config` with `FunctionCallingConfigMode.VALIDATED`
2. Look at `factory.py` for agent creation
3. Check `config.yml` for `generate_config` settings

**Fix:**
Add `FunctionCallingConfigMode.VALIDATED` to enable constrained decoding:
```python
generate_content_config=types.GenerateContentConfig(
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode=types.FunctionCallingConfigMode.VALIDATED
        )
    ),
    # ...existing config
)
```

### Empty Tool Response

**Symptoms:**
- Agent completes but returns no useful data
- `content_summary="None"` or empty string

**Investigation:**
1. Trace the full invocation to see which tools were called
2. Check if tool raised an exception
3. Verify tool has access to required data

### Agent Timeout

**Symptoms:**
- Invocation takes >30 seconds
- May result in gateway timeout (502)

**Investigation:**
1. Check `duration_ms` in invocation_completed
2. Look for slow tool calls (e.g., large graph queries)
3. Check for retry loops

## Generating Comprehensive Error Reports

When investigating agent errors, generate a comprehensive report following this template:

### Report Template

Create a file named `AGENT_TRACE_ERRORS_YYYYMMDD.md` in the machina-meta root with:

```markdown
# Agent Trace Errors Report - YYYY-MM-DD

**Environment:** [environment name] (GKE)
**Pod:** [pod name]
**Log files analyzed:**
- `/app/logs/agent-trace.log` (N lines, current)
- `/app/logs/agent-trace.log.YYYY-MM-DD.gz` (compressed)

---

## Summary

| Metric | Value |
|--------|-------|
| Total invocations analyzed | N |
| Total errors found | N |
| Error types | [list error codes] |
| Affected agent | [agent name] |
| Date range | YYYY-MM-DD to YYYY-MM-DD |

---

## Errors Table

| # | Timestamp | Agent | Error Code | Error Message | Invocation ID | User Query | Impact |
|---|-----------|-------|------------|---------------|---------------|------------|--------|
| 1 | timestamp | agent | ERROR_CODE | message | e-xxx | "query" | impact |

---

## Error #N: [timestamp]

**Location:** `/app/logs/agent-trace.log`

**Full invocation timeline:**

| Time | Event |
|------|-------|
| HH:MM:SS | User message: "query text" |
| HH:MM:SS | Invocation started |
| HH:MM:SS | [Agent] starting |
| HH:MM:SS | **ERROR: [error details]** |
| HH:MM:SS | Invocation completed (Nms) |

**Impact:**
- [Describe user impact]

**Log evidence:**
```
[paste relevant log lines]
```

---

## Root Cause Analysis

### Observations
1. [Pattern observed]
2. [Timing patterns]
3. [Affected components]

### Hypotheses
1. [Hypothesis 1]
2. [Hypothesis 2]

### Investigation Needed
- [ ] [Investigation item 1]
- [ ] [Investigation item 2]

---

## Recommendations

1. **Immediate:** [quick fix or mitigation]
2. **Short-term:** [proper fix]
3. **Long-term:** [architectural improvement]

---

**Report generated:** YYYY-MM-DDTHH:MM:SSZ
**Analyzed by:** [author]
```

### Report Generation Workflow

1. **Identify the error scope:**
   ```bash
   # Count errors by type
   just gcloud-admin::kubectl exec -n tusdi-dev [pod] -- grep -c "ERROR" /app/logs/agent-trace.log

   # List unique error codes
   just gcloud-admin::kubectl exec -n tusdi-dev [pod] -- grep "error_code" /app/logs/agent-trace.log | sort | uniq -c
   ```

2. **Extract affected invocations:**
   ```bash
   # Find invocation IDs with errors
   just gcloud-admin::kubectl exec -n tusdi-dev [pod] -- grep -B5 "ERROR" /app/logs/agent-trace.log | grep "invocation_id"
   ```

3. **Trace each failed invocation:**
   ```bash
   # Get full timeline for specific invocation
   just gcloud-admin::kubectl exec -n tusdi-dev [pod] -- grep "e-xxxxxxxx" /app/logs/agent-trace.log
   ```

4. **Identify user queries:**
   ```bash
   # Find user messages near errors
   just gcloud-admin::kubectl exec -n tusdi-dev [pod] -- grep -B10 "ERROR" /app/logs/agent-trace.log | grep "user_message"
   ```

5. **Analyze patterns:**
   - Group errors by time of day
   - Identify common query patterns
   - Check for model/agent correlations

6. **Document in PROBLEMS.md:**
   - Create entry with [OPEN] status
   - Include severity (CRITICAL/HIGH/MEDIUM/LOW)
   - Reference the error report

7. **Create TODO.md task:**
   - Add [PROPOSED] task for fix
   - Include root cause analysis
   - List investigation steps

## Useful Grep Patterns

```bash
# All errors
grep "\[ERROR\]" agent-trace.log

# Specific error code
grep "MALFORMED_FUNCTION_CALL" agent-trace.log

# Failed invocations (empty responses)
grep "content_length=0.*is_final_response=True" agent-trace.log

# Slow invocations (>10 seconds)
grep "duration_ms=[0-9]\{5,\}" agent-trace.log

# Specific agent errors
grep "agent=\"TriageAgent\".*ERROR" agent-trace.log

# User queries (for context)
grep "user_message" agent-trace.log

# Invocation timeline (replace ID)
grep "e-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" agent-trace.log
```

## Related Documentation

- [docs/MULTI_AGENT_ARCHITECTURE.md](../../../docs/MULTI_AGENT_ARCHITECTURE.md) - Agent architecture documentation
- [PROBLEMS.md](../../../repos/dem2/PROBLEMS.md) - Known issues and investigations
- [TODO.md](../../../repos/dem2/TODO.md) - Planned fixes
- [gcloud-admin/CLAUDE.md](../../../gcloud-admin/CLAUDE.md) - GKE access setup

## Example: Complete Error Investigation

### Scenario: User reports "query hanging"

1. **Get pod name:**
   ```bash
   just gcloud-admin::kubectl get pods -n tusdi-dev | grep tusdi-api
   # tusdi-api-bc58677b8-fwxcd
   ```

2. **Search for recent errors:**
   ```bash
   just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- \
     grep "ERROR" /app/logs/agent-trace.log | tail -20
   ```

3. **Find the user's query:**
   ```bash
   just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- \
     grep -B5 "ERROR" /app/logs/agent-trace.log | grep "user_message"
   ```

4. **Trace full invocation:**
   ```bash
   just gcloud-admin::kubectl exec -n tusdi-dev tusdi-api-bc58677b8-fwxcd -- \
     grep "e-20e9bc1d-4d7c-4b0f-a501-2ae0f909785d" /app/logs/agent-trace.log
   ```

5. **Analyze and document:**
   - Create error report in `AGENT_TRACE_ERRORS_YYYYMMDD.md`
   - Add to PROBLEMS.md with [OPEN] status
   - Create TODO.md task with [PROPOSED] fix

## Skill Metadata

- **Version:** 1.0.0
- **Created:** 2026-01-19
- **Workspace:** machina-meta
- **Scope:** Medical agent debugging, error tracing, report generation
