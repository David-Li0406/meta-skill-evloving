---
name: ecosystem-audit
description: This skill should be used when auditing the complete agent ecosystem - CLIs, skills, rules, prompts, roles, and meta docs. Triggers include "audit my ecosystem", "verify all tools", "check CLI health", "ecosystem health check", "what's broken in my setup", or when starting a maintenance session. Runs deterministic checks + optional agent-assisted analysis.
---

# ecosystem-audit

Comprehensive audit harness for luke's agent/utils ecosystem. Deterministic baseline checks with optional agent-assisted deep analysis.

## philosophy

> "measure first, fix second"

| principle | application |
|-----------|-------------|
| deterministic baseline | PATH checks, file existence, command validation are repeatable |
| agent analysis optional | deep semantic checks use agents but aren't required |
| artifact persistence | results live in gist + ~/.agents/audit-results/ |
| specialist fanout | different domains get different specialists |
| confidence routing | low-confidence findings escalate to human |

## when to use

| use | skip |
|-----|------|
| periodic ecosystem health check | single CLI fix |
| after major tool updates | simple typo corrections |
| before long autonomous sessions | quick command verification |
| onboarding new machine | already know what's broken |
| drift detection (rules vs reality) | targeted skill improvement |

## audit domains

| domain | checks | specialists |
|--------|--------|-------------|
| **CLIs** | PATH presence, --help, --version, basic invocation | cli-validator |
| **skills** | file structure, frontmatter, triggers, references | skill-validator |
| **rules** | CLI coverage, accuracy vs --help output | rule-validator |
| **prompts** | export functionality, @file resolution | prompt-validator |
| **roles** | list/export commands, category coverage | role-validator |
| **meta** | AGENTS.md, GLOSSARY.md freshness and accuracy | meta-validator |
| **agents** | claude, codex, copilot CLI availability | agent-validator |

## decision tree: audit scope

```
What scope should I audit?
├── User says "full audit" or "everything"
│   └── all domains (7 specialists)
├── User mentions specific domain ("check my skills")
│   └── single domain specialist
├── User mentions multiple domains
│   └── requested domains only
├── Time-constrained ("quick check")
│   └── CLIs + agents only (baseline)
└── Default (no specification)
    └── all domains (7 specialists)
```

## decision tree: agent involvement

```
Should I use agent-assisted analysis?
├── User says "deterministic only" or "no agents"
│   └── skip agent specialists, baseline only
├── User says "deep" or "thorough"
│   └── full agent-assisted analysis
├── Baseline checks all pass
│   └── skip agents (healthy ecosystem)
├── Baseline shows failures
│   └── run agent specialists for diagnosis
└── Default
    └── baseline first, agents if issues found
```

## workflow

### phase 0: preflight

```bash
# verify core dependencies
which claude codex copilot jq gh > /dev/null 2>&1
```

output: dependency checklist

### phase 1: baseline checks (deterministic)

Run all deterministic checks without agent involvement:

```bash
~/.agents/skills/ecosystem-audit/scripts/baseline-audit.sh
```

**CLI checks:**
```bash
# verify each CLI on PATH
for cli in outline layer verify agents trails mem slack linear format prompts roles epub; do
  which $cli > /dev/null 2>&1 && echo "✓ $cli" || echo "✗ $cli NOT ON PATH"
done
```

**skill checks:**
```bash
# count skills with valid SKILL.md
ls ~/.agents/skills/*/SKILL.md 2>/dev/null | wc -l
```

**rule checks:**
```bash
# count rule files
ls ~/.agents/rules/*.md 2>/dev/null | wc -l
```

**prompt checks:**
```bash
# verify prompts CLI works
prompts commands list --json --quiet | jq length
```

**role checks:**
```bash
# verify roles CLI works
roles list --json --quiet | jq length
```

**agent checks:**
```bash
# verify agent CLIs
claude --version 2>/dev/null && echo "✓ claude"
codex --version 2>/dev/null && echo "✓ codex"
copilot --version 2>/dev/null && echo "✓ copilot"
```

output: baseline-results.json

### phase 2: specialist fanout (agent-assisted)

If baseline shows issues OR user requests deep audit, spawn specialists:

| specialist | focus | output |
|------------|-------|--------|
| cli-validator | verify each CLI's --help matches rule docs | cli-report.json |
| skill-validator | check skill structure, triggers, references | skill-report.json |
| rule-validator | compare rules to actual CLI behavior | rule-report.json |
| prompt-validator | test @file resolution, export | prompt-report.json |
| role-validator | verify categories and export | role-report.json |
| meta-validator | check AGENTS.md and GLOSSARY.md accuracy | meta-report.json |
| agent-validator | test claude/codex/copilot invocations | agent-report.json |

**specialist invocation pattern:**
```bash
cat <<'EOF' | copilot -p --model gemini-3-pro --output-format json
<role>CLI validator specialist</role>
<task>Verify CLI documentation accuracy</task>
<cli>outline</cli>
<rule_file>~/.agents/rules/outline.md</rule_file>
<checks>
1. Run outline --help
2. Compare documented flags to actual flags
3. Test 2-3 documented examples
4. Report discrepancies
</checks>
<output_contract>
{"cli":"outline","status":"pass|fail","discrepancies":[],"confidence":8}
</output_contract>
EOF
```

### phase 3: synthesis

Aggregate all specialist reports:

```bash
~/.agents/skills/ecosystem-audit/scripts/synthesize-audit.sh
```

output: ecosystem-audit-report.json

### phase 4: artifact persistence

**gist creation:**
```bash
gh gist create --desc "ecosystem-audit $(date +%Y-%m-%d)" \
  baseline-results.json \
  ecosystem-audit-report.json
```

**local storage:**
```bash
mkdir -p ~/.agents/audit-results/$(date +%Y-%m-%d)
cp baseline-results.json ecosystem-audit-report.json ~/.agents/audit-results/$(date +%Y-%m-%d)/
```

### phase 5: handoff

output contract:

```json
{
  "audit_date": "2025-01-23",
  "status": "healthy | degraded | broken",
  "summary": "...",
  "domains": {
    "clis": {"status": "pass", "count": 12, "issues": []},
    "skills": {"status": "pass", "count": 21, "issues": []},
    "rules": {"status": "warn", "count": 25, "issues": ["prompts.md missing"]},
    "prompts": {"status": "pass", "count": 15, "issues": []},
    "roles": {"status": "pass", "count": 22, "issues": []},
    "agents": {"status": "pass", "count": 3, "issues": []},
    "meta": {"status": "pass", "issues": []}
  },
  "artifacts": {
    "gist_url": "https://gist.github.com/...",
    "local_path": "~/.agents/audit-results/2025-01-23/"
  },
  "recommendations": [],
  "confidence": 9
}
```

## validation gates

| gate | criteria | action if fail |
|------|----------|----------------|
| baseline pass | all CLIs on PATH | report missing, suggest fix |
| skill structure | all skills have SKILL.md | list malformed skills |
| rule coverage | each CLI has rule file | list missing rules |
| prompt export | prompts commands export works | check oclif manifest |
| role list | roles list returns results | check roles CLI |
| agent availability | claude/codex/copilot on PATH | report missing agents |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| outline | `outline --help` | verify CLI works |
| layer | `layer --help` | verify CLI works |
| prompts | `prompts commands list --json -q` | enumerate prompts |
| roles | `roles list --json -q` | enumerate roles |
| trails | `trails trail record --agent claude --task "ecosystem-audit"` | persistence |
| gh | `gh gist create` | artifact storage |

### trails integration

```bash
# start audit trace
TRACE=$(trails trail record --agent claude --new-trace --action started \
  --task "ecosystem-audit: full" --json -q | jq -r '.trace_id')

# record completion
trails trail record --agent claude --trace-id $TRACE --action completed \
  --task "ecosystem-audit: $STATUS" --confidence $CONFIDENCE \
  --gist --gist-description "ecosystem-audit $(date +%Y-%m-%d)"
```

## deterministic checks (always run)

### CLI presence matrix

| CLI | required | check |
|-----|----------|-------|
| outline | yes | `which outline` |
| layer | yes | `which layer` |
| verify | yes | `which verify` |
| agents | yes | `which agents` |
| trails | yes | `which trails` |
| mem | yes | `which mem` |
| slack | yes | `which slack` |
| linear | yes | `which linear` |
| format | yes | `which format` |
| prompts | yes | `which prompts` |
| roles | yes | `which roles` |
| epub | yes | `which epub` |

### agent CLI presence

| agent CLI | check |
|-----------|-------|
| claude | `claude --version` |
| codex | `codex --version` |
| copilot | `copilot --version` |

### skill structure checks

```bash
for skill_dir in ~/.agents/skills/*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    # check frontmatter
    head -1 "$skill_dir/SKILL.md" | grep -q "^---" || echo "WARN: $skill_name missing frontmatter"
    # check description
    grep -q "^description:" "$skill_dir/SKILL.md" || echo "WARN: $skill_name missing description"
  else
    echo "ERROR: $skill_name missing SKILL.md"
  fi
done
```

### rule coverage matrix

```bash
# CLIs that should have rules
CLIS=(outline layer verify agents trails mem slack linear format prompts roles)
for cli in "${CLIS[@]}"; do
  [ -f ~/.agents/rules/$cli.md ] && echo "✓ $cli.md" || echo "✗ $cli.md MISSING"
done
```

## quick audit (baseline only)

```bash
# 30-second ecosystem health check
~/.agents/skills/ecosystem-audit/scripts/baseline-audit.sh --quick
```

outputs one-line status per domain:
```
CLIs: 12/12 ✓
Skills: 21 found ✓
Rules: 25 found ✓
Prompts: 15 commands ✓
Roles: 22 personas ✓
Agents: 3/3 ✓
```

## full audit (with agents)

```bash
# comprehensive audit with specialist analysis
~/.agents/skills/ecosystem-audit/scripts/full-audit.sh
```

spawns 7 specialists, aggregates results, creates gist.

## output examples

### baseline pass

```json
{
  "status": "healthy",
  "clis": {"found": 12, "missing": []},
  "skills": {"count": 21, "malformed": []},
  "rules": {"count": 25, "missing": []},
  "prompts": {"count": 15},
  "roles": {"count": 22},
  "agents": {"available": ["claude", "codex", "copilot"]}
}
```

### baseline with issues

```json
{
  "status": "degraded",
  "clis": {"found": 11, "missing": ["epub"]},
  "skills": {"count": 21, "malformed": ["broken-skill"]},
  "rules": {"count": 23, "missing": ["prompts.md", "roles.md"]},
  "prompts": {"count": 15},
  "roles": {"count": 22},
  "agents": {"available": ["claude", "codex"], "missing": ["copilot"]}
}
```

## artifact storage

### gist structure

```
ecosystem-audit-2025-01-23/
├── baseline-results.json     # deterministic checks
├── ecosystem-audit-report.json  # full report
├── cli-report.json          # CLI specialist (if run)
├── skill-report.json        # skill specialist (if run)
└── summary.md               # human-readable summary
```

### local structure

```
~/.agents/audit-results/
├── 2025-01-23/
│   ├── baseline-results.json
│   └── ecosystem-audit-report.json
├── 2025-01-22/
│   └── ...
└── latest -> 2025-01-23/
```

## scheduling

| frequency | scope | trigger |
|-----------|-------|---------|
| daily | quick baseline | cron or manual |
| weekly | full audit | before maintenance |
| on-demand | specific domain | when issues suspected |
| post-update | affected domains | after CLI/skill changes |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| skipping baseline | agents analyze healthy system | always run baseline first |
| ignoring warnings | drift accumulates | fix warnings same session |
| no artifact persistence | can't track trends | always gist + local save |
| running full audit for quick check | wastes time/tokens | use --quick for health checks |
| not reading specialist output | miss detailed findings | review all specialist reports |

## references

- [references/cli-checklist.md](references/cli-checklist.md) - detailed CLI validation steps
- [references/skill-checklist.md](references/skill-checklist.md) - skill structure requirements
- [references/specialist-briefs.md](references/specialist-briefs.md) - prompts for each specialist

## scripts

- [scripts/baseline-audit.sh](scripts/baseline-audit.sh) - deterministic baseline checks
- [scripts/full-audit.sh](scripts/full-audit.sh) - complete audit with specialists
- [scripts/synthesize-audit.sh](scripts/synthesize-audit.sh) - aggregate specialist reports
