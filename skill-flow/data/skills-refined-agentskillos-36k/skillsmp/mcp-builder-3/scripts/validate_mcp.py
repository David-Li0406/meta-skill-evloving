#!/usr/bin/env python3
"""
MCP Server Validator - Validates MCP server structure and best practices

Usage:
    validate_mcp.py <mcp-server-path>

Examples:
    validate_mcp.py ./my-mcp-server
    validate_mcp.py ./servers/weather-api
"""

import sys
import re
import json
from pathlib import Path


def validate_python_mcp(mcp_path):
    """Validate Python MCP server structure."""
    issues = []
    
    # Check for src directory
    src_dir = mcp_path / 'src'
    if not src_dir.exists():
        issues.append("Missing src/ directory")
        return issues
    
    # Check for server.py
    server_py = src_dir / 'server.py'
    if not server_py.exists():
        issues.append("Missing src/server.py")
    else:
        content = server_py.read_text()
        # Check for FastMCP import
        if 'from mcp.server.fastmcp import FastMCP' not in content and 'import fastmcp' not in content:
            issues.append("server.py should use FastMCP for Python MCP servers")
        # Check for tool decorator
        if '@mcp.tool' not in content:
            issues.append("server.py should define tools using @mcp.tool decorator")
    
    # Check for requirements.txt
    requirements = src_dir / 'requirements.txt'
    if not requirements.exists():
        issues.append("Missing src/requirements.txt")
    else:
        content = requirements.read_text()
        if 'mcp' not in content:
            issues.append("requirements.txt should include mcp dependency")
    
    # Check for README.md
    readme = mcp_path / 'README.md'
    if not readme.exists():
        issues.append("Missing README.md (recommended for documentation)")
    
    return issues


def validate_typescript_mcp(mcp_path):
    """Validate TypeScript MCP server structure."""
    issues = []
    
    # Check for src directory
    src_dir = mcp_path / 'src'
    if not src_dir.exists():
        issues.append("Missing src/ directory")
        return issues
    
    # Check for index.ts
    index_ts = src_dir / 'index.ts'
    if not index_ts.exists():
        issues.append("Missing src/index.ts")
    else:
        content = index_ts.read_text()
        # Check for MCP SDK import
        if '@modelcontextprotocol/sdk' not in content:
            issues.append("index.ts should import from @modelcontextprotocol/sdk")
        # Check for server setup
        if 'ListToolsRequestSchema' not in content:
            issues.append("index.ts should implement ListToolsRequestSchema")
        if 'CallToolRequestSchema' not in content:
            issues.append("index.ts should implement CallToolRequestSchema")
    
    # Check for package.json
    package_json = mcp_path / 'package.json'
    if not package_json.exists():
        issues.append("Missing package.json")
    else:
        try:
            data = json.loads(package_json.read_text())
            # Check for MCP SDK dependency
            deps = data.get('dependencies', {})
            if '@modelcontextprotocol/sdk' not in deps:
                issues.append("package.json should include @modelcontextprotocol/sdk in dependencies")
            # Check for build script
            scripts = data.get('scripts', {})
            if 'build' not in scripts:
                issues.append("package.json should include a 'build' script")
        except json.JSONDecodeError:
            issues.append("package.json contains invalid JSON")
    
    # Check for tsconfig.json
    tsconfig = mcp_path / 'tsconfig.json'
    if not tsconfig.exists():
        issues.append("Missing tsconfig.json")
    
    # Check for build output
    build_dir = mcp_path / 'build'
    if not build_dir.exists():
        issues.append("Missing build/ directory (run 'npm run build' to generate)")
    
    # Check for README.md
    readme = mcp_path / 'README.md'
    if not readme.exists():
        issues.append("Missing README.md (recommended for documentation)")
    
    return issues


def validate_mcp(mcp_path):
    """
    Validate an MCP server structure.

    Args:
        mcp_path: Path to the MCP server directory

    Returns:
        (is_valid, message, issues) tuple
    """
    mcp_path = Path(mcp_path).resolve()
    
    if not mcp_path.exists():
        return False, "Directory not found", []
    
    if not mcp_path.is_dir():
        return False, "Path is not a directory", []
    
    # Determine if Python or TypeScript project
    has_package_json = (mcp_path / 'package.json').exists()
    has_requirements = (mcp_path / 'src' / 'requirements.txt').exists() or (mcp_path / 'requirements.txt').exists()
    has_server_py = (mcp_path / 'src' / 'server.py').exists() or (mcp_path / 'server.py').exists()
    has_index_ts = (mcp_path / 'src' / 'index.ts').exists() or (mcp_path / 'index.ts').exists()
    
    if not has_package_json and not has_requirements and not has_server_py and not has_index_ts:
        return False, "Not recognized as an MCP server project", []
    
    issues = []
    
    if has_package_json or has_index_ts:
        issues = validate_typescript_mcp(mcp_path)
        lang = "TypeScript"
    elif has_requirements or has_server_py:
        issues = validate_python_mcp(mcp_path)
        lang = "Python"
    else:
        return False, "Could not determine project type", []
    
    if issues:
        return False, f"{lang} MCP server has validation issues", issues
    else:
        return True, f"{lang} MCP server is valid!", []


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_mcp.py <mcp-server-path>")
        print("\nValidates MCP server structure and best practices.")
        print("\nExamples:")
        print("  validate_mcp.py ./my-mcp-server")
        print("  validate_mcp.py ./servers/weather-api")
        sys.exit(1)
    
    mcp_path = sys.argv[1]
    
    valid, message, issues = validate_mcp(mcp_path)
    
    print(f"🔍 Validating: {mcp_path}")
    print()
    
    if valid:
        print(f"✅ {message}")
        return 0
    else:
        print(f"❌ {message}")
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  • {issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
