---
name: feature-upgrade-skill
description: High-impact competitive analysis and feature ideation. Use when tasked with improving the app vs competitors, identifying market gaps, or researching user pain points in similar products to outperform them.
---

# Feature and Upgrade Skill

This skill enables Claude to perform deep competitive research and propose high-impact app improvements by mining competitor successes and user frustrations.

## Workflow

### 1. Niche & Value Proposition Identification

Identify the core problem the current application solves and its target audience.

- Check `README.md` or `docs/` for project overview.
- Define the "Unique Selling Point" (USP) if already documented.

### 2. Competitor Discovery

Use `search_web` to find the top 3-5 competitors in the niche.

- Search for "best [niche] apps", "top [niche] platforms 2025/2026", "competitors to [niche product]".

### 3. Analysis of Competitor Strengths

Research what competitors prioritize in their marketing.

- Use `read_url_content` on competitor landing pages.
- Identify their "hero" features and main marketing claims.

### 4. Sentiment Mining (Pain Points)

Find out what users DON'T like about competitors.

- Search for "[competitor name] reviews", "[competitor name] reddit", "[competitor name] vs [other competitor]".
- Look for common complaints: "too expensive", "missing [feature]", "bad UI", "buggy performance".

### 5. Gap Analysis & Ideation

Synthesize findings into a competitive matrix.

- What do ALL competitors have? (Table stakes)
- what is NO ONE doing? (Opportunity gap)
- What are the most requested features? (Quick wins)

### 6. Proposal Generation

Create a prioritized list of features for the current app.

- Provide a clear rationale for each feature based on research.
- Estimate the "impact vs effort" for each recommendation.

## Reference Materials

- [Market Analysis Template](references/market-analysis-template.md) - Structure for gathering findings.
