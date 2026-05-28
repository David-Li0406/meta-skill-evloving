#!/usr/bin/env python3
"""
Claude Code Settings Optimizer

Enhanced settings analyzer with sandbox-aware WebFetch migration.
Identifies dangerous patterns, overly specific approvals, redundant entries,
and suggests migrating WebFetch domains to sandbox network allowlists.
"""

import json
import argparse
import shutil
import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = ""
    class Style:
        BRIGHT = RESET_ALL = ""
    HAS_COLOR = False


class IssueType(Enum):
    """Types of permission issues"""
    DANGEROUS = "dangerous"
    SPECIFIC = "specific"
    REDUNDANT = "redundant"
    MIGRATE_TO_SANDBOX = "migrate_to_sandbox"
    GOOD = "good"


@dataclass
class Permission:
    """Represents a single permission entry"""
    pattern: str
    location: str  # "Global" or "Project"

    def __hash__(self):
        return hash((self.pattern, self.location))

    def __eq__(self, other):
        return self.pattern == other.pattern and self.location == other.location


@dataclass
class Issue:
    """Represents a permission issue"""
    permission: Permission
    issue_type: IssueType
    reason: str
    suggestion: Optional[str] = None
    covered_by: Optional[Permission] = None
    migrate_domain: Optional[str] = None  # Domain to migrate to sandbox


class SettingsOptimizer:
    """Analyzes and optimizes Claude Code permission settings"""

    DANGEROUS_PATTERNS = {
        "Bash(*:*)",
        "Read(/*)",
        "Write(/*)",
        "Edit(/*)",
        "Bash(rm:*)",
        "Bash(sudo:*)",
        "Skill(*)",
    }

    def __init__(self, global_path: Optional[Path] = None, project_path: Optional[Path] = None):
        """Initialize with custom paths or use defaults"""
        self.global_path = global_path or Path.home() / ".claude" / "settings.json"
        self.project_path = project_path or Path.cwd() / ".claude" / "settings.local.json"

        self.global_permissions: Set[str] = set()
        self.project_permissions: Set[str] = set()
        self.project_sandbox_network_allow: Set[str] = set()
        self.issues: List[Issue] = []

    def load_settings(self) -> bool:
        """Load settings from both global and project files"""
        try:
            if self.global_path.exists():
                with open(self.global_path, 'r') as f:
                    global_data = json.load(f)
                    self.global_permissions = set(
                        global_data.get("permissions", {}).get("allow", [])
                    )

            if self.project_path.exists():
                with open(self.project_path, 'r') as f:
                    project_data = json.load(f)
                    self.project_permissions = set(
                        project_data.get("permissions", {}).get("allow", [])
                    )
                    # Load sandbox network allowlist
                    sandbox = project_data.get("sandbox", {})
                    network_perms = sandbox.get("permissions", {}).get("network", {})
                    self.project_sandbox_network_allow = set(network_perms.get("allow", []))

            if not self.global_permissions and not self.project_permissions:
                print(f"{Fore.YELLOW}No permissions found in settings files.{Style.RESET_ALL}")
                return False

            return True

        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Error: Invalid JSON in settings file: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}Error loading settings: {e}{Style.RESET_ALL}")
            return False

    def is_dangerous(self, pattern: str) -> bool:
        """Check if pattern is in the dangerous list"""
        return pattern in self.DANGEROUS_PATTERNS

    def is_overly_specific(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """Check if pattern is overly specific (exact command with arguments)"""
        if not pattern.startswith("Bash("):
            return False, None

        if not pattern.endswith(")"):
            return False, None

        args = pattern[5:-1]

        if ":*" in args or args == "*:*":
            return False, None

        if " " in args:
            base_cmd = args.split()[0]
            suggestion = f"Bash({base_cmd}:*)"
            return True, suggestion

        return False, None

    def extract_webfetch_domain(self, pattern: str) -> Optional[str]:
        """Extract domain from WebFetch(domain:X) pattern"""
        match = re.match(r'^WebFetch\(domain:([^)]+)\)$', pattern)
        return match.group(1) if match else None

    def is_pattern_subset(self, specific: str, general: str) -> bool:
        """Check if 'specific' pattern is covered by 'general' pattern"""
        spec_tool = specific.split('(')[0] if '(' in specific else specific
        gen_tool = general.split('(')[0] if '(' in general else general

        if spec_tool != gen_tool:
            return False

        # If general tool has no restrictions, it covers ALL variants
        if '(' not in general:
            return True

        if '(' not in specific:
            return False

        spec_args = specific[specific.index('(')+1:-1] if specific.endswith(')') else ""
        gen_args = general[general.index('(')+1:-1] if general.endswith(')') else ""

        if spec_args == gen_args:
            return True

        if gen_args == "*:*":
            return True

        if gen_args == "domain:*" and spec_args.startswith("domain:"):
            return True

        if gen_args.endswith(":*"):
            base_cmd = gen_args[:-2]
            if spec_args.startswith(base_cmd):
                if spec_args == base_cmd or spec_args.startswith(base_cmd + " ") or spec_args.startswith(base_cmd + ":"):
                    return True

        if spec_tool in ["Read", "Write", "Edit"]:
            if gen_args == "/*":
                return True
            if gen_args.endswith("*") and spec_args.startswith(gen_args[:-1]):
                return True

        return False

    def is_redundant(self, perm: Permission) -> Optional[Permission]:
        """Check if a project permission is redundant (covered by global permission)"""
        if perm.location != "Project":
            return None

        for global_perm in self.global_permissions:
            if self.is_pattern_subset(perm.pattern, global_perm):
                return Permission(global_perm, "Global")

        return None

    def should_migrate_to_sandbox(self, perm: Permission) -> Optional[str]:
        """
        Check if permission should be migrated to sandbox network allowlist.

        Returns domain if:
        1. Project-level WebFetch with specific domain
        2. Covered by global permission (would be REDUNDANT)
        3. Domain NOT already in sandbox.permissions.network.allow
        """
        if perm.location != "Project":
            return None

        domain = self.extract_webfetch_domain(perm.pattern)
        if not domain:
            return None

        # Check if covered by global (would be redundant)
        covered = False
        for global_perm in self.global_permissions:
            if self.is_pattern_subset(perm.pattern, global_perm):
                covered = True
                break

        if not covered:
            return None

        # Check if already in sandbox allowlist
        if domain in self.project_sandbox_network_allow:
            return None

        return domain

    def detect_self_awareness(self) -> Dict:
        """Detect if this skill is in the permissions"""
        skill_patterns = [
            "Skill(claude-settings-optimizer)",
            "Skill(settings-cleaner)",
            "Skill(*)",
        ]

        found_global = []
        found_project = []

        for pattern in skill_patterns:
            if pattern in self.global_permissions:
                found_global.append(pattern)
            if pattern in self.project_permissions:
                found_project.append(pattern)

        return {
            "is_self_aware": bool(found_global or found_project),
            "global_patterns": found_global,
            "project_patterns": found_project,
        }

    def analyze(self) -> Dict[IssueType, List[Issue]]:
        """Analyze all permissions and categorize issues"""
        self.issues = []

        # Analyze global permissions
        for pattern in self.global_permissions:
            perm = Permission(pattern, "Global")

            if self.is_dangerous(pattern):
                self.issues.append(Issue(
                    perm, IssueType.DANGEROUS,
                    "Allows unrestricted access"
                ))
            else:
                is_specific, suggestion = self.is_overly_specific(pattern)
                if is_specific:
                    self.issues.append(Issue(
                        perm, IssueType.SPECIFIC,
                        "Hardcoded arguments should be generalized",
                        suggestion=suggestion
                    ))
                else:
                    self.issues.append(Issue(perm, IssueType.GOOD, ""))

        # Analyze project permissions
        for pattern in self.project_permissions:
            perm = Permission(pattern, "Project")

            if self.is_dangerous(pattern):
                self.issues.append(Issue(
                    perm, IssueType.DANGEROUS,
                    "Allows unrestricted access"
                ))
                continue

            # Check for sandbox migration first (more specific than redundant)
            migrate_domain = self.should_migrate_to_sandbox(perm)
            if migrate_domain:
                covered_by = self.is_redundant(perm)
                self.issues.append(Issue(
                    perm, IssueType.MIGRATE_TO_SANDBOX,
                    "Redundant for WebFetch but needed for Bash network access",
                    covered_by=covered_by,
                    migrate_domain=migrate_domain
                ))
                continue

            # Check redundancy
            covered_by = self.is_redundant(perm)
            if covered_by:
                self.issues.append(Issue(
                    perm, IssueType.REDUNDANT,
                    "Covered by global permission",
                    covered_by=covered_by
                ))
                continue

            # Check overly specific
            is_specific, suggestion = self.is_overly_specific(pattern)
            if is_specific:
                self.issues.append(Issue(
                    perm, IssueType.SPECIFIC,
                    "Hardcoded arguments should be generalized",
                    suggestion=suggestion
                ))
            else:
                self.issues.append(Issue(perm, IssueType.GOOD, ""))

        # Group by issue type
        grouped = {
            IssueType.DANGEROUS: [],
            IssueType.SPECIFIC: [],
            IssueType.REDUNDANT: [],
            IssueType.MIGRATE_TO_SANDBOX: [],
            IssueType.GOOD: []
        }

        for issue in self.issues:
            grouped[issue.issue_type].append(issue)

        return grouped

    def print_report(self, grouped: Dict[IssueType, List[Issue]]):
        """Print a formatted report of all issues"""
        print(f"\n{Style.BRIGHT}=== Claude Code Settings Analysis ==={Style.RESET_ALL}\n")

        self._print_context()

        # Dangerous patterns
        dangerous = grouped[IssueType.DANGEROUS]
        if dangerous:
            print(f"{Fore.RED}{Style.BRIGHT}DANGEROUS ({len(dangerous)} found):{Style.RESET_ALL}")
            for issue in dangerous:
                print(f"  - {issue.permission.pattern} [{issue.permission.location}]")
                print(f"    Risk: {issue.reason}")
            print()

        # Migrate to sandbox
        migrate = grouped[IssueType.MIGRATE_TO_SANDBOX]
        if migrate:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}MIGRATE_TO_SANDBOX ({len(migrate)} found):{Style.RESET_ALL}")
            for issue in migrate:
                print(f"  - {issue.permission.pattern} [{issue.permission.location}]")
                if issue.covered_by:
                    print(f"    Covered by: {issue.covered_by.pattern} [{issue.covered_by.location}]")
                print(f"    -> Migrate '{issue.migrate_domain}' to sandbox.permissions.network.allow")
            print()

        # Overly specific patterns
        specific = grouped[IssueType.SPECIFIC]
        if specific:
            print(f"{Fore.YELLOW}{Style.BRIGHT}OVERLY SPECIFIC ({len(specific)} found):{Style.RESET_ALL}")
            for issue in specific:
                print(f"  - {issue.permission.pattern} [{issue.permission.location}]")
                if issue.suggestion:
                    print(f"    -> Suggest: {issue.suggestion}")
            print()

        # Redundant permissions
        redundant = grouped[IssueType.REDUNDANT]
        if redundant:
            print(f"{Fore.BLUE}{Style.BRIGHT}REDUNDANT ({len(redundant)} found):{Style.RESET_ALL}")
            for issue in redundant:
                print(f"  - {issue.permission.pattern} [{issue.permission.location}]")
                if issue.covered_by:
                    print(f"    Covered by: {issue.covered_by.pattern} [{issue.covered_by.location}]")
            print()

        # Good permissions
        good = grouped[IssueType.GOOD]
        if good:
            print(f"{Fore.GREEN}{Style.BRIGHT}GOOD ({len(good)} permissions){Style.RESET_ALL}")
            print()

        # Summary
        total_issues = len(dangerous) + len(specific) + len(redundant) + len(migrate)
        if total_issues == 0:
            print(f"{Fore.GREEN}No issues found! Your permissions are well-configured.{Style.RESET_ALL}\n")
        else:
            print(f"{Style.BRIGHT}Total issues: {total_issues}{Style.RESET_ALL}\n")

    def _print_context(self):
        """Print contextual information about the analysis"""
        self_aware = self.detect_self_awareness()

        print(f"{Fore.CYAN}{Style.BRIGHT}CONTEXT:{Style.RESET_ALL}")
        print(f"  Global settings: {self.global_path}")
        print(f"  Project settings: {self.project_path}")

        if self.project_sandbox_network_allow:
            print(f"  Sandbox network allowlist: {sorted(self.project_sandbox_network_allow)}")

        if self_aware["is_self_aware"]:
            print(f"\n  {Fore.YELLOW}Self-awareness detected:{Style.RESET_ALL}")
            for pattern in self_aware["global_patterns"]:
                print(f"    - {pattern} [Global]")
            for pattern in self_aware["project_patterns"]:
                print(f"    - {pattern} [Project]")

            if "Skill(*)" in self_aware["global_patterns"] or "Skill(*)" in self_aware["project_patterns"]:
                print(f"    {Fore.RED}Skill(*) grants unrestricted access to all skills.{Style.RESET_ALL}")

        print()

    def create_backup(self, filepath: Path) -> bool:
        """Create a backup of the settings file"""
        if not filepath.exists():
            return True

        backup_path = filepath.with_suffix(filepath.suffix + ".bak")
        try:
            shutil.copy2(filepath, backup_path)
            print(f"{Fore.CYAN}Creating backup: {backup_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Error creating backup: {e}{Style.RESET_ALL}")
            return False

    def save_settings(self, global_perms: Set[str], project_perms: Set[str],
                      sandbox_network_allow: Optional[Set[str]] = None) -> bool:
        """Save updated permissions back to files"""
        try:
            # Save global settings
            if self.global_path.exists():
                with open(self.global_path, 'r') as f:
                    global_data = json.load(f)

                if "permissions" not in global_data:
                    global_data["permissions"] = {}
                global_data["permissions"]["allow"] = sorted(list(global_perms))

                with open(self.global_path, 'w') as f:
                    json.dump(global_data, f, indent=2)
                    f.write('\n')

            # Save project settings
            if self.project_path.exists():
                with open(self.project_path, 'r') as f:
                    project_data = json.load(f)

                if "permissions" not in project_data:
                    project_data["permissions"] = {}
                project_data["permissions"]["allow"] = sorted(list(project_perms))

                # Update sandbox network allowlist if provided
                if sandbox_network_allow is not None:
                    if "sandbox" not in project_data:
                        project_data["sandbox"] = {}
                    if "permissions" not in project_data["sandbox"]:
                        project_data["sandbox"]["permissions"] = {}
                    if "network" not in project_data["sandbox"]["permissions"]:
                        project_data["sandbox"]["permissions"]["network"] = {}
                    project_data["sandbox"]["permissions"]["network"]["allow"] = sorted(list(sandbox_network_allow))

                with open(self.project_path, 'w') as f:
                    json.dump(project_data, f, indent=2)
                    f.write('\n')

            return True

        except Exception as e:
            print(f"{Fore.RED}Error saving settings: {e}{Style.RESET_ALL}")
            return False

    def interactive_clean(self, grouped: Dict[IssueType, List[Issue]]):
        """Interactive cleanup with user confirmation for each issue"""
        global_perms = self.global_permissions.copy()
        project_perms = self.project_permissions.copy()
        sandbox_network = self.project_sandbox_network_allow.copy()

        changes = {
            "dangerous_removed": 0,
            "specific_generalized": 0,
            "redundant_removed": 0,
            "migrated_to_sandbox": 0
        }

        # Handle dangerous patterns
        dangerous = grouped[IssueType.DANGEROUS]
        if dangerous:
            print(f"\n{Fore.RED}{Style.BRIGHT}DANGEROUS PATTERNS:{Style.RESET_ALL}")
            for issue in dangerous:
                print(f"\n  {issue.permission.pattern} [{issue.permission.location}]")
                print(f"  Risk: {issue.reason}")

                response = input(f"  Remove? [y/N]: ").strip().lower()
                if response == 'y':
                    if issue.permission.location == "Global":
                        global_perms.discard(issue.permission.pattern)
                    else:
                        project_perms.discard(issue.permission.pattern)
                    changes["dangerous_removed"] += 1

        # Handle migrate to sandbox
        migrate = grouped[IssueType.MIGRATE_TO_SANDBOX]
        if migrate:
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}MIGRATE TO SANDBOX:{Style.RESET_ALL}")
            for issue in migrate:
                print(f"\n  {issue.permission.pattern} [{issue.permission.location}]")
                print(f"  Covered by: {issue.covered_by.pattern} [{issue.covered_by.location}]")
                print(f"  -> Migrate '{issue.migrate_domain}' to sandbox.permissions.network.allow")

                response = input(f"  Migrate? [Y/n]: ").strip().lower()
                if response != 'n':
                    project_perms.discard(issue.permission.pattern)
                    sandbox_network.add(issue.migrate_domain)
                    changes["migrated_to_sandbox"] += 1

        # Handle overly specific patterns
        specific = grouped[IssueType.SPECIFIC]
        if specific:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}OVERLY SPECIFIC PATTERNS:{Style.RESET_ALL}")
            for issue in specific:
                print(f"\n  {issue.permission.pattern} [{issue.permission.location}]")
                print(f"  -> Suggest: {issue.suggestion}")

                response = input(f"  Generalize? [y/N]: ").strip().lower()
                if response == 'y':
                    if issue.permission.location == "Global":
                        global_perms.discard(issue.permission.pattern)
                        global_perms.add(issue.suggestion)
                    else:
                        project_perms.discard(issue.permission.pattern)
                        project_perms.add(issue.suggestion)
                    changes["specific_generalized"] += 1

        # Handle redundant permissions
        redundant = grouped[IssueType.REDUNDANT]
        if redundant:
            print(f"\n{Fore.BLUE}{Style.BRIGHT}REDUNDANT PERMISSIONS:{Style.RESET_ALL}")
            for issue in redundant:
                print(f"\n  {issue.permission.pattern} [{issue.permission.location}]")
                print(f"  Covered by: {issue.covered_by.pattern} [{issue.covered_by.location}]")

                response = input(f"  Remove? [Y/n]: ").strip().lower()
                if response != 'n':
                    project_perms.discard(issue.permission.pattern)
                    changes["redundant_removed"] += 1

        # Apply changes if any were made
        total_changes = sum(changes.values())
        if total_changes > 0:
            print(f"\n{Style.BRIGHT}Creating backups...{Style.RESET_ALL}")
            self.create_backup(self.global_path)
            self.create_backup(self.project_path)

            # Only pass sandbox_network if we made sandbox changes
            sandbox_arg = sandbox_network if changes["migrated_to_sandbox"] > 0 else None
            if self.save_settings(global_perms, project_perms, sandbox_arg):
                print(f"\n{Fore.GREEN}{Style.BRIGHT}Changes applied successfully:{Style.RESET_ALL}")
                if changes["dangerous_removed"] > 0:
                    print(f"  - Removed {changes['dangerous_removed']} dangerous pattern(s)")
                if changes["migrated_to_sandbox"] > 0:
                    print(f"  - Migrated {changes['migrated_to_sandbox']} domain(s) to sandbox")
                if changes["specific_generalized"] > 0:
                    print(f"  - Generalized {changes['specific_generalized']} specific pattern(s)")
                if changes["redundant_removed"] > 0:
                    print(f"  - Removed {changes['redundant_removed']} redundant permission(s)")
            else:
                print(f"\n{Fore.RED}Failed to save changes.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}No changes made.{Style.RESET_ALL}")

    def auto_fix(self, grouped: Dict[IssueType, List[Issue]]):
        """Auto-fix redundant permissions and migrate WebFetch domains to sandbox"""
        redundant = grouped[IssueType.REDUNDANT]
        migrate = grouped[IssueType.MIGRATE_TO_SANDBOX]

        if not redundant and not migrate:
            print(f"\n{Fore.GREEN}No redundant permissions or migrations needed.{Style.RESET_ALL}")
            return

        project_perms = self.project_permissions.copy()
        sandbox_network = self.project_sandbox_network_allow.copy()

        # Handle migrations
        if migrate:
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Migrating {len(migrate)} domain(s) to sandbox...{Style.RESET_ALL}\n")
            for issue in migrate:
                print(f"  - Migrating: {issue.permission.pattern}")
                print(f"    -> sandbox.permissions.network.allow: {issue.migrate_domain}")
                project_perms.discard(issue.permission.pattern)
                sandbox_network.add(issue.migrate_domain)

        # Handle redundant
        if redundant:
            print(f"\n{Fore.BLUE}{Style.BRIGHT}Removing {len(redundant)} redundant permission(s)...{Style.RESET_ALL}\n")
            for issue in redundant:
                print(f"  - Removing: {issue.permission.pattern}")
                print(f"    (Covered by: {issue.covered_by.pattern} [{issue.covered_by.location}])")
                project_perms.discard(issue.permission.pattern)

        # Create backup and save
        print(f"\n{Style.BRIGHT}Creating backup...{Style.RESET_ALL}")
        self.create_backup(self.project_path)

        # Only pass sandbox_network if we made sandbox changes
        sandbox_arg = sandbox_network if migrate else None
        if self.save_settings(self.global_permissions, project_perms, sandbox_arg):
            total = len(redundant) + len(migrate)
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Fixed {total} issue(s):{Style.RESET_ALL}")
            if migrate:
                print(f"  - Migrated {len(migrate)} domain(s) to sandbox")
            if redundant:
                print(f"  - Removed {len(redundant)} redundant permission(s)")
            print()
        else:
            print(f"\n{Fore.RED}Failed to save changes.{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Optimize Claude Code permission settings with sandbox-aware WebFetch migration"
    )
    parser.add_argument(
        "command",
        choices=["analyze", "clean", "auto-fix"],
        help="Command to execute"
    )
    parser.add_argument(
        "--global-settings",
        type=Path,
        help="Path to global settings file (default: ~/.claude/settings.json)"
    )
    parser.add_argument(
        "--project-settings",
        type=Path,
        help="Path to project settings file (default: ./.claude/settings.local.json)"
    )

    args = parser.parse_args()

    optimizer = SettingsOptimizer(args.global_settings, args.project_settings)

    if not optimizer.load_settings():
        return 1

    grouped = optimizer.analyze()

    if args.command == "analyze":
        optimizer.print_report(grouped)
    elif args.command == "clean":
        optimizer.print_report(grouped)
        optimizer.interactive_clean(grouped)
    elif args.command == "auto-fix":
        optimizer.auto_fix(grouped)

    return 0


if __name__ == "__main__":
    exit(main())
