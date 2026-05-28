#!/usr/bin/env python3
"""
Skill Importer Script

This script automates the process of importing skills from remote GitHub repositories
as documented in the skill-importer SKILL.md.

Usage:
    python import_skills.py [--all] [--skill SKILL_NAME] [--update] [--dry-run]
    
Options:
    --all           Import all enabled skills from skill-sources.yaml
    --skill NAME    Import a specific skill by name
    --update        Update existing skills (removes local copy first)
    --dry-run       Show what would be done without actually doing it
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)


class SkillImporter:
    """Handles importing skills from remote GitHub repositories."""
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the skill importer.
        
        Args:
            dry_run: If True, only show what would be done without executing
        """
        self.dry_run = dry_run
        self.script_dir = Path(__file__).parent.absolute()
        self.skill_importer_dir = self.script_dir.parent
        self.config_file = self.skill_importer_dir / "assets" / "skill-sources.yaml"
        self.skills_dir = self.skill_importer_dir.parent
        self.repo_root = self.skills_dir.parent.parent
        
    def load_config(self) -> Dict:
        """Load skill sources from configuration file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        if not config or 'skills' not in config:
            raise ValueError("Invalid configuration: 'skills' key not found")
        
        return config
    
    def parse_github_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Parse GitHub URL to extract repository details.
        
        Args:
            url: GitHub URL (e.g., https://github.com/owner/repo/tree/branch/path/to/skill)
            
        Returns:
            Dictionary with owner, repo, branch, and path, or None if invalid
        """
        # Pattern for GitHub tree URLs
        pattern = r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)'
        match = re.match(pattern, url)
        
        if match:
            owner, repo, branch, path = match.groups()
            return {
                'owner': owner,
                'repo': repo,
                'branch': branch,
                'path': path,
                'clone_url': f'https://github.com/{owner}/{repo}.git'
            }
        
        return None
    
    def clone_repository(self, repo_details: Dict[str, str], temp_dir: Path) -> bool:
        """
        Clone a GitHub repository to a temporary directory.
        
        Args:
            repo_details: Dictionary with repository details
            temp_dir: Temporary directory path
            
        Returns:
            True if successful, False otherwise
        """
        clone_url = repo_details['clone_url']
        branch = repo_details['branch']
        
        cmd = [
            'git', 'clone',
            '--depth', '1',
            '--branch', branch,
            '--single-branch',
            clone_url,
            str(temp_dir)
        ]
        
        print(f"  Cloning {clone_url} (branch: {branch})...")
        
        if self.dry_run:
            print(f"  [DRY-RUN] Would run: {' '.join(cmd)}")
            return True
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"  Error cloning repository: {e.stderr}")
            return False
    
    def copy_skill(self, source_path: Path, skill_name: str) -> bool:
        """
        Copy skill from source to local skills directory.
        
        Args:
            source_path: Path to the skill in the cloned repository
            skill_name: Name of the skill
            
        Returns:
            True if successful, False otherwise
        """
        dest_path = self.skills_dir / skill_name
        
        if not source_path.exists():
            print(f"  Error: Source path does not exist: {source_path}")
            return False
        
        print(f"  Copying skill to {dest_path}...")
        
        if self.dry_run:
            print(f"  [DRY-RUN] Would copy {source_path} to {dest_path}")
            return True
        
        try:
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
            return True
        except Exception as e:
            print(f"  Error copying skill: {e}")
            return False
    
    def verify_skill(self, skill_name: str) -> bool:
        """
        Verify that a skill was imported correctly.
        
        Args:
            skill_name: Name of the skill to verify
            
        Returns:
            True if skill exists and has a SKILL.md file
        """
        skill_path = self.skills_dir / skill_name
        skill_md = skill_path / "SKILL.md"
        
        if not skill_path.exists():
            print(f"  ✗ Skill directory not found: {skill_path}")
            return False
        
        if not skill_md.exists():
            print(f"  ✗ SKILL.md not found in {skill_path}")
            return False
        
        print(f"  ✓ Skill verified: {skill_name}")
        return True
    
    def import_skill(self, skill_config: Dict, update: bool = False) -> bool:
        """
        Import a single skill from remote repository.
        
        Args:
            skill_config: Skill configuration dictionary
            update: If True, remove existing skill before importing
            
        Returns:
            True if successful, False otherwise
        """
        skill_name = skill_config['name']
        url = skill_config['url']
        enabled = skill_config.get('enabled', True)
        
        print(f"\n{'=' * 60}")
        print(f"Importing skill: {skill_name}")
        print(f"Source: {url}")
        print(f"{'=' * 60}")
        
        if not enabled:
            print(f"  Skipping (disabled in configuration)")
            return False
        
        # Check if skill already exists
        skill_path = self.skills_dir / skill_name
        if skill_path.exists() and not update:
            print(f"  Skill already exists. Use --update to update it.")
            return False
        
        # Parse GitHub URL
        repo_details = self.parse_github_url(url)
        if not repo_details:
            print(f"  Error: Could not parse GitHub URL: {url}")
            return False
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            
            # Clone repository
            if not self.clone_repository(repo_details, temp_dir):
                return False
            
            # Construct path to skill in cloned repository
            skill_source_path = temp_dir / repo_details['path']
            
            # Copy skill
            if not self.copy_skill(skill_source_path, skill_name):
                return False
        
        # Verify import
        if not self.dry_run:
            return self.verify_skill(skill_name)
        
        return True
    
    def import_all_skills(self, update: bool = False) -> None:
        """
        Import all enabled skills from configuration.
        
        Args:
            update: If True, update existing skills
        """
        config = self.load_config()
        skills = config.get('skills', [])
        
        if not skills:
            print("No skills found in configuration.")
            return
        
        enabled_skills = [s for s in skills if s.get('enabled', True)]
        print(f"Found {len(enabled_skills)} enabled skill(s) to import.")
        
        success_count = 0
        fail_count = 0
        skip_count = 0
        
        for skill_config in skills:
            if not skill_config.get('enabled', True):
                skip_count += 1
                continue
            
            if self.import_skill(skill_config, update=update):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n{'=' * 60}")
        print(f"Import Summary")
        print(f"{'=' * 60}")
        print(f"  Successful: {success_count}")
        print(f"  Failed:     {fail_count}")
        print(f"  Skipped:    {skip_count}")
        print(f"{'=' * 60}")
    
    def import_single_skill(self, skill_name: str, update: bool = False) -> None:
        """
        Import a single skill by name.
        
        Args:
            skill_name: Name of the skill to import
            update: If True, update existing skill
        """
        config = self.load_config()
        skills = config.get('skills', [])
        
        # Find skill in configuration
        skill_config = None
        for skill in skills:
            if skill['name'] == skill_name:
                skill_config = skill
                break
        
        if not skill_config:
            print(f"Error: Skill '{skill_name}' not found in configuration.")
            print(f"Available skills:")
            for skill in skills:
                print(f"  - {skill['name']}")
            sys.exit(1)
        
        if self.import_skill(skill_config, update=update):
            print("\n✓ Skill imported successfully!")
        else:
            print("\n✗ Skill import failed.")
            sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Import skills from remote GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import all enabled skills
  python import_skills.py --all

  # Import a specific skill
  python import_skills.py --skill sync-job-expert

  # Update an existing skill
  python import_skills.py --skill doctype-schema-expert --update

  # Dry-run to see what would happen
  python import_skills.py --all --dry-run
        """
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Import all enabled skills')
    parser.add_argument('--skill', type=str,
                        help='Import a specific skill by name')
    parser.add_argument('--update', action='store_true',
                        help='Update existing skills')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without doing it')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all and not args.skill:
        parser.print_help()
        print("\nError: Must specify either --all or --skill")
        sys.exit(1)
    
    if args.all and args.skill:
        print("Error: Cannot specify both --all and --skill")
        sys.exit(1)
    
    # Create importer
    importer = SkillImporter(dry_run=args.dry_run)
    
    try:
        if args.all:
            importer.import_all_skills(update=args.update)
        elif args.skill:
            importer.import_single_skill(args.skill, update=args.update)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
