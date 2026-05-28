# Claude Multi-Repo Workspace Skill

A powerful skill for managing multiple repositories in a single workspace with intelligent context switching and coordinated changes.

## 📦 Installation

### Option 1: Use in Claude Projects (Recommended)

1. Copy the content from `skill.md`
2. In Claude.ai, create a new Project
3. Go to "Project Knowledge" → "Add content"
4. Paste the skill content
5. Done! Use `@workspace` commands in any conversation within the project

### Option 2: Custom Instructions

1. Copy the content from `custom-instructions.md`
2. In Claude.ai, go to Settings ⚙️ → Personalization → Custom Instructions
3. Paste the content
4. Save

### Option 3: Direct Copy-Paste

Copy and paste the content from `prompt.md` at the start of your conversation with Claude.

---

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/jairoFernandez/llm-skills.git

# 2. Navigate to the skill
cd llm-skills/skills/multi-repo-workspace

# 3. Review available files
ls -la
```

**Main files:**
- `skill.md` - Complete skill (for Projects)
- `custom-instructions.md` - Compact version
- `prompt.md` - Prompt for copy-paste
- `examples/` - Configuration examples
- `templates/` - Templates for .claude/config.json

---

## 📖 Usage

### Initialize a workspace

```
@workspace init my-project

# Claude will ask:
# - Base path of the workspace
# - Repositories to add
```

### Add a repository

```
@workspace add ./new-repo
```

### Analyze workspace

```
@workspace analyze
```

### Focus on a specific repo

```
@workspace focus frontend
```

### Multi-repo task

```
@workspace task "Implement OAuth authentication"
```

---

## 📁 File Structure

```
multi-repo-workspace/
├── README.md                    # This file
├── skill.md                     # Complete skill for Projects
├── custom-instructions.md       # Version for Custom Instructions
├── prompt.md                    # Direct prompt
├── docs/
│   ├── setup-guide.md          # Detailed setup guide
│   ├── commands.md             # Command reference
│   └── best-practices.md       # Best practices
├── examples/
│   ├── monorepo-example/       # Monorepo example
│   ├── microservices-example/  # Microservices example
│   └── fullstack-example/      # Fullstack example
├── templates/
│   ├── .claude/
│   │   ├── config.json         # Configuration template
│   │   └── context.md          # Context template
│   └── .workspace/
│       └── config.json         # Workspace template
└── tests/
    └── skill.test.js           # Skill tests
```

---

## 🎯 Repository Configuration

Each repository in your workspace should have:

### `.claude/config.json`

```json
{
  "repository": {
    "name": "frontend-app",
    "type": "frontend",
    "description": "Main web application",
    "tech_stack": ["react", "typescript", "vite"]
  },
  "development": {
    "conventions": {
      "code_style": "airbnb",
      "naming": "camelCase"
    },
    "commands": {
      "dev": "npm run dev",
      "build": "npm run build",
      "test": "npm test"
    }
  },
  "dependencies": {
    "internal": ["@workspace/shared"],
    "external_critical": ["react"]
  },
  "claude_preferences": {
    "code_generation": {
      "style": "functional",
      "testing": "vitest"
    },
    "review_focus": ["performance", "security"]
  }
}
```

### `.claude/context.md`

```markdown
# Frontend App

## Purpose
Main web application for the project...

## Architecture
- React 18 with TypeScript
- Global state with Zustand
- Routing with React Router v6

## Dependencies
- Consumes API from `backend-api`
- Uses components from `shared-ui`
```

Use the templates in `templates/` as a starting point.

---

## 📚 Examples

### Example 1: Monorepo

```bash
cd examples/monorepo-example
cat README.md
```

### Example 2: Microservices

```bash
cd examples/microservices-example
cat README.md
```

---

## 🛠️ Helper Scripts

### Auto-generate configuration

```bash
# Script to detect and generate .claude/config.json
node scripts/auto-generate-config.js /path/to/your/repo
```

### Validate configuration

```bash
# Validates that all repos have correct configuration
node scripts/validate-workspace.js
```

---

## 🤝 Contributing

Want to improve this skill?

1. Fork the repository
2. Create a branch: `git checkout -b feature/improvement`
3. Commit your changes: `git commit -am 'Add: new functionality'`
4. Push: `git push origin feature/improvement`
5. Open a Pull Request

---

## 📄 License

MIT License - see `LICENSE` for more details

---

## 🐛 Report Issues

Found a bug or have a suggestion?

Open an issue at: https://github.com/yourusername/llm-skills/issues

---

## ⭐ Roadmap

- [ ] Auto-detection of dependencies between repos
- [ ] Automatic knowledge graph generation
- [ ] CLI tool for workspace management
- [ ] VS Code integration
- [ ] Support for more languages/frameworks
- [ ] Web dashboard to visualize workspace

---

## 💡 Tips

- Keep `.claude/config.json` updated when you change your stack
- Document important decisions in `.claude/context.md`
- Use `@workspace analyze` regularly to detect inconsistencies
- Review examples in `examples/` for inspiration

---

## 🙋 FAQ

**Q: Does it work with any type of repository?**  
A: Yes, the skill automatically detects frontend, backend, mobile, DevOps, and shared libraries.

**Q: Do I need to configure all fields in config.json?**  
A: No, only the ones relevant to your project. The skill is flexible.

**Q: Can I use this with repos in different languages?**  
A: Yes, it works with JavaScript, TypeScript, Python, Go, Rust, etc.

---

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [Report problem](https://github.com/yourusername/llm-skills/issues)

---

## 🎉 Acknowledgments

Thanks to the Claude community for feedback and suggestions.

---

**Found this useful? ⭐ Star the repo!**
