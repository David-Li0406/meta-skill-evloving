"""
Git Code Review Module

Provides functionality to fetch git commit history for specified users,
analyze code changes, and generate detailed code review reports.
"""

import os
import sys
import subprocess
import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class GitCodeReview:
    """Main class for git code review functionality."""

    def __init__(self, repo_path: str = "."):
        """
        Initialize with repository path.

        Args:
            repo_path: Path to git repository (defaults to current directory)
        """
        self.repo_path = Path(repo_path).absolute()
        self.reports_dir = self.repo_path / ".claude" / "git_code_review"
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

    def validate_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def get_git_commits(self, users: List[str], days: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch git commits for specified users and time period.

        Args:
            users: List of git usernames to filter commits
            days: Number of days to look back (None for current day)

        Returns:
            List of commit dictionaries with metadata and diff
        """
        if not self.validate_git_repo():
            raise ValueError(f"Not a git repository: {self.repo_path}")

        # Build git log command
        cmd = ["git", "log", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=short"]

        # Add author filter if users specified
        if users:
            author_filter = " --author=" + " --author=".join(users)
            cmd.extend(author_filter.split())

        # Add date filter
        if days is not None:
            cmd.append(f"--since={days}.days.ago")
        else:
            cmd.append(f"--since={self.today}")

        cmd.append("--name-status")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e.stderr}")

        commits = []
        current_commit = None
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if '|' in line and '\t' not in line:
                # This is a commit header line
                if current_commit:
                    commits.append(current_commit)

                parts = line.split('|')
                if len(parts) >= 5:
                    current_commit = {
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4],
                        'files': []
                    }
            elif current_commit and '\t' in line:
                # This is a file change line
                parts = line.split('\t')
                if len(parts) >= 2:
                    change_type = parts[0]
                    file_path = parts[1]
                    current_commit['files'].append({
                        'change_type': change_type,
                        'file_path': file_path
                    })

        if current_commit:
            commits.append(current_commit)

        return commits

    def get_file_diff(self, commit_hash: str, file_path: str) -> str:
        """
        Get diff for a specific file in a commit.

        Args:
            commit_hash: Git commit hash
            file_path: Path to file within repository

        Returns:
            Diff output as string
        """
        try:
            result = subprocess.run(
                ["git", "show", f"{commit_hash}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                return result.stdout
            else:
                return f"Unable to retrieve file content: {result.stderr}"
        except subprocess.SubprocessError as e:
            return f"Error retrieving diff: {str(e)}"

    def analyze_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single commit for code review.

        Args:
            commit: Commit dictionary with metadata

        Returns:
            Analysis dictionary with review findings
        """
        analysis = {
            'commit_hash': commit['hash'],
            'author': commit['author'],
            'date': commit['date'],
            'message': commit['message'],
            'file_count': len(commit['files']),
            'files_by_type': {},
            'issues': [],
            'suggestions': [],
            'complexity_score': 0
        }

        # Count files by change type
        for file_info in commit['files']:
            change_type = file_info['change_type']
            analysis['files_by_type'][change_type] = analysis['files_by_type'].get(change_type, 0) + 1

        # Basic analysis based on commit characteristics
        if len(commit['files']) > 10:
            analysis['issues'].append("Large commit: Consider breaking into smaller, focused commits")
            analysis['complexity_score'] += 2

        if any(f['change_type'] == 'D' for f in commit['files']):
            analysis['suggestions'].append("Review deletions carefully for unintended removals")

        if any(f['change_type'] == 'R' for f in commit['files']):
            analysis['suggestions'].append("Verify rename operations preserve file history")

        # Check commit message quality
        message = commit['message'].strip()
        if len(message) < 10:
            analysis['issues'].append("Commit message is too brief")
        elif len(message.split()) < 3:
            analysis['issues'].append("Commit message lacks descriptive detail")

        return analysis

    def generate_report(self, user: str, commits: List[Dict[str, Any]]) -> str:
        """
        Generate markdown report for a user's commits.

        Args:
            user: Git username
            commits: List of commit dictionaries

        Returns:
            Markdown report as string
        """
        report = f"""# Code Review Report for {user}
Generated: {self.today}

## Summary
- **User**: {user}
- **Period**: {commits[0]['date'] if commits else self.today} to {self.today}
- **Total Commits**: {len(commits)}
- **Total Files Changed**: {sum(len(c['files']) for c in commits)}

## Commit Overview
"""

        for commit in commits:
            analysis = self.analyze_commit(commit)
            report += f"""
### Commit: {commit['hash'][:8]} - {commit['date']}
**Message**: {commit['message']}

**Files Changed**: {len(commit['files'])}
- Added: {analysis['files_by_type'].get('A', 0)}
- Modified: {analysis['files_by_type'].get('M', 0)}
- Deleted: {analysis['files_by_type'].get('D', 0)}
- Renamed: {analysis['files_by_type'].get('R', 0)}

**Files**:
"""
            for file_info in commit['files']:
                report += f"- {file_info['change_type']}: {file_info['file_path']}\n"

            if analysis['issues']:
                report += "\n**Issues Identified**:\n"
                for issue in analysis['issues']:
                    report += f"- ⚠️ {issue}\n"

            if analysis['suggestions']:
                report += "\n**Suggestions**:\n"
                for suggestion in analysis['suggestions']:
                    report += f"- 💡 {suggestion}\n"

            report += "\n---\n"

        # Add overall recommendations
        report += """
## Overall Recommendations

1. **Commit Size**: Keep commits focused on single logical changes
2. **Message Quality**: Write descriptive commit messages explaining the "why"
3. **Code Review**: Consider peer review for complex changes
4. **Testing**: Ensure changes are adequately tested
5. **Documentation**: Update relevant documentation with code changes

## Best Practices Checklist

- [ ] Single responsibility per commit
- [ ] Descriptive commit messages
- [ ] Code follows project conventions
- [ ] No commented-out code
- [ ] Proper error handling
- [ ] Adequate test coverage
- [ ] Documentation updates if needed
- [ ] Security considerations addressed
- [ ] Performance implications considered
"""

        return report

    def save_report(self, user: str, report_content: str) -> str:
        """
        Save report to file.

        Args:
            user: Git username
            report_content: Markdown report content

        Returns:
            Path to saved report file
        """
        # Create reports directory if it doesn't exist
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize username for filename
        safe_user = "".join(c for c in user if c.isalnum() or c in ('-', '_')).strip()
        filename = f"{safe_user}-{self.today}.md"
        filepath = self.reports_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return str(filepath)

    def process_users(self, users_str: str, days: Optional[int] = None) -> Dict[str, Any]:
        """
        Main processing method for multiple users.

        Args:
            users_str: Comma-separated list of usernames
            days: Number of days to look back

        Returns:
            Dictionary with processing results
        """
        users = [u.strip() for u in users_str.split(',') if u.strip()]
        results = {
            'users_processed': [],
            'reports_generated': [],
            'total_commits': 0,
            'errors': []
        }

        for user in users:
            try:
                commits = self.get_git_commits([user], days)
                if commits:
                    report = self.generate_report(user, commits)
                    report_path = self.save_report(user, report)

                    results['users_processed'].append(user)
                    results['reports_generated'].append({
                        'user': user,
                        'report_path': report_path,
                        'commit_count': len(commits)
                    })
                    results['total_commits'] += len(commits)
                else:
                    results['errors'].append(f"No commits found for user: {user}")
            except Exception as e:
                results['errors'].append(f"Error processing user {user}: {str(e)}")

        return results


def main():
    """Command-line interface for git code review."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate git code review reports')
    parser.add_argument('--users', required=True, help='Comma-separated list of git usernames')
    parser.add_argument('--days', type=int, help='Number of days to look back (default: current day)')
    parser.add_argument('--repo', default='.', help='Path to git repository (default: current directory)')

    args = parser.parse_args()

    try:
        reviewer = GitCodeReview(args.repo)
        results = reviewer.process_users(args.users, args.days)

        print(json.dumps(results, indent=2))

        if results['errors']:
            print("\nErrors encountered:")
            for error in results['errors']:
                print(f"  - {error}")

        return 0 if not results['errors'] else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())