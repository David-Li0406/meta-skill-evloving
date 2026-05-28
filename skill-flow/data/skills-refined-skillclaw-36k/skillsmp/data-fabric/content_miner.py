"""
Content Miner - Data Fabric Phase 1
Extracts deep metadata from file systems to build a Knowledge Graph.
"""

import os
import sys
import json
import time
import uuid
import hashlib
import mimetypes
import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentMiner:
    def __init__(self, root_path: str, output_file: str = "docs/fabric_index.json"):
        self.root_path = Path(root_path)
        self.output_file = Path(output_file)
        self.index = {
            "metadata": {
                "scan_time": datetime.datetime.now().isoformat(),
                "root_path": str(self.root_path),
                "total_files": 0,
                "total_size_mb": 0
            },
            "files": []
        }

    def generate_id(self, file_path: Path) -> str:
        """Generates a consistent ID based on path."""
        return hashlib.md5(str(file_path).encode('utf-8')).hexdigest()

    def get_temporal_dna(self, file_path: Path) -> Dict[str, str]:
        """Extracts creation and modification times."""
        try:
            stat = file_path.stat()
            return {
                "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.datetime.fromtimestamp(stat.st_atime).isoformat()
            }
        except Exception:
            return {}

    def get_semantic_tags(self, file_path: Path) -> List[str]:
        """Extracts tags from path context."""
        try:
            # Extract parent folders as tags, excluding root parts
            relative_parts = file_path.relative_to(self.root_path).parts[:-1]
            tags = [p for p in relative_parts if p not in ['.', '..']]
            
            # Add extension as tag
            tags.append(file_path.suffix.lower())
            
            # Add year tag if present in path
            for part in relative_parts:
                if part.isdigit() and len(part) == 4 and part.startswith('20'):
                    tags.append(f"year:{part}")
            
            return list(set(tags))
        except ValueError:
            return []

    def scan(self):
        """Walks the directory and builds the index."""
        logger.info(f"Starting mine of {self.root_path}...")
        
        start_time = time.time()
        file_count = 0
        total_size = 0

        # Safe extensions to mine (avoiding system files)
        # We want broad coverage but not junk
        IGNORE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.vscode', '$RECYCLE.BIN', 'System Volume Information'}
        
        for root, dirs, files in os.walk(self.root_path):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file.lower() == "desktop.ini" or file.lower() == "thumbs.db":
                    continue
                    
                file_path = Path(root) / file
                
                try:
                    # Basic attributes
                    stat = file_path.stat()
                    file_size = stat.st_size
                    
                    # Create File Entity
                    entity = {
                        "id": self.generate_id(file_path),
                        "path": str(file_path),
                        "name": file,
                        "extension": file_path.suffix.lower(),
                        "size_bytes": file_size,
                        "dna": self.get_temporal_dna(file_path),
                        "tags": self.get_semantic_tags(file_path),
                        "mime": mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                    }
                    
                    self.index["files"].append(entity)
                    
                    file_count += 1
                    total_size += file_size
                    
                    if file_count % 1000 == 0:
                        logger.info(f"Mined {file_count} files...")
                        
                except Exception as e:
                    logger.warning(f"Failed to mine {file_path}: {e}")

        duration = time.time() - start_time
        
        # Update run stats
        self.index["metadata"]["total_files"] = file_count
        self.index["metadata"]["total_size_bytes"] = total_size
        self.index["metadata"]["duration_seconds"] = duration
        
        logger.info(f"Mining complete. {file_count} files in {duration:.2f}s")

    def save(self):
        """Saves the index to JSON."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
        logger.info(f"Fabric Index saved to {self.output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Data Fabric Content Miner")
    parser.add_argument("--root", required=True, help="Root directory to mine")
    parser.add_argument("--output", default="docs/fabric_index.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    miner = ContentMiner(args.root, args.output)
    miner.scan()
    miner.save()
