---
name: mac-health
description: Quick Mac system health check with battery, RAM, CPU status and actionable recommendations. Use when user mentions "mac health", "mac status", "mac performance", "battery check", "ram usage", "what's eating memory", "should I kill any process", or "mac running slow".
---

# Mac Health Check

**Why?** Quickly diagnose if your Mac is struggling and get actionable fixes without digging through Activity Monitor.

## Quick Start

```
"check my mac health" → battery, RAM, CPU summary + recommendations
```

---

## Workflow

### Step 1: Gather System Metrics

Run these commands in parallel:

```bash
# Battery status
pmset -g batt

# RAM overview (total + usage)
system_profiler SPHardwareDataType | grep "Memory"
vm_stat

# Top processes by memory (top 5)
ps aux -m | head -6

# Top processes by CPU (top 5)  
ps aux -r | head -6

# Network speed (built-in macOS tool)
networkQuality
```

> [!NOTE]
> **Validation checkpoint**: Verify all commands succeeded before proceeding. If `pmset` returns nothing, you're on a desktop Mac — skip battery. If `vm_stat` fails, fall back to `top -l 1` for memory info.

### Step 2: Format Concise Output

Present as a brief summary, NOT tables. Example format:

```
🔋 Battery: 73% (discharging, ~20h remaining)
💾 RAM: 17.1GB / 24GB used (71%)
⚡ CPU: Light load
🌐 Network: ⬇️ 262 Mbps ⬆️ 26 Mbps (36ms latency)

Top memory: Amp (478MB), Passwords (320MB), Spotlight (310MB)
Top CPU: WindowServer (3.2%), Amp (2.1%), Finder (0.8%)
```

### Step 3: Analyze & Recommend

> [!TIP]
> Keep output concise — users want a quick health check, not a system report.

Apply these thresholds and provide recommendations:

**Battery:**
- < 20%: "⚠️ Consider plugging in soon"
- < 10%: "🔴 Critical — plug in now"

**RAM:**
- \> 85% used: "⚠️ Memory pressure high"
- \> 95% used: "🔴 System may slow down — consider closing apps"
- Any single process > 2GB: Flag it for potential action

**CPU:**
- Any process > 80% sustained: "⚠️ [Process] using significant CPU"
- Any process > 150%: "🔴 [Process] may be stuck — consider force-quitting"

**Network:**
- Download < 10 Mbps: "⚠️ Slow download speed"
- Upload < 5 Mbps: "⚠️ Slow upload speed"
- Latency > 100ms: "⚠️ High latency — may affect video calls"

**Common recommendations:**
| Condition | Recommendation |
|-----------|----------------|
| mds_stores high CPU/RAM | "Spotlight indexing — will settle down" |
| kernel_task high CPU | "Thermal throttling — check ventilation" |
| WindowServer high | "GPU load from UI — normal if using many windows" |
| Inactive app using >1GB | "Consider quitting [app] to free memory" |

### Step 4: Offer Actions

> [!CAUTION]
> Only offer to kill a process if it's clearly stuck (>150% CPU) or the user explicitly asks.

If issues found, offer:
- "Want me to kill [process]?" (if clearly stuck)
- "Should I check what's causing [issue]?"

If healthy:
- End with "✅ System looks healthy — no action needed"

## Examples

### Example 1: Healthy System

```
🔋 Battery: 73% (discharging, ~20h remaining)
💾 RAM: 17.1GB / 24GB (71%) — healthy
⚡ CPU: Light load (< 10% average)
🌐 Network: ⬇️ 262 Mbps ⬆️ 26 Mbps (36ms latency)

Top memory: Amp (478MB), Passwords (320MB), Spotlight (310MB)
Top CPU: WindowServer (1.0%), Amp (0.7%), Finder (0.3%)

✅ System looks healthy — no action needed
```

### Example 2: Low Battery + High RAM

```
🔋 Battery: 8% (discharging, ~45min remaining)
   🔴 Critical — plug in now!
💾 RAM: 22.8GB / 24GB (95%)
   🔴 Memory pressure critical — consider closing apps
⚡ CPU: Moderate load

Top memory: Chrome (4.2GB), Slack (1.8GB), Docker (1.5GB)
Top CPU: Chrome Helper (12%), Docker (8%), Spotlight (5%)

⚠️ Chrome using 4.2GB — consider closing unused tabs
⚠️ Docker using 1.5GB — quit if not needed

Want me to help close any of these?
```

### Example 3: Stuck Process

```
🔋 Battery: 45% (charging)
💾 RAM: 14GB / 24GB (58%) — healthy
⚡ CPU: High load

Top memory: Xcode (2.1GB), Simulator (890MB), Safari (650MB)
Top CPU: node (187%), Xcode (45%), coreaudiod (12%)

🔴 node at 187% CPU — likely stuck or in infinite loop
   Process running for 8+ minutes at this level

Want me to kill the stuck node process (PID 12847)?
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `pmset` returns nothing | No battery (desktop Mac) | Skip battery section |
| `vm_stat` weird numbers | Values are in pages | Multiply by 16384 / 1048576 for MB |
| Process names truncated | `ps` default column width | Use `ps aux -m -o pid,rss,comm` for full names |
| RAM numbers don't add up | macOS uses compressed/cached memory | Focus on "active + wired" as true usage |
| High CPU but system feels fine | Brief spikes are normal | Only flag if sustained >30 seconds |

---

## Quality Rules

### Output Validation Checklist

Before presenting results, verify:
- [ ] All four sections present (Battery, RAM, CPU, Network)
- [ ] Percentages calculated correctly (used/total × 100)
- [ ] Top processes listed for both memory AND CPU
- [ ] Recommendations match thresholds (not arbitrary)
- [ ] Emojis used consistently (🔋💾⚡🌐 for sections, ⚠️🔴✅ for status)

### Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Show raw `vm_stat` output | Convert pages to MB/GB |
| List 10+ processes | Top 3-5 only |
| Use technical jargon | Plain language ("memory pressure" not "page faults") |
| Recommend killing system processes | Only suggest for user apps |
| Give advice without thresholds | Always cite the threshold being exceeded |

### Naming Conventions

- Battery states: "charging", "discharging", "fully charged", "not charging"
- RAM levels: "healthy" (<85%), "high" (85-95%), "critical" (>95%)
- CPU levels: "light" (<30%), "moderate" (30-60%), "high" (>60%)
- Network levels: "slow" (download <10Mbps), "moderate" (10-50Mbps), "fast" (>50Mbps)

---

## Testing

### Evaluation Scenarios

| Scenario | Input Condition | Expected Behavior |
|----------|-----------------|-------------------|
| Healthy system | RAM <85%, CPU <30%, Battery >20% | Shows "✅ System looks healthy" |
| Low battery | Battery <10% | Shows 🔴 critical warning |
| High RAM | RAM >95% | Shows 🔴 + suggests closing apps |
| Stuck process | Any process >150% CPU | Offers to kill with PID |
| Desktop Mac | No battery (iMac, Mac Mini, Mac Pro) | Skips battery section gracefully |
| Memory hog | Single process >2GB | Flags for potential action |
| Slow network | Download <10 Mbps | Shows ⚠️ slow download warning |
| High latency | Latency >100ms | Shows ⚠️ latency warning |

### Model Coverage

- **Tested on**: Sonnet, Haiku
- **Edge cases verified**: Desktop Mac (no battery), fresh boot (low usage), compile job (high CPU spike)

### Validation Commands

```bash
# Verify battery section works
pmset -g batt

# Verify RAM calculation
vm_stat | head -5

# Verify process listing
ps aux -m | head -3

# Verify network test works
networkQuality
```
