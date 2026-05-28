#!/usr/bin/env python3
"""
Kiro History Aggregator

Scans ALL Kiro data sources and consolidates them into a single
historical database for analysis.

Data Sources:
1. ~/Library/Application Support/Kiro/User/globalStorage/kiro.kiroagent/**/*.chat - Session files (JSON)
2. ~/Library/Application Support/Kiro/logs/ - Session logs (timestamped folders)
3. ~/.kiro/settings/cli.json - CLI settings
4. ~/.kiro/powers/registry.json - Powers/plugins registry
5. ~/.kiro/.cli_bash_history - CLI command history

Output: ~/.claude/skills/llms-dashboard/data/kiro_history.json
"""

import os
import json
import glob
import sqlite3
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

# =============================================================================
# DATA SOURCE PATHS
# =============================================================================

KIRO_APP_SUPPORT = Path.home() / "Library" / "Application Support" / "Kiro"
KIRO_AGENT_DIR = KIRO_APP_SUPPORT / "User" / "globalStorage" / "kiro.kiroagent"
KIRO_LOGS_DIR = KIRO_APP_SUPPORT / "logs"
KIRO_DOT_DIR = Path.home() / ".kiro"
KIRO_CLI_SETTINGS = KIRO_DOT_DIR / "settings" / "cli.json"
KIRO_POWERS_REGISTRY = KIRO_DOT_DIR / "powers" / "registry.json"
KIRO_CLI_HISTORY = KIRO_DOT_DIR / ".cli_bash_history"
KIRO_CLI_SQLITE = Path.home() / "Library" / "Application Support" / "kiro-cli" / "data.sqlite3"

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "kiro_history.json"


# =============================================================================
# CHAT FILE PARSER
# =============================================================================

def parse_chat_file(file_path):
    """Parse a .chat JSON file and extract session data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        execution_id = data.get('executionId', '')
        action_id = data.get('actionId', 'unknown')
        metadata = data.get('metadata', {})
        chat = data.get('chat', [])
        context = data.get('context', [])
        
        # Extract timestamps
        start_time = metadata.get('startTime', 0)
        end_time = metadata.get('endTime', 0)
        
        # Calculate duration
        if start_time and end_time:
            duration_ms = end_time - start_time
        else:
            duration_ms = 0
        
        # Count messages by role
        human_messages = sum(1 for m in chat if m.get('role') == 'human')
        bot_messages = sum(1 for m in chat if m.get('role') == 'bot')
        tool_messages = sum(1 for m in chat if m.get('role') == 'tool')
        
        # Estimate tokens (rough: 4 chars per token)
        total_chars = sum(len(m.get('content', '')) for m in chat)
        estimated_tokens = total_chars // 4
        
        # Extract context types used
        context_types = [c.get('type', 'unknown') for c in context]
        
        # Get workflow info
        workflow = metadata.get('workflow', 'unknown')
        workflow_id = metadata.get('workflowId', '')
        model_id = metadata.get('modelId', 'auto')
        model_provider = metadata.get('modelProvider', 'unknown')
        
        # Parse workspace from file path
        # Format: /path/kiro.kiroagent/<workspace_hash>/<chat_id>.chat
        parts = str(file_path).split('/')
        workspace_hash = 'unknown'
        for i, part in enumerate(parts):
            if part == 'kiro.kiroagent' and i + 1 < len(parts):
                workspace_hash = parts[i + 1]
                break
        
        # Convert timestamps to ISO format
        start_time_iso = None
        if start_time:
            try:
                start_time_iso = datetime.fromtimestamp(start_time / 1000, tz=timezone.utc).isoformat()
            except (ValueError, OSError):
                pass
        
        return {
            'executionId': execution_id,
            'actionId': action_id,
            'workflow': workflow,
            'workflowId': workflow_id,
            'modelId': model_id,
            'modelProvider': model_provider,
            'workspaceHash': workspace_hash,
            'startTime': start_time_iso,
            'startTimeMs': start_time,
            'endTimeMs': end_time,
            'durationMs': duration_ms,
            'humanMessages': human_messages,
            'botMessages': bot_messages,
            'toolMessages': tool_messages,
            'totalMessages': len(chat),
            'estimatedTokens': estimated_tokens,
            'contextTypes': context_types,
            'filePath': str(file_path),
        }
    
    except Exception as e:
        print(f"  Error parsing {file_path}: {e}")
        return None


def scan_chat_files():
    """Scan all .chat files in the kiro.kiroagent directory"""
    sessions = []
    
    if not KIRO_AGENT_DIR.exists():
        print(f"  ⚠️  Kiro agent directory not found: {KIRO_AGENT_DIR}")
        return sessions
    
    # Find all .chat files
    search_pattern = str(KIRO_AGENT_DIR / "**" / "*.chat")
    chat_files = glob.glob(search_pattern, recursive=True)
    print(f"  📁 Found {len(chat_files)} .chat files")
    
    for file_path in chat_files:
        session = parse_chat_file(file_path)
        if session:
            sessions.append(session)
    
    return sessions


# =============================================================================
# LOG SESSIONS PARSER
# =============================================================================

def scan_log_sessions():
    """Scan Kiro log directories for session info"""
    log_sessions = []
    
    if not KIRO_LOGS_DIR.exists():
        print(f"  ⚠️  Kiro logs directory not found: {KIRO_LOGS_DIR}")
        return log_sessions
    
    log_folders = [d for d in KIRO_LOGS_DIR.iterdir() if d.is_dir()]
    print(f"  📁 Found {len(log_folders)} log session folders")
    
    for folder in log_folders:
        try:
            # Parse start time from folder name (format: YYYYMMDDTHHMMSS)
            folder_name = folder.name
            if len(folder_name) >= 15 and 'T' in folder_name:
                ts_str = folder_name[:15]
                start_time = datetime.strptime(ts_str, "%Y%m%dT%H%M%S")
                
                # Count window folders (indicates multiple projects open)
                window_folders = list(folder.glob("window*"))
                window_count = len(window_folders)
                
                # Find the latest file modification to estimate end time
                max_mtime = 0
                for root, dirs, files in os.walk(folder):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            mtime = os.path.getmtime(fp)
                            if mtime > max_mtime:
                                max_mtime = mtime
                        except OSError:
                            pass
                
                if max_mtime > 0:
                    end_time = datetime.fromtimestamp(max_mtime)
                    duration_seconds = (end_time - start_time).total_seconds()
                else:
                    duration_seconds = 0
                
                log_sessions.append({
                    'id': folder_name,
                    'startTime': start_time.isoformat(),
                    'durationSeconds': max(0, duration_seconds),
                    'windowCount': window_count,
                })
        except Exception as e:
            pass
    
    return log_sessions


# =============================================================================
# CLI HISTORY PARSER
# =============================================================================

def scan_cli_history():
    """Scan CLI command history"""
    commands = []
    
    if not KIRO_CLI_HISTORY.exists():
        print(f"  ⚠️  CLI history not found: {KIRO_CLI_HISTORY}")
        return {'commands': [], 'total': 0}
    
    try:
        with open(KIRO_CLI_HISTORY, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # First line is version marker like "#V2"
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                commands.append(line)
        
        print(f"  ✅ Loaded {len(commands)} CLI commands from history")
    except Exception as e:
        print(f"  ❌ Error loading CLI history: {e}")
    
    return {
        'commands': commands,
        'total': len(commands)
    }


# =============================================================================
# SETTINGS & POWERS PARSER
# =============================================================================

def load_cli_settings():
    """Load CLI settings"""
    if not KIRO_CLI_SETTINGS.exists():
        return {}
    
    try:
        with open(KIRO_CLI_SETTINGS, 'r') as f:
            return json.load(f)
    except:
        return {}


def load_powers_registry():
    """Load powers registry"""
    if not KIRO_POWERS_REGISTRY.exists():
        return {}
    
    try:
        with open(KIRO_POWERS_REGISTRY, 'r') as f:
            data = json.load(f)
        
        powers = data.get('powers', {})
        installed = [name for name, info in powers.items() if info.get('installed', False)]
        available = list(powers.keys())
        
        return {
            'installed': installed,
            'available': available,
            'installedCount': len(installed),
            'availableCount': len(available),
            'lastUpdated': data.get('lastUpdated')
        }
    except:
        return {}


# =============================================================================
# KIRO CLI SQLITE DATABASE PARSER
# =============================================================================

def scan_cli_sqlite():
    """Scan Kiro CLI SQLite database for conversation data"""
    cli_data = {
        'total_conversations': 0,
        'total_requests': 0,
        'models': defaultdict(int),
        'daily_stats': defaultdict(lambda: {'requests': 0, 'models': defaultdict(int)}),
    }
    
    if not KIRO_CLI_SQLITE.exists():
        print(f"  ⚠️  Kiro CLI SQLite not found: {KIRO_CLI_SQLITE}")
        return cli_data
    
    try:
        conn = sqlite3.connect(str(KIRO_CLI_SQLITE))
        cur = conn.cursor()
        
        # Get all conversations
        cur.execute('SELECT key, conversation_id, value, created_at FROM conversations_v2')
        
        for row in cur.fetchall():
            key, conv_id, value, created_at = row
            cli_data['total_conversations'] += 1
            
            try:
                data = json.loads(value)
                history = data.get('history', [])
                
                # Get date for daily stats
                dt = datetime.fromtimestamp(created_at / 1000)
                date_str = dt.strftime('%Y-%m-%d')
                
                for msg in history:
                    meta = msg.get('request_metadata', {})
                    if meta.get('request_id'):
                        cli_data['total_requests'] += 1
                        model_id = meta.get('model_id', 'auto')
                        cli_data['models'][model_id] += 1
                        cli_data['daily_stats'][date_str]['requests'] += 1
                        cli_data['daily_stats'][date_str]['models'][model_id] += 1
            except:
                pass
        
        conn.close()
        
        # Convert defaultdicts for output
        cli_data['models'] = dict(cli_data['models'])
        daily_list = []
        for d in sorted(cli_data['daily_stats'].keys()):
            daily_list.append({
                'date': d,
                'requests': cli_data['daily_stats'][d]['requests'],
                'models': dict(cli_data['daily_stats'][d]['models'])
            })
        cli_data['daily_stats'] = daily_list
        
        print(f"  ✅ Found {cli_data['total_conversations']} CLI conversations, {cli_data['total_requests']} requests")
        
    except Exception as e:
        print(f"  ❌ Error reading CLI SQLite: {e}")
    
    return cli_data


# =============================================================================
# MAIN AGGREGATION
# =============================================================================

def main():
    print("=" * 60)
    print("🔍 Kiro History Aggregator")
    print("=" * 60)
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Scan chat files
    print("📊 Scanning chat sessions...")
    sessions = scan_chat_files()
    print(f"  ✅ Processed {len(sessions)} chat sessions")
    
    # Sort by start time
    sessions.sort(key=lambda x: x.get('startTimeMs', 0), reverse=True)
    
    # 2. Scan log sessions
    print("\n📁 Scanning log sessions...")
    log_sessions = scan_log_sessions()
    
    # 3. Scan CLI history
    print("\n📜 Scanning CLI history...")
    cli_history = scan_cli_history()
    
    # 4. Load settings
    print("\n⚙️  Loading settings...")
    cli_settings = load_cli_settings()
    powers = load_powers_registry()
    
    # 5. Scan CLI SQLite database
    print("\n🗄️  Scanning CLI SQLite database...")
    cli_sqlite = scan_cli_sqlite()
    
    # 6. Calculate aggregates
    total_sessions = len(sessions)
    total_duration_ms = sum(s.get('durationMs', 0) for s in sessions)
    total_messages = sum(s.get('totalMessages', 0) for s in sessions)
    total_human_messages = sum(s.get('humanMessages', 0) for s in sessions)
    total_bot_messages = sum(s.get('botMessages', 0) for s in sessions)
    total_tool_messages = sum(s.get('toolMessages', 0) for s in sessions)
    total_estimated_tokens = sum(s.get('estimatedTokens', 0) for s in sessions)
    
    # Workflow breakdown
    workflows = defaultdict(int)
    for s in sessions:
        workflows[s.get('workflow', 'unknown')] += 1
    
    # Action breakdown
    actions = defaultdict(int)
    for s in sessions:
        actions[s.get('actionId', 'unknown')] += 1
    
    # Model breakdown
    models = defaultdict(int)
    for s in sessions:
        models[s.get('modelId', 'unknown')] += 1
    
    # Workspace breakdown
    workspaces = defaultdict(lambda: {'sessions': 0, 'messages': 0, 'duration': 0})
    for s in sessions:
        ws = s.get('workspaceHash', 'unknown')
        workspaces[ws]['sessions'] += 1
        workspaces[ws]['messages'] += s.get('totalMessages', 0)
        workspaces[ws]['duration'] += s.get('durationMs', 0)
    
    # Context types usage
    context_types = defaultdict(int)
    for s in sessions:
        for ct in s.get('contextTypes', []):
            context_types[ct] += 1
    
    # Daily stats
    daily_stats = defaultdict(lambda: {
        'date': None,
        'sessions': 0,
        'messages': 0,
        'humanMessages': 0,
        'botMessages': 0,
        'toolMessages': 0,
        'durationMs': 0,
        'tokens': 0,
        'models': defaultdict(int),
    })
    
    for s in sessions:
        start_time = s.get('startTime')
        if start_time:
            date = start_time[:10]
            daily_stats[date]['date'] = date
            daily_stats[date]['sessions'] += 1
            daily_stats[date]['messages'] += s.get('totalMessages', 0)
            daily_stats[date]['humanMessages'] += s.get('humanMessages', 0)
            daily_stats[date]['botMessages'] += s.get('botMessages', 0)
            daily_stats[date]['toolMessages'] += s.get('toolMessages', 0)
            daily_stats[date]['durationMs'] += s.get('durationMs', 0)
            daily_stats[date]['tokens'] += s.get('estimatedTokens', 0)
            model_id = s.get('modelId', 'unknown')
            daily_stats[date]['models'][model_id] += 1
    
    # Convert defaultdicts to regular dicts for JSON serialization
    daily_list = []
    for d in sorted(daily_stats.keys()):
        day_data = dict(daily_stats[d])
        day_data['models'] = dict(day_data['models'])
        daily_list.append(day_data)
    
    # Build output
    output = {
        'generated_at': datetime.now().isoformat(),
        'data_sources': {
            'chat_files': KIRO_AGENT_DIR.exists(),
            'log_sessions': KIRO_LOGS_DIR.exists(),
            'cli_history': KIRO_CLI_HISTORY.exists(),
            'cli_settings': KIRO_CLI_SETTINGS.exists(),
            'powers_registry': KIRO_POWERS_REGISTRY.exists(),
        },
        
        'summary': {
            'total_sessions': total_sessions,
            'total_duration_ms': total_duration_ms,
            'total_duration_hours': round(total_duration_ms / 1000 / 3600, 2),
            'total_messages': total_messages,
            'total_human_messages': total_human_messages,
            'total_bot_messages': total_bot_messages,
            'total_tool_messages': total_tool_messages,
            'total_estimated_tokens': total_estimated_tokens,
            'unique_workspaces': len(workspaces),
            'log_sessions': len(log_sessions),
            'cli_commands': cli_history['total'],
            'date_range': {
                'first': daily_list[0]['date'] if daily_list else None,
                'last': daily_list[-1]['date'] if daily_list else None,
                'days_active': len(daily_list),
            }
        },
        
        'settings': cli_settings,
        'powers': powers,
        'cli_history': cli_history,
        'cli_sqlite': cli_sqlite,
        'log_sessions': log_sessions,
        
        'workflows': dict(workflows),
        'actions': dict(actions),
        'models': dict(models),
        'context_types': dict(context_types),
        'workspaces': dict(workspaces),
        
        'daily_stats': daily_list,
        'sessions': sessions,
    }
    
    # Write output
    print(f"\n💾 Writing data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 AGGREGATION SUMMARY")
    print("=" * 60)
    
    print(f"\n📦 Data Sources:")
    print(f"   {'✅' if sessions else '❌'} IDE sessions: {len(sessions)}")
    print(f"   {'✅' if cli_sqlite.get('total_requests') else '❌'} CLI requests: {cli_sqlite.get('total_requests', 0)}")
    print(f"   {'✅' if log_sessions else '❌'} Log sessions: {len(log_sessions)}")
    print(f"   {'✅' if cli_history['total'] else '❌'} CLI commands: {cli_history['total']}")
    print(f"   {'✅' if cli_settings else '❌'} CLI settings loaded")
    print(f"   {'✅' if powers else '❌'} Powers: {powers.get('installedCount', 0)} installed, {powers.get('availableCount', 0)} available")
    
    print(f"\n📊 Session Stats:")
    print(f"   Total sessions: {total_sessions}")
    print(f"   Total duration: {total_duration_ms / 1000 / 3600:.1f} hours")
    print(f"   Total messages: {total_messages:,}")
    print(f"   Estimated tokens: {total_estimated_tokens:,}")
    print(f"   Unique workspaces: {len(workspaces)}")
    
    if workflows:
        print(f"\n⚡ Workflows:")
        for wf, count in sorted(workflows.items(), key=lambda x: -x[1])[:5]:
            print(f"   {wf}: {count}")
    
    if context_types:
        print(f"\n📎 Context Types (Top 5):")
        for ct, count in sorted(context_types.items(), key=lambda x: -x[1])[:5]:
            print(f"   {ct}: {count}")
    
    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✅ Data saved to: {OUTPUT_FILE}")
    print(f"   File size: {file_size:.1f} KB")


if __name__ == "__main__":
    main()
