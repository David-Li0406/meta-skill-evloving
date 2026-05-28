# PowerPoint Workflow

Generate professional presentations (.pptx) from any topic.

## Content JSON Schema

```json
{
  "subtitle": "Presentation subtitle (shown on title slide)",
  "author": "Presenter name (optional)",
  "slides": [
    {
      "title": "Slide Title",
      "layout": "content|title|section|two_column|blank",
      "bullets": ["Point 1", "Point 2"],
      "content": "Text content (alternative to bullets)",
      "left_column": ["Items for left side"],
      "right_column": ["Items for right side"],
      "notes": "Speaker notes for this slide"
    }
  ]
}
```

## Slide Layouts

| Layout | Use Case | Content Fields |
|--------|----------|----------------|
| `content` | Standard bullet slide (default) | bullets, content |
| `title` | Title slide | (uses title field only) |
| `section` | Section divider | (uses title field only) |
| `two_column` | Side-by-side comparison | left_column, right_column |
| `blank` | Custom/image slide | (minimal) |

## Workflow Steps

### 1. Understand Requirements
- What is the presentation's purpose?
- Who is the audience?
- How much time for the presentation?
- Key message to convey?

### 2. Research (if needed)
For factual content, use the Research skill first:
```
/research [topic] for presentation material
```

### 3. Structure Slides
Follow the rule of 3-5 bullets per slide, 10-15 slides for a 15-minute presentation.

**Standard Structure**:
1. Title slide
2. Agenda/Overview
3-N. Content slides
N+1. Summary/Key Takeaways
N+2. Q&A / Next Steps

### 4. Generate Presentation

```bash
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type powerpoint \
  --title "[Presentation Title]" \
  --content '[JSON content]' \
  --output ~/Downloads/[filename].pptx
```

### 5. Report Location
Tell the user:
```
Presentation created: ~/Downloads/[filename].pptx
You can access it locally or via Kai Mobile App.
```

## Example: Product Launch Deck

```bash
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type powerpoint \
  --title "Product Launch: Project Alpha" \
  --content '{
    "subtitle": "Transforming the Industry",
    "author": "Product Team",
    "slides": [
      {
        "title": "Agenda",
        "bullets": [
          "Market Opportunity",
          "Product Overview",
          "Key Features",
          "Go-to-Market Strategy",
          "Timeline & Next Steps"
        ]
      },
      {
        "title": "Market Opportunity",
        "layout": "two_column",
        "left_column": [
          "$50B market size",
          "15% annual growth",
          "Underserved segment"
        ],
        "right_column": [
          "3 major competitors",
          "No clear leader",
          "High customer demand"
        ],
        "notes": "Emphasize the timing opportunity"
      },
      {
        "title": "Product Overview",
        "bullets": [
          "All-in-one solution for enterprise needs",
          "Built on modern cloud architecture",
          "Seamless integration with existing tools",
          "Enterprise-grade security"
        ]
      },
      {
        "title": "Key Features",
        "section": true
      },
      {
        "title": "Feature Highlights",
        "bullets": [
          "AI-powered automation",
          "Real-time collaboration",
          "Advanced analytics dashboard",
          "Mobile-first design"
        ]
      },
      {
        "title": "Timeline",
        "bullets": [
          "Q1: Beta launch with select customers",
          "Q2: Public launch",
          "Q3: Enterprise features",
          "Q4: International expansion"
        ]
      },
      {
        "title": "Questions?",
        "layout": "section"
      }
    ]
  }' \
  --output ~/Downloads/product-launch-alpha.pptx
```

## Best Practices

**Content Guidelines**:
- 3-5 bullets per slide maximum
- 6-8 words per bullet
- Use parallel structure in lists
- One key idea per slide

**Slide Count Guidelines**:
- 5-minute presentation: 5-7 slides
- 15-minute presentation: 10-15 slides
- 30-minute presentation: 20-25 slides

**Filename Convention**:
- `product-launch-2024.pptx`
- `quarterly-review-q4.pptx`
- `team-meeting-2024-01-15.pptx`
