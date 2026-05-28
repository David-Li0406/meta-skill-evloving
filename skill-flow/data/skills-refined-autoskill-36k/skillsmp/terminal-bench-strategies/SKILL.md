---
name: terminal-bench-strategies
description: Comprehensive strategies and patterns for maximizing Terminal-Bench 2.0 task completion. Contains battle-tested approaches from top-performing agents.
---

# Terminal-Bench Strategies

## Overview

This skill encapsulates proven strategies from top-performing agents (Droid #1, Ante, Junie) for Terminal-Bench 2.0 tasks. Apply these patterns to maximize task completion rates.

## PROACTIVE USAGE

**Invoke this skill when:**
- Starting any Terminal-Bench task
- Facing time-constrained terminal tasks
- Working in Docker/container environments
- Encountering multi-step system tasks

---

## Critical Success Factors

### 1. Environmental Awareness First

**ALWAYS bootstrap with system info before doing anything else:**

```bash
# Execute this immediately on task start
echo "=== SYSTEM ===" && uname -a
echo "=== OS ===" && cat /etc/os-release 2>/dev/null || cat /etc/*release 2>/dev/null
echo "=== TOOLS ===" && which bash python python3 pip pip3 npm node go cargo rustc java 2>/dev/null
echo "=== DISK ===" && df -h / 2>/dev/null
echo "=== MEM ===" && free -h 2>/dev/null
echo "=== CWD ===" && pwd && ls -la
echo "=== ENV ===" && env | grep -v -E "^(LS_COLORS|PATH)=" | head -30
echo "=== GIT ===" && git status 2>/dev/null
```

**Why:** Saves time, avoids redundant commands, reveals available tools.

### 2. Speed Optimization

```
SPEED RULES:
├─ Use rg/ripgrep instead of grep (10-100x faster)
├─ Use fd instead of find (faster file discovery)
├─ Short default timeouts (30s), opt-in to longer
├─ Fail fast - don't retry blindly
├─ Parallel operations when possible: make -j$(nproc)
├─ Skip unnecessary steps (docs, tests if not required)
└─ Cache/prebuilt over compile when available
```

### 3. Minimalist Tool Usage

```
TOOL DISCIPLINE:
├─ Fewer tools = fewer error points
├─ Simple schemas = less ambiguity
├─ One tool call per logical operation
├─ Always verify tool output
└─ Handle errors explicitly, don't assume success
```

### 4. Planning and Progress Tracking

```
PLAN FORMAT:
[x] 1. Bootstrap environment info
[x] 2. Analyze task requirements  
[>] 3. Implement solution
[ ] 4. Validate solution
[ ] 5. Write output to required location

Keep plan at END of context (recency bias advantage)
```

---

## Task Category Patterns

### System Administration

```bash
# Kernel tasks
make olddefconfig && make -j$(nproc)

# Network tasks
ip addr show                    # Modern command
ss -tlnp                        # Port listening
systemctl status <service>      # Service status

# Service tasks
systemctl start/stop/restart <service>
journalctl -u <service> -f      # Follow logs
```

### Security Tasks

```bash
# Secret extraction
grep -rE "(password|secret|key|token)=" .
env | grep -iE "(pass|secret|key|token)"
cat /proc/*/environ 2>/dev/null | tr '\0' '\n' | grep -i pass

# CVE exploitation
# Research CVE first, apply known exploit technique
# Example: CVE-2023-28432 for MinIO information disclosure

# Hash cracking
hashcat -m 0 hash.txt wordlist.txt    # MD5
john --wordlist=wordlist.txt hash.txt
```

### ML/Data Science

```python
# Quick model training
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,           # Keep low for speed
    per_device_train_batch_size=16,
    save_strategy='no',           # Skip if not needed
    logging_steps=100,
)
```

### Debugging

```bash
# Python dependency issues
pip check                         # Check conflicts
pip install --no-cache-dir <pkg>  # Fresh install

# Conda conflicts
conda env export > env.yml
conda env remove -n <env>
conda env create -f env.yml

# Git recovery
git reflog                        # Find lost commits
git checkout <hash> -- <file>     # Recover file
```

---

## Common Pitfalls

### DO NOT:

1. **Retry blindly** - Analyze error first
2. **Assume tools exist** - Check with `which`
3. **Ignore time limits** - Use `timeout` command
4. **Skip validation** - Always verify output
5. **Use interactive commands** - Pipe/redirect instead
6. **Trust default configs** - Read task requirements

### DO:

1. **Read task requirements completely** - Twice
2. **Check output path exists** - `mkdir -p $(dirname /path/to/output)`
3. **Verify output after writing** - `cat /path/to/output`
4. **Handle edge cases** - Empty files, missing dirs
5. **Use absolute paths** - Avoid ambiguity

---

## Output Requirements

**ALWAYS verify output matches requirements:**

```bash
# Ensure directory exists
mkdir -p "$(dirname /path/to/output)"

# Write output
echo "result" > /path/to/output

# Verify content
test -f /path/to/output && echo "File exists"
cat /path/to/output

# Check format if specified
file /path/to/output
wc -l /path/to/output
```

---

## Model-Specific Tips

### Claude Opus (Best for Security/Debugging)
- Will attempt risky operations when needed
- Good at CVE exploitation, root cause analysis
- Prefers FIND_AND_REPLACE for file editing

### GPT-5.x (Best for ML/Video)
- Better at model training tasks
- More conservative approach
- Prefers V4A diff format

### Sonnet (Best for Speed)
- Fast iteration
- Good for general tasks
- Prefers absolute paths

---

## Time Budget Management

```
TYPICAL 10-MINUTE TASK:
├─ 0-1 min: Environment bootstrap
├─ 1-2 min: Task analysis
├─ 2-7 min: Implementation
├─ 7-9 min: Validation
└─ 9-10 min: Output verification

IF BEHIND SCHEDULE:
├─ Skip optional validation
├─ Use prebuilt over compile
├─ Simplify approach
└─ Focus on required output only
```

---

## Checklist Before Completion

```
☐ Task requirements fully addressed
☐ Output written to correct location
☐ Output format matches specification
☐ Any test scripts pass
☐ No error messages in final state
```

---

## Reference Commands

### File Operations
```bash
head -n 10 file.txt           # First 10 lines
tail -n 10 file.txt           # Last 10 lines
wc -l file.txt                # Line count
file file.txt                 # File type
md5sum file.txt               # Checksum
```

### Process Management
```bash
ps aux | grep <process>       # Find process
kill -9 <pid>                 # Force kill
timeout 30 <command>          # With timeout
nohup <command> &             # Background
```

### Network
```bash
curl -sI <url> | head -10     # Headers only
wget -q -O - <url>            # Output to stdout
nc -zv host port              # Port check
```

### Archive
```bash
tar -xzf file.tar.gz          # Extract tar.gz
unzip file.zip                # Extract zip
7z x file.7z                  # Extract 7z
```
