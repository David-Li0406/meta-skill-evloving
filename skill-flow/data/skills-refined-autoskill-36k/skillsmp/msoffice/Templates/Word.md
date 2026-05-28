# Word Document Workflow

Generate professional Word documents (.docx) from any topic.

## Content JSON Schema

```json
{
  "subtitle": "Optional document subtitle",
  "author": "Author name (optional)",
  "sections": [
    {
      "heading": "Section Title",
      "level": 1,
      "content": "Paragraph text or array of paragraphs",
      "bullets": ["Bullet point 1", "Bullet point 2"],
      "numbered": ["Numbered item 1", "Numbered item 2"],
      "table": {
        "headers": ["Column 1", "Column 2"],
        "rows": [["Value 1", "Value 2"]]
      }
    }
  ]
}
```

## Section Types

| Element | Usage | Example |
|---------|-------|---------|
| `heading` | Section title | "Executive Summary" |
| `level` | Heading level 1-3 | 1 for main, 2 for sub |
| `content` | Paragraph(s) | String or array of strings |
| `bullets` | Unordered list | ["Item 1", "Item 2"] |
| `numbered` | Ordered list | ["Step 1", "Step 2"] |
| `table` | Data table | {headers: [...], rows: [...]} |

## Workflow Steps

### 1. Understand Requirements
- What is the document's purpose?
- Who is the audience?
- What sections are needed?
- What level of detail?

### 2. Research (if needed)
For factual content, use the Research skill first:
```
/research [topic] for a detailed report
```

### 3. Structure Content
Organize into logical sections:
- **Reports**: Executive Summary → Background → Findings → Recommendations
- **Proposals**: Overview → Problem → Solution → Benefits → Next Steps
- **Guides**: Introduction → Prerequisites → Steps → Troubleshooting

### 4. Generate Document

```bash
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type word \
  --title "[Document Title]" \
  --content '[JSON content]' \
  --output ~/Downloads/[filename].docx
```

### 5. Report Location
Tell the user:
```
Document created: ~/Downloads/[filename].docx
You can access it locally or via Kai Mobile App.
```

## Example: Technical Report

```bash
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type word \
  --title "Q4 Technical Review" \
  --content '{
    "subtitle": "Infrastructure Performance Analysis",
    "author": "Engineering Team",
    "sections": [
      {
        "heading": "Executive Summary",
        "level": 1,
        "content": "This report analyzes Q4 infrastructure performance..."
      },
      {
        "heading": "Key Metrics",
        "level": 1,
        "table": {
          "headers": ["Metric", "Target", "Actual", "Status"],
          "rows": [
            ["Uptime", "99.9%", "99.95%", "Achieved"],
            ["Response Time", "<200ms", "185ms", "Achieved"]
          ]
        }
      },
      {
        "heading": "Recommendations",
        "level": 1,
        "bullets": [
          "Upgrade database cluster to handle growth",
          "Implement additional caching layer",
          "Review security policies quarterly"
        ]
      }
    ]
  }' \
  --output ~/Downloads/q4-technical-review.docx
```

## Filename Convention

Use descriptive, lowercase, hyphenated names:
- `quarterly-report-q4-2024.docx`
- `project-proposal-alpha.docx`
- `meeting-notes-2024-01-15.docx`
