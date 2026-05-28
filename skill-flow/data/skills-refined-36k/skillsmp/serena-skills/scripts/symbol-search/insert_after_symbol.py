#!/usr/bin/env python3
"""
Insert code after a symbol using LSP
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


def insert_after_symbol(
    project_root: str,
    file: str,
    symbol: str,
    body: str,
    language: str | None = None,
    lsp_timeout: float = 10.0
):
    """Insert code after symbol"""
    
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
        full_path = os.path.join(project_root, file)
        
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
        
        # Read file
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Insert after symbol (after end line)
        range_info = target_sym.get("range") or {}
        end_info = range_info.get("end") or {}
        end_line = end_info.get("line")
        if end_line is None:
            raise ValueError(f"Symbol not found: {symbol}")
        
        # Insert body after the symbol
        new_lines = lines[:end_line + 1] + [body if body.endswith('\n') else body + '\n'] + lines[end_line + 1:]
        
        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return f"Code inserted after symbol: {symbol}"
        
    finally:
        ls.stop()


def main():
    parser = argparse.ArgumentParser(description="Insert code after symbol")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="File containing symbol")
    parser.add_argument("--symbol", required=True, help="Symbol name path")
    parser.add_argument("--body", required=True, help="Code to insert")
    parser.add_argument("--language", default=None, help="Programming language (auto-detected if not specified)")
    parser.add_argument("--lsp-timeout", type=float, default=10.0, help="LSP analysis timeout in seconds (default: 10)")
    
    args = parser.parse_args()
    
    try:
        result = insert_after_symbol(
            args.project_root,
            args.file,
            args.symbol,
            args.body,
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
