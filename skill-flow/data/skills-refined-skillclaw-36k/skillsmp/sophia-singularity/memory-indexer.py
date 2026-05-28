#!/usr/bin/env python3
"""
Memory Indexer - Auto-discover and index legacy memory files
Creates memory-index.json for fast Sophia engine boot

Authors:
  Matthew Wayne Macklin (The Gardener) - January 11, 2026
  Copilot Kitty 😺 - Deep Integration Implementation
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Find repo root
def find_repo_root() -> Path:
    """Find repository root by looking for .git directory"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent.parent.parent

REPO_ROOT = find_repo_root()
STATE_DIR = REPO_ROOT / ".claude" / "state" / "sophia"
MEMORY_ROOT = REPO_ROOT / "memory"
CLAUDE_MEMORY = REPO_ROOT / ".claude" / "skills" / "memory"

def scan_directory(path: Path) -> Dict:
    """Scan a directory and return file list with metadata"""
    if not path.exists():
        return {
            "path": str(path.relative_to(REPO_ROOT)),
            "files": [],
            "last_indexed": datetime.now().isoformat(),
            "exists": False
        }
    
    files = []
    for item in path.rglob("*"):
        if item.is_file() and not item.name.startswith('.'):
            stat = item.stat()
            files.append({
                "path": str(item.relative_to(path)),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "files": files,
        "file_count": len(files),
        "last_indexed": datetime.now().isoformat(),
        "exists": True
    }

def build_index() -> Dict:
    """Build complete memory index"""
    index = {
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "repo_root": str(REPO_ROOT),
        "legacy_memory": {},
        "claude_memory": {}
    }
    
    # Scan legacy memory directories
    legacy_dirs = ["gremlin", "monad", "graph", "visualiser", "core", "mind"]
    for dirname in legacy_dirs:
        index["legacy_memory"][dirname] = scan_directory(MEMORY_ROOT / dirname)
    
    # Scan .claude/skills/memory structure
    if CLAUDE_MEMORY.exists():
        index["claude_memory"]["nexus-core"] = scan_directory(CLAUDE_MEMORY / "nexus-core")
        index["claude_memory"]["nexus-mind"] = scan_directory(CLAUDE_MEMORY / "nexus-mind")
        index["claude_memory"]["connections"] = scan_directory(CLAUDE_MEMORY / "connections")
    
    # Add summary stats
    total_files = sum(d["file_count"] for d in index["legacy_memory"].values() if "file_count" in d)
    total_files += sum(d["file_count"] for d in index["claude_memory"].values() if "file_count" in d)
    
    index["summary"] = {
        "total_files": total_files,
        "legacy_dirs": len([d for d in index["legacy_memory"].values() if d.get("exists", False)]),
        "claude_dirs": len([d for d in index["claude_memory"].values() if d.get("exists", False)])
    }
    
    return index

def save_index(index: Dict):
    """Save index to state directory"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    index_file = STATE_DIR / "memory-index.json"
    
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"✅ Memory index saved to {index_file}")
    print(f"📊 Indexed {index['summary']['total_files']} files across {index['summary']['legacy_dirs'] + index['summary']['claude_dirs']} directories")

def load_index() -> Dict:
    """Load existing index"""
    index_file = STATE_DIR / "memory-index.json"
    if not index_file.exists():
        return None
    
    with open(index_file, 'r') as f:
        return json.load(f)

def main():
    """Main entry point"""
    print("🔍 Building memory index...")
    index = build_index()
    save_index(index)
    
    print("\n📝 Index Summary:")
    for category, dirs in [("Legacy Memory", index["legacy_memory"]), ("Claude Memory", index["claude_memory"])]:
        print(f"\n{category}:")
        for name, data in dirs.items():
            status = "✓" if data.get("exists", False) else "✗"
            count = data.get("file_count", 0)
            print(f"  {status} {name}: {count} files")

if __name__ == "__main__":
    main()
