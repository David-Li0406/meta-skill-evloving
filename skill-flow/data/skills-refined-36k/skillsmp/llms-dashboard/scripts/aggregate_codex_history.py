#!/usr/bin/env python3
"""
Codex History Aggregator

Scans ALL Codex (OpenAI Codex CLI) data sources and consolidates them into a single
historical database for analysis.

Data Sources:
1. ~/.codex/sessions/**/*.jsonl - Session transcripts (detailed per-message data)
2. ~/.codex/history.jsonl - User command/prompt history
3. ~/.codex/config.toml - Configuration with model, projects, etc.

Output: ~/.claude/skills/llms-dashboard/data/codex_history.json
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

try:
    import tomllib
except ImportError:
    import tomli as tomllib


CODEX_SESSIONS_DIR = Path.home() / ".codex" / "sessions"
HISTORY_FILE = Path.home() / ".codex" / "history.jsonl"
CONFIG_FILE = Path.home() / ".codex" / "config.toml"

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "codex_history.json"


def load_config():
    """Load Codex config.toml"""
    if not CONFIG_FILE.exists():
        print(f"  ⚠️  Config file not found: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'rb') as f:
            data = tomllib.load(f)
        print(f"  ✅ Loaded config.toml (model: {data.get('model', 'unknown')})")
        return data
    except Exception as e:
        print(f"  ❌ Error loading config: {e}")
        return None


def process_config(config):
    """Extract config info"""
    if not config:
        return {}

    projects = config.get('projects', {})
    trusted_projects = [p for p, v in projects.items() if v.get('trust_level') == 'trusted']

    return {
        'model': config.get('model', 'unknown'),
        'model_reasoning_effort': config.get('model_reasoning_effort', 'default'),
        'total_projects': len(projects),
        'trusted_projects': len(trusted_projects),
        'project_paths': list(projects.keys()),
    }


def load_command_history():
    """Load user command/prompt history from history.jsonl"""
    if not HISTORY_FILE.exists():
        print(f"  ⚠️  History file not found: {HISTORY_FILE}")
        return []

    commands = []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    cmd = json.loads(line)
                    commands.append(cmd)
                except json.JSONDecodeError:
                    continue
        print(f"  ✅ Loaded history.jsonl ({len(commands)} commands)")
        return commands
    except Exception as e:
        print(f"  ❌ Error loading history: {e}")
        return []


def process_command_history(commands):
    """Analyze command history patterns"""
    if not commands:
        return {}

    commands_by_date = defaultdict(int)
    commands_by_hour = defaultdict(int)
    sessions_in_history = set()
    prompt_lengths = []

    for cmd in commands:
        text = cmd.get('text', '')
        ts = cmd.get('ts', 0)
        session_id = cmd.get('session_id', '')

        if session_id:
            sessions_in_history.add(session_id)

        if text:
            prompt_lengths.append(len(text))

        if ts:
            try:
                dt = datetime.fromtimestamp(ts)
                date_str = dt.strftime('%Y-%m-%d')
                commands_by_date[date_str] += 1
                commands_by_hour[dt.hour] += 1
            except (ValueError, TypeError, OSError):
                pass

    avg_prompt_length = sum(prompt_lengths) / len(prompt_lengths) if prompt_lengths else 0

    return {
        'total_commands': len(commands),
        'unique_sessions': len(sessions_in_history),
        'commands_by_date': dict(commands_by_date),
        'commands_by_hour': dict(commands_by_hour),
        'avg_prompt_length': round(avg_prompt_length, 1),
        'longest_prompt': max(prompt_lengths) if prompt_lengths else 0,
        'shortest_prompt': min(prompt_lengths) if prompt_lengths else 0,
    }


def parse_session_file(filepath):
    """Parse a single session JSONL file"""
    session_data = {
        'id': None,
        'timestamp': None,
        'cwd': None,
        'cli_version': None,
        'model': None,
        'source': None,
        'messages': [],
        'user_messages': 0,
        'assistant_messages': 0,
        'reasoning_count': 0,
        'function_calls': 0,
        'tool_names': defaultdict(int),
        'input_tokens': 0,
        'output_tokens': 0,
        'cached_tokens': 0,
        'reasoning_tokens': 0,
    }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if not entry or not isinstance(entry, dict):
                        continue
                        
                    entry_type = entry.get('type')
                    payload = entry.get('payload')
                    if payload is None:
                        payload = {}
                    timestamp = entry.get('timestamp')

                    if entry_type == 'session_meta':
                        session_data['id'] = payload.get('id')
                        session_data['timestamp'] = payload.get('timestamp', timestamp)
                        session_data['cwd'] = payload.get('cwd')
                        session_data['cli_version'] = payload.get('cli_version')
                        session_data['source'] = payload.get('source')
                        session_data['model'] = payload.get('model_provider', 'openai')

                    elif entry_type == 'response_item':
                        msg_type = payload.get('type')
                        role = payload.get('role')

                        if msg_type == 'message':
                            if role == 'user':
                                session_data['user_messages'] += 1
                            elif role == 'assistant':
                                session_data['assistant_messages'] += 1

                        elif msg_type == 'function_call':
                            session_data['function_calls'] += 1
                            tool_name = payload.get('name', 'unknown')
                            session_data['tool_names'][tool_name] += 1

                        elif msg_type == 'reasoning':
                            session_data['reasoning_count'] += 1

                    elif entry_type == 'event_msg':
                        event_type = payload.get('type') if payload else None
                        if event_type == 'token_count':
                            info = payload.get('info', {}) or {}
                            last_usage = info.get('last_token_usage', {}) or {}
                            session_data['input_tokens'] += last_usage.get('input_tokens', 0) or 0
                            session_data['output_tokens'] += last_usage.get('output_tokens', 0) or 0
                            session_data['cached_tokens'] += last_usage.get('cached_input_tokens', 0) or 0
                            session_data['reasoning_tokens'] += last_usage.get('reasoning_output_tokens', 0) or 0

                    elif entry_type == 'turn_context':
                        if not session_data['model'] or session_data['model'] == 'openai':
                            model = payload.get('model') if payload else None
                            if model:
                                session_data['model'] = model

                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue

    except Exception as e:
        return None

    session_data['tool_names'] = dict(session_data['tool_names'])
    session_data['message_count'] = session_data['user_messages'] + session_data['assistant_messages']

    return session_data


def aggregate_sessions():
    """Aggregate all session files"""
    if not CODEX_SESSIONS_DIR.exists():
        print(f"  ⚠️  Sessions directory not found: {CODEX_SESSIONS_DIR}")
        return {'sessions': [], 'daily_stats': [], 'model_totals': {}, 'global_tools_used': {}}

    session_files = list(CODEX_SESSIONS_DIR.rglob("*.jsonl"))
    total_files = len(session_files)
    print(f"  📁 Found {total_files} session files")

    all_sessions = []
    daily_stats = defaultdict(lambda: {
        'date': '',
        'sessions': 0,
        'messages': 0,
        'user_messages': 0,
        'assistant_messages': 0,
        'function_calls': 0,
        'reasoning_count': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'cached_tokens': 0,
        'reasoning_tokens': 0,
        'projects': set(),
        'models': defaultdict(lambda: {'requests': 0, 'tokens': 0}),
        'tools_used': defaultdict(int),
    })
    model_totals = defaultdict(lambda: {
        'sessions': 0,
        'messages': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'reasoning_tokens': 0,
    })
    global_tools_used = defaultdict(int)
    processed_files = 0

    for filepath in session_files:
        session = parse_session_file(filepath)
        if session and session.get('id'):
            all_sessions.append(session)
            processed_files += 1

            if session['timestamp']:
                try:
                    date = session['timestamp'][:10]
                    daily_stats[date]['date'] = date
                    daily_stats[date]['sessions'] += 1
                    daily_stats[date]['messages'] += session['message_count']
                    daily_stats[date]['user_messages'] += session['user_messages']
                    daily_stats[date]['assistant_messages'] += session['assistant_messages']
                    daily_stats[date]['function_calls'] += session['function_calls']
                    daily_stats[date]['reasoning_count'] += session['reasoning_count']
                    daily_stats[date]['input_tokens'] += session['input_tokens']
                    daily_stats[date]['output_tokens'] += session['output_tokens']
                    daily_stats[date]['cached_tokens'] += session['cached_tokens']
                    daily_stats[date]['reasoning_tokens'] += session['reasoning_tokens']

                    if session['cwd']:
                        daily_stats[date]['projects'].add(session['cwd'])

                    model = session.get('model', 'unknown')
                    daily_stats[date]['models'][model]['requests'] += 1
                    daily_stats[date]['models'][model]['tokens'] += session['input_tokens'] + session['output_tokens']

                    for tool, count in session['tool_names'].items():
                        daily_stats[date]['tools_used'][tool] += count

                except (KeyError, ValueError, TypeError):
                    pass

            model = session.get('model', 'unknown')
            model_totals[model]['sessions'] += 1
            model_totals[model]['messages'] += session['message_count']
            model_totals[model]['input_tokens'] += session['input_tokens']
            model_totals[model]['output_tokens'] += session['output_tokens']
            model_totals[model]['reasoning_tokens'] += session['reasoning_tokens']

            for tool, count in session['tool_names'].items():
                global_tools_used[tool] += count

    print(f"  ✅ Processed {processed_files}/{total_files} session files")

    daily_list = []
    for date in sorted(daily_stats.keys()):
        day = daily_stats[date]
        day['projects'] = list(day['projects'])
        day['models'] = dict(day['models'])
        day['tools_used'] = dict(day['tools_used'])
        daily_list.append(day)

    return {
        'sessions': all_sessions,
        'daily_stats': daily_list,
        'model_totals': dict(model_totals),
        'global_tools_used': dict(global_tools_used),
        'total_files_scanned': total_files,
        'files_with_data': processed_files,
    }


def main():
    print("=" * 60)
    print("🔍 Codex History Aggregator")
    print("=" * 60)
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("⚙️  Loading config (config.toml)...")
    config = load_config()
    config_data = process_config(config)

    print("\n📜 Loading command history (history.jsonl)...")
    command_history = load_command_history()
    history_data = process_command_history(command_history)

    print("\n📁 Scanning session transcripts (sessions/**/*.jsonl)...")
    session_data = aggregate_sessions()

    output = {
        'generated_at': datetime.now().isoformat(),
        'data_sources': {
            'config_file': CONFIG_FILE.exists(),
            'history_file': HISTORY_FILE.exists(),
            'sessions_dir': CODEX_SESSIONS_DIR.exists(),
        },

        'summary': {
            'total_sessions': len(session_data['sessions']),
            'total_files_scanned': session_data['total_files_scanned'],
            'files_with_data': session_data['files_with_data'],
            'days_with_activity': len(session_data['daily_stats']),

            'total_commands': history_data.get('total_commands', 0),
            'avg_prompt_length': history_data.get('avg_prompt_length', 0),

            'date_range': {
                'first': session_data['daily_stats'][0]['date'] if session_data['daily_stats'] else None,
                'last': session_data['daily_stats'][-1]['date'] if session_data['daily_stats'] else None,
            },

            'totals': {
                'messages': sum(s['message_count'] for s in session_data['sessions']),
                'user_messages': sum(s['user_messages'] for s in session_data['sessions']),
                'assistant_messages': sum(s['assistant_messages'] for s in session_data['sessions']),
                'function_calls': sum(s['function_calls'] for s in session_data['sessions']),
                'reasoning_count': sum(s['reasoning_count'] for s in session_data['sessions']),
                'input_tokens': sum(s['input_tokens'] for s in session_data['sessions']),
                'output_tokens': sum(s['output_tokens'] for s in session_data['sessions']),
                'cached_tokens': sum(s['cached_tokens'] for s in session_data['sessions']),
                'reasoning_tokens': sum(s['reasoning_tokens'] for s in session_data['sessions']),
            }
        },

        'config': config_data,
        'command_history': history_data,
        'model_totals': session_data['model_totals'],
        'daily_stats': session_data['daily_stats'],
        'global_tools_used': session_data['global_tools_used'],
        'sessions': session_data['sessions'],
    }

    print(f"\n💾 Writing consolidated data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)

    print("\n" + "=" * 60)
    print("📊 CODEX AGGREGATION SUMMARY")
    print("=" * 60)

    print(f"\n📦 Data Sources Loaded:")
    print(f"   {'✅' if config_data else '❌'} config.toml")
    print(f"   {'✅' if history_data else '❌'} history.jsonl ({history_data.get('total_commands', 0)} commands)")
    print(f"   {'✅' if session_data['sessions'] else '❌'} sessions/*.jsonl")

    print(f"\n📁 Sessions: {output['summary']['total_sessions']}")
    print(f"   Files scanned: {output['summary']['total_files_scanned']}")
    print(f"   Days with activity: {output['summary']['days_with_activity']}")

    if output['summary']['date_range']['first']:
        print(f"   Date range: {output['summary']['date_range']['first']} to {output['summary']['date_range']['last']}")

    totals = output['summary']['totals']
    print(f"\n📊 Message Totals:")
    print(f"   Total messages: {totals['messages']:,}")
    print(f"   User messages: {totals['user_messages']:,}")
    print(f"   Assistant messages: {totals['assistant_messages']:,}")
    print(f"   Function calls: {totals['function_calls']:,}")
    print(f"   Reasoning blocks: {totals['reasoning_count']:,}")

    print(f"\n🔢 Token Totals:")
    print(f"   Input: {totals['input_tokens']:,}")
    print(f"   Output: {totals['output_tokens']:,}")
    print(f"   Cached: {totals['cached_tokens']:,}")
    print(f"   Reasoning: {totals['reasoning_tokens']:,}")

    print(f"\n🤖 Model breakdown:")
    for model, usage in output['model_totals'].items():
        total_tokens = usage['input_tokens'] + usage['output_tokens']
        print(f"   {model}: {usage['sessions']} sessions, {total_tokens:,} tokens")

    print(f"\n🔧 Tool Usage (Top 10):")
    tools = output.get('global_tools_used', {})
    if tools:
        top_tools = sorted(tools.items(), key=lambda x: -x[1])[:10]
        for tool, count in top_tools:
            print(f"   {tool}: {count:,}")

    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✅ Data saved to: {OUTPUT_FILE}")
    print(f"   File size: {file_size:.1f} KB")


if __name__ == "__main__":
    main()
