"""业务语言解释模块 - 将统计指标转化为业务洞察

这个模块负责将统计学术语转化为业务人员可以理解的语言，
并提供基于数据的业务洞察和建议。
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from dataclasses import dataclass, asdict


@dataclass
class BusinessInsight:
    """业务洞察数据类"""
    category: str  # 洞察类别：central_trend, variability, distribution, outliers
    level: str  # 重要程度：critical, warning, info, success
    title: str  # 简短标题
    description: str  # 详细描述（业务语言）
    suggestion: Optional[str] = None  # 建议措施

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return asdict(self)


def interpret_basic_stats(series: pd.Series, stats: Dict[str, float],
                         column_name: str = "数据") -> List[BusinessInsight]:
    """解释基础统计量的业务含义

    Args:
        series: 数据系列
        stats: 统计量字典
        column_name: 列名（用于生成描述）

    Returns:
        业务洞察列表
    """
    insights = []
    count = stats.get('count', 0)
    mean = stats.get('mean')
    median = stats.get('median')
    std = stats.get('std')
    cv = stats.get('cv')  # 变异系数

    # 1. 中心趋势分析
    if mean is not None and median is not None:
        if abs(mean - median) / median < 0.05:  # 差异小于5%
            insights.append(BusinessInsight(
                category="central_trend",
                level="info",
                title="数据分布相对集中",
                description=f'"{column_name}"的平均值（{mean:.2f}）和中位数（{median:.2f}）非常接近，'
                           f'说明数据分布比较对称，大多数数据点集中在中心位置。'
                           f'可以用平均值作为该指标的代表性数值。'
            ))
        elif mean > median:
            ratio = (mean - median) / median * 100
            insights.append(BusinessInsight(
                category="central_trend",
                level="warning" if ratio > 20 else "info",
                title="数据存在高值拉动",
                description=f'"{column_name}"的平均值（{mean:.2f}）明显高于中位数（{median:.2f}），'
                           f'高出{ratio:.1f}%。这表明存在一些较高的数值拉动了平均值，'
                           f'大部分实际数据可能低于平均值。建议更多关注中位数，'
                           f'它更能代表"典型"情况。'
            ))
        else:  # mean < median
            ratio = (median - mean) / median * 100
            insights.append(BusinessInsight(
                category="central_trend",
                level="warning" if ratio > 20 else "info",
                title="数据存在低值拖累",
                description=f'"{column_name}"的平均值（{mean:.2f}）明显低于中位数（{median:.2f}），'
                           f'低了{ratio:.1f}%。这表明存在一些较低的数值拖累了平均值。'
                           f'实际表现可能比平均值显示的要好。'
            ))

    # 2. 波动性分析
    if std is not None and mean is not None and mean != 0:
        cv_percent = (std / mean) * 100
        if cv_percent < 15:
            insights.append(BusinessInsight(
                category="variability",
                level="success",
                title="数据波动很小，表现稳定",
                description=f'"{column_name}"的变异系数为{cv_percent:.1f}%，'
                           f'说明数据非常稳定，各数据点之间的差异很小。'
                           f'这通常意味着该指标可控性强，预测准确性高。'
            ))
        elif cv_percent < 30:
            insights.append(BusinessInsight(
                category="variability",
                level="info",
                title="数据波动适中",
                description=f'"{column_name}"的变异系数为{cv_percent:.1f}%，'
                           f'属于正常波动范围。数据有一定变化，但整体可控。'
            ))
        elif cv_percent < 60:
            insights.append(BusinessInsight(
                category="variability",
                level="warning",
                title="数据波动较大",
                description=f'"{column_name}"的变异系数为{cv_percent:.1f}%，'
                           f'说明数据波动较大，不同数据点之间存在明显差异。'
                           f'这可能意味着该指标受多种因素影响，需要进一步分析波动原因。'
            ))
        else:
            insights.append(BusinessInsight(
                category="variability",
                level="critical",
                title="数据波动极大，存在不稳定性",
                description=f'"{column_name}"的变异系数高达{cv_percent:.1f}%，'
                           f'说明数据极度不稳定，存在巨大的个体差异。'
                           f'平均值可能失去代表性，建议按类别分组分析或检查是否存在数据问题。'
            ))

    # 3. 数据量充足性
    if count < 30:
        insights.append(BusinessInsight(
            category="data_quality",
            level="warning",
            title="样本量较少，结论需谨慎",
            description=f'当前只有{count}条数据，样本量较小。'
                       f'统计结果的可靠性可能有限，建议收集更多数据后再做决策。'
        ))
    elif count < 100:
        insights.append(BusinessInsight(
            category="data_quality",
            level="info",
            title="样本量适中",
            description=f'当前有{count}条数据，可以进行初步分析。'
                       f'如需更高精度的结论，建议继续扩大样本量。'
        ))
    else:
        insights.append(BusinessInsight(
            category="data_quality",
            level="success",
            title="样本量充足",
            description=f'当前有{count}条数据，样本量充足。'
                       f'统计分析结果具有较高的可靠性和代表性。'
        ))

    return insights


def interpret_distribution(skewness: float, kurtosis: float,
                           is_normal: bool, column_name: str = "数据") -> List[BusinessInsight]:
    """解释数据分布的业务含义

    Args:
        skewness: 偏度
        kurtosis: 峰度
        is_normal: 是否符合正态分布
        column_name: 列名

    Returns:
        业务洞察列表
    """
    insights = []

    # 1. 对称性分析（偏度）
    if abs(skewness) < 0.5:
        insights.append(BusinessInsight(
            category="distribution",
            level="success",
            title="数据分布对称",
            description=f'"{column_name}"的分布非常对称，没有明显的偏倚。'
                       f'这是理想的数据状态，各种统计方法都能较好地适用。'
        ))
    elif abs(skewness) < 1.0:
        direction = "右偏" if skewness > 0 else "左偏"
        insights.append(BusinessInsight(
            category="distribution",
            level="info",
            title=f"数据呈现轻微{direction}",
            description=f'"{column_name}"的分布{direction}，数据整体{"向高值方向延伸" if skewness > 0 else "向低值方向延伸"}。'
                       f'这种偏倚程度较轻，对大多数分析影响不大。'
        ))
    else:
        direction = "右偏" if skewness > 0 else "左偏"
        level = "critical" if abs(skewness) > 2 else "warning"
        insights.append(BusinessInsight(
            category="distribution",
            level=level,
            title=f"数据呈现明显{direction}，分布不均",
            description=f'"{column_name}"的分布存在明显的{direction}（偏度值：{skewness:.2f}）。'
                       f'{"大部分数据集中在较低水平，少数高值拉高了整体水平" if skewness > 0 else "大部分数据集中在较高水平，少数低值拖累了整体水平"}。'
                       f'在这种情况下，平均值可能不是最佳的代表值，建议使用中位数。'
                       f'同时考虑是否存在异常值或多群体混合的情况。'
        ))

    # 2. 集中程度分析（峰度）
    if abs(kurtosis - 3) < 0.5:  # 接近正态分布的峰度3
        insights.append(BusinessInsight(
            category="distribution",
            level="info",
            title="数据集中程度正常",
            description=f'"{column_name}"的数据集中程度适中，'
                       f'既没有过度集中也没有过度分散。'
        ))
    elif kurtosis > 3.5:
        insights.append(BusinessInsight(
            category="distribution",
            level="warning",
            title="数据高度集中，两端有极端值",
            description=f'"{column_name}"的数据分布呈现尖峰状态（峰度：{kurtosis:.2f}），'
                       f'说明大部分数据非常接近平均值，但同时也存在一些极端值。'
                       f'需要特别关注这些极端值，它们可能是特殊情况或数据质量问题。'
        ))
    elif kurtosis < 2.5:
        insights.append(BusinessInsight(
            category="distribution",
            level="info",
            title="数据分布比较平坦",
            description=f'"{column_name}"的数据分布比较平坦（峰度：{kurtosis:.2f}），'
                       f'说明数据点在各个水平上都有分布，没有特别集中的区域。'
                       f'这可能意味着数据来源较为多样化。'
        ))

    # 3. 正态性判断
    if is_normal:
        insights.append(BusinessInsight(
            category="distribution",
            level="success",
            title="数据符合正态分布假设",
            description=f'"{column_name}"通过了正态性检验，'
                       f'这意味着可以使用基于正态分布的各种统计方法和预测模型。'
                       f'这为后续的数据分析和推断提供了良好的基础。'
        ))
    else:
        insights.append(BusinessInsight(
            category="distribution",
            level="warning",
            title="数据偏离正态分布",
            description=f'"{column_name}"不符合正态分布假设。'
                       f'这可能会影响某些统计方法的有效性（如t检验、ANOVA等）。'
                       f'建议使用非参数方法，或对数据进行适当的转换。'
        ))

    return insights


def interpret_outliers(outlier_count: int, outlier_percentage: float,
                      total_count: int, column_name: str = "数据") -> List[BusinessInsight]:
    """解释异常值的业务含义

    Args:
        outlier_count: 异常值数量
        outlier_percentage: 异常值百分比
        total_count: 总数据量
        column_name: 列名

    Returns:
        业务洞察列表
    """
    insights = []

    if outlier_count == 0:
        insights.append(BusinessInsight(
            category="outliers",
            level="success",
            title="未发现异常数据",
            description=f'"{column_name}"没有检测到异常值，数据质量良好，所有数据点都在合理范围内。'
        ))
    elif outlier_percentage < 1:
        insights.append(BusinessInsight(
            category="outliers",
            level="info",
            title=f"发现{outlier_count}个轻微异常数据点",
            description=f'"{column_name}"中存在{outlier_count}个轻微偏离常规范围的数据点'
                       f'（占比{outlier_percentage:.2f}%）。这些可能是正常范围内的极值，'
                       f'建议人工核实是否为特殊情况。'
        ))
    elif outlier_percentage < 5:
        insights.append(BusinessInsight(
            category="outliers",
            level="warning",
            title=f"发现{outlier_count}个异常数据点（占比{outlier_percentage:.1f}%）",
            description=f'"{column_name}"中存在{outlier_count}个明显偏离常规范围的数据点。'
                       f'建议：1）检查这些数据是否为录入错误；2）确认是否为真实发生的特殊情况；'
                       f'3）考虑在分析中是否需要单独处理这些数据。'
        ))
    else:
        insights.append(BusinessInsight(
            category="outliers",
            level="critical",
            title=f"发现大量异常数据（{outlier_count}个，占比{outlier_percentage:.1f}%）",
            description=f'"{column_name}"中存在大量异常数据，占比达到{outlier_percentage:.1f}%。'
                       f'这可能意味着：1）数据收集或记录过程存在系统性问题；'
                       f'2）实际业务中确实存在大量特殊情况，可能需要分类分析；'
                       f'3）该指标的"正常"范围定义可能需要重新评估。'
                       f'强烈建议进行深入的数据质量检查和业务原因分析。'
        ))

    return insights


def interpret_group_comparison(test_result: Dict[str, Any],
                               group_stats: Dict[str, Dict[str, float]],
                               value_col: str,
                               group_col: str) -> List[BusinessInsight]:
    """解释分组对比的业务含义

    Args:
        test_result: 统计检验结果
        group_stats: 各组统计量
        value_col: 数值列名
        group_col: 分组列名

    Returns:
        业务洞察列表
    """
    insights = []

    is_significant = test_result.get('is_significant', False)
    p_value = test_result.get('p_value', 1.0)
    test_name = test_result.get('test_name', '')
    effect_size = test_result.get('effect_size')

    if is_significant:
        # 差异显著
        if effect_size:
            if effect_size < 0.2:
                size_desc = "差异很小"
                suggestion = "虽然统计上差异显著，但实际业务意义可能不大。"
            elif effect_size < 0.5:
                size_desc = "差异较小"
                suggestion = "各组之间存在一定差异，可以进一步分析差异来源。"
            elif effect_size < 0.8:
                size_desc = "差异中等"
                suggestion = f"建议重点关注表现较好和较差的组别，分析其差异原因，并考虑推广最佳实践。"
            else:
                size_desc = "差异很大"
                suggestion = f"组间差异非常明显，这可能是关键的业务洞察点，建议深入分析造成差异的根本原因。"

            insights.append(BusinessInsight(
                category="group_comparison",
                level="warning" if effect_size > 0.5 else "info",
                title=f"各组之间存在显著{size_desc}",
                description=f'按"{group_col}"分组后，"{value_col}"在不同组之间存在显著差异'
                           f'（{test_name}，p={p_value:.4f}，效应量={effect_size:.2f}）。'
                           f'{suggestion}'
            ))
        else:
            insights.append(BusinessInsight(
                category="group_comparison",
                level="info",
                title="各组之间存在显著差异",
                description=f'按"{group_col}"分组后，"{value_col}"在不同组之间存在显著差异'
                           f'（{test_name}，p={p_value:.4f}）。'
                           f'建议进一步分析哪些组之间存在差异，以及差异的具体表现。'
            ))

        # 找出表现最好和最差的组
        if group_stats:
            means = {group: stats.get('mean', float('inf'))
                    for group, stats in group_stats.items()
                    if stats.get('mean') is not None}

            if means:
                best_group = max(means, key=means.get)
                worst_group = min(means, key=means.get)
                best_value = means[best_group]
                worst_value = means[worst_group]
                improvement = ((best_value - worst_value) / worst_value * 100) if worst_value != 0 else 0

                insights.append(BusinessInsight(
                    category="group_comparison",
                    level="info",
                    title=f"表现最好和最差的组",
                    description=f'在"{value_col}"方面，"{best_group}"组表现最好（平均值：{best_value:.2f}），'
                               f'而"{worst_group}"组表现相对较差（平均值：{worst_value:.2f}）。'
                               f'最好组比较差组高{improvement:.1f}%。'
                               f'建议分析"{best_group}"组的成功经验，看是否可以复制到其他组。'
                ))
    else:
        insights.append(BusinessInsight(
            category="group_comparison",
            level="info",
            title="各组之间无显著差异",
            description=f'按"{group_col}"分组后，"{value_col}"在不同组之间没有发现显著差异'
                       f'（{test_name}，p={p_value:.4f}）。'
                       f'这意味着该指标在不同组之间的表现基本一致，'
                       f'分组因素对该指标没有明显影响。'
        ))

    return insights


def generate_executive_summary(insights: List[BusinessInsight],
                               column_name: str = "数据") -> Dict[str, Any]:
    """生成高管摘要

    Args:
        insights: 所有洞察列表
        column_name: 列名

    Returns:
        摘要字典
    """
    # 分类统计
    by_level = {}
    by_category = {}

    for insight in insights:
        by_level[insight.level] = by_level.get(insight.level, 0) + 1
        by_category[insight.category] = by_category.get(insight.category, 0) + 1

    # 找出最重要的洞察
    critical_insights = [i for i in insights if i.level == 'critical']
    warning_insights = [i for i in insights if i.level == 'warning']

    top_insights = critical_insights[:3] + warning_insights[:2]

    # 生成总体评价
    if by_level.get('critical', 0) > 0:
        overall_status = "需要重点关注"
        overall_color = "danger"
    elif by_level.get('warning', 0) > 2:
        overall_status = "存在一些需要注意的问题"
        overall_color = "warning"
    elif by_level.get('warning', 0) > 0:
        overall_status = "整体良好，有少量改进空间"
        overall_color = "info"
    else:
        overall_status = "表现优秀"
        overall_color = "success"

    return {
        'overall_status': overall_status,
        'overall_color': overall_color,
        'total_insights': len(insights),
        'by_level': by_level,
        'by_category': by_category,
        'top_insights': top_insights,
    }


def translate_statistical_term(term: str) -> str:
    """将统计术语翻译为业务语言

    Args:
        term: 统计术语

    Returns:
        业务语言描述
    """
    translations = {
        'mean': '平均水平',
        'median': '中等水平（中位数）',
        'mode': '最常见值',
        'std': '波动程度（标准差）',
        'variance': '方差',
        'min': '最小值',
        'max': '最大值',
        'q1': '下四分位数（25%位置）',
        'q3': '上四分位数（75%位置）',
        'iqr': '四分位距（中间50%数据的范围）',
        'range': '极差（最大值与最小值的差距）',
        'skewness': '偏度（分布的对称性）',
        'kurtosis': '峰度（分布的尖锐程度）',
        'cv': '变异系数（相对波动程度）',
        'outlier': '异常值',
        'normality_test': '正态性检验',
        'correlation': '相关性',
        'p_value': '显著性水平',
        'effect_size': '效应量（差异的实际大小）',
        'confidence_interval': '置信区间',
    }

    return translations.get(term.lower(), term)
