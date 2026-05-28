---
name: create-lab
description: Guide you through creating a single Red Hat Showroom workshop module from reference materials (URLs, files, docs, or text) with business storytelling and proper AsciiDoc formatting.
---

# Lab Module Generator

Guide you through creating a single Red Hat Showroom workshop module from reference materials (URLs, files, docs, or text) with business storytelling and proper AsciiDoc formatting.

## When to Use

**Use this skill when you want to**:
- Create a new workshop module from scratch
- Convert documentation into hands-on lab format
- Add a module to an existing workshop
- Transform technical content into engaging learning experience

**Don't use this for**:
- Creating demo content → use `/create-demo`
- Converting to blog posts → use `/blog-generate`
- Reviewing existing content → use `/verify-content`

## Shared Rules

**IMPORTANT**: This skill follows shared contracts defined in `.claude/docs/SKILL-COMMON-RULES.md`:
- Version pinning or attribute placeholders (REQUIRED)
- Reference enforcement (REQUIRED)
- Attribute file location (REQUIRED)
- Image path conventions (REQUIRED)
- Navigation update expectations (REQUIRED)
- Failure-mode behavior (stop if cannot proceed safely)

See SKILL-COMMON-RULES.md for complete details.

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-lab                                    # Interactive mode (asks all questions)
/create-lab <directory>                        # Specify target directory
/create-lab <directory> --new                  # Create new lab in directory
/create-lab <directory> --continue <module>    # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for module files
  - Example: `/create-lab content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new lab (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous module
  - Example: `/create-lab content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-01-intro.adoc`
  - Reads previous module to detect story continuity

**How Arguments Work**:
- Arguments skip certain questions (faster workflow)
- You can still use interactive mode by calling `/create-lab` with no arguments
- Arguments are validated before use

## Workflow

**CRITICAL RULES**

### 1. Ask Questions SEQUENTIALLY

- Ask ONE question or ONE group of related questions at a time
- WAIT for user's answer before proceeding
- Do NOT ask questions from multiple steps together
- Do NOT skip workflows based on incomplete answers

### 2. File Generation Order (First Module ONLY)

**If this is the FIRST module of a NEW lab, you MUST generate files in this EXACT order:**

1. **index.adoc** - Learner landing page (NOT facilitator guide)
2. **01-overview.adoc** - Business scenario and learning objectives
3. **02-details.adoc** - Technical requirements and setup
4. **03-module-01-*.adoc** - First hands-on module

**NEVER skip index/overview/details for first module!**

**File naming convention**:
- index.adoc (no number prefix)
- 01-overview.adoc
- 02-details.adoc
- 03-module-01-*.adoc
- 04-module-02-*.adoc
- 05-module-03-*.adoc
- etc.

**If continuing existing lab**:
- Detect next file number from existing modules
- Generate: 0X-module-YY-*.adoc (where X = next sequential file number)
- Example: If existing has 03-module-01, 04-module-02, next is 05-module-03
- Skip index/overview/details (already exist)

### 3. Manage Output Tokens

- **NEVER output full module content** - Use Write tool to create files
- **Show brief confirmations only** - "✅ Created: filename (X lines)"
- **Keep total output under 5000 tokens** - Summaries, not content
- **Files are written, not displayed** - User reviews with their editor
- **Token limit**: Claude Code has 32000 token output limit - stay well below it

### Step 0: Parse Arguments (If Provided)

**Check if user invoked skill with arguments**.

**Pattern 1: `/create-lab <directory> --new`**
```
Parsing arguments: "<directory> --new"

✓ Target directory: <directory>
✓ Mode: Create new lab
✓ Will generate: index.adoc → 01-overview → 02-details → 03-module-01

Validating directory...
[Check if directory exists, create if needed]

Skipping: Step 1 (mode already known: NEW lab)
Proceeding to: Step 2 (Plan Overall Lab Story)
```

**Pattern 2: `/create-lab <directory> --continue <module-path>`**
```
Parsing arguments: "<directory> --continue <module-path>"

✓ Target directory: <directory>
✓ Mode: Continue existing lab
✓ Previous module: <module-path>

Validating directory...
[Check if directory exists]

Reading previous module: <module-path>
[Extract story, company, progression]

Skipping: Step 1 (mode already known: CONTINUE)
Skipping: Step 2 (story detected from previous module)
Proceeding to: Step 3 (Module-Specific Details)
```

**Pattern 3: `/create-lab <directory>`**
```
Parsing arguments: "<directory>"

✓ Target directory: <directory>

Validating directory...
[Check if directory exists]

Skipping: Target directory question
Proceeding to: Step 1 (still need to ask: new vs continue)
```

**Pattern 4: `/create-lab` (no arguments)**
```
No arguments provided.

Using interactive mode.
Target directory: Will use default (content/modules/ROOT/pages/)

Proceeding to: Step 1 (Determine Context)
```

**Argument Validation**:
- If directory doesn't exist, ask user: "Directory not found. Create it? [Yes/No]"
- If `--continue` but module path invalid, fall back to asking for story recap
- All arguments are optional - skill always works in interactive mode

### Step 1: Determine Context (New Lab vs Existing Lab)

**SKIP THIS STEP IF**:
- User provided `--new` flag in arguments (already know: NEW lab)
- User provided `--continue <module>` in arguments (already know: EXISTING lab)

**CRITICAL: DO NOT read any files or make assumptions before asking this question!**

**First, ask the user**:

```
Welcome! Let's create your workshop together.

Are you starting a brand new lab or adding to an existing one?

1. 🆕 NEW lab (I'll create the whole thing: index → overview → details → first module)
2. ➕ EXISTING lab (I'll add the next module and continue your story)
3. 🤔 Something else (tell me what you need)

What's your situation? [1/2/3]
```

**ONLY AFTER user answers, proceed based on their response.**

### Step 1.5: Ask for Target Directory (if not provided as argument)

**SKIP THIS STEP IF**: User provided `<directory>` as argument

**Ask the user**:
```
Where should I create the lab files?

Default location: content/modules/ROOT/pages/

Press Enter to use default, or type a different path:
```

**Validation**:
- If directory doesn't exist, ask: "Directory not found. Create it? [Yes/No]"
- If Yes, create the directory
- If No, ask again for directory

**If option 1 (NEW lab)**:
- Generate ALL workshop files: index.adoc, 01-overview.adoc, 02-details.adoc, 03-module-01-*.adoc
- Proceed to Step 2 (Plan Overall Lab Story)

**If option 2 (EXISTING lab)**:
- Detect next file number from existing modules
- Generate ONLY next module: 0X-module-YY-*.adoc
- Skip Step 2 (already have overall story)
- Ask for previous module path or story recap

**If continuing existing lab**:
- Option 1: Provide path to previous module (I'll read and auto-detect story)
- Option 2: If previous module not available, I'll ask for story recap:
  - Company name and scenario
  - What was completed in previous modules
  - Current learning state
  - What comes next in progression

**Fallback behavior**:
- If user says "continuing" but cannot provide previous module content or workspace access:
  - Ask user to paste content of last module (or key sections)
  - OR ask short "Story Recap" questions:
    1. Company/scenario name?
    2. What topics were covered in previous modules?
    3. What skills have learners gained so far?
    4. What's the current state in the story?
  - This prevents broken continuity

### Step 2: Plan Overall Lab Story (if first module)

Awesome! Let's design your workshop together. I'll ask you some questions to build the perfect learning experience.

**IMPORTANT**: Ask these as **conversational, open-ended questions**. Do NOT provide multiple choice options.

**Question 1 - What Should We Call This?**:
```
What's the name of your workshop?

Example: "Building AI/ML Workloads on OpenShift AI"

I'll use this to set up your lab title and generate a clean URL-friendly slug.

Your lab name:

[After user provides title, I'll suggest a slug like "building-ai-ml-workloads-openshift-ai"]
```

**Question 2 - The Learning Goal**:
```
What's the main goal of this lab?

What should learners be able to do when they finish?

Example: "Learn to build and deploy AI/ML workloads on OpenShift AI"

Your lab goal:
```

**Question 3 - Who's Learning?**:
```
Who is this lab designed for?

Examples: Developers, Architects, SREs, Data Scientists, Platform Engineers

Your target audience:

What's their experience level?
- Beginner (new to the technology)
- Intermediate (some hands-on experience)
- Advanced (production experience)

Their level:
```

**Question 4 - The Learning Journey**:
```
By the end of this lab, what should learners understand and be able to do?

List the key skills they'll gain:

Your learning outcomes:
```

**Question 5 - Make It Real**:
```
What company or business scenario should we use to make this relatable?

Examples: "ACME Corp", "RetailCo", "FinTech Solutions"
Or create your own!

Company name:

What business challenge are they facing that drives this learning?

Their challenge:
```

**Question 6 - How Long?**:
```
How much time should learners budget for the complete lab?

Typical options: 30min, 1hr, 2hr

Your target duration:
```

**Question 7 - Technical Environment**:
```
Let's nail down the technical details:

OpenShift version? (e.g., "4.18", "4.20", or I can use {ocp_version} placeholder)

Product versions? (e.g., "OpenShift Pipelines 1.12, OpenShift AI 2.8")

Cluster type? (SNO or multinode)

Access level? (admin only, or multi-user with keycloak/htpasswd)

Your environment details:

Note: If you're not sure, I'll use placeholders that work across versions.
```

**Then I'll recommend**:
- Suggested module breakdown (how many modules, what each covers)
- Progressive learning flow (foundational → intermediate → advanced)
- Story arc across modules
- Key milestones and checkpoints

**You can**:
- Accept the recommended flow
- Adjust module count and topics
- Change the progression

### Step 2.1: Update Lab Configuration Files (REQUIRED for new labs)

**CRITICAL: Update these files with the lab name BEFORE generating any content files.**

Using the lab title and slug from Step 2, update:

1. **site.yml** (line 3):
   ```yaml
   site:
     title: {{ lab_title }}  # e.g., "Building AI/ML Workloads on OpenShift AI"
   ```

2. **content/antora.yml** (line 2):
   ```yaml
   name: modules
   title: {{ lab_title }}  # Same as site.yml
   ```

3. **content/antora.yml** (line 9):
   ```yaml
   asciidoc:
     attributes:
       lab_name: "{{ lab_slug }}"  # e.g., "building-ai-ml-workloads-openshift-ai"
   ```

**Example transformation**:
- User says: "Building AI/ML Workloads on OpenShift AI"
- Generated slug: `building-ai-ml-workloads-openshift-ai`
- site.yml title: "Building AI/ML Workloads on OpenShift AI"
- antora.yml title: "Building AI/ML Workloads on OpenShift AI"
- antora.yml lab_name: "building-ai-ml-workloads-openshift-ai"

**Note**: These files must be updated BEFORE Step 8 (Generate Files).

### Step 3: Gather Module-Specific Details

Now for this specific module:

1. **Module file name and numbering**:
   - **Naming convention**: `0X-module-YY-<slug>.adoc` (e.g., `03-module-01-pipelines-intro.adoc`)
   - **Title convention**: `= Module X: <Title>` (e.g., `= Module 1: Pipeline Fundamentals`)
   - Files go in `content/modules/ROOT/pages/`
   - **Number prefix**: 03 for first module, 04 for second, etc. (after 01-overview, 02-details)
   - **Conflict detection**: If file exists, suggest next available number
   - **Warning**: Don't overwrite existing modules without confirmation

2. **Reference materials** (optional but recommended):
   - URLs to Red Hat product documentation
   - Local file paths (Markdown, AsciiDoc, text, PDF)
   - Pasted content
   - **Better references = better content quality**
   - If not provided: Generate from templates and common patterns

3. **UserInfo variables** (optional, for accurate showroom content):
   - If not already provided in Step 2.5, **I must ask the user:**

   ```
   Q: Do you have access to a deployed environment on demo.redhat.com or integration.demo.redhat.com?

   If YES (RECOMMENDED - easiest and most accurate):
   Please share the UserInfo variables from your deployed service:

   1. Login to https://demo.redhat.com (or integration.demo.redhat.com)
   2. Go to "My services" → Your service
   3. Click "Details" tab
   4. Expand "Advanced settings" section
   5. Copy and paste the output here

   This provides exact variable NAMES like:
   - openshift_cluster_console_url
   - openshift_cluster_admin_username
   - gitea_console_url
   - [custom workload variables]

   CRITICAL: I will use these to know WHICH variables exist, NOT to replace them with actual values!
   Variables will stay as placeholders: {openshift_cluster_console_url}
   Showroom replaces these at runtime with actual deployment values.

   If NO:
   Q: Would you like to use placeholder attributes for now?

   If YES:
   I'll use placeholders: {openshift_console_url}, {user}, {password}
   You can update these later when you get Advanced settings.

   If NO (RHDP internal team only):
   I can extract variables from AgnosticV repository if you have it cloned locally.
   This requires AgV path and catalog name.
   Note: Less reliable than Advanced settings.
   ```

4. **Main learning objective**:
   - Example: "Create and run a CI/CD pipeline with Tekton"

5. **Business scenario**:
   - Auto-detect from previous module (if exists)
   - Or ask for company name (default: ACME Corp)

6. **Technology/product focus**:
   - Example: "OpenShift Pipelines", "Pod