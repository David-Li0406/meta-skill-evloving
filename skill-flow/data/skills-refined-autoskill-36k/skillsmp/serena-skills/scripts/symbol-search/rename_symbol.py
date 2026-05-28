#!/usr/bin/env python3
"""
Rename symbol across codebase using LSP
"""
import argparse
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
from lib.common.utils import auto_detect_language


def rename_symbol(
    project_root: str,
    file: str,
    symbol: str,
    new_name: str,
    language: str | None = None,
    lsp_timeout: float = 10.0
):
    """Rename symbol across the codebase"""
    
    # Auto-detect language if not specified
    if language is None:
        language = auto_detect_language(project_root, file)
        print(f"Auto-detected language: {language}", file=sys.stderr)
    
    # Setup language server
    try:
        lang = Language(language.lower())
    except (ValueError, KeyError) as e:
        print(f"Error: Unsupported language '{language}'", file=sys.stderr)
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
    ls.start()
    
    try:
        # Find symbol location
        doc_symbols = ls.request_document_symbols(file).root_symbols

        def find_target(syms):
            for sym in syms:
                name = sym.get("name")
                if name == symbol or (name and symbol.endswith(f"/{name}")):
                    return sym
                children = sym.get("children") or []
                found = find_target(children)
                if found:
                    return found
            return None

        target_sym = find_target(doc_symbols)
        
        if not target_sym:
            raise ValueError(f"Symbol not found: {symbol}")
        
        # Get rename edits from LSP
        range_info = target_sym.get("range") or {}
        start_info = range_info.get("start") or {}
        line = start_info.get("line")
        character = start_info.get("character")
        if line is None or character is None:
            raise ValueError(f"Symbol not found: {symbol}")

        workspace_edit = ls.request_rename_symbol_edit(file, line, character, new_name)
        
        changes = None if not workspace_edit else workspace_edit.get("changes")
        if not changes:
            return f"No changes needed for renaming {symbol} to {new_name}"
        
        # Apply edits to files
        files_changed = 0
        for file_uri, edits in changes.items():
            file_path = Path(str(file_uri).replace('file://', ''))
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply edits in reverse order (to preserve positions)
            sorted_edits = sorted(
                edits,
                key=lambda e: (
                    e.get("range", {}).get("start", {}).get("line", 0),
                    e.get("range", {}).get("start", {}).get("character", 0),
                ),
                reverse=True,
            )
            
            lines = content.split('\n')
            for edit in sorted_edits:
                edit_range = edit.get("range", {})
                start = edit_range.get("start", {})
                end = edit_range.get("end", {})
                start_line = start.get("line")
                start_char = start.get("character")
                end_line = end.get("line")
                end_char = end.get("character")
                
                # Simple single-line edit
                if start_line == end_line and start_line is not None and start_char is not None and end_char is not None:
                    line = lines[start_line]
                    lines[start_line] = line[:start_char] + edit.get("newText", "") + line[end_char:]
            
            new_content = '\n'.join(lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            files_changed += 1
        
        return f"Symbol renamed: {symbol} -> {new_name} ({files_changed} file(s) changed)"
        
    finally:
        ls.stop()


def main():
    parser = argparse.ArgumentParser(description="Rename symbol across codebase")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="File containing symbol")
    parser.add_argument("--symbol", required=True, help="Symbol name path")
    parser.add_argument("--new-name", required=True, help="New symbol name")
    parser.add_argument("--language", default=None, help="Programming language (auto-detected if not specified)")
    parser.add_argument("--lsp-timeout", type=float, default=10.0, help="LSP analysis timeout in seconds (default: 10)")
    
    args = parser.parse_args()
    
    try:
        result = rename_symbol(
            args.project_root,
            args.file,
            args.symbol,
            args.new_name,
            args.language,
            args.lsp_timeout
        )
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
