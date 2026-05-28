---
name: teach-course-builder
description: Transform source documents into structured courses via the Teach authoring API. Use when building courses from existing content.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: education
  type: generator
  mode: collaborative
---

# Teach Course Builder

Transform source documents (markdown files, articles, documentation) into structured courses using the Teach authoring API. This skill analyzes source materials, proposes course structure, and creates courses via CLI scripts.

## Core Principle

**Source documents become structured learning paths, not just copied content.**

The skill doesn't just copy files - it analyzes structure, infers units and lessons, identifies audience layers, and creates a coherent course with competencies.

## Setup

### Requirements

1. **Deno** - Install from https://deno.land
2. **Teach Authoring API** - Running at http://localhost:4100

### Configuration

Set the API URL (optional if using default):
```bash
export TEACH_API_URL="http://localhost:4100/api"
```

Start the authoring API:
```bash
cd /path/to/teach
pnpm dev:authoring-api
```

## Workflow Phases

### Phase 1: Analyze

Analyze source documents to understand their structure.

```bash
deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources
```

This produces a course plan showing:
- Suggested course title
- Proposed units (based on directories)
- Proposed lessons (based on files)
- Detected audience layers
- Suggested competencies

### Phase 2: Plan

Review the generated plan with the user. Modify as needed:
- Adjust unit titles and ordering
- Merge or split lessons
- Refine audience layer assignments
- Add or remove competencies

### Phase 3: Research (Optional)

If content needs expansion, use the research skill:
- Identify gaps in the source material
- Research supplementary topics
- Find authoritative sources for claims

### Phase 4: Build

Create the course structure via API:

```bash
# Create the course
deno run --allow-net --allow-env scripts/create-course.ts \
  --title "Working with AI" \
  --description "A practical guide"

# Add units
deno run --allow-net --allow-env scripts/add-unit.ts \
  --course-id <course-id> \
  --title "Foundations"

# Add lessons with content
deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts \
  --unit-id <unit-id> \
  --title "What AI Is and Isn't" \
  --content-file /path/to/what-ai-is-and-isnt.md \
  --audience-layer general

# Add competencies
deno run --allow-net --allow-env scripts/add-competency.ts \
  --course-id <course-id> \
  --name "Understanding AI Limitations" \
  --cluster-name "AI Literacy"
```

### Phase 5: Review

Verify the course in the authoring UI:
- Open http://localhost:4101/courses/<course-id>
- Check Content tab for unit/lesson hierarchy
- Check Competencies tab for learning objectives
- Edit and refine as needed

## Available Scripts

### analyze-sources.ts

Analyze a directory of markdown files and propose course structure.

```bash
# Human-readable output
deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources

# JSON output (for programmatic use)
deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources --json
```

**What it does:**
- Recursively finds all `.md` files (excluding READMEs)
- Extracts titles, descriptions, and headings
- Groups files by directory into units
- Infers audience layers from directory/file names
- Counts words for scope estimation
- Suggests competencies from heading keywords

### create-course.ts

Create a new course.

```bash
deno run --allow-net --allow-env scripts/create-course.ts \
  --title "Course Title" \
  --description "Description" \
  --json
```

### add-unit.ts

Add a unit to a course.

```bash
deno run --allow-net --allow-env scripts/add-unit.ts \
  --course-id <id> \
  --title "Unit Title" \
  --description "Description" \
  --order 1
```

### add-lesson.ts

Add a lesson to a unit.

```bash
deno run --allow-net --allow-env --allow-read scripts/add-lesson.ts \
  --unit-id <id> \
  --title "Lesson Title" \
  --description "Description" \
  --content-file /path/to/content.md \
  --audience-layer general \
  --order 1
```

**Audience layers:**
- `general` - Introductory content for all learners
- `practitioner` - Intermediate content for regular users
- `specialist` - Advanced/technical content for experts

### add-competency.ts

Add a competency to a course.

```bash
# Creates cluster if needed
deno run --allow-net --allow-env scripts/add-competency.ts \
  --course-id <id> \
  --name "Competency Name" \
  --cluster-name "Cluster Name"

# Use existing cluster
deno run --allow-net --allow-env scripts/add-competency.ts \
  --cluster-id <id> \
  --name "Competency Name"
```

### list-courses.ts

List existing courses.

```bash
deno run --allow-net --allow-env scripts/list-courses.ts
deno run --allow-net --allow-env scripts/list-courses.ts --json
```

## Example Interaction

**User:** "Build a course from inbox/ai-education/"

**Workflow:**

1. Analyze the source directory:
   ```bash
   deno run --allow-read --allow-env scripts/analyze-sources.ts inbox/ai-education/
   ```

2. Review the proposed structure:
   ```
   # Course Plan: AI Education

   **Source:** inbox/ai-education/
   **Total:** 12 lessons, ~15,000 words

   ## Proposed Structure

   ### 1. Layer 1: Foundations
   - **What AI Is and Isn't** [general]
   - **Basic Prompting** [general]
   - **When to Use AI** [general]
   - **Data and Privacy** [general]

   ### 2. Layer 2: Effective Use
   - **Why AI Gives Mediocre Results** [practitioner]
   - **Framework-First Prompting** [practitioner]
   ...
   ```

3. Confirm structure with user, then build:
   ```bash
   # Create course
   deno run --allow-net --allow-env scripts/create-course.ts \
     --title "Working with AI: A Practical Guide" \
     --description "Standalone articles about working effectively with AI tools"

   # Get course ID from output, then create units and lessons...
   ```

4. Direct user to http://localhost:4101/courses/<id> to review

## Integration Points

### Research Skill

For content gaps:
- Use research skill's Tavily integration to find sources
- Expand thin lessons with researched content
- Verify claims in source documents

### Competency Skill

For learning objectives:
- Use competency skill to define progression paths
- Map competencies to lessons
- Define rubrics for assessment

### Gentle-Teaching Skill

For content design:
- Apply gentle-teaching principles to lesson content
- Ensure appropriate scaffolding
- Design for learner empowerment

## Anti-Patterns

### The Copy-Paste Course

**Problem:** Just copying files without structure analysis
**Fix:** Always run analyze-sources.ts first; review and refine structure

### The Flat Course

**Problem:** All lessons at same level without units
**Fix:** Group related lessons into units; use directory structure as guide

### The Gapless Course

**Problem:** Assuming source materials are complete
**Fix:** Identify gaps; use research skill to expand; ask user about missing topics

### The Competency-Free Course

**Problem:** Course without learning objectives
**Fix:** Always add competencies; extract from headings or define explicitly

## Output Persistence

Course data is persisted via the authoring API:
- Database: `apps/authoring-api/data/authoring.db`
- Accessible via: http://localhost:4101

### What Gets Stored

| Data | Location | Access |
|------|----------|--------|
| Courses | API database | API or UI |
| Units | API database | API or UI |
| Lessons | API database | API or UI |
| Competencies | API database | API or UI |
| Source analysis | Console output | Re-run script |

## Environment Configuration

```bash
# API endpoint (default: http://localhost:4100/api)
export TEACH_API_URL="http://localhost:4100/api"

# For research integration
export TAVILY_API_KEY="your-key-here"
```

## Troubleshooting

### "Connection refused" errors

The authoring API isn't running:
```bash
cd /path/to/teach
pnpm dev:authoring-api
```

### "Course not found" errors

Use list-courses.ts to verify course ID:
```bash
deno run --allow-net --allow-env scripts/list-courses.ts
```

### Empty course plan

Source directory may only contain READMEs (which are skipped):
- Check for `.md` files that aren't named `README.md`
- Verify the path is correct

## What You Do NOT Do

- You do not bypass the authoring API (always use scripts)
- You do not create courses without user review of structure
- You do not copy content verbatim without structure analysis
- You do not skip competency definition
- You propose structure; the user decides final organization
