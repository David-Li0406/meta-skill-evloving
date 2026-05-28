#!/usr/bin/env python3
"""
Common utilities for Serena Skills
"""
import json
import os
import re
from pathlib import Path
from typing import Any

try:
    import pathspec
    HAS_PATHSPEC = True
except ImportError:
    HAS_PATHSPEC = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_project_config(project_root: str) -> dict[str, Any]:
    """Load project configuration from project.yml"""
    if not HAS_YAML:
        return {}
    
    project_yml = Path(project_root) / ".tmp" / ".serena-skills" / "project.yml"
    if not project_yml.exists():
        return {}
    
    with open(project_yml, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_ignore_patterns(project_root: str):
    """
    Load and merge ignore patterns from project.yml and .gitignore
    Returns pathspec.PathSpec if pathspec is available, None otherwise
    """
    if not HAS_PATHSPEC:
        return None
    
    patterns = []
    config = load_project_config(project_root)
    
    # Load from project.yml
    patterns.extend(config.get('ignored_paths', []))
    
    # Load gitignore if enabled
    if config.get('ignore_all_files_in_gitignore', True):
        gitignore = Path(project_root) / ".gitignore"
        if gitignore.exists():
            with open(gitignore, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
    
    if not patterns:
        return None
    
    # Create pathspec matcher
    return pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern,
        patterns
    )


def is_ignored_path(path: str, project_root: str, ignore_spec=None) -> bool:
    """Check if path should be ignored"""
    if ignore_spec is None:
        ignore_spec = load_ignore_patterns(project_root)
    
    if ignore_spec is None:
        return False
    
    # Convert to relative path if absolute
    if os.path.isabs(path):
        try:
            path = os.path.relpath(path, project_root)
        except ValueError:
            return False
    
    return ignore_spec.match_file(path)


def validate_relative_path(
    project_root: str,
    relative_path: str,
    check_ignored: bool = True,
    ignore_spec=None
) -> None:
    """
    Validate relative path and check if it's ignored
    Raises FileNotFoundError or ValueError if invalid
    """
    full_path = os.path.join(project_root, relative_path)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Path not found: {relative_path}")
    
    if check_ignored and is_ignored_path(relative_path, project_root, ignore_spec):
        raise ValueError(
            f"Path is ignored: {relative_path}. "
            "Check project.yml ignored_paths or .gitignore"
        )


def limit_output_length(
    result: Any,
    project_root: str,
    max_chars: int = -1
) -> str:
    """
    Convert result to JSON and limit length based on configuration
    Returns JSON string or error dict
    """
    config = load_project_config(project_root)
    
    if max_chars == -1:
        max_chars = config.get('max_answer_chars', 100000)
    
    result_str = json.dumps(result, indent=2)
    
    if len(result_str) > max_chars:
        error_result = {
            "error": "Output too long",
            "length": len(result_str),
            "max_allowed": max_chars,
            "hint": "Increase max_answer_chars in project.yml or use more specific query"
        }
        return json.dumps(error_result, indent=2)
    
    return result_str


def format_error(error: Exception, context: dict[str, Any] | None = None) -> str:
    """
    Format error as JSON with context and hints
    """
    error_info = {
        "error": str(error),
        "error_type": type(error).__name__,
    }
    
    if context:
        error_info.update(context)
    
    # Add hints based on error type
    if isinstance(error, FileNotFoundError):
        error_info["hint"] = "Check if the path is correct relative to project root"
    elif isinstance(error, ValueError):
        error_info["hint"] = "Verify the parameters and try again"
    elif isinstance(error, PermissionError):
        error_info["hint"] = "Check file permissions"
    
    return json.dumps(error_info, indent=2)


def replace_content_advanced(
    content: str,
    needle: str,
    repl: str,
    mode: str = "literal",
    allow_multiple: bool = False
) -> tuple[str, int, int | None]:
    """
    Advanced content replacement with ambiguity detection and backreferences
    
    Returns: (new_content, count, first_match_line)
    """
    if mode == "literal":
        count = content.count(needle)
        if count == 0:
            raise ValueError("Pattern not found in content")
        if count > 1 and not allow_multiple:
            raise ValueError(
                f"Pattern found {count} times. "
                "Set allow_multiple=True or make pattern more specific"
            )
        
        new_content = content.replace(needle, repl)
        
        # Find first match line
        first_match_line = None
        for i, line in enumerate(content.split('\n'), 1):
            if needle.split('\n')[0] in line:
                first_match_line = i
                break
        
        return new_content, count, first_match_line
    
    elif mode == "regex":
        pattern = re.compile(needle, re.DOTALL | re.MULTILINE)
        matches = list(pattern.finditer(content))
        count = len(matches)
        
        if count == 0:
            raise ValueError("Pattern not found in content")
        if count > 1 and not allow_multiple:
            raise ValueError(
                f"Pattern found {count} times. "
                "Set allow_multiple=True or make pattern more specific"
            )
        
        # Ambiguity detection for multi-line matches
        for match in matches:
            matched_text = match.group(0)
            if "\n" in matched_text:
                # Check for overlapping matches
                if pattern.search(matched_text[1:]):
                    raise ValueError(
                        "Match is ambiguous: the pattern matches multiple overlapping "
                        "occurrences. Please make the pattern more specific."
                    )
        
        # Backreference expansion ($!1, $!2, etc.)
        def expand_backreferences(match: re.Match) -> str:
            def replace_ref(ref_match: re.Match) -> str:
                group_num = int(ref_match.group(1))
                try:
                    return match.group(group_num) or ''
                except IndexError:
                    return ref_match.group(0)
            
            return re.sub(r'\$!(\d+)', replace_ref, repl)
        
        new_content = pattern.sub(expand_backreferences, content)
        
        # Find first match line
        first_match_line = None
        if matches:
            first_match_pos = matches[0].start()
            first_match_line = content[:first_match_pos].count('\n') + 1
        
        return new_content, count, first_match_line
    
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be 'literal' or 'regex'")


def create_lsp_settings(project_root: str):
    """Create SolidLSP settings with consistent configuration"""
    from solidlsp.settings import SolidLSPSettings
    
    return SolidLSPSettings(
        solidlsp_dir=os.path.expanduser("~/.serena"),
        project_data_relative_path=".tmp/.serena-skills"
    )


def get_project_language(project_root: str) -> str:
    """Get project language from configuration or auto-detect"""
    config = load_project_config(project_root)
    languages = config.get('languages', [])
    
    if languages:
        return languages[0]
    
    # Auto-detect if not configured
    for root, dirs, files in os.walk(project_root):
        if any(f.endswith(('.ts', '.tsx')) for f in files):
            return "typescript"
        elif any(f.endswith('.java') for f in files):
            return "java"
        elif any(f.endswith('.go') for f in files):
            return "go"
        elif any(f.endswith('.rs') for f in files):
            return "rust"
        # Don't walk too deep
        if root != project_root:
            break
    
    return "python"  # Default


def detect_language_from_file(file_path: str) -> str | None:
    """Detect language from file extension"""
    ext_map = {
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.py': 'python',
        '.cs': 'csharp',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.h': 'c',
    }
    ext = Path(file_path).suffix
    return ext_map.get(ext)


def auto_detect_language(project_root: str, file_path: str | None = None, default: str = "python") -> str:
    """
    Auto-detect language with multiple strategies:
    1. From project config (if activated)
    2. From file extension (if file specified)
    3. From project directory scan
    4. Default fallback
    """
    # Strategy 1: Project config
    config = load_project_config(project_root)
    languages = config.get('languages', [])
    if languages:
        return languages[0]
    
    # Strategy 2: File extension
    if file_path:
        lang = detect_language_from_file(file_path)
        if lang:
            return lang
    
    # Strategy 3: Project scan
    return get_project_language(project_root)
