# Best Practices

This guide provides best practices for creating professional McKinsey-style HTML presentations.

## Content Principles

### 1. Content Preservation

**DO**:
- Preserve all original text exactly as written
- Maintain all numerical data points
- Keep all conclusions and recommendations word-for-word
- Respect original document structure and hierarchy

**DON'T**:
- Summarize or paraphrase content
- Add fabricated data or insights
- Modify conclusions or recommendations
- Interpret or add meaning to original text

### 2. Information Hierarchy

**DO**:
- Start with executive summary (top 3-5 points)
- Group related content together
- Use consistent ordering (importance, chronology, or logical flow)
- Maintain visual hierarchy (title → subtitle → body)

**DON'T**:
- Bury key insights in detail slides
- Mix unrelated topics on same slide
- Use random or inconsistent ordering
- Flattened hierarchy (everything same size)

### 3. Data Visualization

**DO**:
- Choose chart type based on data nature:
  - Bar chart: Category comparisons
  - Line chart: Trends over time
  - Pie chart: Percentage breakdowns
  - Table: Detailed multi-metric data
- Use consistent color palette
- Keep charts simple and readable
- Add clear labels and captions

**DON'T**:
- Use wrong chart type for data
- Clutter charts with too many data points
- Use colors outside the defined palette
- Remove labels or make them hard to read
- Create unnecessary or decorative charts

## Design Principles

### 1. Color Usage

**DO**:
- Strict adherence to McKinsey palette:
  - Primary background: #FFFFFF
  - Header: #000000
  - Accent: #F85d42
  - Secondary: #74788d
  - Charts: #556EE6, #34c38f, #50a5f1, #f1b44c
- Use accent color sparingly for emphasis
- Maintain color consistency across all slides
- Ensure high contrast for readability

**DON'T**:
- Add custom colors or variations
- Use purple gradients or AI-generated palettes
- Apply colors randomly
- Use low contrast combinations
- Overuse accent color (loses impact)

### 2. Typography

**DO**:
- Use defined font sizes:
  - Title: 64px (bold, black)
  - Subtitle: 36px (bold, accent color)
  - Section header: 28px (bold, black)
  - Body text: 18px (regular, dark gray)
  - Chart labels: 14px (clear, readable)
- Maintain consistent font family (system fonts)
- Use bold for emphasis, not styling
- Ensure line height 1.6-1.8 for readability

**DON'T**:
- Use inconsistent font sizes
- Mix multiple font families
- Use italic or decorative fonts
- Use underlining for emphasis
- Set line height too tight (<1.4) or loose (>2.0)

### 3. Layout & Spacing

**DO**:
- Use generous white space (40-60px margins)
- Maintain consistent spacing:
  - Between elements: 20-30px
  - Between sections: 40-60px
  - Within cards: 20-30px
- Align all elements to grid
- Balance visual weight across slide

**DON'T**:
- Crowd elements together
- Use inconsistent spacing
- Create unaligned layouts
- Leave large empty areas without purpose
- Create visually unbalanced slides

### 4. Visual Elements

**DO**:
- Use subtle shadows for depth (0-2px, 0-4px)
- Add minimal borders for separation
- Use colored borders for emphasis (4px accent color)
- Keep chart design clean and minimal
- Ensure all elements serve purpose

**DON'T**:
- Use heavy or multiple shadows
- Add unnecessary borders
- Use decorative elements without purpose
- Create complex or cluttered charts
- Add clipart, icons, or decorative graphics

## Slide Design Patterns

### Title Slide

**Purpose**: Introduce presentation with maximum impact

**Pattern**:
```html
<div class="title-slide">
  <h1 class="title">Main Title</h1>
  <h2 class="subtitle">Context or Subtitle</h2>
  <p class="date">Date</p>
</div>
```

**Best Practices**:
- Keep text minimal and bold
- Use large, impactful title (64px)
- Add context through subtitle
- Center align for focus
- No charts or data

### Executive Summary

**Purpose**: Present top 3-5 conclusions or key takeaways

**Pattern**:
```html
<div class="header-bar">
  <h1 class="slide-title">Executive Summary</h1>
</div>
<div class="slide-content">
  <ul class="key-points">
    <li class="key-point">✓ Conclusion 1</li>
    <li class="key-point">✓ Conclusion 2</li>
    <li class="key-point">✓ Conclusion 3</li>
  </ul>
</div>
```

**Best Practices**:
- Limit to 3-5 key points
- Most important first
- Use checkmarks for visual cue
- Bold key metrics or numbers
- Clear, concise statements

### Data Slide

**Purpose**: Present quantitative data with analysis

**Pattern**:
```html
<div class="slide-content two-column">
  <div class="column chart-container">
    <canvas id="chart1"></canvas>
    <p class="chart-caption">Chart Description</p>
  </div>
  <div class="column">
    <h3 class="section-header">Key Insights</h3>
    <ul class="bullet-points">
      <li>Insight 1</li>
      <li>Insight 2</li>
      <li>Insight 3</li>
    </ul>
  </div>
</div>
```

**Best Practices**:
- Chart on left (60%), insights on right (40%)
- 3-5 insights maximum
- Relate insights directly to chart data
- Clear chart caption
- Simple, readable chart design

### Detailed Findings

**Purpose**: Present supporting analysis and evidence

**Pattern**:
```html
<div class="slide-content">
  <h3 class="section-header">Finding Category 1</h3>
  <p class="body-text">Detailed explanation...</p>

  <div class="data-table-container">
    <table class="data-table">
      <!-- table content -->
    </table>
  </div>
</div>
```

**Best Practices**:
- 3-5 paragraphs maximum
- Clear section headers
- Use tables for detailed data
- Moderate text length (100-150 words)
- Avoid walls of text

### Conclusion Slide

**Purpose**: Present final conclusions and recommendations

**Pattern**:
```html
<div class="conclusions-grid">
  <div class="conclusion-card">
    <h3 class="card-title">Conclusion 1</h3>
    <p class="card-text">Text...</p>
  </div>
</div>
<div class="recommendations-box">
  <h3 class="section-header accent-text">Key Recommendations</h3>
  <ol class="numbered-list">
    <li>Recommendation 1</li>
  </ol>
</div>
```

**Best Practices**:
- 3-6 conclusion cards in grid
- Card accent color for visual emphasis
- Recommendations in separate box
- Numbered recommendations for action
- Clear, actionable items

## Anti-Patterns to Avoid

### Content Anti-Patterns

**AI-Generated Style**:
- Purple gradients on white backgrounds
- All corners rounded to 8px
- Cookie-cutter card layouts
- Generic "professional" templates without personality
- Overused fonts (Inter, Roboto, Arial)

**Content Destruction**:
- Summarizing instead of preserving
- Removing "minor" details
- Rephrasing to "improve" readability
- Combining separate points
- Adding clarifying text

### Design Anti-Patterns

**Visual Clutter**:
- Too many elements on one slide
- Excessive colors or accents
- Multiple charts on single slide
- Decorative icons or graphics
- Unnecessary animations

**Poor Hierarchy**:
- All elements same size
- No clear focal point
- Random ordering
- Mixed font weights
- Inconsistent styling

**Accessibility Issues**:
- Low contrast text (<4.5:1)
- Small font sizes (<14px)
- Unclear color differentiation
- Missing chart labels
- Poor keyboard navigation

## Quality Checklist

Before finalizing presentation, verify:

**Content**:
- [ ] All original content preserved
- [ ] No fabricated data or insights
- [ ] All conclusions present
- [ ] Clear information hierarchy
- [ ] Logical flow and organization

**Design**:
- [ ] Strict color palette adherence
- [ ] Consistent typography
- [ ] Generous white space
- [ ] Aligned, balanced layouts
- [ ] Professional, McKinsey-style quality

**Functionality**:
- [ ] Navigation works (buttons, keyboard)
- [ ] All charts render correctly
- [ ] Responsive design tested
- [ ] Fullscreen mode works
- [ ] No console errors

**Accessibility**:
- [ ] High contrast text
- [ ] Readable font sizes
- [ ] Clear chart labels
- [ ] Keyboard navigation
- [ ] Screen reader compatible

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Summarizing content | Loss of detail and meaning | Preserve exact text |
| Too many slides | Loss of focus | Combine related content |
| Wrong chart type | Confusion | Match chart to data nature |
| Inconsistent colors | Unprofessional look | Strict palette adherence |
| Poor spacing | Cluttered look | Generous white space |
| Missing conclusions | Incomplete presentation | Ensure all conclusions included |
| Low contrast | Unreadable text | Ensure 4.5:1 contrast ratio |
| Cluttered slides | Confusing message | Simplify and focus |
