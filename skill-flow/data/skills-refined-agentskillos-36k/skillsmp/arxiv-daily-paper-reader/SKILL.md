---
name: arxiv-daily-paper-reader
description: Comprehensive arXiv paper search and retrieval tool with keyword search, category filtering, date range filtering, and daily paper fetching capabilities. Use for "搜索arXiv论文", "获取最新论文", "arXiv文献调研", "生成论文报告", "查找cs.AI相关论文".
dependencies: ["feedparser>=6.0.10"]
---

# arXiv Daily Paper Reader

## Overview

Powerful arXiv paper search and retrieval tool supporting **keyword search**, **category filtering**, **date range filtering**, and **daily paper fetching**. 
Only Fetch yesterday's latest papers. Ideal for researchers, scholars, and students.

## Core Features

- 🔍 **Search**: Full-text search with keywords, phrases, advanced arXiv syntax
- 📂 **Category Filter**: 85+ arXiv categories (cs.AI, cs.LG, cs.CV, etc.)
- 📅 **Date Range**: Relative dates (last 30 days) or absolute date ranges
- 📊 **Daily Fetch**: Automatically fetch yesterday's arXiv papers (no limit)
- 📝 **Multiple Formats**: Markdown reports, JSON data, console preview
- 🔗 **Complete Links**: Direct links to papers and PDFs

## When to Use

Trigger this skill when user asks to:
- Search arXiv papers by keywords
- Get latest papers from specific categories
- Generate paper reports for research meetings
- Track specific research areas over time
- Find papers on specific topics (GANs, transformers, etc.)

### Example Triggers

- "搜索机器学习相关的最新论文"
- "查找计算机视觉领域关于GAN的论文"
- "给我获取cs.AI领域的最新论文报告"
- "生成cs.PL和cs.SE的最新论文摘要"
- "获取2023年AI领域的重要研究"

## Supported Categories

### Default Categories
- **cs.OS**: Operating Systems
- **cs.PL**: Programming Languages
- **cs.SE**: Software Engineering
- **cs.AI**: Artificial Intelligence

### Other Popular Categories
- cs.LG: Machine Learning
- cs.CV: Computer Vision
- cs.CL: Computation and Language
- cs.DB: Databases
- cs.DC: Distributed, Parallel, and Cluster Computing

## Basic Usage

### Natural Language (Recommended)

```
请使用arXiv Daily Reader获取最新的cs.AI论文并生成报告
```

### Command Line

```bash
# Get yesterday's papers (default categories)
python skill.py fetch

# Fetch specific categories
python skill.py fetch --cats cs.AI cs.LG cs.CV --max-papers 20

# Search by category and date
python skill.py search --categories cs.SE --days 7 --max-results 15

# Get help
python skill.py --help
python skill.py fetch --help
python skill.py search --help
```

## Output Formats

### Markdown Report
```markdown
# arXiv Daily Paper Report
Generated on: 2025-12-18
Categories: cs.OS, cs.PL, cs.SE, cs.AI
Total Papers: 32

## cs.AI (8 papers)
### Paper Title
*Authors:* Author list
*Published:* Date
**Summary:** Abstract excerpt
[Read Paper](link) | [PDF](pdf_link)
```

### JSON Data
```json
{
  "id": "paper-id",
  "title": "Paper Title",
  "authors": ["Author1", "Author2"],
  "summary": "Abstract...",
  "published": "2025-12-18",
  "categories": ["cs.AI"],
  "link": "https://arxiv.org/abs/...",
  "pdf_link": "https://arxiv.org/pdf/..."
}
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python skill.py fetch` | Get yesterday's papers |
| `python skill.py fetch --cats cs.AI` | Fetch specific categories |
| `python skill.py search --categories cs.SE --days 7` | Search last 7 days |
| `python skill.py search --output-format json` | Output as JSON |

See `references/cli-usage.md` for complete CLI documentation.

## Technical Details

- **Python**: 3.12+ with feedparser
- **API**: arXiv Query API and RSS feeds
- **Rate Limiting**: Respects arXiv API limits with automatic retries
- **Output**: Markdown reports, JSON data, or console preview

See `references/` for:
- `api-details.md` - Complete API documentation
- `implementation.md` - Technical implementation details
- `cli-usage.md` - Full command-line reference

## Examples

See `examples/` directory for:
- `basic-fetch.md` - Fetch yesterday's papers
- `category-search.md` - Search specific categories
- `date-range-search.md` - Search by date range
- `output-formats.md` - Different output formats

## Best Practices

1. **Regular Use**: Weekly or biweekly for tracking progress
2. **Category Selection**: Choose relevant research areas
3. **Batch Processing**: Fetch multiple related categories at once
4. **Data Management**: Clean up old report files regularly

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Network errors | Check internet connection, retry |
| API rate limit | Wait before retrying |
| Format issues | System auto-handles special formats |

See `references/cli-usage.md` for complete troubleshooting.
