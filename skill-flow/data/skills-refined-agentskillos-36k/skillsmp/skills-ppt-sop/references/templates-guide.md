# Templates Guide

Complete guide for using HTML presentation templates.

## Template Overview

All templates follow these standards:
- Canvas size: 960×540px
- CSS variables from design system
- Safe margins: 40px
- Single-file HTML structure

## 1. Cover Page (`cover.html`)

### Purpose
First slide of presentation with title and subtitle.

### Key Features
- Gradient background (purple to pink)
- Centered title layout
- Large typography (48px title, 32px subtitle)
- Text shadow for readability

### Usage Pattern

```html
<div class="title-section">
  <h2>主标题</h2>
  <h3>副标题</h3>
</div>
```

### Customization Points
- `h2`: Main title (48px, bold, white)
- `h3`: Subtitle (32px, white with 95% opacity)
- Background gradient: Modify `.content` background property

### When to Use
- Always as first slide
- For presentation title and presenter info
- Optional: Add date or company logo

### Common Mistakes
- Making title too long (max 2 lines)
- Using small font sizes
- Removing gradient background

## 2. Table of Contents (`toc.html`)

### Purpose
List presentation sections with numbering.

### Key Features
- Numbered list (01, 02, 03...)
- 60px row height for consistency
- Accent color for numbers
- Simple border separators

### Usage Pattern

```html
<ul class="toc-list">
  <li class="toc-item">
    <span class="toc-number">01</span>
    <span class="toc-text">第一章标题</span>
  </li>
</ul>
```

### Customization Points
- `toc-number`: Section number (32px, accent color)
- `toc-text`: Section title (24px, dark gray)
- Add/remove `toc-item` elements

### When to Use
- After cover page
- For presentations with 4-6 sections
- Not needed for single-page presentations

### Common Mistakes
- More than 6 items (split into multiple TOC slides)
- Inconsistent numbering format
- Too long section titles (max 20 characters)

## 3. Content Page (`base-template.html`)

### Purpose
Main content slides with flexible layout.

### Key Features
- 12-column grid system
- Card-based layout
- Support for multiple content types
- Left/right column options

### Grid System

```css
.col-4 { grid-column: span 4; }  /* 33% width */
.col-6 { grid-column: span 6; }  /* 50% width */
.col-8 { grid-column: span 8; }  /* 67% width */
.col-12 { grid-column: span 12; } /* 100% width */
```

### Usage Patterns

**Two-column layout (8+4):**
```html
<div class="col-8">
  <div class="card">
    <h2>Section Title</h2>
    <p>Content...</p>
  </div>
</div>
<div class="col-4">
  <div class="card gray">
    <h3>Key Metric</h3>
    <div class="num">123</div>
  </div>
</div>
```

**Full-width layout:**
```html
<div class="col-12">
  <div class="card">
    <h2>Full Width Title</h2>
    <p>Content...</p>
  </div>
</div>
```

### Customization Points
- Card background: `.card` (white) or `.card.gray` (light gray)
- Typography: `h2` (32px, accent), `h3` (24px, bold), `p` (20px)
- Grid columns: Mix `.col-4`, `.col-6`, `.col-8`, `.col-12`

### When to Use
- For all content slides
- When integrating components (tables, charts)
- For mixed content layouts

### Common Mistakes
- Exceeding 12 columns total
- Using too many cards (max 3-4 per slide)
- Text overflow in cards

## 4. Summary Page (`summary.html`)

### Purpose
Display key metrics and takeaways.

### Key Features
- 3-column layout
- Large metric numbers (48px)
- Descriptive labels below numbers
- Centered text

### Usage Pattern

```html
<div class="metric-card">
  <div class="metric-number">1,234</div>
  <div class="metric-description">指标一说明</div>
</div>
```

### Customization Points
- `metric-number`: Large value (48px, accent color, bold)
- `metric-description`: Label (20px, gray)
- Add/remove `metric-card` elements

### When to Use
- Near end of presentation
- For 3-5 key metrics
- To summarize data from content slides

### Common Mistakes
- More than 5 metrics (split into multiple slides)
- Numbers without context
- Inconsistent formatting (mix units, decimals)

## 5. End Page (`end.html`)

### Purpose
Thank you slide with contact information.

### Key Features
- Centered layout
- Large thank you message
- Optional contact details
- Clean, minimal design

### Usage Pattern

```html
<div class="end-content">
  <h2>谢谢</h2>
  <p>联系方式</p>
</div>
```

### Customization Points
- Main message: `h2` (large, centered)
- Contact info: `p` (20px, gray)
- Optional: Add email, phone, website

### When to Use
- Always as last slide
- For presentations requiring follow-up
- Optional for internal presentations

### Common Mistakes
- Too much text (keep minimal)
- Missing contact info when needed
- Inconsistent with presentation style

## 6. Navigation Template (`navigation-template.html`)

### Purpose
Combine multiple slides into single HTML file with navigation.

### Key Features
- Slide switching with JavaScript
- Previous/Next buttons
- Keyboard navigation (arrow keys)
- Page indicator
- Responsive scaling

### Structure

```html
<div class="presentation-wrapper">
  <div class="slide active" id="slide-1">
    <!-- Slide 1 content -->
  </div>
  <div class="slide" id="slide-2">
    <!-- Slide 2 content -->
  </div>
  <div class="nav-controls">
    <!-- Navigation buttons -->
  </div>
</div>
```

### JavaScript Logic

```javascript
let currentSlide = 1;
const totalSlides = document.querySelectorAll('.slide').length;

function showSlide(n) {
  // Update slide visibility
  // Update page indicator
  // Enable/disable buttons
}

function nextSlide() {
  currentSlide++;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide--;
  showSlide(currentSlide);
}
```

### Customization Points
- Add/remove `<div class="slide">` elements
- Update `totalSlides` in JavaScript
- Modify button text (Chinese/English)

### When to Use
- For complete presentations
- Default output format
- When navigation is needed

### Common Mistakes
- Forgetting to update `totalSlides`
- Not adding `.active` class to first slide
- Breaking JavaScript with duplicate IDs

## Template Integration Workflow

1. **Choose base template**
   - Single file: Start with `navigation-template.html`
   - Multiple files: Use individual templates

2. **Copy slide structure**
   - Extract `<div class="slide-container">` from template
   - Insert into appropriate position

3. **Customize content**
   - Replace placeholder text
   - Add components from `components/` directory
   - Adjust grid layout

4. **Verify consistency**
   - Check CSS variables
   - Ensure canvas size (960×540px)
   - Test navigation (if applicable)

## Common Template Issues

### Layout Breaking
**Symptom**: Content overflows or misaligned
**Cause**: Exceeding 12-column grid or ignoring safe margins
**Solution**: Use `.col-*` classes correctly, keep 40px margins

### Styling Inconsistency
**Symptom**: Different fonts or colors across slides
**Cause**: Missing CSS variables or custom styles
**Solution**: Always define CSS variables, use design system colors

### Navigation Not Working
**Symptom**: Buttons don't switch slides
**Cause**: Incorrect slide IDs or JavaScript errors
**Solution**: Ensure unique IDs, check `totalSlides` value

## Best Practices

1. **Start with templates**: Never create from scratch
2. **Keep it simple**: Don't over-customize
3. **Test early**: Verify layout after each change
4. **Use components**: Leverage `components/` directory
5. **Maintain consistency**: Follow design system strictly
