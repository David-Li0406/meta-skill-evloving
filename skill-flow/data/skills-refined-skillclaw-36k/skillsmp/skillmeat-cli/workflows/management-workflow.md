# Artifact Management Workflow

Guidelines for listing, inspecting, syncing, and removing artifacts in SkillMeat.

---

## Core Operations

| User Intent | Command Pattern | Output |
|-------------|----------------|--------|
| "What do I have?" | `skillmeat list` | Collection artifacts |
| "What's deployed here?" | `skillmeat list --project .` | Project artifacts |
| "Tell me about X" | `skillmeat show <name>` | Artifact details |
| "Check for updates" | `skillmeat diff <name>` | Version comparison |
| "Update everything" | `skillmeat sync --all` | Sync all artifacts |
| "Remove X" | `skillmeat remove <name>` | Remove from collection |
| "Undeploy X" | `skillmeat undeploy <name>` | Remove from project |

---

## Listing Artifacts

### List Collection Artifacts

**User Says**: "What skills do I have?", "Show my artifacts", "List everything"

```bash
# All artifacts in collection
skillmeat list

# Filter by type
skillmeat list --type skill
skillmeat list --type command
skillmeat list --type agent

# JSON output (for parsing)
skillmeat list --json
```

**Example Response**:
```
Collection Artifacts:
  Skills (3):
    • canvas-design (v1.2.0)
    • pdf (v2.0.1)
    • postgresql-psql (v1.0.0)

  Commands (1):
    • quick-commit (v1.0.0)
```

### List Project Deployments

**User Says**: "What's deployed here?", "Show project artifacts", "What's in this project?"

```bash
# Artifacts deployed to current project
skillmeat list --project .

# Deployed to specific project
skillmeat list --project /path/to/project

# Filter deployed artifacts by type
skillmeat list --project . --type skill
```

**Example Response**:
```
Deployed Artifacts (.claude/):
  Skills (2):
    • canvas-design → .claude/skills/canvas-design/
    • pdf → .claude/skills/pdf/

  Agents (1):
    • python-backend-engineer → .claude/agents/python-backend-engineer.md
```

### Filtering and Formatting

```bash
# Multiple filters
skillmeat list --type skill --source anthropics

# Compact output
skillmeat list --compact

# Detailed output
skillmeat list --verbose

# JSON for parsing
skillmeat list --json | jq '.[] | select(.type == "skill")'
```

---

## Inspecting Artifacts

### Show Artifact Details

**User Says**: "Tell me about X", "Show me the Y skill", "What does Z do?"

```bash
# Summary view (default)
skillmeat show <artifact-name>

# Full details
skillmeat show <artifact-name> --full

# JSON output
skillmeat show <artifact-name> --json
```

**Example Summary**:
```
Artifact: canvas-design
Type: Skill
Source: anthropics/skills/canvas-design
Version: v1.2.0 (latest)
Status: Deployed to project

Description:
  Create and edit visual designs using Claude's canvas interface.
  Supports SVG, HTML/CSS, and interactive mockups.

Deployed To:
  • Current project (.claude/skills/canvas-design/)

Last Updated: 2 days ago
```

**Example Full Details**:
```
Artifact: canvas-design
Type: Skill
Source: anthropics/skills/canvas-design
Version: v1.2.0
Resolved SHA: abc123def456
Status: Deployed to project

Description:
  [Full description from SKILL.md]

Files:
  • SKILL.md (12 KB)
  • templates/svg-template.html (2 KB)
  • scripts/generate-mockup.js (5 KB)

Dependencies:
  None

Deployments:
  • /Users/you/projects/myapp/.claude/skills/canvas-design/

Locked: Yes
Locked At: 2025-12-20T10:30:00Z

Metadata:
  Author: Anthropic
  License: MIT
  Tags: design, frontend, ui
```

### Show Version Information

```bash
# Check current vs available versions
skillmeat show <name> --versions

# Show changelog
skillmeat show <name> --changelog
```

---

## Syncing and Updating

### Check for Updates

**User Says**: "Check for updates", "Is X up to date?", "What's new?"

```bash
# Check single artifact
skillmeat diff <artifact-name>

# Check all artifacts
skillmeat diff --all

# Check only deployed artifacts
skillmeat diff --project .
```

**Example Response**:
```
Checking for updates...

Updates Available (2):
  • canvas-design: v1.2.0 → v1.3.0
    - Added accessibility features
    - Fixed SVG export bug
    - Performance improvements

  • pdf: v2.0.1 → v2.1.0
    - Added table extraction
    - Better OCR support

Up to Date (1):
  • postgresql-psql: v1.0.0 (latest)
```

### Sync Artifacts

**User Says**: "Update X", "Sync everything", "Get the latest version"

```bash
# Sync specific artifact
skillmeat sync <artifact-name>

# Sync all artifacts
skillmeat sync --all

# Sync only deployed artifacts
skillmeat sync --project .

# Dry run (show what would be updated)
skillmeat sync --all --dry-run
```

**Safety Prompts**:
```
Syncing will update 2 artifacts:
  • canvas-design: v1.2.0 → v1.3.0
  • pdf: v2.0.1 → v2.1.0

This will update deployed instances in 1 project:
  • Current project (.claude/)

Continue? [y/N]:
```

**After Sync**:
```
Synced 2 artifacts:
  ✓ canvas-design updated to v1.3.0
  ✓ pdf updated to v2.1.0

Deployments updated:
  ✓ Current project (.claude/)
```

### Sync Specific Version

```bash
# Sync to specific version
skillmeat sync <artifact-name> --version v1.0.0

# Sync to latest
skillmeat sync <artifact-name> --version latest

# Sync to commit SHA
skillmeat sync <artifact-name> --version abc123
```

---

## Removing Artifacts

### Remove from Collection

**User Says**: "Remove X", "Uninstall Y", "Delete Z from my collection"

```bash
# Remove from collection
skillmeat remove <artifact-name>

# Force remove (skip confirmations)
skillmeat remove <artifact-name> --force
```

**Safety Prompts**:
```
This will remove 'canvas-design' from your collection.

Deployed Instances (1):
  • Current project (.claude/skills/canvas-design/)

What would you like to do?
  [1] Remove from collection AND undeploy from all projects
  [2] Remove from collection, keep deployments
  [3] Cancel

Choice [1-3]:
```

**After Removal**:
```
Removed 'canvas-design' from collection.
Undeployed from 1 project.
```

### Undeploy from Project

**User Says**: "Undeploy X", "Remove Y from this project", "Uninstall Z here"

```bash
# Undeploy from current project
skillmeat undeploy <artifact-name>

# Undeploy from specific project
skillmeat undeploy <artifact-name> --project /path/to/project

# Force undeploy (skip confirmations)
skillmeat undeploy <artifact-name> --force
```

**Safety Prompts**:
```
This will undeploy 'pdf' from the current project.

Files to Remove:
  • .claude/skills/pdf/

This artifact is NOT used by any other artifacts.

Continue? [y/N]:
```

**Dependency Warning**:
```
Warning: 'database-migrations' depends on 'postgresql-psql'

Other deployed artifacts using 'postgresql-psql':
  • database-migrations (agent)

If you undeploy 'postgresql-psql', these artifacts may not work correctly.

Continue anyway? [y/N]:
```

**After Undeploy**:
```
Undeployed 'pdf' from current project.
Removed: .claude/skills/pdf/
```

### Batch Removal

```bash
# Remove multiple artifacts
skillmeat remove skill-1 skill-2 skill-3

# Remove by type
skillmeat remove --type command --all

# Remove unused artifacts
skillmeat remove --unused
```

---

## Common Scenarios

### Scenario 1: "What skills do I have?"

**Workflow**:
```
User: "What skills do I have?"
Agent: [Runs: skillmeat list --type skill]
```

**Response**:
```
You have 3 skills in your collection:

1. canvas-design (v1.2.0)
   - Create visual designs using canvas interface
   - Deployed to current project

2. pdf (v2.0.1)
   - Extract and process PDF documents
   - Deployed to current project

3. postgresql-psql (v1.0.0)
   - PostgreSQL database operations
   - Not deployed
```

### Scenario 2: "Tell me about the PDF skill"

**Workflow**:
```
User: "Tell me about the PDF skill"
Agent: [Runs: skillmeat show pdf]
```

**Response**:
```
The 'pdf' skill (v2.0.1) from anthropics/example-skills:

Extract text, tables, and metadata from PDF documents. Supports:
- Text extraction with layout preservation
- Table detection and conversion to CSV
- PDF form filling
- Merge and split operations

This skill is deployed to the current project at:
.claude/skills/pdf/

Last updated 2 days ago. Up to date with latest version.
```

### Scenario 3: "Update all my skills"

**Workflow**:
```
User: "Update all my skills"
Agent: [Runs: skillmeat diff --all]
       [If updates found: skillmeat sync --all]
```

**Response**:
```
Checking for updates...

Found 2 updates:
- canvas-design: v1.2.0 → v1.3.0
- pdf: v2.0.1 → v2.1.0

I'll update these for you.

[After sync]
✓ Updated canvas-design to v1.3.0
✓ Updated pdf to v2.1.0
```

### Scenario 4: "Remove the canvas skill"

**Workflow**:
```
User: "Remove the canvas skill"
Agent: [Runs: skillmeat remove canvas-design]
       [Shows confirmation prompt]
```

**Response**:
```
'canvas-design' is deployed to the current project.

I can:
1. Remove it from your collection AND undeploy it from this project
2. Just remove it from your collection (keep deployment)

Which would you prefer?

User: "Remove it completely"
Agent: [Confirms removal]

Removed 'canvas-design' from collection.
Undeployed from current project.
```

---

## Safety Checks

### Before Removing Artifacts

1. **Check deployments**: List all projects using artifact
2. **Check dependencies**: Warn if other artifacts depend on it
3. **Confirm action**: Always ask before removing
4. **Show impact**: Display what will be deleted

### Confirmation Flow

```
Step 1: Identify what will be affected
  - Collection entry
  - Deployed instances
  - Dependent artifacts

Step 2: Present options
  - Remove from collection only
  - Remove from collection + undeploy
  - Cancel

Step 3: Execute with feedback
  - Show progress
  - Confirm completion
  - Report any errors
```

### Dependency Detection

```bash
# Before removing artifact, check:
1. Does any other artifact import it?
2. Is it referenced in any agent/command/hook?
3. Is it in any bundle?

# Show warnings:
Warning: Removing 'X' will affect:
  • Artifact Y imports X
  • Bundle Z includes X
```

---

## JSON Output for Parsing

All commands support `--json` for programmatic use:

```bash
# List artifacts
skillmeat list --json | jq '.[] | select(.deployed == true)'

# Show artifact
skillmeat show pdf --json | jq '.version'

# Check updates
skillmeat diff --all --json | jq '.[] | select(.update_available == true)'
```

**JSON Schema**:
```json
{
  "artifacts": [
    {
      "name": "canvas-design",
      "type": "skill",
      "version": "v1.2.0",
      "source": "anthropics/skills/canvas-design",
      "deployed": true,
      "deployments": [".claude/skills/canvas-design/"],
      "update_available": true,
      "latest_version": "v1.3.0"
    }
  ]
}
```

---

## Best Practices

### For Users

- **List before removing**: Always check what will be affected
- **Review updates**: Use `diff` before `sync` to see changes
- **Keep backups**: Consider snapshotting before major syncs
- **Check dependencies**: Be cautious when removing widely-used artifacts

### For AI Agents

- **Respect permissions**: Never remove/undeploy without user confirmation
- **Show impact**: Always display what will be affected
- **Provide context**: Explain why an artifact might be needed
- **Graceful degradation**: If artifact is missing, explain alternatives

---

## Anti-Patterns

### Don't Do This

- **Auto-remove**: Never remove artifacts without asking
  ```
  ❌ User: "I don't use canvas"
  ❌ Agent: [Removes canvas-design]
  ```

- **Force operations**: Don't use `--force` unless user explicitly requests
  ```
  ❌ skillmeat remove canvas --force
  ```

- **Ignore dependencies**: Don't remove artifacts that others depend on
  ```
  ❌ Removing 'postgres' while 'migrations' depends on it
  ```

- **Skip confirmations**: Always show what will be affected
  ```
  ❌ Removing without showing deployment locations
  ```

### Do This Instead

- **Ask first**:
  ```
  ✓ User: "I don't use canvas"
  ✓ Agent: "Would you like me to remove canvas-design from the project?"
  ```

- **Show impact**:
  ```
  ✓ Removing 'canvas-design' will:
      - Delete .claude/skills/canvas-design/
      - Remove from collection
    Continue? [y/N]
  ```

- **Check dependencies**:
  ```
  ✓ Warning: 'migrations' depends on 'postgres'
    Remove anyway? [y/N]
  ```

- **Confirm safely**:
  ```
  ✓ This will remove 'pdf' from:
      • Collection
      • Current project (.claude/)
    Proceed? [y/N]
  ```

---

## Troubleshooting

### "Artifact not found"

```
User: "Remove the docx skill"
Agent: "I don't see 'docx' in your collection. Did you mean 'pdf' or 'xlsx'?"
```

### "Permission denied"

```
Error: Permission denied removing .claude/skills/canvas-design/

Try:
  sudo skillmeat undeploy canvas-design
Or:
  Check file permissions
```

### "Artifact in use"

```
Warning: 'postgresql-psql' is used by:
  • database-migrations (agent)
  • backup-script (command)

You can still remove it, but these artifacts may not work.
Continue? [y/N]
```

---

## Related Workflows

- **Discovery**: `workflows/discovery-workflow.md`
- **Deployment**: See SKILL.md "Deployment: Adding Artifacts"
- **Agent Self-Enhancement**: `workflows/agent-self-enhancement.md`
