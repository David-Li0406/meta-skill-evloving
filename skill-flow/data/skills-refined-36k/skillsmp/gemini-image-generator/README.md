<div align="center">

# Gemini Image Generator

**Claude Code Skill for generating images using Google Gemini (Imagen 3)**

[English](README.md) | [日本語](README.ja.md)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://www.anthropic.com/news/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Generate high-quality AI images directly from Claude Code using Google Gemini's Imagen 3 model through browser automation. One-time Google login, then generate images with simple prompts.

[Installation](#installation) • [Quick Start](#quick-start) • [Usage](#usage) • [How It Works](#how-it-works)

</div>

---

## Features

- **Imagen 3 Image Generation** - Access Google's latest image generation model
- **Persistent Authentication** - Login once, works until cookies expire (~7 days)
- **Automatic Environment Setup** - Virtual environment and dependencies managed automatically
- **Browser Automation** - Based on proven [NotebookLM skill](https://github.com/PleasePrompto/notebooklm-skill) patterns
- **Human-like Interactions** - Anti-detection features for reliable operation

---

## Important: Local Claude Code Only

**This skill works ONLY with local [Claude Code](https://github.com/anthropics/claude-code) installations, NOT in the web UI.**

The web UI runs skills in a sandbox without network access, which this skill requires for browser automation.

---

## Installation

### Option 1: Install to User Skills Directory (Recommended)

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills

# Clone this repository
cd ~/.claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator
```

### Option 2: Install to Project Skills Directory

```bash
# In your project root
mkdir -p .claude/skills

# Clone this repository
cd .claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator
```

### Verify Installation

In Claude Code, say:
```
"What skills do I have?"
```

Claude will list your available skills including Gemini Image Generator.

---

## Quick Start

### 1. Authenticate with Google (One-Time)

```
"Set up Gemini authentication"
```

A Chrome window opens → Log in to your Google account → Authentication is saved.

### 2. Generate Images

```
"Generate an image of a sunset over mountains"
```

Or with specific output:
```
"Generate an image of a futuristic robot and save it to robot.png"
```

---

## Usage

### Check Authentication Status

```bash
python scripts/run.py auth_manager.py status
```

Output:
```
✓ Authenticated
  Session age: 2.5 hours
  Total cookies: 51
  Google auth cookies: 27
```

### Authenticate (If Needed)

```bash
python scripts/run.py auth_manager.py setup
```

### Generate Images

```bash
# Basic generation
python scripts/run.py image_generator.py --prompt "a cute cat sitting on a windowsill"

# Specify output path
python scripts/run.py image_generator.py --prompt "cyberpunk city at night" --output images/city.png

# Show browser (for debugging)
python scripts/run.py image_generator.py --prompt "..." --show-browser

# Custom timeout
python scripts/run.py image_generator.py --prompt "..." --timeout 300
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--prompt` | Yes | - | Image generation prompt |
| `--output` | No | `output/generated_image.png` | Output file path |
| `--show-browser` | No | False | Show browser window |
| `--timeout` | No | 180 | Max wait time in seconds |

---

## How It Works

### Authentication Flow

1. Opens `accounts.google.com` for Google login
2. Waits for successful login (redirect to `myaccount.google.com`)
3. Navigates to Gemini and captures all cookies
4. Saves 51 cookies including 27 Google auth cookies to `state.json`
5. Subsequent runs inject cookies automatically

### Image Generation Flow

1. Opens Gemini (`gemini.google.com`)
2. Clicks **"ツール" (Tools)** button
3. Selects **"画像を作成" (Create Image)** option
4. Enters prompt and clicks send
5. Waits for Imagen 3 to generate the image
6. Downloads and saves the image

### Architecture

```
NanobananaPro-skill/
├── SKILL.md              # Instructions for Claude Code
├── README.md             # This file
├── LICENSE               # MIT License
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── run.py            # Wrapper script (auto-manages venv)
│   ├── config.py         # Centralized settings
│   ├── browser_utils.py  # Browser factory and stealth utilities
│   ├── auth_manager.py   # Google authentication management
│   └── image_generator.py # Image generation logic
├── data/                 # Auth data (auto-created, gitignored)
└── output/               # Generated images (gitignored)
```

---

## Prompt Guidelines

### Good Prompts

```
"A serene sunset over snow-capped mountains with warm orange sky"
"Watercolor painting of a cat sitting by a window, soft lighting"
"Professional product photography of a laptop on a clean white desk"
"Cyberpunk cityscape at night with neon lights and rain"
```

### Avoid

- Vague prompts: "something nice"
- Inappropriate content (Gemini will refuse)
- Copyrighted characters or trademarked content

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Not authenticated" | Run `auth_manager.py setup` |
| ModuleNotFoundError | Always use `run.py` wrapper |
| Timeout | Increase with `--timeout 300` |
| "Could not find tool button" | UI may have changed, try `--show-browser` |
| Generation refused | Modify prompt (avoid restricted content) |

### Clear and Restart

```bash
python scripts/run.py auth_manager.py clear
python scripts/run.py auth_manager.py setup
```

---

## Using in Other Projects

### Method 1: Symlink (Recommended)

```bash
# Install once to user directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator

# In other projects, create symlink
cd /path/to/your/project
mkdir -p .claude/skills
ln -s ~/.claude/skills/gemini-image-generator .claude/skills/
```

### Method 2: Git Submodule

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git submodule add https://github.com/RenTonoduka/NanobananaPro-skill.git .claude/skills/gemini-image-generator
```

### Method 3: Direct Clone

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git .claude/skills/gemini-image-generator
```

---

## Limitations

- **Generation time:** 30-180 seconds per image
- **Browser automation:** May break if Gemini UI changes
- **Authentication:** Manual Google login required initially
- **Content policy:** Gemini may refuse certain prompts
- **Rate limits:** Subject to Google account limits
- **No batch processing:** One image per command
- **Local only:** Does not work in Claude Code web UI

---

## Security Notes

- Authentication data stored locally in `data/` directory
- All sensitive files excluded from git via `.gitignore`
- Uses real Chrome browser for better Google trust
- Never commit `data/` directory contents

---

## Credits

Based on the authentication patterns from [NotebookLM Skill](https://github.com/PleasePrompto/notebooklm-skill).

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

<div align="center">

**Generate images with AI directly in Claude Code**

[Report Issue](https://github.com/RenTonoduka/NanobananaPro-skill/issues) • [Request Feature](https://github.com/RenTonoduka/NanobananaPro-skill/issues)

</div>
