"""
Compatibility checker module for cross-platform command equivalents.
Provides platform-specific alternatives and compatibility warnings.
"""

from typing import Dict, List, Any, Optional, Tuple


class CompatibilityChecker:
    """Check cross-platform compatibility and suggest alternatives."""

    # Command equivalents database
    COMMAND_EQUIVALENTS = {
        # File operations
        "ls": {
            "linux": "ls -lah",
            "macos": "ls -lah",
            "windows_ps": "Get-ChildItem -Force",
            "windows_cmd": "dir /a",
            "compatibility": "full"
        },
        "cat": {
            "linux": "cat {file}",
            "macos": "cat {file}",
            "windows_ps": "Get-Content {file}",
            "windows_cmd": "type {file}",
            "compatibility": "full"
        },
        "grep": {
            "linux": "grep '{pattern}' {file}",
            "macos": "grep '{pattern}' {file}",
            "windows_ps": "Select-String -Pattern '{pattern}' -Path {file}",
            "windows_cmd": "findstr \"{pattern}\" {file}",
            "compatibility": "full"
        },
        "find": {
            "linux": "find {path} -name '{pattern}'",
            "macos": "find {path} -name '{pattern}'",
            "windows_ps": "Get-ChildItem -Path {path} -Filter '{pattern}' -Recurse",
            "windows_cmd": "dir {path}\\{pattern} /s /b",
            "compatibility": "full"
        },
        "cp": {
            "linux": "cp -r {source} {dest}",
            "macos": "cp -r {source} {dest}",
            "windows_ps": "Copy-Item -Path {source} -Destination {dest} -Recurse",
            "windows_cmd": "xcopy {source} {dest} /E /I",
            "compatibility": "full"
        },
        "mv": {
            "linux": "mv {source} {dest}",
            "macos": "mv {source} {dest}",
            "windows_ps": "Move-Item -Path {source} -Destination {dest}",
            "windows_cmd": "move {source} {dest}",
            "compatibility": "full"
        },
        "rm": {
            "linux": "rm -rf {path}",
            "macos": "rm -rf {path}",
            "windows_ps": "Remove-Item -Path {path} -Recurse -Force",
            "windows_cmd": "rd /s /q {path}",
            "compatibility": "full",
            "warning": "Dangerous operation - can cause data loss"
        },
        "mkdir": {
            "linux": "mkdir -p {path}",
            "macos": "mkdir -p {path}",
            "windows_ps": "New-Item -ItemType Directory -Path {path} -Force",
            "windows_cmd": "mkdir {path}",
            "compatibility": "full"
        },

        # System information
        "uname": {
            "linux": "uname -a",
            "macos": "uname -a",
            "windows_ps": "Get-ComputerInfo | Select-Object CsName, OsName, OsVersion",
            "windows_cmd": "systeminfo",
            "compatibility": "partial",
            "note": "Output format differs significantly between platforms"
        },
        "whoami": {
            "linux": "whoami",
            "macos": "whoami",
            "windows_ps": "$env:USERNAME",
            "windows_cmd": "echo %USERNAME%",
            "compatibility": "full"
        },
        "hostname": {
            "linux": "hostname",
            "macos": "hostname",
            "windows_ps": "$env:COMPUTERNAME",
            "windows_cmd": "hostname",
            "compatibility": "full"
        },

        # Process management
        "ps": {
            "linux": "ps aux",
            "macos": "ps aux",
            "windows_ps": "Get-Process",
            "windows_cmd": "tasklist",
            "compatibility": "partial",
            "note": "Output format and columns differ"
        },
        "kill": {
            "linux": "kill -9 {pid}",
            "macos": "kill -9 {pid}",
            "windows_ps": "Stop-Process -Id {pid} -Force",
            "windows_cmd": "taskkill /F /PID {pid}",
            "compatibility": "full"
        },

        # Network
        "ping": {
            "linux": "ping -c 4 {host}",
            "macos": "ping -c 4 {host}",
            "windows_ps": "Test-Connection -ComputerName {host} -Count 4",
            "windows_cmd": "ping -n 4 {host}",
            "compatibility": "full"
        },
        "curl": {
            "linux": "curl {url}",
            "macos": "curl {url}",
            "windows_ps": "Invoke-WebRequest -Uri {url}",
            "windows_cmd": "curl {url}",
            "compatibility": "full",
            "note": "Windows 10+ includes curl.exe"
        },
        "wget": {
            "linux": "wget {url}",
            "macos": "curl -O {url}",
            "windows_ps": "Invoke-WebRequest -Uri {url} -OutFile {filename}",
            "windows_cmd": "curl -O {url}",
            "compatibility": "partial",
            "note": "macOS doesn't include wget by default"
        },
        "netstat": {
            "linux": "netstat -tulpn",
            "macos": "netstat -an",
            "windows_ps": "Get-NetTCPConnection",
            "windows_cmd": "netstat -ano",
            "compatibility": "partial",
            "note": "Options and output format vary"
        },

        # Archive operations
        "tar": {
            "linux": "tar -czf {output}.tar.gz {input}",
            "macos": "tar -czf {output}.tar.gz {input}",
            "windows_ps": "Compress-Archive -Path {input} -DestinationPath {output}.zip",
            "windows_cmd": "tar -czf {output}.tar.gz {input}",
            "compatibility": "partial",
            "note": "PowerShell uses ZIP format, Windows 10+ includes tar"
        },
        "unzip": {
            "linux": "unzip {archive}",
            "macos": "unzip {archive}",
            "windows_ps": "Expand-Archive -Path {archive} -DestinationPath {dest}",
            "windows_cmd": "tar -xf {archive}",
            "compatibility": "full"
        },

        # Text processing
        "sed": {
            "linux": "sed 's/{pattern}/{replacement}/g' {file}",
            "macos": "sed 's/{pattern}/{replacement}/g' {file}",
            "windows_ps": "(Get-Content {file}) -replace '{pattern}', '{replacement}'",
            "windows_cmd": None,
            "compatibility": "limited",
            "note": "CMD has no direct equivalent, use PowerShell"
        },
        "awk": {
            "linux": "awk '{print $1}' {file}",
            "macos": "awk '{print $1}' {file}",
            "windows_ps": "Get-Content {file} | ForEach-Object {{$_.Split()[0]}}",
            "windows_cmd": None,
            "compatibility": "limited",
            "note": "Complex awk scripts may need significant rewrites in PowerShell"
        },

        # Package management
        "apt-get": {
            "linux": "apt-get install {package}",
            "macos": None,
            "windows_ps": None,
            "windows_cmd": None,
            "compatibility": "none",
            "alternatives": {
                "macos": "brew install {package}",
                "windows": "choco install {package} or winget install {package}"
            }
        },
        "yum": {
            "linux": "yum install {package}",
            "macos": None,
            "windows_ps": None,
            "windows_cmd": None,
            "compatibility": "none",
            "alternatives": {
                "macos": "brew install {package}",
                "windows": "choco install {package} or winget install {package}"
            }
        },
        "brew": {
            "linux": None,
            "macos": "brew install {package}",
            "windows_ps": None,
            "windows_cmd": None,
            "compatibility": "none",
            "alternatives": {
                "linux": "apt-get install {package} or yum install {package}",
                "windows": "choco install {package} or winget install {package}"
            }
        }
    }

    # Platform-specific features and limitations
    PLATFORM_FEATURES = {
        "linux": {
            "shell": "bash",
            "package_manager": ["apt", "yum", "dnf", "pacman"],
            "file_permissions": "full",
            "symbolic_links": True,
            "case_sensitive": True,
            "path_separator": "/"
        },
        "macos": {
            "shell": "bash/zsh",
            "package_manager": ["brew"],
            "file_permissions": "full",
            "symbolic_links": True,
            "case_sensitive": False,  # Default: case-insensitive
            "path_separator": "/"
        },
        "windows": {
            "shell": "cmd/powershell",
            "package_manager": ["choco", "winget"],
            "file_permissions": "ACL-based",
            "symbolic_links": "limited",  # Requires admin privileges
            "case_sensitive": False,
            "path_separator": "\\"
        }
    }

    def __init__(self):
        """Initialize compatibility checker."""
        self.compatibility_warnings = []

    def find_equivalent_commands(
        self,
        command: str,
        source_platform: str,
        target_platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Find equivalent commands for target platforms.

        Args:
            command: Command to find equivalents for
            source_platform: Source platform
            target_platforms: List of target platforms

        Returns:
            Dictionary of equivalent commands
        """
        # Extract base command (first word)
        base_command = command.split()[0]

        if base_command not in self.COMMAND_EQUIVALENTS:
            return {
                "command": command,
                "base_command": base_command,
                "equivalents": {},
                "compatibility": "unknown",
                "warning": f"No known equivalents for '{base_command}'"
            }

        equiv_data = self.COMMAND_EQUIVALENTS[base_command]
        result = {
            "command": command,
            "base_command": base_command,
            "source_platform": source_platform,
            "equivalents": {},
            "compatibility": equiv_data.get("compatibility", "unknown"),
            "warnings": []
        }

        # Get equivalents for target platforms
        for platform in target_platforms:
            if platform == "linux":
                result["equivalents"]["linux"] = equiv_data.get("linux")
            elif platform == "macos":
                result["equivalents"]["macos"] = equiv_data.get("macos")
            elif platform == "windows":
                result["equivalents"]["windows"] = {
                    "powershell": equiv_data.get("windows_ps"),
                    "cmd": equiv_data.get("windows_cmd")
                }

        # Add warnings and notes
        if "warning" in equiv_data:
            result["warnings"].append(equiv_data["warning"])

        if "note" in equiv_data:
            result["warnings"].append(equiv_data["note"])

        if equiv_data.get("compatibility") in ["partial", "limited", "none"]:
            result["warnings"].append(
                f"命令 '{base_command}' 在目标平台上的兼容性为: {equiv_data['compatibility']}"
            )

        if "alternatives" in equiv_data:
            result["alternatives"] = equiv_data["alternatives"]

        return result

    def check_platform_compatibility(
        self,
        features_required: List[str],
        target_platform: str
    ) -> Dict[str, Any]:
        """
        Check if platform supports required features.

        Args:
            features_required: List of required features
            target_platform: Target platform to check

        Returns:
            Compatibility result
        """
        if target_platform not in self.PLATFORM_FEATURES:
            return {
                "platform": target_platform,
                "supported": False,
                "error": f"Unknown platform: {target_platform}"
            }

        platform_features = self.PLATFORM_FEATURES[target_platform]
        result = {
            "platform": target_platform,
            "supported_features": [],
            "unsupported_features": [],
            "warnings": []
        }

        # Feature compatibility mapping
        feature_checks = {
            "symbolic_links": lambda: platform_features.get("symbolic_links", False),
            "case_sensitive": lambda: platform_features.get("case_sensitive", False),
            "full_permissions": lambda: platform_features.get("file_permissions") == "full"
        }

        for feature in features_required:
            if feature in feature_checks:
                if feature_checks[feature]():
                    result["supported_features"].append(feature)
                else:
                    result["unsupported_features"].append(feature)
                    result["warnings"].append(
                        f"平台 {target_platform} 不完全支持特性: {feature}"
                    )

        result["fully_compatible"] = len(result["unsupported_features"]) == 0

        return result

    def suggest_alternatives(
        self,
        command: str,
        issue: str,
        target_platform: str
    ) -> List[str]:
        """
        Suggest alternative approaches for incompatible commands.

        Args:
            command: Original command
            issue: Compatibility issue description
            target_platform: Target platform

        Returns:
            List of alternative suggestions
        """
        suggestions = []

        base_command = command.split()[0]

        # Check if command has alternatives
        if base_command in self.COMMAND_EQUIVALENTS:
            equiv_data = self.COMMAND_EQUIVALENTS[base_command]

            if "alternatives" in equiv_data and target_platform in equiv_data["alternatives"]:
                alt_cmd = equiv_data["alternatives"][target_platform]
                suggestions.append(f"使用替代命令: {alt_cmd}")

        # Platform-specific suggestions
        if target_platform == "windows":
            if base_command in ["sed", "awk", "grep"]:
                suggestions.append("考虑使用 PowerShell 的内置 cmdlet 替代 Unix 工具")
                suggestions.append("或安装 Git for Windows (包含 Unix 工具)")

            if "symbolic links" in issue.lower():
                suggestions.append("在 Windows 上创建符号链接需要管理员权限")
                suggestions.append("考虑使用硬链接或快捷方式")

        if target_platform in ["linux", "macos"]:
            if "package" in issue.lower():
                pm = self.PLATFORM_FEATURES[target_platform]["package_manager"]
                suggestions.append(f"使用平台包管理器: {', '.join(pm)}")

        if not suggestions:
            suggestions.append("考虑使用跨平台工具 (Python, Node.js) 实现相同功能")

        return suggestions

    def analyze_script_compatibility(
        self,
        script_commands: List[str],
        target_platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze entire script for cross-platform compatibility.

        Args:
            script_commands: List of commands in script
            target_platforms: Target platforms

        Returns:
            Comprehensive compatibility report
        """
        report = {
            "total_commands": len(script_commands),
            "platforms_analyzed": target_platforms,
            "compatibility_summary": {},
            "incompatible_commands": [],
            "warnings": [],
            "recommendations": []
        }

        for platform in target_platforms:
            report["compatibility_summary"][platform] = {
                "compatible": 0,
                "partial": 0,
                "incompatible": 0
            }

        # Analyze each command
        for cmd in script_commands:
            equiv_result = self.find_equivalent_commands(cmd, "linux", target_platforms)

            compatibility = equiv_result.get("compatibility", "unknown")

            for platform in target_platforms:
                if compatibility == "full":
                    report["compatibility_summary"][platform]["compatible"] += 1
                elif compatibility in ["partial", "limited"]:
                    report["compatibility_summary"][platform]["partial"] += 1
                else:
                    report["compatibility_summary"][platform]["incompatible"] += 1

                    report["incompatible_commands"].append({
                        "command": cmd,
                        "platform": platform,
                        "issue": f"兼容性: {compatibility}"
                    })

            if equiv_result.get("warnings"):
                report["warnings"].extend(equiv_result["warnings"])

        # Generate recommendations
        if report["incompatible_commands"]:
            report["recommendations"].append("发现不兼容命令,建议为每个平台创建单独脚本")

        if len(target_platforms) > 1:
            report["recommendations"].append("考虑使用跨平台工具 (Python/Node.js) 提高兼容性")

        return report


# Example usage
if __name__ == "__main__":
    checker = CompatibilityChecker()

    # Test command equivalents
    print("=== Command Equivalents Test ===")
    result = checker.find_equivalent_commands("ls -la", "linux", ["macos", "windows"])
    print(f"Command: ls -la")
    print(f"Equivalents: {result['equivalents']}")
    print(f"Compatibility: {result['compatibility']}")

    # Test platform features
    print("\n=== Platform Features Test ===")
    features_check = checker.check_platform_compatibility(
        ["symbolic_links", "case_sensitive"],
        "windows"
    )
    print(f"Windows supports symbolic links: {features_check}")

    # Test script compatibility
    print("\n=== Script Compatibility Test ===")
    test_script = ["ls -la", "grep 'error' log.txt", "tar -czf backup.tar.gz data/"]
    compat_report = checker.analyze_script_compatibility(test_script, ["linux", "macos", "windows"])
    print(f"Compatibility report: {compat_report['compatibility_summary']}")
