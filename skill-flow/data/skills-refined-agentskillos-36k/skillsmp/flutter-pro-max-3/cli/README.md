# 🚀 Flutter Pro Max CLI

**The official command-line interface for deploying Flutter Pro Max technical intelligence to your favorite AI coding assistants.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📦 Installation

### The Quick Way (Recommended)
Bootstrap any project in seconds. This command will guide you through selecting and installing the skill for your environment.

```bash
npx flutter-pro-max-cli
```

### Global Installation
For heavy users who want the `flutter-pro-max` command available everywhere:

```bash
# Install globally
npm install -g flutter-pro-max-cli

# Initialize in your project
flutter-pro-max init
```

---

## 🛠️ Usage

### Interactive Setup
Simply run the command and follow the prompts to detect and install the skill for your active AI assistants.

```bash
flutter-pro-max init
```

### Scripted Installation
For CI/CD or automated setups, you can specify the assistant type directly:

```bash
# Install for a specific assistant
flutter-pro-max init --ai claude
flutter-pro-max init --ai cursor
flutter-pro-max init --ai antigravity

# Install for all supported assistants
flutter-pro-max init --ai all
```

### Other Commands

```bash
# List available versions from GitHub releases
flutter-pro-max versions

# Update to the latest version
flutter-pro-max update
flutter-pro-max update --ai claude
```

---

## 🤖 Supported AI Assistants

This CLI bridges the gap between the Flutter Pro Max knowledge base and your development tools:

| Assistant | Type Flag | Install Type | Structure |
|-----------|-----------|--------------|-----------|
| **Claude Code** | `claude` | Full | `.claude/skills/flutter-pro-max/` |
| **Codex CLI** | `codex` | Full | `.codex/skills/flutter-pro-max/` |
| **Continue** | `continue` | Full | `.continue/skills/flutter-pro-max/` |
| **Antigravity** | `antigravity` | Full | `.agent/skills/flutter-pro-max/` |
| **Cursor** | `cursor` | Reference | `.cursor/commands/` + `.shared/` |
| **Windsurf** | `windsurf` | Reference | `.windsurf/workflows/` + `.shared/` |
| **GitHub Copilot** | `copilot` | Reference | `.github/prompts/` + `.shared/` |
| **Kiro** | `kiro` | Reference | `.kiro/skills/` + `.shared/` |
| **RooCode** | `roocode` | Reference | `.roo/commands/` + `.shared/` |
| **Qodo/Qoder** | `qoder` | Reference | `.qodo/skills/` + `.shared/` |
| **Gemini CLI** | `gemini` | Reference | `.gemini/skills/` + `.shared/` |
| **Trae** | `trae` | Reference | `.trae/skills/` + `.shared/` |
| **CodeBuddy** | `codebuddy` | Reference | `.codebuddy/skills/` + `.shared/` |
| **OpenCode** | `opencode` | Reference | `.opencode/skills/` + `.shared/` |

**Install Types:**
- **Full**: Data và scripts nằm trong skill folder (standalone, ~500KB)
- **Reference**: Skill file trỏ đến `.shared/` folder chung (tiết kiệm dung lượng khi dùng nhiều assistants)

---

## 📊 What Gets Installed

### Data Files (17 domains)
| Domain | File | Description |
|--------|------|-------------|
| Widgets | `widget.csv` | 65+ Flutter widgets |
| Packages | `package.csv` | 100+ packages với alternatives |
| Patterns | `patterns.csv` | 110+ design patterns |
| Architecture | `architect.csv` | Architecture layers |
| Performance | `flutter-performance.csv` | 35 optimization patterns |
| Accessibility | `mobile-accessibility.csv` | 35 accessibility patterns |
| UI Reasoning | `ui-reasoning.csv` | 35 app category decisions |
| Colors | `colors.csv` | 50+ color palettes |
| Typography | `typography.csv` | 40+ font pairings |
| Styles | `styles.csv` | 60+ UI styles |
| UX | `ux-guidelines.csv` | 50+ UX rules |
| Icons | `icons.csv` | 100+ icon recommendations |
| Landing | `landing.csv` | 30+ landing patterns |
| Products | `products.csv` | 40+ product recommendations |
| Prompts | `prompts.csv` | 30+ AI prompts |
| Charts | `charts.csv` | 20+ chart types |
| Naming | `name_convention.csv` | Naming conventions |

### Search Scripts
- `search.py` - BM25 search CLI
- `core.py` - Search engine core

---

## 🔧 Development

If you want to contribute or modify the CLI:

```bash
# Clone and install
git clone https://github.com/btLong402/flutter-skill.git
cd cli
npm install

# Build the project
npm run build

# Run locally
node dist/index.js init --ai claude

# Test search
node dist/index.js init --ai claude
cd .claude/skills/flutter-pro-max
python3 scripts/search.py "ListView" --domain widget --top 3
```

---

## 📁 Project Structure

```
cli/
├── src/
│   ├── index.ts              # CLI entry point
│   ├── commands/
│   │   ├── init.ts           # Install command
│   │   ├── versions.ts       # List versions
│   │   └── update.ts         # Update command
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   └── utils/
│       ├── detect.ts         # AI type detection
│       ├── github.ts         # GitHub API client
│       ├── logger.ts         # Console logger
│       └── template.ts       # Template renderer
├── assets/
│   ├── data/                 # 17 CSV knowledge files
│   ├── scripts/              # Python search scripts
│   └── templates/
│       ├── base/             # Markdown templates
│       └── platforms/        # 14 platform JSON configs
├── package.json
└── tsconfig.json
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

### v2.1.0 (2026-01-27)
- **Type Safety**: Full Python type hints cho Pylance strict mode
- **Python 3.10+**: Minimum Python version updated
- **Code Quality**: Xóa unused imports, fix linter warnings

### v2.0.0
- Phiên bản đầu tiên với 14 AI assistant support

---

<div align="center">

**Streamline your Flutter development with AI-powered architectural intelligence.**

</div>
