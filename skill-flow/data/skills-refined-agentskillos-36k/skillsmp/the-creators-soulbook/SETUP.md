# Soulbook Skill Setup Guide

## ✅ What's Been Set Up

Your `/soulbook` skill is now fully configured and ready to use! Here's what was created:

1. **Main Skill Definition** (`SKILL.md`)
   - Complete process overview
   - Session structure
   - File templates
   - Usage instructions

2. **Soulbook Creator Agent** (`soulbook-creator-agent.md`)
   - Detailed agent personality and behavior
   - 5-phase creation process
   - Question templates for each pillar
   - Markdown file templates

3. **Existing Framework**
   - 3 Life Books (Life Symphony, Golden Path, 7 Pillars)
   - 7 Pillars detailed content
   - AI coaching agents
   - Complete documentation

---

## 🚀 Quick Start

To use your Soulbook skill:

```bash
/skill soulbook
```

Or if Claude Code supports shortcuts:

```bash
/soulbook
```

---

## 📋 PDF Generation Setup (Optional but Recommended)

To generate beautiful PDFs from your Soulbook markdown files, you need `pandoc`.

### Install Pandoc on WSL/Linux

```bash
# Update package list
sudo apt update

# Install pandoc (basic)
sudo apt install pandoc

# Install full LaTeX support for better PDFs (optional, ~500MB)
sudo apt install texlive-xelatex texlive-fonts-recommended texlive-fonts-extra
```

### Verify Installation

```bash
pandoc --version
```

### Alternative: Node.js markdown-pdf

If you prefer a lighter option:

```bash
npm install -g markdown-pdf
```

### Without Installation

The skill will still work without pandoc! It will:
1. Create all markdown files
2. Skip PDF generation
3. Provide instructions to generate PDF manually online

**Online PDF converters:**
- https://www.markdowntopdf.com/
- https://dillinger.io/ (with export)
- https://cloudconvert.com/md-to-pdf

---

## 📁 What Gets Created

When you complete the Soulbook process, you'll have:

```
soulbook-personal/
├── _meta.md                      # Session metadata and progress
├── 00-introduction.md            # Your personal introduction
├── 01-energy.md                  # Physical foundation pillar
├── 02-mind.md                    # Mental & emotional pillar
├── 03-soul.md                    # Values & purpose pillar
├── 04-craft.md                   # Skills & mastery pillar
├── 05-capital.md                 # Resources & freedom pillar
├── 06-circle.md                  # Relationships pillar
├── 07-legacy.md                  # Vision & impact pillar
├── 08-integration.md             # Integration & roadmap
└── outputs/
    └── MY-SOULBOOK-2026-01-14.pdf  # Your final PDF
```

Each file contains:
- Current state assessment
- Future vision
- Systems and habits
- 30-day action plan
- Progress tracking
- Reflection prompts

---

## 🎯 Session Types

Choose your creation approach:

### Quick Start (1 hour)
- Brief questions for each pillar
- High-level vision setting
- Basic action plans
- Good for: First-time users, getting overview

### Deep Dive (2-3 hours)
- Comprehensive exploration
- Detailed vision work
- Full system design
- Good for: Serious transformation, complete clarity

### Focus Mode (30 min per pillar)
- One pillar per session
- Deep work on single area
- Can be done over days/weeks
- Good for: Busy schedules, gradual building

---

## 💡 How It Works

1. **Invocation**: You type `/skill soulbook` (or `/soulbook`)

2. **Agent Activation**: Claude becomes the Soulbook Creator Agent

3. **Guided Process**:
   - Welcome and Life Book selection
   - Session preference
   - 7 pillars exploration (one by one)
   - File creation as you go
   - Integration and PDF generation

4. **Output**: Complete Soulbook with markdown + PDF

---

## 🔄 Continuing Your Journey

After initial creation:

```bash
# Monthly review
/skill soulbook --review

# Deep dive single pillar
/skill soulbook --pillar energy

# Resume interrupted session
/skill soulbook --resume

# Regenerate PDF only
/skill soulbook --pdf
```

---

## 🌟 The Three Life Books

Choose the metaphor that resonates with you:

### Life Symphony 🎵
**For**: Artists, musicians, creative souls
**Metaphor**: Musical composition
**Language**: Rhythms, melodies, harmonies
**Pillars become**: 7 Movements

### Golden Path 🛤️
**For**: Seekers, visionaries, spiritual explorers
**Metaphor**: Hero's journey
**Language**: Waypoints, paths, destinations
**Pillars become**: 7 Waypoints

### The 7 Pillars 🏛️
**For**: Builders, architects, systems thinkers
**Metaphor**: Construction and architecture
**Language**: Foundations, structures, building
**Pillars stay**: 7 Pillars

---

## 📖 The 7 Pillars

```
                ╔═══════════════════════════════════════╗
                ║         PILLAR 7: LEGACY              ║
                ║    Vision • Purpose • Impact          ║
                ╚═══════════════════╤═══════════════════╝
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
╔════════╧════════╗        ╔════════╧════════╗        ╔════════╧════════╗
║ PILLAR 4: CRAFT ║        ║PILLAR 5: CAPITAL║        ║PILLAR 6: CIRCLE ║
║                 ║        ║                 ║        ║                 ║
║ Skills          ║        ║ Money           ║        ║ Relationships   ║
║ Mastery         ║        ║ Business        ║        ║ Community       ║
╚════════╤════════╝        ╚════════╤════════╝        ╚════════╤════════╝
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
╔════════════════════════════════════╧════════════════════════════════════╗
║                        FOUNDATION PILLARS                               ║
╠══════════════════╦═══════════════════════╦══════════════════════════════╣
║ PILLAR 1: ENERGY ║   PILLAR 2: MIND      ║      PILLAR 3: SOUL          ║
║                  ║                       ║                              ║
║ Body             ║   Intellect           ║      Values                  ║
║ Health           ║   Emotions            ║      Purpose                 ║
║ Vitality         ║   Focus               ║      Character               ║
╚══════════════════╩═══════════════════════╩══════════════════════════════╝
```

---

## 🎓 Tips for Success

1. **Block Time**: Reserve 1-3 hours (or do Focus Mode)
2. **Be Honest**: This is for you - radical honesty creates transformation
3. **Go Deep**: Don't rush - the insights come from reflection
4. **Take Breaks**: It's okay to pause and resume
5. **Use It Daily**: Your Soulbook is a living document
6. **Review Regularly**: Monthly reviews keep you aligned
7. **Update Often**: As you grow, update your vision

---

## ❓ Troubleshooting

### Skill not found?
Make sure you're in the FrankX directory and using:
```bash
/skill soulbook
```

### PDF generation fails?
- Check pandoc installation: `pandoc --version`
- Use online converter as fallback
- Markdown files are still created and usable

### Want to restart?
- Delete or rename `soulbook-personal/` directory
- Run `/skill soulbook` again

### Session interrupted?
- Your progress is auto-saved in `_meta.md`
- Run `/skill soulbook --resume` to continue

---

## 📞 Support

Questions about:
- **The Framework**: Read `SOULBOOK_OVERVIEW.md`
- **The Process**: Read `SKILL.md`
- **Agent Behavior**: Read `soulbook-creator-agent.md`
- **Using Files**: Each pillar has detailed instructions

---

## 🚀 Ready to Begin?

Your extraordinary life is waiting to be architected.

When you're ready, simply type:

```bash
/skill soulbook
```

And the journey begins. 🌟

---

*"Write the book your soul came here to write."*
