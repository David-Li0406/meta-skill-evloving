# Workflow: Create Workspace File

This workflow guides the creation of a new file in the `.claude/` workspace.

---

## Step 1: Determine Category

**Ask:** What type of file are you creating?

1. **Plan** - Implementation plans, migration plans, project plans
2. **Architecture** - ADRs, design decisions, system architecture
3. **Example** - Code examples, patterns, reference implementations
4. **Research** - External research, comparisons, investigations
5. **Analysis** - Code analysis, performance studies, security reviews

**Wait for response.**

---

## Step 2: Gather Context

Based on the selected category, gather the required information:

### For Plans (category = 1)

Ask:
- What problem does this plan solve?
- What is the proposed solution (high-level)?
- Which codebase files are primarily affected?

### For Architecture (category = 2)

Ask:
- What decision is being documented?
- What alternatives were considered?
- Which components are affected?

### For Examples (category = 3)

Ask:
- What pattern or technique is being demonstrated?
- What programming language?
- Which source files show this pattern in the codebase?

### For Research (category = 4)

Ask:
- What question is being researched?
- What options are being compared?
- What sources will be consulted?

### For Analysis (category = 5)

Ask:
- What scope of code is being analyzed?
- What type of analysis? (code, performance, security, dependency)
- What triggered this analysis?

---

## Step 3: Generate Filename

Format: `{YYYY-MM-DD}-{kebab-case-description}.md`

**Process:**

1. Get today's date in YYYY-MM-DD format
2. Take the title/description from Step 2
3. Convert to kebab-case:
   - Lowercase all characters
   - Replace spaces with hyphens
   - Remove special characters
   - Truncate if over 50 characters
4. Combine: `.claude/{category}/{date}-{description}.md`

**Example:**
- Title: "User Authentication Migration"
- Date: 2025-01-07
- Result: `.claude/plans/2025-01-07-user-authentication-migration.md`

---

## Step 4: Ensure Directory Exists

```bash
mkdir -p .claude/{category}
```

Categories:
- plans
- architecture
- examples
- research
- analysis

---

## Step 5: Identify Codebase Links

**BLOCKING REQUIREMENT:** At least one codebase link is required.

Ask: "Which codebase file(s) does this document relate to?"

**Validate:**
- File must exist in the repository
- Use relative path from `.claude/{category}/` directory
- Format: `../../path/to/file.ext`

**If user cannot identify a codebase file:**
- Help identify relevant files based on the document's topic
- Search codebase for related files
- Do NOT proceed without at least one valid codebase link

---

## Step 6: Check for Related .claude/ Documents

Search existing `.claude/` files for related content:

```bash
# Search for related documents
grep -r "keyword" .claude/ --include="*.md" | grep -v INDEX.md
```

**If related documents found:**
- List them for the user
- Ask if they should be cross-referenced
- Add to Related Documentation section

---

## Step 7: Create File from Template

1. Read the appropriate template:
   - [plan-template.md](../templates/plan-template.md)
   - [architecture-template.md](../templates/architecture-template.md)
   - [example-template.md](../templates/example-template.md)
   - [research-template.md](../templates/research-template.md)
   - [analysis-template.md](../templates/analysis-template.md)

2. Fill in template variables:
   - `{{TITLE}}` - From user input
   - `{{YYYY-MM-DD}}` - Today's date
   - `{{category}}` - Selected category
   - Codebase links from Step 5
   - Related documentation from Step 6

3. Write file to `.claude/{category}/{filename}.md`

---

## Step 8: Validation Gate

<validation_gate name="file-creation" blocking="true">

Before writing, verify ALL requirements:

- [ ] YAML frontmatter has all required fields
- [ ] `category` field matches directory
- [ ] `status` field has valid enum value
- [ ] At least one codebase link in `## Related > ### Codebase`
- [ ] Codebase links use correct relative path format
- [ ] Codebase links point to existing files
- [ ] Filename follows `YYYY-MM-DD-description.md` pattern

**If validation fails:**
- Show specific errors
- Ask user to correct
- Do NOT write file until valid

</validation_gate>

---

## Step 9: Update INDEX.md

After successful file creation:

1. Check if `.claude/{category}/INDEX.md` exists
   - If not, create from [index-template.md](../templates/index-template.md)

2. Update INDEX.md:
   - Add new file to the Files table
   - Update `file_count` in frontmatter
   - Update `updated` date
   - Add to appropriate status section

---

## Step 10: Confirmation

Output:

```
File created:
- .claude/{category}/{filename}.md

INDEX updated:
- .claude/{category}/INDEX.md

Cross-references:
- Codebase: {list of linked files}
- Documentation: {list of linked docs}

What's next?
1. View the created file
2. Create another file
3. Done
```

---

## Error Handling

### No codebase link identified

```
Every workspace file must link to at least one codebase file.

Suggestions based on your topic:
- app/models/{related}.rb
- app/controllers/{related}_controller.rb
- lib/{related}.rb

Which file(s) does this document relate to?
```

### Invalid filename

```
Filename must follow: YYYY-MM-DD-description.md

Issue: {specific problem}
Suggested fix: {corrected filename}

Use suggested filename? (y/n)
```

### Directory doesn't exist

```
Creating directory: .claude/{category}/
```
(Auto-create, no user action needed)
