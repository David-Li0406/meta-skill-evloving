"""报告生成模块

生成扫描结果的格式化报告。
"""

from typing import List, Dict, Any
from rich.table import Table
from rich.console import Console
from rich import box


class ReportGenerator:
    """报告生成器"""

    SEVERITY_COLORS = {
        '严重': 'red',
        '高': 'orange3',
        '中': 'yellow',
        '低': 'blue',
        '安全': 'green',
    }

    SEVERITY_ICONS = {
        '严重': '🔴',
        '高': '🟠',
        '中': '🟡',
        '低': '🔵',
        '安全': '🟢',
    }

    def __init__(self, use_color: bool = True):
        self.use_color = use_color
        self.console = Console() if use_color else Console(force_terminal=False, no_color=True)

    def print_results(self, results: List[Dict[str, Any]]) -> None:
        """打印扫描结果"""
        # 打印概要
        self._print_summary(results)

        if not results:
            return

        # 打印详细表格
        self._print_details_table(results)

    def _print_summary(self, results: List[Dict[str, Any]]) -> None:
        """打印扫描概要"""
        total_skills = len(results)
        total_findings = sum(len(r.get('findings', [])) for r in results)

        severity_counts = {'严重': 0, '高': 0, '中': 0, '低': 0}
        for result in results:
            for finding in result.get('findings', []):
                severity = finding.get('severity', '低')
                if severity in severity_counts:
                    severity_counts[severity] += 1

        # 打印标题
        self.console.print()
        self.console.print('[bold cyan]╔═══════════════════════════════════════════════════════╗[/bold cyan]')
        self.console.print('[bold cyan]║[/bold cyan]          [bold yellow]Skill 安全扫描报告[/bold yellow]                      [bold cyan]║[/bold cyan]')
        self.console.print('[bold cyan]╚═══════════════════════════════════════════════════════╝[/bold cyan]')
        self.console.print()

        # 统计信息
        self.console.print(f'  [bold]扫描 Skills:[/bold] {total_skills}')
        self.console.print(f'  [bold]发现风险:[/bold] {total_findings}')
        self.console.print()

        # 风险分布
        if total_findings > 0:
            self.console.print('  [bold]风险分布:[/bold]')
            for severity in ['严重', '高', '中', '低']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    color = self.SEVERITY_COLORS.get(severity, 'white')
                    icon = self.SEVERITY_ICONS.get(severity, '')
                    self.console.print(f'    [{color}]{icon} {severity}: {count}[/{color}]')
        else:
            self.console.print('  [green]✓ 未发现明显风险[/green]')

        self.console.print()

    def _print_details_table(self, results: List[Dict[str, Any]]) -> None:
        """打印详细信息表格"""
        table = Table(
            title='详细检测结果',
            box=box.ROUNDED,
            show_header=True,
            header_style='bold magenta',
            title_style='bold cyan',
        )

        table.add_column('Skill', style='cyan', width=20)
        table.add_column('任务和能力', style='white', width=30)
        table.add_column('风险等级', width=12)
        table.add_column('详细说明', style='white', width=60)

        has_findings = False

        for result in results:
            skill_name = result.get('skill', 'unknown')
            description = result.get('description', '')
            findings = result.get('findings', [])

            if not findings:
                # 没有发现风险
                table.add_row(
                    skill_name,
                    description,
                    '[green]安全[/green]',
                    '[dim]未发现明显风险[/dim]',
                )
            else:
                has_findings = True
                for finding in findings:
                    severity = finding.get('severity', '低')
                    color = self.SEVERITY_COLORS.get(severity, 'white')
                    icon = self.SEVERITY_ICONS.get(severity, '')

                    # 构造详细信息
                    name = finding.get('name', '')
                    detector = finding.get('detector', '')
                    line = finding.get('line', 0)
                    details = finding.get('details', '')

                    detail_text = f'[{detector}] {name}'
                    if line > 0:
                        detail_text += f' (第{line}行)'
                    detail_text += f'\n{details}'

                    table.add_row(
                        skill_name,
                        description,
                        f'[{color}]{icon} {severity}[/{color}]',
                        detail_text,
                    )

        self.console.print(table)

        if has_findings:
            self.console.print()
            self.console.print('[bold yellow]⚠ 注意:[/bold yellow] 发现潜在风险，请仔细审查相关代码')
