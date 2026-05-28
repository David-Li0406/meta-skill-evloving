---
id: survey-design
name: "Survey Design"
domain: RES
skill: faion-researcher
category: "research"
---

# Survey Design

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #survey, #quantitative |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Surveys often produce misleading or useless data. Common issues:
- Leading questions that bias responses
- Too long (abandonment, random clicking)
- Wrong distribution (sample bias)
- Asking hypotheticals instead of facts
- No clear research objective

**The root cause:** Designing surveys without methodology training.

---

## Framework

### When to Use Surveys

**Good for:**
- Quantifying known patterns from interviews
- Measuring preferences across a population
- Gathering demographic data
- Tracking satisfaction over time

**Not good for:**
- Discovering new problems (use interviews)
- Deep understanding of motivations
- Predicting future behavior

**Rule:** Do 10+ interviews before creating a survey. Surveys quantify; interviews discover.

### Survey Design Process

#### Step 1: Define Research Objective

**Template:**
```
We want to learn: [Specific question]
To inform: [Decision we'll make]
From: [Target audience]
With sample size: [N respondents]
```

**Example:**
```
We want to learn: What price points feel acceptable
To inform: Our pricing tier structure
From: Freelance designers in the US
With sample size: 100+ respondents
```

#### Step 2: Choose Question Types

| Type | When to Use | Example |
|------|-------------|---------|
| Multiple choice | Discrete options | "How often do you...?" |
| Rating scale | Intensity/agreement | "Rate 1-5" |
| Ranking | Priority order | "Rank these features" |
| Open-ended | Qualitative insight | "What else should we know?" |
| Matrix | Multiple items, same scale | Satisfaction across features |
| NPS | Loyalty measure | "How likely to recommend?" |

**Scale best practices:**

| Scale | Use Case |
|-------|----------|
| 5-point | General satisfaction |
| 7-point | Nuanced attitudes |
| 10-point | NPS, detailed ratings |
| Binary | Clear yes/no decisions |

#### Step 3: Write Questions

**Good questions:**
- Specific and concrete
- One concept per question
- Neutral wording
- Clear response options
- Answerable by respondent

**Bad questions:**

| Bad | Why | Better |
|-----|-----|--------|
| "Do you like our product?" | Vague, leading | "How would you rate your experience?" |
| "How satisfied and engaged are you?" | Double-barreled | Split into two questions |
| "Don't you think X is better?" | Leading | "Which do you prefer, X or Y?" |
| "How often will you use this?" | Hypothetical | "How often have you used similar tools?" |

#### Step 4: Structure the Survey

**Flow:**
1. **Screener** (1-2 questions) - Qualify respondents
2. **Easy questions** (2-3) - Build momentum
3. **Core questions** (5-10) - Main research
4. **Demographics** (3-5) - Segmentation
5. **Open-ended** (1-2) - Additional insights

**Length guidelines:**

| Length | Completion Rate | Use Case |
|--------|----------------|----------|
| 1-3 min | 80%+ | Quick pulse |
| 5-7 min | 60-70% | Standard research |
| 10-15 min | 40-50% | Deep research |
| 15+ min | <30% | Avoid unless incentivized |

#### Step 5: Test and Distribute

**Testing:**
- Pilot with 5-10 people
- Measure time to complete
- Ask about confusing questions
- Check for technical issues

**Distribution channels:**

| Channel | Pros | Cons |
|---------|------|------|
| Email list | Qualified, engaged | Biased to current users |
| Social media | Broad reach | Self-selection |
| Paid panels | Fast, targeted | Expensive, quality varies |
| In-product | High completion | Only active users |
| Communities | Engaged, specific | May be small |

#### Step 6: Analyze Results

**Quantitative:**
- Response distributions
- Cross-tabulations
- Statistical significance

**Qualitative (open-ended):**
- Theme coding
- Quote extraction
- Pattern identification

---

## Templates

### Survey Design Document

```markdown
## Survey: [Title]

### Research Objective
**Question:** [What we want to learn]
**Decision:** [What this informs]
**Audience:** [Who will take it]
**Target N:** [Sample size needed]

### Screener Questions
1. [Question to qualify]
   - [Option A] → Continue
   - [Option B] → End survey

### Core Questions

#### Q1: [Topic]
[Question text]
- [ ] Option A
- [ ] Option B
- [ ] Option C
Type: [Multiple choice/Scale/etc.]

#### Q2: [Topic]
...

### Demographics
- Role/title
- Company size
- Geography
- Other relevant segments

### Open-Ended
"Is there anything else you'd like to share about [topic]?"

### Distribution Plan
- **Channel:** [Where]
- **Duration:** [How long]
- **Incentive:** [If any]

### Analysis Plan
- [Metric 1]: Compare across [segment]
- [Metric 2]: Correlate with [factor]
```

### Question Bank by Research Type

```markdown
## Pricing Research Questions

Rate agreement (1-5):
- "The current price is fair for what I get"
- "I would pay more for additional features"

Van Westendorp:
- "At what price would this be so expensive you wouldn't consider it?"
- "At what price would this be expensive but worth considering?"
- "At what price would this be a good deal?"
- "At what price would you question the quality?"

---

## Satisfaction Research Questions

Overall satisfaction (1-5):
"How satisfied are you with [product]?"

NPS (0-10):
"How likely are you to recommend [product] to a colleague?"

Feature satisfaction matrix:
| Feature | Very Dissatisfied | Dissatisfied | Neutral | Satisfied | Very Satisfied |
|---------|-------------------|--------------|---------|-----------|----------------|
| Speed | | | | | |
| Ease of use | | | | | |

---

## Feature Prioritization Questions

Ranking:
"Rank these features by importance to you (1 = most important)"

MaxDiff:
"Of these 4 features, which is MOST important? Which is LEAST important?"

Importance vs Satisfaction matrix:
[Feature] - Importance (1-5) / Satisfaction (1-5)
```

---

## Examples

### Example 1: Pricing Survey for SaaS

**Objective:** Determine acceptable price range for new tier

**Questions:**
1. Screener: "Do you currently use project management software?" (Yes → continue)
2. Current spend: "How much do you pay monthly for PM tools?"
3. Van Westendorp: 4 price sensitivity questions
4. Feature value: "Which features would you pay extra for?"
5. Open: "What would make a $49/mo plan worth it?"

**Results (n=150):**
- Optimal price: $29-39/month
- "Must have" features: Integrations, mobile app
- Insight: Annual discount expected (85% want it)

### Example 2: Feature Prioritization Survey

**Objective:** Decide next quarter's roadmap

**Questions:**
1. MaxDiff: 3 rounds comparing 4 features each
2. Satisfaction with current features (matrix)
3. Open: "What's the #1 thing you wish we'd build?"

**Results (n=200):**
- Top priority: API access (38% first choice)
- Highest gap: Reporting (low satisfaction, high importance)
- Surprise: Mobile app less important than assumed

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Leading questions | Use neutral wording |
| Double-barreled | One concept per question |
| Too long | Keep under 7 minutes |
| No screener | Qualify respondents first |
| Only closed questions | Add 1-2 open-ended |
| Small sample | Get 100+ for quantitative claims |
| No pilot | Test with 5-10 people first |
| Ignoring abandonment | Check where people drop off |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **pricing-research:** Pricing Research
- **user-interviews:** User Interviews
- **user-research-methods:** User Research Methods
- **ab-testing-framework:** A/B Testing Framework

---

## Agent

**faion-market-researcher-agent** helps design surveys. Invoke with:
- "Create a survey for [research goal]"
- "Review my survey questions: [questions]"
- "How should I distribute this survey?"
- "Analyze these survey results: [data]"

---

*Methodology | Research | Version 1.0*
