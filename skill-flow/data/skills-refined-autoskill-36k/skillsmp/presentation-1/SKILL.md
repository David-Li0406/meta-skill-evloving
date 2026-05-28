---
name: presentation
description: This skill should be used when the user asks to "create a presentation", "generate slides", "make a presentation", "turn into slides", "presentation from this document", "slides from PRD", "slides from transcript", or wants to convert any document into an HTML slide presentation.
version: 1.0.0
---

# Presentation Generator

Generate dark-themed HTML presentations from any document type.

## When to Use

Invoke when the user provides document content and requests a presentation, slides, or visual summary.

## Process

1. **Receive content** from the user (PRD, transcript, notes, article, etc.)
2. **Accept optional theme** parameter to override auto-selection
3. **Detect document type** to apply appropriate extraction rules
4. **Detect language** for RTL (Hebrew, Arabic) or LTR layout
5. **Extract structure** - identify chapters/sections for navigation
6. **Extract key content** per section - prioritize numbers, stats, key phrases
7. **Select theme color** based on topic (or use override)
8. **Generate HTML** using the template from `assets/template.html`
9. **Save file** to working directory as `{topic-slug}-presentation.html`

## Theme Selection

Auto-select based on content keywords, or accept explicit override:

| Theme ID | Topic | Accent | Keywords |
|----------|-------|--------|----------|
| `tech` | Technology/Dev | #00d4ff | code, API, software, deploy, dev |
| `business` | Business/Sales | #00ff88 | sales, revenue, market, B2B, growth |
| `finance` | Finance | #ffd700 | budget, ROI, investment, cost, profit |
| `health` | Medical/Health | #20b2aa | patient, clinical, health, medical |
| `education` | Education | #a855f7 | learn, course, student, training |
| `creative` | Design/Creative | #ff6b9d | design, brand, visual, creative |
| `default` | General | #3b82f6 | (fallback) |

## Chapter Accent Colors

Each chapter gets a unique accent color from the palette for visual variety:

| Chapter | Color | Hex |
|---------|-------|-----|
| 1 | Green | #00ff88 |
| 2 | Cyan | #00d4ff |
| 3 | Gold | #ffd700 |
| 4 | Pink | #ff6b9d |
| 5 | Purple | #a855f7 |
| 6 | Blue | #3b82f6 |

Colors cycle for presentations with more than 6 chapters.

## Slide Design Principles

**Content per slide:**
- Maximum 10-15 words
- 1 idea per slide
- Skip source document intros/titles

**Priority order:**
1. Large numbers/statistics (e.g., "60-70%", "$2.5M")
2. Key metrics with context (e.g., "20% growth target")
3. Single impactful phrases
4. Simple diagrams via CSS

**Slide types to generate:**
- **Hero number**: Large stat centered, brief context below
- **Key point**: Single phrase, large typography
- **Comparison**: Side-by-side options or before/after
- **List**: Max 3-4 bullet points, minimal text each
- **Quote**: Large text with attribution
- **Chapter title**: Section name, minimal

## Language Detection & Fonts

Detect RTL languages by checking for Hebrew (א-ת) or Arabic (ء-ي) characters:
- If RTL detected: set `<html dir="rtl">`
- Otherwise: set `<html dir="ltr">`

### Font Selection by Language

| Language | Font | Google Fonts CSS |
|----------|------|------------------|
| Hebrew | Heebo | `family=Heebo:wght@300;400;500;600;700;800;900` |
| Arabic | Noto Sans Arabic | `family=Noto+Sans+Arabic:wght@300;400;500;600;700;800;900` |
| Default (Latin) | Inter | `family=Inter:wght@300;400;500;600;700;800;900` |

Run `scripts/suggest-fonts.sh [hebrew|arabic|latin|all]` for font options by language.

## Output Structure

Generate a single HTML file with embedded CSS and JavaScript:

```html
<!DOCTYPE html>
<html lang="[detected]" dir="[rtl|ltr]">
<head>
  <style>
    :root {
      --accent: [theme-color];
      --accent-glow: [theme-glow];
      /* ... dark theme variables */
    }
    /* Full CSS from template */
  </style>
</head>
<body>
  <nav class="chapter-nav">
    <!-- Chapter links -->
  </nav>
  <div class="slide-container">
    <!-- Slides with data-chapter attributes -->
  </div>
  <div class="slide-counter">1/N</div>
  <script>
    /* Keyboard navigation */
  </script>
</body>
</html>
```

## File Naming

Generate filename from topic:
- Extract main subject from content
- Convert to lowercase slug (spaces → hyphens)
- Append `-presentation.html`
- Example: "B2B Platform PRD" → `b2b-platform-presentation.html`

## Additional Resources

### Template
- **`assets/template.html`** - Complete HTML/CSS/JS base template with RTL support

### Reference
- **`references/content-extraction.md`** - Detailed extraction rules per document type

### Scripts
- **`scripts/suggest-fonts.sh`** - Suggest Google Fonts by language (hebrew/arabic/latin/all)

## Example Invocations

```
User: Create a presentation from this PRD: [content]
→ Auto-detect type, theme, language; generate slides

User: Generate slides with "finance" theme from: [content]
→ Use gold theme override; generate slides

User: Turn this meeting transcript into a presentation
→ Extract decisions, action items, key quotes
```
