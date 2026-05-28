"""
Git Analyzer Module
Analyzes git repository state, detects file counts, and categorizes changes.
"""

import subprocess
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path


class GitAnalyzer:
    """Analyzes git repository state and file changes."""

    def __init__(self, threshold: int = 10):
        """
        Initialize Git Analyzer.

        Args:
            threshold: Maximum number of files before batching is recommended
        """
        self.threshold = threshold
        self.file_changes = []
        self.file_types = {}

    def get_git_status(self) -> Dict[str, List[str]]:
        """
        Get current git status including staged, modified, and untracked files.

        Returns:
            Dictionary with categorized file lists
        """
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )

            staged = []
            modified = []
            untracked = []

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                status = line[:2]
                filepath = line[3:].strip()

                # Staged files (first character is not space)
                if status[0] in ['A', 'M', 'D', 'R', 'C']:
                    staged.append(filepath)
                # Modified but not staged (second character indicates modification)
                elif status[1] in ['M', 'D']:
                    modified.append(filepath)
                # Untracked files
                elif status[0] == '?':
                    untracked.append(filepath)

            return {
                'staged': staged,
                'modified': modified,
                'untracked': untracked,
                'total': len(staged) + len(modified) + len(untracked)
            }
        except subprocess.CalledProcessError as e:
            return {
                'staged': [],
                'modified': [],
                'untracked': [],
                'total': 0,
                'error': str(e)
            }

    def analyze_file_changes(self, filepath: str) -> Dict[str, Any]:
        """
        Analyze what changes were made to a specific file.

        Args:
            filepath: Path to the file to analyze

        Returns:
            Dictionary with change analysis
        """
        try:
            # Get diff for the file
            result = subprocess.run(
                ['git', 'diff', '--cached', filepath],
                capture_output=True,
                text=True
            )

            # If no cached diff, try regular diff
            if not result.stdout:
                result = subprocess.run(
                    ['git', 'diff', filepath],
                    capture_output=True,
                    text=True
                )

            diff_output = result.stdout

            # Analyze diff to determine change type
            change_type = self._categorize_change(diff_output, filepath)

            # Extract file extension
            extension = Path(filepath).suffix

            # Determine scope based on file path
            scope = self._extract_scope_from_path(filepath)

            return {
                'filepath': filepath,
                'change_type': change_type,
                'extension': extension,
                'scope': scope,
                'lines_added': diff_output.count('\n+'),
                'lines_removed': diff_output.count('\n-')
            }
        except Exception as e:
            return {
                'filepath': filepath,
                'change_type': 'unknown',
                'extension': Path(filepath).suffix,
                'scope': 'general',
                'error': str(e)
            }

    def _categorize_change(self, diff: str, filepath: str) -> str:
        """
        Categorize the type of change based on diff content.

        Args:
            diff: Git diff output
            filepath: File path

        Returns:
            Change category (feat/fix/docs/refactor/style/test/chore)
        """
        filepath_lower = filepath.lower()

        # Documentation files
        if any(ext in filepath_lower for ext in ['.md', '.txt', '.rst', 'readme', 'doc']):
            return 'docs'

        # Test files
        if any(pattern in filepath_lower for pattern in ['test_', '_test.', 'spec.', '.test.', '__tests__']):
            return 'test'

        # Configuration files
        if any(ext in filepath_lower for ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.conf', 'config']):
            return 'chore'

        # Style/formatting files
        if any(ext in filepath_lower for ext in ['.css', '.scss', '.less', '.style']):
            return 'style'

        # Analyze diff content for code changes
        if diff:
            diff_lower = diff.lower()

            # Look for new function/class definitions
            if any(keyword in diff_lower for keyword in ['+def ', '+class ', '+function ', '+const ', '+let ']):
                return 'feat'

            # Look for bug fix indicators
            if any(keyword in diff_lower for keyword in ['fix', 'bug', 'error', 'issue', 'repair']):
                return 'fix'

            # Look for performance keywords
            if any(keyword in diff_lower for keyword in ['optimize', 'performance', 'cache', 'speed']):
                return 'perf'

            # Look for refactoring indicators
            if any(keyword in diff_lower for keyword in ['refactor', 'restructure', 'reorganize', 'rename']):
                return 'refactor'

        # Default to feature for code files
        if any(ext in filepath_lower for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs']):
            return 'feat'

        return 'chore'

    def _extract_scope_from_path(self, filepath: str) -> str:
        """
        Extract scope from file path.

        Args:
            filepath: File path

        Returns:
            Scope string (e.g., 'auth', 'ui', 'api')
        """
        parts = Path(filepath).parts

        # Common scope patterns
        scope_keywords = {
            'auth': ['auth', 'authentication', 'login', 'oauth'],
            'api': ['api', 'endpoint', 'routes', 'controllers'],
            'ui': ['ui', 'components', 'views', 'templates', 'frontend'],
            'database': ['db', 'database', 'models', 'schema', 'migration'],
            'core': ['core', 'engine', 'kernel', 'lib', 'library'],
            'config': ['config', 'settings', 'configuration'],
            'tests': ['test', 'tests', 'spec', '__tests__'],
            'docs': ['doc', 'docs', 'documentation'],
            'utils': ['util', 'utils', 'helper', 'helpers'],
            'backend': ['backend', 'server', 'service'],
        }

        # Check path parts for scope keywords
        for scope, keywords in scope_keywords.items():
            for part in parts:
                if any(keyword in part.lower() for keyword in keywords):
                    return scope

        # Use first meaningful directory as scope
        if len(parts) > 1:
            return parts[0].replace('_', '-').replace('.', '')

        return 'general'

    def should_batch(self, file_count: int) -> Dict[str, Any]:
        """
        Determine if batching is needed based on file count.

        Args:
            file_count: Number of files to commit

        Returns:
            Analysis result with recommendation
        """
        requires_batching = file_count > self.threshold

        # Estimate number of batches (aim for ~5-8 files per batch)
        if requires_batching:
            recommended_batches = max(2, (file_count + 7) // 8)
        else:
            recommended_batches = 1

        return {
            'total_files': file_count,
            'threshold': self.threshold,
            'requires_batching': requires_batching,
            'recommended_batches': recommended_batches,
            'message': f"{'Batching recommended' if requires_batching else 'Single commit is fine'}"
        }

    def group_files_by_feature(self, file_analyses: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Group files by feature/functionality rather than just directory.

        Args:
            file_analyses: List of file analysis results

        Returns:
            List of file groups (batches)
        """
        # Group by (change_type, scope) combination
        groups = {}

        for analysis in file_analyses:
            change_type = analysis.get('change_type', 'chore')
            scope = analysis.get('scope', 'general')

            key = f"{change_type}:{scope}"

            if key not in groups:
                groups[key] = []

            groups[key].append(analysis)

        # Convert to list of batches
        batches = list(groups.values())

        # Sort batches by priority (feat > fix > docs > refactor > chore > style > test)
        priority_order = ['feat', 'fix', 'perf', 'docs', 'refactor', 'chore', 'style', 'test']

        def batch_priority(batch):
            change_type = batch[0].get('change_type', 'chore')
            try:
                return priority_order.index(change_type)
            except ValueError:
                return 999

        batches.sort(key=batch_priority)

        return batches

    def analyze_repository(self) -> Dict[str, Any]:
        """
        Complete repository analysis.

        Returns:
            Full analysis report
        """
        # Get git status
        status = self.get_git_status()

        # Combine all files to analyze
        all_files = status['staged'] + status['modified'] + status['untracked']

        # Analyze each file
        file_analyses = [self.analyze_file_changes(f) for f in all_files]

        # Check if batching is needed
        batch_analysis = self.should_batch(len(all_files))

        # Group files if batching is needed
        batches = []
        if batch_analysis['requires_batching']:
            batches = self.group_files_by_feature(file_analyses)
        else:
            batches = [file_analyses] if file_analyses else []

        return {
            'status': status,
            'batch_analysis': batch_analysis,
            'file_analyses': file_analyses,
            'batches': batches,
            'summary': f"Found {len(all_files)} files, grouped into {len(batches)} batch(es)"
        }


if __name__ == "__main__":
    # Example usage
    analyzer = GitAnalyzer(threshold=10)
    result = analyzer.analyze_repository()

    import json
    print(json.dumps(result, indent=2))
