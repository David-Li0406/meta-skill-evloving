---
name: ai-news-daily
description: "Automatically fetch and summarize the latest AI news, research, and industry developments. Use when users request: (1) Daily AI news updates, (2) Latest AI technology developments, (3) Recent AI research papers or breakthroughs, (4) AI industry trends and market news, (5) Specific AI company announcements, or (6) Automated daily AI briefings. Supports customizable search queries, multi-source aggregation, and formatted output in various styles."
---

# AI News Daily

Fetch and curate the latest AI news, research papers, industry developments, and technology breakthroughs from multiple sources.

## Overview

This skill enables automated collection and summarization of AI industry news from across the web. It combines strategic search queries, source quality filtering, and flexible formatting to deliver timely, relevant AI updates tailored to user preferences.

## Core Workflow

1. **Determine Search Strategy** - Based on user request, decide which AI news categories to search
2. **Execute Web Searches** - Query multiple sources for latest information
3. **Filter and Rank** - Prioritize recent, authoritative, and relevant content
4. **Summarize and Present** - Format findings in requested style (brief, detailed, or report)

## Search Categories

### General AI News
- **Query patterns**: "AI news today", "latest AI developments", "AI industry news"
- **Sources to prioritize**: TechCrunch AI, VentureBeat AI, The Verge AI, MIT Technology Review
- **Time filter**: Focus on content from last 24-48 hours

### AI Research & Papers
- **Query patterns**: "latest AI research", "new AI papers", "arxiv AI", "AI breakthroughs"
- **Sources to prioritize**: arXiv.org, Papers with Code, Google AI Blog, OpenAI Research
- **Time filter**: Last 7 days for research papers

### Company Announcements
- **Query patterns**: "[Company] AI announcement", "OpenAI news", "Google AI", "Anthropic updates"
- **Sources to prioritize**: Official company blogs, press releases
- **Time filter**: Last 30 days

### AI Market & Business
- **Query patterns**: "AI funding", "AI startup", "AI market trends", "AI investment"
- **Sources to prioritize**: Bloomberg AI, Reuters Tech, Financial Times Tech
- **Time filter**: Last 7 days

### Specific Technology Areas
- **Query patterns**: "LLM news", "computer vision", "robotics AI", "AI agents"
- **Sources to prioritize**: Domain-specific publications and research sites
- **Time filter**: Last 14 days

## Search Execution Guidelines

### Multi-Source Strategy
For comprehensive coverage, execute 3-5 searches per request:
1. One broad search (e.g., "AI news today")
2. 2-3 targeted searches (e.g., "LLM research", "AI startup funding")
3. One company-specific search if relevant (e.g., "OpenAI announcement")

### Time-Based Filtering
- **Daily briefing**: Use "today" or "yesterday" in queries
- **Weekly summary**: Search "AI news this week" or "latest AI developments"
- **Trending topics**: Search "AI trends 2025" or current month/quarter

### Source Quality Indicators
Prioritize results from:
- Official company blogs and research pages
- Peer-reviewed publications (arXiv, Nature, Science)
- Major tech news outlets (TechCrunch, The Verge, Wired)
- Industry analysts (Gartner, IDC, CB Insights)

## Output Formatting

### Brief Format (Default)
5-10 bullet points with:
- Headline
- 1-2 sentence summary
- Source and date
- Link

Example:
```
• OpenAI Launches GPT-5
  Major performance improvements in reasoning and coding. Announced via company blog today.
  [Link to announcement]
```

### Detailed Format
For each story:
- Full headline
- 2-3 paragraph summary
- Key implications or significance
- Source, author, publication date
- Direct quotes if available
- Related links

### Report Format
Structured document with:
- Executive summary (top 3-5 stories)
- Categorized sections (Research, Products, Business, Policy)
- Trend analysis
- Notable quotes
- Full source citations

## Customization Options

### User Preferences
Ask users about:
- **Focus areas**: "Which AI topics interest you most? (e.g., LLMs, computer vision, robotics)"
- **Update frequency**: "How often would you like updates? (daily, weekly)"
- **Detail level**: "Do you prefer brief headlines or detailed summaries?"
- **Sources**: "Any specific sources you want included or excluded?"

### Filters
- Exclude specific companies or topics
- Focus on open-source projects only
- Academic research only vs. industry news only
- Specific geographic regions (US, China, EU AI news)

## Error Handling

### No Recent Results
If searches return limited recent content:
1. Expand time window to last 3-7 days
2. Broaden search terms
3. Note the date of latest available information
4. Suggest alternative search angles

### Low Quality Results
If results lack authoritative sources:
1. Re-search with "site:" operators for trusted domains
2. Look for original sources vs. aggregators
3. Cross-reference multiple sources
4. Flag uncertainty to user

## Best Practices

1. **Always verify dates** - AI news sites often have outdated content ranked highly
2. **Prioritize original sources** - Go to company blogs, not third-party summaries
3. **Note information currency** - Tell users when content is from (today, this week, etc.)
4. **Provide context** - Explain why a development matters
5. **Include links** - Always give users access to full articles
6. **Avoid speculation** - Stick to announced facts, not rumors
7. **Cite sources clearly** - Maintain attribution for all information

## Example Workflows

### Daily Morning Briefing
```
1. Search "AI news today"
2. Search "AI research papers"
3. Search "AI startup funding"
4. Filter to last 24 hours
5. Select top 5-7 stories
6. Format as brief bullet points
7. Categorize by type (research/product/business)
```

### Weekly Deep Dive
```
1. Search "AI developments this week"
2. Search "latest LLM research"
3. Search "AI policy news"
4. Search top 2-3 AI companies for announcements
5. Aggregate 10-15 key stories
6. Format as detailed report with sections
7. Include trend analysis
```

### Topic-Specific Update
```
1. Ask user for specific AI topic
2. Search "[topic] latest developments"
3. Search "[topic] research papers"
4. Search "[topic] commercial applications"
5. Present findings with technical depth
6. Include academic and industry sources
```

## Resources

### references/
Contains curated lists of trusted AI news sources and search patterns:
- `sources.md` - Authoritative AI news sources organized by category
- `search_patterns.md` - Effective search query templates for different AI topics
