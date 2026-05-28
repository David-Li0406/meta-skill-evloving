#!/usr/bin/env python3
"""
Dashboard Generator Module

Generates visual dashboards and charts for trademark data analysis.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import Counter


class DashboardGenerator:
    """
    Generates interactive HTML dashboards with charts and statistics
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Initialize dashboard generator

        Args:
            data: List of trademark data dictionaries
        """
        self.data = data
        self.stats = self._calculate_statistics()

    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive statistics"""
        total = len(self.data)

        if total == 0:
            return {
                'total': 0,
                'by_registrant': {},
                'by_classification': {},
                'by_confidence': {},
                'by_expiry_status': {},
                'needs_review': 0,
                'expiring_soon': 0,
            }

        # Count by registrant
        registrants = [d.get('注册人', 'Unknown') for d in self.data]
        by_registrant = dict(Counter(registrants).most_common(10))

        # Count by classification
        classifications = [d.get('国际分类', 'Unknown') for d in self.data]
        by_classification = dict(Counter(classifications))

        # Count by confidence level
        confidence_levels = [d.get('confidence_level', 'unknown') for d in self.data]
        by_confidence = dict(Counter(confidence_levels))

        # Count by expiry status
        expiry_statuses = [d.get('expiry_status', 'unknown') for d in self.data]
        by_expiry_status = dict(Counter(expiry_statuses))

        # Count special cases
        needs_review = sum(1 for d in self.data if d.get('requires_manual_review'))
        expiring_soon = sum(1 for d in self.data if d.get('requires_renewal'))

        return {
            'total': total,
            'by_registrant': by_registrant,
            'by_classification': by_classification,
            'by_confidence': by_confidence,
            'by_expiry_status': by_expiry_status,
            'needs_review': needs_review,
            'expiring_soon': expiring_soon,
        }

    def generate_html_dashboard(self, output_path: Path) -> Path:
        """
        Generate interactive HTML dashboard with charts

        Args:
            output_path: Path for output HTML file

        Returns:
            Path to generated dashboard
        """
        html_content = self._generate_dashboard_html()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path

    def _generate_dashboard_html(self) -> str:
        """Generate complete HTML dashboard"""
        stats = self.stats

        # Prepare data for charts
        registrant_labels = list(stats['by_registrant'].keys())
        registrant_values = list(stats['by_registrant'].values())

        classification_labels = list(stats['by_classification'].keys())
        classification_values = list(stats['by_classification'].values())

        confidence_data = stats['by_confidence']
        expiry_data = stats['by_expiry_status']

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>商标数据分析仪表盘</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}
        .stat-card.green::before {{
            background: linear-gradient(90deg, #56ab2f, #a8e063);
        }}
        .stat-card.orange::before {{
            background: linear-gradient(90deg, #f093fb, #f5576c);
        }}
        .stat-card.red::before {{
            background: linear-gradient(90deg, #fa709a, #fee140);
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-value {{
            color: #333;
            font-size: 36px;
            font-weight: bold;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .chart-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .chart-card h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 18px;
        }}
        .chart-container {{
            position: relative;
            height: 300px;
        }}
        .footer {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📊 商标数据分析仪表盘</h1>
            <p>生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总商标数</div>
                <div class="stat-value">{stats['total']}</div>
            </div>
            <div class="stat-card green">
                <div class="stat-label">高置信度</div>
                <div class="stat-value">{stats['by_confidence'].get('high', 0)}</div>
            </div>
            <div class="stat-card orange">
                <div class="stat-label">需要复核</div>
                <div class="stat-value">{stats['needs_review']}</div>
            </div>
            <div class="stat-card red">
                <div class="stat-label">即将到期</div>
                <div class="stat-value">{stats['expiring_soon']}</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h2>📈 按注册人分布（Top 10）</h2>
                <div class="chart-container">
                    <canvas id="registrantChart"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h2>🏷️ 按国际分类分布</h2>
                <div class="chart-container">
                    <canvas id="classificationChart"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h2>🎯 置信度分布</h2>
                <div class="chart-container">
                    <canvas id="confidenceChart"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h2>⏰ 到期状态分布</h2>
                <div class="chart-container">
                    <canvas id="expiryChart"></canvas>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>商标证书提取器 v2.0 - 数据分析仪表盘</p>
        </div>
    </div>

    <script>
        // Chart.js defaults
        Chart.defaults.font.family = 'Microsoft YaHei, Segoe UI, Arial, sans-serif';
        Chart.defaults.plugins.legend.display = true;
        Chart.defaults.plugins.legend.position = 'bottom';

        // Registrant Chart
        new Chart(document.getElementById('registrantChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(registrant_labels, ensure_ascii=False)},
                datasets: [{{
                    label: '商标数量',
                    data: {json.dumps(registrant_values)},
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});

        // Classification Chart
        new Chart(document.getElementById('classificationChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(classification_labels, ensure_ascii=False)},
                datasets: [{{
                    data: {json.dumps(classification_values)},
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(199, 199, 199, 0.8)',
                        'rgba(83, 102, 255, 0.8)',
                        'rgba(255, 99, 255, 0.8)',
                        'rgba(99, 255, 132, 0.8)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});

        // Confidence Chart
        new Chart(document.getElementById('confidenceChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['高置信度', '中等置信度', '低置信度', '需复核'],
                datasets: [{{
                    data: [
                        {confidence_data.get('high', 0)},
                        {confidence_data.get('medium', 0)},
                        {confidence_data.get('low', 0)},
                        {confidence_data.get('requires_review', 0)}
                    ],
                    backgroundColor: [
                        'rgba(86, 171, 47, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 99, 132, 0.8)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});

        // Expiry Chart
        new Chart(document.getElementById('expiryChart'), {{
            type: 'bar',
            data: {{
                labels: ['已过期', '90天内', '180天内', '365天内', '有效'],
                datasets: [{{
                    label: '商标数量',
                    data: [
                        {expiry_data.get('expired', 0)},
                        {expiry_data.get('critical', 0)},
                        {expiry_data.get('warning', 0)},
                        {expiry_data.get('attention', 0)},
                        {expiry_data.get('valid', 0)}
                    ],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(86, 171, 47, 0.8)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html

    def generate_summary_report(self) -> str:
        """Generate text summary report"""
        stats = self.stats

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("商标数据统计摘要")
        report_lines.append("=" * 80)
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("")

        # Overall stats
        report_lines.append("📊 总体统计")
        report_lines.append("-" * 80)
        report_lines.append(f"总商标数: {stats['total']}")
        report_lines.append(f"需要复核: {stats['needs_review']} ({stats['needs_review']/stats['total']*100:.1f}%)" if stats['total'] > 0 else "需要复核: 0")
        report_lines.append(f"即将到期: {stats['expiring_soon']} ({stats['expiring_soon']/stats['total']*100:.1f}%)" if stats['total'] > 0 else "即将到期: 0")
        report_lines.append("")

        # Top registrants
        report_lines.append("🏢 主要注册人（Top 10）")
        report_lines.append("-" * 80)
        for registrant, count in list(stats['by_registrant'].items())[:10]:
            report_lines.append(f"  {registrant}: {count}")
        report_lines.append("")

        # Classification distribution
        report_lines.append("🏷️ 国际分类分布")
        report_lines.append("-" * 80)
        for classification, count in sorted(stats['by_classification'].items()):
            report_lines.append(f"  第{classification}类: {count}")
        report_lines.append("")

        # Confidence distribution
        report_lines.append("🎯 置信度分布")
        report_lines.append("-" * 80)
        for level, count in stats['by_confidence'].items():
            report_lines.append(f"  {level}: {count}")
        report_lines.append("")

        # Expiry status
        report_lines.append("⏰ 到期状态")
        report_lines.append("-" * 80)
        status_labels = {
            'expired': '已过期',
            'critical': '90天内到期',
            'warning': '180天内到期',
            'attention': '365天内到期',
            'valid': '有效',
        }
        for status, label in status_labels.items():
            count = stats['by_expiry_status'].get(status, 0)
            report_lines.append(f"  {label}: {count}")

        report_lines.append("")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)


if __name__ == "__main__":
    # Test dashboard generator
    from datetime import timedelta

    test_data = [
        {
            '注册人': '阿里巴巴集团控股有限公司',
            '注册号': f'1234567{i}',
            '国际分类': str((i % 10) + 1),
            '有效期限': (datetime.now() + timedelta(days=100*i)).strftime('%Y-%m-%d'),
            'overall_confidence': 0.9 if i % 3 == 0 else 0.6,
            'confidence_level': 'high' if i % 3 == 0 else 'medium',
            'requires_manual_review': i % 5 == 0,
            'requires_renewal': i % 4 == 0,
            'expiry_status': 'valid' if i % 2 == 0 else 'warning',
        }
        for i in range(20)
    ]

    # Add some variation
    test_data.extend([
        {
            '注册人': '腾讯科技（深圳）有限公司',
            '注册号': f'8765432{i}',
            '国际分类': '9',
            '有效期限': '2024-12-31',
            'overall_confidence': 0.75,
            'confidence_level': 'medium',
            'requires_manual_review': True,
            'requires_renewal': True,
            'expiry_status': 'critical',
        }
        for i in range(5)
    ])

    generator = DashboardGenerator(test_data)

    # Generate dashboard
    output_path = Path('/tmp/trademark_dashboard.html')
    generator.generate_html_dashboard(output_path)
    print(f"Dashboard generated: {output_path}")

    # Generate summary
    print("\n" + generator.generate_summary_report())
