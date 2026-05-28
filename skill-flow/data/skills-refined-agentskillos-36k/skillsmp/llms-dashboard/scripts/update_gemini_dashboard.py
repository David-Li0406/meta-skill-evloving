#!/usr/bin/env python3
"""
Gemini Dashboard Generator - Comprehensive Edition

Reads aggregated history data and generates a full HTML dashboard
with all available Gemini CLI metrics.

Data Sources (via aggregated history):
- CLI sessions: Detailed JSON session data
- Brain sessions: Antigravity session metadata
- Conversation stats: File counts and sizes
- Implicit stats: Background session stats
- Tracked projects: Code tracker data
- Settings: User preferences
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Constants
HISTORY_FILE = Path(__file__).parent.parent / "data" / "gemini_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "gemini_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "gemini_dashboard.html"


def load_history():
    """Load aggregated history data"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {HISTORY_FILE} not found. Run aggregate_gemini_history.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {HISTORY_FILE}: {e}")
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
    print("=" * 60)
    print("🎨 Gemini Dashboard Generator - Comprehensive Edition")
    print("=" * 60)
    print()

    data = load_history()
    sessions = data.get('sessions', [])
    summary = data.get('summary', {})
    settings = data.get('settings', {})
    tracked_projects = data.get('tracked_projects', [])
    conversation_stats = data.get('conversation_stats', {})
    implicit_stats = data.get('implicit_stats', {})
    cli_logs = data.get('cli_logs', {})
    browser_recordings = data.get('browser_recordings', {})
    daily_stats = data.get('daily_stats', [])
    global_tools = data.get('global_tools_used', {})

    # User info
    user_email = settings.get('activeAccount', 'Unknown User')
    preferences = settings.get('preferences', {})
    ide_enabled = preferences.get('ide', {}).get('enabled', False)
    preview_features = preferences.get('general', {}).get('previewFeatures', False)

    # Calculate totals
    total_sessions = summary.get('total_sessions', len(sessions))
    cli_sessions = summary.get('cli_sessions', 0)
    brain_sessions = summary.get('brain_sessions', 0)
    total_messages = summary.get('total_messages', 0)
    total_input_tokens = summary.get('total_input_tokens', 0)
    total_output_tokens = summary.get('total_output_tokens', 0)
    total_tokens = total_input_tokens + total_output_tokens
    total_duration_seconds = summary.get('total_duration_seconds', 0)

    # Conversation/implicit stats
    conv_files = summary.get('conversation_files', 0)
    conv_size_mb = summary.get('conversation_size_mb', 0)
    implicit_files = summary.get('implicit_files', 0)
    implicit_size_mb = summary.get('implicit_size_mb', 0)

    # CLI logs and browser recordings
    cli_user_commands = cli_logs.get('total', 0)
    slash_commands = cli_logs.get('slash_commands', {})
    slash_command_types = len(slash_commands)
    browser_sessions = browser_recordings.get('total_sessions', 0)
    browser_screenshots = browser_recordings.get('total_screenshots', 0)
    browser_allowlist = settings.get('browserAllowlist', [])

    # Slash command data for chart
    slash_usage = sorted(slash_commands.items(), key=lambda x: -x[1])[:10]
    slash_usage_data = [{'name': cmd, 'count': count} for cmd, count in slash_usage]

    # Prepare chart data
    chart_dates = [d['date'] for d in daily_stats]
    chart_sessions = [d['sessions'] for d in daily_stats]
    chart_cli = [d['cliSessions'] for d in daily_stats]
    chart_brain = [d['brainSessions'] for d in daily_stats]
    chart_messages = [d['messages'] for d in daily_stats]
    chart_input_tokens = [d['inputTokens'] for d in daily_stats]
    chart_output_tokens = [d['outputTokens'] for d in daily_stats]
    chart_cli_messages = [d.get('cliMessages', 0) for d in daily_stats]
    chart_brain_messages = [d.get('brainMessages', 0) for d in daily_stats]

    # Duration boxplot data
    chart_durations = []
    for d in daily_stats:
        day_sessions = [s for s in sessions if s.get('startTime', '').startswith(d['date'])]
        durations = [s.get('durationSeconds', 0) / 60 for s in day_sessions]  # Convert to minutes
        chart_durations.append(durations)

    # Calculate Y-Axis Max for Boxplot
    all_durations = []
    for d_list in chart_durations:
        all_durations.extend(d_list)

    if all_durations:
        all_durations.sort()
        idx = int(len(all_durations) * 0.90)
        y_axis_max = all_durations[idx] if idx < len(all_durations) else all_durations[-1]
        y_axis_max = int(y_axis_max * 1.1)
        y_axis_max = max(y_axis_max, 10)
    else:
        y_axis_max = 60

    # Tool usage data
    tool_usage = sorted(global_tools.items(), key=lambda x: -x[1])[:15]
    tool_usage_data = [{'name': t, 'count': c} for t, c in tool_usage]

    # Generate Recent Sessions Rows
    recent_rows = ""
    for s in sessions[:25]:  # Top 25 recent
        date_str = s.get('startTime', '').split('T')[0]
        duration = format_duration(s.get('durationSeconds', 0))
        msgs = s.get('totalMessages', 0)
        stype = s.get('type', 'CLI')
        summary_text = s.get('summary')
        if not summary_text:
            summary_text = s.get('projectHash', 'N/A')[:12] + "..."

        if len(summary_text) > 60:
            summary_text = summary_text[:57] + "..."

        type_badge = "badge-blue" if stype == "CLI" else "badge-purple"

        input_tokens = s.get('totalInputTokens', 0)
        output_tokens = s.get('totalOutputTokens', 0)
        if input_tokens or output_tokens:
            tokens_str = f"{input_tokens:,} / {output_tokens:,}"
        else:
            tokens_str = "-"

        # Task items for brain sessions
        task_info = ""
        if s.get('taskItems'):
            completed = s['taskItems'].get('completed', 0)
            pending = s['taskItems'].get('pending', 0)
            task_info = f'<span class="text-xs text-green-400">[{completed}/{completed + pending}]</span>'

        recent_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3"><span class="badge {type_badge}">{stype}</span></td>
            <td class="p-3 text-gray-300">{date_str}</td>
            <td class="p-3 text-gray-400">{duration}</td>
            <td class="p-3 text-blue-400 font-mono">{msgs}</td>
            <td class="p-3 text-gray-400 text-xs">{tokens_str}</td>
            <td class="p-3 text-gray-400 text-sm">{summary_text} {task_info}</td>
        </tr>
        """

    # Generate Projects Rows
    project_rows = ""
    for p in tracked_projects:
        last_mod = p.get('lastModified', '')[:10] if p.get('lastModified') else 'N/A'
        project_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3 text-white font-semibold">{p['name']}</td>
            <td class="p-3 text-blue-400 font-mono">{p['trackedFiles']}</td>
            <td class="p-3 text-gray-400">{last_mod}</td>
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
    replacements = {
        '{{USER_EMAIL}}': user_email,
        '{{TIMESTAMP}}': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '{{TOTAL_SESSIONS}}': str(total_sessions),
        '{{CLI_SESSIONS}}': str(cli_sessions),
        '{{BRAIN_SESSIONS}}': str(brain_sessions),
        '{{TOTAL_MESSAGES}}': f"{total_messages:,}",
        '{{USER_MESSAGES}}': str(sum(s.get('userMessages', 0) for s in sessions)),
        '{{TOTAL_DURATION}}': format_duration(total_duration_seconds),
        '{{TOTAL_TOKENS}}': f"{total_tokens:,}",
        '{{TOTAL_INPUT_TOKENS}}': f"{total_input_tokens:,}",
        '{{TOTAL_OUTPUT_TOKENS}}': f"{total_output_tokens:,}",
        '{{CONV_FILES}}': str(conv_files),
        '{{CONV_SIZE_MB}}': f"{conv_size_mb:.1f}",
        '{{IMPLICIT_FILES}}': str(implicit_files),
        '{{IMPLICIT_SIZE_MB}}': f"{implicit_size_mb:.1f}",
        '{{TRACKED_PROJECTS}}': str(len(tracked_projects)),
        '{{IDE_ENABLED}}': 'Yes' if ide_enabled else 'No',
        '{{PREVIEW_FEATURES}}': 'Yes' if preview_features else 'No',
        '{{CHART_DATES}}': json.dumps(chart_dates),
        '{{CHART_SESSIONS}}': json.dumps(chart_sessions),
        '{{CHART_CLI}}': json.dumps(chart_cli),
        '{{CHART_BRAIN}}': json.dumps(chart_brain),
        '{{CHART_MESSAGES}}': json.dumps(chart_messages),
        '{{CHART_INPUT_TOKENS}}': json.dumps(chart_input_tokens),
        '{{CHART_OUTPUT_TOKENS}}': json.dumps(chart_output_tokens),
        '{{CHART_CLI_MESSAGES}}': json.dumps(chart_cli_messages),
        '{{CHART_BRAIN_MESSAGES}}': json.dumps(chart_brain_messages),
        '{{CHART_DURATIONS}}': json.dumps(chart_durations),
        '{{TOOL_USAGE}}': json.dumps(tool_usage_data),
        '{{Y_AXIS_MAX}}': str(y_axis_max),
        '{{RECENT_SESSIONS_ROWS}}': recent_rows,
        '{{PROJECT_ROWS}}': project_rows,
        '{{CLI_USER_COMMANDS}}': str(cli_user_commands),
        '{{SLASH_COMMAND_TYPES}}': str(slash_command_types),
        '{{SLASH_USAGE}}': json.dumps(slash_usage_data),
        '{{BROWSER_SESSIONS}}': str(browser_sessions),
        '{{BROWSER_SCREENSHOTS}}': f"{browser_screenshots:,}",
        '{{BROWSER_ALLOWLIST_COUNT}}': str(len(browser_allowlist)),
    }

    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # Write Output
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html)

    print(f"📊 Dashboard generated at {OUTPUT_FILE}")
    print()
    print("📈 Summary:")
    print(f"   User: {user_email}")
    print(f"   Total sessions: {total_sessions} (CLI: {cli_sessions}, Brain: {brain_sessions})")
    print(f"   Total messages: {total_messages:,}")
    print(f"   Total tokens: {total_tokens:,}")
    print(f"   Total duration: {format_duration(total_duration_seconds)}")
    print(f"   Conversation files: {conv_files} ({conv_size_mb:.1f} MB)")
    print(f"   Implicit files: {implicit_files} ({implicit_size_mb:.1f} MB)")
    print(f"   CLI commands: {cli_user_commands} ({slash_command_types} slash types)")
    print(f"   Browser recordings: {browser_sessions} sessions ({browser_screenshots:,} screenshots)")
    print(f"   Tracked projects: {len(tracked_projects)}")
    print()
    print(f"🌐 Open in browser: file://{OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dashboard()
