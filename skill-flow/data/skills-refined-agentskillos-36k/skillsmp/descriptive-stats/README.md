# 描述性统计分析 Skill

产品级的描述性统计分析工具，支持CSV和Excel数据的交互式分析。

## 功能特性

- **基础描述统计**: 均值、中位数、标准差、分位数、偏度、峰度
- **分布分析**: 正态性检验、直方图、密度图、Q-Q图
- **异常值检测**: IQR方法、Z-score方法、共识检测
- **分组对比**: ANOVA、Kruskal-Wallis检验、箱线图、小提琴图
- **双输出模式**: 终端彩色表格 + HTML交互报告
- **交互式引导**: 友好的命令行交互界面

## 安装

### 依赖安装

```bash
# 安装Python依赖
cd ~/.claude/skills/descriptive-stats
pip3 install -r requirements.txt
```

### 依赖包

- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- seaborn >= 0.12.0
- matplotlib >= 3.7.0
- plotly >= 5.14.0
- rich >= 13.7.0
- jinja2 >= 3.1.0
- openpyxl >= 3.1.0

## 快速开始

### 基本用法

在Claude Code中直接请求数据分析：

```
请分析 data.csv 的统计特征
对数据进行描述性统计分析
查看数据的分布情况
检测数据中的异常值
```

### 指定文件分析

```
分析 /path/to/sales_data.csv 的统计特征
对 /path/to/employee_data.xlsx 进行完整分析
```

### 分组分析

```
按部门分组分析薪资数据
比较不同产品类别的评分分布
```

## 使用模式

### 交互式模式

推荐用于探索性分析，skill会引导完成：

1. 选择数据文件
2. 预览数据并选择分析列
3. 选择分析类型
4. 选择输出方式
5. 查看和解释结果

### 直接模式

指定文件和分析参数：

```
分析 data.csv 的所有数值列，生成HTML报告
```

## 命令行使用

skill也可以作为独立Python脚本使用：

```bash
# 进入scripts目录
cd ~/.claude/skills/descriptive-stats/scripts

# 运行分析（开发中）
python3 cli.py analyze ../data.csv --output report.html
```

## 数据格式支持

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| CSV | .csv | 逗号分隔值，UTF-8编码 |
| Excel | .xlsx, .xls | 支持多sheet工作簿 |

## 输出格式

### 终端输出
- Rich彩色表格
- ASCII风格图表
- 进度条和加载动画
- 分页显示

### HTML报告
- 响应式布局
- Plotly交互式图表
- 完整统计报告
- 可导出为PDF

## 分析类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| 基础统计 | 计算描述性统计量 | 快速了解数据特征 |
| 分布分析 | 检验分布形状 | 判断数据分布类型 |
| 异常值检测 | 识别异常观测 | 数据清洗和质量检查 |
| 分组对比 | 组间差异检验 | A/B测试、分组研究 |

## 示例数据

skill包含测试数据用于演示：

```bash
# 使用测试数据
分析 ~/.claude/skills/descriptive-stats/examples/test_data.csv
```

## 目录结构

```
descriptive-stats/
├── SKILL.md              # Skill定义文件
├── README.md             # 本文档
├── requirements.txt      # Python依赖
├── references/           # 参考文档
│   ├── statistical-methods.md
│   ├── visualizations.md
│   └── best-practices.md
├── examples/             # 使用示例
│   ├── basic-analysis.md
│   └── advanced-analysis.md
└── scripts/              # 分析脚本
    ├── cli.py           # 主入口
    ├── core/            # 核心分析
    ├── visualization/   # 可视化
    └── reporting/       # 报告生成
```

## 统计方法说明

### 中心趋势
- **均值**: 正态分布数据的代表值
- **中位数**: 偏态分布，抗异常值
- **众数**: 最频繁出现的值

### 离散程度
- **标准差**: 数据平均偏离程度
- **IQR**: 中间50%数据的范围
- **变异系数**: 相对变异程度

### 分布形状
- **偏度**: 分布对称性，正值右偏
- **峰度**: 分布尖锐程度

### 正态性检验
- **Shapiro-Wilk**: 小样本首选
- **K-S检验**: 大样本适用
- **D'Agostino**: 基于偏度和峰度

### 异常值检测
- **IQR方法**: Q1-1.5×IQR 或 Q3+1.5×IQR
- **Z-score**: |Z| > 3 视为异常
- **共识**: 多方法交集

### 组间检验
- **ANOVA**: 参数检验，正态+方差齐
- **Kruskal-Wallis**: 非参数，任意分布

## 最佳实践

1. **先做数据质量检查**: 了解缺失值和异常值
2. **选择合适的统计量**: 偏态用中位数，正态用均值
3. **可视化辅助理解**: 图表比数字更直观
4. **报告效应量**: 不仅看显著性，更要看实际意义
5. **结合领域知识**: 统计结果需要专业解释

## 常见问题

**Q: 支持大数据集吗？**
A: 支持自动采样和增量计算，适合大型数据集。

**Q: 可以处理中文数据吗？**
A: 完全支持中文列名和数据，使用UTF-8编码。

**Q: 如何引用分析结果？**
A: HTML报告包含完整方法和参数，可直接引用。

**Q: 分析结果可靠吗？**
A: 使用成熟的统计库（scipy、statsmodels），方法经过验证。

## 进阶使用

### 自定义分析参数
```
分析data.csv，使用95%置信区间，异常值阈值为2.5倍标准差
```

### 批量分析
```
分析当前目录所有csv文件的统计特征
```

### 自定义报告模板
编辑 `scripts/reporting/templates/report.html` 自定义报告样式。

## 技术支持

- 详细统计方法: `references/statistical-methods.md`
- 可视化指南: `references/visualizations.md`
- 使用示例: `examples/`

## 版本历史

- **1.0.0** (2025): 初始版本
  - 基础描述统计
  - 分布分析
  - 异常值检测
  - 分组对比
  - HTML报告生成

## 许可证

作为Claude Code skill使用，遵循相应许可条款。

## 贡献

改进建议和问题反馈请通过Claude Code渠道提交。
