# AI Agent Self-Enhancement Workflow

Guidelines for AI agents to discover and deploy artifacts during development tasks.

---

## Core Principles

1. **Never auto-deploy** - Always get explicit user permission
2. **Be helpful, not intrusive** - Suggest only when genuinely useful
3. **Respect user focus** - Don't interrupt deep work with suggestions
4. **Show, don't tell** - Demonstrate what artifact provides before suggesting

---

## Capability Gap Detection

### When to Detect Gaps

| Situation | Action |
|-----------|--------|
| User asks for help with X | Check if X-related artifacts exist |
| Task requires specific tooling | Search for relevant artifacts |
| User says "I wish I could..." | Search for capability match |
| Error suggests missing tool | Check for relevant artifact |

### How to Search (Silently)

```bash
# Don't announce this search to user
skillmeat search "<capability>" --json 2>/dev/null
```

Parse JSON output to check if relevant artifacts exist.

### Gap Categories

| Gap Type | Example | Search Terms |
|----------|---------|--------------|
| File processing | "Process this PDF" | `pdf`, `document` |
| Code generation | "Create React component" | `react`, `frontend` |
| Testing | "Test this API" | `testing`, `api-test` |
| Documentation | "Document this API" | `openapi`, `docs` |
| Database | "Run migrations" | `database`, `migration` |
| Browser automation | "Take screenshot" | `browser`, `puppeteer` |

---

## Suggestion Protocol

### When to Suggest

**DO suggest** when:
- User explicitly asks about capabilities
- Task clearly requires capability user doesn't have
- User expresses frustration with manual process
- Gap is obvious and artifact is well-matched

**DON'T suggest** when:
- User is in flow state on focused task
- Suggestion would be tangential to main goal
- User already declined similar suggestion
- Task can reasonably be done without artifact

### Suggestion Format

```markdown
I notice this task involves [specific capability].

The **[artifact-name]** skill could help with this:
- [Key feature 1]
- [Key feature 2]
- Source: `[source-path]`

Would you like me to add it to the project?
```

### Example Suggestions

**PDF Processing**:
```
I notice you're working with PDF files.

The **pdf** skill from `anthropics/example-skills` could help:
- Extract text and tables from PDFs
- Fill PDF forms programmatically
- Merge and split PDF documents

Would you like me to add it to the project?
```

**React Development**:
```
This looks like a React project without the frontend-design skill.

The **frontend-design** skill provides:
- Modern UI component patterns
- Tailwind CSS integration
- Accessibility best practices

Would you like me to add it?
```

---

## Deployment Protocol

### Before Deploying

1. **Confirm permission**: "I'll add [artifact] to the project. Proceed?"
2. **Show what changes**: "This will create `.claude/skills/[name]/`"
3. **Check for conflicts**: Verify no existing artifact with same name

### Deployment Commands

```bash
# Add to collection first (if not present)
skillmeat add skill <source>

# Deploy to project
skillmeat deploy <artifact-name> --project .
```

### After Deploying

1. **Confirm success**: "Added [artifact] to the project."
2. **Show location**: "Skill is now available at `.claude/skills/[name]/`"
3. **Brief usage hint**: "You can use it by [brief instruction]"

---

## Permission Escalation

### Levels of Permission

| Level | Scope | Example |
|-------|-------|---------|
| Single | One artifact | "Add the PDF skill?" |
| Category | Related artifacts | "Add all document skills?" |
| Session | For this session | "Add artifacts as needed?" |
| Standing | Permanent | (Not recommended) |

### Handling Permission

```
User: "Yes, add what you need"
Agent: I'll add artifacts as needed for this task.
       Currently adding: [artifact-1], [artifact-2]
       I'll confirm before adding anything else.
```

### When User Declines

```
User: "No, I don't need that"
Agent: Understood. I'll proceed without it.
       Let me know if you change your mind.
```

Don't suggest the same artifact again in the same session unless context changes significantly.

---

## Project Analysis

### Analyze Project Context

Before suggesting artifacts, understand the project:

```javascript
// Check for project indicators
const indicators = {
  react: ['package.json', 'React'],
  python: ['pyproject.toml', 'requirements.txt'],
  fastapi: ['fastapi', 'uvicorn'],
  nextjs: ['next.config.js', 'next.config.ts'],
};
```

### Already Deployed Check

```bash
# Check what's already deployed
skillmeat list --project . --json
```

Don't suggest artifacts that are already deployed.

### Complementary Artifacts

| If User Has | Consider Suggesting |
|-------------|---------------------|
| `frontend-design` | `webapp-testing` |
| `pdf` | `docx`, `xlsx` |
| `postgresql-psql` | Database migration skills |
| `chrome-devtools` | `webapp-testing` |

---

## Multi-Artifact Scenarios

### When Multiple Artifacts Help

```
For your document processing needs, I'd suggest these artifacts:
1. **pdf** - PDF text extraction and forms
2. **docx** - Word document processing
3. **xlsx** - Spreadsheet analysis

Would you like me to add:
[ ] All three
[ ] Just PDF
[ ] Let me pick specific ones
```

### Bundle Suggestion

If user needs many related artifacts:

```
There's a document-processing bundle that includes all these skills.
Would you like to import that instead of adding individually?
```

---

## Edge Cases

### Artifact Not Found

```
I looked for [capability] skills but didn't find a good match.
You might need to:
1. Create a custom skill for this
2. Use a general-purpose approach
3. Check community sources
```

### Rate Limited

```
I can't search for artifacts right now (rate limited).
Try: skillmeat config set github-token <your-token>
```

### Network Issues

```
I couldn't reach the artifact source.
Once connectivity is restored, I can help you find relevant skills.
```

---

## Anti-Patterns

### Don't Do This

- **Over-suggesting**: "You should also add X, Y, Z..."
- **Auto-deploying**: Adding artifacts without asking
- **Interrupting flow**: Suggesting mid-task unnecessarily
- **Repeating suggestions**: Asking again after user declined
- **Vague suggestions**: "There might be a skill for that"

### Do This Instead

- **Targeted suggestions**: One relevant artifact at a time
- **Permission-first**: Always ask before adding
- **Context-aware**: Suggest at natural breakpoints
- **Graceful acceptance**: Accept "no" without pushback
- **Specific suggestions**: "The PDF skill from anthropics/skills"
