# Design Review and Critique Examples

Examples for conducting design reviews, heuristic evaluations, accessibility audits, and visual design critiques using Gemini's multimodal capabilities.

---

## Example 1: Heuristic Evaluation (Nielsen's 10 Heuristics)

Evaluate designs against established usability principles.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: heuristic-eval
backend: gemini
files: ./dashboard-mockup.png
files-mode: embed
workdir: /path/to/reviews
---CONTENT---
使用Nielsen's 10 Heuristics评估这个仪表板设计：

对每一条启发式原则，评估：
1. 符合程度（1-5分，5分最好）
2. 发现的问题
3. 改进建议

10条原则：
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

最后给出总分和优先修复项。
---END---
EOF
```

### Expected Output

```
▶ heuristic-eval (gemini)
  📄 dashboard-mockup.png (245KB)

# 仪表板设计启发式评估报告

## 1. Visibility of System Status (系统状态可见性)

**评分:** ⭐⭐⭐ (3/5)

**符合之处:**
- ✅ 数据图表实时更新，显示最新数据
- ✅ 加载时有Loading动画

**问题:**
- ❌ 数据最后更新时间不明显（需要仔细查找）
- ❌ 没有显示当前页面位置（面包屑导航缺失）

**改进建议:**
- 在仪表板顶部显眼位置显示"最后更新：2分钟前"
- 添加面包屑导航：首页 > 分析 > 销售仪表板

---

## 2. Match Between System and Real World (系统与现实世界匹配)

**评分:** ⭐⭐⭐⭐ (4/5)

**符合之处:**
- ✅ 使用商业术语（"销售额"、"转化率"）而非技术术语
- ✅ 图表类型符合数据特点（趋势用折线图，占比用饼图）

**问题:**
- ⚠️ 货币符号使用"$"，但目标用户可能是中国市场（应使用"¥"）

**改进建议:**
- 根据用户区域自动显示对应货币符号
- 日期格式本地化（YYYY-MM-DD vs MM/DD/YYYY）

---

## 3. User Control and Freedom (用户控制和自由)

**评分:** ⭐⭐ (2/5)

**问题:** 🔴 **高优先级**
- ❌ 时间范围筛选无法撤销（需刷新页面）
- ❌ 删除自定义图表无确认提示，无撤销功能
- ❌ 无法自定义仪表板布局（拖拽调整）

**改进建议:**
- 添加"重置筛选"按钮
- 删除操作增加二次确认："确定删除该图表？ [撤销]"
- 支持拖拽调整图表位置和大小

---

## 4. Consistency and Standards (一致性和标准)

**评分:** ⭐⭐⭐ (3/5)

**符合之处:**
- ✅ 按钮样式统一（主按钮、次要按钮）
- ✅ 图标使用一致（Material Icons）

**问题:**
- ❌ 两个下拉菜单样式不同（左侧是Pill样式，右侧是方形）
- ❌ 百分比格式不一致（"15%"和"15.5%"混用）

**改进建议:**
- 统一所有下拉菜单为相同样式
- 制定数值格式规范（整数无小数点，小数统一保留1位）

---

## 5. Error Prevention (错误预防)

**评分:** ⭐⭐⭐⭐ (4/5)

**符合之处:**
- ✅ 日期选择使用日历组件（防止手动输入错误）
- ✅ 数值输入限制范围（0-100%）

**问题:**
- ⚠️ 导出大数据集无警告（可能导致浏览器卡顿）

**改进建议:**
- 导出超过10000条数据时，提示："数据量较大，导出可能需要1-2分钟，是否继续？"

---

## 6. Recognition Rather Than Recall (识别而非回忆)

**评分:** ⭐⭐⭐⭐ (4/5)

**符合之处:**
- ✅ 时间范围显示预设选项（今天、本周、本月）
- ✅ 最近使用的筛选条件在下拉菜单顶部

**轻微问题:**
- ⚠️ 自定义筛选器命名不够描述性（"筛选器1"、"筛选器2"）

**改进建议:**
- 自动生成描述性名称："销售额>10000 AND 地区=北京"

---

## 7. Flexibility and Efficiency of Use (灵活性和使用效率)

**评分:** ⭐⭐ (2/5)

**问题:** 🔴 **高优先级**
- ❌ 无键盘快捷键（无法快速切换时间范围）
- ❌ 无快速操作（如右键菜单）
- ❌ 高级用户无法直接输入SQL查询

**改进建议:**
- 添加快捷键：T (Today), W (This Week), M (This Month)
- 图表右键菜单：导出、添加到收藏、分享
- 为高级用户提供"SQL模式"切换

---

## 8. Aesthetic and Minimalist Design (美观和极简设计)

**评分:** ⭐⭐⭐ (3/5)

**符合之处:**
- ✅ 配色简洁（蓝色主色调）
- ✅ 留白充足，不拥挤

**问题:**
- ❌ 顶部工具栏有8个按钮，过于复杂（实际只用到3个）
- ❌ 图表标题过长，占用太多空间

**改进建议:**
- 隐藏低频使用的按钮到"更多"菜单
- 简化图表标题："Q1销售额趋势" → "销售额趋势"
- 移除装饰性图标（不传达功能信息）

---

## 9. Help Users Recognize, Diagnose, and Recover from Errors (帮助用户识别、诊断和恢复错误)

**评分:** ⭐⭐ (2/5)

**问题:** 🔴 **高优先级**
- ❌ 错误信息不明确："加载失败"（没说明原因和解决方法）
- ❌ 无数据状态不友好（空白页，无提示）

**改进建议:**
- 改进错误信息："无法加载数据，请检查网络连接或稍后重试 [重新加载]"
- 无数据状态设计：
  ```
  [图标]
  暂无数据
  尝试调整筛选条件或时间范围
  [清除筛选]
  ```

---

## 10. Help and Documentation (帮助和文档)

**评分:** ⭐⭐⭐ (3/5)

**符合之处:**
- ✅ 顶部有"帮助"链接
- ✅ 复杂图表有Tooltip说明

**问题:**
- ⚠️ 帮助文档在外部页面（需离开当前页面）
- ⚠️ 无搜索功能

**改进建议:**
- 添加侧边栏帮助面板（不离开当前页面）
- 提供上下文帮助（"?图标" Tooltip）
- 添加交互式教程（首次使用引导）

---

## 总体评分

**总分:** 30/50 (60%)

**评级:** 🟡 **及格**（需改进）

---

## 优先修复项（按严重程度排序）

### 🔴 高优先级（影响核心功能）

1. **用户控制不足** - 无撤销/重置功能
   - 影响：用户误操作无法恢复，体验极差
   - 修复工时：2天

2. **错误处理差** - 错误信息不明确
   - 影响：用户遇到问题不知如何解决
   - 修复工时：1天

3. **缺少快捷操作** - 无键盘快捷键，效率低
   - 影响：高频用户操作繁琐
   - 修复工时：3天

### 🟡 中优先级（影响体验）

4. **一致性问题** - 下拉菜单样式不统一
   - 影响：视觉混乱，品牌感差
   - 修复工时：0.5天

5. **界面冗余** - 顶部按钮过多
   - 影响：视觉负担，分散注意力
   - 修复工时：1天

### 🟢 低优先级（优化点）

6. **系统状态可见性** - 更新时间不明显
   - 影响：用户不确定数据新鲜度
   - 修复工时：0.5天

---

## 建议行动计划

**第一阶段（本周）:**
- 修复撤销/重置功能
- 改进错误提示文案

**第二阶段（下周）:**
- 添加键盘快捷键
- 统一组件样式

**第三阶段（下月）:**
- 优化帮助文档
- 添加引导教程

» 写入 heuristic-evaluation-report.md
✓ heuristic-eval 18.5s
```

---

## Example 2: Accessibility Audit (WCAG 2.1)

Evaluate designs for accessibility compliance.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: accessibility-audit
backend: gemini
files: ./login-page.png
files-mode: embed
workdir: /path/to/audits
---CONTENT---
对登录页面进行无障碍性审查（WCAG 2.1 Level AA）：

审查项：
1. 色彩对比度（文本/背景）
2. 键盘导航（Tab顺序、焦点可见）
3. 表单标签（Label与Input关联）
4. 错误提示（清晰、可识别）
5. 替代文本（图片alt text）
6. 语义HTML（正确使用heading、button等）
7. 触摸目标大小（移动端≥44×44pt）
8. 屏幕阅读器兼容性

对每一项，评估：
- 是否符合WCAG AA标准
- 发现的问题
- 修复建议（具体代码示例）

生成无障碍审查报告。
---END---
EOF
```

---

## Example 3: Visual Design Critique

Provide constructive feedback on visual design.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: visual-critique
backend: gemini
files: ./home-page-design.png
files-mode: embed
workdir: /path/to/critiques
---CONTENT---
对首页设计进行视觉评审：

评审维度：
1. 视觉层次（标题、正文、CTA的权重分配）
2. 色彩使用（品牌色、对比、和谐度）
3. 字体排版（字号、行高、对齐）
4. 留白和间距（呼吸感、元素分组）
5. 图片和图标（质量、一致性、适配）
6. 整体风格（现代/传统、专业/活泼）

对每个维度：
- 优点（做得好的地方）
- 问题（需要改进的地方）
- 建议（具体修改方案）

最后给出总体印象和核心改进方向。
---END---
EOF
```

---

## Example 4: Competitive Design Analysis

Compare your design with competitors.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: competitive-design
backend: gemini
files: ./our-app.png, ./competitor-a.png, ./competitor-b.png, ./competitor-c.png
files-mode: embed
workdir: /path/to/analysis
---CONTENT---
对比分析我们的App与3个竞品的设计：

对比维度：
1. 首屏信息架构（内容优先级、CTA位置）
2. 导航设计（Tab Bar、侧边栏、汉堡菜单）
3. 视觉风格（色彩、字体、图标）
4. 交互模式（手势、动画、反馈）
5. 空间利用（信息密度、留白）

对每个竞品，评估：
- 优势（值得学习的地方）
- 劣势（我们做得更好的地方）
- 差异化机会（我们可以创新的地方）

最后提出3-5条设计改进建议。
---END---
EOF
```

---

## Example 5: Design System Compliance Check

Verify designs follow design system guidelines.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: design-system-check
backend: gemini
files: ./new-feature-mockup.png
files-mode: embed
workdir: /path/to/checks
---CONTENT---
检查新功能设计是否符合设计系统规范：

设计系统规范：
- 主色：#1E88E5 (蓝色)
- 圆角：8px (按钮/输入框), 12px (卡片)
- 间距：8px的倍数
- 字体：Roboto, 16px正文
- 按钮高度：48px
- 图标尺寸：24px

检查项：
1. 色彩使用（是否使用设计系统定义的颜色）
2. 圆角半径（是否符合规范）
3. 间距系统（是否基于8px grid）
4. 字体大小和行高（是否符合字阶）
5. 组件样式（按钮、输入框是否复用现有组件）

列出所有不符合规范的地方，并提供修改建议。
---END---
EOF
```

---

## Tips for Design Reviews

1. **Heuristic Evaluation**
   - Evaluate against objective criteria (Nielsen's heuristics)
   - Assign severity ratings (critical, moderate, minor)
   - Prioritize fixes by impact and effort
   - Involve multiple reviewers for diverse perspectives

2. **Accessibility Audit**
   - Use automated tools first (WAVE, Axe DevTools)
   - Test with keyboard navigation
   - Test with screen readers (NVDA, VoiceOver)
   - Include users with disabilities in testing

3. **Visual Critique**
   - Be specific ("Button too small" → "Increase button from 40px to 48px")
   - Balance positive and negative feedback
   - Suggest alternatives, not just problems
   - Consider brand and context

4. **Competitive Analysis**
   - Analyze 3-5 direct competitors
   - Use screenshots at same device size
   - Focus on differentiators, not just features
   - Update quarterly as market evolves

5. **Design System Compliance**
   - Create checklist from design system
   - Automate checks where possible (Figma plugins)
   - Review before development handoff
   - Track compliance over time

---

## Related Resources

- [references/design-principles.md](../references/design-principles.md) - Nielsen's heuristics details
- [references/multimodal-tips.md](../references/multimodal-tips.md) - Image analysis techniques
- [examples/component-systems.md](./component-systems.md) - Design system reference
- [SKILL.md](../SKILL.md) - Gemini multimodal usage
