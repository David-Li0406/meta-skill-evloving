# Serena Skills - Setup Guide

Complete setup guide for getting started with Serena Skills standalone tools.

## Overview

Serena Skills provides standalone Python scripts for code intelligence operations without requiring the MCP server. These tools offer LSP-based symbol search, file operations, memory management, code editing, and shell execution capabilities.

**Important for AI Agents:** When using these scripts from a project root (e.g., when an AI agent is working within a project), scripts should be invoked with their full path from project root:

```bash
python .claude/skills/serena-skills/scripts/<category>/<script>.py --project-root . [other args]
```

For symbol search scripts that require the `lib` module, set `PYTHONPATH` appropriately:

```powershell
# Windows PowerShell
$env:PYTHONPATH = ".claude/skills/serena-skills"
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

```bash
# Linux/macOS/WSL
export PYTHONPATH=.claude/skills/serena-skills
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

## System Requirements

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Node.js**: (Optional) For TypeScript/JavaScript language server support
- **Operating System**: Windows, Linux, macOS, or WSL

## Installation

### Method 1: System-Wide Installation (Recommended)

Install all dependencies to your system Python environment for easy access across projects.

#### Windows (PowerShell)

```powershell
python -m pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions
```

#### Linux/macOS/WSL

```bash
python3 -m pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions
```

### Method 2: Virtual Environment (Isolated Environment)

Use a virtual environment to isolate dependencies from your system Python.

#### Windows (PowerShell)

```powershell
# Navigate to serena-skills directory
cd path\to\serena-skills

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions
```

#### Linux/macOS/WSL

```bash
# Navigate to serena-skills directory
cd path/to/serena-skills

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions
```

## Package Description

| Package | Purpose |
|---------|---------|
| **pathspec** | File pattern matching for ignore rules |
| **requests** | HTTP client (provides charset-normalizer as dependency) |
| **pyright** | Python language server for LSP-based operations |
| **joblib** | Parallel processing utilities |
| **pyyaml** | YAML configuration file parsing |
| **psutil** | Process and system utilities |
| **overrides** | Decorator for method overrides |
| **python-dotenv** | Environment variable management |
| **typing-extensions** | Backport of newer typing features |

## Language Server Installation (Optional)

For full language support beyond Python, install the appropriate language servers:

### TypeScript/JavaScript

```bash
npm install -g typescript typescript-language-server
```

### Go

```bash
go install golang.org/x/tools/gopls@latest
```

### Rust

Install via rustup:
```bash
rustup component add rust-analyzer
```

### Other Languages

See the [Serena documentation](https://github.com/freedmand/serena) for additional language servers.

## Verification

After installing dependencies, verify your setup in two steps:

### Step 1: Verify Environment Setup

Check that Python and all required packages are installed:

```bash
cd .claude/skills/serena-skills
python scripts/verify_setup.py
```

Expected output:
```
✓ Python version: 3.x.x
✓ pathspec installed
✓ requests installed
✓ pyright installed
... (all packages)
✓ lib directory found
✓ All checks passed
```

### Step 2: Verify Functionality

Test that all script categories work correctly:

```bash
cd .claude/skills/serena-skills
python scripts/verify_functionality.py
```

This will test:
- Project configuration scripts
- File operations (list, read, find, search)
- Symbol search (if Python files available in lib/)
- Memory management
- Code editing
- Workflow assistant
- Shell execution

Expected output:
```
✓ All functionality tests passed!
serena-skills is working correctly.
```

If any tests fail, check the error messages for troubleshooting guidance.

### Manual Verification

Test individual components:

#### 1. Check Dependencies

```bash
python -c "import pathspec, requests, pyright, joblib, yaml, psutil, overrides, dotenv, typing_extensions; print('✓ All dependencies available')"
```

#### 2. Test File Operations

```bash
python scripts/file-ops/list_dir.py --help
```

#### 3. Test Project Configuration

```bash
python scripts/project-config/get_config.py
```

## Quick Start

### 1. Activate Your Project

Register your project with serena-skills:

**From serena-skills directory:**
```bash
python scripts/project-config/activate_project.py --project-path /path/to/your/project
```

**From project root (recommended for AI agents):**
```bash
python .claude/skills/serena-skills/scripts/project-config/activate_project.py --project-path .
```

This creates a `.tmp/.serena-skills/` directory in your project with configuration files.

### 2. Explore Project Structure

List directory contents:

**From project root:**
```bash
python .claude/skills/serena-skills/scripts/file-ops/list_dir.py --project-root . --path src
```

Get symbols overview from a file:

**From project root (with PYTHONPATH):**

```powershell
# Windows PowerShell
$env:PYTHONPATH = ".claude/skills/serena-skills"
python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts
```

```bash
# Linux/macOS/WSL
export PYTHONPATH=.claude/skills/serena-skills
python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts
```

### 3. Use Memory Management

Store project knowledge:

**From project root:**
```bash
python .claude/skills/serena-skills/scripts/memory-manager/write_memory.py \
  --project-root . \
  --name "architecture-notes" \
  --content "Key components: API, Database, Frontend"
```

Retrieve stored knowledge:

```bash
python .claude/skills/serena-skills/scripts/memory-manager/read_memory.py \
  --project-root . \
  --name "architecture-notes"
```

### 4. Execute Shell Commands Safely

**From project root:**
```bash
python .claude/skills/serena-skills/scripts/shell-executor/execute_shell_command.py \
  --project-root . \
  --command "echo Hello World"
```

## Usage Patterns

### Running from Project Root (AI Agents)

When AI agents or users run scripts from the project root directory, use full paths:

**Basic file operations (no PYTHONPATH needed):**
```bash
python .claude/skills/serena-skills/scripts/file-ops/list_dir.py --project-root . --path src
python .claude/skills/serena-skills/scripts/file-ops/read_file.py --project-root . --file manifest.json
python .claude/skills/serena-skills/scripts/memory-manager/write_memory.py --project-root . --name "notes" --content "..."
```

**Symbol search tools (requires PYTHONPATH):**

```powershell
# Windows PowerShell - set once per session
$env:PYTHONPATH = ".claude/skills/serena-skills"
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

```bash
# Linux/macOS/WSL - set once per session
export PYTHONPATH=.claude/skills/serena-skills
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

### Working with Symbol Search Tools

Symbol search tools require the `lib` module to be importable. Use one of these approaches:

#### Approach 1: Set PYTHONPATH (Recommended for AI Agents)

**From project root - Windows PowerShell:**
```powershell
$env:PYTHONPATH = ".claude/skills/serena-skills"
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

**From project root - Linux/macOS/WSL:**
```bash
export PYTHONPATH=.claude/skills/serena-skills
python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
```

**From serena-skills directory:**

**Windows PowerShell:**
```powershell
cd path\to\serena-skills
$env:PYTHONPATH = "."
python scripts\symbol-search\find_symbol.py --project-root "..." --pattern "..."
```

**Linux/macOS:**
```bash
cd path/to/serena-skills
export PYTHONPATH=.
python scripts/symbol-search/find_symbol.py --project-root "..." --pattern "..."
```

#### Approach 2: Run from serena-skills Directory

Run from the serena-skills directory (PYTHONPATH not needed):

```bash
cd .claude/skills/serena-skills
python scripts/symbol-search/get_symbols_overview.py --project-root /absolute/path/to/project --file "src/main.ts"
```

Note: This approach is less suitable for AI agents operating from the project root.

### Common Workflows

#### Understanding a New Codebase

**From project root:**

1. Get project structure:
   ```bash
   python .claude/skills/serena-skills/scripts/file-ops/list_dir.py --project-root . --path . --recursive
   ```

2. Get file symbols (requires PYTHONPATH):
   ```powershell
   # Windows
   $env:PYTHONPATH = ".claude/skills/serena-skills"
   python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts
   ```
   
   ```bash
   # Linux/macOS
   export PYTHONPATH=.claude/skills/serena-skills
   python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts
   ```

3. Document findings:
   ```bash
   python scripts/memory-manager/write_memory.py \
     --project-root /path/to/project \
     --name "initial-analysis" \
     --content "Main entry point is src/main.py..."
   ```

#### Making Code Changes

1. Find target symbol:
   ```bash
   python scripts/symbol-search/find_symbol.py \
     --project-root /path/to/project \
     --pattern "MyClass/myMethod"
   ```

2. Check references:
   ```bash
   python scripts/symbol-search/find_referencing_symbols.py \
     --project-root /path/to/project \
     --file src/module.py \
     --line 42 \
     --column 10
   ```

3. Edit code:
   ```bash
   python scripts/code-editor/replace_content.py \
     --project-root /path/to/project \
     --file src/module.py \
     --old "old code" \
     --new "new code"
   ```

4. Run tests:
   ```bash
   python scripts/shell-executor/execute_shell_command.py \
     --project-root /path/to/project \
     --command "pytest tests/"
   ```

## Best Practices for AI Agents

When AI agents use serena-skills from a project root:

1. **Always use `--project-root .`** when running from project root

2. **Set PYTHONPATH once per session** for symbol search tools:
   ```powershell
   # Windows PowerShell
   $env:PYTHONPATH = ".claude/skills/serena-skills"
   ```
   
   ```bash
   # Linux/macOS/WSL
   export PYTHONPATH=.claude/skills/serena-skills
   ```

3. **Use full script paths** from project root:
   ```bash
   python .claude/skills/serena-skills/scripts/<category>/<script>.py
   ```

4. **File operations and memory management** don't require PYTHONPATH

5. **Symbol search and LSP-based tools** require PYTHONPATH to be set

## Troubleshooting

### Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'lib'`

**Solution:** This occurs when running symbol-search scripts. Set PYTHONPATH:

```bash
# Linux/macOS
export PYTHONPATH=/path/to/serena-skills

# Windows PowerShell
$env:PYTHONPATH = "C:\path\to\serena-skills"
```

### Missing Dependencies

**Error:** `ModuleNotFoundError: No module named 'requests'` (or other packages)

**Solution:** Install missing packages:

```bash
python -m pip install <package-name>
```

Or reinstall all dependencies:

```bash
python -m pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions
```

### Python Version Issues

**Error:** Type hints or syntax errors

**Solution:** Ensure you're using Python 3.8 or higher:

```bash
python --version
```

If you have multiple Python versions, use `python3` explicitly:

```bash
python3 --version
python3 -m pip install ...
```

### Language Server Not Found

**Error:** Pyright or other language server not working

**Solution:** Verify language server installation:

```bash
# For Python
pyright --version

# For TypeScript
typescript-language-server --version
```

If not installed, see [Language Server Installation](#language-server-installation-optional).

### Permission Issues (Linux/macOS)

**Error:** Permission denied when installing packages

**Solution:** Use `--user` flag:

```bash
python3 -m pip install --user <package-name>
```

Or use a virtual environment (Method 2).

## Project Structure

```
serena-skills/
├── SETUP.md                    # This file
├── SKILL.md                    # Main documentation and usage guide
├── lib/                        # Shared implementation libraries
│   ├── common/                # Common utilities
│   ├── serena_deps/           # Serena dependencies
│   └── solidlsp/              # LSP implementation
└── scripts/                    # Executable scripts
    ├── code-editor/           # Code editing operations
    ├── file-ops/              # File system operations
    ├── memory-manager/        # Project memory management
    ├── project-config/        # Project configuration
    ├── shell-executor/        # Shell command execution
    ├── symbol-search/         # LSP-based symbol operations
    └── workflow-assistant/    # Workflow automation helpers
```

## Data Storage

Serena Skills stores project-specific data in your project directory:

- **Project data:** `{project}/.tmp/.serena-skills/`
- **Memories:** `{project}/.tmp/.serena-skills/memories/`
- **Configuration:** `{project}/.tmp/.serena-skills/project.yml`

These directories are automatically created when you activate a project.

## Next Steps

1. **Read the main documentation:** See [SKILL.md](SKILL.md) for detailed usage patterns and API reference
2. **Explore script categories:** Review each script category's capabilities
3. **Try example workflows:** Follow the usage patterns for common tasks
4. **Integrate with your workflow:** Adapt scripts for your specific use cases

## Additional Resources

- **Main Documentation:** [SKILL.md](SKILL.md)
- **Serena Project:** [github.com/freedmand/serena](https://github.com/freedmand/serena)
- **LSP Specification:** [microsoft.github.io/language-server-protocol](https://microsoft.github.io/language-server-protocol/)

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [SKILL.md](SKILL.md) for usage examples
3. Verify your setup with `scripts/verify_setup.py`
4. Check the original Serena project documentation
