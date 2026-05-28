# The Soulbook Skill 🌟

**"Write the book your soul came here to write"**

---

## What This Is

The `/soulbook` skill is a guided process that helps you create your personalized **Creator's Soulbook** - a comprehensive life transformation document covering all 7 pillars of your extraordinary life.

---

## Quick Start

```bash
# Start creating your Soulbook
/skill soulbook

# Or if shortcuts are enabled
/soulbook
```

---

## What You'll Get

After completing the guided process (1-3 hours), you'll have:

✅ **7 Detailed Markdown Files** - One for each life pillar
✅ **Complete Life Vision** - Clear 10/10 vision for each area
✅ **Action Plans** - 30-day roadmaps for transformation
✅ **Systems & Habits** - Designs for sustainable change
✅ **Beautiful PDF** - Your complete Soulbook as a stunning document
✅ **Tracking Templates** - For ongoing progress reviews

---

## The Process

### 1. Choose Your Life Book (5 min)
Pick the metaphor that resonates:
- **Life Symphony** 🎵 (for artists)
- **Golden Path** 🛤️ (for seekers)
- **7 Pillars** 🏛️ (for builders)

### 2. Foundation Pillars (30-60 min)
Deep dive on:
- **Energy**: Physical foundation
- **Mind**: Mental & emotional
- **Soul**: Values & purpose

### 3. Growth Pillars (30-60 min)
Design systems for:
- **Craft**: Skills & mastery
- **Capital**: Resources & freedom
- **Circle**: Relationships

### 4. Integration (20-30 min)
- **Legacy**: Vision & impact
- Cross-pillar integration
- 90-day transformation roadmap

### 5. PDF Generation (5 min)
Beautiful formatted document ready to use

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition and overview |
| `soulbook-creator-agent.md` | Detailed agent instructions and process |
| `SETUP.md` | Setup guide and troubleshooting |
| `SOULBOOK_OVERVIEW.md` | Complete framework documentation |
| `README.md` | This file |

---

## Key Features

### Adaptive Language
The agent adapts language based on your Life Book choice:
- Symphony: Musical metaphors
- Golden Path: Journey metaphors
- 7 Pillars: Architectural metaphors

### Flexible Pacing
Choose your session type:
- **Quick Start** (1 hour): Brief, high-level
- **Deep Dive** (2-3 hours): Comprehensive
- **Focus Mode** (30 min/pillar): One at a time

### Auto-Save Progress
If interrupted, your progress is saved. Resume with:
```bash
/skill soulbook --resume
```

### Living Document
Your Soulbook grows with you:
```bash
/skill soulbook --review        # Monthly review
/skill soulbook --pillar energy # Deep dive one area
/skill soulbook --pdf           # Regenerate PDF
```

---

## Setup Required

### For Full PDF Generation (Recommended)

Install pandoc:
```bash
sudo apt update && sudo apt install pandoc texlive-xelatex
```

### Without Pandoc

The skill works fine! It will:
- Create all markdown files
- Skip PDF generation
- Provide online conversion options

---

## Example Session Flow

```
You: /skill soulbook

Agent: Welcome to The Creator's Soulbook! 🌟
       [explains process]
       Which Life Book resonates with you?
       1. Life Symphony 🎵
       2. Golden Path 🛤️
       3. The 7 Pillars 🏛️

You: 3

Agent: Perfect! We'll use architectural language throughout.
       How would you like to create your Soulbook?
       1. Quick Start (1 hour)
       2. Deep Dive (2-3 hours)
       3. Focus Mode (30 min per pillar)

You: 2

Agent: Excellent! Let's begin with deep exploration.

       ═══════════════════════════════════════════
       PILLAR 1: ENERGY
       "The bedrock that powers everything"
       ═══════════════════════════════════════════

       On a scale of 1-10, how satisfied are you
       with your physical energy and health?

[...guided conversation continues through all 7 pillars...]

Agent: 🎉 Your Soulbook is Complete! 🎉

       Files created:
       ✓ soulbook-personal/01-energy.md
       ✓ soulbook-personal/02-mind.md
       [... all 7 pillars ...]
       ✓ soulbook-personal/outputs/MY-SOULBOOK-2026-01-14.pdf

       Your extraordinary life starts now. ✨
```

---

## Use Cases

### Daily Practice
- Morning review: Read one pillar (5 min)
- Evening reflection: Journal using prompts

### Weekly Review
- Update scores for all 7 pillars (15 min)
- Reflect on progress and challenges

### Monthly Deep Dive
- Focus on lowest-scored pillar (30 min)
- Update vision and action plans
- `/skill soulbook --pillar [name]`

### Quarterly Overhaul
- Complete review of all pillars (1-2 hours)
- Regenerate updated PDF
- `/skill soulbook --review`

---

## The 7 Pillars

1. **Energy** - Physical foundation (body, health, vitality)
2. **Mind** - Mental clarity (focus, emotions, learning)
3. **Soul** - Purpose alignment (values, meaning, character)
4. **Craft** - Skills mastery (expertise, output, quality)
5. **Capital** - Resource freedom (money, business, wealth)
6. **Circle** - Relationships (love, friends, community)
7. **Legacy** - Life integration (vision, impact, meaning)

---

## Philosophy

Your Soulbook is:
- **Personal**: Uniquely yours, honest and raw
- **Actionable**: Not just dreams, but systems and plans
- **Living**: Updated regularly as you grow
- **Transformative**: Changes how you see and build your life
- **Complete**: All areas of life, integrated together

---

## Next Steps

1. **Install pandoc** (optional): See SETUP.md
2. **Block time**: Reserve 1-3 hours
3. **Find quiet space**: Deep work environment
4. **Run the skill**: `/skill soulbook`
5. **Be honest**: This is for your eyes only
6. **Complete it**: Even if it takes multiple sessions
7. **Use it daily**: Make it your life operating system

---

## Support & Documentation

- **Setup help**: Read `SETUP.md`
- **Framework details**: Read `SOULBOOK_OVERVIEW.md`
- **Process details**: Read `SKILL.md`
- **Agent behavior**: Read `soulbook-creator-agent.md`

---

## About

Created as part of **The Creator's Soulbook** system by FrankX.

**Mission**: Help creators architect their extraordinary life through AI-guided transformation.

**Website**: [frankx.ai/soulbook](https://frankx.ai/soulbook)

---

*Your soul knows what it came here to create.*
*The Soulbook helps you build it.*
*Start now.* ✨
