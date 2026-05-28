# People Finder Playbook

## When to Use
- Building outbound lead lists
- ABM contact mapping
- Finding decision makers
- Influencer identification
- Partnership contact finding

## Contact Quality Tiers

| Tier | Definition | Use Case |
|------|------------|----------|
| **Verified** | Email confirmed deliverable | Primary outreach |
| **Enriched** | Email found, not verified | Secondary outreach with verification |
| **Identified** | Name + title, no email | LinkedIn outreach or further enrichment |

## Quick Contact Find (2 minutes)

For a single contact at known company:

```
apollo_people_search(
    company="[Company Name]",
    titles=["VP Marketing", "Head of Marketing", "CMO"],
    limit=5
)
```

Then enrich the best match:
```
apollo_enrich(email="[found_email]")
```

## Deep Contact Research (15 minutes)

For full profile with personalization:

### Step 1: Find the Contact
```
apollo_people_search(
    company="[Company]",
    titles=["target titles"],
    seniority=["director", "vp", "c_suite"]
)
```

### Step 2: Enrich Contact Data
```
apollo_enrich(
    email="[found_email]"
    # Returns: email, phone, LinkedIn, company data
)
```

### Step 3: LinkedIn Deep Dive
```
proxycurl_linkedin(linkedin_url)
# Returns: full profile, experience, education, posts
```

### Step 4: Recent Activity
```
web_search("[person name] [company]")
web_search("[person name] linkedin post")
web_search("[person name] podcast OR interview OR webinar")
```

## Building Lead Lists

### By ICP Criteria

```
apollo_people_search(
    titles=["VP Marketing", "Director of Marketing", "Head of Growth"],
    company_size=["50-200", "200-500"],
    industries=["SaaS", "Software"],
    locations=["United States"],
    limit=100
)
```

### By Company List

For a list of target companies:

```python
companies = ["Notion", "Figma", "Airtable", "Coda"]

for company in companies:
    apollo_people_search(
        company=company,
        titles=["VP Marketing", "CMO"],
        limit=3
    )
```

### By Competitor Customers

```
# Find companies using competitor
builtwith_lookup(competitor_domain)  # Get their customer list
# Then find contacts at those companies
```

## Title Mapping

### Marketing Titles by Seniority

| Seniority | Common Titles |
|-----------|---------------|
| **C-Suite** | CMO, Chief Marketing Officer, Chief Growth Officer |
| **VP** | VP Marketing, VP Growth, VP Demand Gen, VP Brand |
| **Director** | Director of Marketing, Director of Growth, Director of Content |
| **Manager** | Marketing Manager, Growth Manager, Content Manager |
| **IC** | Growth Lead, Content Lead, Marketing Lead |

### By Function

| Function | Titles to Target |
|----------|-----------------|
| **Brand** | VP Brand, Brand Director, Head of Brand |
| **Demand Gen** | VP Demand Gen, Director of Growth, Head of Acquisition |
| **Content** | VP Content, Content Director, Head of Content |
| **Product Marketing** | VP Product Marketing, PMM Director, Head of PMM |
| **Marketing Ops** | VP Marketing Ops, MOps Director, Marketing Operations |

### Decision Maker vs Influencer

| Role | Likely Title | Approach |
|------|--------------|----------|
| **Economic Buyer** | CMO, VP Marketing | Focus on ROI, business impact |
| **Technical Buyer** | Marketing Ops, MOps Manager | Focus on features, integrations |
| **User** | Marketing Manager, Specialist | Focus on ease of use, daily workflow |
| **Champion** | Any level who loves product | Enable them to sell internally |

## LinkedIn Profile Analysis

When you get Proxycurl data, extract:

### Professional Context
- Current role tenure (how long in job)
- Company tenure (might be internal move)
- Previous companies (shared experiences?)
- Career trajectory (rising star? plateaued?)

### Personalization Gold
- Recent posts (topics they care about)
- Articles written (thought leadership)
- Groups (professional interests)
- Volunteer work (personal values)
- Education (alumni connection?)
- Skills endorsed (what they're known for)

### Timing Signals
- New job (first 90 days = evaluating tools)
- Promotion (has budget/authority now)
- Company change (bringing old tools to new company)

## Personalization Hooks

### Tier 1: Specific & Recent (Best)
- Reference specific LinkedIn post from last 30 days
- Mention recent podcast/webinar appearance
- Note recent company announcement they were part of

### Tier 2: Professional Context (Good)
- Shared previous employer
- Similar career path
- Same industry background
- Mutual connection

### Tier 3: Company-Level (Acceptable)
- Company news/funding
- Company product launch
- Industry trend affecting them

### Tier 4: Generic (Last Resort)
- Role-based challenges
- Industry-wide pain points

## Output Templates

### Single Contact

```markdown
## Contact: [Full Name]

### Contact Info
| Field | Value |
|-------|-------|
| Email | [email] (verified/unverified) |
| Phone | [phone] |
| LinkedIn | [url] |
| Twitter | [handle] |

### Current Role
**[Title]** at **[Company]**
Since [Start Date] ([X years, Y months])

### Background
- Previously: [Previous Role] at [Previous Company]
- Education: [Degree] from [School]
- Location: [City, State]

### Recent Activity
- [Date]: [Post/Article summary]
- [Date]: [Podcast/Event appearance]

### Personalization Hooks
1. **Best Hook:** [Most specific, recent reference]
2. **Backup Hook:** [Professional context]
3. **Company Hook:** [Company-level angle]

### Suggested First Line
"[Personalized opening line for email/LinkedIn]"
```

### Lead List

```markdown
## Lead List: [Criteria/Segment Name]

**Criteria:**
- Titles: [titles]
- Company Size: [size]
- Industry: [industry]
- Location: [location]

**Found:** [X] contacts

| Name | Title | Company | Email | LinkedIn | Hook |
|------|-------|---------|-------|----------|------|
| | | | | | |
| | | | | | |

### List Quality
- Verified emails: X%
- LinkedIn profiles found: X%
- Personalization hooks identified: X%
```

## Data Quality Checks

### Email Verification Status
| Status | Meaning | Action |
|--------|---------|--------|
| Verified | Confirmed deliverable | Safe to send |
| Valid | Correct format, not verified | Verify before bulk send |
| Catch-all | Domain accepts all | Test with single send first |
| Invalid | Will bounce | Do not use |
| Unknown | Couldn't verify | Verify manually |

### Data Freshness
- LinkedIn data: Check "last updated" in Proxycurl
- Email: Verify before major campaigns
- Phone: Often outdated, verify before calling
- Title: Check LinkedIn is current (people update slowly)

## Tool Error Handling

### Apollo: No Results
- Try broader title search
- Try company domain instead of name
- Check company is in Apollo database

### Proxycurl: Profile Not Found
- Verify LinkedIn URL format
- Profile may be private
- Try with just the profile ID

### Email Not Found
- Try personal email enrichment
- Use LinkedIn for direct outreach
- Find alternate contact at company

## Compliance Notes

### GDPR/Privacy
- Only use business emails
- Honor opt-outs immediately
- Don't store personal data longer than needed
- Document legitimate interest

### Platform Terms
- Don't scrape LinkedIn directly (use Proxycurl)
- Respect rate limits on all APIs
- Don't resell contact data

### Best Practices
- Personalize to show legitimate interest
- Keep outreach relevant to their role
- Make unsubscribe easy
- Follow up reasonably (not spam)
