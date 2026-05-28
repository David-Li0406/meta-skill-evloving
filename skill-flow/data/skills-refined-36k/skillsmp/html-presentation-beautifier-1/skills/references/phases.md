# Phase Detail Guide

This document provides detailed information for each phase of the presentation generation process.

## Phase 1: Document Parsing

**Goal**: Extract and analyze the source document to understand content structure, data points, and conclusions.

**Detailed Steps**:

1. **Detect Document Format**
   - Check file extension (`.md`, `.json`, `.txt`)
   - Analyze content for format indicators (headers, JSON structure)
   - Confirm document type with confidence

2. **Read and Preserve Content**
   - Read entire document into memory
   - Store raw content for reference
   - Never modify original text

3. **Parse Document Structure**
   - Identify headers and their levels (H1, H2, H3)
   - Create hierarchical section tree
   - Extract content under each header
   - Preserve section relationships

4. **Extract Data Points**
   - Scan content for numerical patterns
   - Extract values with units (%$, k, m, b)
   - Assign category based on section context
   - Create data point objects with metadata

5. **Extract Conclusions**
   - Identify conclusion sections by keywords
   - Extract complete sentences
   - Preserve exact wording
   - Classify by category (conclusion, finding, recommendation)

6. **Validate Extraction**
   - Verify all sections captured
   - Confirm data points extracted
   - Check conclusions completeness
   - Ensure no content loss

**Common Issues**:

- **Nested sections**: Handle indentation and hierarchy correctly
- **Multiple conclusion sections**: Merge or keep separate based on context
- **Inconsistent formatting**: Use regex patterns for flexible parsing
- **Large documents**: Ensure memory efficiency for file reading

## Phase 2: Content Structuring

**Goal**: Transform parsed content into slide-friendly format while preserving all original meaning and conclusions.

**Detailed Steps**:

1. **Analyze Content Volume**
   - Count total sections and content length
   - Estimate number of slides needed
   - Identify content density by section

2. **Create Slide Groups**
   - **Executive Summary Group**: Title slide + summary points
   - **Data Analysis Group**: Charts with insights (1-3 slides)
   - **Detail Slides Group**: Detailed findings and analysis
   - **Conclusion Group**: Final conclusions and recommendations

3. **Assign Content to Slides**
   - Map sections to appropriate slide types
   - Balance content across slides (avoid overcrowding)
   - Prioritize high-impact conclusions for summary
   - Group related data points together

4. **Design Visualizations**
   - For each data set, determine best chart type:
     - **Bar Chart**: Comparisons across categories
     - **Line Chart**: Trends over time periods
     - **Pie Chart**: Percentage breakdowns
     - **Table**: Detailed multi-metric data
   - Assign chart colors from palette
   - Ensure clarity and readability

5. **Verify Content Coverage**
   - All sections assigned to slides
   - All data points visualized
   - All conclusions preserved
   - No content duplication

**Slide Templates**:

**Title Slide**:
- Main title (document title)
- Subtitle (context or date)
- Minimal text, maximum impact

**Executive Summary**:
- Top 3-5 conclusions
- Key metrics highlighted
- Actionable takeaways
- Clear hierarchy (most important first)

**Data Slide**:
- Chart on left (60% width)
- Insights on right (40% width)
- Chart caption describing data
- Bullet points for key insights

**Detail Slide**:
- Section header
- Body text (3-5 paragraphs)
- Supporting data table if needed
- Clear visual hierarchy

**Conclusion Slide**:
- Grid of conclusion cards (3 columns)
- Each card: conclusion number + text
- Recommendations box with numbered list
- Accent colors for emphasis

**Common Issues**:

- **Content overflow**: Split into multiple slides
- **Content sparse**: Combine related sections
- **Data mismatch**: Verify data extraction accuracy
- **Missing context**: Ensure slide tells complete story

## Phase 3: Design & Layout

**Goal**: Apply McKinsey-style design system to structured content for professional presentation.

**Detailed Steps**:

1. **Establish Design System**
   - Load color palette from `styles.css`
   - Set typography scale (title: 64px, subtitle: 36px, body: 18px)
   - Define spacing rules (margins: 40-60px, gaps: 20-30px)
   - Standardize border radius (4-8px)

2. **Apply Color Scheme**
   - **Backgrounds**: White (#FFFFFF) for all slides
   - **Headers**: Black (#000000) with white text
   - **Accents**: Orange (#F85d42) for highlights
   - **Secondary**: Gray (#74788d) for supporting text
   - **Charts**: Use palette colors (blue, green, yellow) for variety

3. **Design Layouts**
   - **Single Column**: Title slides, conclusion slides
   - **Two Column**: Data slides (chart + text)
   - **Three Column**: Comparison slides
   - **Grid Layout**: Conclusion cards (3 columns)

4. **Typography Hierarchy**
   - **Level 1**: Title (64px, bold, black)
   - **Level 2**: Subtitle (36px, bold, accent)
   - **Level 3**: Section header (28px, bold, black)
   - **Level 4**: Body text (18px, regular, dark gray)
   - **Level 5**: Chart labels (14px, clear, readable)

5. **Optimize Spacing**
   - Margins: 40-60px on all sides
   - Line height: 1.6-1.8 for readability
   - Gap between elements: 20-30px
   - Gap between sections: 40-60px
   - Generous white space for clarity

6. **Design Visual Elements**
   - **Charts**: Clean, minimal, clear labels
   - **Tables**: Borders, alternating row colors, aligned text
   - **Cards**: Subtle shadow, colored border accent
   - **Icons**: Minimal, consistent style (if used)

**Design Consistency Rules**:

1. **Alignment**: All elements aligned to grid
2. **Proximity**: Related elements close together
3. **Contrast**: High contrast for emphasis
4. **Repetition**: Consistent styles across slides
5. **Balance**: Visual weight evenly distributed

**Common Issues**:

- **Inconsistent colors**: Strict adherence to palette
- **Poor spacing**: Use defined spacing scale
- **Mixed fonts**: Use system font stack consistently
- **Cluttered layouts**: Simplify and use white space
- **Low contrast**: Ensure text is readable

## Phase 4: HTML Generation

**Goal**: Generate interactive HTML presentation file with all slides, styling, and functionality.

**Detailed Steps**:

1. **Generate Slide HTML**
   - Iterate through structured slides
   - Apply appropriate HTML template for each slide type
   - Inject content exactly from Phase 2
   - Add data attributes for navigation
   - Set first slide as `active`

2. **Generate Chart Scripts**
   - For each data slide, create Chart.js initialization
   - Map data points to chart labels and values
   - Apply McKinsey color palette
   - Configure chart options (responsive, plugins, scales)
   - Generate clean, readable JavaScript

3. **Combine with Template**
   - Load base template (`template.html`)
   - Insert generated slides into container
   - Insert chart scripts before closing body tag
   - Ensure valid HTML structure
   - Verify no duplicate IDs

4. **Add Navigation Script**
   - Initialize slide counter
   - Add event listeners for keyboard (arrows, space, escape)
   - Implement prev/next button functionality
   - Add fullscreen toggle
   - Ensure smooth transitions

5. **Generate Output File**
   - Write HTML to specified output path
   - Use UTF-8 encoding
   - Include CSS reference (`styles.css`)
   - Include Chart.js CDN
   - Include navigation script

6. **Test Functionality**
   - Verify all slides render correctly
   - Test navigation (buttons, keyboard)
   - Verify charts display with correct data
   - Check responsiveness on different screen sizes
   - Ensure fullscreen mode works

**HTML Structure**:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Document Title</title>
  <link rel="stylesheet" href="styles.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <nav>
    <button onclick="navigate(-1)">Previous</button>
    <span>Slide <span id="current">1</span> of <span id="total">N</span></span>
    <button onclick="navigate(1)">Next</button>
  </nav>

  <div class="presentation-container">
    <div class="slide active" data-slide="1">...</div>
    <div class="slide" data-slide="2">...</div>
    ...
  </div>

  <button onclick="toggleFullscreen()">Fullscreen</button>

  <script>
    // Navigation logic
    // Chart initialization scripts
  </script>
</body>
</html>
```

**Chart Configuration**:

```javascript
new Chart(canvasId, {
  type: 'bar',
  data: {
    labels: [...],
    datasets: [{
      label: 'Value',
      data: [...],
      backgroundColor: '#556EE6',
      borderWidth: 0
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: '#e0e0e0' }
      },
      x: {
        grid: { display: false }
      }
    }
  }
});
```

**Common Issues**:

- **Missing dependencies**: Ensure Chart.js CDN is included
- **Chart not rendering**: Verify canvas element ID matches script
- **Navigation broken**: Check event listeners and slide classes
- **Content distorted**: Verify HTML structure and CSS classes
- **Duplicate IDs**: Ensure unique IDs for all elements

## Phase Transitions

**Phase 1 → Phase 2**:
- Validate all content extracted
- Verify data points catalogued
- Confirm conclusions captured
- Check no content loss

**Phase 2 → Phase 3**:
- Ensure all content assigned to slides
- Verify visualizations planned
- Check content balance across slides
- Confirm all conclusions included

**Phase 3 → Phase 4**:
- Validate design system applied
- Check color and typography consistency
- Verify spacing and layout optimized
- Ensure professional quality achieved

**Phase 4 → Complete**:
- Test all functionality
- Verify presentation renders correctly
- Check responsiveness
- Validate against original requirements
