#!/usr/bin/env python3
"""
VS Code Dashboard Generator

Reads aggregated VS Code data and generates a full HTML dashboard.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import sys

# Constants
DATA_FILE = Path(__file__).parent.parent / "data" / "vscode_data.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "vscode_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "vscode_dashboard.html"

def load_data():
    """Load aggregated data"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Run aggregate_vscode_data.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {DATA_FILE}: {e}")
        sys.exit(1)

def format_duration(seconds):
    """Format seconds to human readable duration"""
    if not seconds:
        return '0s'
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {int(seconds % 60)}s"
    else:
        return f"{int(seconds)}s"

def generate_dashboard():
    data = load_data()
    sessions = data.get('sessions', [])
    extensions = data.get('extensions', [])
    projects = data.get('projects', [])
    
    # Calculate totals
    total_sessions = len(sessions)
    total_duration_seconds = sum(s.get('durationSeconds', 0) for s in sessions)
    total_extensions = len(extensions)
    total_projects = len(projects)
    
    publishers = [e.get('publisher') for e in extensions if e.get('publisher')]
    unique_publishers = len(set(publishers))
    
    # Project Stats
    project_parents = [p.get('parent') for p in projects if p.get('parent')]
    # Clean up parents to be more readable (e.g. /Users/you/Documents -> ~/Documents)
    home_dir = str(Path.home())
    clean_parents = []
    for p in project_parents:
        if p.startswith(home_dir):
            clean_parents.append(p.replace(home_dir, '~'))
        else:
            clean_parents.append(p)
            
    parent_counts = Counter(clean_parents)
    top_parents = parent_counts.most_common(8)
    chart_proj_labels = [p[0] for p in top_parents]
    chart_proj_counts = [p[1] for p in top_parents]
    
    # Prepare chart data (daily aggregation)
    daily_stats = defaultdict(lambda: {'sessions': 0, 'durations': []})
    
    for s in sessions:
        start_time = s.get('startTime')
        if start_time:
            date_str = start_time.split('T')[0]
            daily_stats[date_str]['sessions'] += 1
            # Convert to minutes
            daily_stats[date_str]['durations'].append(s.get('durationSeconds', 0) / 60)
            
    sorted_dates = sorted(daily_stats.keys())
    chart_sessions = [daily_stats[d]['sessions'] for d in sorted_dates]
    chart_durations = [daily_stats[d]['durations'] for d in sorted_dates]
    
    # Calculate Y-Axis Max for Boxplot
    all_durations = []
    for d_list in chart_durations:
        all_durations.extend(d_list)
    
    if all_durations:
        # Use max value to ensure nothing is cut off, as requested
        y_axis_max = max(all_durations)
        y_axis_max = int(y_axis_max * 1.1) # 10% padding
        y_axis_max = max(y_axis_max, 10)
    else:
        y_axis_max = 60

    # Publisher Stats
    pub_counts = Counter(publishers)
    top_publishers = pub_counts.most_common(10)
    chart_pub_labels = [p[0] for p in top_publishers]
    chart_pub_counts = [p[1] for p in top_publishers]
    
    # Generate Projects Rows
    projects_rows = ""
    # Sort by name
    sorted_projects = sorted(projects, key=lambda x: x.get('name', '').lower())
    
    for p in sorted_projects:
        name = p.get('name', 'Unknown')
        path = p.get('path', '')
        if path.startswith(home_dir):
            path = path.replace(home_dir, '~')
            
        projects_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3 text-white font-medium">{name}</td>
            <td class="p-3 text-gray-400 text-xs font-mono">{path}</td>
        </tr>
        """
    
    # Generate Recent Sessions Rows
    recent_rows = ""
    for s in sessions[:20]:  # Top 20 recent
        date_str = s.get('startTime', '').replace('T', ' ')
        duration = format_duration(s.get('durationSeconds', 0))
        source = s.get('source', 'Unknown')
        lid = s.get('id', '-')
        
        badge_color = "badge-green" if source == "Insiders" else "badge-blue"
        
        recent_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3"><span class="badge {badge_color}">{source}</span></td>
            <td class="p-3 text-gray-300">{date_str}</td>
            <td class="p-3 text-gray-400">{duration}</td>
            <td class="p-3 text-gray-500 text-xs font-mono">{lid}</td>
        </tr>
        """

    # Generate Extensions Rows
    extensions_rows = ""
    # Sort extensions by name
    sorted_extensions = sorted(extensions, key=lambda x: x.get('name', '').lower())
    
    for ext in sorted_extensions:
        name = ext.get('name', 'Unknown')
        publisher = ext.get('publisher', 'Unknown')
        version = ext.get('version', '-')
        source = ext.get('source', 'Unknown')
        
        badge_color = "badge-green" if source == "Insiders" else "badge-blue"
        
        extensions_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3 text-white font-medium">{name}</td>
            <td class="p-3 text-gray-400">{publisher}</td>
            <td class="p-3 text-gray-500 text-xs">{version}</td>
            <td class="p-3"><span class="badge {badge_color}">{source}</span></td>
        </tr>
        """

    # Read Template
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: {TEMPLATE_FILE} not found")
        sys.exit(1)

    # Replace Placeholders
    html = template.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    html = html.replace('{{TOTAL_SESSIONS}}', str(total_sessions))
    html = html.replace('{{TOTAL_DURATION}}', format_duration(total_duration_seconds))
    html = html.replace('{{TOTAL_EXTENSIONS}}', str(total_extensions))
    html = html.replace('{{TOTAL_PROJECTS}}', str(total_projects))
    html = html.replace('{{UNIQUE_PUBLISHERS}}', str(unique_publishers))
    
    html = html.replace('{{CHART_DATES}}', json.dumps(sorted_dates))
    html = html.replace('{{CHART_SESSIONS}}', json.dumps(chart_sessions))
    html = html.replace('{{CHART_DURATIONS}}', json.dumps(chart_durations))
    html = html.replace('{{Y_AXIS_MAX}}', str(y_axis_max))
    
    html = html.replace('{{CHART_PUB_LABELS}}', json.dumps(chart_pub_labels))
    html = html.replace('{{CHART_PUB_COUNTS}}', json.dumps(chart_pub_counts))
    
    html = html.replace('{{CHART_PROJ_LABELS}}', json.dumps(chart_proj_labels))
    html = html.replace('{{CHART_PROJ_COUNTS}}', json.dumps(chart_proj_counts))
    
    html = html.replace('{{RECENT_SESSIONS_ROWS}}', recent_rows)
    html = html.replace('{{EXTENSIONS_ROWS}}', extensions_rows)
    html = html.replace('{{PROJECTS_ROWS}}', projects_rows)

    # Write Output
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html)
        
    print(f"Dashboard generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dashboard()
