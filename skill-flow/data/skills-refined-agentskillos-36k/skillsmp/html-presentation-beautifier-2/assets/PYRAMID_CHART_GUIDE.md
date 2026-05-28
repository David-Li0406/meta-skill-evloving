# 金字塔概念图实现指南

## 概述

金字塔概念图是一种使用三角形层级展示层次结构、优先级或递进关系的可视化图表。本指南基于 McKinsey 设计风格，使用 CSS `clip-path` 属性创建真实的三角形形状。

## 核心特性

- ✅ **真实三角形**：使用 CSS clip-path 创建真正的三角形，而非矩形
- ✅ **McKinsey 配色**：专业的配色方案（橙色、蓝色、绿色）
- ✅ **交互效果**：悬停放大、阴影增强
- ✅ **响应式设计**：自动适配不同屏幕尺寸
- ✅ **灵活配置**：支持 3-5 层金字塔结构

## 文件清单

```
skills/assets/
├── pyramid-chart-example.md      # 使用场景说明文档
├── pyramid-chart-example.html    # 完整 HTML 示例（3 个示例）
└── PYRAMID_CHART_GUIDE.md        # 本实现指南
```

## 快速开始

### 1. 查看 HTML 示例

在浏览器中打开 `pyramid-chart-example.html` 查看完整示例：

```bash
open /Users/wxj/ai-task/minto-plugin-tools/html-presentation-beautifier/skills/assets/pyramid-chart-example.html
```

### 2. 复制代码到项目

从 HTML 示例中复制以下部分到你的项目：

- CSS 样式（`<style>` 标签内容）
- HTML 结构（`.pyramid-container` 和 `.pyramid-level`）

### 3. 自定义内容

修改金字塔各层的文本和数据：

```html
<div class="pyramid-level py-level-1">
    顶层标题<br>
    <span style="font-size: 0.85em;">(数据说明)</span>
</div>
```

## CSS 核心代码

### 三角形实现（clip-path）

```css
/* 顶层 - 倒三角形 */
.py-level-1 {
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

/* 中层 - 梯形 */
.py-level-2 {
    clip-path: polygon(25% 0%, 75% 0%, 100% 100%, 0% 100%);
}

/* 底层 - 宽梯形 */
.py-level-3 {
    clip-path: polygon(16.67% 0%, 83.33% 0%, 100% 100%, 0% 100%);
}
```

### McKinsey 配色

```css
:root {
    --accent-primary: #F85d42;  /* 橙红色 - 顶层 */
    --accent-blue: #556EE6;     /* 深蓝色 - 中层 */
    --accent-green: #34c38f;    /* 绿色 - 底层 */
    --accent-blue-light: #50a5f1; /* 浅蓝色 - 可选 */
    --accent-yellow: #f1b44c;   /* 黄色 - 可选 */
}
```

### 尺寸规范

| 层级 | 宽度 | 高度 | 字体 | top 位置 |
|------|------|------|------|----------|
| 顶层 | 140px | 80px | 13px | 0px |
| 中层 | 280px | 90px | 15px | 95px |
| 底层 | 420px | 100px | 17px | 200px |

### 交互效果

```css
.pyramid-level:hover {
    transform: translateX(-50%) scale(1.05);
    box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    z-index: 10;
}
```

## HTML 结构

```html
<div class="pyramid-container">
    <div class="pyramid-wrapper">
        <!-- 顶层 -->
        <div class="pyramid-level py-level-1">
            标题文本<br>
            <span style="font-size: 0.85em;">(数据说明)</span>
        </div>
        
        <!-- 中层 -->
        <div class="pyramid-level py-level-2">
            标题文本<br>
            <span style="font-size: 0.85em;">(数据说明)</span>
        </div>
        
        <!-- 底层 -->
        <div class="pyramid-level py-level-3">
            标题文本
        </div>
    </div>
</div>
```

## 应用场景

### ✅ 适用场景

1. **需求层次**：马斯洛需求理论、用户价值分层
2. **产品定位**：入门版 → 专业版 → 旗舰版
3. **市场细分**：大众市场 → 中端市场 → 高端市场
4. **技术成熟度**：基础技术 → 应用技术 → 前沿技术
5. **组织架构**：高层管理 → 中层管理 → 基层执行
6. **优先级排序**：P0 紧急 → P1 重要 → P2 一般

### ❌ 不适用场景

- **平等关系的数据** → 使用饼图、环形图
- **时间序列数据** → 使用折线图、柱状图
- **多维对比** → 使用雷达图
- **流程流向** → 使用流程图、桑基图

## 示例展示

### 示例 1：AI 儿童玩具需求层次

```
        情感陪伴
       (增长 173%)
         /   \
        /     \
   教育认知 (50%)
    /           \
   /             \
 基础娱乐
```

### 示例 2：企业战略金字塔

```
      愿景使命
     (10 年目标)
       /   \
      /     \
  战略目标 (3-5 年)
   /           \
  /             \
执行计划 (年度 OKR)
```

### 示例 3：产品功能金字塔

```
    AI 智能功能
   (自适应学习)
      /   \
     /     \
  交互功能
 (语音对话)
  /       \
 /         \
基础功能
(播放、灯光)
```

## 最佳实践

### 1. 层次数量
- **建议**：3-5 层
- **原因**：过多会导致视觉拥挤，文本难以阅读

### 2. 文本长度
- **建议**：每层 10-15 字以内
- **原因**：保持简洁，突出重点

### 3. 色彩选择
- **建议**：从上到下使用渐变色或对比色
- **原因**：增强视觉层次感

### 4. 数据标注
- **建议**：在每层添加关键数据指标
- **示例**：增长率、占比、时间范围

### 5. 响应式设计
- **建议**：在小屏幕上自动缩小尺寸
- **实现**：使用媒体查询调整宽度和字体

### 6. 交互效果
- **建议**：添加悬停效果
- **实现**：scale(1.05) + 增强阴影

## 扩展层数

如需添加第 4、第 5 层，参考以下配置：

### 第 4 层

```css
.py-level-4 {
    top: 310px;
    width: 560px;
    height: 110px;
    background-color: var(--accent-blue-light);
    font-size: 19px;
    clip-path: polygon(12.5% 0%, 87.5% 0%, 100% 100%, 0% 100%);
    padding: 10px 80px 40px 80px;
}
```

### 第 5 层

```css
.py-level-5 {
    top: 435px;
    width: 700px;
    height: 120px;
    background-color: var(--accent-yellow);
    font-size: 21px;
    clip-path: polygon(10% 0%, 90% 0%, 100% 100%, 0% 100%);
    padding: 10px 100px 50px 100px;
}
```

## 浏览器兼容性

| 浏览器 | clip-path 支持 |
|--------|----------------|
| Chrome 55+ | ✅ 完全支持 |
| Firefox 54+ | ✅ 完全支持 |
| Safari 9.1+ | ✅ 完全支持 |
| Edge 79+ | ✅ 完全支持 |
| IE 11 | ❌ 不支持 |

## 故障排除

### 问题 1：三角形显示为矩形

**原因**：浏览器不支持 clip-path

**解决方案**：
- 升级到现代浏览器
- 或使用降级方案（border 方式创建三角形）

### 问题 2：文本位置不居中

**原因**：padding 值不正确

**解决方案**：
- 调整 padding-top 和 padding-bottom
- 顶层：padding: 40px 20px 10px 20px
- 中层：padding: 10px 40px 20px 40px
- 底层：padding: 10px 60px 30px 60px

### 问题 3：悬停效果不明显

**原因**：z-index 值太低

**解决方案**：
```css
.pyramid-level:hover {
    z-index: 10; /* 确保在顶层 */
}
```

## 相关资源

- **MDN 文档**：https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path
- **CSS Tricks**：https://css-tricks.com/clipping-masking-css/
- **示例文件**：`pyramid-chart-example.html`
- **场景说明**：`pyramid-chart-example.md`

## 更新日志

### v1.0 (2026-01-21)
- ✅ 初始版本
- ✅ 支持 3 层金字塔
- ✅ McKinsey 风格配色
- ✅ 交互效果
- ✅ 响应式设计
- ✅ 3 个完整示例

---

**维护者**：HTML Presentation Beautifier Team  
**最后更新**：2026 年 1 月 21 日
