import argparse
import os
import sys
import re
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install PyYAML")
    sys.exit(1)


class TagFixer:
    def __init__(self, vault_path, dry_run=False, verbose=False):
        self.vault_path = vault_path
        self.dry_run = dry_run
        self.verbose = verbose
        self.changes = defaultdict(list)
        
    def log(self, message, force=False):
        """Log message if verbose or force is True."""
        if self.verbose or force:
            print(message)
    
    def fix_formatting_issues(self):
        """Fix tag formatting issues like #tag in frontmatter."""
        files_modified = 0
        
        for root, dirs, files in os.walk(self.vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not file.endswith('.md'):
                    continue
                    
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.vault_path)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Check if file has frontmatter
                    if not content.startswith('---'):
                        continue
                    
                    # Split frontmatter and body
                    parts = content.split('---', 2)
                    if len(parts) < 3:
                        continue
                    
                    frontmatter = parts[1]
                    body = parts[2]
                    
                    # Parse frontmatter
                    try:
                        metadata = yaml.safe_load(frontmatter)
                    except yaml.YAMLError:
                        continue
                    
                    if not metadata or 'tags' not in metadata:
                        continue
                    
                    # Fix tags with # prefix
                    tags = metadata['tags']
                    modified = False
                    
                    if isinstance(tags, list):
                        new_tags = []
                        for tag in tags:
                            tag_str = str(tag).strip()
                            if tag_str.startswith('#'):
                                old_tag = tag_str
                                new_tag = tag_str.lstrip('#')
                                new_tags.append(new_tag)
                                self.changes[rel_path].append(f"Tag: {old_tag} → {new_tag}")
                                modified = True
                            else:
                                new_tags.append(tag_str)
                        
                        if modified:
                            metadata['tags'] = new_tags
                    
                    elif isinstance(tags, str):
                        if tags.startswith('#'):
                            old_tag = tags
                            new_tag = tags.lstrip('#')
                            metadata['tags'] = new_tag
                            self.changes[rel_path].append(f"Tag: {old_tag} → {new_tag}")
                            modified = True
                    
                    if modified:
                        files_modified += 1
                        
                        if not self.dry_run:
                            # Reconstruct file
                            new_frontmatter = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
                            new_content = f"---\n{new_frontmatter}---{body}"
                            
                            with open(full_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            self.log(f"✓ Fixed: {rel_path}")
                        else:
                            self.log(f"[DRY RUN] Would fix: {rel_path}")
                
                except Exception as e:
                    self.log(f"Warning: Could not process {rel_path}: {e}", force=True)
        
        return files_modified
    
    def remove_tags(self, tags_to_remove=None, pattern=None):
        """Remove specific tags or tags matching a pattern."""
        if not tags_to_remove and not pattern:
            return 0
        
        files_modified = 0
        pattern_re = re.compile(pattern) if pattern else None
        
        for root, dirs, files in os.walk(self.vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not file.endswith('.md'):
                    continue
                    
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.vault_path)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Check if file has frontmatter
                    if not content.startswith('---'):
                        continue
                    
                    # Split frontmatter and body
                    parts = content.split('---', 2)
                    if len(parts) < 3:
                        continue
                    
                    frontmatter = parts[1]
                    body = parts[2]
                    
                    # Parse frontmatter
                    try:
                        metadata = yaml.safe_load(frontmatter)
                    except yaml.YAMLError:
                        continue
                    
                    if not metadata or 'tags' not in metadata:
                        continue
                    
                    # Remove specified tags
                    tags = metadata['tags']
                    modified = False
                    
                    if isinstance(tags, list):
                        new_tags = []
                        for tag in tags:
                            tag_str = str(tag).strip()
                            should_remove = False
                            
                            # Check if tag should be removed
                            if tags_to_remove and tag_str in tags_to_remove:
                                should_remove = True
                            elif pattern_re and pattern_re.match(tag_str):
                                should_remove = True
                            
                            if should_remove:
                                self.changes[rel_path].append(f"Removed tag: {tag_str}")
                                modified = True
                            else:
                                new_tags.append(tag_str)
                        
                        if modified:
                            if new_tags:
                                metadata['tags'] = new_tags
                            else:
                                # Remove tags key if no tags left
                                del metadata['tags']
                    
                    elif isinstance(tags, str):
                        tag_str = tags.strip()
                        should_remove = False
                        
                        if tags_to_remove and tag_str in tags_to_remove:
                            should_remove = True
                        elif pattern_re and pattern_re.match(tag_str):
                            should_remove = True
                        
                        if should_remove:
                            self.changes[rel_path].append(f"Removed tag: {tag_str}")
                            del metadata['tags']
                            modified = True
                    
                    if modified:
                        files_modified += 1
                        
                        if not self.dry_run:
                            # Reconstruct file
                            new_frontmatter = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
                            new_content = f"---\n{new_frontmatter}---{body}"
                            
                            with open(full_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            self.log(f"✓ Modified: {rel_path}")
                        else:
                            self.log(f"[DRY RUN] Would modify: {rel_path}")
                
                except Exception as e:
                    self.log(f"Warning: Could not process {rel_path}: {e}", force=True)
        
        return files_modified
    
    def print_summary(self):
        """Print summary of changes."""
        if not self.changes:
            print("\nNo changes needed.")
            return
        
        print(f"\n{'='*60}")
        print(f"{'DRY RUN - ' if self.dry_run else ''}Changes Summary")
        print(f"{'='*60}")
        
        for file_path, changes in sorted(self.changes.items()):
            print(f"\n📄 {file_path}")
            for change in changes:
                print(f"   • {change}")
        
        print(f"\n{'='*60}")
        print(f"Total files affected: {len(self.changes)}")
        print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fix tag issues in an Obsidian vault",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview formatting fixes
  %(prog)s --vault /path/to/vault --fix-format --dry-run
  
  # Fix formatting issues
  %(prog)s --vault /path/to/vault --fix-format
  
  # Remove specific tags
  %(prog)s --vault /path/to/vault --remove-tags "step-1,step-2,cate2"
  
  # Remove tags matching pattern
  %(prog)s --vault /path/to/vault --remove-pattern "^step-.*" --dry-run
        """
    )
    
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--fix-format", action="store_true", help="Fix tag formatting issues (e.g., #tag → tag)")
    parser.add_argument("--remove-tags", help="Comma-separated list of tags to remove")
    parser.add_argument("--remove-pattern", help="Regex pattern for tags to remove")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.vault):
        print(f"Error: Vault path '{args.vault}' does not exist.")
        sys.exit(1)
    
    if not any([args.fix_format, args.remove_tags, args.remove_pattern]):
        print("Error: Must specify at least one action (--fix-format, --remove-tags, or --remove-pattern)")
        sys.exit(1)
    
    fixer = TagFixer(args.vault, dry_run=args.dry_run, verbose=args.verbose)
    
    total_files = 0
    
    # Fix formatting issues
    if args.fix_format:
        print("Fixing tag formatting issues...")
        total_files += fixer.fix_formatting_issues()
    
    # Remove tags
    if args.remove_tags or args.remove_pattern:
        tags_list = args.remove_tags.split(',') if args.remove_tags else None
        tags_list = [t.strip() for t in tags_list] if tags_list else None
        
        if tags_list:
            print(f"Removing tags: {', '.join(tags_list)}")
        if args.remove_pattern:
            print(f"Removing tags matching pattern: {args.remove_pattern}")
        
        total_files += fixer.remove_tags(tags_to_remove=tags_list, pattern=args.remove_pattern)
    
    # Print summary
    fixer.print_summary()
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files were modified")
        print("Remove --dry-run flag to apply changes")
    else:
        print(f"\n✅ Successfully processed {total_files} files")
