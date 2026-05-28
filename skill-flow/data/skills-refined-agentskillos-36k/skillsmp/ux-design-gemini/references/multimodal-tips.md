# Gemini Multimodal Usage Tips

Leverage Gemini's image analysis capabilities for design critique, competitive analysis, and visual QA using memex-cli.

---

## Image Upload and Analysis

### Supported Formats

| Format | Support | Recommended Use |
|--------|---------|-----------------|
| **PNG** | ✅ Best | UI screenshots, mockups with transparency |
| **JPG/JPEG** | ✅ Good | Photos, full-page designs |
| **WEBP** | ✅ Good | Modern web formats |
| **GIF** | ⚠️ Limited | Static images only (no animation analysis) |
| **SVG** | ❌ No | Use PNG export instead |

### File Size and Resolution

**Optimal Settings:**
- **File size:** < 5MB per image (faster processing)
- **Resolution:** 72-150 DPI (screen resolution)
- **Dimensions:** 1920×1080 or native device resolution

**Compression Tips:**
- Use TinyPNG or Squoosh for compression
- Balance quality vs file size
- Maintain text readability after compression

### Upload Method

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: design-review
backend: gemini
workdir: /path/to/project
files: ./mockups/home.png, ./mockups/product.png
files-mode: embed    # Embeds image content
---CONTENT---
审查这两个设计稿，提供改进建议
---END---
EOF
```

**Key Field:**
- `files-mode: embed` - Required for image analysis
- Supports multiple images (comma-separated)

---

## Design Critique Prompt Templates

### Template 1: Visual Hierarchy Analysis

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: visual-hierarchy
backend: gemini
files: ./design.png
files-mode: embed
---CONTENT---
分析这个设计的视觉层次：

1. 视觉流向
   - 用户视线首先看向哪里？
   - 视觉路径是F型还是Z型？
   - 关键元素是否获得足够关注？

2. 视觉权重
   - 主要CTA是否突出？
   - 次要信息是否过于抢眼？
   - 标题、正文、按钮的对比度是否合理？

3. 留白使用
   - 元素间距是否一致？
   - 是否有足够呼吸空间？
   - 留白是否帮助引导视线？

4. 改进建议
   - 具体调整方案（颜色、大小、位置）
---END---
EOF
```

### Template 2: Usability Heuristic Evaluation

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: heuristic-eval
backend: gemini
files: ./interface.png
files-mode: embed
---CONTENT---
使用Nielsen's 10 Heuristics评估这个界面：

1. 系统状态可见性
   - 是否清晰显示当前状态？
   - 加载、成功、错误状态是否明确？

2. 用户控制和自由
   - 是否提供撤销/返回选项？
   - 用户能否轻松退出流程？

3. 一致性和标准
   - 按钮样式是否统一？
   - 是否符合平台规范（iOS/Android/Web）？

4. 错误预防
   - 是否有防误操作设计？
   - 危险操作是否有确认？

5. 易识别而非回忆
   - 选项是否可见？
   - 是否需要记忆上一步信息？

为每一项打分（1-5分）并提供改进建议。
---END---
EOF
```

### Template 3: Accessibility Audit

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: accessibility-audit
backend: gemini
files: ./design.png
files-mode: embed
---CONTENT---
评估这个设计的无障碍性（WCAG 2.1 Level AA）：

1. 色彩对比度
   - 文本与背景对比是否≥4.5:1？
   - 大文本（18pt+）是否≥3:1？
   - 列出需要调整的文本元素

2. 色彩使用
   - 是否仅依赖颜色传达信息？
   - 状态提示是否有图标或文字辅助？

3. 文字可读性
   - 字体大小是否足够（最小14px）？
   - 行间距是否适当？

4. 交互元素
   - 按钮、链接是否足够大（44×44pt）？
   - 触摸目标间距是否充足？

5. 焦点指示
   - 是否有清晰的焦点状态设计？

提供具体修改建议（颜色值、尺寸调整）。
---END---
EOF
```

### Template 4: Consistency Check

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: consistency-check
backend: gemini
files: ./page1.png, ./page2.png, ./page3.png
files-mode: embed
---CONTENT---
检查这3个页面的设计一致性：

1. 按钮样式
   - 主按钮、次要按钮、文字按钮是否统一？
   - 圆角、内边距、字体是否一致？

2. 导航栏
   - 位置、高度、元素排布是否相同？
   - 激活状态样式是否一致？

3. 颜色使用
   - 品牌色使用是否规范？
   - 状态颜色（成功绿、错误红、警告黄）是否统一？

4. 间距系统
   - 是否遵循统一的间距体系（8px grid）？

列出所有不一致之处及修改建议。
---END---
EOF
```

---

## Multi-Image Comparison Analysis

### Use Case 1: Version Comparison

Compare different iterations of the same design:

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: version-compare
backend: gemini
files: ./v1-home.png, ./v2-home.png
files-mode: embed
---CONTENT---
对比这两个版本的首页设计：

1. 主要变化
   - 列出所有视觉和布局差异

2. 改进之处
   - V2相比V1的优势

3. 潜在问题
   - V2可能引入的新问题

4. 推荐
   - 应采用V1还是V2？
   - 或建议混合两者优点的V3方案
---END---
EOF
```

### Use Case 2: A/B Testing Design Analysis

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: ab-test-analysis
backend: gemini
files: ./variant-a.png, ./variant-b.png
files-mode: embed
---CONTENT---
分析这两个A/B测试变体：

变体A：蓝色CTA按钮，位于页面顶部
变体B：橙色CTA按钮，位于页面中部

预测：
1. 哪个变体转化率可能更高？为什么？
2. 各自的优势和劣势
3. 建议测试指标（点击率、完成率、跳出率）
4. 后续优化方向
---END---
EOF
```

### Use Case 3: Competitive Analysis

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: competitive-analysis
backend: gemini
files: ./our-app.png, ./competitor-a.png, ./competitor-b.png
files-mode: embed
---CONTENT---
竞品设计对比分析：

1. 布局结构
   - 各产品的信息架构差异
   - 导航设计对比

2. 视觉风格
   - 色彩、字体、图标风格对比
   - 哪个视觉冲击力更强？

3. 交互设计
   - CTA设计和位置
   - 用户引导策略

4. 优劣分析
   - 我们的优势
   - 竞品值得借鉴之处
   - 差异化机会

5. 改进建议
   - 3-5条具体优化建议
---END---
EOF
```

---

## Screenshot Preparation Tips

### Best Practices

**1. High-Quality Captures**
- Use native screenshot tools (Cmd+Shift+3/4 on Mac, Win+Shift+S on Windows)
- Capture at actual device resolution
- Avoid scaling after capture (maintains clarity)

**2. Clean Screenshots**
- Hide personal information (dummy data)
- Remove browser UI if analyzing web design
- Close unnecessary tabs/windows

**3. Annotated Screenshots**

For complex critiques, add annotations before upload:

```bash
# Example with annotations
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: annotated-review
backend: gemini
files: ./annotated-design.png
files-mode: embed
---CONTENT---
我已在设计稿上标注了红色箭头和数字1-5。
请针对每个标注点提供具体的设计建议。
---END---
EOF
```

**4. Mobile Screenshots**

For mobile designs, include:
- Device frame context (iPhone, Android)
- Status bar (shows realistic screen space)
- Multiple states (scroll position, keyboard visible)

**Example:**
```bash
---TASK---
id: mobile-review
backend: gemini
files: ./mobile-home.png, ./mobile-home-scrolled.png, ./mobile-with-keyboard.png
files-mode: embed
---CONTENT---
分析这个移动端设计（3个不同状态）：
1. 首屏内容布局
2. 滚动后的内容展示
3. 键盘弹出时的表单体验
---END---
EOF
```

### Batch Upload

For comprehensive reviews, organize screenshots:

```bash
---TASK---
id: full-app-review
backend: gemini
files: ./screens/01-splash.png, ./screens/02-onboarding.png, ./screens/03-home.png, ./screens/04-product.png, ./screens/05-cart.png
files-mode: embed
---CONTENT---
完整App流程设计审查（5个关键页面）：

为每个页面评估：
1. 与前后页面的连贯性
2. 视觉一致性
3. 交互合理性
4. 改进建议

最后提供整体App设计评分（1-10分）和核心优化方向。
---END---
EOF
```

---

## Visual Annotation Techniques

### 1. Textual Context in Prompt

Provide context that may not be obvious from image:

```bash
---CONTENT---
这是一个健身App的会员升级页面（目标用户：25-35岁健身爱好者）。
当前转化率仅2.5%，低于行业平均5%。

请分析：
1. 哪些设计因素可能导致低转化？
2. 如何优化以提升转化率？
[附上设计稿截图]
---END---
```

### 2. Highlight Key Areas

Use image editing tools to:
- Draw red boxes around problem areas
- Add numbered labels for reference
- Use arrows to indicate flow issues

```bash
---CONTENT---
设计稿中我用红色标注了3个问题区域：
区域1（左上）：导航栏过于拥挤
区域2（中部）：CTA按钮不够突出
区域3（底部）：版权信息占用太多空间

请针对每个区域提供改进方案。
---END---
```

### 3. State Indication

Clarify what state the design represents:

```bash
---CONTENT---
这是登录表单的"错误状态"设计：
- 邮箱格式错误
- 密码长度不足

请评估错误提示的清晰度和友好性。
---END---
```

---

## Use Cases by Design Phase

### Research Phase

**Competitive Screenshots:**
```bash
---TASK---
id: comp-analysis
backend: gemini
files: ./competitor-screenshots/*.png
files-mode: embed
---CONTENT---
分析5个竞品的首页设计，总结行业趋势和最佳实践
---END---
EOF
```

### Ideate Phase

**Inspiration Analysis:**
```bash
---TASK---
id: inspiration
backend: gemini
files: ./inspiration/dribbble-*.png
files-mode: embed
---CONTENT---
从这些设计灵感中提取可借鉴的元素：
- 布局创意
- 交互模式
- 视觉风格
结合我们的品牌，提出3个设计方向
---END---
EOF
```

### Prototype Phase

**Design Review:**
```bash
---TASK---
id: mockup-review
backend: gemini
files: ./mockups/*.png
files-mode: embed
---CONTENT---
审查高保真视觉稿：
1. 品牌一致性
2. 视觉层次
3. 交互清晰度
4. 无障碍性
---END---
EOF
```

### Test Phase

**Usability Issue Documentation:**
```bash
---TASK---
id: usability-issues
backend: gemini
files: ./test-recording-screenshots/*.png
files-mode: embed
---CONTENT---
这些截图来自可用性测试录屏，显示了用户遇到困难的时刻。
分析每个问题点并提出解决方案。
---END---
EOF
```

---

## Advanced Tips

### 1. Combine Text + Image Context

```bash
---CONTENT---
背景：这是一个B2B SaaS产品的定价页面。
目标：提升企业版套餐的购买率（当前占比仅15%）。
用户反馈："价格表太复杂，看不懂区别"

[附上定价页设计稿]

请提供简化建议。
---END---
```

### 2. Sequential Analysis

For multi-step flows:

```bash
---TASK---
id: flow-analysis
backend: gemini
files: ./flow/step1.png, ./flow/step2.png, ./flow/step3.png, ./flow/step4.png
files-mode: embed
---CONTENT---
分析这个4步注册流程：
1. 每一步的摩擦点
2. 步骤间的衔接是否流畅
3. 进度指示是否清晰
4. 如何优化以减少流失？
---END---
EOF
```

### 3. Design System Validation

```bash
---TASK---
id: design-system-check
backend: gemini
files: ./components/*.png
files-mode: embed
---CONTENT---
验证这些组件是否符合我们的设计系统规范：

规范要求：
- 主色：#1E88E5
- 圆角：8px
- 间距：8px倍数
- 字体：Roboto

找出所有不符合规范的组件并列出修改清单。
---END---
EOF
```

---

## Related Resources

- [design-principles.md](./design-principles.md) - Visual hierarchy and color theory
- [design-workflow.md](./design-workflow.md) - When to use image analysis in workflow
- [examples/design-review.md](../examples/design-review.md) - Complete review examples
- [SKILL.md](../SKILL.md) - Gemini basic usage
