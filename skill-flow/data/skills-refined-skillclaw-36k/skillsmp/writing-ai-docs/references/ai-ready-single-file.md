---
title: "AI-Ready Single File Documentation"
description: "Core principles and rules for writing individual markdown files that AI tools can effectively process"
skill: writing-ai-docs
type: reference
created: 2025-10-20
lastUpdated: 2025-10-28
---

## Why AI Reads Differently

AI tools process documentation through **chunking** - splitting files into 500-1000 token pieces based on
semantic similarity. Each chunk may be read independently, so:

- **Sections must be self-contained** - AI may only see one chunk
- **Context must be explicit** - AI can't infer unstated requirements
- **Terminology must be consistent** - Synonyms confuse embedding similarity
- **Structure must be strict** - Heading hierarchy builds AI's mental model

## The 5 Structural Rules

### 1. One H1, Strict Hierarchy

**Rule**: ONE H1 per document. Never skip heading levels.

```markdown
✅ CORRECT:
# Document Title
## Section
### Subsection
#### Detail

❌ WRONG:
# Document Title
### Subsection (skipped H2)
##### Detail (skipped H3 and H4)
```

**Why**: AI builds document structure from heading hierarchy. Skipped levels break the mental model.

### 2. Self-Contained Sections

**Rule**: Each section must work independently without reading other sections.

```markdown
✅ CORRECT:
## Rate Limits

Rate limits control API requests per hour to prevent abuse.

**Your limits**:
- Free tier: 100 requests/hour
- Pro tier: 1000 requests/hour

**Check remaining quota**:
```http
X-RateLimit-Remaining: 45
```

**When exceeded**: Returns 429 status code.

❌ WRONG:

## Rate Limits

Controls API usage. [No context about what/why/how]

[10 sections later...]

## Headers

Use X-RateLimit-Remaining to check limits. [Separated from definition]

```

**Why**: Chunking may retrieve only one section. It needs its own context.

### 3. Consistent Terminology

**Rule**: Use ONE term per concept throughout the entire document.

```markdown
✅ CORRECT:
"Use your API key... The API key should be... Insert the API key..."
(Same term repeated)

❌ WRONG:
"Use your API key... The access token should be... Insert the auth credential..."
(Three different terms for the same thing)
```

**Why**: AI matches by semantic similarity. Synonyms reduce match accuracy by 40-60%.

### 3. Code in Fenced Blocks

**Rule**: All code must be in fenced blocks with language tags. Never inline.

```markdown
✅ CORRECT:
Install the package:
```bash
npm install @company/sdk
```

Then configure:

```javascript
const sdk = new SDK({ apiKey: process.env.API_KEY });
```

❌ WRONG:
Install with npm install @company/sdk and configure it with your API key.

```

**Why**: AI tools struggle to parse commands embedded in prose. They may alter or merge them.

### 5. Explicit Prerequisites

**Rule**: State all requirements explicitly. Never assume context.

```markdown
✅ CORRECT:
## Prerequisites

Before configuring webhooks, ensure you have:
- Publicly accessible HTTPS URL (not localhost)
- Valid SSL certificate (self-signed not supported)
- API credentials from Settings > API Keys in dashboard
- Webhook endpoint that responds to POST requests

❌ WRONG:
## Prerequisites

Configure your webhook endpoint in the dashboard.
```

**Why**: AI cannot infer unstated requirements. Users waste time discovering missing steps.

## File Naming Conventions

**Format**: `lowercase-kebab-case.md`

**Rules**:

- Lowercase only (`a-z`, `0-9`, hyphens)
- Use hyphens, not underscores or spaces
- Under 50 characters
- Descriptive, not abbreviated
- Match document content/purpose

**Good examples**:

```text
installation-guide.md
api-authentication.md
troubleshooting-rate-limits.md
tutorial-first-oauth-app.md
reference-cli-commands.md
how-to-deploy-production.md
understanding-webhooks.md
```

**Bad examples**:

```text
install.md              # Too vague
API_Auth.md             # Not lowercase, underscore
trouble shooting.md     # Spaces not allowed
tut-1st-app.md         # Unclear abbreviations
API-Documentation.md    # Not lowercase
```

**Special files** (always capitalized):

```text
README.md               # Project overview
CHANGELOG.md            # Version history
CONTRIBUTING.md         # Contribution guide
LICENSE.md              # License information
```

**Why it matters**: Consistent naming enables AI tools to:

- Infer content from filename
- Group related documents
- Suggest relevant files to load
- Build better search indexes

## The 3 Content Patterns

### 1. Explicit Over Implicit Language

**Pattern**: Use specific names, not vague pronouns.

```markdown
✅ EXPLICIT:
"Update the database.conf file and restart the database service.
If the database service fails, check the database logs in /var/log/db/"

❌ VAGUE:
"Update the config file and restart it. If it fails, check the logs."
```

### 2. Keep Related Information Together

**Pattern**: Definition + application in the same section.

```markdown
✅ TOGETHER:
## Authentication

Authentication uses Bearer tokens in the Authorization header.

**Get your API key**: Dashboard > Settings > API Keys

**Use in requests**:
```http
Authorization: Bearer YOUR_API_KEY
```

**Example**:

```bash
curl -H "Authorization: Bearer sk_test_123" https://api.example.com/users
```

❌ SCATTERED:

## Authentication

Uses Bearer tokens. [Definition only]

[10 sections later]

## Making Requests

Add your API key to the header. [Application separated from definition]

```

### 3. Repeat Context in Each Section

**Pattern**: Brief context at section start, even if mentioned before.

```markdown
✅ WITH CONTEXT:
## Step 3: Configure OAuth

OAuth handles user authentication using the authorization code flow.

**Prerequisites for this step**:
- Client ID and Secret from Step 1
- Redirect URI configured in dashboard

[Continue with step content...]

❌ WITHOUT CONTEXT:
## Step 3: Configure OAuth

Now configure the OAuth settings... [Assumes reader completed Step 1 and 2]
```

## The 5 Worst Anti-Patterns

### ❌ 1. Skipped Heading Levels

**Impact**: Breaks AI's document structure understanding
**Fix**: Always use H1→H2→H3→H4 progression

### ❌ 2. Inconsistent Terminology

**Impact**: Reduces AI retrieval accuracy by 40-60%
**Fix**: Create terminology list, use ONE term per concept

### ❌ 3. Scattered Related Content

**Impact**: AI retrieves definition without application (or vice versa)
**Fix**: Keep definition + usage + examples in same section

### ❌ 4. Vague Pronouns

**Impact**: AI cannot resolve "it", "this", "they" without clear antecedent
**Fix**: Use specific nouns instead of pronouns

### ❌ 5. Inline Code Mixed With Prose

**Impact**: AI alters or merges commands during processing
**Fix**: Always use fenced code blocks with language tags

## Validation Checklist

Before publishing, verify:

**File**:

- [ ] Filename is lowercase-kebab-case.md
- [ ] Filename under 50 characters
- [ ] Filename descriptive and matches content

**Structure**:

- [ ] YAML frontmatter with title, description, type, created, lastUpdated
- [ ] One H1 matching document title
- [ ] No skipped heading levels
- [ ] Sections follow logical progression

**Content**:

- [ ] Opening paragraph states purpose and audience
- [ ] Prerequisites explicitly listed with versions/requirements
- [ ] Each section self-contained with context
- [ ] ONE term used consistently per concept
- [ ] No vague pronouns without clear antecedent

**Code**:

- [ ] All code in fenced blocks with language tags
- [ ] No commands inline in prose
- [ ] Complete, runnable examples
- [ ] Expected output shown
- [ ] Error cases covered

**AI Readiness**:

- [ ] Related content physically close (not scattered)
- [ ] Definitions near applications
- [ ] Context repeated in major sections
- [ ] Common issues section included
- [ ] Next steps provided

## Key Principles Summary

**The Three Imperatives**:

1. **Explicit > Implicit** - State everything clearly
2. **Consistent > Varied** - One term per concept
3. **Self-Contained > Cross-Referenced** - Each section works alone

**The Critical Five**:

1. YAML frontmatter on every file
2. One H1, no skipped heading levels
3. Code in fenced blocks with language tags
4. Prerequisites explicitly listed
5. Each section self-contained

**Red Flags** (fix immediately):

- Bad filename (spaces, capitals, underscores, abbreviations)
- Skipped heading levels (H1→H3)
- Multiple terms for same concept
- Inline code without blocks
- Vague pronouns ("it", "this", "they")
- Related content scattered across document
