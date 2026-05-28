# Onboarding Documentation Templates

Templates for generating `docs/onboarding/` files. These are **full tutorials** for developers new to the codebase. Link to (don't repeat) architecture and standards content.

## Key Principles

1. **Tutorial style**: Step-by-step instructions a new developer can follow
2. **Reference, don't repeat**: Link to architecture/standards docs for detailed rationale
3. **Practical focus**: "How to" guides, not "why" explanations
4. **Numbered for progression**: Files ordered by logical learning path

---

## 01-setup.md

```markdown
# Environment Setup

Get your local development environment running.

## Prerequisites

- {Language runtime} ({version})
- {Package manager} ({version})
- {Database/services} (if needed)
- {Other tools}

### Installing Prerequisites

<details>
<summary>macOS</summary>

```bash
{macOS installation commands}
```

</details>

<details>
<summary>Linux</summary>

```bash
{Linux installation commands}
```

</details>

<details>
<summary>Windows</summary>

```bash
{Windows installation commands}
```

</details>

## Clone and Install

```bash
# Clone the repository
git clone {repo-url}
cd {project-name}

# Install dependencies
{install command}
```

## Configuration

### Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{VAR_NAME}` | {Purpose} | `{example value}` |

### Local Services

{Instructions for setting up any required local services like databases.}

```bash
# Start local database (example)
{database start command}
```

## Verify Installation

Run the test suite to verify everything is working:

```bash
{test command}
```

Expected output:
```
{what success looks like}
```

## Running Locally

Start the development server:

```bash
{dev command}
```

Access the application at `http://localhost:{port}`.

## IDE Setup

### Recommended Extensions

- {Extension 1} — {Purpose}
- {Extension 2} — {Purpose}

### Settings

{Any recommended IDE settings or configuration files to use.}

## Troubleshooting

### {Common Issue 1}

**Symptom**: {What you see}

**Solution**:
```bash
{fix command}
```

### {Common Issue 2}

**Symptom**: {What you see}

**Solution**: {Steps to fix}

## Next Steps

- Read the [Architecture Overview](../architecture/01-overview.md) to understand the system design
- Review [Coding Standards](../standards/) before making changes
- Continue to [Making Your First Contribution](./02-first-contribution.md)
```

---

## 02-first-contribution.md

```markdown
# Making Your First Contribution

Guide to making your first code contribution to the project.

## Before You Start

Ensure you've completed [Environment Setup](./01-setup.md) and your local environment is working.

Familiarize yourself with:
- [Architecture Overview](../architecture/01-overview.md) — understand the system structure
- [Directory Structure](../architecture/02-directory-structure.md) — know where things live
- [Coding Standards](../standards/) — conventions to follow

## Development Workflow

### 1. Create a Branch

```bash
# Start from main
git checkout main
git pull origin main

# Create feature branch
git checkout -b {branch-naming-convention}
```

Branch naming convention: `{pattern}` (e.g., `feature/add-user-auth`, `fix/login-validation`)

### 2. Make Changes

{Overview of the change process}

#### Finding Your Way Around

| To work on... | Look in... |
|---------------|------------|
| {Area 1} | `{path}` |
| {Area 2} | `{path}` |

See [Directory Structure](../architecture/02-directory-structure.md) for full layout.

#### Code Style

Follow the patterns in:
- [Naming Conventions](../standards/naming-conventions.md)
- [Error Handling](../standards/error-handling.md)
- {Other relevant standards}

### 3. Test Your Changes

```bash
# Run unit tests
{unit test command}

# Run linter
{lint command}

# Run full test suite
{full test command}
```

See [Testing Standards](../standards/testing.md) for testing conventions.

### 4. Commit Your Changes

```bash
# Stage changes
git add {files}

# Commit with descriptive message
git commit -m "{commit message format}"
```

Commit message format: `{pattern}`

Examples:
- `feat: add user authentication`
- `fix: resolve login validation error`
- `docs: update API documentation`

### 5. Push and Create PR

```bash
# Push your branch
git push -u origin {branch-name}
```

Create a pull request:
1. Go to {repo URL}
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template

### PR Checklist

Before submitting:

- [ ] Tests pass locally
- [ ] Linter passes
- [ ] New code has tests
- [ ] PR description explains the change
- [ ] Linked to issue (if applicable)

## Code Review Process

{Description of the review process}

### Responding to Feedback

- Address all comments before merging
- Mark conversations as resolved after addressing
- Request re-review after making changes

### After Approval

{How merging works — squash, merge commit, etc.}

## Common Tasks

### Adding a New Feature

1. {Step 1}
2. {Step 2}
3. {Step 3}

See [Core Components](../architecture/03-core-components.md) for module responsibilities.

### Fixing a Bug

1. Write a failing test that reproduces the bug
2. Fix the bug
3. Verify the test passes
4. Check for related edge cases

### Adding Tests

Location: `{test directory pattern}`

Naming: `{test file naming pattern}`

See [Testing Standards](../standards/testing.md) for conventions.

## Getting Help

- {How to ask questions — Slack channel, GitHub discussions, etc.}
- {Who to contact for different areas}
- {Links to additional resources}
```

---

## Additional Onboarding Docs (as needed)

### 03-workflow.md (optional)

```markdown
# Development Workflow

Detailed workflow for common development tasks.

## Feature Development

{Detailed feature development process}

## Bug Fixing

{Detailed bug fixing process}

## Hotfixes

{Emergency fix process}
```

### 04-debugging.md (optional)

```markdown
# Debugging Guide

How to debug common issues in this codebase.

## Debugging Tools

{Available debugging tools and how to use them}

## Common Debug Scenarios

{Step-by-step debugging for common issues}
```

---

## Writing Guidelines

### Do

- Write step-by-step instructions that a new developer can follow
- Include copy-pasteable commands
- Provide troubleshooting for common issues
- Link to architecture/standards docs for "why" explanations
- Use collapsible sections for platform-specific content
- Include expected output so readers know they're on track

### Don't

- Repeat detailed rationale from architecture docs
- Duplicate coding standards (link instead)
- Assume prior knowledge of the codebase
- Skip steps that seem "obvious"
- Include outdated commands or paths

### Linking Pattern

When referencing other docs:

```markdown
<!-- Good: Clear link with context -->
See [Architecture Overview](../architecture/01-overview.md) to understand the system design.

<!-- Good: Inline reference -->
Follow the patterns in [Naming Conventions](../standards/naming-conventions.md).

<!-- Bad: Repeating content from other docs -->
The system uses a layered architecture where... [500 words duplicating architecture doc]
```
