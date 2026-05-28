---
name: competitive-analysis
description: "Market and competitive analysis toolkit. Research competitors, analyze market positioning, identify differentiation opportunities, and create comprehensive competitive landscape assessments for software projects."
allowed-tools: [Read, Write, Edit, Bash, WebFetch, WebSearch]
---

# Competitive Analysis

## Overview

Competitive analysis is a systematic process for understanding the market landscape, identifying competitors, and finding differentiation opportunities. Research existing solutions, analyze their strengths and weaknesses, understand market positioning, and inform product strategy with evidence-based insights.

## When to Use This Skill

This skill should be used when:
- Researching competitors before starting a new project
- Analyzing market positioning and differentiation opportunities
- Understanding feature landscapes across competing products
- Identifying market gaps and opportunities
- Creating competitive analysis documents for stakeholders
- Informing product strategy and roadmap decisions

## Visual Enhancement with Project Diagrams

**When documenting competitive analysis, always include visualizations.**

Use the **project-diagrams** skill to generate:
- Competitive positioning maps (2x2 matrices)
- Feature comparison charts
- Market segment diagrams
- SWOT analysis visualizations
- Competitor landscape maps

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Competitive Analysis Framework

### Analysis Components

| Component | Purpose | Key Questions |
|-----------|---------|--------------|
| **Market Overview** | Understand the market | What is the market size? Who are the players? |
| **Competitor Profiles** | Deep dive on competitors | What do they do? How are they positioned? |
| **Feature Analysis** | Compare capabilities | What features exist? What's missing? |
| **Positioning Analysis** | Understand market positions | Where do competitors position themselves? |
| **Differentiation Strategy** | Find your angle | How can we be different and better? |

## Research Process

### Phase 1: Market Discovery

**Identify the market landscape:**

1. **Define the market category**
   - What problem space are we in?
   - What are adjacent categories?
   - How do customers describe this space?

2. **Search for competitors**
   - Use `research-lookup` to find existing solutions
   - Search product directories (G2, Capterra, Product Hunt)
   - Review industry reports and analyst coverage
   - Search for "[category] alternatives" and "[competitor] vs"

3. **Categorize competitors**

   | Category | Description | Priority |
   |----------|-------------|----------|
   | **Direct** | Same problem, same solution approach | High |
   | **Indirect** | Same problem, different solution | Medium |
   | **Potential** | Could enter this space easily | Monitor |
   | **Substitute** | Alternative ways to solve the problem | Awareness |

### Phase 2: Competitor Profiling

**For each significant competitor, research:**

```yaml
competitor_profile:
  name: "Competitor Name"
  website: "https://..."
  category: "direct | indirect | potential | substitute"
  priority: "primary | secondary | tertiary"

  company_info:
    founded: YYYY
    headquarters: "City, Country"
    funding: "Series X / Public / Bootstrapped"
    employees: "Range"
    valuation_revenue: "If known"

  product:
    description: "What they do in 1-2 sentences"
    target_market: "Who they serve"
    positioning: "How they position themselves"
    pricing:
      model: "SaaS / Usage / One-time / Freemium"
      tiers: ["Free", "Pro: $X/mo", "Enterprise: Custom"]

  strengths:
    - "Key strength 1"
    - "Key strength 2"

  weaknesses:
    - "Key weakness 1"
    - "Key weakness 2"

  market_presence:
    estimated_customers: "If known"
    notable_customers: ["Company A", "Company B"]
    geographic_focus: "Global / Regional"

  technology:
    platform: "Web / Mobile / Desktop / API"
    tech_stack: "If known"
    integrations: ["Integration 1", "Integration 2"]

  recent_developments:
    - date: "YYYY-MM"
      event: "What happened"

  sources:
    - "URL where information was found"
```

### Phase 3: Feature Analysis

**Create a feature comparison matrix:**

```yaml
feature_comparison:
  categories:
    - name: "Core Features"
      features:
        - name: "Feature A"
          description: "What this feature does"
          importance: "critical | important | nice_to_have"
          competitors:
            "Competitor 1": "full | partial | none"
            "Competitor 2": "full | partial | none"
            "Our Plan": "full | partial | none | future"

        - name: "Feature B"
          # ...

    - name: "Advanced Features"
      features:
        # ...

    - name: "Platform & Integration"
      features:
        # ...
```

**Feature rating definitions:**
- **Full**: Complete implementation
- **Partial**: Limited or basic implementation
- **None**: Not offered
- **Future**: Planned for our product

### Phase 4: Positioning Analysis

**Map competitors on positioning dimensions:**

**Common positioning axes:**
- Price (Low ↔ High)
- Complexity (Simple ↔ Advanced)
- Target Market (SMB ↔ Enterprise)
- Focus (Generalist ↔ Specialist)
- Approach (Self-serve ↔ High-touch)

**Positioning Map:**
```
                    High Price
                        │
          ┌─────────────┼─────────────┐
          │ Premium     │ Enterprise  │
          │ [Comp C]    │ [Comp A]    │
          │             │             │
Simple ───┼─────────────┼─────────────┼─── Advanced
          │             │             │
          │ Budget      │ Power User  │
          │ [Comp D]    │ [Comp B]    │
          └─────────────┼─────────────┘
                        │
                    Low Price
```

**Identify white space:**
- Where are there gaps in the map?
- Which positions are crowded?
- Where could we uniquely position?

### Phase 5: SWOT Analysis

**For each major competitor:**

```yaml
swot_analysis:
  competitor: "Competitor Name"

  strengths:
    - factor: "Strong brand recognition"
      impact: "high"
      evidence: "Top-of-mind in category, high search volume"

    - factor: "Extensive integrations"
      impact: "medium"
      evidence: "500+ integrations listed"

  weaknesses:
    - factor: "Complex pricing"
      impact: "medium"
      evidence: "Frequent complaints in reviews about unexpected costs"

    - factor: "Poor mobile experience"
      impact: "high"
      evidence: "2.5 star app store rating"

  opportunities:
    - factor: "Underserved SMB segment"
      impact: "high"
      evidence: "Pricing starts at $50/user, reviews mention 'too expensive for small teams'"

  threats:
    - factor: "Strong network effects"
      impact: "high"
      evidence: "Viral adoption within organizations"
```

**Aggregate into market SWOT:**
- Industry-wide strengths and weaknesses
- Market opportunities
- Competitive threats

### Phase 6: Differentiation Strategy

**Identify differentiation opportunities:**

1. **Feature Gaps**
   - What do customers want that no one offers?
   - What's done poorly by everyone?
   - What new capabilities are becoming possible?

2. **Market Segment Gaps**
   - Which customer segments are underserved?
   - Where is pricing misaligned with value?
   - Which use cases are ignored?

3. **Experience Gaps**
   - Where is UX frustrating?
   - What's overly complex?
   - Where can we simplify?

4. **Technology Gaps**
   - What's outdated?
   - What new tech enables better solutions?
   - Where is performance lacking?

**Differentiation Strategy Options:**

| Strategy | When to Use | Risk |
|----------|-------------|------|
| **Cost Leadership** | Can sustainably be cheaper | Race to bottom |
| **Differentiation** | Clear unique value | Hard to communicate |
| **Focus (Niche)** | Specific segment underserved | Limited market |
| **Innovation** | New approach is possible | Execution risk |
| **Experience** | Can be significantly better UX | Easily copied |

## Output Templates

### Competitive Analysis Report

```markdown
# Competitive Analysis: [Market Category]

## Executive Summary
- Market overview (2-3 sentences)
- Number of competitors analyzed
- Key insights (3-5 bullets)
- Recommended positioning

## Market Overview
### Market Size and Growth
[TAM, SAM, SOM if available]

### Market Segments
[Key customer segments and their characteristics]

### Market Trends
[Important trends affecting the market]

## Competitor Landscape

### Primary Competitors
[Detailed profiles of direct competitors]

### Secondary Competitors
[Brief profiles of indirect competitors]

### Competitive Positioning Map
[Visual representation of market positions]

## Feature Comparison
[Feature matrix comparing capabilities]

## Analysis and Insights

### Market Opportunities
[Where gaps exist]

### Competitive Threats
[What to watch out for]

### Differentiation Opportunities
[How to stand out]

## Recommended Strategy
[Positioning recommendation with rationale]

## Appendix
- Detailed competitor profiles
- Data sources
- Feature comparison data
```

### Competitor Profile Template

```markdown
# Competitor Profile: [Name]

## Overview
**Website:** [URL]
**Category:** Direct / Indirect
**Founded:** [Year]
**Funding:** [Amount or status]
**Employees:** [Range]

## Product Description
[What they do and who they serve]

## Pricing
| Tier | Price | Key Features |
|------|-------|--------------|
| | | |

## Strengths
- [Strength 1]
- [Strength 2]

## Weaknesses
- [Weakness 1]
- [Weakness 2]

## Key Features
[List of notable features]

## Customer Reviews Summary
**Positive themes:**
- [Theme 1]

**Negative themes:**
- [Theme 1]

## Recent News
- [Date]: [Event]

## Sources
- [URL 1]
- [URL 2]
```

## Research Best Practices

### Do's
- Use multiple sources (don't rely on competitor's marketing alone)
- Include customer reviews (G2, Capterra, Reddit, Twitter)
- Look for recent news and funding announcements
- Document all sources for credibility
- Update analysis regularly (market changes)
- Talk to actual users when possible

### Don'ts
- Don't just copy competitor marketing claims
- Don't ignore indirect competitors
- Don't assume feature lists equal actual capabilities
- Don't skip pricing research
- Don't make analysis too long (focus on insights)
- Don't let analysis replace customer research

### Finding Information

**Product information:**
- Company websites and blogs
- Press releases and news
- Crunchbase, PitchBook for funding
- LinkedIn for employee counts

**Customer sentiment:**
- G2, Capterra, TrustRadius reviews
- Reddit discussions
- Twitter mentions
- App store reviews

**Market data:**
- Industry analyst reports
- Market research firms
- Trade publications
- SEC filings (public companies)

**Feature details:**
- Product documentation
- Help centers
- YouTube demos
- Free trials

## Quality Checklist

Before completing competitive analysis:

- [ ] Market clearly defined
- [ ] All major competitors identified
- [ ] At least 3 direct competitors profiled
- [ ] Feature comparison completed
- [ ] Positioning map created
- [ ] Strengths and weaknesses documented
- [ ] Differentiation opportunities identified
- [ ] All sources cited
- [ ] Analysis is actionable (not just descriptive)
- [ ] Insights support product strategy decisions
