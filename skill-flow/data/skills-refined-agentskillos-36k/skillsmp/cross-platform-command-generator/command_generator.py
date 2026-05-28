"""
Cross-platform command generator module.
Converts natural language task descriptions into platform-specific commands.
"""

from typing import Dict, List, Any, Optional
import json
import re


class PlatformCommandGenerator:
    """Generate platform-specific commands from task descriptions."""

    # Command mapping database: common tasks to platform-specific commands
    COMMAND_PATTERNS = {
        "list_files": {
            "linux": "ls -lah",
            "macos": "ls -lah",
            "windows_ps": "Get-ChildItem -Force",
            "windows_cmd": "dir /a",
            "description": "List all files including hidden ones with details"
        },
        "find_files": {
            "linux": "find {path} -name '{pattern}'",
            "macos": "find {path} -name '{pattern}'",
            "windows_ps": "Get-ChildItem -Path {path} -Filter '{pattern}' -Recurse",
            "windows_cmd": "dir {path}\\{pattern} /s",
            "description": "Find files by name pattern"
        },
        "find_large_files": {
            "linux": "find {path} -type f -size +{size}M -exec ls -lh {{}} \\;",
            "macos": "find {path} -type f -size +{size}M -exec ls -lh {{}} \\;",
            "windows_ps": "Get-ChildItem -Path {path} -Recurse | Where-Object {{$_.Length -gt {size}MB}} | Select-Object FullName, @{{Name='Size(MB)';Expression={{[math]::Round($_.Length/1MB,2)}}}}",
            "windows_cmd": "forfiles /P {path} /S /M * /C \"cmd /c if @fsize GEQ {size_bytes} echo @path @fsize\"",
            "description": "Find files larger than specified size"
        },
        "check_disk_space": {
            "linux": "df -h",
            "macos": "df -h",
            "windows_ps": "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{{Name='Used(GB)';Expression={{[math]::Round($_.Used/1GB,2)}}}}, @{{Name='Free(GB)';Expression={{[math]::Round($_.Free/1GB,2)}}}}",
            "windows_cmd": "wmic logicaldisk get name,size,freespace",
            "description": "Check disk space usage"
        },
        "check_memory": {
            "linux": "free -h",
            "macos": "vm_stat",
            "windows_ps": "Get-CimInstance Win32_OperatingSystem | Select-Object @{{Name='FreePhysicalMemory(GB)';Expression={{[math]::Round($_.FreePhysicalMemory/1MB,2)}}}}, @{{Name='TotalVisibleMemory(GB)';Expression={{[math]::Round($_.TotalVisibleMemorySize/1MB,2)}}}}",
            "windows_cmd": "systeminfo | findstr /C:\"Total Physical Memory\" /C:\"Available Physical Memory\"",
            "description": "Check memory usage"
        },
        "check_processes": {
            "linux": "ps aux",
            "macos": "ps aux",
            "windows_ps": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 20",
            "windows_cmd": "tasklist",
            "description": "List running processes"
        },
        "check_network_ports": {
            "linux": "sudo netstat -tulpn",
            "macos": "sudo lsof -i -P -n | grep LISTEN",
            "windows_ps": "Get-NetTCPConnection | Where-Object {{$_.State -eq 'Listen'}} | Select-Object LocalAddress, LocalPort, OwningProcess, @{{Name='ProcessName';Expression={{(Get-Process -Id $_.OwningProcess).ProcessName}}}}",
            "windows_cmd": "netstat -ano | findstr LISTENING",
            "description": "Check listening network ports and processes"
        },
        "create_directory": {
            "linux": "mkdir -p {path}",
            "macos": "mkdir -p {path}",
            "windows_ps": "New-Item -ItemType Directory -Path {path} -Force",
            "windows_cmd": "mkdir {path}",
            "description": "Create directory (with parent directories if needed)"
        },
        "copy_files": {
            "linux": "cp -r {source} {destination}",
            "macos": "cp -r {source} {destination}",
            "windows_ps": "Copy-Item -Path {source} -Destination {destination} -Recurse",
            "windows_cmd": "xcopy {source} {destination} /E /I",
            "description": "Copy files and directories recursively"
        },
        "delete_files": {
            "linux": "rm -rf {path}",
            "macos": "rm -rf {path}",
            "windows_ps": "Remove-Item -Path {path} -Recurse -Force",
            "windows_cmd": "rd /s /q {path}",
            "description": "Delete files/directories recursively (DANGEROUS)"
        },
        "search_text_in_files": {
            "linux": "grep -r '{pattern}' {path}",
            "macos": "grep -r '{pattern}' {path}",
            "windows_ps": "Get-ChildItem -Path {path} -Recurse | Select-String -Pattern '{pattern}'",
            "windows_cmd": "findstr /s /i \"{pattern}\" {path}\\*",
            "description": "Search for text pattern in files"
        },
        "compress_files": {
            "linux": "tar -czf {output}.tar.gz {input}",
            "macos": "tar -czf {output}.tar.gz {input}",
            "windows_ps": "Compress-Archive -Path {input} -DestinationPath {output}.zip",
            "windows_cmd": "tar -czf {output}.tar.gz {input}",
            "description": "Compress files into archive"
        },
        "extract_archive": {
            "linux": "tar -xzf {archive}",
            "macos": "tar -xzf {archive}",
            "windows_ps": "Expand-Archive -Path {archive} -DestinationPath {destination}",
            "windows_cmd": "tar -xzf {archive}",
            "description": "Extract archive file"
        },
        "check_system_info": {
            "linux": "uname -a && lsb_release -a",
            "macos": "sw_vers && uname -a",
            "windows_ps": "Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, OsArchitecture",
            "windows_cmd": "systeminfo",
            "description": "Display system information"
        }
    }

    def __init__(self, task_description: str, platforms: List[str] = None):
        """
        Initialize command generator.

        Args:
            task_description: Natural language description of the task
            platforms: List of target platforms (linux, macos, windows)
        """
        self.task_description = task_description.lower()
        self.platforms = platforms or ["linux", "macos", "windows"]
        self.generated_commands = {}

    def analyze_task(self) -> Optional[str]:
        """
        Analyze task description and identify matching command pattern.

        Returns:
            Command pattern key if found, None otherwise
        """
        # Keyword matching for common tasks
        task_keywords = {
            "list_files": ["list files", "show files", "directory listing", "ls", "dir"],
            "find_files": ["find files", "search files", "locate files"],
            "find_large_files": ["large files", "big files", "files larger than", "files bigger than"],
            "check_disk_space": ["disk space", "disk usage", "free space", "df"],
            "check_memory": ["memory", "ram", "free memory"],
            "check_processes": ["processes", "running programs", "ps", "tasklist"],
            "check_network_ports": ["network ports", "listening ports", "open ports", "netstat"],
            "create_directory": ["create directory", "make directory", "mkdir", "new folder"],
            "copy_files": ["copy files", "copy directory", "cp", "xcopy"],
            "delete_files": ["delete files", "remove files", "rm", "del"],
            "search_text_in_files": ["search text", "grep", "find string", "search in files"],
            "compress_files": ["compress", "archive", "zip", "tar"],
            "extract_archive": ["extract", "unzip", "decompress", "untar"],
            "check_system_info": ["system info", "os info", "system information"]
        }

        for pattern_key, keywords in task_keywords.items():
            if any(keyword in self.task_description for keyword in keywords):
                return pattern_key

        return None

    def extract_parameters(self, pattern_key: str) -> Dict[str, str]:
        """
        Extract parameters from task description based on pattern.

        Args:
            pattern_key: Command pattern identifier

        Returns:
            Dictionary of extracted parameters
        """
        params = {}

        # Extract common parameters
        # File size (e.g., "100MB", "1GB")
        size_match = re.search(r'(\d+)\s*(mb|gb)', self.task_description, re.IGNORECASE)
        if size_match:
            size_value = int(size_match.group(1))
            size_unit = size_match.group(2).lower()
            params['size'] = size_value if size_unit == 'mb' else size_value * 1024
            params['size_bytes'] = params['size'] * 1024 * 1024

        # File path
        path_match = re.search(r'(?:in|from|at)\s+([^\s,]+)', self.task_description)
        if path_match:
            params['path'] = path_match.group(1)
        else:
            params['path'] = '.'  # Default to current directory

        # File pattern
        pattern_match = re.search(r'(?:named|pattern|matching)\s+["\']?([^\s"\']+)["\']?', self.task_description)
        if pattern_match:
            params['pattern'] = pattern_match.group(1)
        else:
            params['pattern'] = '*'

        # Source and destination for copy operations
        if 'from' in self.task_description and 'to' in self.task_description:
            parts = self.task_description.split('to')
            source_part = parts[0]
            dest_part = parts[1] if len(parts) > 1 else ''

            source_match = re.search(r'from\s+([^\s,]+)', source_part)
            dest_match = re.search(r'^\s*([^\s,]+)', dest_part)

            if source_match:
                params['source'] = source_match.group(1)
            if dest_match:
                params['destination'] = dest_match.group(1)

        return params

    def generate_commands(self) -> Dict[str, Any]:
        """
        Generate platform-specific commands based on task description.

        Returns:
            Dictionary with generated commands for each platform
        """
        pattern_key = self.analyze_task()

        if not pattern_key:
            return {
                "error": "Could not identify command pattern from task description",
                "task_description": self.task_description,
                "suggestion": "Please provide more specific task description or use keywords like 'list files', 'find files', 'check disk space', etc."
            }

        pattern = self.COMMAND_PATTERNS[pattern_key]
        params = self.extract_parameters(pattern_key)

        result = {
            "task_description": self.task_description,
            "identified_pattern": pattern_key,
            "description": pattern["description"],
            "platforms": {}
        }

        # Generate commands for each platform
        if "linux" in self.platforms:
            result["platforms"]["linux"] = {
                "command": self._format_command(pattern["linux"], params),
                "description": pattern["description"],
                "requires_sudo": "sudo" in pattern["linux"],
                "safety_level": self._assess_safety(pattern["linux"])
            }

        if "macos" in self.platforms:
            result["platforms"]["macos"] = {
                "command": self._format_command(pattern["macos"], params),
                "description": pattern["description"],
                "requires_sudo": "sudo" in pattern["macos"],
                "safety_level": self._assess_safety(pattern["macos"])
            }

        if "windows" in self.platforms:
            result["platforms"]["windows"] = {
                "powershell": self._format_command(pattern["windows_ps"], params),
                "cmd": self._format_command(pattern["windows_cmd"], params),
                "description": pattern["description"],
                "requires_admin": self._requires_admin(pattern["windows_ps"]),
                "safety_level": self._assess_safety(pattern["windows_ps"])
            }

        return result

    def _format_command(self, command_template: str, params: Dict[str, str]) -> str:
        """
        Format command template with extracted parameters.

        Args:
            command_template: Command template with placeholders
            params: Extracted parameters

        Returns:
            Formatted command string
        """
        try:
            return command_template.format(**params)
        except KeyError:
            # If parameter is missing, return template with available params
            for key, value in params.items():
                command_template = command_template.replace(f"{{{key}}}", str(value))
            return command_template

    def _assess_safety(self, command: str) -> str:
        """
        Assess safety level of command.

        Args:
            command: Command string to assess

        Returns:
            Safety level: 'safe', 'warning', or 'dangerous'
        """
        dangerous_patterns = [
            r'rm\s+-rf',
            r'del\s+/[fs]',
            r'format\s+',
            r'Remove-Item.*-Force',
            r'rd\s+/s\s+/q',
            r'mkfs\.',
            r'dd\s+if=',
            r'>\s*/dev/sd'
        ]

        warning_patterns = [
            r'sudo\s+',
            r'chmod\s+777',
            r'chown\s+',
            r'Set-ExecutionPolicy',
            r'reg\s+delete',
            r'sc\s+delete'
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return "dangerous"

        for pattern in warning_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return "warning"

        return "safe"

    def _requires_admin(self, command: str) -> bool:
        """
        Check if command requires administrator privileges.

        Args:
            command: Command string to check

        Returns:
            True if admin privileges required
        """
        admin_patterns = [
            r'Get-Service',
            r'Start-Service',
            r'Stop-Service',
            r'Set-ExecutionPolicy',
            r'New-Service',
            r'Install-Module'
        ]

        return any(re.search(pattern, command, re.IGNORECASE) for pattern in admin_patterns)


def cross_platform_translate(task: str, platforms: List[str] = None) -> Dict[str, Any]:
    """
    Convenience function to translate task description to platform-specific commands.

    Args:
        task: Natural language task description
        platforms: Target platforms (default: all platforms)

    Returns:
        Generated commands dictionary
    """
    generator = PlatformCommandGenerator(task, platforms)
    return generator.generate_commands()


# Example usage
if __name__ == "__main__":
    # Test examples
    test_tasks = [
        "List all files in the current directory",
        "Find all files larger than 100MB in /home/user",
        "Check disk space usage",
        "Search for text 'error' in all log files"
    ]

    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"Task: {task}")
        print(f"{'='*60}")
        result = cross_platform_translate(task)
        print(json.dumps(result, indent=2))
