# JikiME Worktree Examples

Purpose: Real-world usage examples and patterns for jikime worktree skill integration with JikiME-ADK workflow.

Version: 2.0.0
Last Updated: 2026-01-22

---

## Command Integration Examples

### Example 1: SPEC Development with Worktree

Scenario: Creating a new SPEC with automatic worktree setup

```bash
# Plan Phase - Create SPEC with worktree
/jikime:1-plan "User Authentication System" --worktree

# Output:
# SPEC created: SPEC-AUTH-001
# Worktree created: .jikime/worktrees/JikiME-ADK/SPEC-AUTH-001
#
# Next steps:
# 1. Navigate to worktree: eval $(jikime worktree go SPEC-AUTH-001)
# 2. Start development: /jikime:2-run SPEC-AUTH-001

# Development Phase - Implement in isolated environment
eval $(jikime worktree go SPEC-AUTH-001)
/jikime:2-run SPEC-AUTH-001

# Sync Phase - Synchronize and integrate
jikime worktree sync SPEC-AUTH-001
/jikime:3-sync SPEC-AUTH-001

# Cleanup Phase - Remove completed worktree
jikime worktree remove SPEC-AUTH-001
```

### Example 2: Parallel SPEC Development

Scenario: Working on multiple SPECs simultaneously

```bash
# Create multiple worktrees for parallel development
jikime worktree new SPEC-AUTH-001
jikime worktree new SPEC-PAY-001
jikime worktree new SPEC-DASH-001

# Navigate between worktrees using shell eval
eval $(jikime worktree go SPEC-AUTH-001)
# Work on authentication...

eval $(jikime worktree go SPEC-PAY-001)
# Work on payment system...

eval $(jikime worktree go SPEC-DASH-001)
# Work on dashboard...

# Check status of all worktrees
jikime worktree status --all

# Sync all worktrees
jikime worktree sync --all

# Clean up completed worktrees
jikime worktree clean --merged-only
```

### Example 3: Worktree in Development Commands

Scenario: Using worktree-aware DDD implementation

```bash
# /jikime:2-run automatically detects worktree environment
/jikime:2-run SPEC-AUTH-001

# Command behavior in worktree:
# - Detects worktree: SPEC-AUTH-001
# - Loads worktree-specific configuration
# - Executes DDD in isolated environment
# - Updates worktree metadata

# Manual worktree management during development
jikime worktree status SPEC-AUTH-001
jikime worktree sync SPEC-AUTH-001 --include "src/"
jikime worktree config get worktree_root
```

---

## Agent Integration Examples

### Example 4: Manager-Project with Worktree Setup

Agent Usage: Project initialization with worktree support

```python
# In manager-project agent context
Skill("jikime-workflow-worktree") # Load worktree patterns

# Setup project with worktree support
project_config = {
 "name": "User Authentication System",
 "worktree_enabled": True,
 "worktree_root": ".jikime/worktrees/UserAuth",
 "auto_create_worktree": True
}

# Create worktree after project setup
if project_config.get("worktree_enabled"):
 from jikime_worktree import WorktreeManager

 worktree_manager = WorktreeManager(
 repo_path=Path.cwd(),
 worktree_root=Path(project_config["worktree_root"]).expanduser()
 )

 worktree_info = worktree_manager.create(
 spec_id="SPEC-AUTH-001",
 template="authentication"
 )
```

### Example 5: Manager-Git with Worktree Branch Management

Agent Usage: Git operations with worktree awareness

```python
# In manager-git agent context
Skill("jikime-workflow-worktree") # Load worktree patterns

def create_feature_branch_with_worktree(spec_id: str, branch_name: str = None):
 """Create feature branch and associated worktree."""

 # Check if in worktree environment
 current_worktree = detect_worktree_environment()

 # Use default branch name if not provided
 if branch_name is None:
 branch_name = f"feature/{spec_id}"

 if current_worktree:
 # In worktree - create branch from worktree
 git_checkout(branch_name, create_new=True)

 # Update worktree registry
 update_worktree_branch(current_worktree, branch_name)
 else:
 # In main repo - create worktree
 from jikime_worktree import WorktreeManager

 worktree_manager = WorktreeManager(Path.cwd())
 worktree_manager.create(
 spec_id=spec_id,
 branch=branch_name
 )

# Usage in agent workflow
create_feature_branch_with_worktree("SPEC-AUTH-001")
```

---

## Workflow Integration Examples

### Example 6: Complete SPEC Development Workflow

End-to-End Example: Full SPEC development cycle with worktree

```bash
#!/bin/bash
# spec_development_workflow.sh

SPEC_ID="$1"
SPEC_DESCRIPTION="$2"

echo " Starting SPEC development workflow for $SPEC_ID"

# Phase 1: Plan (with worktree)
echo " Phase 1: Creating SPEC and worktree..."
/jikime:1-plan "$SPEC_DESCRIPTION" --worktree --spec-id "$SPEC_ID"

# Check if worktree was created successfully
if jikime worktree list --format json | jq -r ".worktrees[\"$SPEC_ID\"]" > /dev/null; then
 echo " Worktree $SPEC_ID created successfully"

 # Phase 2: Develop
 echo " Phase 2: Switching to worktree for development..."
 cd $(jikime worktree go "$SPEC_ID")

 # Development loop
 while true; do
 echo " Running DDD implementation..."
 /jikime:2-run "$SPEC_ID"

 echo " Continue development? (y/n)"
 read -r response
 if [[ ! "$response" =~ ^[Yy]$ ]]; then
 break
 fi
 done

 # Phase 3: Sync
 echo " Phase 3: Synchronizing worktree..."
 jikime worktree sync "$SPEC_ID"
 cd - # Return to main repository
 /jikime:3-sync "$SPEC_ID"

 # Phase 4: Cleanup (optional)
 echo " Phase 4: Clean up options"
 echo "Remove worktree $SPEC_ID? (y/n)"
 read -r cleanup_response
 if [[ "$cleanup_response" =~ ^[Yy]$ ]]; then
 jikime worktree remove "$SPEC_ID"
 echo " Worktree $SPEC_ID removed"
 fi

else
 echo " Worktree creation failed. Falling back to branch development."
 /jikime:1-plan "$SPEC_DESCRIPTION" --branch --spec-id "$SPEC_ID"
fi

echo " SPEC development workflow completed for $SPEC_ID"
```

### Example 7: Team Collaboration Workflow

Team Setup: Shared worktree configuration for team development

```bash
#!/bin/bash
# team_worktree_setup.sh

TEAM_NAME="$1"
PROJECT_NAME="$2"

echo " Setting up team worktree configuration for $TEAM_NAME"

# Create shared worktree root
WORKTREE_ROOT=".jikime/worktrees/$PROJECT_NAME"
mkdir -p "$WORKTREE_ROOT"

# Configure team registry
cat > "$WORKTREE_ROOT/.team-config.json" << EOF
{
 "team": "$TEAM_NAME",
 "project": "$PROJECT_NAME",
 "worktree_root": "$WORKTREE_ROOT",
 "shared_registry": true,
 "auto_sync": true,
 "cleanup_policy": "team_coordinated"
}
EOF

# Initialize shared registry
jikime worktree config set worktree_root "$WORKTREE_ROOT"
jikime worktree config set registry_type team

echo " Team worktree configuration completed"
echo "Team members can now join with: jikime worktree join --team $TEAM_NAME"
```

---

## Advanced Usage Examples

### Example 8: Custom Worktree Templates

Template Creation: Development environment templates

```python
# custom_worktree_templates.py

from pathlib import Path

def create_fullstack_template():
 """Create fullstack development template."""

 template_config = {
 "name": "fullstack",
 "description": "Fullstack development environment",
 "setup_commands": [
 "npm install",
 "pip install -r requirements.txt",
 "docker-compose up -d database",
 "echo 'Environment ready for fullstack development'"
 ],
 "files": {
 "docker-compose.yml": """version: '3.8'
services:
 database:
 image: postgres:13
 environment:
 POSTGRES_DB: app_development
 POSTGRES_USER: developer
 POSTGRES_PASSWORD: password
 ports:
 - "5432:5432"
 volumes:
 - postgres_data:/var/lib/postgresql/data

volumes:
 postgres_data:""",

 ".env.example": """# Environment Configuration
DATABASE_URL=postgresql://developer:password@localhost:5432/app_development
NODE_ENV=development
FLASK_ENV=development
DEBUG=true""",

 ".vscode/launch.json": """{
 "version": "0.2.0",
 "configurations": [
 {
 "name": "Debug Frontend",
 "type": "node",
 "request": "launch",
 "program": "${workspaceFolder}/src/frontend/index.js",
 "console": "integratedTerminal"
 },
 {
 "name": "Debug Backend",
 "type": "python",
 "request": "launch",
 "program": "${workspaceFolder}/src/backend/app.py",
 "console": "integratedTerminal"
 }
 ]
}"""
 },
 "env_vars": {
 "TEMPLATE_TYPE": "fullstack",
 "INCLUDE_DATABASE": "true",
 "INCLUDE_FRONTEND": "true",
 "INCLUDE_BACKEND": "true"
 }
 }

 # Save template
 template_path = Path.home() / ".jikime/worktree-templates" / "fullstack.json"
 template_path.parent.mkdir(parents=True, exist_ok=True)

 import json
 with open(template_path, 'w') as f:
 json.dump(template_config, f, indent=2)

 print(f" Fullstack template created: {template_path}")

# Usage
create_fullstack_template()

# Create worktree with template
# jikime worktree new SPEC-FULL-001 --template fullstack
```

### Example 9: Worktree Automation Script

Automation: Batch worktree operations

```python
# worktree_automation.py

import subprocess
import json
from pathlib import Path
from datetime import datetime

class WorktreeAutomation:
 def __init__(self, project_root: str):
 self.project_root = Path(project_root)

 def batch_create_worktrees(self, specs: list):
 """Create multiple worktrees from SPEC list."""

 results = []

 for spec in specs:
 spec_id = spec.get('id')
 template = spec.get('template', 'default')
 branch = spec.get('branch')

 try:
 print(f" Creating worktree: {spec_id}")

 cmd = ["jikime", "worktree", "new", spec_id]
 if template != 'default':
 cmd.extend(["--template", template])
 if branch:
 cmd.extend(["--branch", branch])

 result = subprocess.run(cmd, capture_output=True, text=True, check=True)

 worktree_info = {
 'spec_id': spec_id,
 'status': 'created',
 'path': self._extract_worktree_path(result.stdout),
 'created_at': datetime.utcnow().isoformat()
 }

 results.append(worktree_info)
 print(f" Worktree {spec_id} created successfully")

 except subprocess.CalledProcessError as e:
 error_info = {
 'spec_id': spec_id,
 'status': 'failed',
 'error': e.stderr,
 'created_at': datetime.utcnow().isoformat()
 }

 results.append(error_info)
 print(f" Failed to create worktree {spec_id}: {e.stderr}")

 return results

 def batch_sync_worktrees(self, spec_ids: list = None):
 """Sync multiple worktrees."""

 if spec_ids is None:
 # Get all active worktrees
 result = subprocess.run([
 "jikime", "worktree", "list", "--status", "active", "--format", "json"
 ], capture_output=True, text=True, check=True)

 worktrees = json.loads(result.stdout)
 spec_ids = list(worktrees['worktrees'].keys())

 results = []

 for spec_id in spec_ids:
 try:
 print(f" Syncing worktree: {spec_id}")

 result = subprocess.run([
 "jikime", "worktree", "sync", spec_id
 ], capture_output=True, text=True, check=True)

 sync_info = {
 'spec_id': spec_id,
 'status': 'synced',
 'details': result.stdout,
 'synced_at': datetime.utcnow().isoformat()
 }

 results.append(sync_info)
 print(f" Worktree {spec_id} synced successfully")

 except subprocess.CalledProcessError as e:
 error_info = {
 'spec_id': spec_id,
 'status': 'sync_failed',
 'error': e.stderr,
 'synced_at': datetime.utcnow().isoformat()
 }

 results.append(error_info)
 print(f" Failed to sync worktree {spec_id}: {e.stderr}")

 return results

 def generate_worktree_report(self):
 """Generate comprehensive worktree status report."""

 # Get worktree status
 status_result = subprocess.run([
 "jikime", "worktree", "status", "--all", "--format", "json"
 ], capture_output=True, text=True, check=True)

 worktrees = json.loads(status_result.stdout)

 # Generate report
 report = {
 'generated_at': datetime.utcnow().isoformat(),
 'total_worktrees': len(worktrees.get('worktrees', {})),
 'active_worktrees': len([
 w for w in worktrees.get('worktrees', {}).values()
 if w.get('status') == 'active'
 ]),
 'worktrees': worktrees.get('worktrees', {}),
 'recommendations': self._generate_recommendations(worktrees)
 }

 return report

 def _extract_worktree_path(self, output: str) -> str:
 """Extract worktree path from command output."""

 for line in output.split('\n'):
 if 'Path:' in line:
 return line.split('Path:')[-1].strip()
 return ""

 def _generate_recommendations(self, worktrees: dict) -> list:
 """Generate cleanup and optimization recommendations."""

 recommendations = []

 # Check for stale worktrees
 stale_worktrees = [
 w_id for w_id, w_info in worktrees.get('worktrees', {}).items()
 if self._is_stale(w_info)
 ]

 if stale_worktrees:
 recommendations.append({
 'type': 'cleanup',
 'message': f"Found {len(stale_worktrees)} stale worktrees: {', '.join(stale_worktrees)}",
 'action': 'jikime worktree clean --stale --days 30'
 })

 # Check for large worktrees
 large_worktrees = [
 w_id for w_id, w_info in worktrees.get('worktrees', {}).items()
 if w_info.get('metadata', {}).get('estimated_size', '0') > '500MB'
 ]

 if large_worktrees:
 recommendations.append({
 'type': 'optimization',
 'message': f"Found {len(large_worktrees)} large worktrees: {', '.join(large_worktrees)}",
 'action': 'jikime worktree optimize --analyze'
 })

 return recommendations

# Usage example
if __name__ == "__main__":
 automation = WorktreeAutomation("/path/to/project")

 # Create worktrees from spec list
 specs = [
 {'id': 'SPEC-AUTH-001', 'template': 'backend'},
 {'id': 'SPEC-PAY-001', 'template': 'backend'},
 {'id': 'SPEC-UI-001', 'template': 'frontend'}
 ]

 results = automation.batch_create_worktrees(specs)

 # Sync all worktrees
 sync_results = automation.batch_sync_worktrees()

 # Generate report
 report = automation.generate_worktree_report()

 print(f"Report generated: {len(report['worktrees'])} worktrees analyzed")
```

---

## Troubleshooting Examples

### Example 10: Common Issues and Solutions

Issue Resolution: Typical worktree problems and solutions

```bash
# Problem 1: Worktree creation fails
echo " Diagnosing worktree creation issues..."

# Check disk space
df -h ~/workflows/

# Check Git repository status
git status
git remote -v

# Try with verbose output
jikime worktree new SPEC-DEBUG-001 --verbose

# Problem 2: Worktree sync conflicts
echo " Resolving sync conflicts..."

# Check sync status
jikime worktree status SPEC-CONFLICT-001

# Interactive conflict resolution
jikime worktree sync SPEC-CONFLICT-001 --interactive

# Force sync (if appropriate)
jikime worktree sync SPEC-CONFLICT-001 --force

# Problem 3: Worktree registry corruption
echo " Repairing worktree registry..."

# Backup current registry
cp .jikime/worktrees/PROJECT/worktree-registry.json .jikime/worktrees/PROJECT/worktree-registry.json.backup

# Rebuild registry from worktree directories
jikime worktree config set registry_rebuild true
jikime worktree list --rebuild-registry

# Problem 4: Permission issues
echo " Fixing permission issues..."

# Check worktree permissions
ls -la .jikime/worktrees/PROJECT/

# Fix permissions
chmod -R 755 .jikime/worktrees/PROJECT/
```

---

Version: 2.0.0
Last Updated: 2026-01-22
Examples: Real-world usage patterns for jikime worktree integration
