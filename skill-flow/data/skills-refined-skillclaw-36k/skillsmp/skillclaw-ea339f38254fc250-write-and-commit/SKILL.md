---
name: write-and-commit
description: Use this skill when you need to create a new file and commit it atomically, significantly reducing the time and steps involved in the process.
---

# Write and Commit Skill

**Purpose**: Create a new file and commit it in a single atomic operation, reducing LLM round-trips from 4-5 to 2-3.

**Performance**: 60-75% faster than traditional workflow.

## When to Use This Skill

### ✅ Use write-and-commit When:

- Creating a **new file** that will be committed immediately.
- File content is **ready and complete** (no iterative edits needed).
- You want to **save time** on routine file creation.
- Creating **scripts** that need executable permissions.
- Adding **configuration files** or **documentation**.
- Creating **test files** or **example code**.

### ❌ Do NOT Use When:

- **Editing existing files** (use Edit tool instead).
- File content is **complex and may need iteration**.
- Creating multiple related files that should be in **one commit together**.
- File is **part of larger refactoring** (commit all changes together).
- You need to **review the file** before committing.

## Performance Comparison

### Traditional Workflow (4-5 LLM round-trips, 20-30s)

```
[LLM Round 1] Write file
  → Write tool: Create file with content

[LLM Round 2] Make executable (if needed)
  → Bash: chmod +x file.sh

[LLM Round 3] Stage file
  → Bash: git add file.sh

[LLM Round 4] Commit file
  → Bash: git commit -m "Add file"

[LLM Round 5] Report success
  → Report commit SHA to user
```

**Total**: 20-30 seconds, 4-5 LLM round-trips.

### Optimized Workflow (2-3 LLM round-trips, 5-8s)

```
[LLM Round 1] Change and execute
  → Write content to temp file
  → Write commit message to temp file
  → Bash: write-and-commit.sh file.sh /tmp/content /tmp/msg --executable

[LLM Round 2] Report success
  → Parse JSON result
  → Report commit SHA to user
```

**Total**: 5-8 seconds, 2-3 LLM round-trips.

**Savings**: 60-75% faster.

## Usage

### Basic File Creation

```bash
# Step 1: Prepare content and commit message (in LLM)
cat > /tmp/content-$$.txt <<'EOF'
File content goes here...
EOF

cat > /tmp/commit-msg-$$.txt <<'EOF'
Add new feature file

Description of what this file does.

EOF

# Step 2: Execute atomic creation
~/.claude/scripts/write-and-commit.sh \
  "path/to/file.txt" \
  "/tmp/content-$$.txt" \
  "/tmp/commit-msg-$$.txt"
```

### Executable Script Creation

```bash
# For scripts that need executable permissions
~/.claude/scripts/write-and-commit.sh \
  "path/to/my-script.sh" \
  "/tmp/content-$$.txt" \
  "/tmp/commit-msg-$$.txt" --executable
```