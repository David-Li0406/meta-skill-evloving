"""
Language configuration module.
Maps language-specific tools, commands, and settings.
"""

from typing import Dict, List, Any, Optional


class LanguageConfig:
    """Configuration for language-specific tools and settings."""

    # Tool requirements for each language
    TOOL_REQUIREMENTS = {
        'python': {
            'formatter': 'black',
            'linter': 'flake8',
            'type_checker': 'mypy',
            'optional': ['isort', 'autopep8']
        },
        'javascript': {
            'formatter': 'prettier',
            'linter': 'eslint',
            'optional': []
        },
        'typescript': {
            'formatter': 'prettier',
            'linter': 'eslint',
            'type_checker': 'tsc',
            'optional': []
        },
        'java': {
            'formatter': 'google-java-format',
            'linter': 'checkstyle',
            'compiler': 'javac',
            'optional': ['spotbugs']
        },
        'go': {
            'formatter': 'gofmt',
            'linter': 'golangci-lint',
            'compiler': 'go',
            'optional': ['goimports', 'go vet']
        },
        'rust': {
            'formatter': 'rustfmt',
            'linter': 'clippy',
            'compiler': 'rustc',
            'optional': []
        }
    }

    # Installation commands
    INSTALL_COMMANDS = {
        'python': {
            'black': 'pip install black',
            'flake8': 'pip install flake8',
            'mypy': 'pip install mypy',
            'isort': 'pip install isort',
            'autopep8': 'pip install autopep8'
        },
        'javascript': {
            'prettier': 'npm install -g prettier',
            'eslint': 'npm install -g eslint'
        },
        'typescript': {
            'prettier': 'npm install -g prettier',
            'eslint': 'npm install -g eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin',
            'tsc': 'npm install -g typescript'
        },
        'java': {
            'google-java-format': 'Download from https://github.com/google/google-java-format/releases',
            'checkstyle': 'Download from https://checkstyle.org/',
            'javac': 'Included with JDK'
        },
        'go': {
            'gofmt': 'Included with Go',
            'golangci-lint': 'go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest',
            'goimports': 'go install golang.org/x/tools/cmd/goimports@latest'
        },
        'rust': {
            'rustfmt': 'rustup component add rustfmt',
            'clippy': 'rustup component add clippy',
            'rustc': 'Included with Rust'
        }
    }

    # File extensions
    FILE_EXTENSIONS = {
        'python': ['.py', '.pyw'],
        'javascript': ['.js', '.jsx', '.mjs'],
        'typescript': ['.ts', '.tsx'],
        'java': ['.java'],
        'go': ['.go'],
        'rust': ['.rs']
    }

    # Default configurations
    DEFAULT_CONFIGS = {
        'python': {
            'black': {
                'line_length': 88,
                'target_version': ['py38', 'py39', 'py310', 'py311']
            },
            'flake8': {
                'max_line_length': 88,
                'ignore': ['E203', 'E266', 'E501', 'W503']
            },
            'mypy': {
                'strict': False,
                'ignore_missing_imports': True
            }
        },
        'javascript': {
            'prettier': {
                'semi': True,
                'singleQuote': False,
                'tabWidth': 2,
                'trailingComma': 'es5'
            },
            'eslint': {
                'env': {
                    'browser': True,
                    'es2021': True,
                    'node': True
                }
            }
        },
        'typescript': {
            'prettier': {
                'semi': True,
                'singleQuote': False,
                'tabWidth': 2,
                'trailingComma': 'all'
            },
            'eslint': {
                'parser': '@typescript-eslint/parser',
                'plugins': ['@typescript-eslint']
            }
        },
        'java': {
            'google-java-format': {
                'style': 'google'
            }
        },
        'go': {
            'gofmt': {
                'simplify': True
            }
        },
        'rust': {
            'rustfmt': {
                'edition': '2021'
            }
        }
    }

    @classmethod
    def get_tools(cls, language: str) -> Dict[str, Any]:
        """Get required tools for a language."""
        return cls.TOOL_REQUIREMENTS.get(language.lower(), {})

    @classmethod
    def get_install_commands(cls, language: str) -> Dict[str, str]:
        """Get installation commands for a language's tools."""
        return cls.INSTALL_COMMANDS.get(language.lower(), {})

    @classmethod
    def get_default_config(cls, language: str, tool: str = None) -> Dict[str, Any]:
        """Get default configuration for a language or specific tool."""
        lang_config = cls.DEFAULT_CONFIGS.get(language.lower(), {})

        if tool:
            return lang_config.get(tool, {})

        return lang_config

    @classmethod
    def get_file_extensions(cls, language: str) -> List[str]:
        """Get file extensions for a language."""
        return cls.FILE_EXTENSIONS.get(language.lower(), [])

    @classmethod
    def detect_language(cls, file_path: str) -> Optional[str]:
        """Detect language from file extension."""
        import os
        _, ext = os.path.splitext(file_path)

        for language, extensions in cls.FILE_EXTENSIONS.items():
            if ext.lower() in extensions:
                return language

        return None

    @classmethod
    def validate_tool_availability(cls, language: str) -> Dict[str, bool]:
        """
        Check which tools are available for a language.

        Returns:
            Dictionary mapping tool names to availability status
        """
        import subprocess

        tools = cls.get_tools(language)
        availability = {}

        for tool_type, tool_name in tools.items():
            if tool_type == 'optional':
                for opt_tool in tool_name:
                    availability[opt_tool] = cls._check_tool(opt_tool)
            else:
                availability[tool_name] = cls._check_tool(tool_name)

        return availability

    @staticmethod
    def _check_tool(tool_name: str) -> bool:
        """Check if a tool is installed."""
        import subprocess

        # Common version check commands
        version_commands = [
            [tool_name, '--version'],
            [tool_name, '-v'],
            [tool_name, 'version'],
            [tool_name, '-h']
        ]

        for cmd in version_commands:
            try:
                subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=2
                )
                return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return False

    @classmethod
    def get_missing_tools_report(cls, language: str) -> Dict[str, Any]:
        """
        Generate report of missing tools for a language.

        Returns:
            Dictionary with missing tools and installation instructions
        """
        availability = cls.validate_tool_availability(language)
        install_commands = cls.get_install_commands(language)

        missing_tools = []
        for tool, available in availability.items():
            if not available:
                missing_tools.append({
                    'tool': tool,
                    'install_command': install_commands.get(tool, 'See documentation')
                })

        return {
            'language': language,
            'missing_count': len(missing_tools),
            'missing_tools': missing_tools,
            'all_available': len(missing_tools) == 0
        }


# Example usage and utilities
def get_setup_instructions(language: str) -> str:
    """Generate setup instructions for a language."""
    config = LanguageConfig()
    tools = config.get_tools(language)
    install_cmds = config.get_install_commands(language)

    instructions = f"# Setup Instructions for {language.title()}\n\n"
    instructions += "## Required Tools\n\n"

    for tool_type, tool_name in tools.items():
        if tool_type == 'optional':
            instructions += "\n## Optional Tools\n\n"
            for opt_tool in tool_name:
                cmd = install_cmds.get(opt_tool, 'See documentation')
                instructions += f"- **{opt_tool}**: `{cmd}`\n"
        else:
            cmd = install_cmds.get(tool_name, 'See documentation')
            instructions += f"- **{tool_name}** ({tool_type}): `{cmd}`\n"

    return instructions
