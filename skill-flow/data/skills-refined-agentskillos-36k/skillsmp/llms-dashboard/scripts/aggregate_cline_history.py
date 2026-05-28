#!/usr/bin/env python3
"""Cline History Aggregator - Scans Cline/amzn-cline task data from VS Code"""

import os, json, glob
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

CLINE_DIR = Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "asbx.amzn-cline"
TASK_HISTORY = CLINE_DIR / "state" / "taskHistory.json"
TASKS_DIR = CLINE_DIR / "tasks"
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "cline_history.json"

def load_model_usage_from_tasks():
    """Load model usage data from individual task_metadata.json files"""
    model_usage = []
    if not TASKS_DIR.exists():
        return model_usage
    
    for task_dir in TASKS_DIR.iterdir():
        if task_dir.is_dir():
            meta_file = task_dir / "task_metadata.json"
            if meta_file.exists():
                try:
                    with open(meta_file, 'r') as f:
                        data = json.load(f)
                    usage = data.get('model_usage', [])
                    if isinstance(usage, list):
                        for u in usage:
                            u['task_id'] = task_dir.name
                            model_usage.append(u)
                except:
                    pass
    return model_usage

def main():
    print("=" * 60)
    print("🔍 Cline History Aggregator")
    print("=" * 60)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not TASK_HISTORY.exists():
        print(f"❌ Task history not found: {TASK_HISTORY}")
        return
    
    with open(TASK_HISTORY, 'r') as f:
        tasks = json.load(f)
    
    print(f"✅ Loaded {len(tasks)} tasks")
    
    # Load model usage from task metadata
    print("📊 Scanning task metadata for model usage...")
    model_usage_list = load_model_usage_from_tasks()
    print(f"  ✅ Found {len(model_usage_list)} model usage records")
    
    total_cost = sum(t.get('totalCost', 0) for t in tasks)
    total_tokens_in = sum(t.get('tokensIn', 0) for t in tasks)
    total_tokens_out = sum(t.get('tokensOut', 0) for t in tasks)
    total_cache_writes = sum(t.get('cacheWrites', 0) for t in tasks)
    total_cache_reads = sum(t.get('cacheReads', 0) for t in tasks)
    
    daily_stats = defaultdict(lambda: {'date': None, 'tasks': 0, 'cost': 0, 'tokensIn': 0, 'tokensOut': 0, 'models': defaultdict(int)})
    workspaces = defaultdict(lambda: {'tasks': 0, 'cost': 0})
    models = defaultdict(int)
    
    # Build task ID to date mapping
    task_dates = {}
    for t in tasks:
        ts = t.get('ts', 0)
        task_id = str(t.get('id', ''))
        if ts:
            date = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
            task_dates[task_id] = date
            daily_stats[date]['date'] = date
            daily_stats[date]['tasks'] += 1
            daily_stats[date]['cost'] += t.get('totalCost', 0)
            daily_stats[date]['tokensIn'] += t.get('tokensIn', 0)
            daily_stats[date]['tokensOut'] += t.get('tokensOut', 0)
        
        ws = t.get('cwdOnTaskInitialization', 'unknown')
        ws_short = ws.split('/')[-1] if ws else 'unknown'
        workspaces[ws_short]['tasks'] += 1
        workspaces[ws_short]['cost'] += t.get('totalCost', 0)
    
    # Process model usage
    for mu in model_usage_list:
        model_id = mu.get('model_id', 'unknown')
        # Simplify model name
        model_short = model_id.split('/')[-1] if '/' in model_id else model_id
        model_short = model_short.replace('anthropic.', '').replace('-v1:0', '')
        models[model_short] += 1
        
        # Try to get date from task or timestamp
        ts = mu.get('ts', 0)
        if ts:
            date = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
            if date in daily_stats:
                daily_stats[date]['models'][model_short] += 1
    
    # Convert defaultdicts for JSON serialization
    daily_list = []
    for d in sorted(daily_stats.keys()):
        day_data = dict(daily_stats[d])
        day_data['models'] = dict(day_data['models'])
        daily_list.append(day_data)
    
    workspace_list = [{'name': k, **v} for k, v in sorted(workspaces.items(), key=lambda x: -x[1]['tasks'])[:15]]
    
    sessions = [{'id': t.get('id'), 'task': t.get('task', '')[:100], 'ts': t.get('ts'), 
                 'tokensIn': t.get('tokensIn', 0), 'tokensOut': t.get('tokensOut', 0),
                 'cost': t.get('totalCost', 0), 'cwd': t.get('cwdOnTaskInitialization', '')} 
                for t in sorted(tasks, key=lambda x: x.get('ts', 0), reverse=True)]
    
    output = {
        'generated_at': datetime.now().isoformat(),
        'summary': {'total_tasks': len(tasks), 'total_cost': round(total_cost, 2), 
                    'total_tokens_in': total_tokens_in, 'total_tokens_out': total_tokens_out,
                    'total_cache_writes': total_cache_writes, 'total_cache_reads': total_cache_reads,
                    'unique_workspaces': len(workspaces), 'model_switches': len(model_usage_list)},
        'models': dict(models),
        'daily_stats': daily_list, 'workspaces': workspace_list, 'sessions': sessions[:50]
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Summary: {len(tasks)} tasks, ${total_cost:.2f} cost, {total_tokens_in + total_tokens_out:,} tokens")
    if models:
        print(f"🤖 Models used: {', '.join(f'{k}({v})' for k, v in sorted(models.items(), key=lambda x: -x[1])[:5])}")
    print(f"✅ Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
