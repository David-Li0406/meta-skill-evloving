# Code Project CLAUDE.md Template

Use this template for Node.js, Python, Go, Java, and other code projects.

---

```markdown
# [Project Name]

## Quick Reference

\`\`\`bash
# Development
[package-manager] install    # Install dependencies
[package-manager] run dev    # Start development server
[package-manager] run build  # Build for production

# Testing
[package-manager] test       # Run tests
[package-manager] test:cov   # Run with coverage

# Linting
[package-manager] lint       # Check code style
[package-manager] lint:fix   # Auto-fix issues
\`\`\`

---

## 1. Project Overview

**Type**: [Framework/Library/Application]
**Language**: [Language] [Version]
**Framework**: [Framework name and version]

### Key Dependencies

| Package | Purpose |
|---------|---------|
| [dep-1] | [Purpose] |
| [dep-2] | [Purpose] |

---

## 2. Project Structure

\`\`\`
[project-name]/
├── src/              # Source code
│   ├── components/   # [If applicable]
│   ├── services/     # Business logic
│   └── utils/        # Utilities
├── tests/            # Test files
├── scripts/          # Build/utility scripts
└── docs/             # Documentation
\`\`\`

### Key Files

| File | Purpose |
|------|---------|
| `[config-file]` | [Configuration purpose] |
| `[entry-point]` | Application entry |

---

## 3. Development

### Setup

\`\`\`bash
# Clone and install
git clone [repo-url]
cd [project-name]
[package-manager] install

# Environment setup
cp .env.example .env
# Edit .env with your values
\`\`\`

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `[VAR_1]` | Yes | [Description] |
| `[VAR_2]` | No | [Description, default: X] |

---

## 4. Testing

### Test Structure

| Directory | Test Type |
|-----------|-----------|
| `tests/unit/` | Unit tests |
| `tests/integration/` | Integration tests |
| `tests/e2e/` | End-to-end tests |

### Running Tests

\`\`\`bash
# All tests
[package-manager] test

# Specific file
[package-manager] test -- [path/to/test]

# Watch mode
[package-manager] test:watch
\`\`\`

---

## 5. API Reference

[If applicable]

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/[resource]` | List all |
| POST | `/api/[resource]` | Create new |
| GET | `/api/[resource]/:id` | Get by ID |

### Authentication

[Auth mechanism - JWT, API key, OAuth, etc.]

---

## 6. Deployment

### Build

\`\`\`bash
[package-manager] run build
\`\`\`

### CI/CD

| Stage | Actions |
|-------|---------|
| Test | Run linting, unit tests |
| Build | Compile/bundle |
| Deploy | [Deployment target] |

---

## 7. Conventions

### Code Style

- [Style guide reference]
- [Naming conventions]
- [File organization rules]

### Git Workflow

- Branch naming: `[pattern]`
- Commit format: `[format]`
- PR process: [Process]
```

---

## Customization Notes

- Adjust package manager commands (npm, yarn, pnpm, pip, go, etc.)
- Remove sections not applicable
- Add framework-specific sections (React components, Django apps, etc.)
- Include debugging tips if relevant
