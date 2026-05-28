#!/usr/bin/env python3
"""
Get symbols overview from a file using LSP
"""
import argparse
import json
import os
import sys
import platform
from pathlib import Path

# Auto-activate venv if available
skills_root = Path(__file__).parent.parent.parent
if platform.system() == "Windows":
    venv_python = skills_root / ".venv" / "Scripts" / "python.exe"
else:
    venv_python = skills_root / ".venv" / "bin" / "python"

if venv_python.exists() and str(Path(sys.executable).parent) != str(venv_python.parent):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# Add serena-skills to path
sys.path.insert(0, str(skills_root))

from lib.solidlsp import SolidLanguageServer
from solidlsp import ls_types
from lib.solidlsp.ls_config import Language, LanguageServerConfig
from lib.common.utils import (
    create_lsp_settings,
    get_project_language,
    limit_output_length,
    format_error
)


def get_symbols_overview(
    project_root: str,
    relative_file_path: str,
    depth: int = 0,
    language: str | None = None,
    max_answer_chars: int = -1,
    lsp_timeout: float = 10.0
):
    """Get symbols overview for a file"""
    
    # Auto-detect language if not provided
    if language is None:
        from lib.common.utils import auto_detect_language
        language = auto_detect_language(project_root, relative_file_path)
        print(f"Auto-detected language: {language}", file=sys.stderr)
    
    # Setup language server
    try:
        lang = Language(language.lower())
    except (ValueError, KeyError) as e:
        print(f"Error: Unsupported language '{language}'", file=sys.stderr)
        print(f"Tip: Supported languages include: typescript, javascript, python, java, go, rust, etc.", file=sys.stderr)
        raise ValueError(f"Unsupported language: {language}") from e
    ls_config = LanguageServerConfig(
        code_language=lang,
        ignored_paths=[],
        encoding="utf-8"
    )
    
    settings = create_lsp_settings(project_root)
    
    ls = SolidLanguageServer.create(ls_config, project_root, solidlsp_settings=settings)
    
    try:
        ls.start()
    except TimeoutError as e:
        print(f"Warning: LSP analysis timed out after {lsp_timeout}s", file=sys.stderr)
        print(f"Tip: Try --language {language} if auto-detection is incorrect", file=sys.stderr)
        print(f"Tip: Try --lsp-timeout 20 for large projects", file=sys.stderr)
        print(f"Tip: Run 'activate_project.py --project-path . --language {language}' to configure", file=sys.stderr)
        raise
    
    try:
        # Get document symbols
        full_path = os.path.join(project_root, relative_file_path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_file_path}")
        
        symbols = ls.request_document_symbols(relative_file_path).root_symbols
        
        # Transform to compact format
        def get_kind_name(kind_value):
            if hasattr(kind_value, "name"):
                return kind_value.name
            try:
                return ls_types.SymbolKind(kind_value).name
            except Exception:
                return str(kind_value)

        def transform_symbols(syms, current_depth=0):
            result = {}
            for sym in syms:
                kind_name = get_kind_name(sym.get("kind"))
                if kind_name not in result:
                    result[kind_name] = []
                
                children = sym.get("children") or []
                if current_depth < depth and children:
                    children_dict = transform_symbols(children, current_depth + 1)
                    result[kind_name].append({sym.get("name"): children_dict})
                else:
                    result[kind_name].append(sym.get("name"))
            
            return result
        
        overview = transform_symbols(symbols)
        return overview
        
    finally:
        ls.stop()


def main():
    parser = argparse.ArgumentParser(description="Get symbols overview from a file")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="Relative path to file")
    parser.add_argument("--depth", type=int, default=0, help="Descendant depth (default: 0)")
    parser.add_argument("--language", default=None, help="Programming language (auto-detected if not specified)")
    parser.add_argument("--max-answer-chars", type=int, default=-1, help="Max output chars (-1 for default)")
    parser.add_argument("--lsp-timeout", type=float, default=10.0, help="LSP analysis timeout in seconds (default: 10)")
    
    args = parser.parse_args()
    
    try:
        overview = get_symbols_overview(
            args.project_root,
            args.file,
            args.depth,
            args.language,
            args.max_answer_chars,
            args.lsp_timeout
        )
        
        # Apply output limit
        output = limit_output_length(overview, args.project_root, args.max_answer_chars)
        print(output)
        
    except ValueError as e:
        # Language detection or validation error
        context = {
            "project_root": args.project_root,
            "file": args.file,
            "operation": "get_symbols_overview"
        }
        print(format_error(e, context), file=sys.stderr)
        sys.exit(1)
    except TimeoutError as e:
        # LSP timeout - already printed helpful messages
        sys.exit(1)
    except Exception as e:
        context = {
            "project_root": args.project_root,
            "file": args.file,
            "operation": "get_symbols_overview"
        }
        print(format_error(e, context), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
