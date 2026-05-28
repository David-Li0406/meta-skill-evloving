"""
Report Generator Module.

This module provides functionality to generate markdown reports
from git commit analysis results.
"""

import os
from datetime import datetime
from typing import Dict, Any, List


class ReportGenerator:
    """Generates markdown reports from git commit analysis."""

    def __init__(self, reports_dir: str = ".claude/git_commit_report"):
        """
        Initialize report generator.

        Args:
            reports_dir: Directory to save reports (relative to repository root)
        """
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_user_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate markdown report for a single user.

        Args:
            analysis_result: Analysis result from GitCommitAnalyzer

        Returns:
            Markdown report content
        """
        username = analysis_result['username']
        period = analysis_result['period']
        total_commits = analysis_result['total_commits']
        commits = analysis_result['commits']
        stats = analysis_result.get('statistics', {})

        # Generate report header
        report = f"""# Git Commit Summary: {username}

**Analysis Period**: {period}
**Total Commits**: {total_commits}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

{analysis_result['summary']}

"""

        # Add statistics section only if we have stats
        if stats:
            report += """## Statistics

"""
            report += f"- **Total Commits**: {total_commits}\n"
            report += f"- **Total Files Changed**: {stats.get('total_files_changed', 0)}\n"
            report += f"- **Average Files per Commit**: {stats.get('avg_files_per_commit', 0)}\n"
            report += f"- **Days with Commits**: {stats.get('days_with_commits', 0)}\n\n"

        report += "## Commits by Date\n\n"

        # Add commits by date table
        commits_by_date = stats.get('commits_by_date', {})
        if commits_by_date:
            report += "| Date | Commits |\n"
            report += "|------|---------|\n"
            for date, count in sorted(commits_by_date.items(), reverse=True):
                report += f"| {date} | {count} |\n"
        else:
            report += "*No commits in this period*\n"

        report += "\n---\n\n## Detailed Commits\n\n"

        # Add detailed commit information
        if commits:
            for commit in commits:
                report += f"### Commit: `{commit['hash'][:8]}`\n\n"
                report += f"**Date**: {commit['date']}  \n"
                report += f"**Message**: {commit['message']}  \n\n"

                if commit.get('changed_files'):
                    report += "**Changed Files**:\n\n"
                    for file in commit['changed_files']:
                        report += f"- `{file}`\n"

                if commit.get('stats'):
                    stat_info = commit['stats']
                    if stat_info:
                        report += "\n**Statistics**:\n"
                        if 'files_changed' in stat_info:
                            report += f"- Files Changed: {stat_info['files_changed']}\n"
                        if 'insertions' in stat_info:
                            report += f"- Insertions: {stat_info['insertions']}\n"
                        if 'deletions' in stat_info:
                            report += f"- Deletions: {stat_info['deletions']}\n"

                report += "\n---\n\n"
        else:
            report += "*No commits found*\n"

        return report

    def generate_multi_user_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate summary report for multiple users.

        Args:
            analysis_result: Multi-user analysis result from GitCommitAnalyzer

        Returns:
            Markdown report content
        """
        period = analysis_result['period']
        overall = analysis_result['overall']
        users = analysis_result['users']

        # Generate report header
        report = f"""# Multi-User Git Commit Summary

**Analysis Period**: {period}
**Total Users**: {overall['total_users']}
**Active Users**: {overall['active_users']}
**Total Commits**: {overall['total_commits']}
**Total Files Changed**: {overall['total_files_changed']}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## User Summary

| User | Commits | Files Changed | Status |
|------|---------|---------------|--------|
"""

        # Add user summary table
        for username, user_data in users.items():
            total_commits = user_data['total_commits']
            files_changed = user_data.get('statistics', {}).get('total_files_changed', 0)
            status = "Active" if total_commits > 0 else "Inactive"
            report += f"| {username} | {total_commits} | {files_changed} | {status} |\n"

        report += "\n---\n\n## Detailed User Reports\n\n"

        # Add links to individual user reports
        for username in users.keys():
            report += f"- [{username}]({username}-{datetime.now().strftime('%Y%m%d')}.md)\n"

        return report

    def save_report(self, content: str, filename: str) -> str:
        """
        Save report to file.

        Args:
            content: Report content
            filename: Output filename

        Returns:
            Path to saved report
        """
        filepath = os.path.join(self.reports_dir, filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_and_save_user_reports(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate and save reports for all users.

        Args:
            analysis_results: Multi-user analysis result from GitCommitAnalyzer

        Returns:
            Dictionary mapping usernames to report filepaths
        """
        saved_reports = {}
        users = analysis_results['users']
        period = analysis_results['period']

        for username, user_data in users.items():
            # Generate report content
            report_content = self.generate_user_report(user_data)

            # Generate filename
            days = None
            if "days" in period.lower():
                try:
                    days = int(period.split()[1])  # Extract number from "Last X days"
                except (IndexError, ValueError):
                    pass

            # Create filename
            date_str = datetime.now().strftime("%Y%m%d")
            if days:
                filename = f"{username}-{date_str}-{days}days.md"
            else:
                filename = f"{username}-{date_str}.md"

            # Save report
            filepath = self.save_report(report_content, filename)
            saved_reports[username] = filepath

        # Generate and save multi-user summary report
        if len(users) > 1:
            summary_content = self.generate_multi_user_report(analysis_results)
            summary_filename = f"summary-{datetime.now().strftime('%Y%m%d')}.md"
            summary_path = self.save_report(summary_content, summary_filename)
            saved_reports['summary'] = summary_path

        return saved_reports