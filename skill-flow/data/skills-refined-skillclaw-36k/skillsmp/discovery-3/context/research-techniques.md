# Discovery Research Techniques

## Interview Frameworks

### Jobs-to-be-Done (JTBD) Framework

Focus on understanding what "job" the user is trying to accomplish.

**Key Questions**:
- When you [situation], what are you trying to accomplish?
- What are all the steps you go through to [accomplish the job]?
- What's frustrating or time-consuming about the current process?
- How do you know when you've done the job successfully?

### Five Whys Technique

Dig deeper into root causes by asking "why" repeatedly.

**Example**:
- Problem: Users abandon the checkout process
- Why? The form is too long
- Why? We ask for too much information
- Why? We need it for shipping and billing
- Why? Systems aren't integrated
- Why? (Root cause emerges)

### Problem-Solution Fit Validation

Test whether the solution addresses the actual problem.

**Framework**:
1. State the problem hypothesis
2. Present the proposed solution
3. Ask: "Does this solve your problem?"
4. If no: "What would solve it?"
5. If yes: "How would you use this?"

## Competitive Analysis Frameworks

### Feature-Benefit Matrix

| Feature | Competitor A | Competitor B | Our Vision | User Benefit |
|---------|-------------|-------------|------------|-------------|
| [Feature] | [Implementation] | [Implementation] | [Our approach] | [Why it matters] |

### SWOT Analysis Per Competitor

**Strengths**: What they do well
**Weaknesses**: Their gaps and limitations
**Opportunities**: Where we can differentiate
**Threats**: What they could do to compete with us

### Porter's Five Forces (for market assessment)

1. **Threat of New Entrants**: How easy is market entry?
2. **Bargaining Power of Suppliers**: Dependency on suppliers/vendors
3. **Bargaining Power of Buyers**: Customer leverage
4. **Threat of Substitutes**: Alternative solutions
5. **Industry Rivalry**: Competitive intensity

## Market Sizing Approaches

### Top-Down Approach

Start with total market, narrow down:
```
Total Market Size (TAM)
  ↓ (filter by geography, segment)
Serviceable Available Market (SAM)
  ↓ (filter by realistic capture)
Serviceable Obtainable Market (SOM)
```

### Bottom-Up Approach

Start with unit economics, scale up:
```
Average Revenue Per User (ARPU)
  × Target Customer Count
  = Market Opportunity
```

### Value-Theory Approach

Estimate value created:
```
Time/Cost Saved Per User
  × Number of Users
  = Total Value Created
  × Capture Rate (typically 10-20%)
  = Revenue Opportunity
```

## Stakeholder Mapping

### Power-Interest Grid

```
High Power, High Interest → Key Players (manage closely)
High Power, Low Interest → Keep Satisfied (keep informed)
Low Power, High Interest → Keep Informed (show consideration)
Low Power, Low Interest → Monitor (minimal effort)
```

### Influence Map

Identify:
- Decision makers (final authority)
- Influencers (shape decisions)
- Users (day-to-day usage)
- Blockers (could derail project)

## Requirements Prioritization

### MoSCoW Method

- **Must Have**: Non-negotiable, MVP blockers
- **Should Have**: Important but not critical
- **Could Have**: Nice to have if time permits
- **Won't Have**: Explicitly out of scope

### Kano Model

- **Basic Needs**: Expected, dissatisfiers if missing
- **Performance Needs**: More is better
- **Excitement Needs**: Delighters, unexpected value

### Value vs Effort Matrix

```
High Value, Low Effort → Do First (quick wins)
High Value, High Effort → Do Next (strategic)
Low Value, Low Effort → Do Later (fill time)
Low Value, High Effort → Don't Do (waste)
```

## Survey Design Best Practices

### Question Types

**Open-Ended**: "What frustrates you about [current solution]?"
- Use for: Discovery, unexpected insights
- Caution: Harder to analyze at scale

**Closed-Ended**: "How often do you [perform task]?" (Daily/Weekly/Monthly/Rarely)
- Use for: Quantifiable data, prioritization
- Caution: May miss nuance

**Likert Scale**: "Rate your agreement: [statement]" (1-5)
- Use for: Measuring attitudes, satisfaction
- Caution: Cultural response bias

### Survey Structure

1. **Introduction**: Purpose, time estimate, privacy
2. **Screening**: Qualify respondents
3. **Core Questions**: Main research questions
4. **Demographics**: Background information
5. **Open Feedback**: Anything we missed?

### Avoiding Bias

- **Leading Questions**: ❌ "Don't you think [solution] would be helpful?"
- **Neutral Questions**: ✓ "How helpful would [solution] be?"

- **Double-Barreled**: ❌ "Is the product fast and easy to use?"
- **Single Focus**: ✓ "Is the product fast?" + "Is the product easy to use?"

## Data Source References

### Market Research Sources

- Industry reports: Gartner, Forrester, IDC
- Government data: Census, BLS, trade organizations
- Public company filings: 10-K, investor presentations
- Academic research: Google Scholar, industry journals

### Competitive Intelligence Sources

- Company websites and documentation
- Product Hunt, G2, Capterra reviews
- Social media and community discussions
- News articles and press releases
- Patent databases

### Technology Research Sources

- Official documentation
- GitHub repositories
- Stack Overflow trends
- Developer surveys (Stack Overflow, JetBrains)
- Technology radar (ThoughtWorks)

## Analysis Documentation Standards

### Citing Sources

Always include:
- Source name
- URL (if online)
- Date accessed
- Relevant excerpt or data point

Example:
```markdown
Market size: $50B by 2025 (Source: Gartner "Enterprise Software Market Forecast",
accessed Dec 2025, https://...)
```

### Confidence Levels

Indicate certainty:
- **High Confidence**: Multiple reliable sources, recent data
- **Medium Confidence**: Single source, or older data
- **Low Confidence**: Estimation, limited data available

### Assumptions and Limitations

Document:
- Data quality concerns
- Missing information
- Extrapolations made
- Time constraints on research
