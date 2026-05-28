# Document Project - Workflow Steps Reference

This file contains the detailed workflow steps for the document-project skill.

## Step 0: Load Configuration

**[[AGENT: Execute this step first, then confirm completion before proceeding]]**

- Load `.prism/core-config.yaml` from the project root
- If file does not exist, HALT and inform user: "core-config.yaml not found. This task requires configuration. Please ensure PRISM is properly installed."
- Look for `documentation.output_folder` in config, default to `docs/project/` if not found
- Store as `{{output_folder}}`
- **Announce to user:** "Document Project Task Starting - Output: {{output_folder}}"
- **Announce to user:** "Step 0 Complete: Configuration loaded"

## Step 1: Check Existing Documentation

**[[AGENT: Execute this step only after Step 0 is complete]]**

Check if `{{output_folder}}/index.md` exists.

**If index.md EXISTS:**

Ask user:
```
I found existing project documentation generated on {{existing_doc_date}}.

What would you like to do?

1. **Re-scan entire project** - Update all documentation with latest changes
2. **Deep-dive into specific area** - Generate detailed documentation for a particular feature/module/folder
3. **Cancel** - Keep existing documentation as-is

Your choice [1/2/3]:
```

- If user selects **1**: Set `workflow_mode = "full_rescan"` -> Continue to Step 2
- If user selects **2**: Set `workflow_mode = "deep_dive"` -> Jump to Step 6 (Deep-Dive Mode)
- If user selects **3**: Display "Keeping existing documentation. Exiting." -> EXIT TASK

**If index.md DOES NOT EXIST:**

- Set `workflow_mode = "initial_scan"`
- **Announce to user:** "No existing documentation found. Starting initial project scan..."
- **Announce to user:** "Workflow mode: initial_scan"
- **Announce to user:** "Step 1 Complete: Workflow mode determined"
- **PROCEED IMMEDIATELY TO STEP 2** (do not wait for user input)

## Step 2: Select Scan Level

**[[AGENT: Execute this step only after Step 1 is complete and workflow_mode is set]]**

**Announce to user:** "Step 2: Select Scan Depth"

Ask user:
```
Choose your scan depth level:

**1. Quick Scan** (2-5 minutes) [DEFAULT]
   - Pattern-based analysis without reading source files
   - Scans: Config files, package manifests, directory structure
   - Best for: Quick project overview, initial understanding
   - File reading: Minimal (configs, README, package.json, etc.)

**2. Deep Scan** (10-30 minutes)
   - Reads files in critical directories based on project type
   - Scans: All critical paths from documentation requirements
   - Best for: Comprehensive documentation for PRD creation
   - File reading: Selective (key files in critical directories)

**3. Exhaustive Scan** (30-120 minutes)
   - Reads ALL source files in project
   - Scans: Every source file (excludes node_modules, dist, build)
   - Best for: Complete analysis, migration planning, detailed audit
   - File reading: Complete (all source files)

Your choice [1/2/3] (default: 1):
```

- Store user selection as `{{scan_level}}`: "quick" | "deep" | "exhaustive"
- If user presses enter without selecting, use `documentation.default_scan_level` from config, or default to "quick"
- **Announce to user:** "Using {{scan_level}} Scan"
- **Announce to user:** "Step 2 Complete: Scan level selected"

## Step 3: Initialize State File

**[[AGENT: Execute this step only after Step 2 is complete]]**

**Announce to user:** "Step 3: Initialize State Tracking"

Create state file at: `{{output_folder}}/project-scan-report.json`

Write initial state:
```json
{
  "workflow_version": "1.2.0-prism",
  "timestamps": {
    "started": "{{current_timestamp}}",
    "last_updated": "{{current_timestamp}}"
  },
  "mode": "{{workflow_mode}}",
  "scan_level": "{{scan_level}}",
  "project_root": "{{project_root_path}}",
  "output_folder": "{{output_folder}}",
  "completed_steps": [],
  "current_step": "step_1",
  "findings": {},
  "outputs_generated": ["project-scan-report.json"],
  "resume_instructions": "Starting from step 1"
}
```

**Announce to user:** "Step 3 Complete: State file initialized at {{output_folder}}/project-scan-report.json"

**CRITICAL:** Update this state file after EVERY step completion with:
- Step ID
- Human-readable summary (what was actually done)
- Precise timestamp
- Any outputs written

## Step 4: Detect Project Structure

**[[AGENT: Execute this step only after Step 3 is complete]]**

**Announce to user:** "Step 4: Analyzing Project Structure"

### 4.1 Scan Project Root

Ask user: "What is the root directory of the project to document?" (default: current working directory)

Store as `{{project_root_path}}`

Scan `{{project_root_path}}` for key indicators:
- Directory structure (presence of client/, server/, api/, src/, app/, skills/, etc.)
- Key files (package.json, .prism/, .claude/, commands/, tasks/, etc.)
- Technology markers (Node.js, TypeScript, Python, Go, Ruby, etc.)

### 4.2 Detect Project Type

Based on indicators, classify as one of:
- **claude-code-plugin**: PRISM-style plugins with skills/commands/tasks
- **web**: Web applications (React, Vue, Angular, etc.)
- **mobile**: Mobile apps (React Native, Flutter, etc.)
- **backend**: API servers (Express, FastAPI, Rails, etc.)
- **cli**: Command-line tools
- **library**: Reusable libraries/packages
- **desktop**: Desktop applications (Electron, Tauri, etc.)
- **game**: Game development projects
- **data**: Data pipelines and ETL
- **extension**: Browser extensions
- **infra**: Infrastructure as Code
- **embedded**: Embedded systems

### 4.3 Detect Multi-Part Structure

Check if project has multiple distinct parts (e.g., client/ and server/, or skills/ and commands/):

If multiple parts detected:
```
I detected multiple parts in this project:
{{detected_parts_list}}

Is this correct? Should I document each part separately? [y/n]
```

- If yes: Set `repository_type = "multi-part"` and create entry for each part
- If no: Ask user to specify correct structure

If single cohesive project:
- Set `repository_type = "monolith"`

### 4.4 Confirm with User

Display:
```
I've classified this project:

Type: {{project_type}}
Structure: {{repository_type}}
Parts: {{parts_count}}
{{parts_summary}}

Does this look correct? [y/n/edit]
```

- If no/edit: Allow user to correct classification
- Store final classification in state file
- **Announce to user:** "Step 4 Complete: Project classified as {{repository_type}} {{project_type}}"

### 4.5 Update State File

Add to state file:
```json
{
  "completed_steps": [
    {
      "step": "step_4",
      "status": "completed",
      "timestamp": "{{now}}",
      "summary": "Classified as {{repository_type}} {{project_type}} with {{parts_count}} parts"
    }
  ],
  "current_step": "step_5",
  "findings": {
    "project_classification": {
      "repository_type": "{{repository_type}}",
      "project_type": "{{project_type}}",
      "parts_count": {{parts_count}}
    }
  }
}
```

## Step 5: Comprehensive Project Scanning

**[[AGENT: Execute this step only after Step 4 is complete]]**

**Announce to user:** "Step 5: Scanning Project ({{scan_level}} mode)"

Execute scanning based on `{{scan_level}}` and `{{project_type}}`:

### 5.1 For QUICK Scan
- Use pattern matching only - do NOT read source files
- Use glob to find files by pattern
- Extract information from filenames, directory structure, and config files
- Identify: Entry points, config files, test patterns, critical directories

### 5.2 For DEEP Scan
- Read files in critical directories based on project type
- For claude-code-plugin: Read all SKILL.md files, sample tasks, sample commands
- For web: Read key components, API routes, data models
- For backend: Read API endpoints, database models, services
- Apply BATCHING: Process one subfolder at a time, write outputs immediately, purge context

### 5.3 For EXHAUSTIVE Scan
- Read ALL source files (excluding node_modules, .git, dist, build, coverage)
- Extract complete file inventory with exports, imports, dependencies
- Document all patterns, architectural decisions, code organization
- Apply BATCHING: Process subfolders one at a time to manage token usage

### 5.4 Extract Key Information

For each part, gather:
- **Technology Stack**: Languages, frameworks, versions, dependencies
- **Architecture Pattern**: MVC, microservices, plugin system, etc.
- **Entry Points**: Main files, initialization code
- **Directory Structure**: Purpose of each major directory
- **Configuration**: Environment variables, config files
- **API Endpoints** (if applicable): Routes, methods, request/response schemas
- **Data Models** (if applicable): Schemas, relationships, validation
- **UI Components** (if applicable): Component inventory, design patterns
- **Testing Strategy**: Test files, frameworks, coverage patterns
- **Build & Deployment**: Scripts, CI/CD, deployment targets

### 5.5 Write Documentation Immediately (Write-as-You-Go)

As you extract information, write documentation files immediately:

1. **project-overview.md** - Executive summary and classification
2. **source-tree-analysis.md** - Annotated directory structure
3. **technology-stack.md** - Complete tech stack with versions
4. **architecture.md** (or per-part) - Detailed architecture documentation
5. **component-inventory.md** (if applicable) - Catalog of major components
6. **development-guide.md** - Local setup and development workflow
7. **api-contracts.md** (if applicable) - API endpoints and schemas
8. **data-models.md** (if applicable) - Database schema and models
9. **deployment-guide.md** (if deployment config found) - Deployment process
10. **integration-architecture.md** (if multi-part) - How parts communicate

**CRITICAL RULES:**
- Write each document to disk IMMEDIATELY after generating content
- Validate document has required sections (no placeholders)
- Update state file with output filename
- PURGE detailed data from context after writing
- Keep only 1-2 sentence summary in context

### 5.6 Update State File After Each Document

After writing each document:
```json
{
  "completed_steps": [
    {
      "step": "step_5_{{doc_name}}",
      "status": "completed",
      "timestamp": "{{now}}",
      "summary": "{{doc_name}} written with {{section_count}} sections"
    }
  ],
  "outputs_generated": [
    "{{doc_name}}.md"
  ]
}
```

## Step 6: Deep-Dive Mode

**[[AGENT: Only execute this step if workflow_mode == "deep_dive"]]**

**Announce to user:** "Step 6: Deep-Dive Analysis"

See main SKILL.md for full deep-dive workflow details including:
- 6.1 Identify Area for Deep-Dive
- 6.2 Exhaustive Scan of Target Area
- 6.3 Build Dependency Graph
- 6.4 Find Related Code
- 6.5 Generate Deep-Dive Documentation
- 6.6 Update Master Index
- 6.7 Offer to Continue or Complete

## Step 6.5: Check for Existing Documentation

**[[AGENT: Execute this step before generating any new documents]]**

**Announce to user:** "Step 6.5: Checking for Existing Documentation"

**Purpose:** Use semantic search to find existing documentation that covers similar topics. **Update existing docs instead of creating duplicates.**

See main SKILL.md for Smart Connections integration details.

## Step 7: Generate Master Index

**[[AGENT: Execute this step only after Step 6.5 is complete]]**

**Announce to user:** "Step 7: Generating Master Index"

Create `{{output_folder}}/index.md` as master entry point.

See main SKILL.md for full index structure template.

## Step 8: Validate and Offer Completion

**[[AGENT: Execute this step only after Step 7 is complete]]**

**Announce to user:** "Step 8: Validation and Completion"

- Display summary of documents created
- Detect incomplete documentation
- Offer options for additional work or finalization

## Step 9: Generate Incomplete Documentation

**[[AGENT: Only execute this step if user requested it in Step 8]]**

**Announce to user:** "Step 9: Generating Incomplete Documentation"

Generate any selected incomplete items and update the index.

## Step 10: Finalize and Complete

**[[AGENT: Execute this step as the final step]]**

**Announce to user:** "Step 10: Finalizing Documentation"

- Update state file as complete
- Display final summary with statistics
- Archive state file
