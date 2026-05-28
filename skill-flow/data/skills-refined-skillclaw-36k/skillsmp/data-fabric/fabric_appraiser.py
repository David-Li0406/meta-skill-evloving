"""
Fabric Appraiser - Data Fabric Phase 2
Analyzes the Knowledge Graph (JSON) to discover patterns, clusters, and timelines.
Generates 'docs/discovery_report.md'.
"""

import json
import logging
import datetime
from pathlib import Path
from collections import Counter, defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FabricAppraiser:
    def __init__(self, index_file: str, report_file: str):
        self.index_file = Path(index_file)
        self.report_file = Path(report_file)
        self.data = None

    def load(self):
        """Loads the JSON index."""
        logger.info(f"Loading index from {self.index_file}...")
        with open(self.index_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        logger.info(f"Loaded {len(self.data.get('files', []))} files.")

    def analyze(self):
        """Performs deep analysis on the data."""
        if not self.data:
            return

        files = self.data.get('files', [])
        
        # 1. Timeline Analysis (By Year-Month)
        timeline = Counter()
        for f in files:
            m_time = f.get('dna', {}).get('modified')
            if m_time:
                ym = m_time[:7] # YYYY-MM
                timeline[ym] += 1
        
        # 2. Type Analysis
        extensions = Counter(f.get('extension', 'unknown') for f in files)
        
        # 3. Tag Clusters (Project Contexts)
        tag_clusters = Counter()
        for f in files:
            for tag in f.get('tags', []):
                if tag.startswith('.'): continue # Skip extensions
                if tag.startswith('year:'): continue # Skip year tags
                tag_clusters[tag] += 1
                
        # 4. Size Analysis (Big Cats)
        files.sort(key=lambda x: x.get('size_bytes', 0), reverse=True)
        top_files = files[:20]
        
        # 5. Potential "Collections" (Top Tags with significant file counts)
        collections = {tag: count for tag, count in tag_clusters.most_common(20) if count > 10}

        self.generate_report(timeline, extensions, tag_clusters, top_files, collections)

    def generate_report(self, timeline, extensions, tag_clusters, top_files, collections):
        """Generates the Markdown report."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md = f"# ðŸ”­ Discovery Report: The Data Fabric\n"
        md += f"**Generated**: {timestamp}\n"
        md += f"**Source**: `{self.data['metadata']['root_path']}`\n"
        md += f"**Total Files**: {self.data['metadata']['total_files']:,}\n"
        md += f"**Total Size**: {self.data['metadata']['total_size_bytes'] / (1024**3):.2f} GB\n\n"
        
        md += "## 1. ðŸ•° The Timeline (Productivity Pulse)\n"
        md += "When was the work done?\n\n| Period | Activity (Files) |\n|---|---|\n"
        for ym, count in sorted(timeline.items(), reverse=True)[:12]:
             md += f"| **{ym}** | {count} |\n"
        
        md += "\n## 2. ðŸŒŸ Suggested Collections (Virtual Folders)\n"
        md += "Based on your directory structure and file clusters, here are potential 'Albums':\n\n"
        for tag, count in collections.items():
            md += f"- **{tag}**: {count} assets\n"

        md += "\n## 3. ðŸ“‚ File Composition\n"
        md += "| Type | Count | Description |\n|---|---|---|\n"
        for ext, count in extensions.most_common(10):
            desc = self.get_ext_desc(ext)
            md += f"| `{ext}` | {count} | {desc} |\n"

        md += "\n## 4. ðŸ’Ž Hidden Gems (Largest/Most Complex)\n"
        for f in top_files[:10]:
            size_mb = f['size_bytes'] / (1024*1024)
            md += f"- `{f['name']}` ({size_mb:.2f} MB) - *{f['path']}*\n"
            
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        logger.info(f"Discovery Report saved to {self.report_file}")

    def get_ext_desc(self, ext):
        known = {
            '.jpg': 'Image', '.png': 'Image', '.mp4': 'Video', '.pdf': 'Document', 
            '.py': 'Python Source', '.js': 'JavaScript', '.json': 'Data', 
            '.md': 'Markdown', '.txt': 'Text', '.zip': 'Archive',
            '.psd': 'Photoshop', '.ai': 'Illustrator', '.stl': '3D Model'
        }
        return known.get(ext, 'Unknown')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fabric Appraiser")
    parser.add_argument("--index", default="docs/fabric_index.json", help="Input Index JSON")
    parser.add_argument("--output", default="docs/discovery_report.md", help="Output Report MD")
    
    args = parser.parse_args()
    
    appraiser = FabricAppraiser(args.index, args.output)
    appraiser.load()
    appraiser.analyze()
