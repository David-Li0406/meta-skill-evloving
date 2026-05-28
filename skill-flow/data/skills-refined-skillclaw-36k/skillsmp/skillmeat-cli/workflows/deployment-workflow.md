# Deployment Workflow

Safe artifact deployment to projects with user confirmation and error handling.

---

## Overview

This workflow guides artifact deployment from collection to project, ensuring user awareness and explicit permission at every step.

**Core Principles**:
- **Never auto-deploy**: Always request explicit user permission
- **Show before do**: Display deployment plan before execution
- **Clear communication**: Explain what will happen and where
- **Graceful errors**: Handle failures with helpful guidance

---

## Workflow Steps

### 1. Artifact Selection

**Identify the artifact** to deploy (from user request or task context).

**Validation**:
```bash
# Check if artifact exists in collection
skillmeat show <artifact-name>
```

**If not found**:
```bash
# Search for similar artifacts
skillmeat search <query>
```

**Output**: Artifact name, type, source, and current deployment status.

---

### 2. Plan Generation

**Show deployment plan** to user with clear details.

**Plan Format**:
```
Deployment Plan for: <artifact-name>

Source: <github-url-or-local-path>
Type: <skill|command|agent>
Target: .claude/<type>s/<artifact-name>/

Files to be created:
  - .claude/skills/<artifact-name>/SKILL.md
  - .claude/skills/<artifact-name>/README.md
  - .claude/skills/<artifact-name>/scripts/process.js
  (... list all files if known)

Current status: <not-in-collection|in-collection|already-deployed>

Required steps:
  1. Add to collection (if needed)
  2. Deploy to project
```

**Example**:
```
Deployment Plan for: pdf-processor

Source: anthropics/skills/document-skills/pdf@latest
Type: skill
Target: .claude/skills/pdf-processor/

Files to be created:
  - .claude/skills/pdf-processor/SKILL.md
  - .claude/skills/pdf-processor/scripts/extract-text.js
  - .claude/skills/pdf-processor/scripts/extract-images.js

Current status: not-in-collection

Required steps:
  1. Add to collection
  2. Deploy to project
```

---

### 3. Permission Request

**Ask explicit permission** before any filesystem changes.

#### Single Artifact

**Template**:
```
Deploy <artifact-name> to this project?

This will:
- Add <artifact-name> to your collection (if needed)
- Create .claude/<type>s/<artifact-name>/ directory
- Copy <N> files to the project

Proceed? (yes/no)
```

**Example**:
```
Deploy pdf-processor to this project?

This will:
- Add pdf-processor to your collection
- Create .claude/skills/pdf-processor/ directory
- Copy 3 files to the project

Proceed? (yes/no)
```

#### Multiple Artifacts

**Template**:
```
Deploy the following artifacts to this project?

1. <artifact-1> (<type>)
2. <artifact-2> (<type>)
3. <artifact-3> (<type>)

This will:
- Add <N> artifacts to your collection (if needed)
- Create <N> directories in .claude/
- Copy <total> files to the project

Proceed? (yes/no/select)
```

**Example**:
```
Deploy the following document processing skills?

1. pdf-processor (skill)
2. docx-processor (skill)
3. xlsx-processor (skill)

This will:
- Add 3 skills to your collection
- Create 3 directories in .claude/skills/
- Copy 12 files to the project

Proceed? (yes/no/select)
```

**Select Option**: User can choose which artifacts to deploy.

#### Session Permission

For iterative tasks where multiple artifacts might be needed:

**Template**:
```
This task may require multiple artifacts. Grant session permission to add artifacts as needed?

If yes, I will:
- Show deployment plan for each artifact
- Ask for confirmation before adding
- Proceed with deployment on approval

If no, I will:
- Ask permission for each individual artifact

Grant session permission? (yes/no)
```

**Session Permission Rules**:
- Still show plan for each artifact
- Still ask "Add <artifact>?" before each
- Reduces verbosity for multi-artifact tasks
- Can be revoked mid-session

---

### 4. Execution

**Execute deployment** only after explicit permission.

#### Step 4a: Add to Collection (if needed)

```bash
# Check if already in collection
skillmeat show <artifact-name> 2>/dev/null

# If not found, add to collection
if [ $? -ne 0 ]; then
  skillmeat add <type> <source>
fi
```

**Example**:
```bash
skillmeat add skill anthropics/skills/document-skills/pdf@latest
```

**Output**: Confirm addition to collection.

#### Step 4b: Deploy to Project

```bash
# Deploy artifact to current project
skillmeat deploy <artifact-name> --project .
```

**Example**:
```bash
skillmeat deploy pdf-processor --project .
```

**Output**: Confirm deployment location.

#### Error Handling During Execution

**Artifact not found**:
```
Error: Artifact 'pdf-processor' not found in collection or marketplace.

Suggestions:
- Search marketplace: skillmeat search pdf
- Check source format: user/repo/path/to/artifact[@version]
- Verify artifact name spelling
```

**Already deployed**:
```
Artifact 'pdf-processor' is already deployed to this project.

Location: .claude/skills/pdf-processor/

No action needed. Would you like to:
- Redeploy (overwrite existing files)?
- Update to latest version?
- Skip and continue?
```

**Permission denied**:
```
Error: Permission denied when writing to .claude/skills/

Suggestions:
- Check directory permissions: ls -la .claude/
- Ensure .claude/ directory exists: mkdir -p .claude/skills/
- Run with appropriate permissions

Fix and retry? (yes/no)
```

**Network error** (for remote sources):
```
Error: Failed to fetch artifact from GitHub (network timeout).

Retrying in 2 seconds... (attempt 1/3)
```

**Retry logic**:
- Attempt 1: Wait 2 seconds
- Attempt 2: Wait 5 seconds
- Attempt 3: Wait 10 seconds
- After 3 failures: Abort with error

---

### 5. Confirmation

**Confirm successful deployment** with clear output.

**Template**:
```
✓ Successfully deployed <artifact-name>!

Location: .claude/<type>s/<artifact-name>/
Files created: <N>

Next steps:
- <artifact-specific-usage-hint>
- View documentation: cat .claude/<type>s/<artifact-name>/SKILL.md
- Test artifact: <example-command>

<artifact-name> is now ready to use.
```

**Example**:
```
✓ Successfully deployed pdf-processor!

Location: .claude/skills/pdf-processor/
Files created: 3

Next steps:
- Use skill: "Extract text from report.pdf"
- View documentation: cat .claude/skills/pdf-processor/SKILL.md
- Test extraction: skillmeat run pdf-processor --file test.pdf

pdf-processor is now ready to use.
```

---

## Permission Protocol Reference

### Quick Decision Matrix

| Scenario | Permission Type | Template |
|----------|----------------|----------|
| Single artifact, one-time task | Single | "Deploy <artifact>?" |
| Multiple artifacts, related | Multiple | "Deploy all <category> skills?" |
| Iterative task, unknown needs | Session | "Grant session permission?" |
| Already deployed | None | "Already deployed. Redeploy?" |

### Permission Verbosity Levels

**Level 1: Minimal** (session permission granted)
```
Add pdf-processor? (yes/no)
→ Deploying pdf-processor...
✓ Deployed to .claude/skills/pdf-processor/
```

**Level 2: Standard** (single artifact)
```
Deploy pdf-processor to this project?
This will create .claude/skills/pdf-processor/ with 3 files.
Proceed? (yes/no)
→ Adding to collection...
→ Deploying to project...
✓ Successfully deployed!
```

**Level 3: Detailed** (multiple artifacts)
```
Deployment Plan for: document-skills

Artifacts:
1. pdf-processor (skill) - 3 files
2. docx-processor (skill) - 4 files
3. xlsx-processor (skill) - 5 files

This will:
- Add 3 skills to collection
- Create 3 directories in .claude/skills/
- Copy 12 files total

Proceed? (yes/no/select)
→ [detailed execution steps]
✓ All artifacts deployed successfully!
```

---

## Error Recovery Patterns

### Artifact Not Found

**Detection**:
```bash
skillmeat show <artifact-name>
# Exit code 1 = not found
```

**Recovery**:
1. Suggest search: `skillmeat search <query>`
2. Ask user to provide source: "What's the GitHub URL or local path?"
3. Retry with user-provided source

### Already Deployed

**Detection**:
```bash
skillmeat deploy <artifact-name> --project .
# Output: "already deployed" or exit code 2
```

**Recovery**:
1. Inform user: "Already deployed to .claude/skills/<name>/"
2. Offer options:
   - Skip (do nothing)
   - Redeploy (overwrite)
   - Update (fetch latest version)

### Permission Denied

**Detection**:
```bash
# Exit code 13 or error message contains "Permission denied"
```

**Recovery**:
1. Check directory existence: `ls -la .claude/`
2. Suggest fix: `mkdir -p .claude/skills/`
3. Offer to retry after user fixes permissions

### Network Error

**Detection**:
```bash
# Error message contains "timeout", "connection", "unreachable"
```

**Recovery**:
1. Retry with exponential backoff (3 attempts)
2. After 3 failures:
   - Suggest checking network connection
   - Suggest using local source if available
   - Offer to continue without this artifact

---

## Integration with Task Execution

When deploying artifacts as part of a larger task:

### Pre-Task Deployment

If artifact needed before starting main task:

```
To complete this task, I need the pdf-processor skill.

Deploy pdf-processor now? (yes/no/skip-task)
```

**skip-task**: Abort entire task if artifact is required.

### Mid-Task Deployment

If artifact needed during task execution:

```
I need the xlsx-processor skill to continue.

Deploy xlsx-processor? (yes/no/manual)
```

**manual**: Pause task, let user deploy manually, then resume.

### Post-Task Deployment

If artifact would help for future similar tasks:

```
Task complete! For future document processing, consider adding:
- docx-processor (for Word documents)
- xlsx-processor (for Excel spreadsheets)

Deploy these skills? (yes/no/later)
```

**later**: Save suggestion for next session.

---

## Examples

### Example 1: Simple Deployment

**User**: "Add the PDF skill"

**Claude**:
```
Deploy pdf-processor to this project?

Source: anthropics/skills/document-skills/pdf@latest
Type: skill
Target: .claude/skills/pdf-processor/

This will:
- Add pdf-processor to your collection
- Create .claude/skills/pdf-processor/ directory
- Copy 3 files to the project

Proceed? (yes/no)
```

**User**: "yes"

**Claude**:
```bash
skillmeat add skill anthropics/skills/document-skills/pdf@latest
skillmeat deploy pdf-processor --project .
```

**Output**:
```
✓ Successfully deployed pdf-processor!

Location: .claude/skills/pdf-processor/
Files created: 3

pdf-processor is now ready to use.
```

### Example 2: Multiple Artifacts

**User**: "Add all document skills"

**Claude**:
```
Deploy the following document processing skills?

1. pdf-processor (skill)
2. docx-processor (skill)
3. xlsx-processor (skill)

This will:
- Add 3 skills to your collection
- Create 3 directories in .claude/skills/
- Copy 12 files to the project

Proceed? (yes/no/select)
```

**User**: "yes"

**Claude**:
```bash
# Add all to collection
skillmeat add skill anthropics/skills/document-skills/pdf@latest
skillmeat add skill anthropics/skills/document-skills/docx@latest
skillmeat add skill anthropics/skills/document-skills/xlsx@latest

# Deploy all
skillmeat deploy pdf-processor --project .
skillmeat deploy docx-processor --project .
skillmeat deploy xlsx-processor --project .
```

**Output**:
```
✓ Successfully deployed all document skills!

Deployed:
- pdf-processor → .claude/skills/pdf-processor/
- docx-processor → .claude/skills/docx-processor/
- xlsx-processor → .claude/skills/xlsx-processor/

All skills are now ready to use.
```

### Example 3: Session Permission

**User**: "Help me process various document types"

**Claude**:
```
This task may require multiple document processing skills.

Grant session permission to add artifacts as needed?

If yes, I will show deployment plan and ask confirmation before adding each skill.

Grant session permission? (yes/no)
```

**User**: "yes"

**Claude**:
```
Session permission granted. I'll deploy artifacts as needed with confirmation.

Starting with pdf-processor for PDF files.

Add pdf-processor? (yes/no)
```

**User**: "yes"

**Claude**:
```bash
skillmeat add skill anthropics/skills/document-skills/pdf@latest
skillmeat deploy pdf-processor --project .
```

**Later in session**:
```
I need xlsx-processor for Excel files.

Add xlsx-processor? (yes/no)
```

### Example 4: Already Deployed

**User**: "Add the PDF skill"

**Claude**:
```bash
skillmeat show pdf-processor
```

**Output**:
```
pdf-processor is already deployed to this project.

Location: .claude/skills/pdf-processor/
Version: v1.2.0

No action needed. Would you like to:
- Redeploy (overwrite existing files)?
- Update to latest version?
- Skip and continue?
```

**User**: "skip"

**Claude**:
```
Skipping deployment. Using existing pdf-processor skill.
```

### Example 5: Error Recovery

**User**: "Add the canvas skill"

**Claude**:
```bash
skillmeat show canvas
# Not found
skillmeat search canvas
```

**Output**:
```
Artifact 'canvas' not found in collection.

Search results for 'canvas':
1. canvas-design (anthropics/skills/canvas-design@latest)
2. canvas-editor (community/skills/canvas-editor@v2.0.0)

Did you mean canvas-design? (yes/no/manual)
```

**User**: "yes"

**Claude**:
```
Deploy canvas-design to this project?

Source: anthropics/skills/canvas-design@latest
Type: skill
Target: .claude/skills/canvas-design/

Proceed? (yes/no)
```

---

## Safety Checklist

Before deploying any artifact, verify:

- [ ] Artifact source is valid (GitHub URL or local path)
- [ ] User has granted explicit permission
- [ ] Target directory is writable
- [ ] No conflicting artifacts already deployed (or user approved overwrite)
- [ ] Network connectivity (for remote sources)
- [ ] Disk space available (for large artifacts)

After deployment, confirm:

- [ ] Files created successfully
- [ ] Artifact appears in `skillmeat list --deployed`
- [ ] User notified of deployment location
- [ ] Next steps provided (how to use artifact)

---

## Reference

- **CLI Commands**: `cli-reference.md`
- **Search Workflow**: `search-workflow.md`
- **Error Codes**: `troubleshooting.md`
- **Artifact Types**: See skillmeat documentation
