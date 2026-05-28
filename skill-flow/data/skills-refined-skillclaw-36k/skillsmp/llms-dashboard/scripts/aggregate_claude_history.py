#!/usr/bin/env python3
"""
Claude History Aggregator - Comprehensive Edition

Scans ALL Claude Code data sources and consolidates them into a single
historical database for analysis.

Data Sources:
1. ~/.claude/projects/**/*.jsonl - Session transcripts (detailed per-message data)
2. ~/.claude/stats-cache.json - Pre-computed authoritative stats from Claude Code
3. ~/.claude.json - Main config (startups, feature usage, user info)
4. ~/.claude/history.jsonl - User command/prompt history

Output: ~/.claude/skills/llms-dashboard/data/claude_history.json
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# =============================================================================
# DATA SOURCE PATHS
# =============================================================================

# Session transcripts - detailed per-message data
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Pre-computed stats from Claude Code (authoritative source)
STATS_CACHE_FILE = Path.home() / ".claude" / "stats-cache.json"

# Main config file with user info, feature usage, startups
CLAUDE_CONFIG_FILE = Path.home() / ".claude.json"

# User command/prompt history
HISTORY_FILE = Path.home() / ".claude" / "history.jsonl"

# Output paths
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "claude_history.json"


# =============================================================================
# STATS CACHE PARSER (Authoritative Stats)
# =============================================================================

def load_stats_cache():
    """Load pre-computed stats from Claude Code's stats-cache.json"""
    if not STATS_CACHE_FILE.exists():
        print(f"  ⚠️  Stats cache not found: {STATS_CACHE_FILE}")
        return None

    try:
        with open(STATS_CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✅ Loaded stats-cache.json (version {data.get('version', 'unknown')})")
        return data
    except Exception as e:
        print(f"  ❌ Error loading stats-cache: {e}")
        return None


def process_stats_cache(stats_cache):
    """Extract authoritative metrics from stats-cache.json"""
    if not stats_cache:
        return {}

    result = {
        'authoritative': True,
        'last_computed_date': stats_cache.get('lastComputedDate'),
        'total_sessions': stats_cache.get('totalSessions', 0),
        'total_messages': stats_cache.get('totalMessages', 0),
        'first_session_date': stats_cache.get('firstSessionDate'),

        # Daily activity from authoritative source
        'daily_activity': stats_cache.get('dailyActivity', []),

        # Daily model tokens breakdown
        'daily_model_tokens': stats_cache.get('dailyModelTokens', []),

        # Model usage totals
        'model_usage': stats_cache.get('modelUsage', {}),

        # Hour of day activity
        'hour_counts': stats_cache.get('hourCounts', {}),

        # Longest session info
        'longest_session': stats_cache.get('longestSession', {}),
    }

    return result


# =============================================================================
# MAIN CONFIG PARSER (~/.claude.json)
# =============================================================================

def load_claude_config():
    """Load main Claude config with user info and feature usage"""
    if not CLAUDE_CONFIG_FILE.exists():
        print(f"  ⚠️  Config file not found: {CLAUDE_CONFIG_FILE}")
        return None

    try:
        with open(CLAUDE_CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✅ Loaded ~/.claude.json ({data.get('numStartups', 0)} startups)")
        return data
    except Exception as e:
        print(f"  ❌ Error loading config: {e}")
        return None


def process_claude_config(config):
    """Extract user info and feature usage from config"""
    if not config:
        return {}

    result = {
        'num_startups': config.get('numStartups', 0),
        'install_method': config.get('installMethod', 'unknown'),
        'auto_updates': config.get('autoUpdates', False),
        'first_start_time': config.get('firstStartTime'),
        'prompt_queue_use_count': config.get('promptQueueUseCount', 0),

        # Feature usage (tips history)
        'tips_history': config.get('tipsHistory', {}),

        # User info
        'oauth_account': config.get('oauthAccount', {}),

        # GitHub repos
        'github_repo_paths': config.get('githubRepoPaths', {}),

        # Last version seen
        'last_release_notes_seen': config.get('lastReleaseNotesSeen', 'N/A'),

        # Statsig gates (feature flags)
        'cached_statsig_gates': config.get('cachedStatsigGates', {}),
    }

    return result


# =============================================================================
# COMMAND HISTORY PARSER (~/.claude/history.jsonl)
# =============================================================================

def load_command_history():
    """Load user command/prompt history"""
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

    # Command type analysis
    slash_commands = defaultdict(int)
    regular_prompts = 0
    commands_by_date = defaultdict(int)
    commands_by_hour = defaultdict(int)
    projects_used = defaultdict(int)

    for cmd in commands:
        display = cmd.get('display', '')
        timestamp = cmd.get('timestamp', 0)
        project = cmd.get('project', '')

        # Categorize command type
        if display.startswith('/'):
            # Extract slash command name
            parts = display.split()
            if parts:
                cmd_name = parts[0]
                slash_commands[cmd_name] += 1
        else:
            regular_prompts += 1

        # Track by date and hour
        if timestamp:
            try:
                dt = datetime.fromtimestamp(timestamp / 1000)
                date_str = dt.strftime('%Y-%m-%d')
                commands_by_date[date_str] += 1
                commands_by_hour[dt.hour] += 1
            except (ValueError, TypeError, OSError):
                pass

        # Track projects
        if project:
            # Simplify project path
            proj_name = Path(project).name if project else 'unknown'
            projects_used[proj_name] += 1

    # Calculate command length stats
    prompt_lengths = [len(cmd.get('display', '')) for cmd in commands if not cmd.get('display', '').startswith('/')]
    avg_prompt_length = sum(prompt_lengths) / len(prompt_lengths) if prompt_lengths else 0

    result = {
        'total_commands': len(commands),
        'regular_prompts': regular_prompts,
        'slash_commands': dict(slash_commands),
        'slash_command_total': sum(slash_commands.values()),
        'commands_by_date': dict(commands_by_date),
        'commands_by_hour': dict(commands_by_hour),
        'projects_used': dict(projects_used),
        'avg_prompt_length': round(avg_prompt_length, 1),
        'longest_prompt': max(prompt_lengths) if prompt_lengths else 0,
    }

    return result


# =============================================================================
# SESSION TRANSCRIPT PARSER (Existing functionality)
# =============================================================================

def parse_jsonl_file(filepath):
    """Parse a JSONL file and extract session data"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    messages.append(data)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        return []
    return messages


def extract_session_data(messages, project_path, filename):
    """Extract relevant data from session messages"""
    # Determine if this is an agent session
    is_agent = filename.startswith('agent-')

    session = {
        'filename': filename,
        'project': project_path,
        'project_name': project_path.split('-')[-1] if project_path else 'unknown',
        'is_agent': is_agent,
        'session_id': None,
        'agent_id': None,
        'version': None,
        'git_branch': None,
        'start_time': None,
        'end_time': None,
        'duration_ms': 0,
        'message_count': 0,
        'user_messages': 0,
        'assistant_messages': 0,
        'tool_calls': 0,
        'tools_used': defaultdict(int),
        'models_used': defaultdict(lambda: {
            'input_tokens': 0,
            'output_tokens': 0,
            'cache_read': 0,
            'cache_creation': 0,
            'requests': 0
        }),
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_cache_read': 0,
        'total_cache_creation': 0,
    }

    timestamps = []

    for msg in messages:
        # Extract session metadata
        if not session['session_id'] and msg.get('sessionId'):
            session['session_id'] = msg.get('sessionId')
        if not session['agent_id'] and msg.get('agentId'):
            session['agent_id'] = msg.get('agentId')
        if not session['version'] and msg.get('version'):
            session['version'] = msg.get('version')
        if not session['git_branch'] and msg.get('gitBranch'):
            session['git_branch'] = msg.get('gitBranch')

        # Track timestamps
        if msg.get('timestamp'):
            try:
                ts = msg['timestamp']
                if isinstance(ts, str):
                    timestamps.append(ts)
            except (KeyError, TypeError):
                pass

        # Count messages
        session['message_count'] += 1
        msg_type = msg.get('type')

        if msg_type == 'user':
            session['user_messages'] += 1
        elif msg_type == 'assistant':
            session['assistant_messages'] += 1

            # Extract token usage from assistant messages
            message_data = msg.get('message', {})
            model = message_data.get('model', 'unknown')
            usage = message_data.get('usage', {})

            if usage:
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
                cache_read = usage.get('cache_read_input_tokens', 0)
                cache_creation = usage.get('cache_creation_input_tokens', 0)

                session['models_used'][model]['input_tokens'] += input_tokens
                session['models_used'][model]['output_tokens'] += output_tokens
                session['models_used'][model]['cache_read'] += cache_read
                session['models_used'][model]['cache_creation'] += cache_creation
                session['models_used'][model]['requests'] += 1

                session['total_input_tokens'] += input_tokens
                session['total_output_tokens'] += output_tokens
                session['total_cache_read'] += cache_read
                session['total_cache_creation'] += cache_creation

            # Count tool calls and track which tools
            content = message_data.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        session['tool_calls'] += 1
                        tool_name = item.get('name', 'unknown')
                        session['tools_used'][tool_name] += 1

    # Calculate time range
    if timestamps:
        timestamps.sort()
        session['start_time'] = timestamps[0]
        session['end_time'] = timestamps[-1]
        try:
            start = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
            end = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
            session['duration_ms'] = int((end - start).total_seconds() * 1000)
        except (ValueError, TypeError, AttributeError):
            pass

    # Convert defaultdicts to regular dicts
    session['models_used'] = dict(session['models_used'])
    session['tools_used'] = dict(session['tools_used'])

    return session


def aggregate_session_transcripts():
    """Scan all project directories and aggregate session data"""

    if not CLAUDE_PROJECTS_DIR.exists():
        print(f"  ⚠️  Projects directory not found: {CLAUDE_PROJECTS_DIR}")
        return {'sessions': [], 'daily_stats': [], 'project_stats': {}, 'model_totals': {}}

    all_sessions = []
    main_sessions = []
    agent_sessions = []

    daily_stats = defaultdict(lambda: {
        'date': None,
        'sessions': 0,
        'main_sessions': 0,
        'agent_sessions': 0,
        'messages': 0,
        'user_messages': 0,
        'assistant_messages': 0,
        'tool_calls': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'cache_read': 0,
        'cache_creation': 0,
        'models': defaultdict(lambda: {'requests': 0, 'tokens': 0}),
        'projects': set(),
        'tools_used': defaultdict(int)
    })

    model_totals = defaultdict(lambda: {
        'input_tokens': 0,
        'output_tokens': 0,
        'cache_read': 0,
        'cache_creation': 0,
        'requests': 0
    })

    project_stats = defaultdict(lambda: {
        'sessions': 0,
        'main_sessions': 0,
        'agent_sessions': 0,
        'messages': 0,
        'input_tokens': 0,
        'output_tokens': 0,
        'first_session': None,
        'last_session': None,
        'tools_used': defaultdict(int)
    })

    # Global tool usage tracking
    global_tools_used = defaultdict(int)

    # Scan all project directories
    project_dirs = [d for d in CLAUDE_PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    print(f"  📁 Found {len(project_dirs)} project directories")

    total_files = 0
    processed_files = 0

    for project_dir in project_dirs:
        project_path = project_dir.name
        jsonl_files = list(project_dir.glob("*.jsonl"))
        total_files += len(jsonl_files)

        for jsonl_file in jsonl_files:
            messages = parse_jsonl_file(jsonl_file)
            if not messages:
                continue

            session = extract_session_data(messages, project_path, jsonl_file.name)

            # Skip empty sessions
            if session['message_count'] == 0:
                continue

            all_sessions.append(session)
            processed_files += 1

            # Categorize as main or agent session
            if session['is_agent']:
                agent_sessions.append(session)
            else:
                main_sessions.append(session)

            # Track global tool usage
            for tool, count in session['tools_used'].items():
                global_tools_used[tool] += count

            # Aggregate into daily stats
            if session['start_time']:
                try:
                    date = session['start_time'][:10]
                    daily_stats[date]['date'] = date
                    daily_stats[date]['sessions'] += 1
                    daily_stats[date]['main_sessions'] += 0 if session['is_agent'] else 1
                    daily_stats[date]['agent_sessions'] += 1 if session['is_agent'] else 0
                    daily_stats[date]['messages'] += session['message_count']
                    daily_stats[date]['user_messages'] += session['user_messages']
                    daily_stats[date]['assistant_messages'] += session['assistant_messages']
                    daily_stats[date]['tool_calls'] += session['tool_calls']
                    daily_stats[date]['input_tokens'] += session['total_input_tokens']
                    daily_stats[date]['output_tokens'] += session['total_output_tokens']
                    daily_stats[date]['cache_read'] += session['total_cache_read']
                    daily_stats[date]['cache_creation'] += session['total_cache_creation']
                    daily_stats[date]['projects'].add(project_path)

                    for model, usage in session['models_used'].items():
                        daily_stats[date]['models'][model]['requests'] += usage['requests']
                        daily_stats[date]['models'][model]['tokens'] += usage['input_tokens'] + usage['output_tokens']

                    for tool, count in session['tools_used'].items():
                        daily_stats[date]['tools_used'][tool] += count
                except (KeyError, ValueError, TypeError):
                    pass

            # Aggregate model totals
            for model, usage in session['models_used'].items():
                model_totals[model]['input_tokens'] += usage['input_tokens']
                model_totals[model]['output_tokens'] += usage['output_tokens']
                model_totals[model]['cache_read'] += usage['cache_read']
                model_totals[model]['cache_creation'] += usage['cache_creation']
                model_totals[model]['requests'] += usage['requests']

            # Aggregate project stats
            project_stats[project_path]['sessions'] += 1
            project_stats[project_path]['main_sessions'] += 0 if session['is_agent'] else 1
            project_stats[project_path]['agent_sessions'] += 1 if session['is_agent'] else 0
            project_stats[project_path]['messages'] += session['message_count']
            project_stats[project_path]['input_tokens'] += session['total_input_tokens']
            project_stats[project_path]['output_tokens'] += session['total_output_tokens']

            for tool, count in session['tools_used'].items():
                project_stats[project_path]['tools_used'][tool] += count

            if session['start_time']:
                if not project_stats[project_path]['first_session'] or session['start_time'] < project_stats[project_path]['first_session']:
                    project_stats[project_path]['first_session'] = session['start_time']
                if not project_stats[project_path]['last_session'] or session['start_time'] > project_stats[project_path]['last_session']:
                    project_stats[project_path]['last_session'] = session['start_time']

    print(f"  ✅ Processed {processed_files}/{total_files} session files")
    print(f"     Main sessions: {len(main_sessions)}, Agent sessions: {len(agent_sessions)}")

    # Convert daily stats for JSON serialization
    daily_list = []
    for date in sorted(daily_stats.keys()):
        day = daily_stats[date]
        day['projects'] = list(day['projects'])
        day['models'] = dict(day['models'])
        day['tools_used'] = dict(day['tools_used'])
        daily_list.append(day)

    # Convert project stats for JSON
    for proj in project_stats.values():
        proj['tools_used'] = dict(proj['tools_used'])

    return {
        'sessions': all_sessions,
        'main_sessions_count': len(main_sessions),
        'agent_sessions_count': len(agent_sessions),
        'daily_stats': daily_list,
        'project_stats': dict(project_stats),
        'model_totals': dict(model_totals),
        'global_tools_used': dict(global_tools_used),
        'total_files_scanned': total_files,
        'files_with_data': processed_files,
    }


# =============================================================================
# MAIN AGGREGATION
# =============================================================================

def main():
    print("=" * 60)
    print("🔍 Claude History Aggregator - Comprehensive Edition")
    print("=" * 60)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load stats-cache.json (authoritative)
    print("📊 Loading authoritative stats (stats-cache.json)...")
    stats_cache = load_stats_cache()
    stats_cache_data = process_stats_cache(stats_cache)

    # 2. Load main config
    print("\n⚙️  Loading config (~/.claude.json)...")
    claude_config = load_claude_config()
    config_data = process_claude_config(claude_config)

    # 3. Load command history
    print("\n📜 Loading command history (history.jsonl)...")
    command_history = load_command_history()
    history_data = process_command_history(command_history)

    # 4. Load session transcripts
    print("\n📁 Scanning session transcripts (projects/**/*.jsonl)...")
    transcript_data = aggregate_session_transcripts()

    # 5. Build comprehensive output
    output = {
        'generated_at': datetime.now().isoformat(),
        'data_sources': {
            'stats_cache': STATS_CACHE_FILE.exists(),
            'claude_config': CLAUDE_CONFIG_FILE.exists(),
            'history_file': HISTORY_FILE.exists(),
            'projects_dir': CLAUDE_PROJECTS_DIR.exists(),
        },

        # Summary combining all sources
        'summary': {
            # From stats-cache (authoritative)
            'authoritative_sessions': stats_cache_data.get('total_sessions', 0),
            'authoritative_messages': stats_cache_data.get('total_messages', 0),

            # From transcripts (detailed)
            'total_sessions_scanned': len(transcript_data['sessions']),
            'main_sessions': transcript_data['main_sessions_count'],
            'agent_sessions': transcript_data['agent_sessions_count'],
            'total_files_scanned': transcript_data['total_files_scanned'],
            'files_with_data': transcript_data['files_with_data'],
            'total_projects': len(transcript_data['project_stats']),

            # From config
            'num_startups': config_data.get('num_startups', 0),
            'prompt_queue_uses': config_data.get('prompt_queue_use_count', 0),

            # From command history
            'total_commands': history_data.get('total_commands', 0),
            'slash_commands_used': history_data.get('slash_command_total', 0),

            # Date range from transcripts
            'date_range': {
                'first': transcript_data['daily_stats'][0]['date'] if transcript_data['daily_stats'] else None,
                'last': transcript_data['daily_stats'][-1]['date'] if transcript_data['daily_stats'] else None,
                'days_with_activity': len(transcript_data['daily_stats']),
            },

            # Token totals from transcripts
            'totals': {
                'messages': sum(s['message_count'] for s in transcript_data['sessions']),
                'user_messages': sum(s['user_messages'] for s in transcript_data['sessions']),
                'assistant_messages': sum(s['assistant_messages'] for s in transcript_data['sessions']),
                'tool_calls': sum(s['tool_calls'] for s in transcript_data['sessions']),
                'input_tokens': sum(s['total_input_tokens'] for s in transcript_data['sessions']),
                'output_tokens': sum(s['total_output_tokens'] for s in transcript_data['sessions']),
                'cache_read': sum(s['total_cache_read'] for s in transcript_data['sessions']),
                'cache_creation': sum(s['total_cache_creation'] for s in transcript_data['sessions']),
            }
        },

        # Authoritative stats from stats-cache
        'authoritative_stats': stats_cache_data,

        # User config and feature usage
        'user_config': config_data,

        # Command history analysis
        'command_history': history_data,

        # Detailed transcript data
        'model_totals': transcript_data['model_totals'],
        'project_stats': transcript_data['project_stats'],
        'daily_stats': transcript_data['daily_stats'],
        'global_tools_used': transcript_data['global_tools_used'],
        'sessions': transcript_data['sessions'],
    }

    # Write output
    print(f"\n💾 Writing consolidated data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE AGGREGATION SUMMARY")
    print("=" * 60)

    print("\n📦 Data Sources Loaded:")
    print(f"   {'✅' if stats_cache_data else '❌'} stats-cache.json (authoritative stats)")
    print(f"   {'✅' if config_data else '❌'} ~/.claude.json (config & features)")
    print(f"   {'✅' if history_data else '❌'} history.jsonl (command history)")
    print(f"   {'✅' if transcript_data['sessions'] else '❌'} projects/*.jsonl (session transcripts)")

    print(f"\n📁 Projects: {output['summary']['total_projects']}")
    print(f"📄 Session files scanned: {output['summary']['total_files_scanned']}")
    print(f"✅ Sessions with data: {output['summary']['files_with_data']}")
    print(f"   └─ Main sessions: {output['summary']['main_sessions']}")
    print(f"   └─ Agent sessions: {output['summary']['agent_sessions']}")

    if stats_cache_data:
        print(f"\n📊 Authoritative Stats (from stats-cache):")
        print(f"   Sessions: {stats_cache_data.get('total_sessions', 0)}")
        print(f"   Messages: {stats_cache_data.get('total_messages', 0)}")
        longest = stats_cache_data.get('longest_session', {})
        if longest:
            print(f"   Longest session: {longest.get('messageCount', 0)} messages")

    if history_data:
        print(f"\n📜 Command History:")
        print(f"   Total commands: {history_data.get('total_commands', 0)}")
        print(f"   Slash commands: {history_data.get('slash_command_total', 0)}")
        print(f"   Avg prompt length: {history_data.get('avg_prompt_length', 0)} chars")

        # Top slash commands
        slash_cmds = history_data.get('slash_commands', {})
        if slash_cmds:
            top_cmds = sorted(slash_cmds.items(), key=lambda x: -x[1])[:5]
            print(f"   Top commands: {', '.join(f'{c}({n})' for c, n in top_cmds)}")

    if config_data:
        print(f"\n⚙️  User Config:")
        print(f"   Startups: {config_data.get('num_startups', 0)}")
        print(f"   Prompt queue uses: {config_data.get('prompt_queue_use_count', 0)}")
        tips = config_data.get('tips_history', {})
        if tips:
            top_tips = sorted(tips.items(), key=lambda x: -x[1])[:3]
            print(f"   Most seen tips: {', '.join(f'{t}({n})' for t, n in top_tips)}")

    print(f"\n🔧 Tool Usage (Top 10):")
    tools = output.get('global_tools_used', {})
    if tools:
        top_tools = sorted(tools.items(), key=lambda x: -x[1])[:10]
        for tool, count in top_tools:
            print(f"   {tool}: {count:,}")

    print(f"\n🤖 Model breakdown:")
    for model, usage in output['model_totals'].items():
        model_short = model.replace('claude-', '').replace('-20251101', '').replace('-20251001', '').replace('-20250929', '')
        total_tokens = usage['input_tokens'] + usage['output_tokens']
        print(f"   {model_short}: {usage['requests']:,} requests, {total_tokens:,} tokens")

    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✅ Data saved to: {OUTPUT_FILE}")
    print(f"   File size: {file_size:.1f} KB")


if __name__ == "__main__":
    main()
