# 图表示例文件索引

HTML Presentation Beautifier 提供了完整的 McKinsey 风格图表示例，方便参考和使用。

## 📁 示例文件清单

| 文件名 | 大小 | 图表类型 | 描述 |
|--------|------|---------|------|
| `pyramid-chart-example.html` | ~20KB | 金字塔图 | 层次结构、需求层次、优先级排序 |
| `gauge-chart-example.html` | ~18KB | 仪表盘 | KPI 指标、目标完成度、绩效评分 |
| `venn-diagram-example.html` | ~16KB | 韦恩图 | 集合关系、市场重叠、技能组合 |
| `timeline-example.html` | ~19KB | 时间轴 | 项目里程碑、发展历程、产品路线图 |
| `flowchart-example.html` | ~17KB | 流程图 | 业务流程、决策流程、审批流程 |
| `funnel-chart-example.html` | ~18KB | 漏斗图 | 销售漏斗、用户转化、营销效果 |

## 🎯 快速使用

### 查看示例

在浏览器中打开任意示例文件：

```bash
cd /Users/wxj/ai-task/minto-plugin-tools/html-presentation-beautifier/skills/assets
open pyramid-chart-example.html
open gauge-chart-example.html
open venn-diagram-example.html
open timeline-example.html
open flowchart-example.html
open funnel-chart-example.html
```

### 复制代码到项目

从示例文件中复制以下内容：

1. **CSS 样式**：`<style>` 标签内的所有样式
2. **HTML 结构**：图表容器的 HTML 结构
3. **JavaScript**：图表渲染脚本（如有）

## 📊 图表类型详解

### 1. 金字塔图

**文件**：`pyramid-chart-example.html`

**特点**：
- 使用 CSS `clip-path` 创建真实三角形
- 三层结构，从上到下递减
- McKinsey 配色：橙→蓝→绿

**适用场景**：
- 需求层次（马斯洛）
- 产品定位（基础→高级）
- 市场细分（大众→高端）

**核心代码**：
```css
clip-path: polygon(50% 0%, 0% 100%, 100% 100%); /* 顶层 */
clip-path: polygon(25% 0%, 75% 0%, 100% 100%, 0% 100%); /* 中层 */
```

---

### 2. 仪表盘

**文件**：`gauge-chart-example.html`

**特点**：
- 半圆形速度计样式
- 基于 Chart.js 环形图
- 动态颜色：达成（绿）、接近（蓝）、未达标（红）

**适用场景**：
- KPI 完成率
- 客户满意度评分
- 生产效率指标

**核心配置**：
```javascript
{
    type: 'doughnut',
    options: {
        circumference: 180,  // 半圆
        rotation: 270,       // 从左侧开始
        cutout: '75%'        // 中心孔径
    }
}
```

---

### 3. 韦恩图

**文件**：`venn-diagram-example.html`

**特点**：
- 纯 CSS 实现，无 JavaScript 依赖
- 支持 2-3 个集合
- 20% 透明度展示重叠区域

**适用场景**：
- 市场定位重叠
- 产品功能对比
- 团队技能互补

**核心代码**：
```css
.venn-set {
    border-radius: 50%;
    background: rgba(85, 110, 230, 0.2);
    border: 3px solid #556EE6;
}
```

---

### 4. 时间轴

**文件**：`timeline-example.html`

**特点**：
- 垂直时间线布局
- 左右交替内容展示
- 圆点 + 箭头连接

**适用场景**：
- 项目里程碑
- 公司发展历程
- 产品版本演进

**核心结构**：
```css
.timeline::before {
    left: 50%;
    width: 3px;
    background: #556EE6;
}
.timeline-content {
    width: 45%;
}
.timeline-left { left: 0; }
.timeline-right { left: 55%; }
```

---

### 5. 流程图

**文件**：`flowchart-example.html`

**特点**：
- 4 种节点类型（开始、过程、决策、结束）
- 垂直流程布局
- 箭头连接节点

**适用场景**：
- 业务流程设计
- 审批流程
- 决策树

**节点形状**：
- **开始/结束**：圆角矩形
- **过程**：矩形
- **决策**：菱形（旋转 45°）

---

### 6. 漏斗图

**文件**：`funnel-chart-example.html`

**特点**：
- 横向条形图，宽度递减
- 基于 Chart.js 实现
- 自动计算转化率

**适用场景**：
- 销售漏斗
- 用户转化
- 营销活动效果

**核心配置**：
```javascript
{
    type: 'bar',
    options: {
        indexAxis: 'y',  // 横向
        barPercentage: [0.8, 0.7, 0.6, 0.5, 0.4]  // 宽度递减
    }
}
```

## 🎨 McKinsey 配色方案

所有示例统一使用 McKinsey 标准配色：

```css
--accent-primary: #F85d42;   /* 橙红色 - 主强调色 */
--accent-blue: #556EE6;      /* 深蓝色 - 次强调色 */
--accent-green: #34c38f;     /* 绿色 - 成功/增长 */
--accent-blue-light: #50a5f1; /* 浅蓝色 - 中性强调 */
--accent-yellow: #f1b44c;    /* 黄色 - 警告/注意 */
--text-light: #74788d;       /* 灰色 - 辅助文本 */
```

## 📐 设计规范

### 通用原则

1. **简洁设计**：避免过度装饰，突出数据本身
2. **清晰标注**：每个图表都有明确的标题和数据标签
3. **视觉层次**：使用颜色、大小、字重区分信息重要性
4. **响应式布局**：适配不同屏幕尺寸
5. **交互效果**：适当的悬停效果增强用户体验

### 排版规范

- **标题**：48px，粗体，黑色
- **副标题**：32px，粗体，强调色
- **正文**：16px，常规字重，深灰色
- **标签**：14px，清晰易读

## 🚀 在项目中使用

### 方法 1：直接引用

将示例文件作为模板，修改数据部分：

```bash
cp skills/assets/pyramid-chart-example.html my_presentation.html
# 编辑 my_presentation.html，修改数据和标题
```

### 方法 2：复制代码

从示例中复制需要的代码片段：

1. 复制 CSS 到 `<style>` 标签
2. 复制 HTML 结构到 `<body>`
3. 复制 JavaScript 到 `<script>` 标签

### 方法 3：使用生成器

通过 Python 脚本自动生成：

```bash
python3 skills/scripts/generator_v3.py parsed_data.json output.html
```

## 📚 相关资源

- **实现指南**：`PYRAMID_CHART_GUIDE.md`
- **技术文档**：`CHART_TYPES_ANALYSIS.md`
- **主文档**：`../../SKILL.md`
- **测试数据**：`test_new_charts.json`

## 🔄 更新日志

### v1.0 (2026-01-21)
- ✅ 创建金字塔图示例
- ✅ 创建仪表盘示例
- ✅ 创建韦恩图示例
- ✅ 创建时间轴示例
- ✅ 创建流程图示例
- ✅ 创建漏斗图示例
- ✅ 统一 McKinsey 设计风格
- ✅ 完整的使用说明和技术文档

---

**维护者**：HTML Presentation Beautifier Team  
**最后更新**：2026 年 1 月 21 日  
**版本**：v1.0
