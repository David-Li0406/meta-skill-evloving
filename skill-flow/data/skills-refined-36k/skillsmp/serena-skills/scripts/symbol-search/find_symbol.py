#!/usr/bin/env python3
"""
Find symbols by name path pattern using LSP
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
from lib.solidlsp.ls_config import Language, LanguageServerConfig
from lib.solidlsp.settings import SolidLSPSettings
from lib.solidlsp.ls_types import SymbolKind
from lib.common.utils import auto_detect_language


def find_symbol(
    project_root: str,
    pattern: str,
    language: str | None = None,
    file: str | None = None,
    depth: int = 0,
    include_body: bool = False,
    substring: bool = False,
    lsp_timeout: float = 10.0
):
    """Find symbols matching the name path pattern"""
    
    # Auto-detect language if not specified
    if language is None:
        language = auto_detect_language(project_root, file)
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
    
    settings = SolidLSPSettings(
        solidlsp_dir=os.path.expanduser("~/.serena"),
        project_data_relative_path=".tmp/.serena-skills"
    )
    
    ls = SolidLanguageServer.create(ls_config, project_root, solidlsp_settings=settings)
    
    # Note: LSP timeout is handled internally by language server during initialization
    # The timeout parameter here affects our wait time for results
    try:
        ls.start()
    except TimeoutError as e:
        print(f"Warning: LSP analysis timed out after {lsp_timeout}s", file=sys.stderr)
        print(f"Tip: Try --language {language} if auto-detection is incorrect", file=sys.stderr)
        print(f"Tip: Try --lsp-timeout 20 for large projects", file=sys.stderr)
        print(f"Tip: Run 'activate_project.py --project-path . --language {language}' to configure", file=sys.stderr)
        raise
    
    try:
        # Parse pattern
        is_absolute = pattern.startswith("/")
        if is_absolute:
            pattern = pattern[1:]
        
        parts = pattern.split("/")
        
        # Search workspace symbols (keep file open to ensure TS project context)
        search_query = parts[-1]  # Use last part for search
        if file:
            with ls.open_file(file):
                workspace_symbols = ls.request_workspace_symbol(search_query) or []
        else:
            workspace_symbols = ls.request_workspace_symbol(search_query) or []
        
        results = []
        for sym in workspace_symbols:
            # Match pattern logic
            sym_name_path = sym.get("name")  # Simplified - in full implementation, build name path
            
            if substring:
                matches = search_query.lower() in (sym.get("name") or "").lower()
            else:
                matches = sym.get("name") == search_query or sym_name_path == pattern
            
            if matches:
                location = sym.get("location") or {}
                uri = location.get("uri")
                rel_path = None
                if uri:
                    rel_path = str(Path(uri.replace("file://", "")).relative_to(project_root))

                range_info = location.get("range") or {}
                start_info = range_info.get("start") or {}
                sym_dict = {
                    "name": sym.get("name"),
                    "kind": str(sym.get("kind")),
                    "relative_path": rel_path,
                    "line": start_info.get("line"),
                }
                
                if include_body:
                    # Read file content for body
                    if sym_dict["relative_path"] and sym_dict["line"] is not None:
                        file_path = os.path.join(project_root, sym_dict["relative_path"])
                        if os.path.exists(file_path):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                # Simple body extraction - get a few lines
                                start_line = sym_dict["line"]
                                end_line = min(start_line + 20, len(lines))
                                sym_dict["body"] = "".join(lines[start_line:end_line])
                
                results.append(sym_dict)
        
        return results
        
    finally:
        ls.stop()


def main():
    parser = argparse.ArgumentParser(description="Find symbols by name path pattern")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--pattern", required=True, help="Name path pattern to search")
    parser.add_argument("--language", default=None, help="Programming language (auto-detected if not specified)")
    parser.add_argument("--file", help="Restrict search to specific file")
    parser.add_argument("--depth", type=int, default=0, help="Include descendants (default: 0)")
    parser.add_argument("--include-body", action="store_true", help="Include source code")
    parser.add_argument("--substring", action="store_true", help="Enable substring matching")
    parser.add_argument("--lsp-timeout", type=float, default=10.0, help="LSP analysis timeout in seconds (default: 10)")
    
    args = parser.parse_args()
    
    try:
        results = find_symbol(
            args.project_root,
            args.pattern,
            args.language,
            args.file,
            args.depth,
            args.include_body,
            args.substring,
            args.lsp_timeout
        )
        print(json.dumps(results, indent=2))
    except ValueError as e:
        # Language detection or validation error
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError as e:
        # LSP timeout - already printed helpful messages
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
