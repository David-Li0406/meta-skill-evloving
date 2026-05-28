#!/usr/bin/env python3
"""
Gemini History Aggregator - Comprehensive Edition

Scans ALL Gemini CLI and Antigravity data sources and consolidates them
into a single historical database for analysis.

Data Sources:
1. ~/.gemini/tmp/**/chats/*.json - CLI session files (JSON, detailed)
2. ~/.gemini/tmp/**/logs.json - CLI command history logs
3. ~/.gemini/antigravity/brain/ - Brain folders with metadata
4. ~/.gemini/antigravity/conversations/*.pb - Conversation files (stats only)
5. ~/.gemini/antigravity/implicit/*.pb - Implicit sessions (stats only)
6. ~/.gemini/antigravity/code_tracker/ - Project tracking
7. ~/.gemini/antigravity/browser_recordings/ - Browser automation recordings
8. ~/.gemini/antigravity/browserAllowlist.txt - Allowed browser domains
9. ~/.gemini/settings.json - User settings
10. ~/.gemini/state.json - State data

Output: ~/.claude/skills/llms-dashboard/data/gemini_history.json
"""

import os
import json
import glob
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

# =============================================================================
# DATA SOURCE PATHS
# =============================================================================

GEMINI_DIR = Path.home() / ".gemini"
GEMINI_TMP_DIR = GEMINI_DIR / "tmp"
GEMINI_ANTIGRAVITY_DIR = GEMINI_DIR / "antigravity"
GEMINI_BRAIN_DIR = GEMINI_ANTIGRAVITY_DIR / "brain"
GEMINI_CONVERSATIONS_DIR = GEMINI_ANTIGRAVITY_DIR / "conversations"
GEMINI_IMPLICIT_DIR = GEMINI_ANTIGRAVITY_DIR / "implicit"
GEMINI_CODE_TRACKER_DIR = GEMINI_ANTIGRAVITY_DIR / "code_tracker"
GEMINI_BROWSER_RECORDINGS_DIR = GEMINI_ANTIGRAVITY_DIR / "browser_recordings"
GEMINI_BROWSER_ALLOWLIST = GEMINI_ANTIGRAVITY_DIR / "browserAllowlist.txt"
GEMINI_SETTINGS_FILE = GEMINI_DIR / "settings.json"
GEMINI_STATE_FILE = GEMINI_DIR / "state.json"
GEMINI_ACCOUNTS_FILE = GEMINI_DIR / "google_accounts.json"
GEMINI_INSTALLATION_ID = GEMINI_DIR / "installation_id"

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "gemini_history.json"


# =============================================================================
# CLI SESSION PARSER (JSON files)
# =============================================================================

def parse_cli_session(file_path):
    """Parse a CLI session JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        session_id = data.get('sessionId')
        start_time_str = data.get('startTime')
        last_updated_str = data.get('lastUpdated')
        project_hash = data.get('projectHash')
        messages = data.get('messages', [])

        if not start_time_str:
            return None

        # Calculate counts
        user_messages = sum(1 for m in messages if m.get('type') == 'user')
        model_messages = sum(1 for m in messages if m.get('type') in ('gemini', 'model'))

        # Calculate tokens (Incremental estimation)
        total_input_tokens = 0
        total_output_tokens = 0
        last_input_tokens = 0

        sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''))

        for m in sorted_messages:
            tokens = m.get('tokens')
            if tokens:
                current_input = tokens.get('input', 0)
                current_output = tokens.get('output', 0)
                total_output_tokens += current_output

                if current_input >= last_input_tokens:
                    diff = current_input - last_input_tokens
                    total_input_tokens += diff
                else:
                    total_input_tokens += current_input

                last_input_tokens = current_input + current_output

        # Calculate duration
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        if last_updated_str:
            last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
            duration_seconds = (last_updated - start_time).total_seconds()
        else:
            duration_seconds = 0

        # Extract tools used
        tools_used = defaultdict(int)
        for m in messages:
            tool_calls = m.get('toolCalls', [])
            for tc in tool_calls:
                tool_name = tc.get('name', 'unknown')
                tools_used[tool_name] += 1

        return {
            "type": "CLI",
            "sessionId": session_id,
            "startTime": start_time_str,
            "projectHash": project_hash,
            "userMessages": user_messages,
            "modelMessages": model_messages,
            "totalMessages": len(messages),
            "totalInputTokens": total_input_tokens,
            "totalOutputTokens": total_output_tokens,
            "durationSeconds": duration_seconds,
            "filePath": str(file_path),
            "toolsUsed": dict(tools_used),
            "summary": None
        }

    except Exception as e:
        print(f"  Error parsing CLI session {file_path}: {e}")
        return None


def scan_cli_sessions():
    """Scan CLI session files"""
    sessions = []

    if not GEMINI_TMP_DIR.exists():
        print(f"  ⚠️  CLI temp directory not found: {GEMINI_TMP_DIR}")
        return sessions

    search_pattern = str(GEMINI_TMP_DIR / "**" / "chats" / "session-*.json")
    session_files = glob.glob(search_pattern, recursive=True)
    print(f"  📁 Found {len(session_files)} CLI session files")

    for file_path in session_files:
        session = parse_cli_session(file_path)
        if session:
            sessions.append(session)

    return sessions


# =============================================================================
# CLI LOGS PARSER (logs.json - command history)
# =============================================================================

def scan_cli_logs():
    """Scan CLI logs.json files for command history"""
    all_commands = []
    slash_commands = defaultdict(int)

    if not GEMINI_TMP_DIR.exists():
        return {'commands': [], 'slash_commands': {}, 'total': 0}

    log_files = list(GEMINI_TMP_DIR.glob("*/logs.json"))
    print(f"  📁 Found {len(log_files)} logs.json files")

    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)

            for entry in logs:
                msg = entry.get('message', '')
                timestamp = entry.get('timestamp', '')
                msg_type = entry.get('type', '')

                if msg_type == 'user':
                    all_commands.append({
                        'message': msg,
                        'timestamp': timestamp,
                        'sessionId': entry.get('sessionId', '')
                    })

                    # Track slash commands
                    if msg.startswith('/'):
                        cmd = msg.split()[0]
                        slash_commands[cmd] += 1
        except Exception as e:
            print(f"  Error parsing {log_file}: {e}")

    return {
        'commands': all_commands,
        'slash_commands': dict(slash_commands),
        'total': len(all_commands)
    }


# =============================================================================
# BROWSER RECORDINGS PARSER
# =============================================================================

def scan_browser_recordings():
    """Scan browser recordings for automation stats"""
    recordings = []

    if not GEMINI_BROWSER_RECORDINGS_DIR.exists():
        return {'sessions': [], 'total_screenshots': 0, 'total_sessions': 0}

    recording_dirs = [d for d in GEMINI_BROWSER_RECORDINGS_DIR.iterdir() if d.is_dir()]

    for rec_dir in recording_dirs:
        try:
            # Count screenshots
            screenshots = list(rec_dir.glob("*.jpg")) + list(rec_dir.glob("*.png"))
            screenshot_count = len(screenshots)

            # Load metadata
            metadata_file = rec_dir / "metadata.json"
            highlights = []
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    highlights = metadata.get('highlights', [])

            # Get date range from screenshots
            dates = []
            for s in screenshots[:10]:  # Sample first 10
                try:
                    dates.append(s.stat().st_mtime)
                except:
                    pass

            date_range = None
            if dates:
                dates.sort()
                date_range = {
                    'start': datetime.fromtimestamp(dates[0], tz=timezone.utc).isoformat(),
                    'end': datetime.fromtimestamp(dates[-1], tz=timezone.utc).isoformat()
                }

            recordings.append({
                'id': rec_dir.name,
                'screenshots': screenshot_count,
                'highlights': len(highlights),
                'date_range': date_range
            })
        except Exception as e:
            print(f"  Error parsing recording {rec_dir}: {e}")

    total_screenshots = sum(r['screenshots'] for r in recordings)
    return {
        'sessions': recordings,
        'total_screenshots': total_screenshots,
        'total_sessions': len(recordings)
    }


# =============================================================================
# BRAIN FOLDER PARSER (Antigravity)
# =============================================================================

def parse_brain_folder(folder_path):
    """Parse an Antigravity brain folder"""
    try:
        session_id = os.path.basename(folder_path)
        all_files = list(Path(folder_path).glob("*"))

        if not all_files:
            return None

        timestamps = []
        summaries = set()
        task_items = []

        # Scan metadata files
        meta_files = list(Path(folder_path).glob("*.metadata.json"))
        for meta_file in meta_files:
            try:
                with open(meta_file, 'r') as f:
                    data = json.load(f)
                    if data.get('updatedAt'):
                        timestamps.append(datetime.fromisoformat(data['updatedAt'].replace('Z', '+00:00')))
                    if data.get('summary'):
                        s = data['summary']
                        if isinstance(s, list):
                            summaries.update(s)
                        elif isinstance(s, str):
                            summaries.add(s)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                pass

        # Check task.md for task details
        task_file = Path(folder_path) / "task.md"
        if task_file.exists():
            try:
                with open(task_file, 'r') as f:
                    content = f.read()
                    # Count completed vs pending tasks
                    completed = content.count('[x]')
                    pending = content.count('[ ]')
                    task_items = {'completed': completed, 'pending': pending}
            except:
                pass

        # Use file modification times
        for f in all_files:
            mtime = os.path.getmtime(f)
            timestamps.append(datetime.fromtimestamp(mtime, tz=timezone.utc))

        if not timestamps:
            return None

        timestamps.sort()
        start_time = timestamps[0]
        end_time = timestamps[-1]
        duration_seconds = max((end_time - start_time).total_seconds(), 60)

        # Categorize files
        resolved_files = len(list(Path(folder_path).glob("*.resolved*")))
        md_files = len(list(Path(folder_path).glob("*.md")))

        return {
            "type": "Antigravity",
            "sessionId": session_id,
            "startTime": start_time.isoformat(),
            "projectHash": "antigravity-brain",
            "userMessages": 0,
            "modelMessages": 0,
            "totalMessages": len(all_files),
            "totalInputTokens": 0,
            "totalOutputTokens": 0,
            "durationSeconds": duration_seconds,
            "filePath": str(folder_path),
            "toolsUsed": {},
            "summary": list(summaries)[0] if summaries else "Antigravity Session",
            "resolvedFiles": resolved_files,
            "mdFiles": md_files,
            "taskItems": task_items if task_items else None
        }

    except Exception as e:
        print(f"  Error parsing brain folder {folder_path}: {e}")
        return None


def scan_brain_folders():
    """Scan Antigravity brain folders"""
    sessions = []

    if not GEMINI_BRAIN_DIR.exists():
        print(f"  ⚠️  Brain directory not found: {GEMINI_BRAIN_DIR}")
        return sessions

    brain_folders = [f for f in GEMINI_BRAIN_DIR.iterdir() if f.is_dir()]
    print(f"  📁 Found {len(brain_folders)} brain folders")

    for folder in brain_folders:
        session = parse_brain_folder(folder)
        if session:
            sessions.append(session)

    return sessions


# =============================================================================
# CONVERSATION/IMPLICIT FILES (File stats only)
# =============================================================================

def scan_pb_files(directory, session_type):
    """Scan .pb files and extract file stats"""
    stats = {
        'count': 0,
        'total_size_bytes': 0,
        'files': [],
        'date_range': {'first': None, 'last': None}
    }

    if not directory.exists():
        return stats

    pb_files = list(directory.glob("*.pb"))
    stats['count'] = len(pb_files)

    file_dates = []
    for pb_file in pb_files:
        try:
            stat = pb_file.stat()
            file_info = {
                'id': pb_file.stem,
                'size_bytes': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
            }
            stats['files'].append(file_info)
            stats['total_size_bytes'] += stat.st_size
            file_dates.append(stat.st_mtime)
        except Exception:
            pass

    if file_dates:
        file_dates.sort()
        stats['date_range']['first'] = datetime.fromtimestamp(file_dates[0], tz=timezone.utc).isoformat()
        stats['date_range']['last'] = datetime.fromtimestamp(file_dates[-1], tz=timezone.utc).isoformat()

    return stats


# =============================================================================
# CODE TRACKER PARSER
# =============================================================================

def scan_code_tracker():
    """Scan code_tracker for project info"""
    projects = []

    active_dir = GEMINI_CODE_TRACKER_DIR / "active"
    if not active_dir.exists():
        print(f"  ⚠️  Code tracker not found: {active_dir}")
        return projects

    project_dirs = [d for d in active_dir.iterdir() if d.is_dir()]
    print(f"  📁 Found {len(project_dirs)} tracked projects")

    for proj_dir in project_dirs:
        try:
            # Parse project name from folder name (format: "Name_hash")
            folder_name = proj_dir.name
            parts = folder_name.rsplit('_', 1)
            project_name = parts[0] if len(parts) > 1 else folder_name
            project_hash = parts[1] if len(parts) > 1 else 'unknown'

            # Count tracked files
            tracked_files = list(proj_dir.glob("*"))
            file_count = len(tracked_files)

            # Get modification dates
            mod_times = []
            for f in tracked_files:
                try:
                    mod_times.append(f.stat().st_mtime)
                except:
                    pass

            last_modified = None
            if mod_times:
                last_modified = datetime.fromtimestamp(max(mod_times), tz=timezone.utc).isoformat()

            projects.append({
                'name': project_name,
                'hash': project_hash,
                'trackedFiles': file_count,
                'lastModified': last_modified,
                'path': str(proj_dir)
            })
        except Exception as e:
            print(f"  Error parsing project {proj_dir}: {e}")

    return projects


# =============================================================================
# SETTINGS & CONFIG PARSER
# =============================================================================

def load_settings():
    """Load Gemini settings"""
    settings = {}

    # settings.json
    if GEMINI_SETTINGS_FILE.exists():
        try:
            with open(GEMINI_SETTINGS_FILE, 'r') as f:
                settings['preferences'] = json.load(f)
        except:
            pass

    # state.json
    if GEMINI_STATE_FILE.exists():
        try:
            with open(GEMINI_STATE_FILE, 'r') as f:
                settings['state'] = json.load(f)
        except:
            pass

    # google_accounts.json
    if GEMINI_ACCOUNTS_FILE.exists():
        try:
            with open(GEMINI_ACCOUNTS_FILE, 'r') as f:
                data = json.load(f)
                settings['activeAccount'] = data.get('active', 'Unknown')
        except:
            pass

    # installation_id
    if GEMINI_INSTALLATION_ID.exists():
        try:
            with open(GEMINI_INSTALLATION_ID, 'r') as f:
                settings['installationId'] = f.read().strip()
        except:
            pass

    # Browser allowlist
    if GEMINI_BROWSER_ALLOWLIST.exists():
        try:
            with open(GEMINI_BROWSER_ALLOWLIST, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
                settings['browserAllowlist'] = domains
                settings['browserAllowlistCount'] = len(domains)
        except:
            pass

    return settings


# =============================================================================
# MAIN AGGREGATION
# =============================================================================

def main():
    print("=" * 60)
    print("🔍 Gemini History Aggregator - Comprehensive Edition")
    print("=" * 60)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Scan CLI Sessions
    print("📊 Scanning CLI sessions (~/.gemini/tmp/)...")
    cli_sessions = scan_cli_sessions()
    print(f"  ✅ Found {len(cli_sessions)} CLI sessions")

    # 2. Scan Brain Folders
    print("\n🧠 Scanning Antigravity brain folders...")
    brain_sessions = scan_brain_folders()
    print(f"  ✅ Found {len(brain_sessions)} brain sessions")

    # 3. Scan Conversation Files (stats only)
    print("\n💬 Scanning conversation files (stats)...")
    conversation_stats = scan_pb_files(GEMINI_CONVERSATIONS_DIR, 'conversation')
    print(f"  ✅ Found {conversation_stats['count']} conversation files ({conversation_stats['total_size_bytes'] / 1024 / 1024:.1f} MB)")

    # 4. Scan Implicit Sessions (stats only)
    print("\n🔮 Scanning implicit sessions (stats)...")
    implicit_stats = scan_pb_files(GEMINI_IMPLICIT_DIR, 'implicit')
    print(f"  ✅ Found {implicit_stats['count']} implicit files ({implicit_stats['total_size_bytes'] / 1024 / 1024:.1f} MB)")

    # 5. Scan Code Tracker
    print("\n📁 Scanning code tracker...")
    tracked_projects = scan_code_tracker()
    print(f"  ✅ Found {len(tracked_projects)} tracked projects")

    # 6. Scan CLI Logs
    print("\n📜 Scanning CLI logs (command history)...")
    cli_logs = scan_cli_logs()
    print(f"  ✅ Found {cli_logs['total']} user commands, {len(cli_logs['slash_commands'])} slash command types")

    # 7. Scan Browser Recordings
    print("\n🖼️  Scanning browser recordings...")
    browser_recordings = scan_browser_recordings()
    print(f"  ✅ Found {browser_recordings['total_sessions']} recording sessions, {browser_recordings['total_screenshots']} screenshots")

    # 8. Load Settings
    print("\n⚙️  Loading settings...")
    settings = load_settings()
    print(f"  ✅ Active account: {settings.get('activeAccount', 'Unknown')}")

    # Combine all sessions
    all_sessions = cli_sessions + brain_sessions
    all_sessions.sort(key=lambda x: x.get('startTime', ''), reverse=True)

    # Calculate aggregates
    total_cli = len(cli_sessions)
    total_brain = len(brain_sessions)
    total_messages = sum(s.get('totalMessages', 0) for s in all_sessions)
    total_input_tokens = sum(s.get('totalInputTokens', 0) for s in all_sessions)
    total_output_tokens = sum(s.get('totalOutputTokens', 0) for s in all_sessions)
    total_duration = sum(s.get('durationSeconds', 0) for s in all_sessions)

    # Aggregate tools used
    global_tools = defaultdict(int)
    for s in all_sessions:
        for tool, count in s.get('toolsUsed', {}).items():
            global_tools[tool] += count

    # Daily stats
    daily_stats = defaultdict(lambda: {
        'date': None,
        'sessions': 0,
        'cliSessions': 0,
        'brainSessions': 0,
        'messages': 0,
        'cliMessages': 0,
        'brainMessages': 0,
        'inputTokens': 0,
        'outputTokens': 0,
        'duration': 0
    })

    for s in all_sessions:
        start_time = s.get('startTime')
        if start_time:
            date = start_time[:10]
            daily_stats[date]['date'] = date
            daily_stats[date]['sessions'] += 1
            daily_stats[date]['cliSessions'] += 1 if s['type'] == 'CLI' else 0
            daily_stats[date]['brainSessions'] += 1 if s['type'] == 'Antigravity' else 0
            daily_stats[date]['messages'] += s.get('totalMessages', 0)
            daily_stats[date]['cliMessages'] += s.get('totalMessages', 0) if s['type'] == 'CLI' else 0
            daily_stats[date]['brainMessages'] += s.get('totalMessages', 0) if s['type'] == 'Antigravity' else 0
            daily_stats[date]['inputTokens'] += s.get('totalInputTokens', 0)
            daily_stats[date]['outputTokens'] += s.get('totalOutputTokens', 0)
            daily_stats[date]['duration'] += s.get('durationSeconds', 0)

    daily_list = [daily_stats[d] for d in sorted(daily_stats.keys())]

    # Build output
    output = {
        'generated_at': datetime.now().isoformat(),
        'data_sources': {
            'cli_sessions': GEMINI_TMP_DIR.exists(),
            'cli_logs': bool(cli_logs['total']),
            'brain_folders': GEMINI_BRAIN_DIR.exists(),
            'conversations': GEMINI_CONVERSATIONS_DIR.exists(),
            'implicit': GEMINI_IMPLICIT_DIR.exists(),
            'code_tracker': (GEMINI_CODE_TRACKER_DIR / "active").exists(),
            'browser_recordings': GEMINI_BROWSER_RECORDINGS_DIR.exists(),
            'settings': GEMINI_SETTINGS_FILE.exists(),
        },

        'summary': {
            'total_sessions': len(all_sessions),
            'cli_sessions': total_cli,
            'brain_sessions': total_brain,
            'total_messages': total_messages,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'total_duration_seconds': total_duration,
            'conversation_files': conversation_stats['count'],
            'conversation_size_mb': round(conversation_stats['total_size_bytes'] / 1024 / 1024, 1),
            'implicit_files': implicit_stats['count'],
            'implicit_size_mb': round(implicit_stats['total_size_bytes'] / 1024 / 1024, 1),
            'tracked_projects': len(tracked_projects),
            'cli_user_commands': cli_logs['total'],
            'slash_command_types': len(cli_logs['slash_commands']),
            'browser_recording_sessions': browser_recordings['total_sessions'],
            'browser_screenshots': browser_recordings['total_screenshots'],
            'date_range': {
                'first': daily_list[0]['date'] if daily_list else None,
                'last': daily_list[-1]['date'] if daily_list else None,
                'days_active': len(daily_list)
            }
        },

        'settings': settings,
        'tracked_projects': tracked_projects,
        'conversation_stats': conversation_stats,
        'implicit_stats': implicit_stats,
        'cli_logs': cli_logs,
        'browser_recordings': browser_recordings,
        'daily_stats': daily_list,
        'global_tools_used': dict(global_tools),
        'sessions': all_sessions,
    }

    # Write output
    print(f"\n💾 Writing data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE AGGREGATION SUMMARY")
    print("=" * 60)

    print("\n📦 Data Sources:")
    print(f"   {'✅' if cli_sessions else '❌'} CLI sessions: {len(cli_sessions)}")
    print(f"   {'✅' if cli_logs['total'] else '❌'} CLI command logs: {cli_logs['total']} commands")
    print(f"   {'✅' if brain_sessions else '❌'} Brain sessions: {len(brain_sessions)}")
    print(f"   {'✅' if conversation_stats['count'] else '❌'} Conversation files: {conversation_stats['count']} ({conversation_stats['total_size_bytes']/1024/1024:.1f}MB)")
    print(f"   {'✅' if implicit_stats['count'] else '❌'} Implicit files: {implicit_stats['count']} ({implicit_stats['total_size_bytes']/1024/1024:.1f}MB)")
    print(f"   {'✅' if browser_recordings['total_sessions'] else '❌'} Browser recordings: {browser_recordings['total_sessions']} sessions ({browser_recordings['total_screenshots']} screenshots)")
    print(f"   {'✅' if tracked_projects else '❌'} Tracked projects: {len(tracked_projects)}")

    print(f"\n📊 Session Totals:")
    print(f"   Total sessions: {len(all_sessions)}")
    print(f"   Total messages: {total_messages:,}")
    print(f"   Total tokens: {total_input_tokens + total_output_tokens:,}")
    print(f"   Total duration: {total_duration/3600:.1f} hours")

    if tracked_projects:
        print(f"\n📁 Tracked Projects:")
        for proj in tracked_projects[:5]:
            print(f"   {proj['name']}: {proj['trackedFiles']} files")

    if global_tools:
        print(f"\n🔧 Tool Usage (Top 10):")
        top_tools = sorted(global_tools.items(), key=lambda x: -x[1])[:10]
        for tool, count in top_tools:
            print(f"   {tool}: {count}")

    if cli_logs['slash_commands']:
        print(f"\n⚡ Slash Commands (Top 10):")
        top_slash = sorted(cli_logs['slash_commands'].items(), key=lambda x: -x[1])[:10]
        for cmd, count in top_slash:
            print(f"   {cmd}: {count}")

    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✅ Data saved to: {OUTPUT_FILE}")
    print(f"   File size: {file_size:.1f} KB")


if __name__ == "__main__":
    main()
