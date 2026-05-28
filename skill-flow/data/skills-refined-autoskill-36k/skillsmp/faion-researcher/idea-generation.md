---
id: idea-generation
name: "Idea Generation"
domain: RES
skill: faion-researcher
category: "research"
---

# Idea Generation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #ideas, #discovery |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-idea-generator-agent |

---

## Problem

Most aspiring solopreneurs get stuck at "I don't have any good ideas." They either:
- Wait for inspiration that never comes
- Chase trending topics without personal fit
- Pick random ideas without systematic evaluation
- Give up before even starting

**The root cause:** No structured framework for generating viable business ideas.

---

## Framework

### What is Idea Generation?

Idea generation is a systematic process of discovering business opportunities by combining your skills, market needs, and personal interests. It's not about waiting for a "eureka" moment.

### The 7 Idea Generation Frameworks

#### 1. Skills Inventory Framework

Map what you already know:

```
My Skills:
- Technical: [Python, SQL, APIs...]
- Domain: [Marketing, Finance, Healthcare...]
- Soft: [Writing, Teaching, Consulting...]

Question: What problems can I solve with these skills?
```

**Example:**
- Skill: Python + Marketing
- Idea: "Automated social media analytics tool for small businesses"

#### 2. Pain Point Mining

Look for complaints in:
- Reddit threads (sort by "top" in niche subreddits)
- Twitter/X rants
- App store reviews (1-2 star)
- Quora questions
- Forum complaints

**Template:**
```markdown
Pain Point: [What people complain about]
Frequency: [How often mentioned]
Current Solutions: [What exists]
Gap: [What's missing]
Idea: [Your solution]
```

#### 3. Job Substitution Framework

List tedious tasks people pay others to do:
- What do freelancers on Upwork/Fiverr do repeatedly?
- What tasks do small businesses outsource?
- What manual work could be automated?

**Idea formula:** "Automate [repetitive task] for [specific audience]"

#### 4. Productized Service Framework

Turn services into products:
1. Find a service you or others provide
2. Identify the repeatable part
3. Package it as a product

**Examples:**
- Consulting → Course
- Custom development → SaaS template
- Design work → Design system

#### 5. Unbundling Framework

Break existing platforms into focused tools:
- Excel → [specific use case tool]
- Notion → [focused app]
- Salesforce → [simpler CRM]

**Question:** "What do people use [big platform] for that deserves its own tool?"

#### 6. Market Stacking

Combine two niches:
- Niche A × Niche B = New opportunity

**Examples:**
- AI × Legal = Contract analysis
- Fitness × Remote work = Home workout for developers
- Crypto × Freelancing = Payment platform

#### 7. Your Own Problems

Document problems you face daily:
- What tools do you wish existed?
- What workflows frustrate you?
- What did you build for yourself?

**Rule:** If you have the problem, others likely do too.

### Idea Scoring Matrix

Rate each idea 1-5:

| Criterion | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Market Size | 20% | ? | |
| Personal Fit | 25% | ? | |
| Competition | 15% | ? | |
| Monetization | 20% | ? | |
| Speed to MVP | 20% | ? | |
| **TOTAL** | 100% | | **?** |

**Scoring Guide:**
- Market Size: 5 = billion dollar, 1 = tiny niche
- Personal Fit: 5 = excited daily, 1 = dreading work
- Competition: 5 = blue ocean, 1 = dominated by giants
- Monetization: 5 = clear path, 1 = unclear revenue
- Speed to MVP: 5 = 2 weeks, 1 = 1+ year

---

## Templates

### Idea Discovery Session Template

```markdown
## Idea Discovery Session - [Date]

### Time Spent: [X] hours
### Frameworks Used: [1-7]

### Ideas Generated

#### Idea 1: [Name]
- **Source Framework:** [Which framework]
- **Problem Solved:** [Description]
- **Target Audience:** [Who]
- **Rough Solution:** [How]
- **Initial Score:** [1-5]
- **Notes:** [Why interesting/not]

#### Idea 2: [Name]
...

### Top 3 to Validate
1. [Idea] - Score: [X]
2. [Idea] - Score: [X]
3. [Idea] - Score: [X]

### Next Steps
- [ ] Validate idea 1 via [method]
- [ ] Research competitors for idea 2
- [ ] Find potential users for idea 3
```

### Weekly Idea Capture Template

```markdown
## Week of [Date]

### Problems I Encountered
1. [Problem] - Potential idea: [Y/N]
2. [Problem] - Potential idea: [Y/N]

### Complaints I Saw Online
1. [Link] - Summary: [X]
2. [Link] - Summary: [X]

### Interesting Services on Upwork
1. [Gig type] - Could be productized: [Y/N]

### Total Ideas Added: [X]
### Ideas Worth Scoring: [X]
```

---

## Examples

### Example 1: Developer Finds SaaS Idea

**Process:**
1. Skills Inventory: Python, APIs, web scraping
2. Pain Point Mining: Reddit r/startups - "monitoring competitor prices is tedious"
3. Market Stack: E-commerce × Automation

**Idea:** Price monitoring SaaS for e-commerce stores

**Score:**
- Market Size: 4 (e-commerce huge)
- Personal Fit: 5 (loves building scrapers)
- Competition: 3 (exists but fragmented)
- Monetization: 5 (clear SaaS model)
- Speed to MVP: 4 (2-3 weeks)
- **Total: 4.2**

**Result:** Built MVP, $3K MRR in 6 months.

### Example 2: Marketer Creates Course

**Process:**
1. Skills Inventory: Facebook Ads, copywriting
2. Job Substitution: Freelancers charge $500+ for ad copy
3. Productized Service: Turn copy framework into templates

**Idea:** Facebook Ad Copy Templates + Course

**Score:**
- Market Size: 4
- Personal Fit: 4
- Competition: 4 (unique angle)
- Monetization: 5 (direct sales)
- Speed to MVP: 5 (2 weeks)
- **Total: 4.4**

**Result:** $15K launch, recurring content revenue.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Waiting for perfect idea | Generate 10 ideas, score them, pick one |
| Only one framework | Use all 7 frameworks systematically |
| Not documenting ideas | Capture every idea, review weekly |
| Ignoring personal fit | Prioritize ideas you're excited about |
| Chasing trends blindly | Trends + personal skills = best combo |

---

## Related Methodologies

- **niche-evaluation:** Niche Evaluation
- **problem-validation:** Problem Validation
- **pain-point-research:** Pain Point Research
- **market-research-tam-sam-som:** Market Research (TAM/SAM/SOM)
- **sdd-workflow-overview:** SDD Workflow Overview

---

## Agent

**faion-idea-generator-agent** helps discover business ideas. Invoke with:
- "Generate ideas based on my skills: [list skills]"
- "Find pain points in [niche]"
- "Score these ideas: [list]"
- "Run a full idea discovery session"

---

*Methodology | Research | Version 1.0*
