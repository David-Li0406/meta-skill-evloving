# Skill Creation Process: Step-by-Step Guide

> **Use this guide** to systematically build a new Claude Code skill following progressive disclosure principles and token optimization.

**Example Used**: `incident-triage` skill (adapt for your use case)

---

## 📋 Process Overview

```
Phase 1: Planning → Phase 2: Structure → Phase 3: Implementation → Phase 4: Testing → Phase 5: Refinement
   (30 min)           (15 min)              (2-4 hours)              (30 min)          (ongoing)
```

---

## Phase 1: Planning (30 minutes)

### Step 1.1: Define the Core Problem

**Questions to answer:**
- [ ] What specific, repeatable task does this solve?
- [ ] When should Claude invoke this skill?
- [ ] What are the inputs and outputs?
- [ ] What's the 1-sentence description?

**Example (incident-triage):**
- **Task**: Triage incidents by extracting facts, enriching with data, proposing severity/priority
- **Triggers**: "triage", "new incident", "assign severity", "prioritize ticket"
- **Inputs**: Free text or JSON ticket payload
- **Outputs**: Summary, severity/priority, next steps, assignment hint
- **Description**: "Triage incidents by extracting key facts, enriching with CMDB/log data, and proposing severity, priority, and next actions."

### Step 1.2: Identify the Three Levels

**Level 1: Metadata** (~100 tokens, always loaded)
- [ ] Skill name (kebab-case)
- [ ] Description (triggers Claude's router)
- [ ] Version

**Level 2: SKILL.md Body** (<2k tokens, loaded on trigger)
- [ ] When to Use (2-3 bullet points)
- [ ] What It Does (high-level flow)
- [ ] Inputs/Outputs (contract)
- [ ] Quick Start (1-3 commands)
- [ ] Links to Level 3 docs

**Level 3: Bundled Files** (unlimited, loaded as-needed)
- [ ] Detailed documentation
- [ ] Executable scripts
- [ ] API specs, examples, decision matrices
- [ ] Shared utilities

### Step 1.3: Token Budget Plan

Fill out this table:

| Component | Target Tokens | What Goes Here |
|-----------|--------------|----------------|
| Metadata | ~100 | Name, description, version |
| SKILL.md Body | <2k (aim for 1.5k) | Quick ref, links to Level 3 |
| reference/*.md | 500-1000 each | Detailed docs (as many files as needed) |
| scripts/*.py | n/a | Executable code (not loaded unless run) |

---

## Phase 2: Structure (15 minutes)

### Step 2.1: Create Folder Layout

**⚠️ CRITICAL: Create `/reference/` folder and put ALL reference .md files there!**

```bash
# Navigate to skills directory
cd .claude/skills

# Create skill structure
mkdir -p incident-triage/{scripts,reference,shared}
touch incident-triage/SKILL.md
touch incident-triage/scripts/{triage_main.py,enrich_ticket.py,suggest_priority.py,common.py}
touch incident-triage/reference/{inputs-and-prompts.md,decision-matrix.md,runbook-links.md,api-specs.md,examples.md}
touch incident-triage/shared/{config.py,api_client.py,formatters.py}
```

**Verify structure matches this EXACT pattern:**
```
incident-triage/
├── SKILL.md                  # ✅ Level 1+2 (≤2k tokens) - ONLY .md in root
├── reference/                # ✅ REQUIRED: Level 3 docs folder
│   ├── inputs-and-prompts.md #    ✅ All reference .md files go HERE
│   ├── decision-matrix.md    #    ✅ NOT in root!
│   ├── runbook-links.md
│   ├── api-specs.md
│   └── examples.md
├── scripts/                  # Level 3: executable code
│   ├── triage_main.py
│   ├── enrich_ticket.py
│   ├── suggest_priority.py
│   └── common.py
└── shared/                   # Level 3: utilities
    ├── config.py
    ├── api_client.py
    └── formatters.py
```

**❌ WRONG - DO NOT DO THIS:**
```
incident-triage/
├── SKILL.md
├── inputs-and-prompts.md     # ❌ WRONG! Should be in reference/
├── decision-matrix.md         # ❌ WRONG! Should be in reference/
└── scripts/
```

### Step 2.2: Stub Out Files

Create minimal stubs for each file to establish contracts:

**SKILL.md** (copy template from best-practices.md)
**reference/*.md** (headers only for now)
**scripts/*.py** (function signatures with pass)
**shared/*.py** (class/function signatures)

### Step 2.3: Validate Folder Structure

**Run this validation BEFORE moving to Phase 3:**

```bash
# Check structure
ls -la incident-triage/

# Verify:
# ✅ SKILL.md exists in root
# ✅ reference/ folder exists
# ✅ NO .md files in root except SKILL.md
# ✅ scripts/ folder exists (if needed)
# ✅ shared/ folder exists (if needed)

# Check reference folder
ls -la incident-triage/reference/

# Verify:
# ✅ All .md reference files are HERE
# ✅ inputs-and-prompts.md
# ✅ decision-matrix.md
# ✅ api-specs.md
# ✅ examples.md
```

**Checklist:**
- [ ] `/reference/` folder created
- [ ] All reference .md files in `/reference/` (not root)
- [ ] SKILL.md links use `./reference/filename.md` format
- [ ] No .md files in root except SKILL.md

---

## Phase 3: Implementation (2-4 hours)

Work in this order to maintain focus and avoid scope creep:

### Step 3.1: Write Level 1 (Metadata) - 5 minutes

Open `SKILL.md` and write the frontmatter:

```yaml
---
name: incident-triage
description: Triage incidents by extracting key facts, enriching with CMDB/log data, and proposing severity, priority, and next actions.
version: 1.0.0
---
```

**Checklist:**
- [ ] Name is clear and specific (not "helper" or "utility")
- [ ] Description contains trigger keywords
- [ ] Description explains what it does (not what it is)
- [ ] Total metadata ≤100 tokens

### Step 3.2: Write Level 2 (SKILL.md Body) - 30 minutes

Follow this exact structure:

```markdown
# Level 2: Body (<2k tokens recommended) — Loaded when the skill triggers

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

## What It Does (at a glance)
- **[Action 1]**: [brief description]
- **[Action 2]**: [brief description]
- **[Action 3]**: [brief description]
- **[Action 4]**: [brief description]

## Inputs
- [Input format 1]
- [Input format 2]

Details: see [reference/inputs-and-prompts.md](./reference/inputs-and-prompts.md).

## Quick Start
1. **Dry-run** (no external calls):
   ```bash
   python scripts/main.py --example --dry-run
   ```

2. **With enrichment**:
   ```bash
   python scripts/main.py --ticket-id 12345 --include-logs
   ```

3. Review output

Examples: [reference/examples.md](./reference/examples.md)

## Decision Logic (high-level)
[2-3 sentences on how decisions are made]

Full details: [reference/decision-matrix.md](./reference/decision-matrix.md)

## Outputs (contract)
- `field1`: [description]
- `field2`: [description]
- `field3`: [description]

## Guardrails
- [Security consideration 1]
- [Token budget note]
- [Error handling approach]

## Links (Level 3, loaded only when needed)
- Prompts: [reference/inputs-and-prompts.md](./reference/inputs-and-prompts.md)
- Decision logic: [reference/decision-matrix.md](./reference/decision-matrix.md)
- Examples: [reference/examples.md](./reference/examples.md)
- API specs: [reference/api-specs.md](./reference/api-specs.md)

## Triggers (help the router)
Keywords: [keyword1], [keyword2], [keyword3]
Inputs containing: [field1], [field2]

## Security & Config
Set environment variables:
- `VAR1_API_KEY`
- `VAR2_API_KEY`

Centralized in `shared/config.py`. Never echo secrets.

## Testing
```bash
# Smoke test
python scripts/main.py --fixture reference/examples.md

# End-to-end
python scripts/main.py --text "Example input" --dry-run
```
```

**Checklist:**
- [ ] <2k tokens (aim for 1.5k)
- [ ] Links to Level 3 for details
- [ ] Quick Start is copy-paste ready
- [ ] Output contract is clear
- [ ] No extensive examples or specs embedded

### Step 3.3: Write Level 3 Reference Docs - 45 minutes

Create each reference file systematically:

#### reference/inputs-and-prompts.md
```markdown
# Inputs and Prompt Shapes

## Input Format 1: Free Text
- Description
- Example

## Input Format 2: Structured JSON
```json
{
  "field": "value"
}
```

## Prompt Snippets
- Extraction goals
- Summarization style
- Redaction rules
```

#### reference/decision-matrix.md
```markdown
# Decision Matrix

[Full decision logic with tables, formulas, edge cases]

## Base Matrix
| Dimension 1 \ Dimension 2 | Value A | Value B | Value C |
|---|---|---|---|
| Low  | Result | Result | Result |
| Med  | Result | Result | Result |
| High | Result | Result | Result |

## Adjustments
- Adjustment rule 1
- Adjustment rule 2

## Rationale
[Why this matrix, examples, edge cases]
```

#### reference/api-specs.md
```markdown
# API Specs & Schemas

## API 1: CMDB
- Base URL: `{SERVICE_MAP_URL}`
- Auth: Header `X-API-Key: {CMDB_API_KEY}`
- Endpoints:
  - GET `/service/{name}/dependencies`
  - Response schema: [...]

## API 2: Logs
- Base URL: [...]
- Endpoints: [...]
```

#### reference/examples.md
```markdown
# Examples

## Example 1: [Scenario Name]
**Input:**
```
[Example input]
```

**Output:**
```
[Example output with all fields]
```

**Explanation:** [Why these decisions were made]

## Example 2: [Another Scenario]
[...]
```

#### reference/runbook-links.md
```markdown
# Runbook Links

- [Service 1]: <URL>
- [Service 2]: <URL>
- [Escalation tree]: <URL>
```

**Checklist for all reference docs:**
- [ ] Each file focuses on one aspect
- [ ] 500-1000 tokens per file (can be more if needed)
- [ ] Referenced from SKILL.md but not embedded
- [ ] Includes examples where helpful

### Step 3.4: Write Shared Utilities - 30 minutes

#### shared/config.py
```python
"""Centralized configuration from environment variables."""
import os

class Config:
    """Config object - never logs secrets"""
    CMDB_API_KEY = os.getenv("CMDB_API_KEY")
    LOGS_API_KEY = os.getenv("LOGS_API_KEY")
    SERVICE_MAP_URL = os.getenv("SERVICE_MAP_URL")
    DASHBOARD_BASE_URL = os.getenv("DASHBOARD_BASE_URL")

    @classmethod
    def validate(cls):
        """Check required env vars are set"""
        missing = []
        for key in ["CMDB_API_KEY", "LOGS_API_KEY"]:
            if not getattr(cls, key):
                missing.append(key)
        if missing:
            raise ValueError(f"Missing required env vars: {missing}")

cfg = Config()
```

#### shared/api_client.py
```python
"""API client wrappers."""
import requests
from .config import cfg

class CMDBClient:
    def __init__(self):
        self.base_url = cfg.SERVICE_MAP_URL
        self.headers = {"X-API-Key": cfg.CMDB_API_KEY}

    def get_service_dependencies(self, service_name):
        """Fetch service dependencies"""
        try:
            resp = requests.get(
                f"{self.base_url}/service/{service_name}/dependencies",
                headers=self.headers,
                timeout=5
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"CMDB API failed: {e}")

class LogsClient:
    def __init__(self):
        self.base_url = cfg.LOGS_API_URL
        self.headers = {"Authorization": f"Bearer {cfg.LOGS_API_KEY}"}

    def recent_errors(self, service_name, last_minutes=15):
        """Fetch recent error logs"""
        # Implementation
        pass

def cmdb_client():
    return CMDBClient()

def logs_client():
    return LogsClient()
```

#### shared/formatters.py
```python
"""Output formatting helpers."""

def format_output(enriched, severity, priority, rationale, next_steps):
    """Format triage result as markdown."""
    lines = [
        "### Incident Triage Result",
        f"**Severity**: {severity} | **Priority**: {priority}",
        f"**Rationale**: {rationale}",
        "",
        "**Summary**:",
        enriched.get("summary", "N/A"),
        "",
        "**Next Steps**:",
    ]
    for i, step in enumerate(next_steps, 1):
        lines.append(f"{i}. {step}")

    if "evidence" in enriched:
        lines.extend(["", "**Evidence**:"])
        for link in enriched["evidence"]:
            lines.append(f"- {link}")

    return "\n".join(lines)
```

### Step 3.5: Write Main Scripts - 1 hour

#### scripts/triage_main.py (entry point)
```python
#!/usr/bin/env python3
"""Main entry point for incident triage."""
import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config import cfg
from shared.formatters import format_output
from scripts.enrich_ticket import enrich
from scripts.suggest_priority import score

def main():
    parser = argparse.ArgumentParser(description="Triage an incident")
    parser.add_argument("--text", help="Free-text incident description")
    parser.add_argument("--ticket-id", help="Ticket ID to enrich")
    parser.add_argument("--include-logs", action="store_true")
    parser.add_argument("--include-cmdb", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                       help="Skip external API calls")
    args = parser.parse_args()

    # Validate inputs
    if not args.text and not args.ticket_id:
        print("Error: Provide --text or --ticket-id")
        sys.exit(1)

    # Build payload
    payload = {
        "text": args.text,
        "ticket_id": args.ticket_id
    }

    try:
        # Enrich (respects --dry-run)
        enriched = enrich(
            payload,
            include_logs=args.include_logs and not args.dry_run,
            include_cmdb=args.include_cmdb and not args.dry_run
        )

        # Score (deterministic)
        severity, priority, rationale = score(enriched)

        # Generate next steps
        next_steps = generate_next_steps(enriched, severity)

        # Format output
        output = format_output(enriched, severity, priority, rationale, next_steps)
        print(output)

    except Exception as e:
        print(f"❌ Triage failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check environment variables are set")
        print("2. Verify API endpoints are accessible")
        print("3. Run with --dry-run to test without external calls")
        sys.exit(1)

def generate_next_steps(enriched, severity):
    """Generate action items based on enrichment and severity"""
    steps = []

    if severity in ["SEV1", "SEV2"]:
        steps.append("Page on-call immediately")

    if "dashboard_url" in enriched:
        steps.append(f"Review dashboard: {enriched['dashboard_url']}")

    steps.append("Compare last 15m vs 24h baseline")

    if enriched.get("recent_deploy"):
        steps.append("Consider rollback if error budget breached")

    return steps

if __name__ == "__main__":
    main()
```

#### scripts/enrich_ticket.py
```python
"""Enrich ticket with external data."""
from shared.config import cfg
from shared.api_client import cmdb_client, logs_client

def enrich(payload, include_logs=False, include_cmdb=False):
    """
    Enrich ticket payload with CMDB/logs data.

    Args:
        payload: Dict with 'text' and/or 'ticket_id'
        include_logs: Fetch recent logs
        include_cmdb: Fetch CMDB dependencies

    Returns:
        Dict with original payload + enrichment
    """
    result = {"input": payload}

    # Extract service name from text or ticket
    service = extract_service(payload)
    if service:
        result["service"] = service

    # Enrich with CMDB
    if include_cmdb and service:
        try:
            cmdb_data = cmdb_client().get_service_dependencies(service)
            result["cmdb"] = cmdb_data
            result["blast_radius"] = cmdb_data.get("dependent_services", [])
        except Exception as e:
            result["cmdb_error"] = str(e)

    # Enrich with logs
    if include_logs and service:
        try:
            logs = logs_client().recent_errors(service)
            result["logs"] = logs
        except Exception as e:
            result["logs_error"] = str(e)

    # Derive scope/impact hints
    result["scope"] = derive_scope(result)
    result["impact"] = derive_impact(result)

    return result

def extract_service(payload):
    """Extract service name from payload."""
    # Check explicit service field
    if "service" in payload:
        return payload["service"]

    # Parse from text (simple keyword matching)
    text = payload.get("text", "").lower()
    known_services = ["checkout", "payments", "inventory", "auth"]
    for service in known_services:
        if service in text:
            return service

    return None

def derive_scope(enriched):
    """Determine blast radius scope."""
    blast_radius = len(enriched.get("blast_radius", []))
    if blast_radius == 0:
        return "single-service"
    elif blast_radius < 3:
        return "few-services"
    else:
        return "multi-service"

def derive_impact(enriched):
    """Estimate user impact level."""
    # Check for explicit impact data
    if "impact" in enriched.get("input", {}):
        pct = enriched["input"]["impact"].get("users_affected_pct", 0)
        if pct > 50:
            return "high"
        elif pct > 10:
            return "medium"
        else:
            return "low"

    # Infer from service criticality
    service = enriched.get("service", "")
    critical_services = ["checkout", "payments", "auth"]
    if service in critical_services:
        return "medium"  # Default to medium for critical services

    return "low"
```

#### scripts/suggest_priority.py
```python
"""Deterministic severity/priority scoring."""

DECISION_MATRIX = {
    # (impact, scope) -> (severity, priority)
    ("low", "single-service"): ("SEV4", "P4"),
    ("low", "few-services"): ("SEV3", "P3"),
    ("low", "multi-service"): ("SEV3", "P3"),
    ("medium", "single-service"): ("SEV3", "P3"),
    ("medium", "few-services"): ("SEV2", "P2"),
    ("medium", "multi-service"): ("SEV2", "P2"),
    ("high", "single-service"): ("SEV2", "P2"),
    ("high", "few-services"): ("SEV1", "P1"),
    ("high", "multi-service"): ("SEV1", "P1"),
}

def score(enriched):
    """
    Score incident severity and priority.

    Args:
        enriched: Dict from enrich_ticket()

    Returns:
        Tuple of (severity, priority, rationale)
    """
    impact = enriched.get("impact", "medium")
    scope = enriched.get("scope", "single-service")

    # Base score from matrix
    key = (impact, scope)
    if key not in DECISION_MATRIX:
        # Default fallback
        severity, priority = "SEV3", "P3"
        rationale = f"Default scoring (impact={impact}, scope={scope})"
    else:
        severity, priority = DECISION_MATRIX[key]
        rationale = f"{impact.title()} impact, {scope} scope"

    # Apply adjustments
    if should_escalate(enriched):
        severity, priority = escalate(severity, priority)
        rationale += " (escalated: long recovery expected)"

    return severity, priority, rationale

def should_escalate(enriched):
    """Check if incident should be escalated."""
    # Check for long recovery indicators
    logs = enriched.get("logs", {})
    if logs.get("error_rate_increasing"):
        return True

    # Check for repeated incidents
    if enriched.get("recent_incidents_count", 0) > 3:
        return True

    return False

def escalate(severity, priority):
    """Escalate severity/priority by one level."""
    sev_map = {"SEV4": "SEV3", "SEV3": "SEV2", "SEV2": "SEV1", "SEV1": "SEV1"}
    pri_map = {"P4": "P3", "P3": "P2", "P2": "P1", "P1": "P1"}
    return sev_map.get(severity, severity), pri_map.get(priority, priority)
```

---

## Phase 4: Testing (30 minutes)

### Step 4.1: Create Test Fixtures

Create `reference/test-fixtures.json`:
```json
{
  "test1": {
    "text": "Checkout API seeing 500 errors at 12%; started 15:05Z",
    "expected_severity": "SEV2",
    "expected_priority": "P2"
  },
  "test2": {
    "text": "Single user reports login issue on mobile app",
    "expected_severity": "SEV4",
    "expected_priority": "P4"
  }
}
```

### Step 4.2: Run Tests

```bash
# 1. Smoke test deterministic components
python scripts/suggest_priority.py --test

# 2. Dry-run end-to-end
python scripts/triage_main.py --text "API timeouts on checkout" --dry-run

# 3. With enrichment (requires env vars)
export CMDB_API_KEY="test_key"
export LOGS_API_KEY="test_key"
python scripts/triage_main.py --ticket-id 12345 --include-logs --include-cmdb
```

### Step 4.3: Test with Claude

Ask Claude:
```
"I have a new incident: checkout API showing 500 errors affecting 15% of users in EU region. Can you triage this?"
```

Verify:
- [ ] Skill triggers correctly
- [ ] Output is well-formatted
- [ ] Severity/priority makes sense
- [ ] Next steps are actionable
- [ ] Links work

---

## Phase 5: Refinement (Ongoing)

### Step 5.1: Token Count Audit

```bash
# Count tokens in SKILL.md body (exclude metadata)
wc -w incident-triage/SKILL.md
# Multiply by 0.75 for rough token count
```

**Checklist:**
- [ ] Metadata ~100 tokens
- [ ] Body <2k tokens
- [ ] If over, move content to reference/*.md

### Step 5.2: Real-World Usage Monitoring

Track these metrics:
- [ ] Does Claude trigger the skill appropriately?
- [ ] Are users getting helpful results?
- [ ] What questions/errors come up?
- [ ] Which Level 3 docs are never used?

### Step 5.3: Iterate Based on Feedback

**If skill triggers too often:**
→ Make description more specific

**If skill triggers too rarely:**
→ Add more trigger keywords

**If output is unhelpful:**
→ Improve decision logic or examples

**If token limit exceeded:**
→ Move more content to Level 3

---

## 🎓 Adaptation Checklist

To create YOUR skill from this template:

- [ ] **Folder Structure** (CRITICAL):
  - [ ] Create `/reference/` folder
  - [ ] Put ALL reference .md files IN `/reference/` folder
  - [ ] NO .md files in root except SKILL.md
  - [ ] Links in SKILL.md use `./reference/filename.md` format
- [ ] **Rename**: Replace "incident-triage" with your skill name
- [ ] **Metadata**: Write name/description with your trigger keywords
- [ ] **Triggers**: List all keywords/patterns that should invoke your skill
- [ ] **Inputs/Outputs**: Define your specific contract
- [ ] **Scripts**: Replace enrichment/scoring with your logic
- [ ] **Reference docs**: Create docs for your domain (decision matrices, API specs, etc.)
- [ ] **Config**: Add your required environment variables
- [ ] **Examples**: Create 3-5 realistic examples
- [ ] **Test**: Dry-run → with real data → with Claude
- [ ] **Validate Structure**: Run structure validation checklist
- [ ] **Refine**: Monitor usage, iterate based on feedback

---

## 📚 Related Resources

- [Quick Reference](./quick-reference.md) - Best practices at a glance
- [Progressive Disclosure](./progressive-disclosure.md) - Design philosophy
- [Philosophy Guide](./philosophy.md) - Token optimization explained

---

**Last Updated**: 2025-10-20
**Version**: 1.0.0
