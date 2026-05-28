# Collection Templates

Pre-curated artifact collections for common development stacks.

## Available Templates

### 1. React Development (`react.toml`)

**For**: React, Next.js, TypeScript frontend projects

**Includes**:
- `frontend-design` (required) - UI patterns, Tailwind CSS
- `webapp-testing` (optional) - Jest, Testing Library
- `chrome-devtools` (optional) - Browser debugging
- `npm-package-manager` (optional) - NPM/Yarn management

**Usage**:
```bash
skillmeat template apply react
```

**Best For**: Single-page apps, Next.js projects, React component libraries

---

### 2. Python Development (`python.toml`)

**For**: Python backend projects (FastAPI, Django, Flask)

**Includes**:
- `openapi-expert` (optional) - API schema design
- `postgresql-psql` (optional) - Database management
- `pytest-expert` (optional) - Python testing
- `python-package-manager` (optional) - Pip/Poetry/uv
- `data-processing` (optional) - Pandas, NumPy

**Usage**:
```bash
skillmeat template apply python
```

**Best For**: REST APIs, microservices, data processing backends

---

### 3. Node.js Backend (`nodejs.toml`)

**For**: Node.js/Express backend projects with TypeScript

**Includes**:
- `webapp-testing` (optional) - Jest, Supertest
- `openapi-expert` (optional) - API documentation
- `postgresql-psql` (optional) - Database queries
- `npm-package-manager` (optional) - Package management
- `typescript-config` (optional) - TypeScript setup

**Usage**:
```bash
skillmeat template apply nodejs
```

**Best For**: Express APIs, GraphQL servers, TypeScript backends

---

### 4. Full-Stack Development (`fullstack.toml`)

**For**: Complete web applications with frontend + backend

**Includes**:
- `frontend-design` (required) - UI development
- `webapp-testing` (optional) - Full-stack testing
- `openapi-expert` (required) - API contracts
- `postgresql-psql` (optional) - Database
- `chrome-devtools` (optional) - Debugging
- `python-package-manager` (optional) - Python backend deps
- `npm-package-manager` (optional) - Frontend deps
- `data-processing` (optional) - Data transformation

**Recommended Stacks**:
1. **Next.js + FastAPI**: Modern, type-safe, excellent DX
2. **Next.js + Express**: Full TypeScript, shared types
3. **React SPA + Django**: Django admin + REST API

**Usage**:
```bash
skillmeat template apply fullstack
```

**Best For**: Monorepo projects, complex web applications, SaaS products

---

## Template Commands

### Apply Template
```bash
# Apply template to current project
skillmeat template apply <name>

# Preview without applying
skillmeat template apply <name> --dry-run

# Apply with custom scope
skillmeat template apply <name> --scope local
```

### List Templates
```bash
# List all available templates
skillmeat template list

# Show template details
skillmeat template show <name>
```

### Template Structure

Each template includes:
- **Metadata**: Name, description, version, tags
- **Artifacts**: Required and optional skills/tools
- **Dependencies**: Runtime requirements (node, python, etc.)
- **Recommendations**: Suggested packages, scripts, tools
- **Notes**: Setup guides, best practices, project structure

---

## Customization

Templates are starting points. After applying:

1. **Add more artifacts**: `skillmeat add <source>`
2. **Remove unwanted**: Edit `.claude/manifest.toml`
3. **Adjust scope**: Move artifacts between user/local scopes
4. **Update versions**: `skillmeat sync` to get latest

---

## Creating Custom Templates

Copy an existing template and modify:

```toml
[template]
name = "my-custom-stack"
display_name = "My Custom Stack"
description = "..."
version = "1.0.0"
tags = ["custom"]

[[artifacts]]
name = "artifact-name"
type = "skill"
source = "owner/repo/path"
required = true
description = "..."

[dependencies]
node = ">=18.0.0"

[notes]
setup_guide = """
Custom setup instructions...
"""
```

Save to `.claude/skills/skillmeat-cli/templates/my-custom-stack.toml`

---

## Best Practices

1. **Start minimal**: Apply basic template, add more as needed
2. **Use dry-run**: Preview before applying (`--dry-run`)
3. **Keep updated**: Run `skillmeat sync` regularly
4. **Document customizations**: Note changes in project docs
5. **Share templates**: Contribute useful templates back to community

---

## Examples

### Example 1: New React App
```bash
# Create new Next.js project
npx create-next-app@latest my-app --typescript --tailwind --app

# Apply React template
cd my-app
skillmeat init
skillmeat template apply react

# Start coding with artifact support
npm run dev
```

### Example 2: Python API Project
```bash
# Create project structure
mkdir my-api && cd my-api
python -m venv venv
source venv/bin/activate

# Apply Python template
skillmeat init
skillmeat template apply python

# Install dependencies
pip install fastapi uvicorn sqlalchemy
```

### Example 3: Full-Stack Monorepo
```bash
# Create monorepo structure
mkdir my-fullstack && cd my-fullstack
mkdir api web shared

# Apply full-stack template
skillmeat init
skillmeat template apply fullstack

# Set up backend
cd api && python -m venv venv && pip install -e ".[dev]"

# Set up frontend
cd ../web && npm install
```

---

## Template Versioning

Templates follow semantic versioning:
- **Major**: Breaking changes (incompatible artifacts)
- **Minor**: New features (additional artifacts)
- **Patch**: Bug fixes, documentation updates

Check template version:
```bash
skillmeat template show <name> | grep version
```

---

## Support

For issues or suggestions:
- GitHub Issues: [skillmeat/issues](https://github.com/user/skillmeat/issues)
- Documentation: [docs/templates.md](../../docs/templates.md)
- Community: [Discord/Slack](#)
