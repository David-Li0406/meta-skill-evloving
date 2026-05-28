---
name: marp-slide
description: Use this skill when you need to create professional Marp presentation slides with various themes and best practices for design.
---

# Marp Slide Creator

Create professional, visually appealing Marp presentation slides with 7 pre-designed themes and built-in best practices.

## When to Use This Skill

Use this skill when the user:
- Requests to create presentation slides or Marp documents
- Asks to "make slides look good" or "improve slide design"
- Provides vague instructions like "良い感じにして" (make it nice) or "かっこよく" (make it cool)
- Wants to create lecture or seminar materials
- Needs bullet-point focused slides with occasional images

## Quick Start

### Step 1: Select Theme

First, determine the appropriate theme based on the user's request and content.

**Quick theme selection:**
- **Technical/Developer content** → tech theme
- **Business/Corporate** → business theme
- **Creative/Event** → colorful or gradient theme
- **Academic/Simple** → minimal theme
- **General/Unsure** → default theme
- **Dark background preferred** → dark or tech theme

### Step 2: Create Slides

1. **Read relevant references first**:
   - Start by reading `references/marp-syntax.md` for basic syntax.
   - For images, refer to `references/image-patterns.md` (official Marpit image syntax).
   - For advanced features (math, emoji), check `references/advanced-features.md`.
   - For custom themes, consult `references/theme-css-guide.md`.

2. Copy content from the appropriate template file:
   - `assets/template-basic.md` - Default theme (most common)
   - `assets/template-minimal.md` - Minimal theme
   - `assets/template-colorful.md` - Colorful theme
   - `assets/template-dark.md` - Dark mode theme
   - `assets/template-gradient.md` - Gradient theme
   - `assets/template-tech.md` - Tech/code theme
   - `assets/template-business.md` - Business theme

3. Read `references/best-practices.md` for quality guidelines.

4. Structure content following best practices:
   - Title slide with `<!-- _class: lead -->`
   - Concise h2 titles (5-7 characters in Japanese)
   - 3-5 bullet points per slide
   - Adequate whitespace

5. Add images if needed using patterns from `references/image-patterns.md`.

6. Save the presentation in the desired format.