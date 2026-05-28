# Complete UX Design Workflow

Systematic design process from research to development handoff using Gemini and memex-cli.

---

## 5-Stage Design Process

### Overview

```
Research → Define → Ideate → Prototype → Test
   ↓         ↓        ↓         ↓         ↓
 Discover  Problem  Solutions  Tangible  Validate
  Users    Space     Space    Artifacts  & Iterate
```

Each stage produces specific deliverables that inform the next stage.

---

### Stage 1: Research

**Objective:** Understand users, context, and existing solutions.

**Activities:**
- User interviews and surveys
- Contextual inquiry (observe users in environment)
- Competitive analysis
- Stakeholder interviews
- Analytics review

**Key Deliverables:**
- User personas
- User journey maps
- Empathy maps
- Research findings report
- Competitive analysis matrix

**Gemini Workflow:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: user-interviews
backend: gemini
workdir: ./research
---CONTENT---
分析5份用户访谈记录，提取关键需求和痛点
---END---

---TASK---
id: personas
backend: gemini
workdir: ./research
dependencies: user-interviews
---CONTENT---
基于访谈分析，创建3个主要用户画像（包含目标、痛点、行为特征）
---END---

---TASK---
id: journey-map
backend: gemini
workdir: ./research
dependencies: personas
---CONTENT---
为主要用户画像绘制当前使用流程的旅程地图，标注痛点和机会点
---END---
EOF
```

**Duration:** 1-2 weeks for initial research

---

### Stage 2: Define

**Objective:** Synthesize research into clear problem statements and requirements.

**Activities:**
- Affinity mapping (group insights)
- Problem statement creation
- Feature prioritization (MoSCoW method)
- Success metrics definition
- Information architecture planning

**Key Deliverables:**
- Problem statement ("How Might We...")
- User stories and acceptance criteria
- Feature roadmap
- Information architecture (IA)
- Site map

**Gemini Workflow:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: problem-statement
backend: gemini
workdir: ./define
---CONTENT---
基于用户研究，撰写核心问题陈述（How Might We格式）
---END---

---TASK---
id: user-stories
backend: gemini
workdir: ./define
dependencies: problem-statement
---CONTENT---
创建15-20条用户故事（As a [user], I want [goal], so that [benefit]）
---END---

---TASK---
id: ia-design
backend: gemini
workdir: ./define
dependencies: user-stories
---CONTENT---
设计信息架构：导航结构、页面层级、内容分类
---END---
EOF
```

**Duration:** 1 week

---

### Stage 3: Ideate

**Objective:** Generate diverse solutions and select the most promising.

**Activities:**
- Brainstorming sessions
- Sketching and crazy 8s
- Design studio workshops
- Solution evaluation (effort vs impact)
- Concept selection

**Key Deliverables:**
- Sketches and concept drawings
- User flow diagrams
- Task flows
- Selected design direction

**Gemini Workflow:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: user-flows
backend: gemini
workdir: ./ideate
---CONTENT---
设计3个核心功能的用户流程图：注册、购买、分享
---END---

---TASK---
id: interaction-concepts
backend: gemini
workdir: ./ideate
dependencies: user-flows
---CONTENT---
为每个流程设计2-3种不同的交互方案（描述式）
---END---

---TASK---
id: concept-evaluation
backend: gemini
workdir: ./ideate
dependencies: interaction-concepts
---CONTENT---
评估各方案的可行性、用户价值、技术难度，推荐最佳方案
---END---
EOF
```

**Duration:** 1-2 weeks

---

### Stage 4: Prototype

**Objective:** Create tangible representations to test with users.

**Activities:**
- Wireframing (low-fidelity)
- Interactive prototyping
- Visual design (high-fidelity)
- Design system creation
- Content writing

**Key Deliverables:**
- Low-fidelity wireframes
- High-fidelity mockups
- Interactive prototypes (Figma, Adobe XD)
- Design system documentation
- UI specifications

**Gemini Workflow:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: wireframes
backend: gemini
workdir: ./prototype
---CONTENT---
创建10个关键页面的线框图规格说明（文字描述布局、组件位置）
---END---

---TASK---
id: design-system
backend: gemini
workdir: ./prototype
dependencies: wireframes
---CONTENT---
定义设计系统：颜色、字体、间距、组件规范
---END---

---TASK---
id: mockup-specs
backend: gemini
workdir: ./prototype
dependencies: design-system, wireframes
---CONTENT---
为5个核心页面编写高保真视觉稿规格说明
---END---
EOF
```

**Parallel Task Example:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: wireframes
backend: gemini
workdir: ./prototype
---CONTENT---
线框图设计
---END---

---TASK---
id: page1-mockup
backend: gemini
workdir: ./prototype
dependencies: wireframes
---CONTENT---
首页视觉稿
---END---

---TASK---
id: page2-mockup
backend: gemini
workdir: ./prototype
dependencies: wireframes
---CONTENT---
商品列表页视觉稿
---END---

---TASK---
id: page3-mockup
backend: gemini
workdir: ./prototype
dependencies: wireframes
---CONTENT---
购物车页视觉稿
---END---

---TASK---
id: design-handoff
backend: gemini
workdir: ./prototype
dependencies: page1-mockup, page2-mockup, page3-mockup
---CONTENT---
生成设计交接文档：标注规范、切图说明、交互细节
---END---
EOF
```

**Duration:** 2-3 weeks

---

### Stage 5: Test

**Objective:** Validate designs with users and iterate.

**Activities:**
- Usability testing (moderated/unmoderated)
- A/B testing
- Heuristic evaluation
- Accessibility audit
- Analytics setup

**Key Deliverables:**
- Usability test report
- Design iteration recommendations
- Validated high-fidelity prototypes
- Final design specifications

**Gemini Workflow:**

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: test-plan
backend: gemini
workdir: ./test
---CONTENT---
创建可用性测试计划：测试目标、任务场景、成功指标
---END---

---TASK---
id: test-analysis
backend: gemini
workdir: ./test
files: ./test-recordings-summary.md
files-mode: embed
dependencies: test-plan
---CONTENT---
分析5名用户的测试结果，总结问题和改进建议
---END---

---TASK---
id: iteration-plan
backend: gemini
workdir: ./test
dependencies: test-analysis
---CONTENT---
基于测试结果，制定设计迭代计划（优先级排序）
---END---
EOF
```

**Duration:** 1-2 weeks

---

## Deliverables by Stage

### Quick Reference Table

| Stage | Key Deliverables | Tools/Methods | Gemini Output |
|-------|-----------------|---------------|---------------|
| **Research** | Personas, Journey Maps | Interviews, Surveys | User insights analysis |
| **Define** | Problem Statement, IA, User Stories | Affinity Mapping | Feature prioritization |
| **Ideate** | User Flows, Concepts | Brainstorming, Sketching | Interaction design specs |
| **Prototype** | Wireframes, Mockups, Design System | Figma, Adobe XD | Component specifications |
| **Test** | Test Reports, Iterations | Usability Testing | Improvement recommendations |

---

## Design-Specific DAG Workflows

### Example 1: Complete App Design (Sequential)

```
Research → Define → Ideate → Prototype → Test
```

```bash
---TASK---
id: research
backend: gemini
---CONTENT---
用户研究
---END---

---TASK---
id: define
backend: gemini
dependencies: research
---CONTENT---
问题定义和IA设计
---END---

---TASK---
id: ideate
backend: gemini
dependencies: define
---CONTENT---
用户流程和交互方案
---END---

---TASK---
id: prototype
backend: gemini
dependencies: ideate
---CONTENT---
线框图和视觉稿
---END---

---TASK---
id: test
backend: gemini
dependencies: prototype
---CONTENT---
可用性测试和迭代
---END---
```

### Example 2: Parallel Page Design

After IA is defined, design multiple pages in parallel:

```
        IA Design
       /    |    \
  Page1  Page2  Page3
       \    |    /
     Design System
```

```bash
---TASK---
id: ia
backend: gemini
---CONTENT---
信息架构设计
---END---

---TASK---
id: home-page
backend: gemini
dependencies: ia
---CONTENT---
首页设计规格
---END---

---TASK---
id: product-page
backend: gemini
dependencies: ia
---CONTENT---
商品详情页设计规格
---END---

---TASK---
id: checkout-page
backend: gemini
dependencies: ia
---CONTENT---
结算页设计规格
---END---

---TASK---
id: design-system
backend: gemini
dependencies: home-page, product-page, checkout-page
---CONTENT---
提取通用组件，创建设计系统
---END---
```

### Example 3: Multi-Backend Workflow

Use Claude for architecture, Gemini for UX, Codex for implementation:

```bash
---TASK---
id: architecture
backend: claude
---CONTENT---
设计系统架构和API规范
---END---

---TASK---
id: ux-design
backend: gemini
dependencies: architecture
---CONTENT---
基于API规范，设计用户界面和交互流程
---END---

---TASK---
id: frontend-impl
backend: codex
dependencies: ux-design
---CONTENT---
实现前端React组件
---END---
```

See [memex-cli/references/advanced-usage.md](../../memex-cli/references/advanced-usage.md) for more DAG patterns.

---

## Iteration and Feedback Loops

### Continuous Improvement Cycle

```
Design → Test → Analyze → Iterate → Design
                   ↑__________________|
```

### Feedback Sources

1. **User Testing**
   - Moderated usability sessions
   - Remote unmoderated tests
   - Guerrilla testing

2. **Stakeholder Reviews**
   - Weekly design critiques
   - Sprint reviews
   - Executive presentations

3. **Analytics**
   - Heatmaps (Hotjar, Crazy Egg)
   - User recordings
   - Conversion funnels

4. **A/B Testing**
   - Button colors/text
   - Layout variations
   - Content hierarchy

### Iteration Strategies

**Quick Iterations:**
- Daily design updates based on team feedback
- Adjust colors, spacing, copy
- Small UX improvements

**Major Iterations:**
- Redesign entire flows after testing
- Pivot on core concepts
- Architecture changes

**When to Iterate:**
- ✅ User testing reveals blockers (>50% failure rate)
- ✅ Analytics show high drop-off (>40% bounce)
- ✅ Accessibility issues identified
- ⚠️ Stakeholder preference (validate with data first)

---

## Handoff to Development

### Design Specifications Document

**Contents:**
1. **Overview** - Project goals, target users
2. **User flows** - Interaction diagrams
3. **Page specifications**
   - Layout dimensions
   - Component breakdown
   - States (default, hover, active, disabled)
4. **Design system**
   - Color palette (HEX codes)
   - Typography (fonts, sizes, line heights)
   - Spacing (8px grid system)
   - Component library
5. **Assets**
   - Icons (SVG)
   - Images (optimized)
   - Illustrations
6. **Interactions**
   - Animations (duration, easing)
   - Transitions
   - Micro-interactions

### Annotation Best Practices

**Figma/Sketch:**
- Use frames for different screen sizes
- Create component variants (states)
- Add comments for interaction notes
- Share live prototypes for feedback

**Developer-Friendly Specs:**
- CSS units (px, rem, %)
- Responsive breakpoints
- Z-index layering
- Accessibility notes (ARIA labels, alt text)

### Collaboration Tools

| Tool | Purpose |
|------|---------|
| **Figma/Adobe XD** | Design and prototyping |
| **Zeplin/Avocode** | Design handoff and specs |
| **Abstract/Git** | Version control |
| **Notion/Confluence** | Documentation |
| **Slack/Teams** | Communication |

### Developer Collaboration Tips

1. **Involve devs early** - Include in design reviews
2. **Document constraints** - Note technical limitations
3. **Provide fallbacks** - What if image doesn't load?
4. **Use shared language** - Align on component names
5. **Test together** - Joint QA sessions

---

## Gemini Workflow Tips

### 1. Use Dependencies for Sequential Stages

```bash
---TASK---
id: research
backend: gemini
---CONTENT---
用户研究
---END---

---TASK---
id: define
backend: gemini
dependencies: research  # Waits for research to complete
---CONTENT---
基于研究结果，定义问题和IA
---END---
```

### 2. Parallelize Independent Tasks

Design multiple pages simultaneously after IA:

```bash
---TASK---
id: page1
backend: gemini
dependencies: ia
---END---

---TASK---
id: page2
backend: gemini
dependencies: ia  # Runs in parallel with page1
---END---
```

### 3. Resume for Iterations

```bash
memex-cli resume --backend gemini --run-id <RUN_ID> --stdin <<'EOF'
---TASK---
id: iteration-v2
backend: gemini
---CONTENT---
基于测试反馈，优化结算流程
---END---
EOF
```

See [memex-cli/examples/resume-workflow.md](../../memex-cli/examples/resume-workflow.md).

---

## Common Workflow Patterns

### Pattern 1: Single Page Design

```
Research → Define → Wireframe → Mockup → Review
```

**Duration:** 3-5 days

### Pattern 2: Feature Addition

```
User Story → Flow Design → Wireframe → Review → Iterate
```

**Duration:** 1-2 weeks

### Pattern 3: Redesign

```
Audit → Research → Define → Ideate → Prototype → Test → Iterate
```

**Duration:** 6-8 weeks

---

## Related Resources

- [design-principles.md](./design-principles.md) - UX fundamentals
- [multimodal-tips.md](./multimodal-tips.md) - Gemini image analysis
- [examples/user-research.md](../examples/user-research.md) - Research examples
- [examples/wireframes-mockups.md](../examples/wireframes-mockups.md) - Prototype examples
- [memex-cli/references/advanced-usage.md](../../memex-cli/references/advanced-usage.md) - DAG workflows
