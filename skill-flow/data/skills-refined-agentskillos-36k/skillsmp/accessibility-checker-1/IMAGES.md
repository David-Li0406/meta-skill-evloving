# Accessible Images Reference

## Alt Text Principles

1. **Describe the content and function**, not the appearance
2. **Be concise** - usually under 125 characters
3. **Don't start with "Image of..." or "Picture of..."**
4. **Consider context** - same image may need different alt in different contexts

## Image Types

### Informative Images

Images that convey information:

```html
<!-- Describes what the image shows -->
<img src="chart.png" alt="Sales increased 45% from Q3 to Q4"/>

<!-- Logo with company name -->
<img src="logo.png" alt="Acme Corporation"/>

<!-- Photo with relevant content -->
<img src="team.jpg" alt="Our support team: Sarah, Mike, and Alex"/>
```

### Decorative Images

Images that are purely visual decoration:

```html
<!-- Empty alt for decorative images -->
<img src="divider.png" alt=""/>
<img src="background-pattern.png" alt=""/>
```

### Functional Images

Images that trigger actions (buttons, links):

```html
<!-- Describe the action, not the image -->
<a href="/search">
  <img src="magnifying-glass.png" alt="Search"/>
</a>

<button type="submit">
  <img src="arrow-right.png" alt="Submit form"/>
</button>
```

### Complex Images

Images with detailed information:

```html
<!-- Use figure with extended description -->
<figure>
  <img src="flowchart.png" alt="Order processing workflow"/>
  <figcaption>
    Figure 1: Orders flow from submission through validation,
    payment processing, fulfillment, and shipping confirmation.
  </figcaption>
</figure>

<!-- Or link to detailed description -->
<img src="data-visualization.png" alt="2024 revenue breakdown by region"
     aria-describedby="revenue-details"/>
<div id="revenue-details">
  <h3>Revenue Details</h3>
  <ul>
    <li>North America: 45%</li>
    <li>Europe: 30%</li>
    <li>Asia Pacific: 25%</li>
  </ul>
</div>
```

### Images of Text

Avoid when possible; if necessary:

```html
<!-- Include all text in alt -->
<img src="sale-banner.png" alt="Summer Sale: 50% off all items through July 31"/>
```

## Common Mistakes

### Don't Do This

```html
<!-- Too vague -->
<img src="photo.jpg" alt="image"/>
<img src="photo.jpg" alt="photo"/>

<!-- Redundant -->
<img src="dog.jpg" alt="Image of a dog"/>
<img src="sunset.jpg" alt="Picture of sunset"/>

<!-- Missing alt -->
<img src="important-chart.png">

<!-- File name as alt -->
<img src="IMG_2847.jpg" alt="IMG_2847.jpg"/>
```

### Do This Instead

```html
<!-- Descriptive and concise -->
<img src="photo.jpg" alt="Golden retriever playing fetch in the park"/>

<!-- Describes function -->
<img src="sunset.jpg" alt="Sunset over Pacific Ocean from Santa Monica pier"/>

<!-- Always include alt -->
<img src="important-chart.png" alt="Quarterly revenue chart showing 20% growth"/>

<!-- Meaningful description -->
<img src="IMG_2847.jpg" alt="Team celebrating product launch"/>
```

## SVG Images

```html
<!-- Decorative SVG -->
<svg aria-hidden="true">...</svg>

<!-- Informative SVG -->
<svg role="img" aria-label="Company logo">...</svg>

<!-- Complex SVG -->
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Pie Chart</title>
  <desc id="svg-desc">Revenue distribution: 60% products, 40% services</desc>
  ...
</svg>
```

## Icon Fonts / Icon Images

```html
<!-- Icon with visible text -->
<button>
  <img src="save-icon.png" alt=""/>
  Save Document
</button>

<!-- Icon-only button -->
<button aria-label="Save document">
  <img src="save-icon.png" alt=""/>
</button>

<!-- Icon with tooltip -->
<button aria-label="Settings">
  <img src="gear.png" alt=""/>
</button>
```
