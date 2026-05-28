# Presentation Template 使用指南

## 📄 模板文件

**文件名**：`presentation-template.html`
**大小**：22KB
**行数**：740 行
**用途**：生成 McKinsey 风格 HTML 演示文稿的基础模板

---

## 🎯 模板特性

### ✅ 完整功能
- **McKinsey/BCG 设计系统**：专业配色和排版
- **响应式布局**：适配桌面、平板、手机
- **导航控制**：按钮导航 + 键盘快捷键
- **幻灯片计数器**：显示当前页/总页数
- **全屏模式**：支持全屏演示
- **Chart.js 集成**：数据可视化支持
- **打印优化**：支持打印输出

### 🎨 设计系统

#### 配色方案
```css
--primary-bg: #FFFFFF;       /* 主背景 */
--header-bg: #000000;        /* 标题栏背景 */
--primary-accent: #F85d42;   /* 主强调色（橙红） */
--secondary-accent: #74788d; /* 次强调色（灰） */
--deep-blue: #556EE6;        /* 深蓝色 */
--green: #34c38f;            /* 绿色 */
--blue: #50a5f1;             /* 蓝色 */
--yellow: #f1b44c;           /* 黄色 */
```

#### 排版规范
- **标题幻灯片标题**：64px，粗体，白色
- **内容幻灯片标题**：48px，粗体，黑色
- **副标题**：32px，粗体，强调色
- **章节标题**：24px，粗体，深蓝色
- **正文**：20px，常规，深灰色
- **列表项**：20px，带项目符号

---

## 🚀 使用方法

### 方法 1：占位符替换（推荐）

模板中使用 `{{PLACEHOLDER}}` 占位符，可以直接替换：

```html
<!-- 原始模板 -->
<h1 class="title">{{MAIN_TITLE}}</h1>

<!-- 替换后 -->
<h1 class="title">简优战略方向梳理</h1>
```

**主要占位符**：
- `{{PRESENTATION_TITLE}}` - 演示文稿标题（浏览器标签）
- `{{MAIN_TITLE}}` - 主标题
- `{{SUBTITLE}}` - 副标题
- `{{SECTION_TITLE}}` - 章节标题
- `{{BULLET_POINT_N}}` - 列表项
- `{{CHART_TITLE}}` - 图表标题
- `{{CONCLUSION_N_TITLE}}` - 结论标题
- `{{CONCLUSION_N_TEXT}}` - 结论内容

### 方法 2：完整生成

1. **读取模板**
```javascript
// 读取模板文件
ctemplate = readFile('presentation-template.html');
```

2. **提取基础结构**
```javascript
// 提取 <head> 部分（CSS 样式）
const headSection = extractBetween(template, '<head>', '</head>');

// 提取导航栏
const navbar = extractBetween(template, '<nav class="navbar">', '</nav>');

// 提取 JavaScript
const scripts = extractBetween(template, '<script>', '</script>');
```

3. **生成幻灯片**
```javascript
// 根据文档内容生成幻灯片
const slides = generateSlides(documentContent);
```

4. **组装 HTML**
```javascript
const finalHTML = `
<!DOCTYPE html>
<html>
${headSection}
<body>
    ${navbar}
    <div class="presentation-container">
        ${slides.join('\n')}
    </div>
    <button class="fullscreen-btn" onclick="toggleFullscreen()">全屏 ⛶</button>
    ${scripts}
</body>
</html>
`;
```

---

## 📐 幻灯片类型模板

### 1. 标题幻灯片（Title Slide）

```html
<div class="slide title-slide active" data-slide="1">
    <h1 class="title">演示文稿主标题</h1>
    <p class="subtitle">副标题或日期</p>
</div>
```

**适用场景**：演示文稿第一张

---

### 2. 内容幻灯片 - 项目符号列表

```html
<div class="slide" data-slide="2">
    <h2 class="slide-title">章节标题</h2>
    <ul class="bullet-list">
        <li>第一个要点</li>
        <li>第二个要点</li>
        <li>第三个要点</li>
    </ul>
</div>
```

**适用场景**：列表型内容

---

### 3. 内容幻灯片 - 编号列表

```html
<div class="slide" data-slide="3">
    <h2 class="slide-title">实施步骤</h2>
    <ol class="numbered-list">
        <li>第一步：需求分析</li>
        <li>第二步：方案设计</li>
        <li>第三步：实施落地</li>
    </ol>
</div>
```

**适用场景**：步骤、流程、排序内容

---

### 4. 两栏布局幻灯片

```html
<div class="slide" data-slide="4">
    <h2 class="slide-title">对比分析</h2>
    <div class="two-column">
        <div class="column">
            <h3 class="section-heading">方案 A</h3>
            <ul class="bullet-list">
                <li>优点 1</li>
                <li>优点 2</li>
            </ul>
        </div>
        <div class="column">
            <h3 class="section-heading">方案 B</h3>
            <ul class="bullet-list">
                <li>优点 1</li>
                <li>优点 2</li>
            </ul>
        </div>
    </div>
</div>
```

**适用场景**：对比、并列内容

---

### 5. 数据可视化幻灯片

```html
<div class="slide" data-slide="5">
    <h2 class="slide-title">市场数据分析</h2>
    <div class="chart-container">
        <canvas id="chart1"></canvas>
    </div>
</div>

<script>
// 在 initializeCharts() 函数中添加
const chart1 = new Chart(document.getElementById('chart1'), {
    type: 'bar',
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
            label: '销售额',
            data: [120, 150, 180, 200],
            backgroundColor: '#F85d42'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
</script>
```

**适用场景**：数据图表展示

---

### 6. 强调框幻灯片

```html
<div class="slide" data-slide="6">
    <h2 class="slide-title">核心洞察</h2>
    <div class="emphasis-container">
        <div class="emphasis-box">
            <div class="emphasis-icon">💡</div>
            <div class="emphasis-text">第一个核心洞察</div>
        </div>
        <div class="emphasis-box">
            <div class="emphasis-icon">🎯</div>
            <div class="emphasis-text">第二个核心洞察</div>
        </div>
        <div class="emphasis-box">
            <div class="emphasis-icon">✨</div>
            <div class="emphasis-text">第三个核心洞察</div>
        </div>
    </div>
</div>
```

**适用场景**：关键要点、洞察、结论

**可用图标**：
- 💡 创意、洞察
- 🎯 目标、重点
- ✨ 亮点、特色
- 📊 数据、分析
- 🚀 增长、发展
- ⚡ 快速、效率
- 🔍 发现、研究
- 💰 财务、收益
- 👥 团队、用户
- 🌟 优势、价值

---

### 7. 结论卡片网格幻灯片

```html
<div class="slide" data-slide="7">
    <h2 class="slide-title">核心结论</h2>
    <div class="conclusions-grid">
        <div class="conclusion-card">
            <div class="conclusion-number">01</div>
            <h3 class="conclusion-title">结论标题一</h3>
            <p class="conclusion-text">详细说明文本内容</p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-number">02</div>
            <h3 class="conclusion-title">结论标题二</h3>
            <p class="conclusion-text">详细说明文本内容</p>
        </div>
        <div class="conclusion-card">
            <div class="conclusion-number">03</div>
            <h3 class="conclusion-title">结论标题三</h3>
            <p class="conclusion-text">详细说明文本内容</p>
        </div>
    </div>
</div>
```

**适用场景**：总结、结论、关键发现

---

### 8. 数据表格幻灯片

```html
<div class="slide" data-slide="8">
    <h2 class="slide-title">数据对比</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th>项目</th>
                <th>2023</th>
                <th>2024</th>
                <th>增长率</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>收入</td>
                <td>$100M</td>
                <td>$150M</td>
                <td>+50%</td>
            </tr>
            <tr>
                <td>利润</td>
                <td>$20M</td>
                <td>$35M</td>
                <td>+75%</td>
            </tr>
        </tbody>
    </table>
</div>
```

**适用场景**：数据对比、详细数据

---

## ⌨️ 键盘快捷键

| 按键 | 功能 |
|------|------|
| `→` 或 `Space` | 下一张幻灯片 |
| `←` | 上一张幻灯片 |
| `Home` | 跳转到第一张 |
| `End` | 跳转到最后一张 |
| `Esc` | 退出全屏 |

---

## 🎨 自定义样式

### 修改配色

在 `<style>` 标签的 `:root` 部分修改颜量：

```css
:root {
    --primary-accent: #FF6B6B;  /* 改为红色系 */
    --deep-blue: #4ECDC4;       /* 改为青色系 */
}
```

### 修改字体大小

```css
.slide-title {
    font-size: 56px;  /* 原来是 48px */
}

.bullet-list li {
    font-size: 22px;  /* 原来是 20px */
}
```

### 修改布局间距

```css
.slide {
    padding: 100px 120px;  /* 原来是 80px 100px */
}
``--

## 📊 Chart.js 图表类型

模板已集成 Chart.js，支持以下图表类型：

### 柱状图（Bar Chart）
```javascript
type: 'bar',
data: {
    labels: ['A', 'B', 'C'],
    datasets: [{
        data: [10, 20, 30],
        backgroundColor: '#F85d42'
    }]
}
```

### 折线图（Line Chart）
```javascript
type: 'line',
data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
        data: [10, 20, 15],
        borderColor: '#556EE6',
        fill: false
    }]
}
```

### 饼图（Pie Chart）
```javascript
type: 'pie',
data: {
    labels: ['A', 'B', 'C'],
    datasets: [{
        data: [30, 50, 20],
        backgroundColor: ['#F85d42', '#556EE6', '#34c38f']
    }]
}
```

### 环形图（Doughnut Chart）
```javascript
type: 'doughnut',
data: {
    labels: ['A', 'B', 'C'],
    datasets: [{
        data: [30, 50, 20],
        backgroundColor: ['#F85d42', '#556EE6', '#34c38f']
    }]
}
```

更多图表类型和配置，参考 [Chart.js 文档](https://www.chartjs.org/docs/)

---

## 🔧 常见问题

### Q: 如何添加更多幻灯片？

A: 复制现有幻灯片模板，修改 `data-slide` 属性为递增数字：

```html
<div class="slide" data-slide="9">
    <!-- 内容 -->
</div>
```

### Q: 如何隐藏某张幻灯片？

A: 删除该幻灯片的 `<div class="slide">` 块即可。

### Q: 图表不显示怎么办？

A: 检查：
1. Chart.js CDN 是否加载成功
2. `canvas` 元素 ID 是否唯一
3. `initializeCharts()` 函数中是否正确初始化

### Q: 如何导出为 PDF？

A: 使用浏览器打印功能（Ctrl+P / Cmd+P），选择"另存为 PDF"。

### Q: 如何修改幻灯片切换动画？

A: 修改 `.slide` 的 `transition` 属性：

```css
.slide {
    transition: opacity 0.8s ease;  /* 改为 0.8 秒 */
}
```

---

## 📝 完整示例

参考 `chart-examples.html` 和其他示例文件：

- `pyramid-chart-example.html` - 金字塔图
- `funnel-chart-example.html` - 漏斗图
- `timeline-example.html` - 时间轴
- `mindmap-example.html` - 思维导图
- 更多示例见 `CHART_EXAMPLES_INDEX.md`

---

## 🎯 最佳实践

1. **内容为王**：确保每张幻灯片信息清晰、重点突出
2. **视觉层次**：使用标题、副标题、正文建立层次
3. **适度使用颜色**：主要用强调色突出关键信息
4. **图表优于文字**：数据尽量用图表展示
5. **保持一致性**：统一使用模板提供的样式
6. **测试响应式**：在不同设备上测试显示效果
7. **控制内容量**：每张幻灯片不超过 5-7 个要点

---

## 📚 相关资源

- **SKILL.md** - 完整的插件使用指南
- **CHART_EXAMPLES_INDEX.md** - 图表示例索引
- **INSIGHT_VISUALIZATION_GUIDE.md** - 观点可视化指南
- **Chart.js 官方文档** - https://www.chartjs.org/

---

**最后更新**：2026-01-25
**模板版本**：v1.0
**维护者**：HTML Presentation Beautifier Team
