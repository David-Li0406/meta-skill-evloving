# Transformation Rules for AI-Optimized Documentation

Apply these rules when transforming documents for Claude Code consumption.

## Structure Rules

### 1. Strict Heading Hierarchy

Use H1 → H2 → H3 progression. Never skip levels. Avoid H4+ when possible.

```markdown
# Title (H1 - one per document)

## Major Section (H2)

### Subsection (H3)

# Avoid H4+ - restructure content instead
```

**Why**: LLMs build mental maps from heading structure. Skipping levels breaks content relationship understanding. H4+ creates ambiguity in AI pattern recognition - prefer flatter hierarchies with clear H2/H3 boundaries.

### 2. Tables Over Prose

Convert lists of related items into tables.

**Before**:

```markdown
The dev command starts the development server. The build command creates
a production build. The test command runs the test suite.
```

**After**:

```markdown
| Command         | Purpose                  |
| --------------- | ------------------------ |
| `npm run dev`   | Start development server |
| `npm run build` | Create production build  |
| `npm run test`  | Run test suite           |
```

### 3. Bullet Points Over Paragraphs

Convert dense paragraphs into scannable lists.

**Before**:

```markdown
You should use ES modules for imports, follow the existing naming
conventions, and add tests for new functionality.
```

**After**:

```markdown
- Use ES modules for imports
- Follow existing naming conventions
- Add tests for new functionality
```

### 4. Front-Load Critical Information

Place most important content at the beginning of sections.

**Pattern**:

1. What it is / does (1 sentence)
2. Key constraints or requirements
3. Details and examples
4. Edge cases and exceptions

### 5. Single Topic Per Section

Each heading should cover one concept. Split mixed-topic sections.

**Before**:

```markdown
## Authentication and Authorization

Configure login, manage sessions, and set up role-based permissions...
```

**After**:

```markdown
## Authentication

Configure login and manage sessions...

## Authorization

Set up role-based permissions...
```

### 6. Blockquote Summary After Title

Add a one-sentence summary immediately after the H1 title.

**After**:

```markdown
# Pattern Name

> One-sentence summary of what this pattern solves and when to use it.

## First Section
```

**Why**: Provides instant context for Claude to determine relevance. From llms.txt standard (844K+ sites).

### 7. End-Load Actionable Instructions

Place checklists, summaries, and key takeaways at the document END.

**Why**: Anthropic research shows LLMs have better recall for content at document beginning AND end (U-shaped attention curve). Middle content has ~30% lower recall.

**Structure**:

- First 20%: Critical rules, key context
- Middle 60%: Details, examples, explanations
- Final 20%: Actionable checklists, summaries, instructions to apply

---

## Content Rules

### 1. Consistent Terminology

Pick one term and use it throughout. No synonyms.

| Instead of cycling through...          | Use one consistently |
| -------------------------------------- | -------------------- |
| API key, access token, auth credential | API key              |
| user, customer, client                 | user                 |
| error, exception, failure              | error                |

### 2. Explicit References (Eliminate Vague Pronouns)

Replace "it," "this," "that," "they" with specific nouns. Repetition is preferred over ambiguity.

**Why**: LLMs may process sections out of order. Vague pronouns require context that may not be available.

**Before**:

```markdown
Update it and restart. If it fails, check the logs.
This causes problems when that happens.
```

**After**:

```markdown
Update the configuration file and restart the server.
If the server fails, check the server logs.
Missing organization_id filtering causes data leaks when users access shared endpoints.
```

**Pronouns to eliminate**: it, this, that, they, these, those, here, there

### 3. Imperative Form

Write instructions as direct commands.

**Before**:

```markdown
You should run the database migration.
You need to verify the output.
```

**After**:

```markdown
Run the database migration.
Verify the output.
```

### 4. Positive Framing

State what to do, not what to avoid.

**Before**:

```markdown
Don't use CommonJS require statements.
Never commit directly to main.
```

**After**:

```markdown
Use ES module import statements.
Create a feature branch before committing.
```

### 5. Complete Code Examples

Include all context needed to run the code.

**Before**:

```javascript
const data = await fetchData();
```

**After**:

```javascript
import { fetchData } from "@/services/api";

// Fetch user data from the API
const data = await fetchData({
  endpoint: "/users",
  timeout: 5000,
});
```

---

## Format Rules

### 1. XML Tags for Claude

Wrap semantic sections in XML tags for reliable parsing.

```markdown
<when_to_use>

## When to Use

- Trigger phrase 1
- Trigger phrase 2
  </when_to_use>

<workflow>
## Workflow
| Step | Action |
|------|--------|
| 1 | First step |
</workflow>
```

### 2. Fenced Code Blocks

Always specify the language.

````markdown
```javascript
const x = 1;
```
````

```

Never use inline code for multi-line content.

### 3. Target Length

| Document Type | Target Lines | Overflow Strategy |
|--------------|--------------|-------------------|
| CLAUDE.md | < 300 | Move details to pattern files |
| Pattern files | < 500 | Progressive disclosure |
| Skill files | < 300 | Use references/ subdirectory |

### 4. Remove Redundancy

- Delete duplicate explanations
- Consolidate similar sections
- Remove filler phrases ("It should be noted that...", "As mentioned above...")

### 5. Self-Contained Sections

Each section should work without requiring context from other sections.

- Include necessary background at section start
- Use explicit cross-references when linking to other content
- Avoid orphaned references that depend on prior reading

---

## Token Efficiency

### Concise Language

| Verbose | Concise |
|---------|---------|
| In order to | To |
| It is important to note that | Note: |
| At the present time | Now |
| Due to the fact that | Because |
| In the event that | If |

### Remove Placeholder Content

Delete sections that add no value:
- "TODO: Add content here"
- Empty examples
- Repeated boilerplate

### Prioritize Signal Over Noise

Every line should either:
1. Provide actionable instruction
2. Explain critical context
3. Show a concrete example

If a line does none of these, consider removing it.
```
