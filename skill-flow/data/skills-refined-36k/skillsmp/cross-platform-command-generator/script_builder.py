"""
Script builder module for generating cross-platform scripts.
Creates complete script files with error handling, logging, and best practices.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ScriptBuilder:
    """Build cross-platform scripts with proper structure and error handling."""

    def __init__(self, script_name: str, description: str, author: str = "Claude"):
        """
        Initialize script builder.

        Args:
            script_name: Name of the script
            description: Description of script functionality
            author: Script author name
        """
        self.script_name = script_name
        self.description = description
        self.author = author
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_bash_script(
        self,
        functions: List[Dict[str, str]],
        main_logic: str,
        parameters: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate Bash script for Linux/macOS.

        Args:
            functions: List of function definitions (name, code, description)
            main_logic: Main script logic
            parameters: Script parameters/arguments

        Returns:
            Complete Bash script as string
        """
        script_parts = []

        # Shebang and header
        script_parts.append("#!/bin/bash")
        script_parts.append(f"""
################################################################################
# Script Name: {self.script_name}
# Description: {self.description}
# Author: {self.author}
# Created: {self.timestamp}
# Platform: Linux/macOS
################################################################################
""")

        # Error handling setup
        script_parts.append("""
# Enable strict error handling
set -euo pipefail
IFS=$'\\n\\t'

# Error handling function
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}
""")

        # Parameter parsing
        if parameters:
            script_parts.append("\n# Parameter definitions")
            for param in parameters:
                param_name = param.get("name", "")
                param_default = param.get("default", "")
                param_desc = param.get("description", "")

                script_parts.append(f"# {param_desc}")
                script_parts.append(f"{param_name}=\"{param_default}\"")

            script_parts.append("""
# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
        shift
    done
}

# Show help message
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

$description

Options:
    -h, --help    Show this help message

EOF
}
""")

        # User-defined functions
        if functions:
            script_parts.append("\n# User-defined functions")
            for func in functions:
                func_name = func.get("name", "")
                func_code = func.get("code", "")
                func_desc = func.get("description", "")

                script_parts.append(f"\n# {func_desc}")
                script_parts.append(f"{func_name}() {{")
                script_parts.append(f"    {func_code}")
                script_parts.append("}")

        # Prerequisite checks
        script_parts.append("""
# Check if script is run with required privileges
check_privileges() {
    if [[ $EUID -ne 0 ]] && [[ "$REQUIRE_ROOT" == "true" ]]; then
        error_exit "This script must be run as root (use sudo)"
    fi
}

# Check required commands exist
check_dependencies() {
    local missing_deps=()

    for cmd in "${REQUIRED_COMMANDS[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        error_exit "Missing required commands: ${missing_deps[*]}"
    fi
}
""")

        # Main execution
        script_parts.append(f"""
################################################################################
# Main Execution
################################################################################

main() {{
    log "Starting {self.script_name}..."

    # Prerequisite checks
    # check_privileges
    # check_dependencies

    # Parse arguments if provided
    # parse_arguments "$@"

    # Main logic
{self._indent_code(main_logic, 4)}

    log "{self.script_name} completed successfully"
}}

# Run main function
main "$@"
""")

        return "\n".join(script_parts)

    def generate_powershell_script(
        self,
        functions: List[Dict[str, str]],
        main_logic: str,
        parameters: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate PowerShell script for Windows.

        Args:
            functions: List of function definitions
            main_logic: Main script logic
            parameters: Script parameters

        Returns:
            Complete PowerShell script as string
        """
        script_parts = []

        # Header
        script_parts.append(f"""<#
.SYNOPSIS
    {self.script_name}

.DESCRIPTION
    {self.description}

.AUTHOR
    {self.author}

.CREATED
    {self.timestamp}

.PLATFORM
    Windows (PowerShell 5.1+)

.EXAMPLE
    .\\{self.script_name}.ps1
#>
""")

        # Error handling setup
        script_parts.append("""
# Enable strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Logging function
function Write-Log {
    param([string]$Message, [string]$Level = 'INFO')

    $Timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $LogMessage = "[$Timestamp] [$Level] $Message"

    switch ($Level) {
        'ERROR'   { Write-Error $LogMessage }
        'WARNING' { Write-Warning $LogMessage }
        default   { Write-Host $LogMessage }
    }
}

# Error handling function
function Exit-WithError {
    param([string]$Message)

    Write-Log -Message $Message -Level 'ERROR'
    exit 1
}
""")

        # Parameters
        if parameters:
            script_parts.append("\n# Script parameters")
            script_parts.append("param(")

            param_lines = []
            for param in parameters:
                param_name = param.get("name", "")
                param_type = param.get("type", "string")
                param_default = param.get("default", "")
                param_desc = param.get("description", "")

                param_line = f"    [Parameter()]\n    [{param_type}]${param_name}"
                if param_default:
                    param_line += f" = '{param_default}'"

                param_lines.append(param_line)

            script_parts.append(",\n\n".join(param_lines))
            script_parts.append(")\n")

        # User-defined functions
        if functions:
            script_parts.append("\n# User-defined functions")
            for func in functions:
                func_name = func.get("name", "")
                func_code = func.get("code", "")
                func_desc = func.get("description", "")

                script_parts.append(f"\n<# {func_desc} #>")
                script_parts.append(f"function {func_name} {{")
                script_parts.append(f"    {func_code}")
                script_parts.append("}\n")

        # Prerequisite checks
        script_parts.append("""
# Check if script is run with administrator privileges
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check required PowerShell modules
function Test-Dependencies {
    param([string[]]$RequiredModules)

    $missingModules = @()

    foreach ($module in $RequiredModules) {
        if (-not (Get-Module -ListAvailable -Name $module)) {
            $missingModules += $module
        }
    }

    if ($missingModules.Count -gt 0) {
        Exit-WithError "Missing required modules: $($missingModules -join ', ')"
    }
}
""")

        # Main execution
        script_parts.append(f"""
################################################################################
# Main Execution
################################################################################

try {{
    Write-Log "Starting {self.script_name}..."

    # Prerequisite checks
    # if (-not (Test-Administrator)) {{
    #     Exit-WithError "This script requires administrator privileges"
    # }}

    # Test-Dependencies -RequiredModules @('ModuleName1', 'ModuleName2')

    # Main logic
{self._indent_code(main_logic, 4)}

    Write-Log "{self.script_name} completed successfully"
    exit 0
}}
catch {{
    Write-Log "Script failed: $_" -Level 'ERROR'
    exit 1
}}
""")

        return "\n".join(script_parts)

    def generate_batch_script(
        self,
        commands: List[str],
        main_logic: str = None
    ) -> str:
        """
        Generate Windows batch script (.bat/.cmd).

        Args:
            commands: List of commands to execute
            main_logic: Optional main logic (if None, uses commands list)

        Returns:
            Complete batch script as string
        """
        script_parts = []

        # Header
        script_parts.append("@echo off")
        script_parts.append(f"""
REM ============================================================================
REM Script Name: {self.script_name}.bat
REM Description: {self.description}
REM Author: {self.author}
REM Created: {self.timestamp}
REM Platform: Windows
REM ============================================================================
""")

        # Error handling
        script_parts.append("""
setlocal enabledelayedexpansion

REM Error handling
set ERROR_CODE=0

:error_exit
echo ERROR: %1
exit /b 1

REM Logging function
:log
echo [%date% %time%] %1
goto :eof
""")

        # Main execution
        script_parts.append("\nREM Main execution")
        script_parts.append(f"call :log \"Starting {self.script_name}...\"")
        script_parts.append("")

        if main_logic:
            script_parts.append(main_logic)
        else:
            for cmd in commands:
                script_parts.append(cmd)
                script_parts.append("if errorlevel 1 call :error_exit \"Command failed: %errorlevel%\"")
                script_parts.append("")

        script_parts.append(f"call :log \"{self.script_name} completed successfully\"")
        script_parts.append("exit /b 0")

        return "\n".join(script_parts)

    def _indent_code(self, code: str, spaces: int) -> str:
        """
        Indent code block with specified number of spaces.

        Args:
            code: Code to indent
            spaces: Number of spaces for indentation

        Returns:
            Indented code
        """
        indent = " " * spaces
        lines = code.split("\n")
        return "\n".join(indent + line if line.strip() else "" for line in lines)

    def create_readme(self, usage_examples: List[str], requirements: List[str]) -> str:
        """
        Create README.md for the script package.

        Args:
            usage_examples: List of usage examples
            requirements: List of requirements/dependencies

        Returns:
            README.md content
        """
        readme_parts = []

        readme_parts.append(f"# {self.script_name}\n")
        readme_parts.append(f"{self.description}\n")
        readme_parts.append(f"**Author:** {self.author}")
        readme_parts.append(f"**Created:** {self.timestamp}\n")

        readme_parts.append("## Requirements\n")
        for req in requirements:
            readme_parts.append(f"- {req}")

        readme_parts.append("\n## Platform Support\n")
        readme_parts.append("- **Linux/Unix**: Use `.sh` script")
        readme_parts.append("- **macOS**: Use `.sh` script")
        readme_parts.append("- **Windows**: Use `.ps1` (PowerShell) or `.bat` (CMD) script\n")

        readme_parts.append("## Usage\n")
        readme_parts.append("### Linux/macOS\n")
        readme_parts.append("```bash")
        readme_parts.append(f"chmod +x {self.script_name}.sh")
        readme_parts.append(f"./{self.script_name}.sh")
        readme_parts.append("```\n")

        readme_parts.append("### Windows (PowerShell)\n")
        readme_parts.append("```powershell")
        readme_parts.append(f".\\{self.script_name}.ps1")
        readme_parts.append("```\n")

        readme_parts.append("### Windows (CMD)\n")
        readme_parts.append("```cmd")
        readme_parts.append(f"{self.script_name}.bat")
        readme_parts.append("```\n")

        if usage_examples:
            readme_parts.append("## Examples\n")
            for i, example in enumerate(usage_examples, 1):
                readme_parts.append(f"### Example {i}\n")
                readme_parts.append(f"```\n{example}\n```\n")

        readme_parts.append("## License\n")
        readme_parts.append("Generated by Claude Code - Cross-Platform Command Generator")

        return "\n".join(readme_parts)


# Example usage
if __name__ == "__main__":
    builder = ScriptBuilder(
        script_name="system_health_check",
        description="Check system health including CPU, memory, and disk usage"
    )

    # Define functions
    functions = [
        {
            "name": "check_disk_space",
            "code": "df -h | grep -v tmpfs",
            "description": "Check disk space usage"
        },
        {
            "name": "check_memory",
            "code": "free -h",
            "description": "Check memory usage"
        }
    ]

    # Main logic
    main_logic = """
    log "Checking system health..."
    check_disk_space
    check_memory
    """

    # Generate Bash script
    bash_script = builder.generate_bash_script(functions, main_logic)
    print("=== Bash Script ===")
    print(bash_script[:500])

    # Generate PowerShell script
    ps_script = builder.generate_powershell_script(functions, main_logic)
    print("\n=== PowerShell Script ===")
    print(ps_script[:500])
