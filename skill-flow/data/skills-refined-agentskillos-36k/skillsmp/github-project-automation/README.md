# GitHub Projects v2 Automation Skill

Automate GitHub project planning AND autonomous issue implementation.

## What This Skill Does

### Mode 1: Project Planning
Converts codebase analysis into a fully organized GitHub Projects v2 board with:
- Bulk issue creation (50-100+ issues)
- Epic/status/priority labels
- Automated status field synchronization
- Kanban board organization
- Comprehensive project documentation

### Mode 2: Issue Implementation (NEW!)
Autonomously implements GitHub issues with full workflow automation:
- Issue selection (specific or auto-select by priority)
- Codebase context analysis
- Implementation plan generation
- TDD workflow execution
- Quality gates (tests, types, lint)
- Commit and PR creation
- Issue linking and status updates

## When to Use

### Project Planning Mode
- **Trigger phrases:**
  - "Build project plan from codebase"
  - "Create GitHub project from feature analysis"
  - "Set up project board with all epics"
  - "Audit codebase and create roadmap"

- **Use cases:**
  - New project needs comprehensive planning
  - Existing codebase lacks project organization
  - Sprint planning requires feature inventory
  - Stakeholder visibility into development status

### Issue Implementation Mode
- **Trigger phrases:**
  - "work on #104"
  - "implement #104"
  - "work on next critical issue"
  - "work on next payment issue"

- **Use cases:**
  - Autonomous feature implementation
  - Batch-process multiple issues
  - Reduce manual development time
  - Ensure consistent quality standards

## Quick Start

### Project Planning Mode

1. **Authenticate GitHub CLI:**
   ```bash
   gh auth refresh -h github.com -s project,repo
   ```

2. **Analyze codebase:**
   - Use Task tool with Explore agent
   - Identify features by epic and status

3. **Run automation scripts:**
   ```bash
   # Create labels
   ./scripts/create_labels.sh

   # Create issues (requires issues.json)
   python3 scripts/create_issues.py issues.json

   # Add to project
   ./scripts/add_to_project.sh 4 owner repo 64 151

   # Sync status fields
   python3 scripts/update_status.py PROJECT_ID 4 owner repo 64 151
   ```

### Issue Implementation Mode

1. **Work on specific issue:**
   ```bash
   python3 scripts/implement_issue.py 104
   ```

2. **Auto-select next issue:**
   ```bash
   # Next critical issue
   python3 scripts/implement_issue.py --auto-select --priority critical

   # Next payment issue (filtered by epic)
   python3 scripts/implement_issue.py --auto-select --epic booking-payment
   ```

3. **Follow Claude Code prompts:**
   - Script generates context analysis prompt
   - Claude Code analyzes codebase
   - Generates implementation plan
   - **Wait for your approval**
   - Implements with TDD workflow
   - Creates commit and PR

## Supporting Scripts

### Project Planning
- `create_labels.sh` - Create epic, status, priority, type labels
- `create_issues.py` - Bulk issue creation from JSON
- `add_to_project.sh` - Add issues to project board
- `update_status.py` - Sync status fields with labels

### Issue Implementation
- `implement_issue.py` - Orchestrate full implementation workflow
- `fetch_issue.py` - Fetch and parse issue details
- `select_issue.py` - Auto-select next issue by priority/epic

## Verified Success

### Project Planning Mode
Tested on RoadDux project:
- ✅ 88 issues created across 11 epics
- ✅ 100% success rate (0 failures)
- ✅ Full kanban board organization
- ✅ Comprehensive status documentation

**Time saved:** ~4-6 hours of manual project setup

### Issue Implementation Mode
Design approved and scripts implemented:
- ✅ Issue selection (specific and auto-select)
- ✅ Context analysis with epic-specific templates
- ✅ Plan generation with approval gate
- ✅ TDD workflow integration
- ✅ Quality gates (tests, types, lint)
- ✅ Commit and PR automation

**Time saved:** 1.5-3 hours per issue (2-4 hours manual → 30-45 min automated)

## See Also

- Full skill documentation: `SKILL.md`
- Design document: `../../docs/plans/2026-01-21-issue-implementation-automation-design.md`
- Example JSON structure in main skill file
- GitHub Projects v2 API docs (linked in References)
