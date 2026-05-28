"""
Batch Committer Module
Groups files by feature and generates Conventional Commit messages.
"""

import subprocess
from typing import Dict, List, Any, Optional
from git_analyzer import GitAnalyzer


class BatchCommitter:
    """Generates and executes batch commits with Conventional Commit messages."""

    def __init__(self, language: str = 'en', dry_run: bool = True):
        """
        Initialize Batch Committer.

        Args:
            language: Language for commit messages (en, zh, es, etc.)
            dry_run: If True, only preview commits without executing
        """
        self.language = language
        self.dry_run = dry_run
        self.analyzer = GitAnalyzer()

    def generate_commit_message(
        self,
        change_type: str,
        scope: str,
        files: List[Dict[str, Any]],
        language: str = 'en'
    ) -> str:
        """
        Generate a Conventional Commit message.

        Args:
            change_type: Type of change (feat/fix/docs/etc.)
            scope: Scope of change (auth/api/ui/etc.)
            files: List of files in this batch
            language: Language for commit message

        Returns:
            Formatted commit message
        """
        # Extract file paths
        file_paths = [f['filepath'] for f in files]

        # Generate description based on files and change type
        description = self._generate_description(change_type, scope, file_paths, language)

        # Build commit message
        if scope and scope != 'general':
            commit_msg = f"{change_type}({scope}): {description}"
        else:
            commit_msg = f"{change_type}: {description}"

        # Add file list as body if multiple files
        if len(file_paths) > 1:
            file_list = '\n'.join([f"- {fp}" for fp in file_paths])
            commit_msg += f"\n\n{file_list}"

        return commit_msg

    def _generate_description(
        self,
        change_type: str,
        scope: str,
        file_paths: List[str],
        language: str
    ) -> str:
        """
        Generate commit message description.

        Args:
            change_type: Type of change
            scope: Scope of change
            file_paths: List of file paths
            language: Language for message

        Returns:
            Description string
        """
        # Description templates by language and change type
        templates = {
            'en': {
                'feat': 'add {scope} functionality',
                'fix': 'fix {scope} issues',
                'docs': 'update {scope} documentation',
                'refactor': 'refactor {scope} implementation',
                'chore': 'update {scope} configuration',
                'style': 'improve {scope} styling',
                'test': 'add {scope} tests',
                'perf': 'optimize {scope} performance'
            },
            'zh': {
                'feat': '新增{scope}功能',
                'fix': '修复{scope}问题',
                'docs': '更新{scope}文档',
                'refactor': '重构{scope}实现',
                'chore': '更新{scope}配置',
                'style': '优化{scope}样式',
                'test': '添加{scope}测试',
                'perf': '优化{scope}性能'
            },
            'es': {
                'feat': 'agregar funcionalidad de {scope}',
                'fix': 'corregir problemas de {scope}',
                'docs': 'actualizar documentación de {scope}',
                'refactor': 'refactorizar implementación de {scope}',
                'chore': 'actualizar configuración de {scope}',
                'style': 'mejorar estilos de {scope}',
                'test': 'agregar pruebas de {scope}',
                'perf': 'optimizar rendimiento de {scope}'
            },
            'ja': {
                'feat': '{scope}機能を追加',
                'fix': '{scope}の問題を修正',
                'docs': '{scope}ドキュメントを更新',
                'refactor': '{scope}の実装をリファクタリング',
                'chore': '{scope}設定を更新',
                'style': '{scope}スタイルを改善',
                'test': '{scope}テストを追加',
                'perf': '{scope}パフォーマンスを最適化'
            }
        }

        # Get language templates (fallback to English)
        lang_templates = templates.get(language, templates['en'])

        # Get template for change type (fallback to chore)
        template = lang_templates.get(change_type, lang_templates['chore'])

        # Format scope for description
        scope_desc = scope if scope != 'general' else 'core'

        # Generate description
        description = template.format(scope=scope_desc)

        # For single file, include filename
        if len(file_paths) == 1:
            from pathlib import Path
            filename = Path(file_paths[0]).name

            if language == 'zh':
                description = f"{description} ({filename})"
            else:
                description = f"{description} in {filename}"

        return description

    def create_batch_plan(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create execution plan for batch commits.

        Args:
            analysis_result: Result from GitAnalyzer.analyze_repository()

        Returns:
            List of batch commit plans
        """
        batches = analysis_result.get('batches', [])
        batch_plans = []

        for idx, batch in enumerate(batches, 1):
            if not batch:
                continue

            # Get change type and scope from first file in batch
            change_type = batch[0].get('change_type', 'chore')
            scope = batch[0].get('scope', 'general')

            # Get file paths
            file_paths = [f['filepath'] for f in batch]

            # Generate commit message
            commit_message = self.generate_commit_message(
                change_type, scope, batch, self.language
            )

            batch_plan = {
                'batch_id': idx,
                'change_type': change_type,
                'scope': scope,
                'files': file_paths,
                'file_count': len(file_paths),
                'commit_message': commit_message
            }

            batch_plans.append(batch_plan)

        return batch_plans

    def stage_files(self, file_paths: List[str]) -> bool:
        """
        Stage specific files for commit.

        Args:
            file_paths: List of file paths to stage

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.dry_run:
                print(f"[DRY RUN] Would stage: {', '.join(file_paths)}")
                return True

            subprocess.run(
                ['git', 'add'] + file_paths,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error staging files: {e}")
            return False

    def unstage_all(self) -> bool:
        """
        Unstage all currently staged files.

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.dry_run:
                print("[DRY RUN] Would unstage all files")
                return True

            subprocess.run(
                ['git', 'reset', 'HEAD'],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error unstaging files: {e}")
            return False

    def commit(self, message: str) -> bool:
        """
        Create a commit with the given message.

        Args:
            message: Commit message

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.dry_run:
                print(f"[DRY RUN] Would commit with message:\n{message}\n")
                return True

            subprocess.run(
                ['git', 'commit', '-m', message],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating commit: {e}")
            return False

    def execute_batch_commits(self, batch_plans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute all batch commits.

        Args:
            batch_plans: List of batch commit plans

        Returns:
            Execution summary
        """
        successful_commits = []
        failed_commits = []

        # Unstage all files first
        if not self.unstage_all():
            return {
                'success': False,
                'error': 'Failed to unstage files',
                'successful_commits': [],
                'failed_commits': batch_plans
            }

        # Execute each batch
        for plan in batch_plans:
            batch_id = plan['batch_id']
            files = plan['files']
            message = plan['commit_message']

            print(f"\n--- Batch {batch_id}/{len(batch_plans)} ---")
            print(f"Type: {plan['change_type']}({plan['scope']})")
            print(f"Files: {len(files)}")

            # Stage files
            if not self.stage_files(files):
                failed_commits.append(plan)
                continue

            # Commit
            if not self.commit(message):
                failed_commits.append(plan)
                continue

            successful_commits.append(plan)
            print(f"✓ Committed: {message.split(':')[0]}")

        return {
            'success': len(failed_commits) == 0,
            'total_batches': len(batch_plans),
            'successful_commits': successful_commits,
            'failed_commits': failed_commits,
            'summary': f"Completed {len(successful_commits)}/{len(batch_plans)} commits"
        }

    def preview_batch_commits(self, batch_plans: List[Dict[str, Any]]) -> str:
        """
        Generate a preview of batch commits.

        Args:
            batch_plans: List of batch commit plans

        Returns:
            Formatted preview string
        """
        preview = "=" * 60 + "\n"
        preview += "BATCH COMMIT PREVIEW\n"
        preview += "=" * 60 + "\n\n"

        for plan in batch_plans:
            preview += f"Batch {plan['batch_id']}: {plan['change_type']}({plan['scope']})\n"
            preview += f"Files ({len(plan['files'])}):\n"

            for filepath in plan['files']:
                preview += f"  - {filepath}\n"

            preview += f"\nCommit Message:\n{plan['commit_message']}\n"
            preview += "-" * 60 + "\n\n"

        preview += f"Total: {len(batch_plans)} batch(es)\n"

        return preview


if __name__ == "__main__":
    # Example usage
    import json

    # Analyze repository
    analyzer = GitAnalyzer(threshold=10)
    analysis = analyzer.analyze_repository()

    # Create batch committer
    committer = BatchCommitter(language='en', dry_run=True)

    # Generate batch plans
    plans = committer.create_batch_plan(analysis)

    # Preview
    print(committer.preview_batch_commits(plans))

    # Execute (dry run)
    result = committer.execute_batch_commits(plans)
    print("\nExecution Result:")
    print(json.dumps(result, indent=2))
