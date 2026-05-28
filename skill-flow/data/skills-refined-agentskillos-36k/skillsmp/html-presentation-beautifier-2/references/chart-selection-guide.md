# Chart Selection Guide

Decision trees and strategies for selecting appropriate charts and visualizations.

## Quick Decision Tree

```
START: What type of content do I have?
│
├─ NUMERICAL DATA → Go to Data Chart Selection
│
└─ CONCEPTUAL CONTENT → Go to Conceptual Visualization Selection
```

## Data Chart Selection (Chart.js)

### Decision Matrix

| Data Characteristic | Recommended Chart | Chart.js Type |
|---------------------|------------------|---------------|
| Categorical comparison | Column chart | `bar` |
| Time series trends | Line chart | `line` |
| Part-to-whole (≤5 items) | Doughnut chart | `doughnut` |
| Part-to-whole (≤8 items) | Pie chart | `pie` |
| Multi-dimensional comparison | Radar chart | `radar` |
| Rankings, cyclical data | Polar area chart | `polarArea` |
| Three dimensions (x, y, size) | Bubble chart | `bubble` |
| Correlation analysis | Scatter chart | `scatter` |

### Smart Selection Algorithm

```
IF data has time dimension:
    → Use 'line' chart

ELIF data shows parts of a whole:
    IF items ≤ 5:
        → Use 'doughnut' chart
    ELIF items ≤ 8:
        → Use 'pie' chart
    ELSE:
        → Use 'bar' chart (too many for pie)

ELIF data compares categories:
    IF need to show multiple metrics per category:
        → Use 'radar' chart
    ELSE:
        → Use 'bar' chart

ELIF data shows correlation:
    IF need to show size dimension:
        → Use 'bubble' chart
    ELSE:
        → Use 'scatter' chart

ELIF data is cyclical or shows rankings:
    → Use 'polarArea' chart

ELSE:
    → Default to 'bar' chart (most versatile)
```

## Conceptual Visualization Selection

### 9 Content Structure Types

#### 1. Progressive/Sequential (递进型)

**Keywords**: 首先、其次、最后、第一步、第二步、阶段、步骤

**Decision Tree**:
```
IF 3-5 sequential steps with no branches:
    → Use 'progression' (simple arrow flow)

ELIF has time labels (dates, years):
    → Use 'timeline' (horizontal timeline)

ELIF has decision points or branches:
    → Use 'flowchart' (with decision diamonds)

ELIF multi-phase with parallel activities:
    → Use 'strategy-roadmap' (swimlane timeline)

ELSE:
    → Default to 'progression'
```

**Example Files**:
- `assets/flowchart-example.html`
- `assets/timeline-example.html`
- `assets/strategy-roadmap-example.html`

---

#### 2. Temporal/Time-series (时间序列型)

**Keywords**: 年份(2024)、季度(Q1)、月份、过去、现在、未来、趋势、预测

**Decision Tree**:
```
IF clear chronological sequence:
    → Use 'timeline' (horizontal with milestones)

ELIF strategic planning with phases:
    → Use 'strategy-roadmap' (multi-track timeline)

ELIF numerical trend data:
    → Use Chart.js 'line' chart

ELSE:
    → Default to 'timeline'
```

**Example Files**:
- `assets/timeline-example.html`
- `assets/strategy-roadmap-example.html`

---

#### 3. Parallel/Coordinate (并列型)

**Keywords**: 同时、以及、另外、此外、包括

**Decision Tree**:
```
IF 2-4 equal-weight points:
    → Use 'emphasis-box' (grid of boxes)

ELIF 5+ points branching from central theme:
    → Use 'mindmap' (radial layout)

ELIF 2x2 or 3x3 framework:
    → Use 'matrix' (grid layout)

ELIF horizontal comparison with labels:
    → Use 'mckinsey-label-bar' (labeled bars)

ELSE:
    → Default to 'emphasis-box'
```

**Example Files**:
- `assets/mindmap-example.html`
- `assets/mckinsey-label-bar-example.html`

---

#### 4. Hierarchical (层级型)

**Keywords**: 基础、中级、高级、核心、外围、层次、级别

**Decision Tree**:
```
IF bottom-up hierarchy (foundation → top):
    → Use 'pyramid' (triangle pointing up)

ELIF top-down hierarchy (most important → details):
    → Use 'inverted-pyramid' (triangle pointing down)

ELIF organizational structure:
    → Use 'tree' (hierarchical boxes)

ELSE:
    → Default to 'pyramid'
```

**Example Files**:
- `assets/pyramid-chart-example.html`
- `assets/inverted-pyramid-example.html`

---

#### 5. Comparative/Dual (对比型)

**Keywords**: 对比、差异、优劣、vs、相比、两者、A方案B方案、现状vs目标

**Decision Tree**:
```
IF two states side-by-side (before/after, current/target):
    → Use 'comparison' (left-right layout)

ELIF advantages vs disadvantages:
    → Use 'pros-cons' (two-column with +/-)

ELIF overlapping sets or shared attributes:
    → Use 'venn-diagram' (circles)

ELIF variable comparison with slider:
    → Use 'slider-chart' (interactive comparison)

ELSE:
    → Default to 'comparison'
```

**Example Files**:
- `assets/pros-cons-example.html`
- `assets/venn-diagram-example.html`
- `assets/slider-chart-example.html`

---

#### 6. Analytical Framework (分析框架型)

**Keywords**: SWOT、PEST、4P、5W1H、3C、波特五力、BCG矩阵

**Decision Tree**:
```
IF mentions "SWOT", "优势", "劣势", "机会", "威胁":
    → Use 'swot-analysis' (2x2 grid)

ELIF mentions "市场", "产品", "增长策略":
    → Use 'ansoff-matrix' (market-product matrix)

ELIF mentions "What", "Why", "Who", "When", "Where", "How":
    → Use '5w1h' (hexagonal layout)

ELIF mentions "竞争", "定位", "市场地位":
    → Use 'competitive-4box' (positioning matrix)

ELIF mentions "基本", "期望", "魅力", "满意度":
    → Use 'kano-model' (satisfaction matrix)

ELSE:
    → Use 'matrix' (generic 2x2 or 3x3)
```

**Example Files**:
- `assets/swot-analysis-example.html`
- `assets/ansoff-matrix-example.html`
- `assets/competitive-4box-example.html`
- `assets/5w1h-example.html`
- `assets/kano-model-example.html`

---

#### 7. Transformation/Funnel (转化流程型)

**Keywords**: 转化、漏斗、筛选、流失、通过率、转化率、阶段

**Decision Tree**:
```
IF stage-by-stage filtering with decreasing numbers:
    → Use 'funnel-chart' (inverted triangle stages)

ELIF value creation process with flow:
    → Use 'value-stream' (horizontal flow with value adds)

ELIF sequential additions/subtractions:
    → Use 'waterfall-chart' (bars with bridges)

ELSE:
    → Default to 'funnel-chart'
```

**Example Files**:
- `assets/funnel-chart-example.html`
- `assets/value-stream-example.html`

---

#### 8. Cyclical/Iterative (循环型)

**Keywords**: 循环、迭代、反馈、持续、闭环、反复、优化、改进

**Decision Tree**:
```
IF closed-loop process with feedback:
    → Use 'cycle' (circular with arrows)

ELIF iterative process with phases:
    → Use 'circular-flow' (circular with labeled segments)

ELIF cyclical data comparison:
    → Use 'polar-chart' (Chart.js polarArea)

ELSE:
    → Default to 'cycle'
```

**Example Files**:
- `assets/polar-chart-example.html`

---

#### 9. Causal/Problem-Solution (因果/问题解决型)

**Keywords**: 原因、结果、问题、解决方案、根源、导致、引起、因为、所以

**Decision Tree**:
```
IF problem on left, solution on right:
    → Use 'problem-solution' (two-column with arrow)

ELIF 80/20 rule or key factors:
    → Use 'pareto-chart' (bar + line chart)

ELIF root cause analysis:
    → Use 'fishbone' (cause-effect diagram)

ELIF KPI measurement:
    → Use 'gauge-chart' (speedometer)

ELSE:
    → Default to 'problem-solution'
```

**Example Files**:
- `assets/problem-solution-example.html`
- `assets/pareto-chart-example.html`
- `assets/gauge-chart-example.html`

---

## Special Cases

### When Content is Ambiguous

```
IF unclear content structure:
    IF ≤4 points:
        → Use 'emphasis-box' (safe default)
    ELIF 5+ points:
        → Use 'mindmap' (handles many items)
    ELSE:
        → Ask user to clarify structure
```

### When Multiple Types Apply

**Priority Order**:
1. Framework (if mentions SWOT, 5W1H, etc.) → Use framework
2. Time-based (if has dates/timeline) → Use timeline
3. Comparison (if explicit comparison) → Use comparison
4. Sequential (if has steps) → Use progression
5. Parallel (default) → Use emphasis-box

### Multi-Department Processes

```
IF process involves multiple actors/departments:
    → Use 'swimlane' (horizontal lanes per actor)
```

**Example File**: `assets/swimlane-example.html`

---

## Critical Rules

1. **NEVER use plain text bullet lists** for conclusions/insights
2. **ALWAYS assign a visualization type** for conceptual content
3. **Match visualization to content structure**, not just aesthetics
4. **Reference example files** for implementation guidance
5. **Use McKinsey color palette** for all visualizations

---

## Implementation Workflow

**Step 1**: Identify content structure type (1-9)
**Step 2**: Follow decision tree to select visualization
**Step 3**: Open corresponding example file from `assets/`
**Step 4**: Copy CSS styles and HTML structure
**Step 5**: Customize with actual content
**Step 6**: Integrate into slide
