# Agent Integration Guide for skillmeat-cli Skill

This guide teaches Claude Code agents how to integrate with the skillmeat-cli skill to discover, recommend, and deploy artifacts that enhance development workflows.

---

## Quick Integration Pattern

When an agent identifies a capability gap or receives a task requiring specialized tooling:

```
1. RECOGNIZE: Does this task need special capability?
   ↓ No → Continue with task
   ↓ Yes → Go to step 2

2. SEARCH: Query skillmeat for relevant artifacts
   skillmeat search "<capability>" --type <type> --json
   ↓ Parse JSON results

3. ANALYZE: Does an artifact exist?
   ↓ No → Implement manually, suggest user create skill
   ↓ Yes → Go to step 4

4. SUGGEST: Present to user (never auto-deploy)
   "This task would benefit from the X skill.
    Would you like me to add it to your project?"
   ↓ Wait for explicit "yes"

5. DEPLOY: Execute with permission
   skillmeat add <type> <source>
   skillmeat deploy <name>

6. CONFIRM: Verify and update task context
```

---

## Decision Tree: When to Check for Artifacts

### ALWAYS Check When:

- User explicitly asks: "Do you have a skill for...?"
- User says: "Search for..." or "Find a tool for..."
- User imports a file type not natively supported (PDF, DOCX, etc.)
- User asks about documentation/reference generation
- User wants to integrate with external services

### CHECK DURING EXECUTION When:

- Error indicates missing capability (import fails, format unsupported)
- Code pattern emerges that suggests reusable skill exists
- Third-party API requires specialized handling
- Complex transformation task (PDF → JSON, DOCX → Markdown, etc.)

### SUGGEST AFTER COMPLETION When:

- Task involved pattern that appears frequently
- Similar tasks would benefit from deployed skill
- Team has indicated pain point this skill solves

### SKIP When:

- Task requires only standard language features
- Custom implementation is simpler than learning skill
- Skill already deployed in current project
- User is in focused coding session (don't interrupt)

---

## How to Search for Artifacts

### Basic Search (as Agent)

```bash
# For parsing in automation (recommended)
skillmeat search "<query>" --type <type> --json

# Types: skill, command, agent, mcp, hook
skillmeat search "pdf" --type skill --json
skillmeat search "database" --type agent --json
skillmeat search "testing" --type command --json
```

### Parse JSON Results

When using `--json` flag, results come as structured data:

```json
{
  "results": [
    {
      "id": "ms-office-suite:pdf",
      "name": "PDF Processor",
      "type": "skill",
      "description": "Extract, transform, and analyze PDF documents",
      "source": "anthropics/skills/ms-office-suite/pdf",
      "version": "latest",
      "tags": ["pdf", "document", "extraction"],
      "deployments": 2
    }
  ],
  "total": 1
}
```

**Key Fields**:
- `id`: Unique identifier (use for deploy/add commands)
- `source`: Full GitHub source path
- `version`: Version to install (default: latest)
- `tags`: Search keywords

### Quick List (What's Already Available)

```bash
# In user's collection
skillmeat list --type skill --json

# Deployed in current project
skillmeat list --type skill --project . --json
```

---

## Suggestion Format

### Agent-to-User Communication

**Pattern**: Direct, brief, with clear value proposition

```markdown
I notice this task involves [capability].
The [artifact-name] skill provides [specific benefit].

Would you like me to add it?

• Provides: [Key feature 1], [Key feature 2]
• Source: [source-path]
• Status: [Latest | Trusted | Community]
```

**Example 1: PDF Processing**
```
I notice you need to extract data from a PDF.
The pdf skill from the ms-office-suite collection
provides built-in PDF parsing and text extraction.

Would you like me to add it?

• Provides: PDF text extraction, table parsing, metadata reading
• Source: anthropics/skills/ms-office-suite/pdf
• Status: Official Anthropic skill (v2.1.0)
```

**Example 2: Database Design**
```
This microservice needs a database schema.
The database-designer agent can help design schemas
that follow best practices for your architecture.

Would you like me to search for database agents?

• Provides: Schema design, migration generation, optimization
• Status: Community-maintained, widely used
```

### Permission Protocol (CRITICAL)

**BEFORE DEPLOYING**:

1. **Search** silently (user doesn't need to see this)
2. **Suggest** with specific artifact details
3. **Wait** for explicit user permission
4. **Confirm** what will be deployed
5. **Execute** the deployment commands
6. **Report** success/failure

**NEVER**:
- Auto-deploy without permission
- Deploy multiple artifacts without asking for each
- Deploy to wrong project path
- Suggest without explaining why

**Examples of Correct Permission**:
```
User: "Yes, add the PDF skill"
User: "Sure, deploy it"
User: "Go ahead and add both the PDF and DOCX skills"
```

**Examples of Ambiguous Permission** (ask for clarification):
```
User: "Maybe"           → "Does that mean yes, add it?"
User: "Sounds good"     → "I'll add the PDF skill. Confirm?"
User: "I'll think about it" → "Let me know when ready."
```

---

## Agent-Specific Integration Patterns

### ui-engineer / ui-engineer-enhanced

**When to check**:
- Creating React components that need styling frameworks
- Building design system components
- Need testing utilities for frontend
- Component documentation generation

**Common artifacts to suggest**:
```bash
skillmeat search "react component" --type skill --json
skillmeat search "storybook" --type command --json
skillmeat search "a11y testing" --type skill --json
```

**Integration example**:
```
Task: Create a modal component with validation

Agent thinks: "This needs form validation + accessibility testing"

Search: skillmeat search "form validation react" --type skill --json

Suggest: "The form-builder skill handles validation
         and accessibility. Want me to add it?"
```

**Decision criteria**:
- ✓ Add if: Component needs form handling, validation, a11y
- ✗ Skip if: Simple presentational component (just CSS)

---

### python-backend-engineer

**When to check**:
- Creating new FastAPI endpoints
- Implementing complex business logic
- Database schema generation
- API specification/documentation generation

**Common artifacts to suggest**:
```bash
skillmeat search "openapi" --type skill --json
skillmeat search "database design" --type agent --json
skillmeat search "api testing" --type command --json
```

**Integration example**:
```
Task: Create REST API for user management

Agent thinks: "New API endpoints need OpenAPI documentation
             and schema validation"

Search: skillmeat search "openapi generator" --type skill --json

Suggest: "The openapi-expert skill auto-generates
         OpenAPI specs and validation schemas.
         Want me to deploy it?"
```

**Decision criteria**:
- ✓ Add if: API endpoints need documentation, complex validation
- ✗ Skip if: Using standard Pydantic models that auto-document

---

### codebase-explorer

**When to check**:
- User asks "what files handle X?"
- Looking for patterns across codebase
- Need to understand architecture
- Finding where to implement new feature

**Common artifacts to help exploration**:
```bash
skillmeat search "code analysis" --type skill --json
skillmeat search "architecture" --type command --json
skillmeat search "symbol navigation" --type skill --json
```

**Integration example**:
```
Task: Find all API endpoints that handle authentication

Agent executes: codebase search for auth patterns

If struggling to find patterns:
Suggest: "The code-analyzer skill can help find
         related functions across the codebase.
         Want me to deploy it?"
```

---

### documentation-writer

**When to check**:
- User needs to generate documentation from code
- Creating guides from existing implementation
- Converting code to multiple documentation formats
- Documentation from binary files (PDF, DOCX, etc.)

**Common artifacts to suggest**:
```bash
skillmeat search "documentation" --type skill --json
skillmeat search "pdf to markdown" --type command --json
skillmeat search "openapi docs" --type skill --json
```

**Integration example**:
```
Task: Generate README from existing codebase

Agent thinks: "Need to extract patterns from code
             and format nicely in Markdown"

Search: skillmeat search "code doc generator" --type skill --json

Suggest: "The doc-generator skill can auto-create
         READMEs from code structure.
         Want me to add it?"
```

---

### ultrathink-debugger

**When to check**:
- Debugging complex multi-file issues
- Need to trace execution flow
- Looking for performance bottlenecks
- Understanding error propagation

**Common artifacts to suggest**:
```bash
skillmeat search "debugging" --type skill --json
skillmeat search "profiling" --type command --json
skillmeat search "trace" --type skill --json
```

**Integration example**:
```
Task: Diagnose why API endpoint returns 500 error

Agent investigates: Stack traces, error logs

If trace is complex:
Suggest: "The debug-trace skill can help visualize
         error flow across multiple files.
         Want me to deploy it?"
```

---

## Cross-Agent Handoff with Artifacts

When one agent discovers an artifact another agent needs:

### Pattern: Explicit Recommendation

```
Agent A completes analysis:
"I found that this task would benefit from the
X skill. I'm passing this to Agent B who will
help you implement it."

→ Task("Agent B", "The user needs the X skill deployed.
                   Here's the artifact info:
                   - Name: X
                   - Source: source/path
                   - Why: [reason]")
```

### Example: Backend + Frontend Handoff

**Backend engineer discovers frontend design need**:

```
Task complete: New API endpoint created

Discovery: "The web UI will need a component
          that consumes this API."

Recommendation: "The form-builder skill handles
               API integration with forms.
               I'll suggest it to the UI team."

→ Task("ui-engineer", "New API endpoint created.
                      The form-builder skill can help
                      wire the frontend forms.
                      Source: anthropics/skills/form-builder")
```

**Frontend engineer discovers backend need**:

```
Task: Build admin dashboard with analytics

Discovery: "This needs complex data aggregation
          from multiple API endpoints."

Recommendation: "The analytics-aggregator agent
               can help design the backend queries."

→ Task("python-backend-engineer", "Need analytics
                                  aggregation skill.
                                  Check skillmeat search for
                                  'analytics aggregator'")
```

---

## Project Context Analysis

Before suggesting artifacts, analyze the project to understand what might be relevant:

### File-Based Context Signals

```
If found in project           → Consider suggesting
─────────────────────────────────────────────────
package.json + React imports  → frontend-design, webapp-testing, accessibility
pyproject.toml + FastAPI      → openapi-expert, database-design
requirements.txt + pandas     → data-processing, jupyter-builder
Dockerfile + Node/Python      → containerization, deployment skills
.github/workflows/ present     → ci-cd, automation skills
tests/ directory (50+ files)  → testing-framework, test-generation
docs/ directory               → doc-generator, markdown-to-X
```

### Capability Gap Signals

```
When user mentions           → Check for
────────────────────────────────────────────
"PDF" / "documents"          → ms-office-suite:pdf, document-processor
"Database" / "schema"        → database-designer, migration-generator
"API" / "REST"               → openapi-expert, api-testing
"React" / "component"        → form-builder, accessibility-checker
"Testing" / "QA"             → test-framework, test-generation
"Deployment" / "DevOps"      → deployment-helper, docker-expert
```

### Skip Signals

```
Skip suggesting if
─────────────────────────────────
Skill already deployed (skillmeat list --project .)
Task is nearly complete
User said "no" to similar suggestion
Custom implementation is simpler
Standard library suffices
```

---

## Complete Integration Examples

### Example 1: ui-engineer Adding Form Component

**Scenario**: User asks engineer to create a contact form with validation.

**Agent flow**:

```typescript
// Step 1: Agent recognizes capability need
if (taskInvolves("form validation") && taskInvolves("react")) {
  // Step 2: Search silently
  await search("form validation react", "skill");
  // Returns: form-builder (anthropics/skills/form-builder)

  // Step 3: Suggest to user (don't auto-deploy)
  suggest({
    artifact: "form-builder",
    reason: "handles form validation and submission",
    deployed: false
  });

  // Step 4: Wait for user response (blocking)
  const permission = await user.confirm(
    "Add form-builder skill to handle validation?"
  );

  if (!permission) {
    // Continue with manual implementation
    return implementFormManually();
  }

  // Step 5: Deploy with permission
  await skillmeat("add skill anthropics/skills/form-builder");
  await skillmeat("deploy form-builder");

  // Step 6: Report success
  console.log("✓ form-builder deployed. Using it for validation logic...");

  // Continue task using the skill
  return implementFormWithSkill();
}
```

**User sees**:
```
You: Create a contact form with validation

Agent: I notice this involves form validation.
       The form-builder skill provides built-in
       validation and submission handling.

       Would you like me to add it?

       • Provides: Form validation, error handling, API integration
       • Source: anthropics/skills/form-builder
       • Deployment time: ~10s

User: Yes, add it

Agent: ✓ Added form-builder skill to project
       Now I'll create your contact form using it...
```

---

### Example 2: python-backend-engineer Adding OpenAPI Documentation

**Scenario**: User asks engineer to create new API endpoints for artifact management.

**Agent flow**:

```python
# Step 1: Recognize capability need
if endpoint_count > 5 and not has_openapi_docs():
    # Step 2: Search for documentation tools
    results = await skillmeat_search("openapi", "skill")
    # Returns: openapi-expert, openapi-generator

    # Step 3: Suggest the best match
    best_artifact = select_best(results)  # openapi-expert

    suggestion = f"""
    I notice you're creating multiple API endpoints.
    The openapi-expert skill auto-generates OpenAPI specs
    and provides validation schemas.

    Would you like me to deploy it?

    • Provides: OpenAPI 3.0 specs, schema validation
    • Reduces manual documentation
    • Source: anthropics/skills/openapi-expert
    """

    await present_suggestion(suggestion)

    # Step 4: Wait for permission
    if not await user.confirm():
        return implement_manual_docs()

    # Step 5: Deploy
    await skillmeat("add skill anthropics/skills/openapi-expert")
    await skillmeat("deploy openapi-expert")

    # Step 6: Use in implementation
    return generate_api_with_openapi_docs()
```

**User interaction**:
```
You: Add artifact CRUD endpoints to the API

Agent: I see you're adding multiple endpoints.
       The openapi-expert skill auto-generates
       OpenAPI documentation and validation.

       Want me to add it?

       • Provides: OpenAPI 3.0 specs, Pydantic validation
       • Status: Official Anthropic skill

User: Sure, deploy it

Agent: ✓ Deploying openapi-expert...
       ✓ Ready to use in endpoint decorators

       Creating endpoints with auto-documentation...
```

---

### Example 3: codebase-explorer Finding Related Files

**Scenario**: User asks agent to find all authentication-related code.

**Agent flow**:

```javascript
// Step 1: Attempt standard exploration
const authFiles = await exploreCodebase("authentication");

// Step 2: If results are scattered/incomplete
if (authFiles.length > 20 && hasComplexPatterns()) {
    // Suggest code analysis tool
    const suggestion = `
    I found 20+ authentication-related files
    with complex cross-dependencies.

    The code-analyzer skill can map these relationships
    and find patterns more efficiently.

    Want me to deploy it?

    • Provides: Architecture visualization, dependency graphs
    • Helps with: Understanding complex systems
    • Source: anthropics/skills/code-analyzer
    `;

    await present_suggestion(suggestion);

    if (await user.confirm()) {
        await skillmeat("add skill anthropics/skills/code-analyzer");
        await skillmeat("deploy code-analyzer");

        // Continue with better analysis
        return analyzeWithCodeAnalyzer();
    }
}

return { authFiles, patterns: analyzePatterns(authFiles) };
```

---

### Example 4: documentation-writer Converting PDF to Markdown

**Scenario**: User asks to convert technical specification PDF to Markdown README.

**Agent flow**:

```
// Step 1: Recognize file type requires special handling
if (file.endsWith('.pdf') && task === 'convert_to_markdown') {

    // Step 2: Search for PDF tools
    results = search("pdf markdown conversion", "skill");
    // Returns: pdf-processor, document-converter

    // Step 3: Present option
    suggestion = """
    Converting PDF to Markdown requires specialized
    PDF parsing. The pdf-processor skill handles
    text extraction, table recognition, and formatting.

    Want me to add it?

    • Provides: PDF text extraction, table parsing, format preservation
    • Accuracy: 95%+ on technical documents
    • Source: anthropics/skills/ms-office-suite/pdf
    """

    await suggest(suggestion);

    // Step 4: Get permission
    if (await user.confirm()) {
        await skillmeat("add skill anthropics/skills/ms-office-suite/pdf");
        await skillmeat("deploy pdf-processor");

        // Step 5: Use it
        markdown = await pdf_processor.extract_and_convert(file);
        return markdown;
    }
}
```

---

### Example 5: Cross-Agent Recommendation

**Scenario**: Backend engineer creates complex query aggregator; frontend engineer needs to consume it.

**Backend engineer's flow**:

```
// Step 1: Complete backend task
analytics_endpoint = create_analytics_aggregator()

// Step 2: Recognize frontend will need help consuming this
if (requires_complex_state_management()) {
    // Step 3: Suggest to frontend engineer
    recommendation = {
        artifact: "react-query-helper",
        reason: "Handles complex query caching and synchronization",
        related_endpoint: analytics_endpoint,
        source: "anthropics/skills/react-query-helper"
    }

    // Step 4: Pass to next agent
    Task("ui-engineer",
         "New analytics API created.
          The react-query-helper skill handles
          complex queries. Should I deploy it?

          Source: anthropics/skills/react-query-helper")
}
```

**Frontend engineer receives**:

```
New API available: /api/v1/analytics/aggregated

(from backend engineer)
"The react-query-helper skill can wire this efficiently.
Want me to add it?"

Agent: The analytics endpoint needs sophisticated
       query caching and background refresh.

       react-query-helper is perfect for this.
       Adding it...

✓ Deployed react-query-helper
  Creating analytics dashboard component...
```

---

## Artifact Naming and Resolution

skillmeat-cli uses fuzzy matching to resolve artifact names:

### Common Artifact Names

```
User Input          → Resolves To
─────────────────────────────────────────────────
"pdf"               → ms-office-suite:pdf
"docx"              → ms-office-suite:docx
"xlsx"              → ms-office-suite:xlsx
"canvas"            → canvas-design
"testing"           → test-framework
"database"          → database-designer
"forms"             → form-builder
"api"               → openapi-expert
"a11y"              → accessibility-checker
```

When suggesting artifacts, use clear names and always provide the full source:

```markdown
**GOOD**:
"The pdf skill (anthropics/skills/ms-office-suite/pdf)
 can extract text from PDFs."

**AVOID**:
"The pdf thing might help" (vague)
"Install anthropics/skills/ms-office-suite/pdf" (no explanation)
```

---

## Error Handling

### Network/Rate Limit Errors

```bash
# If search fails due to rate limiting
Error: Rate limit exceeded

Solution: Suggest user set GitHub token
skillmeat config set github-token <token>
```

### Artifact Not Found

```bash
# If search returns empty
skillmeat search "very-specific-capability" --json
# Returns: { "results": [], "total": 0 }

Action: Inform user and suggest alternatives
"No existing skill found for [capability].
 Would you like to create one?"
```

### Permission Denied During Deploy

```bash
skillmeat deploy canvas-design
# Error: Permission denied on .claude/skills/

Solution: Check directory permissions
          Suggest user run with appropriate permissions
```

---

## Best Practices

### DO:

✓ **Search silently** - User doesn't need to see search output
✓ **Suggest specifically** - Name the artifact and its benefits
✓ **Wait for permission** - Never assume "yes"
✓ **Confirm success** - Report when deployment completes
✓ **Provide context** - Explain why artifact helps
✓ **Handle "no" gracefully** - Implement manually if user declines
✓ **Use full sources** - Always include complete source path
✓ **Check project context** - Consider what's already deployed

### DON'T:

✗ **Auto-deploy** - This breaks user trust
✗ **Over-suggest** - One artifact per suggestion
✗ **Vague recommendations** - "Might be useful" isn't enough
✗ **Ignore user preference** - If user says "no", respect it
✗ **Suggest already-deployed skills** - Check with `skillmeat list --project .`
✗ **Deploy to wrong project** - Always verify `--project` path
✗ **Assume compatibility** - Different frameworks may conflict
✗ **Interrupt focused work** - Ask if suggestion is welcome

---

## Related Documentation

- **skillmeat-cli SKILL.md**: Main skill documentation and workflows
- **command-quick-reference.md**: Complete command reference
- **Claude Code Main Docs**: Agent delegation patterns in CLAUDE.md

---

## Support

For issues or questions about artifact recommendations:

1. Check `skillmeat list --json` to see available artifacts
2. Use `skillmeat show <artifact-name>` for details
3. Run `skillmeat search <query> --json` to explore
4. Consult artifact's own documentation for integration help
