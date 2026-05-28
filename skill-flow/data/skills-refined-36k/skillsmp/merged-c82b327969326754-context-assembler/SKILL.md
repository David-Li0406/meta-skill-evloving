---
name: context-assembler
description: Assembles relevant context for agent spawns with prioritized ranking, enforcing token budgets and capturing error patterns for learning.
---

# Context-Assembler Skill

You are the context-assembler skill. When invoked, you assemble relevant context packages for agent spawns, prioritizing by relevance and respecting token budgets.

## When to Invoke This Skill

**Invoke this skill when:**
- Orchestrator prepares to spawn an agent and needs relevant context.
- Any agent mentions "assemble context", "get context packages", or "context-assembler".
- Preparing developer/QA/tech lead spawns with session context.
- Need to check for relevant error patterns before agent spawn.

**Do NOT invoke when:**
- No active orchestration session exists.
- Manually reading specific files (use Read tool directly).
- Working outside BAZINGA orchestration.

---

## Your Task

When invoked, execute these steps in order:

### Step 1: Determine Context Parameters

Extract from the calling request or infer from conversation:
- `session_id`: Current orchestration session (REQUIRED).
- `group_id`: Task group being processed (OPTIONAL - use empty string "" if not provided).
- `agent_type`: Target agent - developer/senior_software_engineer/qa_expert/tech_lead/investigator (REQUIRED).
- `model`: Model being used - haiku/sonnet/opus or full model ID (OPTIONAL, for token budgeting).
- `current_tokens`: Current token usage in conversation (OPTIONAL, for zone detection).
- `iteration`: Current iteration number (optional, default 0).
- `include_reasoning`: Whether to include prior agent reasoning for handoff (OPTIONAL).
  - **DEFAULT BEHAVIOR:** Automatically `true` when reasoning context is beneficial:
    - `qa_expert`, `tech_lead`: ALWAYS (handoff recipients).
    - `senior_software_engineer`: ALWAYS (escalation needs prior context).
    - `investigator`: ALWAYS (debugging needs full context).
    - `developer`: When `iteration > 0` (retry needs prior reasoning; first attempt has none).
  - Explicitly set to `false` to disable reasoning for any agent.
- `reasoning_level`: Level of detail for reasoning retrieval (OPTIONAL).
  - `minimal`: 400 tokens - key decisions only.
  - `medium`: 800 tokens - decisions + approach (DEFAULT).
  - `full`: 1200 tokens - complete reasoning chain.

If `session_id` or `agent_type` are missing, check recent conversation context or ask the orchestrator.

### Step 2: Load Configuration and Check FTS5

**Step 2a: Load retrieval limit for this agent type:**

```bash
# Extract retrieval limit for the specific agent type
AGENT_TYPE="developer"  # Replace with actual agent_type

# Pass AGENT_TYPE via command-line argument (not string interpolation)
LIMIT=$(cat bazinga/skills_config.json 2>/dev/null | python3 -c "
import sys, json
agent = sys.argv[1] if len(sys.argv) > 1 else 'developer'
defaults = {'developer': 3, 'senior_software_engineer': 5, 'qa_expert': 5, 'tech_lead': 5, 'investigator': 5}
try:
    c = json.load(sys.stdin).get('context_engineering', {})
    limits = c.get('retrieval_limits', {})
    print(limits.get(agent, defaults.get(agent, 3)))
except:
    print(defaults.get(agent, 3))
" "$AGENT_TYPE" 2>/dev/null || echo 3)
echo "Retrieval limit for $AGENT_TYPE: $LIMIT"
```

Default limits: developer=3, senior_software_engineer=5, qa_expert=5, tech_lead=5, investigator=5.

**Step 2b: FTS5 availability:**

FTS5 is assumed unavailable (requires special SQLite build). Always use heuristic fallback in Step 3b for ranking.

```bash
# FTS5 disabled by default - use heuristic ranking
FTS5_AVAILABLE="false"
echo "FTS5_AVAILABLE=$FTS5_AVAILABLE (heuristic fallback enabled)"
```

**Step 2c: Determine token zone and budget:**

```bash
# Token estimation with tiktoken (with fallback to character estimation)
# Input: MODEL, CURRENT_TOKENS (from Step 1)
MODEL="sonnet"  # or "haiku", "opus", or full model ID
CURRENT_TOKENS=0  # Current usage if known, else 0

# IMPORTANT: Use eval to capture output as shell variables
eval "$(python3 -c "
import sys, json

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

# Model context limits (conservative estimates)
MODEL_LIMITS = {
    'haiku': 200000, 'claude-3-5-haiku': 200000,
    'sonnet': 200000, 'claude-sonnet-4-20250514': 200000, 'claude-3-5-sonnet': 200000,
    'opus': 200000, 'claude-opus-4-20250514': 200000
}

# Read safety margin from config (default 15%)
try:
    with open('bazinga/skills_config.json') as f:
        cfg = json.load(f).get('context_engineering', {})
        SAFETY_MARGIN = cfg.get('token_safety_margin', 0.15)
except:
    SAFETY_MARGIN = 0.15

model = sys.argv[1] if len(sys.argv) > 1 else 'sonnet'
current = int(sys.argv[2]) if len(sys.argv) > 2 else 0

# Normalize model name (longest key first to avoid partial matches)
model_key = model.lower()
for key in sorted(MODEL_LIMITS.keys(), key=len, reverse=True):
    if key in model_key:
        model_key = key
        break

limit = MODEL_LIMITS.get(model_key, 200000)
effective_limit = int(limit * (1 - SAFETY_MARGIN))

# Calculate REMAINING budget (not total)
remaining_budget = max(0, effective_limit - current)
usage_pct = (current / effective_limit * 100) if effective_limit > 0 else 0

# Determine zone
if usage_pct >= 95:
    zone = 'Emergency'
elif usage_pct >= 85:
    zone = 'Wrap-up'
elif usage_pct >= 75:
    zone = 'Conservative'
elif usage_pct >= 60:
    zone = 'Soft_Warning'  # Underscore for shell variable safety
else:
    zone = 'Normal'

# Output as shell variable assignments (will be eval'd)
print(f'ZONE={zone}')
print(f'USAGE_PCT={usage_pct:.1f}')
print(f'EFFECTIVE_LIMIT={effective_limit}')
print(f'REMAINING_BUDGET={remaining_budget}')
print(f'HAS_TIKTOKEN={HAS_TIKTOKEN}')
" "$MODEL" "$CURRENT_TOKENS")"

# Now $ZONE, $USAGE_PCT, $EFFECTIVE_LIMIT, $REMAINING_BUDGET, $HAS_TIKTOKEN are set
echo "Zone: $ZONE, Usage: $USAGE_PCT%, Remaining: $REMAINING_BUDGET tokens"
```

**Token Zone Behaviors:**

| Zone | Usage % | Behavior |
|------|---------|----------|
| Normal | 0-60% | Full context with all packages |
| Soft Warning | 60-75% | Prefer summaries over full content |
| Conservative | 75-85% | Minimal context, critical packages only |
| Wrap-up | 85-95% | Essential info only, no new packages |
| Emergency | 95%+ | Return immediately, suggest checkpoint |

**Token Budget Allocation by Agent Type:**

| Agent | Task | Specialization | Context Pkgs | Errors |
|-------|------|----------------|--------------|--------|
| developer | 50% | 20% | 20% | 10% |
| senior_software_engineer | 40% | 20% | 25% | 15% |
| qa_expert | 40% | 15% | 30% | 15% |
| tech_lead | 30% | 15% | 40% | 15% |
| investigator | 35% | 15% | 35% | 15% |

**Note:** SSE and Investigator handle escalations/complex debugging, so they need more context and error budget.

### Step 3: Query Context Packages (Zone-Conditional)

**CRITICAL: Execute query based on zone from Step 2c**

The query behavior depends entirely on the zone. Use this conditional structure:

```bash
# Zone-conditional query execution
# Variables from previous steps: $ZONE, $SESSION_ID, $GROUP_ID, $AGENT_TYPE, $LIMIT, $REMAINING_BUDGET

# Initialize result variable
QUERY_RESULT=""

if [ "$ZONE" = "Emergency" ]; then
    # Emergency zone: Skip all queries, go directly to Step 5
    echo "ZONE=Emergency: Skipping context query, proceeding to emergency output"
    QUERY_RESULT='{"packages":[],"total_available":0,"zone_skip":true}'

elif [ "$ZONE" = "Wrap-up" ]; then
    # Wrap-up zone: Skip context packages, minimal output only
    echo "ZONE=Wrap-up: Skipping context packages"
    QUERY_RESULT='{"packages":[],"total_available":0,"zone_skip":true}'

elif [ "$ZONE" = "Conservative" ]; then
    # Conservative zone: Priority fallback with LIMIT items across buckets
    echo "ZONE=Conservative: Using priority fallback ladder via bazinga-db"

    # Use bazinga-db get-context-packages command for each priority level
    QUERY_RESULT=$(python3 -c "
import subprocess
import json
import sys
import time

session_id = sys.argv[1]
group_id = sys.argv[2]
limit = int(sys.argv[3])
agent_type = sys.argv[4] if len(sys.argv) > 4 else 'developer'

def db_cmd_with_retry(cmd_args, max_retries=3, backoff_ms=[100, 250, 500]):
    '''Execute bazinga-db command with retry on database busy.'''
    for attempt in range(max_retries + 1):
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout) if result.stdout.strip() else []
            except json.JSONDecodeError:
                # Surface error rather than silently returning empty
                sys.stderr.write(f'JSON decode error: {result.stdout[:100]}\\n')
                return []
        if 'database is locked' in result.stderr or 'SQLITE_BUSY' in result.stderr:
            if attempt < max_retries:
                time.sleep(backoff_ms[attempt] / 1000.0)
                continue
        # Surface command errors
        if result.stderr:
            sys.stderr.write(f'Command error: {result.stderr[:200]}\\n')
        return []
    return []

# Priority fallback: Use bazinga-db to fetch packages by priority
# The get-context-packages command handles priority ordering internally
collected = db_cmd_with_retry([
    'python3', '.claude/skills/bazinga-db/scripts/bazinga_db.py', '--quiet',
    'get-context-packages', session_id, group_id, agent_type, str(limit)
])

# Handle result format
if isinstance(collected, dict):
    packages = collected.get('packages', [])
    total_available = collected.get('total_available', len(packages))
elif isinstance(collected, list):
    packages = collected
    total_available = len(packages)
else:
    packages = []
    total_available = 0

print(json.dumps({'packages': packages, 'total_available': total_available}))
" "$SESSION_ID" "$GROUP_ID" "$LIMIT" "$AGENT_TYPE")

else
    # Normal or Soft_Warning zone: Standard query
    echo "ZONE=$ZONE: Standard query with LIMIT=$LIMIT"
    QUERY_RESULT=$(python3 -c "
import subprocess
import json
import sys
import time

session_id = sys.argv[1]
group_id = sys.argv[2]
agent_type = sys.argv[3]
limit = int(sys.argv[4])

def db_query_with_retry(cmd_args, max_retries=3, backoff_ms=[100, 250, 500]):
    for attempt in range(max_retries + 1):
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout) if result.stdout.strip() else []
            except json.JSONDecodeError:
                return []
        if 'SQLITE_BUSY' in result.stderr or 'database is locked' in result.stderr:
            if attempt < max_retries:
                time.sleep(backoff_ms[attempt] / 1000.0)
                continue
        return []
    return []

# Use bazinga-db get-context-packages (parameterized, safe)
result = db_query_with_retry([
    'python3', '.claude/skills/bazinga-db/scripts/bazinga_db.py', '--quiet',
    'get-context-packages', session_id, group_id, agent_type, str(limit)
])

# If result is dict with 'packages' key, use it; otherwise wrap
if isinstance(result, dict):
    print(json.dumps(result))
elif isinstance(result, list):
    print(json.dumps({'packages': result, 'total_available': len(result)}))
else:
    print(json.dumps({'packages': [], 'total_available': 0}))
" "$SESSION_ID" "$GROUP_ID" "$AGENT_TYPE" "$LIMIT")
fi

# Parse result for next steps (log count only - summaries may contain secrets before redaction)
echo "Query returned: $(echo "$QUERY_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"packages\",[]))} packages, total_available={d.get(\"total_available\",0)}')" 2>/dev/null || echo 'parse error')"
```

**If query fails or returns empty, proceed to Step 3b (Heuristic Fallback).**

### Step 3b: Heuristic Fallback (Query Failed or FTS5 Unavailable)

**First, fetch raw context packages with consumer data:**

```bash
# Fetch packages with LEFT JOIN to get consumer info for agent_relevance calculation
SESSION_ID="bazinga_20250212_143530"
GROUP_ID="group_a"  # or empty string for session-wide
AGENT_TYPE="developer"

# Note: SESSION_ID is system-generated (not user input), but use shell variables for clarity
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet query \
  "SELECT cp.id, cp.file_path, cp.priority, cp.summary, cp.group_id, cp.created_at,
          GROUP_CONCAT(cs.agent_type) as consumers
   FROM context_packages cp
   LEFT JOIN consumption_scope cs ON cp.id = cs.package_id AND cs.session_id = cp.session_id
   WHERE cp.session_id = '$SESSION_ID'
   GROUP BY cp.id"
```

**Then apply heuristic ranking:**

| Priority | Weight |
|----------|--------|
| critical | 4 |
| high | 3 |
| medium | 2 |
| low | 1 |

**Scoring Formula:**
```
score = (priority_weight * 4) + (same_group_boost * 2) + (agent_relevance * 1.5) + recency_factor

Where:
- same_group_boost = 1 if package.group_id == request.group_id, else 0
- agent_relevance = 1 if AGENT_TYPE appears in package.consumers (from JOIN), else 0
- recency_factor = 1 / (days_since_created + 1)
```

Sort packages by score DESC, then by `created_at DESC` (tie-breaker), take top N.
Calculate: `overflow_count = max(0, total_packages - limit)`

### Step 3c: Token Packing with Redaction

After Step 3 or 3b retrieves packages, apply redaction, truncation, and token packing in the correct order:

```bash
# Token packing with