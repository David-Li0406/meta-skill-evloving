
"""
Virtual Gallery Generator (Phase 1: Lightweight Museum)
Generates a premium, dark-mode HTML portfolio from the Fabric Index.
Designed to be the efficient precursor to the future 3D NFT Museum.
"""

import json
import os
import random
from pathlib import Path
from datetime import datetime
import structlog

log = structlog.get_logger()

# HTML TEMPLATE (Embedded for single-file portability)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity Museum | Proof of Work</title>
    <style>
        :root {
            --bg-color: #0a0a0a;
            --card-bg: #161616;
            --accent: #00f3ff; /* Neon Cyan */
            --text-main: #e0e0e0;
            --text-dim: #888;
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }

        /* HERO SECTION */
        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
            text-align: center;
            position: relative;
        }

        .hero h1 {
            font-size: 5rem;
            margin: 0;
            background: linear-gradient(135deg, #fff 0%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -2px;
        }

        .hero p {
            font-size: 1.5rem;
            color: var(--text-dim);
            max-width: 600px;
            margin-top: 1rem;
        }

        .stats-bar {
            margin-top: 3rem;
            display: flex;
            gap: 3rem;
        }

        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .stat-val { font-size: 2rem; font-weight: bold; color: var(--accent); }
        .stat-lbl { font-size: 0.9rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }

        /* GALLERY GRID */
        .section-title {
            font-size: 2rem;
            margin: 4rem 2rem 2rem;
            border-left: 4px solid var(--accent);
            padding-left: 1rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #222;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            position: relative;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 243, 255, 0.1);
            border-color: var(--accent);
        }

        .card-media-placeholder {
            height: 200px;
            background: #222;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #444;
            font-size: 3rem;
        }
        
        .card-img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }

        .card-info {
            padding: 1.5rem;
        }

        .card-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .card-meta {
            font-size: 0.85rem;
            color: var(--text-dim);
            display: flex;
            justify-content: space-between;
        }

        .badge {
            background: rgba(0, 243, 255, 0.1);
            color: var(--accent);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
        }

        /* NFT FUTURE NOTICE */
        .nft-notice {
            text-align: center;
            padding: 4rem;
            background: #111;
            margin-top: 4rem;
            border-top: 1px solid #333;
        }
        
        .nft-notice h3 { color: var(--accent); }

    </style>
</head>
<body>

    <div class="hero">
        <h1>VIRTUAL GALLERY</h1>
        <p>Strategic Archive & Proof of Work</p>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-val" id="total-assets">0</div>
                <div class="stat-lbl">Assets Preserved</div>
            </div>
            <div class="stat-item">
                <div class="stat-val" id="total-size">0 GB</div>
                <div class="stat-lbl">Digital Weight</div>
            </div>
             <div class="stat-item">
                <div class="stat-val">PHASE 1</div>
                <div class="stat-lbl">Status</div>
            </div>
        </div>
    </div>

    <div id="content-area">
        <!-- Content injected here -->
    </div>

    <div class="nft-notice">
        <h3>FUTURE ARCHITECTURE READY</h3>
        <p>This lightweight gallery is the seed for the upcoming 3D NFT Museum.</p>
        <p>Metadata structure is compatible with future tokenization standards.</p>
    </div>

    <script>
        // Data injected from Python
        const GALLERY_DATA = {{data_payload}};

        function formatSize(bytes) {
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            if (bytes === 0) return '0 Byte';
            const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
            return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
        }

        // Init Header
        document.getElementById('total-assets').innerText = GALLERY_DATA.stats.total_files.toLocaleString();
        document.getElementById('total-size').innerText = formatSize(GALLERY_DATA.stats.total_size);

        const contentArea = document.getElementById('content-area');

        // CATEGORY: HEAVYWEIGHTS (Largest Files)
        if (GALLERY_DATA.heavyweights.length > 0) {
            const section = document.createElement('div');
            section.innerHTML = `<div class="section-title">ðŸ’Ž Heavyweights (Top Assets)</div>`;
            const grid = document.createElement('div');
            grid.className = 'grid';
            
            GALLERY_DATA.heavyweights.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => alert('Asset Path: ' + item.path); // Placeholder for opening
                
                // Simple icon based on type
                let icon = 'ðŸ“ƒ';
                if (item.mime.includes('video')) icon = 'ðŸŽ¬';
                if (item.mime.includes('image')) icon = 'ðŸ–¼';
                if (item.mime.includes('zip') || item.mime.includes('compressed')) icon = 'ðŸ“¦';

                card.innerHTML = `
                    <div class="card-media-placeholder">${icon}</div>
                    <div class="card-info">
                        <div class="card-title">${item.name}</div>
                        <div class="card-meta">
                            <span>${formatSize(item.size_bytes)}</span>
                            <span class="badge">${item.extension}</span>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
            section.appendChild(grid);
            contentArea.appendChild(section);
        }

        // CATEGORY: RECENT WORKS (Last Modified)
        // ... (Can expand later)

    </script>
</body>
</html>
"""

class GalleryGenerator:
    def __init__(self, index_path: str, output_path: str):
        self.index_path = Path(index_path)
        self.output_path = Path(output_path)

    def generate(self):
        log.info(f"Loading index from {self.index_path}")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_files = data.get("files", [])
        
        # 1. Sort by Size (Heavyweights)
        sorted_by_size = sorted(all_files, key=lambda x: x.get("size_bytes", 0), reverse=True)
        top_20_heavy = sorted_by_size[:20]

        # 2. Stats
        total_size = sum(f.get("size_bytes", 0) for f in all_files)
        
        # Prepare Payload
        payload = {
            "stats": {
                "total_files": len(all_files),
                "total_size": total_size
            },
            "heavyweights": top_20_heavy
            # Add timeline data later
        }

        # Inject into HTML
        html_content = HTML_TEMPLATE.replace("{{data_payload}}", json.dumps(payload))

        # Write
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        log.info(f"Gallery generated at {self.output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="docs/fabric_index.json")
    parser.add_argument("--output", default="docs/gallery/index.html")
    args = parser.parse_args()

    gen = GalleryGenerator(args.index, args.output)
    gen.generate()
