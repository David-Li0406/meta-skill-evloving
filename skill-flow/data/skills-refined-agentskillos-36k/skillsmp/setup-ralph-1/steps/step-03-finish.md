---
name: step-03-finish
description: Show run command and instructions
prev_step: steps/step-02-create-stories.md
next_step: null
---

# Step 3: Ready to Run Ralph

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER skip showing the run command
- 🛑 NEVER run ralph.sh - user runs it themselves
- ✅ ALWAYS verify prd.json exists and has stories
- ✅ ALWAYS show the complete run command for user to copy
- ✅ ALWAYS let user decide when to run
- 📋 YOU ARE a helper providing clear instructions
- 💬 FOCUS on making it easy for user to start Ralph
- 🚫 FORBIDDEN to run Ralph automatically
- 🚫 FORBIDDEN to execute any ralph.sh commands

## EXECUTION PROTOCOLS:

- 🎯 Verify all files are in place
- 💾 Show summary of what was created
- 📖 Provide clear run instructions
- 🚫 FORBIDDEN to modify any files in this step

## CONTEXT BOUNDARIES:

**Available from previous steps:**

- `{project_path}` - Absolute path to project
- `{ralph_dir}` - Path to .claude/ralph
- `{feature_name}` - Feature folder name
- `{feature_dir}` - Path to feature folder
- prd.json exists with user stories

## YOUR TASK:

Verify setup is complete and provide clear instructions for running Ralph.

---

## EXECUTION SEQUENCE:

### 1. Verify Files Exist

Check all required files:

```bash
# Check ralph.sh
ls -la {ralph_dir}/ralph.sh

# Check prompt.md
ls -la {ralph_dir}/prompt.md

# Check feature files
ls -la {feature_dir}/PRD.md
ls -la {feature_dir}/prd.json
ls -la {feature_dir}/progress.txt
```

### 2. Get Story Count

```bash
# Count stories
jq '.userStories | length' {feature_dir}/prd.json
```

### 3. Show Summary

Display a comprehensive summary:

```
╔════════════════════════════════════════════════════════════════╗
║                    ✅ RALPH READY TO RUN                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  📁 Project: {project_path}                                    ║
║  📁 Ralph:   {ralph_dir}                                       ║
║  📁 Feature: {feature_name}                                    ║
║                                                                 ║
║  📋 User Stories: {count} stories ready                        ║
║  🌿 Branch: {branchName}                                       ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 4. Show Files Created

```
📁 Files Created:

{ralph_dir}/
├── ralph.sh          # Main loop script
├── prompt.md         # Agent instructions
└── tasks/
    └── {feature_name}/
        ├── PRD.md        # Feature requirements
        ├── prd.json      # User stories ({count})
        └── progress.txt  # Learning log
```

### 5. Provide Run Command

**Primary command:**

```bash
# Navigate to project
cd {project_path}

# Run Ralph (recommended: start with low iterations to test)
bun run {ralph_dir}/ralph.sh -f {feature_name} -n 5

# Or with bash
bash {ralph_dir}/ralph.sh -f {feature_name} -n 5

# Full run (up to 20 iterations)
bun run {ralph_dir}/ralph.sh -f {feature_name} -n 20
```

### 6. Show Quick Reference

```
📖 Quick Reference:

# Check progress
jq '.userStories[] | {id, title, passes}' {feature_dir}/prd.json

# See completed stories
jq '[.userStories[] | select(.passes == true)] | length' {feature_dir}/prd.json

# View learnings
cat {feature_dir}/progress.txt

# Resume after interruption (just run again)
bun run {ralph_dir}/ralph.sh -f {feature_name}
```

### 7. Important Tips

```
💡 Tips for Success:

1. Start with -n 5 to test the first few iterations
2. Watch the first 2-3 stories to verify they work correctly
3. Ralph accumulates learnings - later iterations are smarter
4. If a story fails, it will retry in the next iteration
5. You can stop anytime with Ctrl+C and resume later

⚠️  Before Running:

1. Make sure you're on a clean git branch
2. The branch will be: {branchName}
3. Consider using Docker sandbox for isolation:
   docker sandbox run claude ./ralph.sh -f {feature_name}
```

### 8. Final Confirmation

**Use AskUserQuestion:**

```yaml
questions:
  - header: "Ready"
    question: "All set! Would you like me to explain anything else?"
    options:
      - label: "I'm ready to run Ralph"
        description: "Thanks, I'll run the command myself"
      - label: "Show me the first few stories"
        description: "Let me preview what Ralph will implement"
      - label: "How do I monitor progress?"
        description: "Explain how to track what Ralph is doing"
      - label: "What if something fails?"
        description: "Explain error recovery"
    multiSelect: false
```

**Handle responses:**

**"Show first few stories":**

```bash
jq '.userStories[:5]' {feature_dir}/prd.json
```

**"How do I monitor progress":**

```
📊 Monitoring Ralph:

1. Watch the terminal - Ralph shows iteration progress
2. Check completed stories:
   jq '[.userStories[] | select(.passes == true)] | length' {feature_dir}/prd.json

3. View learnings (grows each iteration):
   tail -50 {feature_dir}/progress.txt

4. Check git log:
   git log --oneline -10
```

**"What if something fails":**

```
🔧 Error Recovery:

1. If a story fails, Ralph will skip it and try the next
2. Run Ralph again - it picks up incomplete stories
3. If stuck, manually set "passes": true in prd.json to skip
4. Check progress.txt for learnings about what went wrong
5. Edit prd.json to break large stories into smaller ones
```

---

## SUCCESS METRICS:

✅ All files verified to exist
✅ Story count shown
✅ Run command provided
✅ Quick reference shown
✅ Tips explained
✅ User questions answered

## FAILURE MODES:

❌ Missing files (ralph.sh, prd.json, etc.)
❌ Empty prd.json (no stories)
❌ Invalid JSON in prd.json

## FINISH PROTOCOLS:

- Never run Ralph automatically
- Always let user decide when to start
- Provide complete run command they can copy
- Explain monitoring and recovery

## WORKFLOW COMPLETE:

This is the final step. The user now has everything they need to run Ralph.

<critical>
Remember: Ralph runs autonomously. Make sure the user understands:
1. How to start it
2. How to monitor it
3. How to stop/resume it
4. How to handle failures
</critical>
