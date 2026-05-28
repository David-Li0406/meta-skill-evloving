---
name: doc-writer
description: Documentation specialist for Faiston NEXO. Use when creating README files, API docs, code comments, or explaining complex code. Keeps all docs in docs/ folder.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Doc Writer Skill

Documentation specialist for the Faiston NEXO platform.

## Project Context

| Aspect | Details |
|--------|---------|
| Domain | Educational platform (LMS-style) |
| Frontend | React 18 + TypeScript + Vite + Tailwind + shadcn/ui |
| Backend | FastAPI + Python 3.11 + Mangum (Lambda) |
| AI Agents | Google ADK + Bedrock AgentCore + Gemini 3.0 Pro |
| Infrastructure | Terraform + AWS (Lambda, S3, DynamoDB, Cognito) |
| Audience | Full-stack developers, DevOps, AI engineers |
| Tone | Clear, concise, practical |
| Location | All docs in `docs/` folder |

## Documentation Structure

```
docs/
├── README.md                    # Documentation index
├── KNOWN_ISSUES.md             # Troubleshooting reference
├── AgentCore/
│   └── IMPLEMENTATION_GUIDE.md # AgentCore architecture guide
├── architecture/               # System design docs
├── api/                        # API documentation
└── agents/                     # Agent documentation
```

## Key Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `CLAUDE.md` | AI assistant instructions | Claude/AI tools |
| `README.md` | Project overview | New developers |
| `docs/KNOWN_ISSUES.md` | Troubleshooting | All developers |
| `docs/AgentCore/IMPLEMENTATION_GUIDE.md` | Agent architecture | AI engineers |
| `client/CLAUDE.md` | Frontend context | Frontend devs |
| `server/CLAUDE.md` | Backend context | Backend devs |
| `terraform/CLAUDE.md` | Infra context | DevOps |

## Documentation Types

### 1. README Files

**Structure for Features:**

```markdown
# Feature Name

Brief description (1-2 sentences)

## Quick Start

\`\`\`bash
# Commands to get started
pnpm dev
\`\`\`

## Usage

### Basic Example

\`\`\`tsx
import { Component } from "@/components/Component"

function Example() {
  return <Component prop="value" />
}
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | required | Card title |
| `onClose` | `() => void` | - | Close callback |

## Troubleshooting

### Issue: Component not rendering

**Cause:** Missing provider wrapper

**Solution:**
\`\`\`tsx
<Provider>
  <Component />
</Provider>
\`\`\`
```

### 2. Component Documentation

```markdown
# ComponentName

## Purpose

What this component does and when to use it.

## Props Interface

\`\`\`typescript
interface Props {
  /** Display title - required */
  title: string

  /** Content to render inside */
  children: React.ReactNode

  /** Called when user clicks action button */
  onAction?: () => void
}
\`\`\`

## Examples

### Basic Usage

\`\`\`tsx
<Card title="Welcome">
  <p>Hello world</p>
</Card>
\`\`\`

## Accessibility

- Keyboard navigable
- ARIA labels on interactive elements
- Focus visible states
```

### 3. API Documentation (Mock Endpoints)

```markdown
# API Reference

## Authentication

### POST /api/auth/login

Login with email and password.

**Request:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "password123"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "user": {
    "id": "1",
    "email": "user@example.com",
    "name": "User Name"
  },
  "token": "jwt-token-here"
}
\`\`\`

**Errors:**
- `401` - Invalid credentials
- `400` - Missing required fields

**Mock Handler:** `client/mocks/handlers.ts`
```

## Documentation Best Practices

### Writing Style

- Use present tense ("renders", not "will render")
- Be concise - no unnecessary words
- Use bullet points for lists
- Include code examples

### Code Examples

- Always test examples work
- Use realistic data
- Show imports
- Include TypeScript types

### Tables

Use tables for:
- Props documentation
- API parameters
- Command references
- Feature comparisons

### File Location

**All documentation goes in `docs/` folder:**
- `docs/README.md` - Documentation index
- `docs/architecture/` - System design docs
- `docs/components/` - Component guides
- `docs/api/` - API documentation

## Documentation Checklist

Before completing documentation:

- [ ] Accurate and up-to-date
- [ ] Code examples tested
- [ ] Links work (relative paths)
- [ ] Tables formatted correctly
- [ ] Located in `docs/` folder
- [ ] Added to docs/README.md index
- [ ] No typos

## Response Format

When creating documentation:

1. **Identify the audience**
   - New developers? Contributors? Users?
   - What do they need to accomplish?

2. **Structure for scanning**
   - Clear headings
   - Code examples early
   - Tables for reference

3. **Keep it maintainable**
   - Don't duplicate information
   - Link to source of truth
   - Use relative paths

4. **Location reminder**
   - All docs in `docs/` folder
   - Update docs/README.md index

Remember: Good documentation is documentation that gets read!

---

## Faiston NEXO Specific Documentation

### AgentCore Documentation

**Location**: `docs/AgentCore/`

```markdown
# Agent Name

## Purpose

What this agent does and when it's invoked.

## Actions

| Action | Input | Output |
|--------|-------|--------|
| `action_name` | `{field: type}` | `{response: type}` |

## Architecture

\`\`\`
Frontend → Cognito JWT → AgentCore Runtime → Agent → Gemini 3.0 Pro
\`\`\`

## Implementation

**File**: `server/agentcore/agents/agent_name.py`

\`\`\`python
AGENT_INSTRUCTION = """
[System instruction here]
"""
\`\`\`

## Deployment

- Workflow: `.github/workflows/deploy-agentcore.yml`
- Trigger: Push to `server/agentcore/**`
```

### FastAPI Endpoint Documentation

**Location**: `docs/api/`

```markdown
# Endpoint Name

## POST /api/endpoint

Description of what this endpoint does.

### Request

\`\`\`json
{
  "field1": "string",
  "field2": 123
}
\`\`\`

### Response (200)

\`\`\`json
{
  "success": true,
  "data": { ... }
}
\`\`\`

### Errors

| Code | Message | Cause |
|------|---------|-------|
| 400 | Invalid input | Missing required field |
| 401 | Unauthorized | Invalid/expired token |
| 500 | Internal error | Server exception |

### Lambda Handler

**File**: `server/lambda_handler.py`

\`\`\`python
@app.post("/api/endpoint")
async def endpoint_handler(request: RequestModel):
    ...
\`\`\`
```

### Terraform Documentation

**Location**: `terraform/CLAUDE.md` or `docs/infrastructure/`

```markdown
# Resource Name

## Purpose

What AWS resource this manages and why.

## Configuration

\`\`\`hcl
resource "aws_service_resource" "name" {
  name = "faiston-nexo-..."
  # Key configuration
}
\`\`\`

## Dependencies

- Depends on: `resource.other`
- Required by: `resource.dependent`

## Outputs

| Output | Description |
|--------|-------------|
| `resource_arn` | ARN for IAM policies |
| `resource_url` | URL for client config |

## CORS Note

CORS is configured ONLY in `terraform/main/locals.tf`:

\`\`\`hcl
locals {
  cors_allowed_origins = [
    "https://nexo.faiston.com",
    "http://localhost:8081"
  ]
}
\`\`\`
```

### Known Issues Documentation

**Location**: `docs/KNOWN_ISSUES.md`

```markdown
# Known Issues

## Issue: [Short Description]

**Symptom**: What the user sees

**Cause**: Root cause analysis

**Solution**:
\`\`\`code
Fix or workaround
\`\`\`

**Status**: Fixed in PR #123 / Open / Workaround

**Related Files**:
- `path/to/file.ts`
- `path/to/other.py`
```

## Documentation Workflow

### When to Create Documentation

| Event | Documentation Required |
|-------|------------------------|
| New feature | README in `docs/features/` |
| New agent | Entry in `docs/AgentCore/` |
| New API endpoint | Entry in `docs/api/` |
| Bug fix | Update `docs/KNOWN_ISSUES.md` |
| Infrastructure change | Update `terraform/CLAUDE.md` |

### Documentation Review Checklist

- [ ] Located in `docs/` folder (not root)
- [ ] Added to `docs/README.md` index
- [ ] Code examples are tested and work
- [ ] Tables are properly formatted
- [ ] Links use relative paths
- [ ] Brazilian Portuguese for UI text (if applicable)
- [ ] No hardcoded AWS values (use Terraform references)

## Quick Templates

### CLAUDE.md Section

```markdown
## Quick Reference

| Purpose | File |
|---------|------|
| [Purpose] | `path/to/file` |

### Key Patterns

\`\`\`typescript
// Example pattern
\`\`\`

### Common Commands

\`\`\`bash
pnpm dev     # Development
pnpm build   # Production build
pnpm test    # Run tests
\`\`\`
```

### Troubleshooting Section

```markdown
## Troubleshooting

### Problem: [Description]

**Check these first:**
1. [ ] Check 1
2. [ ] Check 2

**Solution:**
\`\`\`bash
# Command or code fix
\`\`\`
```
