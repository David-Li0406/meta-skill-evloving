"""
Template loading and rendering utilities.
"""

import re
from pathlib import Path
from datetime import datetime
import subprocess


class TemplateManager:
    """Load and render entry templates."""

    def __init__(self, scripts_dir: Path = None):
        """
        Initialize template manager.

        Args:
            scripts_dir: Path to scripts/ directory (auto-detected if None)
        """
        if scripts_dir is None:
            # Auto-detect: assume we're in lib/ subdirectory
            scripts_dir = Path(__file__).parent.parent

        self.templates_dir = scripts_dir.parent / 'templates' / 'entries'

        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

    def load_template(self, template_name: str) -> str:
        """
        Load template content.

        Args:
            template_name: Template filename (e.g., "decision-entry.md")

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        return template_path.read_text(encoding='utf-8')

    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render template with variables.

        Args:
            template_name: Template filename
            **kwargs: Variable substitutions

        Returns:
            Rendered template

        Supported variables:
            - {ID}: Auto-generated ID
            - {DATE}: Current date (YYYY-MM-DD)
            - {TIMESTAMP}: Current timestamp (YYYY-MM-DD HH:MM UTC)
            - {AUTHOR}: From git config user.name or $USER
            - Any other custom variables passed in kwargs
        """
        template = self.load_template(template_name)

        # Build variable map with defaults
        variables = {
            'DATE': datetime.now().strftime('%Y-%m-%d'),
            'TIMESTAMP': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'AUTHOR': self._get_author()
        }

        # Add user-provided variables
        variables.update(kwargs)

        # Substitute variables
        rendered = template
        for key, value in variables.items():
            placeholder = '{' + key + '}'
            rendered = rendered.replace(placeholder, str(value))

        return rendered

    @staticmethod
    def _get_author() -> str:
        """
        Get author name from git config or fallback to $USER.

        Returns:
            Author name
        """
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except:
            pass

        # Fallback to $USER environment variable
        import os
        return os.environ.get('USER', 'Unknown')

    def get_template_path(self, template_name: str) -> Path:
        """
        Get full path to template file.

        Args:
            template_name: Template filename

        Returns:
            Path to template file
        """
        return self.templates_dir / template_name
