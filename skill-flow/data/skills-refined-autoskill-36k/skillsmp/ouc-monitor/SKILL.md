---
name: ouc-monitor
description: >
  Use this skill when monitoring OUC system state for anomalies or changes.
  Detects upgrade events, auditor pool changes, proposal status, and triggers
  appropriate actions. Part of the Self-Amending Protocol AI Agent infrastructure.
allowed-tools: Bash,Read,Grep,WebFetch
---

# OUC Monitoring Skill

This skill provides patterns for continuous monitoring of the OUC ecosystem.

## Monitoring Targets

### 1. ERC-7546 Dictionary Changes

Monitor for implementation changes:
```bash
# Get current block
CURRENT_BLOCK=$(cast block-number --rpc-url $RPC_URL)

# Compare with last known state
# Store snapshots in .ouc-monitor/snapshots/
```

**Triggers**:
- New selector added → Log + potential proposal
- Selector implementation changed → Alert + propose audit
- Selector removed → High priority alert
- Zombie reference detected → CRITICAL alert

### 2. OUC Canister State

```bash
# Check proposal queue
dfx canister call ouc getProposalCount

# Check for pending proposals needing review
dfx canister call ouc getPendingProposals

# Check auditor pool health
dfx canister call ouc getAuditorCount
```

**Triggers**:
- New proposal submitted → Notify auditors
- Proposal voting deadline approaching → Reminder
- Auditor pool below threshold → Warning

### 3. Auditor Pool Health

```bash
# Get active auditor count
dfx canister call ouc getActiveAuditorCount

# Check for slashed auditors
dfx canister call ouc getSlashedAuditors
```

**Triggers**:
- Active auditors < minimum threshold → Critical
- Auditor slashed → Investigation required
- Average reputation declining → Warning

## Protocol Health States (LazyShared.Types.Health)

The monitoring system maps observations to standardized health states:

| Health State | Description | Mapped From |
|--------------|-------------|-------------|
| `Healthy` | Normal operation, no changes | All checks pass |
| `Wounded` | Minor anomaly, auto-recovery | ENV issues, pending audits |
| `Drifting` | Local vs deployed divergence | Implementation changes detected |
| `Frozen` | Awaiting human decision | Audit failed, liveness issues |
| `Dead` | Unrecoverable | Key compromise, ops unavailable |

### Health Indicators (FR Monad failure taxonomy)

| Indicator | FR Monad | Trigger |
|-----------|----------|---------|
| `EnvContamination` | f_env | Build environment issue |
| `KeyCompromise` | f_key | Key leak or loss |
| `ReproFailure` | f_repro | Non-reproducible build |
| `OpsUnavailable` | f_ops | Operator stopped |
| `AuditPending` | OUC | Upgrade awaiting audit |
| `AuditFailed` | OUC | Audit rejected |
| `LivenessFailing` | OUC | Execution subject unavailable |
| `DriftDetected` | drift | Local vs deployed diff |
| `ProposalPending` | OUC | Proposals awaiting decision |

## Urgency Levels

| Urgency | Health State | Action |
|---------|--------------|--------|
| `Immediate` | Frozen (AuditFailed) | Stop everything, human review |
| `Soon` | Drifting, Frozen | Handle in next batch window |
| `Routine` | Wounded, Healthy | Normal monitoring cycle |
| `Archive` | Dead | Record only, no action expected |

## Automatic Quarantine (止血の自動化)

The monitoring system automatically applies quarantine rules to prevent damage propagation:

### Quarantine Rules (defaultQuarantineRules)

| Rule | Trigger | Action |
|------|---------|--------|
| `key-compromise` | KeyCompromise indicator | Freeze + immediate human review |
| `audit-failed` | AuditFailed indicator | Freeze + block upgrade |
| `liveness-failing` | LivenessFailing indicator | Freeze + block operations |
| `high-drift` | DriftDetected >= 100 lines | RequireMoreAuditors(2) |
| `repro-failure` | ReproFailure indicator | RollbackPending |

### Quarantine Actions

| Action | Effect |
|--------|--------|
| `Freeze(reason)` | Set health=Frozen, urgency=Immediate |
| `RequireMoreAuditors(n)` | Add note to require N additional auditors |
| `RollbackPending` | Set health=Frozen, urgency=Soon |
| `NoAction` | No automatic intervention |

### Example Output with Quarantine

```
=== Protocol Health ===
  [frozen/immediate] OUC Mainnet (ouc-mainnet): Audit failed - upgrade blocked
    ⚠ QUARANTINED: Audit failed - upgrade blocked until resolved
  Protocols: 1 (critical=1, warning=0, healthy=0)
```

### Customizing Quarantine Rules

To override default rules, create custom `QuarantineRule` list in your monitoring code:

```idris
myRules : List QuarantineRule
myRules =
  [ MkQuarantineRule "custom-freeze"
      (any (\case EnvContamination _ => True; _ => False))
      (Freeze "Environment contaminated - manual review needed")
  ]

-- Use custom rules
let action = shouldQuarantine myRules indicators
```

## Legacy Alert Levels (for backward compatibility)

| Level | Description | Action |
|-------|-------------|--------|
| CRITICAL | System integrity at risk | Immediate human review |
| HIGH | Significant change detected | Automated proposal + notification |
| MEDIUM | Notable change | Log + daily summary |
| LOW | Minor change | Log only |
| INFO | Status update | Periodic report |

## Monitoring Loop Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Loop                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Fetch Current State                                     │
│     ├── EVM: Dictionary implementations                     │
│     ├── ICP: OUC canister state                            │
│     └── Store snapshot                                      │
│                                                             │
│  2. Compare with Baseline                                   │
│     ├── Load previous snapshot                             │
│     ├── Detect changes                                      │
│     └── Classify by severity                                │
│                                                             │
│  3. Generate Actions                                        │
│     ├── CRITICAL → Human alert + halt                      │
│     ├── HIGH → Auto-propose + notify                       │
│     ├── MEDIUM → Queue for review                          │
│     └── LOW/INFO → Log                                     │
│                                                             │
│  4. Execute Actions                                         │
│     ├── Submit proposals                                    │
│     ├── Send notifications                                  │
│     └── Update baseline                                     │
│                                                             │
│  5. Wait for next interval                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## State Storage

Store monitoring state in `.ouc-monitor/`:

```
.ouc-monitor/
├── config.json           # Monitoring configuration
├── health/
│   └── protocol-PROTOCOL_ID.json  # ProtocolHealthReport
├── snapshots/
│   ├── evm-YYYYMMDD-HHMMSS.json
│   └── icp-YYYYMMDD-HHMMSS.json
├── alerts/
│   └── alert-TIMESTAMP.json
└── logs/
    └── monitor-YYYYMMDD.log
```

### Health Report Format

Each protocol's health is stored in `health/protocol-*.json`:

```json
{
  "protocolId": "ouc-mainnet",
  "protocolName": "OUC Mainnet",
  "health": "healthy",
  "indicators": ["ok"],
  "urgency": "routine",
  "lastChecked": "2026-01-11T12:00:00Z",
  "message": "All checks passed"
}
```

### Dashboard Output

When running `lazy ask` with Health integration:

```
=== Protocol Health ===
  [healthy/routine] OUC Mainnet (ouc-mainnet): All checks passed
  [drifting/soon] OUC Testnet (ouc-testnet): 15 gaps detected
  Protocols: 2 (critical=0, warning=1, healthy=1)
```

## Integration with lazy CLI

Use lazy tools for analysis:
```bash
# EVM lifecycle analysis
lazy evm-lifecycle ask . --steps=1,2,3

# ICP canister analysis
lazy dfx ask . --steps=1,2,3,4
```

## Automation

For continuous monitoring, use cron or systemd:

```bash
# Cron: Every 5 minutes
*/5 * * * * /path/to/ouc-monitor.sh >> /var/log/ouc-monitor.log 2>&1

# Or use watch for development
watch -n 300 '/path/to/ouc-monitor.sh'
```

## Example Monitor Script

```bash
#!/bin/bash
# ouc-monitor.sh - Health-aware monitoring

set -e

MONITOR_DIR=".ouc-monitor"
PROTOCOL_ID="${1:-ouc-default}"
mkdir -p "$MONITOR_DIR/snapshots" "$MONITOR_DIR/alerts" "$MONITOR_DIR/logs" "$MONITOR_DIR/health"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ISO_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Take EVM snapshot and get health
lazy evm-lifecycle ask . --output-json > "$MONITOR_DIR/snapshots/evm-$TIMESTAMP.json"

# Extract health from lazy ask output (assumes Health integration)
# The output includes healthReports field
HEALTH=$(jq -r '.healthReports[0].health // "unknown"' "$MONITOR_DIR/snapshots/evm-$TIMESTAMP.json" 2>/dev/null || echo "unknown")
URGENCY=$(jq -r '.healthReports[0].urgency // "routine"' "$MONITOR_DIR/snapshots/evm-$TIMESTAMP.json" 2>/dev/null || echo "routine")
GAP_COUNT=$(jq -r '.result.gaps | length' "$MONITOR_DIR/snapshots/evm-$TIMESTAMP.json" 2>/dev/null || echo "0")

# Generate health report
cat > "$MONITOR_DIR/health/protocol-$PROTOCOL_ID.json" << EOF
{
  "protocolId": "$PROTOCOL_ID",
  "protocolName": "$PROTOCOL_ID",
  "health": "$HEALTH",
  "urgency": "$URGENCY",
  "lastChecked": "$ISO_TIMESTAMP",
  "message": "$GAP_COUNT gaps detected"
}
EOF

# Alert based on health state
case "$HEALTH" in
  "dead"|"frozen")
    echo "[CRITICAL] Protocol $PROTOCOL_ID is $HEALTH - immediate attention required"
    echo "{\"level\":\"CRITICAL\",\"protocol\":\"$PROTOCOL_ID\",\"health\":\"$HEALTH\",\"timestamp\":\"$ISO_TIMESTAMP\"}" \
      > "$MONITOR_DIR/alerts/alert-$TIMESTAMP.json"
    ;;
  "drifting")
    echo "[WARNING] Protocol $PROTOCOL_ID is drifting - review soon"
    ;;
  "wounded")
    echo "[INFO] Protocol $PROTOCOL_ID has minor issues"
    ;;
  "healthy")
    echo "[OK] Protocol $PROTOCOL_ID is healthy"
    ;;
esac

# Take ICP snapshot
dfx canister call ouc getStatus > "$MONITOR_DIR/snapshots/icp-$TIMESTAMP.json" 2>/dev/null || true

echo "[$(date)] Monitor cycle complete: $PROTOCOL_ID is $HEALTH ($URGENCY)" \
  >> "$MONITOR_DIR/logs/monitor-$(date +%Y%m%d).log"
```

## Multi-Protocol Dashboard

To monitor multiple protocols and aggregate health:

```bash
#!/bin/bash
# ouc-dashboard.sh - Aggregate health across protocols

MONITOR_DIR=".ouc-monitor"

echo "=== Protocol Health Dashboard ==="
echo ""

CRITICAL=0
WARNING=0
HEALTHY=0

for health_file in "$MONITOR_DIR"/health/protocol-*.json; do
  [ -f "$health_file" ] || continue

  HEALTH=$(jq -r '.health' "$health_file")
  URGENCY=$(jq -r '.urgency' "$health_file")
  NAME=$(jq -r '.protocolName' "$health_file")
  MSG=$(jq -r '.message' "$health_file")

  echo "  [$HEALTH/$URGENCY] $NAME: $MSG"

  case "$HEALTH" in
    "dead"|"frozen") ((CRITICAL++)) ;;
    "drifting"|"wounded") ((WARNING++)) ;;
    "healthy") ((HEALTHY++)) ;;
  esac
done

TOTAL=$((CRITICAL + WARNING + HEALTHY))
echo ""
echo "Protocols: $TOTAL (critical=$CRITICAL, warning=$WARNING, healthy=$HEALTHY)"

# Exit with error if any critical
[ "$CRITICAL" -eq 0 ] || exit 1
```
