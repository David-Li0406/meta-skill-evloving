---
name: financing-presentation
description: "Generate professional HTML financing presentations for startups and businesses. Use when creating investment pitch decks, fundraising materials, or business proposal presentations. Collects project data and generates 12-page HTML slides covering cover, problem and opportunity, solution, product demo, market size, competition, business model, traction, team, financial projections, funding needs, and investment highlights."
---

# Financing Presentation

## Overview

This skill transforms project data into professional HTML financing presentations. It guides users through collecting essential information for each slide section and generates a complete 12-page investment pitch deck in HTML format.

## Workflow

### Step 1: Collect Project Information

Ask the user to provide the following information:

**Required for all presentations:**
- Project name
- One-line slogan
- Founder name and contact information

**For each slide section, collect:**
1. **Problem & Opportunity**: Market pain points, data supporting the problem, timing factors
2. **Solution**: How the product/service solves the problem, technical innovations, competitive advantages
3. **Product Demo**: Product interface, core features, user experience flow, early traction data
4. **Market Size**: TAM/SAM/SOM analysis, growth trends, CAGR, data sources
5. **Competition**: Direct/indirect competitors, competitive positioning, differentiation
6. **Business Model**: Revenue sources, pricing strategy, unit economics (CAC, LTV, LTV/CAC), growth strategy
7. **Traction & Milestones**: Key achievements, growth metrics, partnerships, product iterations
8. **Team**: Core team members, backgrounds, complementary skills, advisors/investors
9. **Financial Projections**: 3-5 year forecasts (revenue, costs, profit, cash flow), assumptions, key ratios
10. **Funding Needs**: Amount sought, valuation (if applicable), use of funds, runway, expected milestones, ROI expectations

### Step 2: Generate HTML Presentation

Use the template from [`assets/financing_template.html`](assets/financing_template.html) to create the presentation.

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read [`assets/financing_template.html`](assets/financing_template.html) completely. **NEVER set range limits when reading this file.**

Replace placeholder content with collected information:
- Page 1 (cover): Project name, slogan, founder contact
- Pages 2-11: Content sections based on collected data
- Page 12 (final): Investment highlights summary

### Step 3: Review and Refine

Ensure the presentation:
- Has clear, compelling messaging
- Uses specific data points and metrics
- Maintains professional formatting
- Flows logically from problem to solution to opportunity

## Slide Structure

The presentation follows this 12-page structure:

| Page | Type | Title | Key Content |
|------|------|-------|-------------|
| 1 | cover | [项目名称]融资演示 | Slogan, founder contact |
| 2 | content | 问题与机会 | Market pain points, timing, data support |
| 3 | content | 解决方案 | Product/service, innovation, competitive advantage |
| 4 | content | 产品展示 | Interface, features, user experience, traction |
| 5 | content | 市场规模 | TAM/SAM/SOM, growth trends, CAGR |
| 6 | content | 竞争格局 | Competitor analysis, positioning, differentiation |
| 7 | content | 商业模式 | Revenue, pricing, unit economics, growth |
| 8 | content | 牵引力与里程碑 | Achievements, metrics, partnerships |
| 9 | content | 团队介绍 | Team members, backgrounds, complementary skills |
| 10 | content | 财务预测 | 3-5 year forecasts, assumptions, ratios |
| 11 | content | 融资需求 | Amount, use of funds, runway, ROI |
| 12 | final | 投资亮点总结 | 3-5 key points, call to action |

## Best Practices

**Content Quality:**
- Use specific numbers and data points (e.g., "市场规模达100亿元" not "市场规模很大")
- Include credible data sources when referencing market data
- Show, don't tell (use examples, case studies, testimonials)
- Be concise and focused on key messages

**Visual Design:**
- Maintain consistent styling throughout all slides
- Use professional color schemes and typography
- Ensure text is readable and well-organized
- Include visual elements (charts, diagrams) where appropriate

**Storytelling:**
- Create a compelling narrative arc from problem to opportunity
- Emphasize unique value proposition
- Build credibility with data and traction
- End with strong call to action

## Common Traps

**NEVER do these things:**
- Use vague or unsubstantiated claims
- Overpromise without evidence
- Ignore or misrepresent competitors
- Use generic templates without customization
- Include irrelevant information that dilutes the message

**AVOID these mistakes:**
- Missing key data points (market size, traction, team)
- Inconsistent formatting across slides
- Overcrowding slides with too much text
- Failing to explain the "why" behind the "what"
- Not tailoring the presentation to the audience

## Resources

### scripts/
- [`generate_presentation.py`](scripts/generate_presentation.py) - Script to generate HTML presentation from JSON data

### assets/
- [`financing_template.html`](assets/financing_template.html) - HTML template for the presentation

### references/
- [`financing_guide.md`](references/financing_guide.md) - Detailed guide on creating effective financing presentations
