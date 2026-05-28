#!/usr/bin/env python3
"""
Global Prompt Sync Script

Synchronizes prompt files from the skill's prompts directory to both GitHub Copilot
and OpenCode global configuration directories.

Directory structure:
- prompts/agents/    -> agents
- prompts/rules/     -> rules/instructions
- prompts/commands/  -> commands/prompts
"""

import os
import shutil
import glob
import sys
import subprocess
import argparse
import re
import yaml
from pathlib import Path
from typing import List, Optional


class PromptSyncer:
    """Handles synchronization of prompt files to multiple editors."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.skill_root = self.script_dir.parent
        self.prompts_dir = self.skill_root / "prompts"
        self.username = self._get_windows_username()
        
    def _get_windows_username(self) -> Optional[str]:
        """Get Windows username via cmd.exe."""
        try:
            result = subprocess.run(
                ["cmd.exe", "/c", "echo", "%USERNAME%"],
                capture_output=True,
                check=True
            )
            try:
                return result.stdout.decode('utf-8').strip()
            except UnicodeDecodeError:
                return result.stdout.decode('cp932').strip()
        except Exception as e:
            print(f"Error getting Windows username: {e}")
            return None
    
    def _is_wsl(self) -> bool:
        """Detect if running in WSL environment."""
        return os.path.exists("/proc/version") and "microsoft" in open("/proc/version").read().lower()
    
    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML front matter from markdown content."""
        # Match front matter: --- at start, content, --- at end
        pattern = r'^---\s*\n.*?\n---\s*\n'
        return re.sub(pattern, '', content, flags=re.DOTALL)
    
    def _remove_tools_from_frontmatter(self, content: str, target_format: str) -> str:
        """
        Remove tools property from frontmatter if format doesn't match target.
        
        Args:
            content: Markdown content with frontmatter
            target_format: 'copilot' or 'opencode'
        
        Returns:
            Content with tools removed if necessary, or original content
        """
        # Extract frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            return content
        
        frontmatter_str, body = match.groups()
        
        try:
            metadata = yaml.safe_load(frontmatter_str)
            
            if not metadata or 'tools' not in metadata:
                return content  # No tools property, nothing to do
            
            # Detect format
            tools = metadata['tools']
            is_copilot_format = isinstance(tools, list)
            is_opencode_format = isinstance(tools, dict)
            
            # Decide if we need to remove tools
            should_remove = False
            if target_format == 'copilot' and is_opencode_format:
                should_remove = True
                print(f"    (Detected OpenCode format tools, removing for Copilot)")
            elif target_format == 'opencode' and is_copilot_format:
                should_remove = True
                print(f"    (Detected Copilot format tools, removing for OpenCode)")
            
            if should_remove:
                del metadata['tools']
                # Reconstruct frontmatter
                new_frontmatter = yaml.dump(metadata, default_flow_style=False, 
                                          allow_unicode=True, sort_keys=False)
                return f"---\n{new_frontmatter}---\n{body}"
            
            return content
            
        except Exception as e:
            print(f"    Warning: Could not parse frontmatter ({e}), using as-is")
            return content
    
    def _merge_rules(self, rules_files: List[Path]) -> str:
        """Merge multiple rule files into one, removing front matter."""
        merged_content = []
        
        for file_path in sorted(rules_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove front matter
                    content = self._remove_frontmatter(content)
                    if content.strip():
                        merged_content.append(content.strip())
            except Exception as e:
                print(f"Warning: Could not read {file_path.name}: {e}")
        
        return "\n\n".join(merged_content)
    
    def sync_to_copilot(self) -> bool:
        """Sync prompts to GitHub Copilot directory."""
        if not self.username:
            print("Could not determine Windows username. Skipping Copilot sync.")
            return False
        
        # Determine copilot directory path based on environment
        if self._is_wsl():
            copilot_dir = Path(f"/mnt/c/Users/{self.username}/AppData/Roaming/Code/User/prompts")
        else:
            # Windows environment - use Path to handle both forward and backslashes
            copilot_dir = Path(f"C:/Users/{self.username}/AppData/Roaming/Code/User/prompts")
        
        print(f"\n=== Syncing to GitHub Copilot ===")
        print(f"Target: {copilot_dir}")
        
        if not copilot_dir.exists():
            try:
                copilot_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {copilot_dir}")
            except OSError as e:
                print(f"Error creating directory: {e}")
                return False
        
        success = True
        
        # Sync agents (*.agent.md)
        agents_dir = self.prompts_dir / "agents"
        if agents_dir.exists():
            for file_path in agents_dir.glob("*.md"):
                # Change extension to .agent.md if not already
                if file_path.stem.endswith('.agent'):
                    dest_name = file_path.name
                else:
                    dest_name = f"{file_path.stem}.agent.md"
                
                dest_path = copilot_dir / dest_name
                try:
                    # Read and process frontmatter
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Remove tools if format doesn't match
                    content = self._remove_tools_from_frontmatter(content, 'copilot')
                    
                    # Write processed content
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✓ Agent: {file_path.name} -> {dest_name}")
                except Exception as e:
                    print(f"✗ Error copying {file_path.name}: {e}")
                    success = False
        
        # Sync rules (*.instructions.md)
        rules_dir = self.prompts_dir / "rules"
        if rules_dir.exists():
            for file_path in rules_dir.glob("*.md"):
                # Change extension to .instructions.md if not already
                if file_path.stem.endswith('.instructions'):
                    dest_name = file_path.name
                else:
                    dest_name = f"{file_path.stem}.instructions.md"
                
                dest_path = copilot_dir / dest_name
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"✓ Rule: {file_path.name} -> {dest_name}")
                except Exception as e:
                    print(f"✗ Error copying {file_path.name}: {e}")
                    success = False
        
        # Sync commands (*.prompt.md)
        commands_dir = self.prompts_dir / "commands"
        if commands_dir.exists():
            for file_path in commands_dir.glob("*.md"):
                # Change extension to .prompt.md if not already
                if file_path.stem.endswith('.prompt'):
                    dest_name = file_path.name
                else:
                    dest_name = f"{file_path.stem}.prompt.md"
                
                dest_path = copilot_dir / dest_name
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"✓ Command: {file_path.name} -> {dest_name}")
                except Exception as e:
                    print(f"✗ Error copying {file_path.name}: {e}")
                    success = False
        
        return success
    
    def sync_to_opencode(self) -> bool:
        """Sync prompts to OpenCode directories."""
        print(f"\n=== Syncing to OpenCode ===")
        
        # Determine target paths based on environment
        opencode_paths = []
        
        if self._is_wsl():
            # In WSL, sync to both WSL and Windows paths
            wsl_config = Path.home() / ".config" / "opencode"
            opencode_paths.append(("WSL", wsl_config))
            
            if self.username:
                win_config = Path(f"/mnt/c/Users/{self.username}/.config/opencode")
                if win_config.parent.exists():
                    opencode_paths.append(("Windows", win_config))
        else:
            # Not in WSL, use local config
            local_config = Path.home() / ".config" / "opencode"
            opencode_paths.append(("Local", local_config))
        
        if not opencode_paths:
            print("No OpenCode config paths available")
            return False
        
        success = True
        
        for env_name, opencode_base in opencode_paths:
            print(f"\n--- Syncing to {env_name} OpenCode: {opencode_base} ---")
            
            # Sync agents to agent/ directory
            agents_dest = opencode_base / "agent"
            agents_dir = self.prompts_dir / "agents"
            if agents_dir.exists():
                agents_dest.mkdir(parents=True, exist_ok=True)
                for file_path in agents_dir.glob("*.md"):
                    dest_path = agents_dest / file_path.name
                    try:
                        # Read and process frontmatter
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Remove tools if format doesn't match
                        content = self._remove_tools_from_frontmatter(content, 'opencode')
                        
                        # Write processed content
                        with open(dest_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"✓ Agent: {file_path.name}")
                    except Exception as e:
                        print(f"✗ Error copying agent {file_path.name}: {e}")
                        success = False
            
            # Sync and merge rules to AGENTS.md
            rules_dir = self.prompts_dir / "rules"
            if rules_dir.exists():
                rules_files = list(rules_dir.glob("*.md"))
                if rules_files:
                    merged_content = self._merge_rules(rules_files)
                    agents_md_path = opencode_base / "AGENTS.md"
                    try:
                        opencode_base.mkdir(parents=True, exist_ok=True)
                        with open(agents_md_path, 'w', encoding='utf-8') as f:
                            f.write(merged_content)
                        print(f"✓ Rules merged into AGENTS.md ({len(rules_files)} files)")
                    except Exception as e:
                        print(f"✗ Error creating AGENTS.md: {e}")
                        success = False
            
            # Sync commands to command/ directory
            commands_dest = opencode_base / "command"
            commands_dir = self.prompts_dir / "commands"
            if commands_dir.exists():
                commands_dest.mkdir(parents=True, exist_ok=True)
                for file_path in commands_dir.glob("*.md"):
                    dest_path = commands_dest / file_path.name
                    try:
                        shutil.copy2(file_path, dest_path)
                        print(f"✓ Command: {file_path.name}")
                    except Exception as e:
                        print(f"✗ Error copying command {file_path.name}: {e}")
                        success = False
        
        return success
    
    def sync_all(self, target: Optional[str] = None) -> bool:
        """Sync to all targets or a specific target."""
        if not self.prompts_dir.exists():
            print(f"Error: Prompts directory not found: {self.prompts_dir}")
            return False
        
        success = True
        
        if target is None or target == "copilot":
            if not self.sync_to_copilot():
                success = False
        
        if target is None or target == "opencode":
            if not self.sync_to_opencode():
                success = False
        
        return success


def main():
    parser = argparse.ArgumentParser(
        description="Sync prompt files to GitHub Copilot and OpenCode"
    )
    parser.add_argument(
        "--target",
        choices=["copilot", "opencode"],
        help="Sync to a specific target (default: sync to all)"
    )
    
    args = parser.parse_args()
    
    syncer = PromptSyncer()
    success = syncer.sync_all(args.target)
    
    print("\n" + "=" * 50)
    if success:
        print("✓ Synchronization completed successfully")
    else:
        print("✗ Synchronization completed with errors")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
