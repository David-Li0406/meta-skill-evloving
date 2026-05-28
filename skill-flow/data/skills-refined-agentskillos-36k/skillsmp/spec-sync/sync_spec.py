#!/usr/bin/env python3
"""
Spec Synchronization Script (Auto-Detection Version)

This script ensures that the decomposed spec files in the Skills directory
stay in sync with the master DEV_SPEC.md file.

Features:
- **Auto-Detection**: Automatically detects all top-level chapters (## N. Title)
- **Smart Naming**: Generates slug-based filenames from Chinese titles
- **Hash-based Sync**: Only regenerates when DEV_SPEC.md actually changes
- **Dynamic Index**: Generates SPEC_INDEX.md based on detected chapters

Usage:
    python sync_spec.py [--force]

Options:
    --force    Force regeneration even if hash matches
"""

import hashlib
import re
import sys
from pathlib import Path
from typing import List, Tuple, NamedTuple


class Chapter(NamedTuple):
    """Represents a detected chapter"""
    number: int           # Chapter number (1, 2, 3...)
    cn_title: str         # Chinese title (e.g., "项目概述")
    filename: str         # Generated filename (e.g., "01-overview.md")
    start_line: int       # Start line in DEV_SPEC.md
    end_line: int         # End line in DEV_SPEC.md
    line_count: int       # Number of lines in this chapter


class SpecSynchronizer:
    """Synchronizes DEV_SPEC.md with decomposed chapter files"""
    
    # Chinese title -> English slug mapping
    # Add new mappings here when you create new top-level chapters
    TITLE_SLUG_MAP = {
        "项目概述": "overview",
        "核心特点": "features",
        "技术选型": "tech-stack",
        "测试方案": "testing",
        "系统架构与模块设计": "architecture",
        "项目排期": "schedule",
        "可扩展性与未来展望": "future",
        # ========================================
        # Add new chapters here as needed:
        # "安全与合规": "security",
        # "部署运维指南": "operations",
        # ========================================
    }
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.dev_spec_path = repo_root / "DEV_SPEC.md"
        self.skills_dir = repo_root / ".github" / "skills" / "spec-sync"
        self.specs_dir = self.skills_dir / "specs"
        self.hash_file = self.skills_dir / ".spec_hash"
        self.index_file = self.skills_dir / "SPEC_INDEX.md"
        
        # Will be populated by auto-detection
        self.chapters: List[Chapter] = []
    
    def calculate_hash(self) -> str:
        """Calculate SHA256 hash of DEV_SPEC.md"""
        if not self.dev_spec_path.exists():
            raise FileNotFoundError(f"DEV_SPEC.md not found at {self.dev_spec_path}")
        
        sha256 = hashlib.sha256()
        with open(self.dev_spec_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def load_stored_hash(self) -> str | None:
        """Load the stored hash from .spec_hash file"""
        if not self.hash_file.exists():
            return None
        return self.hash_file.read_text().strip()
    
    def save_hash(self, hash_value: str):
        """Save the hash to .spec_hash file"""
        self.hash_file.write_text(hash_value)
    
    def needs_sync(self, force: bool = False) -> bool:
        """Check if sync is needed"""
        if force:
            return True
        
        current_hash = self.calculate_hash()
        stored_hash = self.load_stored_hash()
        
        if stored_hash is None:
            print("⚠️  No stored hash found. First-time sync required.")
            return True
        
        if current_hash != stored_hash:
            print("🔄 DEV_SPEC.md has changed. Re-sync required.")
            return True
        
        print("✅ Spec files are up to date.")
        return False
    
    def _generate_slug(self, cn_title: str) -> str:
        """
        Generate English slug from Chinese title.
        Falls back to sanitized title if not in mapping.
        """
        # Try exact match first
        if cn_title in self.TITLE_SLUG_MAP:
            return self.TITLE_SLUG_MAP[cn_title]
        
        # Try partial match (for titles with minor variations)
        for key, slug in self.TITLE_SLUG_MAP.items():
            if key in cn_title or cn_title in key:
                return slug
        
        # Fallback: use sanitized Chinese title (replace spaces with dashes)
        # This is not ideal but ensures the script doesn't fail
        print(f"⚠️  No slug mapping for '{cn_title}'. Using sanitized title.")
        print(f"   💡 Tip: Add this to TITLE_SLUG_MAP for better filenames.")
        return re.sub(r'[^\w\u4e00-\u9fff]+', '-', cn_title).strip('-').lower()
    
    def auto_detect_chapters(self, content: str) -> List[Chapter]:
        """
        Automatically detect all top-level chapters in the spec.
        
        Looks for patterns like:
        - ## 1. 项目概述
        - ## 2. 核心特点
        - etc.
        
        Returns list of Chapter objects with boundaries.
        """
        lines = content.split('\n')
        chapter_starts: List[Tuple[int, str, int]] = []  # (chapter_num, title, line_num)
        
        # Pattern: ## {number}. {title}
        pattern = r'^## (\d+)\.\s+(.+)$'
        
        # First pass: find all chapter headers
        for i, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                chapter_num = int(match.group(1))
                chapter_title = match.group(2).strip()
                chapter_starts.append((chapter_num, chapter_title, i))
        
        if not chapter_starts:
            raise ValueError("No chapters found in DEV_SPEC.md. Expected format: '## N. Title'")
        
        # Second pass: calculate boundaries and create Chapter objects
        chapters = []
        for idx, (num, title, start) in enumerate(chapter_starts):
            # End line is the start of next chapter, or end of file
            end = chapter_starts[idx + 1][2] if idx + 1 < len(chapter_starts) else len(lines)
            
            # Generate filename
            slug = self._generate_slug(title)
            filename = f"{num:02d}-{slug}.md"
            
            chapter = Chapter(
                number=num,
                cn_title=title,
                filename=filename,
                start_line=start,
                end_line=end,
                line_count=end - start
            )
            chapters.append(chapter)
        
        return chapters
    
    def split_spec(self):
        """Split DEV_SPEC.md into chapter files"""
        print("📄 Reading DEV_SPEC.md...")
        content = self.dev_spec_path.read_text(encoding='utf-8')
        
        print("🔍 Auto-detecting chapters...")
        self.chapters = self.auto_detect_chapters(content)
        
        print(f"   Found {len(self.chapters)} chapters:")
        for ch in self.chapters:
            print(f"      {ch.number}. {ch.cn_title}")
        
        # Create specs directory
        self.specs_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up old files that might no longer exist
        existing_files = set(f.name for f in self.specs_dir.glob("*.md"))
        new_files = set(ch.filename for ch in self.chapters)
        orphaned_files = existing_files - new_files
        
        if orphaned_files:
            print(f"\n🗑️  Removing {len(orphaned_files)} orphaned file(s)...")
            for orphan in orphaned_files:
                (self.specs_dir / orphan).unlink()
                print(f"   ✗ Removed {orphan}")
        
        lines = content.split('\n')
        
        print("\n✂️  Splitting into chapter files...")
        for chapter in self.chapters:
            chapter_content = '\n'.join(lines[chapter.start_line:chapter.end_line])
            output_path = self.specs_dir / chapter.filename
            output_path.write_text(chapter_content, encoding='utf-8')
            print(f"   ✓ {chapter.filename} ({chapter.line_count} lines)")
        
        print(f"\n📁 Generated {len(self.chapters)} chapter files in {self.specs_dir}")
    
    def generate_index(self):
        """Generate SPEC_INDEX.md navigation file based on detected chapters"""
        
        # Build chapter table rows dynamically
        table_rows = []
        for ch in self.chapters:
            table_rows.append(
                f"| **{ch.number}. {ch.cn_title}** | "
                f"[`specs/{ch.filename}`](specs/{ch.filename}) | "
                f"{ch.line_count} lines |"
            )
        
        chapter_table = "\n".join(table_rows)
        
        # Build quick links dynamically
        quick_links = []
        for ch in self.chapters:
            quick_links.append(f"- [{ch.cn_title}](specs/{ch.filename})")
        quick_links_text = "\n".join(quick_links)
        
        index_content = f"""# Spec Index & Navigation Guide

> **Purpose**: This index helps you quickly locate the relevant chapter without reading the entire DEV_SPEC.md.
> **Auto-Generated**: This file is automatically generated by `sync_spec.py`. Do not edit manually.
> **Last Sync**: Based on DEV_SPEC.md with {len(self.chapters)} chapters detected.

---

## 📚 Chapter Overview

| Chapter | File | Size |
|---------|------|------|
{chapter_table}

---

## 🔗 Quick Links

{quick_links_text}

---

## 🎯 Reading Strategy

### For First-Time Contributors
1. Start with the **overview** chapter to understand the project's mission
2. Skim the **architecture** chapter to familiarize yourself with the directory structure
3. Read the **schedule** chapter to see the current progress and next steps

### For Implementing a New Feature
1. Check the **schedule** chapter to find the relevant phase/task
2. Read the corresponding section in **tech-stack** or **architecture** chapters
3. Consult the **testing** chapter for testing guidelines

### For Debugging or Optimization
1. Read the **architecture** chapter to understand the data flow
2. Check the **tech-stack** chapter for observability design
3. Review the **testing** chapter for regression testing strategies

---

## ⚠️ Important Notes

1. **Do NOT edit files in `specs/` directly** - they are auto-generated
2. **Always edit `DEV_SPEC.md`** at the repo root, then run `sync_spec.py`
3. **Adding new chapters**: Just add `## N. Title` in DEV_SPEC.md and update `TITLE_SLUG_MAP` in sync_spec.py

---

*Generated by sync_spec.py*
"""
        self.index_file.write_text(index_content, encoding='utf-8')
        print(f"📑 Generated SPEC_INDEX.md")
    
    def sync(self, force: bool = False):
        """Main sync operation"""
        if not self.needs_sync(force):
            return
        
        print("\n🔄 Starting spec synchronization...\n")
        
        try:
            self.split_spec()
            self.generate_index()
            
            current_hash = self.calculate_hash()
            self.save_hash(current_hash)
            
            print(f"\n✅ Sync completed successfully!")
            print(f"   Hash: {current_hash[:16]}...")
            
        except Exception as e:
            print(f"\n❌ Sync failed: {e}")
            sys.exit(1)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Sync DEV_SPEC.md with Skills directory")
    parser.add_argument('--force', action='store_true', help="Force regeneration even if hash matches")
    args = parser.parse_args()
    
    # Detect repo root (assuming script is in .github/skills/implement-from-spec/)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent
    
    synchronizer = SpecSynchronizer(repo_root)
    synchronizer.sync(force=args.force)


if __name__ == "__main__":
    main()
