# News & Trigger Event Monitoring

## When to Use
- Finding outreach triggers
- Competitive monitoring
- Market intelligence
- Content inspiration
- Crisis detection

## Trigger Events That Matter

### High-Value Triggers (Act immediately)

| Trigger | Why It Matters | Outreach Timing |
|---------|---------------|-----------------|
| **Funding Round** | Budget unlocked, growth mode | Within 1 week |
| **New Executive** | New decision maker, fresh perspective | Within 2 weeks |
| **Acquisition** | Integration needs, budget reallocation | Within 1 month |
| **Product Launch** | Momentum, may need supporting tools | Within 2 weeks |
| **IPO/Going Public** | Compliance needs, scaling pressure | Within 1 month |

### Medium-Value Triggers (Act within 2 weeks)

| Trigger | Why It Matters | Outreach Timing |
|---------|---------------|-----------------|
| **Office Expansion** | Growth, new market needs | Within 1 month |
| **Major Partnership** | Strategic shift, integration needs | Within 2 weeks |
| **Award/Recognition** | Good time for congratulations | Within 1 week |
| **Conference Speaking** | Thought leadership, accessible | Before/after event |
| **Hiring Surge** | Scaling pains, tool needs | Within 1 month |

### Low-Value Triggers (Use for personalization)

| Trigger | Use Case |
|---------|----------|
| Blog post | Reference in outreach |
| Social post | Engagement opportunity |
| Podcast appearance | Reference in outreach |
| Minor news | Personalization hook |

## Monitoring Tool Sequences

### Daily Competitor Watch
```
web_search("[competitor] news")
web_search("[competitor] announces OR launches OR raises")
firecrawl_scrape(competitor_blog_url)
```

### Weekly Market Scan
```
web_search("[market] funding OR acquisition")
web_search("[market] startup news")
reddit_search("[market] new", subreddit="SaaS")
```

### Account-Based Monitoring
For specific target accounts:
```
web_search("[company name] news")
web_search("[company name] [CEO name]")
proxycurl_linkedin(ceo_linkedin_url)  # Check for posts
crunchbase_lookup(company)  # Check for funding updates
```

## News Search Strategies

### Funding News
```
web_search("[company] raises OR funding OR series")
web_search("[company] investors OR backed")
crunchbase_lookup(company_slug)
```

### Leadership Changes
```
web_search("[company] names OR appoints OR hires")
web_search("[company] new CEO OR CMO OR VP")
apollo_people_search(company, titles=["CEO", "CMO"]) # Compare to known
```

### Product News
```
web_search("[company] launches OR announces OR introduces")
web_search("[company] new feature OR product")
firecrawl_scrape(company_blog)
firecrawl_scrape(company_changelog)
```

### Partnership/Integration News
```
web_search("[company] partners OR integrates OR joins")
web_search("[company] [potential partner]")
```

### Expansion News
```
web_search("[company] expands OR opens OR enters")
web_search("[company] new office OR headquarters")
```

## Trigger Event Detection Patterns

### In Web Search Results

**Funding signals:**
- "raises $X"
- "secures funding"
- "closes round"
- "led by [investor]"
- "Series A/B/C"

**Hiring signals:**
- "is hiring"
- "opens X positions"
- "growing team"
- "hiring spree"

**Product signals:**
- "launches"
- "introduces"
- "announces"
- "unveils"
- "releases"

**Expansion signals:**
- "expands to"
- "opens office"
- "enters market"
- "international expansion"

## Alert Configuration

### Google Alerts (Free)
Set up alerts for:
- `"[competitor name]"`
- `"[competitor name]" funding OR acquisition`
- `"[your market]" startup OR launch`
- `"[target company]" news`

### Social Monitoring
- Follow competitor executives on LinkedIn
- Set up Twitter lists for industry voices
- Monitor relevant subreddits

## Trigger-Based Outreach Templates

### Funding Round
```
Subject: Congrats on the [Series X] 🎉

Hi [Name],

Saw the news about [Company]'s [Series X] - congrats! 
[Investor] is a great partner.

Funding rounds often mean scaling [area we help with]. 
[Short value prop].

Worth a quick chat?

[Name]
```

### New Executive
```
Subject: Welcome to [Company]

Hi [Name],

Congrats on the new role at [Company]! 
The first 90 days are always intense.

One thing [similar executives] often tackle early: [problem we solve].
[1-sentence value prop].

Would 15 mins be useful as you get settled?

[Name]
```

### Product Launch
```
Subject: [Product] looks great

Hi [Name],

Just saw [Company] launched [Product] - the [specific feature] is clever.

Curious: are you seeing [challenge related to launch]? 
We helped [similar company] with that during their launch.

Worth comparing notes?

[Name]
```

### Office Expansion
```
Subject: [City] expansion

Hi [Name],

Saw [Company] is expanding to [City] - exciting growth!

New markets often mean [challenge we solve]. 
[How we help].

Happy to share how [similar company] handled this.

[Name]
```

## Competitive Monitoring Dashboard

Track these metrics weekly:

| Metric | How to Track |
|--------|--------------|
| Website changes | firecrawl_screenshot + compare |
| Pricing changes | firecrawl_scrape(pricing_page) |
| New features | firecrawl_scrape(changelog) |
| Content published | firecrawl_scrape(blog) |
| Social engagement | Manual or social tools |
| Review ratings | g2_scrape, capterra_scrape |
| Job postings | web_search("[company] careers") |
| News mentions | web_search("[company] news") |

## Output Templates

### Daily Intel Brief
```markdown
# Daily Intel: [Date]

## 🔥 Hot Triggers (Action Today)
- [Company]: [Trigger] - [Source]
- [Company]: [Trigger] - [Source]

## 📰 Competitor News
- [Competitor]: [News item]
- [Competitor]: [News item]

## 📈 Market Signals
- [Trend/news item]
- [Trend/news item]

## 🎯 Outreach Opportunities
1. [Company] - [Trigger] - [Suggested action]
2. [Company] - [Trigger] - [Suggested action]
```

### Weekly Competitive Digest
```markdown
# Weekly Competitive Digest: [Week]

## Summary
[2-3 sentences on key themes this week]

## Competitor Updates

### [Competitor 1]
- **News:** [Summary]
- **Product:** [Any updates]
- **Content:** [Notable content]
- **Implication:** [What it means for us]

### [Competitor 2]
[Same structure]

## Market Movements
- [Trend 1]
- [Trend 2]

## Action Items
- [ ] [Action based on intel]
- [ ] [Action based on intel]
```

## Quality Checklist

Before delivering trigger/news intelligence:

- [ ] Events verified from multiple sources
- [ ] Dates are accurate and recent
- [ ] Trigger relevance to outreach explained
- [ ] Suggested timing included
- [ ] Outreach angle provided
- [ ] Sources linked
