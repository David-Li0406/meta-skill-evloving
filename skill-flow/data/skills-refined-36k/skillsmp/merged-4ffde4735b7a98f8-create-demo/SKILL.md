---
name: create-demo
description: Guide you through creating a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.
---

# Demo Module Generator

Guide you through creating a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.

## When to Use

**Use this skill when you want to**:
- Create presenter-led demo content
- Transform technical documentation into business-focused demos
- Add a module to an existing demo
- Create content for sales engineers or field demonstrations

**Don't use this for**:
- Hands-on workshop content → use `/create-lab`
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

## Know/Show Structure

Demos use a different format than workshops:

- **Know sections**: Business context, customer pain points, value propositions, why this matters
- **Show sections**: Step-by-step presenter instructions, what to demonstrate, expected outcomes

This separates what presenters need to **understand** (business value) from what they need to **do** (technical demonstration).

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-demo                                   # Interactive mode (asks all questions)
/create-demo <directory>                       # Specify target directory
/create-demo <directory> --new                 # Create new demo in directory
/create-demo <directory> --continue <module>   # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for demo files
  - Example: `/create-demo content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new demo (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous demo module
  - Example: `/create-demo content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-01-intro.adoc`
  - Reads previous module to detect story continuity

**How Arguments Work**:
- Arguments skip certain questions (faster workflow)
- You can still use interactive mode by calling `/create-demo` with no arguments
- Arguments are validated before use

## Workflow

**CRITICAL RULES**

### 1. Ask Questions SEQUENTIALLY

- Ask ONE question or ONE group of related questions at a time
- WAIT for user's answer before proceeding
- Do NOT ask questions from multiple steps together
- Do NOT skip workflows based on incomplete answers

### 2. Manage Output Tokens

- **NEVER output full demo content** - Use Write tool to create files
- **Show brief confirmations only** - "✅ Created: filename (X lines)"
- **Keep total output under 5000 tokens** - Summaries, not content
- **Files are written, not displayed** - User reviews with their editor
- **Token limit**: Claude Code has 32000 token output limit - stay well below it

---

### Step 0: Parse Arguments (If Provided)

**Check if user invoked skill with arguments**.

**Pattern 1: `/create-demo <directory> --new`**
```
Parsing arguments: "<directory> --new"

✓ Target directory: <directory>
✓ Mode: Create new demo
✓ Will generate: index.adoc → 01-overview → 02-details → 03-module-01

Validating directory...
[Check if directory exists, create if needed]

Skipping: Step 1 (mode already known: NEW demo)
Proceeding to: Step 2 (Plan Overall Demo Story)
```

**Pattern 2: `/create-demo <directory> --continue <module-path>`**
```
Parsing arguments: "<directory> --continue <module-path>"

✓ Target directory: <directory>
✓ Mode: Continue existing demo
✓ Previous module: <module-path>

Validating directory...
[Check if directory exists]

Reading previous module: <module-path>
[Extract story, business context, progression]

Skipping: Step 1 (mode already known: CONTINUE)
Skipping: Step 2 (story detected from previous module)
Proceeding to: Step 3 (Module-Specific Details)
```

**Pattern 3: `/create-demo <directory>`**
```
Parsing arguments: "<directory>"

✓ Target directory: <directory>

Validating directory...
[Check if directory exists]

Skipping: Target directory question
Proceeding to: Step 1 (still need to ask: new vs continue)
```

**Pattern 4: `/create-demo` (no arguments)**
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

---

### Step 1: Determine Context (New Demo vs Continuation)

**SKIP THIS STEP IF**:
- User provided `--new` flag in arguments (already know: NEW demo)
- User provided `--continue <module>` in arguments (already know: EXISTING demo)

**CRITICAL: DO NOT read any files or make assumptions before asking this question!**

**First, ask the user**:

```
Let's get started! I'll help you create amazing demo content.

Are you creating a new demo or continuing an existing one?

1. 🆕 Creating a NEW demo (I'll help you plan the whole story)
2. ➡️  Continuing an EXISTING demo (I'll pick up where you left off)
3. 🤔 Something else (tell me what you need)

What's your situation? [1/2/3]
```

**ONLY AFTER user answers, proceed based on their response.**

### Step 1.5: Ask for Target Directory (if not provided as argument)

**SKIP THIS STEP IF**: User provided `<directory>` as argument

**Ask the user**:
```
Where should I create the demo files?

Default location: content/modules/ROOT/pages/

Press Enter to use default, or type a different path:
```

**Validation**:
- If directory doesn't exist, ask: "Directory not found. Create it? [Yes/No]"
- If Yes, create the directory
- If No, ask again for directory

**If continuing existing demo**:
- Provide path to previous module (I'll read and auto-detect the story)

### Step 2: Plan Overall Demo Story (if new demo)

Great! Let's plan your demo together. I'll ask you a few questions to understand what you're trying to achieve.

**IMPORTANT**: Ask these as **conversational, open-ended questions**. Do NOT provide multiple choice options.

**Question 1 - The Big Picture**:
```
What's the main message you want to deliver in this demo?

Think about: What should your audience remember after seeing this?

Example: "Show how OpenShift accelerates application deployment for enterprises"

Your answer:
```

**Question 2 - Know Your Audience**:
```
Who will be watching this demo?

Examples: C-level executives, Sales engineers, Technical managers, Partners

Your audience:

And what matters most to them right now? (their business priorities)

Examples: Cost reduction, faster time-to-market, competitive advantage

Their priorities:
```

**Question 3 - The Transformation Story**:
```
Let's create the before-and-after narrative.

What's the customer challenge you're solving?

What's painful about their current state?

What does the ideal future state look like?

Your story:
```

**Question 4 - Customer Scenario**:
```
What company or industry should we feature in this demo?

Examples: "RetailCo" (retail), "FinanceCorp" (banking), "HealthTech" (healthcare)
Or create your own!

Company/industry:

What specific business challenge is driving urgency for them?

Their urgent challenge:
```

**Question 5 - Show the Impact**:
```
What quantifiable improvements will you highlight?

Examples:
- "6 weeks → 5 minutes deployment time"
- "80% reduction in infrastructure costs"
- "10x faster developer productivity"

Your key metrics:
```

**Question 6 - Timing**:
```
How long should the complete demo take?

Typical options: 15min, 30min, 45min

Your target duration:
```

**Then I'll recommend**:
- Suggested module/section breakdown
- Know/Show structure for each section
- Business narrative arc across modules
- Key proof points and "wow moments"
- Competitive differentiators to emphasize

**You can**:
- Accept the recommended flow
- Adjust sections and messaging
- Change business emphasis

---

### Step 3: Gather Module-Specific Details

Now for this specific module:

1. **Module file name**:
   - Module file name (e.g., "03-demo-intro.adoc", "04-platform-demo.adoc")
   - Files go directly in `content/modules/ROOT/pages/`
   - Pattern: `[number]-[topic-name].adoc`

2. **Reference materials** (optional but recommended):
   - URLs to Red Hat product documentation
   - Marketing materials, solution briefs
   - Local files (Markdown, AsciiDoc, PDF)
   - Pasted content
   - **Better references = better business value extraction**
   - If not provided: Generate from templates and common value propositions

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

4. **Target audience**:
   - Sales engineers, C-level executives, technical managers, developers

5. **Business scenario/challenge**:
   - Auto-detect from previous module (if exists)
   - Or ask for customer scenario (e.g., "RetailCo needs faster deployments")

6. **Technology/product focus**:
   - Example: "OpenShift", "Ansible Automation Platform"

7. **Number of demo parts**:
   - Recommended: 2-4 parts (each with Know/Show sections)

8. **Key metrics/business value**:
   - Example: "Reduce deployment time from 6 weeks to 5 minutes"

9. **Diagrams, screenshots, or demo scripts** (optional):
   - Do you have architecture diagrams, demo screenshots, or scripts?
   - If yes: Provide file paths or paste content
   - I'll save them to `content/modules/ROOT/assets/images/`
   - And reference them properly in Show sections

### Step 4: Get UserInfo Variables (if applicable)

If UserInfo variables weren't already provided in Step 2.5 or Step 3, I'll ask for them now.

**RECOMMENDED: Get from Deployed Environment (Primary Method)**

I'll ask: "Do you have access to a deployed environment on demo.redhat.com or integration.demo.redhat.com?"

**If YES** (recommended):
```
Please share the UserInfo variables from your deployed service:

1. Login to https://integration.demo.redhat.com (or demo.redhat.com)
2. Go to "My services" → Find your service
3. Click on "Details" tab
4. Expand "Advanced settings" section
5. Copy and paste the output here
```

This shows all available variables like:
- `openshift_cluster_console_url` → For showing presenter where to log in
- `openshift_api_server_url` → For API demonstrations
- `openshift_cluster_admin_username` → For admin access demos
- `openshift_cluster_admin_password` → For demo credentials
- `gitea_console_url` → For Git server demos
- `gitea_admin_username`, `gitea_admin_password` → For Gitea access
- Custom workload-specific variables → Product-specific endpoints

**If NO** (fallback):
I'll use common placeholder variables:
- `{openshift_console_url}`
- `{openshift_api_url}`
- `{user}`
- `{password}`
- `{bastion_public_hostname}`

**Alternative**: Clone collections from AgV catalog
- Read `common.yaml` from user-provided AgV path
- Clone collections from any repository (agnosticd, rhpds, etc.)
- Read workload roles to find `agnosticd_user_info` tasks
- Extract variables from `data:` sections
- Note: Less reliable than deployed environment output

**Result**: I'll use these in Show sections for precise presenter instructions with actual URLs and credentials.

### Step 5: Handle Diagrams, Screenshots, and Demo Scripts (if provided)

If you provided visual assets or scripts:

**For presenter screenshots**:
- Save to `content/modules/ROOT/assets/images/`
- Use descriptive names showing what presenters will see
- Reference in Show sections with proper context:
  ```asciidoc
  image::console-developer-view.png[Developer Perspective - What Presenters Will See,link=self,window=blank,align="center",width=700,title="Developer Perspective - What Presenters Will See"]
  ```
- **CRITICAL**: **ALWAYS** include `link=self,window=blank` to make images clickable

**For architecture diagrams**:
- Save to `content/modules/ROOT/assets/images/`
- Use business-context names: `retail-transformation-architecture.png`
- Reference in Know sections to show business value
- Use larger width (700-800px) for visibility during presentations
- **ALWAYS include `link=self,window=blank`** for clickable images

**For demo scripts or commands**:
- Format in code blocks with syntax highlighting
- Add presenter notes about what to emphasize:
  ```asciidoc
  [source,bash]
  ----
  oc new-app https://github.com/example/nodejs-ex
  ----

  [NOTE]
  ====
  **Presenter Tip:** Emphasize how this single command eliminates 3-5 days of manual setup.
  ====
  ```

**For before/after comparisons**:
- Save both images: `before-manual-deployment.png`, `after-automated-deployment.png`
- Use side-by-side or sequential placement
- Highlight business transformation visually

**Recommended image naming for demos**:
- Business context: `customer-challenge-overview.png`, `transformation-roadmap.png`
- UI walkthroughs: `step-1-login-console.png`, `step-2-create-project.png`
- Results: `deployment-success.png`, `metrics-dashboard.png`
- Comparisons: `before-state.png`, `after-state.png`

**Clickable Images (Links)**:
If an image should be clickable and link to external content, use `^` caret to open