---
name: readme-generator
description: Creates or updates README.md files following GitHub best practices with badges, visual hierarchy, and comprehensive documentation. Use when asked to "create a README", "generate documentation", "write a README for this project", or when starting a new project that needs documentation.
argument-hint: "[project-path]"
disable-model-invocation: false
user-invocable: true
metadata:
  version: "1.1.1"
---

# README Generator

Create READMEs that hook readers in 5 seconds, prove value in 30 seconds, and enable success in under 10 minutes.

## Core Framework: Hook → Prove → Enable → Extend

Every README follows this psychological progression:

| Phase | Time | Purpose | Elements |
|-------|------|---------|----------|
| **Hook** | 0-5 sec | Instant recognition | Logo + badges + one-liner + demo visual |
| **Prove** | 5-30 sec | Build credibility | Social proof, features, trust signals |
| **Enable** | 30 sec - 10 min | Immediate success | One-liner install + working example |
| **Extend** | Committed users | Deep engagement | Docs links, contributing, API reference |

**The goal: Time to first success under 10 minutes.**

The first 5-10 lines visible without scrolling determine whether users stay or leave.

## Logo Generation (Mandatory)

Every README must have a logo. Follow this process:

### Step 1: Check for Existing Logo

Look for `logo.png` at the repo root. If found, use it and skip to README generation.

### Step 1.5: Load Configuration (Optional)

Check for logo configuration in order of precedence:
1. `./.claude/readme-generator.json` (project level - highest priority)
2. `~/.claude/readme-generator.json` (user level)

These files customize logo appearance (background color, icon colors, style, model). See **repo-logo-generator** skill for full configuration options.

### Step 2: Generate Logo (if missing)

Invoke the **repo-logo-generator** skill to generate a logo. That skill contains the prompt templates, visual metaphors, and technical requirements for logo generation.

### Step 3: Determine Logo Display Size

For crisp display on retina/high-DPI screens, set the HTML width to **half the actual image width**:

1. Get the image dimensions:
   ```bash
   sips -g pixelWidth logo.png 2>/dev/null | grep pixelWidth | awk '{print $2}'
   ```

2. Divide by 2 for the display width (e.g., 512px image → `width="256"`)

3. Use the calculated width in the HTML img tag

This ensures the logo renders at native resolution on 2x displays while maintaining appropriate size on standard displays.

### Dark/Light Mode Support

For theme-aware logos, use the `<picture>` element:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="logo-light.png">
  <img src="logo-light.png" alt="Project Name" width="{DISPLAY_WIDTH}">
</picture>
```

## Hero Section

The hero section is the most critical part of the README. It must be center-aligned and contain these elements in order:

### Title Rule

**The title must be exactly the same as the repository name.** Preserve the original casing and formatting:
- If the repo is `my-awesome-tool`, the title is `my-awesome-tool` (not "My Awesome Tool")
- If the repo is `fastAPI`, the title is `fastAPI` (not "FastAPI" or "Fastapi")
- If the repo is `README-Generator`, the title is `README-Generator`

Do not "prettify" or transform the repo name. Use it verbatim as the H1 title.

```markdown
<div align="center">
  <img src="logo.png" alt="Project Name" width="{DISPLAY_WIDTH}"/>

  [![Build](badge)](link) [![Version](badge)](link) [![License](badge)](link)

  **A clear, catchy one-liner that explains what this does and why it matters**

  [Documentation](url) · [Demo](url) · [Discord](url)
</div>
```

### Hero Element Requirements

| Element | Specification |
|---------|---------------|
| Logo | Width = half actual pixels (for retina), centered |
| Badges | 3-6 maximum, shields.io for consistency |
| Tagline | One sentence with emoji(s), max 350 chars (fits GitHub "About" field) |
| Quick links | Docs, demo, community (if available) |

### Tagline Patterns That Work

**Rules:**
- **Must include emoji(s)** - 1-3 relevant emojis that reinforce the message
- **Max 350 characters** - fits GitHub's "About → Description" field
- **Ideal length: 80-150 chars** - punchy and scannable

Good taglines lead with benefits, not features:

- ✅ "🔧 Magnificent app which corrects your previous console command"
- ✅ "⚡ High-performance, easy to learn, fast to code, ready for production"
- ✅ "🚀 A blazing fast CLI for X"
- ✅ "🛠️ Build, test, and deploy with zero config"
- ❌ "A Python library for doing Y" (no emoji, too generic)
- ❌ "Version 2.0 of the Z project" (no emoji, self-focused)

### GIF Demo Placement

For CLI tools, place an animated GIF demo **immediately after the tagline**. This is the single most distinctive pattern across successful CLI projects (thefuck, lazygit, fzf, bat).

## Badges

Use 4-7 badges in this priority order:

1. **Build/CI status** - project health
2. **Code coverage** - quality signal
3. **Version/release** - active development
4. **License** - legal clarity
5. **Downloads** - adoption proof
6. **Discord/community** - engagement signal

### Badge Implementation

```markdown
[![Build](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml?branch=main)](link)
[![Coverage](https://img.shields.io/codecov/c/github/user/repo)](link)
[![PyPI](https://img.shields.io/pypi/v/package-name)](link)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](link)
[![Downloads](https://img.shields.io/pypi/dm/package-name)](link)
[![Discord](https://img.shields.io/discord/SERVER_ID)](link)
```

**Rules:**
- Use shields.io for all badges (consistent styling)
- Pick one style (flat, flat-square, for-the-badge) and use it consistently
- For CLI tools, include a Repology badge showing packaging status

## Visual Elements

### GIF Demos (Mandatory for CLI Tools)

Terminal recordings are mandatory for CLI tools. Use:
- **vhs** - scripted terminal GIFs (recommended)
- **terminalizer** - interactive recording
- **asciinema** - terminal session sharing

**GIF Requirements:**
- Under 10MB (GitHub limit)
- 10-15fps is sufficient
- Show the "aha moment" - core value in action
- Drag-drop into README editor to host on GitHub's CDN

### Screenshots

For UI-heavy projects:
- Include both light and dark mode versions
- Compress before adding (ImageOptim, XConvert)
- Use descriptive alt text

### Tables

Use tables for:
- Feature comparisons
- API parameters
- Benchmark results
- Installation matrices (cross-platform)

### Architecture Diagrams

For complex projects, use Mermaid (GitHub-native):

```markdown
```mermaid
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
```
```

## Writing Style

### Voice and Tone

- **Active voice, imperative mood**: "Install the package" not "The package can be installed"
- **Second person**: "You can configure..." not "Users can configure..."
- **Present tense**: "This library handles..." feels immediate
- **Contractions**: "don't," "it's," "you'll" create conversational tone

### Structure

- Maximum 3-5 lines per paragraph
- One concept per paragraph
- 80-character line width for readability

### Emoji Strategy

Strategic emojis boost engagement:

| Location | Examples | Purpose |
|----------|----------|---------|
| Section headers | 🚀 Quick Start, ⚙️ Config, 📦 Install | Visual navigation |
| Feature bullets | ✨ New, ⚡ Fast, 🔒 Secure | Scannable benefits |
| Status indicators | ✅ Done, ⏳ WIP, ❌ Deprecated | Quick comprehension |
| CTAs | ⭐ Star us!, 🤝 Contribute | Engagement boost |

**Rules**: 1-2 per section max. Never in code blocks. Consistent style throughout.

### Anti-Pattern

Focus on user benefits, not project history or developer achievements. The README is for users, not a changelog.

## Engagement Boosters

### Humor That Works

Subtle, inclusive humor increases engagement:
- **Self-aware**: "Yes, another X. But hear us out..."
- **Relatable pain**: "We got tired of Y, so we built this"
- **Easter eggs**: Hidden features for curious readers

Avoid: Dated memes, inside jokes, anything requiring context.

## README by Project Type

### Standard Sections (All Projects)

```markdown
## Overview
Brief explanation of purpose and value proposition.

## Features
- Feature 1 with benefit
- Feature 2 with benefit
- Feature 3 with benefit

## Quick Start
```bash
pip install mypackage
```

```python
from mypackage import Feature
result = Feature().run("input")
print(result)  # Output: "Success"
```

## Installation
Detailed installation for different platforms/methods.

## Usage
Comprehensive examples with code snippets.

## Contributing
How to contribute to the project.

## License
License information and link.
```

### AI/ML Projects

Include these additional sections:

**Model Card (YAML header):**
```yaml
---
language: en
license: mit
library_name: transformers
tags: [text-classification, bert]
datasets: [imdb]
metrics: [accuracy, f1]
base_model: bert-base-uncased
---
```

**Hardware Requirements:**
```markdown
## Requirements
- **GPU**: NVIDIA with CUDA support (8GB+ VRAM)
- **CUDA**: 11.7+
- **RAM**: 16GB+ recommended
```

**Benchmark Table:**

| Model | Dataset | Accuracy | GPU | Training Time |
|-------|---------|----------|-----|---------------|
| Base | SQuAD 2.0 | 83.1% | V100 | 2h 15m |
| Large | SQuAD 2.0 | 87.4% | A100 | 4h 30m |

Include random seeds, batch sizes, and hardware for reproducibility.

**Demo Links:**
```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](link)
[![Hugging Face](https://img.shields.io/badge/🤗-Demo-yellow)](link)
```

**Required Ethical Sections:**
- Bias, risks, and limitations
- Out-of-scope uses
- Environmental impact
- Data privacy considerations

**Citation:**
```bibtex
@article{author2024model,
  title={Model Name},
  author={Author, A.},
  year={2024}
}
```

### CLI Tools

**Shell Integration:**
```bash
# Bash
eval "$(myapp init bash)"

# Zsh
eval "$(myapp init zsh)"

# Fish
myapp init fish | source
```

**Cross-Platform Installation Matrix:**

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install myapp` |
| Linux (apt) | `sudo apt install myapp` |
| Windows (Scoop) | `scoop install myapp` |
| From source | `cargo install myapp` |

**Performance Benchmarks:**

| Tool | Time | Relative |
|------|------|----------|
| myapp | 0.082s | 1.00x |
| alternative1 | 0.273s | 3.34x |
| alternative2 | 0.443s | 5.43x |

Specify exact hardware, scenarios, and equivalent flags for fair comparison.

**Keybinding Reference:**

| Key | Action |
|-----|--------|
| `space` | Stage selected line |
| `CTRL-R` | Search history |

**Configuration Example:**
```toml
# ~/.config/myapp/config
--theme="TwoDark"
--style="numbers,changes,header"
```

### Libraries

**API Reference Table:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `process()` | `data: str` | `Result` | Process input data |
| `configure()` | `options: dict` | `None` | Set configuration |

**Quick Example:**
```python
from mylib import Thing

thing = Thing()
result = thing.process(data)
```

### Web Apps

**Live Demo Link** prominently placed after hero section.

**Environment Variables Table:**

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Database connection string |
| `API_KEY` | Yes | External API key |

**Docker Quick Start:**
```bash
docker run -p 3000:3000 myapp
```

## Social Proof

### "Used By" Section

Place prominently after hero section with 6-12 company logos:

```markdown
## Used By

<p align="center">
  <img src="logos/company1.svg" alt="Company 1" height="40">
  &nbsp;&nbsp;&nbsp;
  <img src="logos/company2.svg" alt="Company 2" height="40">
</p>
```

### Star CTA

Engaging call-to-action patterns:
- `⭐ Star if this saved you hours of debugging!`
- `🌟 If this helped, a star would make our day!`

**Rules**: One CTA max. Humor optional but never cringe. Self-deprecation > bragging.

### Community Links

```markdown
[![Discord](https://img.shields.io/discord/SERVER_ID?label=Discord&logo=discord)](link)
[![Twitter](https://img.shields.io/twitter/follow/handle?style=social)](link)
```

### Supporting Files

These files signal project maturity:
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md
- LICENSE

## Anti-Patterns

Avoid these mistakes:

| Anti-Pattern | Problem |
|--------------|---------|
| No README or empty README | Single worst error |
| Wall of text | No structure, long paragraphs |
| Missing install instructions | Users immediately lost |
| Scary build instructions upfront | `git clone; cmake...` scares users |
| No visual demonstration | Text-only descriptions of visual software |
| Outdated information | Erodes trust |
| API-dump documentation | README shouldn't be complete API reference |
| Redundant information | Repeating title (already in URL) |
| Inconsistent formatting | Mixed badge styles, varying headers |
| Self-focused writing | Developer achievements over user benefits |
| Emoji overload 🎉🚀✨💯🔥 | Visual noise, unprofessional |

## Workflow

1. **Analyze project** - scan for package.json, Cargo.toml, pyproject.toml, go.mod, etc.
2. **Detect project type** - CLI, library, AI/ML, web app, API
3. **Extract metadata** - name, description, version, author, license
4. **Check for existing logo** - look for `logo.png` at repo root
5. **Generate logo if missing** - use repo-logo-generator skill
6. **Calculate display width** - use half the actual image pixel width (for retina displays)
7. **Generate README.md** - following Hook → Prove → Enable → Extend structure

## Quick Reference Checklist

### Essential (Must Include)

- [ ] Project logo (width = half actual pixels, centered)
- [ ] 4-7 relevant badges
- [ ] One-liner description ("What and why?")
- [ ] GIF/screenshot demonstration
- [ ] One-liner installation command
- [ ] Minimal working code example
- [ ] License information

### Professional Tier

- [ ] Table of contents (if >500 words)
- [ ] Feature highlights with benefits
- [ ] Multiple installation methods
- [ ] Documentation links
- [ ] Contributing section
- [ ] "Used by" company logos

### Elite Tier

- [ ] Dark/light mode image support
- [ ] Architecture diagram
- [ ] Benchmark comparisons
- [ ] FAQ section
- [ ] Star history graph
- [ ] Contributor avatars

### AI/ML Specific

- [ ] Model card with YAML metadata
- [ ] Hardware requirements table
- [ ] Benchmark results with reproducibility
- [ ] Colab/demo links
- [ ] Training vs. inference split
- [ ] Ethical considerations
- [ ] Citation in BibTeX format

### CLI Specific

- [ ] Terminal GIF demo
- [ ] Cross-platform installation matrix
- [ ] Shell integration instructions
- [ ] Configuration file examples
- [ ] Keybinding reference table
- [ ] Performance benchmarks
