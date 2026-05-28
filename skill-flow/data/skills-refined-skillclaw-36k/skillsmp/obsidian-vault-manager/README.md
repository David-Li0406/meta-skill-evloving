# Obsidian Vault Manager Plugin

Manage an AI-powered Obsidian knowledge base with automatic organization and GitHub Pages publishing.

## Features

- **YouTube Video Capture**: Fetch transcripts and create comprehensive notes (`/youtube-note`)
- **Smart AI Tagging**: Automatic tagging based on content analysis (`/capture`, `/idea`)
- **Bundled Scripts**: Executable scripts for transcript fetching and publishing
- **Template System**: Consistent note structure across all content types
- **GitHub Pages Publishing**: Publish notes to your public sharehub (`/publish`)
- **URL-Based Sharing**: Share notes via URL with no server storage (`/share`) - Plannotator-compatible

## Installation

### Claude Code CLI (Recommended)

1. **Add the plugin marketplace**:
```bash
/plugin marketplace add ZorroCheng-MC/obsidian-vault-manager-plugin
```

2. **Install the plugin**:
```bash
# Option A: Browse available plugins
/plugin

# Option B: Install directly
/plugin install obsidian-vault-manager@ZorroCheng-MC/obsidian-vault-manager-plugin
```

3. **Verify installation**:
```bash
/plugin list
# Should show: obsidian-vault-manager
```

### Manual Installation (Legacy)

For development or when marketplace is unavailable:

```bash
# Clone to Claude plugins directory
mkdir -p ~/.claude/plugins
cd ~/.claude/plugins
git clone https://github.com/ZorroCheng-MC/obsidian-vault-manager-plugin.git obsidian-vault-manager

# Make scripts executable
chmod +x ~/.claude/plugins/obsidian-vault-manager/scripts/core/*.sh
```

## Bundled Resources

### Scripts

**Core Scripts (`scripts/core/`)**:
- `fetch-youtube-transcript.sh` - Fetches YouTube transcripts using youtube_transcript_api

**Validation Scripts (`scripts/validation/`)**:
- `validate-frontmatter.py` - Validates note frontmatter structure

### Templates

**`templates/youtube-note-template.md`** - Structured template for YouTube video notes with:
- Comprehensive frontmatter
- Learning objectives
- Curriculum structure
- Key takeaways sections
- Rating and tags analysis

## Usage

### In Claude Code CLI

```bash
# Capture YouTube video
/youtube-note https://youtu.be/VIDEO_ID

# Capture quick idea
/idea My brilliant idea about AI agents

# Publish to GitHub Pages
/publish my-note.md

# Share via URL (no server storage)
/share my-note.md
```

### Share Command Details

The `/share` command creates a shareable URL with the note content encoded directly in the URL (Plannotator-style):

```
https://zorrocheng-mc.github.io/sharehub/share.html#<compressed-base64>
```

**Features:**
- No server storage - content lives in the URL
- Recipients can add comments/annotations
- Comments generate new URLs for sharing back
- Compatible with Plannotator format

**Limitations:**
- Large notes (>10KB) create very long URLs
- For large content, use `/publish` instead

### In Claude Desktop

Simply provide a YouTube URL:
```
Create a note from this video: https://youtu.be/VIDEO_ID
```

## Optional: Automatic Validation Hooks

For advanced users who want automatic frontmatter validation before note creation, you can configure hooks in your Claude Code settings.

### Hook Setup

Add the following to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "description": "Validate frontmatter before creating Obsidian notes",
        "matcher": "mcp__obsidian-mcp-tools__create_vault_file",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/obsidian-vault-manager/scripts/validation/validate-frontmatter.py"
          }
        ]
      }
    ]
  }
}
```

### What Hooks Do

When configured, the validation hook will:
- ✅ Run automatically before every note creation
- ✅ Check for required frontmatter fields (title, tags, date, type)
- ✅ Validate tag structure (must be a list)
- ✅ Verify content type tag is present (video, article, idea, etc.)
- ✅ Warn if 'inbox' tag is missing
- ❌ Block creation if validation fails

### Hook Behavior

**Exit Codes**:
- `0` - Validation passed, allow creation
- `1` - Warning only, allow creation with message
- `2` - Validation failed, block creation

**Without Hooks**: Claude runs validation script as part of SKILL.md workflow (default behavior)

**With Hooks**: Automatic enforcement before any Obsidian note creation (opt-in)

## Testing Scripts

### Test Transcript Fetching

```bash
# Test with a video ID
~/.claude/skills/obsidian-vault-manager/scripts/core/fetch-youtube-transcript.sh jI2LC3WTryw
```

### Test Validation

```bash
# Create a test file
cat > test-note.md << 'EOF'
---
title: "Test Video"
tags: [video, AI, inbox]
date: 2025-10-28
type: video
---
# Test
EOF

# Validate it
python3 ~/.claude/skills/obsidian-vault-manager/scripts/validation/validate-frontmatter.py test-note.md
```

## Tag Taxonomy

### Content Type Tags (choose 1)
- `idea`, `video`, `article`, `study-guide`, `repository`, `reference`, `project`

### Topic Tags (choose 2-4)
- `AI`, `productivity`, `knowledge-management`, `development`, `learning`, `research`, `writing`, `tools`, `business`, `design`, `automation`, `data-science`, `web-development`, `personal-growth`, `finance`

### Status Tags (choose 1)
- `inbox`, `processing`, `evergreen`, `published`, `archived`, `needs-review`

### Metadata Tags (choose 0-2)
- `high-priority`, `quick-read`, `deep-dive`, `technical`, `conceptual`, `actionable`, `tutorial`, `inspiration`

**Total tags**: 6-8 for optimal filtering

## Troubleshooting

### Script Permission Errors

Make scripts executable:
```bash
chmod +x ~/.claude/skills/obsidian-vault-manager/scripts/core/*.sh
chmod +x ~/.claude/skills/obsidian-vault-manager/scripts/validation/*.py
```

### Transcript Fetching Fails

Ensure `uvx` and `youtube_transcript_api` are available:
```bash
uvx youtube_transcript_api --help
```

### Validation Errors

Check Python dependencies:
```bash
python3 -c "import yaml; print('PyYAML installed')"
```

If missing:
```bash
pip3 install pyyaml
```

## Structure

```
~/.claude/skills/obsidian-vault-manager/
├── SKILL.md                    # Main skill file with instructions
├── README.md                   # This file
├── scripts/
│   ├── core/
│   │   ├── fetch-youtube-transcript.sh
│   │   └── publish.sh
│   └── validation/
│       └── validate-frontmatter.py
└── templates/
    ├── youtube-note-template.md
    ├── idea-template.md
    └── study-guide-template.md

# Commands (in plugin root)
commands/
├── share.md                    # URL-based sharing (Plannotator-compatible)
├── publish.md                  # GitHub Pages publishing
├── youtube-note.md             # YouTube video capture
├── idea.md                     # Quick idea capture
└── ...

# Related: ShareHub decoder page
~/Dev/sharehub/share.html       # URL decoder for /share command
```

## Version

- **Version**: 1.0.0 (Post-Migration)
- **Migration Date**: 2025-10-28
- **Architecture**: Skill-primary with bundled scripts

## License

This skill is provided for personal use. Modify and distribute as needed.

## Support

For issues or questions:
1. Check this README
2. Verify script permissions
3. Test scripts individually
4. Review SKILL.md for workflow details

---

**Note**: Hooks are optional. The skill works without hook configuration - Claude will run validation scripts as part of the workflow instructions in SKILL.md.
