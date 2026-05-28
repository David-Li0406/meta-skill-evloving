"""
Git Commit Analyzer Module.

This module provides functionality to analyze git commit history
for specified users and generate summary reports.
"""

import subprocess
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re


class GitCommitAnalyzer:
    """Analyzes git commits for specified users and time periods."""

    def __init__(self, repository_path: str = "."):
        """
        Initialize the analyzer with repository path.

        Args:
            repository_path: Path to git repository (defaults to current directory)
        """
        self.repository_path = repository_path
        self.reports_dir = os.path.join(repository_path, ".claude", "git_commit_report")

        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)

    def get_git_log(self, usernames: List[str], days: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get git log for specified users and time period.

        Args:
            usernames: List of git usernames to analyze
            days: Number of days to look back (None = today only)

        Returns:
            List of commit dictionaries with commit details

        Raises:
            subprocess.CalledProcessError: If git command fails
            FileNotFoundError: If not in a git repository
        """
        # Build git log command
        cmd = ["git", "log", "--all", "--pretty=format:%H|%an|%ad|%s", "--date=short"]

        # Add author filter if usernames provided
        if usernames:
            author_filter = "--author=" + "|".join(usernames)
            cmd.append(author_filter)

        # Add date filter if days specified
        if days is not None:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            cmd.append(f"--since={since_date}")

        try:
            # Execute git command with encoding handling
            result = subprocess.run(
                cmd,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                check=True
            )

            # Parse git log output
            commits = []
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue

                    parts = line.split('|', 3)
                    if len(parts) >= 4:
                        commit_hash, author, date, message = parts
                        commits.append({
                            'hash': commit_hash,
                            'author': author,
                            'date': date,
                            'message': message.strip()
                        })

            return commits

        except subprocess.CalledProcessError as e:
            if "not a git repository" in e.stderr.lower():
                raise FileNotFoundError("Not a git repository. Please run this command from within a git repository.")
            raise

    def get_commit_details(self, commit_hash: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific commit.

        Args:
            commit_hash: Git commit hash

        Returns:
            Dictionary with commit details including changed files
        """
        try:
            # Get changed files
            diff_cmd = ["git", "show", "--name-only", "--pretty=format:", commit_hash]
            diff_result = subprocess.run(
                diff_cmd,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                check=True
            )

            changed_files = []
            if diff_result.stdout:
                changed_files = [f.strip() for f in diff_result.stdout.strip().split('\n') if f.strip()]

            # Get commit stats
            stat_cmd = ["git", "show", "--stat", "--pretty=format:", commit_hash]
            stat_result = subprocess.run(
                stat_cmd,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # Parse stats
            stats = {}
            if stat_result.stdout:
                for line in stat_result.stdout.strip().split('\n'):
                    if 'files changed' in line:
                        match = re.search(r'(\d+) files? changed', line)
                        if match:
                            stats['files_changed'] = int(match.group(1))

                    if 'insertions' in line:
                        match = re.search(r'(\d+) insertions', line)
                        if match:
                            stats['insertions'] = int(match.group(1))

                    if 'deletions' in line:
                        match = re.search(r'(\d+) deletions', line)
                        if match:
                            stats['deletions'] = int(match.group(1))

            return {
                'hash': commit_hash,
                'changed_files': changed_files,
                'stats': stats
            }

        except subprocess.CalledProcessError:
            return {
                'hash': commit_hash,
                'changed_files': [],
                'stats': {}
            }

    def analyze_user_commits(self, username: str, days: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyze commits for a specific user.

        Args:
            username: Git username to analyze
            days: Number of days to look back (None = today only)

        Returns:
            Dictionary with analysis results
        """
        # Get commits for user
        commits = self.get_git_log([username], days)

        if not commits:
            return {
                'username': username,
                'period': f"Last {days} days" if days else "Today",
                'total_commits': 0,
                'commits': [],
                'summary': f"No commits found for user '{username}' in the specified period."
            }

        # Get detailed information for each commit
        detailed_commits = []
        for commit in commits:
            details = self.get_commit_details(commit['hash'])
            detailed_commits.append({
                **commit,
                **details
            })

        # Calculate statistics
        commits_by_date = {}
        total_files_changed = 0

        for commit in detailed_commits:
            date = commit['date']
            if date not in commits_by_date:
                commits_by_date[date] = 0
            commits_by_date[date] += 1

            total_files_changed += len(commit.get('changed_files', []))

        # Generate summary
        period_desc = f"Last {days} days" if days else "Today"
        avg_files_per_commit = total_files_changed / len(detailed_commits) if detailed_commits else 0

        return {
            'username': username,
            'period': period_desc,
            'total_commits': len(detailed_commits),
            'commits': detailed_commits,
            'statistics': {
                'commits_by_date': commits_by_date,
                'total_files_changed': total_files_changed,
                'avg_files_per_commit': round(avg_files_per_commit, 2),
                'days_with_commits': len(commits_by_date)
            },
            'summary': f"User '{username}' made {len(detailed_commits)} commits {period_desc.lower()}, "
                      f"changing {total_files_changed} files across {len(commits_by_date)} days."
        }

    def analyze_multiple_users(self, usernames: List[str], days: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyze commits for multiple users.

        Args:
            usernames: List of git usernames to analyze
            days: Number of days to look back (None = today only)

        Returns:
            Dictionary with analysis results for all users
        """
        results = {}
        all_commits = []

        for username in usernames:
            user_result = self.analyze_user_commits(username, days)
            results[username] = user_result
            all_commits.extend(user_result['commits'])

        # Calculate overall statistics
        total_commits = sum(r['total_commits'] for r in results.values())
        total_files_changed = sum(r.get('statistics', {}).get('total_files_changed', 0) for r in results.values())

        return {
            'users': results,
            'overall': {
                'total_users': len(usernames),
                'total_commits': total_commits,
                'total_files_changed': total_files_changed,
                'active_users': sum(1 for r in results.values() if r['total_commits'] > 0)
            },
            'period': f"Last {days} days" if days else "Today"
        }

    def generate_report_filename(self, username: str, days: Optional[int] = None) -> str:
        """
        Generate report filename for a user.

        Args:
            username: Git username
            days: Number of days analyzed (None = today)

        Returns:
            Report filename
        """
        date_str = datetime.now().strftime("%Y%m%d")
        if days:
            filename = f"{username}-{date_str}-{days}days.md"
        else:
            filename = f"{username}-{date_str}.md"

        # Replace any characters that might cause issues in filenames
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename