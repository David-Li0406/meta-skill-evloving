#!/usr/bin/env python3
"""
MCP Server Packager - Creates a distributable package for an MCP server

Usage:
    package_mcp.py <mcp-server-path> [output-directory]

Examples:
    package_mcp.py ./my-mcp-server
    package_mcp.py ./servers/weather-api ./dist
"""

import sys
import shutil
import zipfile
from pathlib import Path
from validate_mcp import validate_mcp


def package_python_mcp(mcp_path, output_path):
    """Package a Python MCP server."""
    issues = []
    
    # Build the project (create distribution)
    src_dir = mcp_path / 'src'
    if not src_dir.exists():
        return False, "Missing src/ directory"
    
    # Create a portable package structure
    package_name = mcp_path.name
    
    # Create zip with portable structure
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add source files
        if src_dir.exists():
            for file_path in src_dir.rglob('*'):
                if file_path.is_file():
                    arcname = f"{package_name}/src/{file_path.relative_to(src_dir)}"
                    zipf.write(file_path, arcname)
        
        # Add README
        readme = mcp_path / 'README.md'
        if readme.exists():
            zipf.write(readme, f"{package_name}/README.md")
        
        # Add reference docs if they exist
        ref_dir = mcp_path / 'reference'
        if ref_dir.exists():
            for file_path in ref_dir.glob('*.md'):
                zipf.write(file_path, f"{package_name}/reference/{file_path.name}")
        
        # Add installation script
        install_script = f"""#!/bin/bash
# Installation script for {package_name}

echo "Installing {package_name}..."

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r src/requirements.txt

echo "✅ {package_name} installed successfully!"
echo ""
echo "To run the server:"
echo "  python src/server.py"
echo ""
echo "Or with MCP Inspector:"
echo "  npx @modelcontextprotocol/inspector python src/server.py"
"""
        zipf.writestr(f"{package_name}/install.sh", install_script)
    
    return True, None


def package_typescript_mcp(mcp_path, output_path):
    """Package a TypeScript MCP server."""
    package_name = mcp_path.name
    
    # Check if build exists
    build_dir = mcp_path / 'build'
    if not build_dir.exists():
        return False, "Missing build/ directory. Run 'npm run build' first"
    
    # Create zip with portable structure
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add build output
        for file_path in build_dir.rglob('*'):
            if file_path.is_file():
                arcname = f"{package_name}/build/{file_path.relative_to(build_dir)}"
                zipf.write(file_path, arcname)
        
        # Add package.json
        package_json = mcp_path / 'package.json'
        if package_json.exists():
            zipf.write(package_json, f"{package_name}/package.json")
        
        # Add README
        readme = mcp_path / 'README.md'
        if readme.exists():
            zipf.write(readme, f"{package_name}/README.md")
        
        # Add reference docs if they exist
        ref_dir = mcp_path / 'reference'
        if ref_dir.exists():
            for file_path in ref_dir.glob('*.md'):
                zipf.write(file_path, f"{package_name}/reference/{file_path.name}")
        
        # Add installation script
        install_script = f"""#!/bin/bash
# Installation script for {package_name}

echo "Installing {package_name}..."

# Install dependencies
npm install

echo "✅ {package_name} installed successfully!"
echo ""
echo "To run the server:"
echo "  npm run server"
echo ""
echo "Or with MCP Inspector:"
echo "  npx @modelcontextprotocol/inspector npm run server"
"""
        zipf.writestr(f"{package_name}/install.sh", install_script)
    
    return True, None


def package_mcp(mcp_path, output_dir=None):
    """
    Package an MCP server for distribution.

    Args:
        mcp_path: Path to the MCP server directory
        output_dir: Optional output directory (defaults to current directory)

    Returns:
        Path to the created package file, or None if error
    """
    mcp_path = Path(mcp_path).resolve()
    
    # Validate MCP server exists
    if not mcp_path.exists():
        print(f"❌ Error: MCP server directory not found: {mcp_path}")
        return None
    
    if not mcp_path.is_dir():
        print(f"❌ Error: Path is not a directory: {mcp_path}")
        return None
    
    # Run validation before packaging
    print("🔍 Validating MCP server...")
    valid, message, issues = validate_mcp(mcp_path)
    
    if not valid:
        print(f"❌ Validation failed: {message}")
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  • {issue}")
        print("\nPlease fix the validation errors before packaging.")
        return None
    
    print(f"✅ {message}\n")
    
    # Determine output location
    server_name = mcp_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    
    package_filename = output_path / f"{server_name}.zip"
    
    # Determine type and package
    has_package_json = (mcp_path / 'package.json').exists()
    
    try:
        if has_package_json:
            success, error = package_typescript_mcp(mcp_path, package_filename)
            lang = "TypeScript"
        else:
            success, error = package_python_mcp(mcp_path, package_filename)
            lang = "Python"
        
        if not success:
            print(f"❌ Error: {error}")
            return None
        
        print(f"✅ Successfully packaged {lang} MCP server to: {package_filename}")
        print(f"\n📦 Package contents:")
        
        # List package contents
        with zipfile.ZipFile(package_filename, 'r') as zipf:
            for name in zipf.namelist()[:10]:  # Show first 10 files
                print(f"  - {name}")
            if len(zipf.namelist()) > 10:
                print(f"  ... and {len(zipf.namelist()) - 10} more files")
        
        print(f"\n🚀 To install and use:")
        print(f"  1. Unzip: unzip {server_name}.zip")
        print(f"  2. cd {server_name}")
        print(f"  3. bash install.sh")
        
        return package_filename
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: package_mcp.py <mcp-server-path> [output-directory]")
        print("\nPackages an MCP server for distribution.")
        print("\nExamples:")
        print("  package_mcp.py ./my-mcp-server")
        print("  package_mcp.py ./servers/weather-api ./dist")
        sys.exit(1)
    
    mcp_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"📦 Packaging MCP server: {mcp_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()
    
    result = package_mcp(mcp_path, output_dir)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
