#!/usr/bin/env python3
"""
Find references to a symbol using LSP
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
from lib.common.utils import auto_detect_language


def find_references(
    project_root: str,
    file: str,
    symbol: str,
    language: str | None = None,
    lsp_timeout: float = 10.0
):
    """Find all references to a symbol"""
    
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
    
    try:
        ls.start()
    except TimeoutError as e:
        print(f"Warning: LSP analysis timed out after {lsp_timeout}s", file=sys.stderr)
        print(f"Tip: Try --language {language} if auto-detection is incorrect", file=sys.stderr)
        print(f"Tip: Try --lsp-timeout 20 for large projects", file=sys.stderr)
        print(f"Tip: Run 'activate_project.py --project-path . --language {language}' to configure", file=sys.stderr)
        raise
    
    try:
        # First find the symbol definition
        full_path = os.path.join(project_root, file)
        # Get document symbols to find the target
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
            return []
        
        # Find references
        range_info = target_sym.get("range") or {}
        start_info = range_info.get("start") or {}
        line = start_info.get("line")
        character = start_info.get("character")
        if line is None or character is None:
            return []
        references = ls.request_references(file, line, character)
        
        results = []
        for ref in references:
            ref_uri = ref.get("uri")
            ref_path = Path(ref_uri.replace("file://", "")).relative_to(project_root) if ref_uri else None
            ref_range = ref.get("range") or {}
            ref_start = ref_range.get("start") or {}
            ref_line = ref_start.get("line")
            
            # Get code snippet around reference
            snippet = ""
            if ref_path and ref_line is not None:
                ref_file_path = os.path.join(project_root, str(ref_path))
                if os.path.exists(ref_file_path):
                    with open(ref_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        start = max(0, ref_line - 1)
                        end = min(len(lines), ref_line + 2)
                        snippet = "".join(lines[start:end])
            
            results.append({
                "relative_path": str(ref_path) if ref_path else None,
                "line": ref_line,
                "snippet": snippet
            })
        
        return results
        
    finally:
        ls.stop()


def main():
    parser = argparse.ArgumentParser(description="Find references to a symbol")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--file", required=True, help="File containing the symbol")
    parser.add_argument("--symbol", required=True, help="Symbol name path")
    parser.add_argument("--language", default=None, help="Programming language (auto-detected if not specified)")
    parser.add_argument("--lsp-timeout", type=float, default=10.0, help="LSP analysis timeout in seconds (default: 10)")
    
    args = parser.parse_args()
    
    try:
        results = find_references(
            args.project_root,
            args.file,
            args.symbol,
            args.language,
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
