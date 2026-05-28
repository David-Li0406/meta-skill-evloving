# Template Usage Guide

Comprehensive guide for using the 4 pre-built McKinsey-style slide templates.

## Template Overview

| Template | File | Slide Position | When to Use |
|----------|------|----------------|-------------|
| Cover | `cover-slide-template.html` | #1 (always) | First slide of any presentation |
| TOC | `toc-slide-template.html` | #2 (optional) | Presentations with 10+ slides |
| Content | `content-slide-template.html` | #3 to #N-1 | All middle slides |
| End | `end-slide-template.html` | #N (always) | Final slide |

## 1. Cover Slide Template

**Location**: `templates/cover-slide-template.html`

**Purpose**: First slide with title and metadata

**Structure**:
```html
<div class="slide title-slide active" data-slide="1">
    <h1 class="main-title">{presentation_title}</h1>
    <div class="decorative-line"></div>
    <p class="subtitle">{subtitle}</p>
    <div class="meta-info">
        <div class="meta-item">
            <div class="meta-label">汇报人</div>
            <div class="meta-value">{presenter_name}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">日期</div>
            <div class="meta-value">{date}</div>
        </div>
    </div>
</div>
```

**Customization Points**:
- `.main-title`: Main presentation title (64px, white, bold)
- `.subtitle`: Subtitle or tagline (36px, white)
- `.meta-item`: Add/remove metadata fields as needed

**Design Features**:
- Gradient background (deep blue to orange)
- Fade-in animations
- Centered layout

## 2. Table of Contents Template

**Location**: `templates/toc-slide-template.html`

**Purpose**: Navigation slide showing presentation structure

**When to Use**: Only for presentations with 10+ slides

**Structure**:
```html
<div class="slide toc-slide" data-slide="2">
    <div class="toc-header">
        <h1 class="toc-title">目录</h1>
        <p class="toc-subtitle">Table of Contents</p>
    </div>
    <div class="toc-container">
        <a href="#section1" class="toc-section" onclick="jumpToSlide(3); return false;">
            <div class="toc-number">1</div>
            <div class="toc-section-title">{section_title}</div>
            <div class="toc-section-subtitle">{section_description}</div>
        </a>
        <!-- Repeat for each section -->
    </div>
    <div class="toc-footer">
        <div class="toc-meta">
            <span>📊 共 {total_slides} 页</span>
            <span>⏱️ 预计 {estimated_time} 分钟</span>
        </div>
    </div>
</div>
```

**Customization Points**:
- `.toc-section`: One block per major section
- `onclick="jumpToSlide(X)"`: Set jump target slide number
- `.toc-meta`: Update total slides and time estimaDesign Features**:
- Two-column grid layout
- Clickable sections with hover effects
- Quick navigation

## 3. Content Slide Template

**Location**: `templates/content-slide-template.html`

**Purpose**: Universal template for all content slides

**Available Components**:

### Text Components
- `.slide-title`: Main slide title (48-64px)
- `.slide-subtitle`: Subtix)
- `.section-heading`: Section heading (24px)
- `.text-content`: Body text (16-20px)
- `.key-point`: Emphasized point (20px bold)

### List Components
- `.bullet-list`: Unordered list with McKinsey bullets
- `.numbered-list`: Ordered list with numbering

### Layout Components
- `.two-column`: Two-column grid layout
  - `.column`: Column child (50% width each)
- `.full-width`: Full-width container

### ChComponents
- `.chart-container`: Container for Chart.js charts
  - `<canvas id="chartX">`: Canvas element for chart

### Emphasis Components
- `.emphasis-container`: Grid of emphasis boxes
- `.emphasis-box`: Individual emphasis box
- `.conclusions-grid`: Grid for conclusions
- `.conclusion-card`: Individual conclusion card
- `.info-box`: ion box with icon
- `.highlight-box`: Highlighted content box

### Flow Components
- `.flow-container`: Container for flow diagrams
- `.flow-step`: Individual flow step
- `.flow-number`: Step number circle
- `.flow-title`: Step title
- `.flow-description`: Step description

### Table Components
- `.data-table`: Professional data table
  - `<thead>`: Table header
  - `<tbody>`: Table body

**Example Layouts**:

**Two-column with chart**:
```html
<div class="slide" data-slide="3">
    <h1 class="slide-title">{title}</h1>
    <div class="two-column">
        <div class="column">
            <p class="text-content">{text}</p>
        </div>
        <div class="column">
            <div class="chart-container">
                <canvas id="chart3"></canvas>
            </div>
        </div>
    </div>
</div>
```

**Flow diagram**:
```html
<div class="slide" data-slide="4">
    <h1 class="slide-title">{title}</h1>
    <div class="flow-container">
        <div class="flow-step">
            <div class="flow-number">1</div>
            <div class="flow-content">
                <div class="flow-title">{step_title}</div>
                <div class="flow-description">{step_description}</div>
            </div>
        </div>
        <!-- Repeat for each step -->
    </div>
</div>
```

**Emphasis boxes**:
```html
<div class="slide" data-slide="5">
    <h1 class="slide-title">{title}</h1>
    <div class="emphasis-container">
        <div class="emphasis-box">
            <div class="emphasis-number">1</div>
            <div class="emphasis-title">{point_title}</div>
            <div class="emphasis-content">{point_content}</div>
        </div>
        <!-- Repeat for each point -->
    </div>
</div>
```

## 4. End Slide Template

**Location**: `templates/end-slide-template.html`

**Purpose**: Final thank you/closing slide

**Structure**:
```html
<div class="slide end-slide" data-slide="{total_slides}">
    <div class="decorative-icon">🎉</div>
    <h1 class="thank-you">感谢聆听！</h1>
    <p class="main-message">感谢您的时间和关注</p>

    <div class="contact-info">
        <div class="contact-title">联系方式</div>
        <div class="contact-details">
            📧 Email: {email}<br>
            📱 电话: {phone}
        </div>
    </div>

    <div class="company-info">
        <div class="company-logo">LOGO</div>
        <div class="company-name">{company_name}</div>
    </div>
</div>
```

**Customization Points**:
- `.thank-you`: Thank you message (可改为"谢谢"、"Q&A"等)
- `.contact-details`: Contact information
- `.company-name`: Company name
- `.company-logo`: Logo or company identifier

**Design Features**:
- Gradient background (orange to deep blue)
- Large thank you text (72px)
- Glass-effect contact card
- Fade-in animations

## Template Assembly Workflow

**Step 1**: Copy cover slide structure → Slide #1
**Step 2**: Copy TOC slide structure → Slide #2 (if 10+ slides)
**Step 3**: Copy content slide structure → Slides #3 to #N-1
**Step 4**: Copy end slide structure → Final slide

**Step 5**: Combine into single HTML file:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{presentation_title}</title>
    <style>
        /* Copy CSS from any template (all have same McKinsey CSS) */
    </style>
</head>
<body>
    <nav class="navbar">...</nav>
    <div class="presentation-container">
        <!-- All slides here -->
    </div>
    <button class="fullscreen-btn">全屏 ⛶</button>
    <script>
        // Copy JavaScript from any template
        // Initialize charts
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</body>
</html>
```

## Chart.js Integration

**For each chart in content slides**:

```javascript
new Chart(document.getElementById('chart{slide_number}'), {
    type: '{chart_type}',  // bar, line, pie, doughnut, radar, polarArea, bubble, scatter
    data: {
        labels: {data_labels},
        datasets: [{
            label: '{series_label}',
            data: {data_values},
            backgroundColor: ['#F85d42', '#556EE6', '#34c38f', '#50a5f1', '#f1b44c']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            title: {
                display: true,
                text: '{chart_title}',
                font: { size: 18, weight: 'bold' }
            }
        }
    }
});
```

## Template Quality Guarantees

All templates ensure:
- ✅ Exact McKinsey color codes
- ✅ Precise font sizes
- ✅ Standardized layouts
- ✅ Responsive design (1200px, 768px breakpoints)
- ✅ Interactive features (navigation, keyboard shortcuts, fullscreen)
- ✅ Chart.js integration with McKinsey colors
- ✅ Professional animations
