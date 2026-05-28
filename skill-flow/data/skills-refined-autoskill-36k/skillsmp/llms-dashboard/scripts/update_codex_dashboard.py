#!/usr/bin/env python3
"""
Codex Dashboard Generator

Reads aggregated history data and generates a comprehensive HTML dashboard
with all available metrics for OpenAI Codex CLI usage.

Never modifies source files - read-only operation.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

HISTORY_FILE = Path(__file__).parent.parent / "data" / "codex_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "codex_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "codex_dashboard.html"


def load_history_data():
    """Load aggregated history data"""
    if not HISTORY_FILE.exists():
        print(f"  ❌ History file not found: {HISTORY_FILE}")
        print("     Run aggregate_codex_history.py first")
        sys.exit(1)

    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"  ❌ Error loading history: {e}")
        sys.exit(1)


def format_number(n):
    """Format number with K/M suffix"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def process_data(history):
    """Process history data for dashboard"""
    summary = history.get('summary', {})
    totals = summary.get('totals', {})
    daily_stats = history.get('daily_stats', [])
    sessions = history.get('sessions', [])
    model_totals = history.get('model_totals', {})
    global_tools = history.get('global_tools_used', {})
    command_history = history.get('command_history', {})
    config = history.get('config', {})

    daily_activity = [
        {
            'date': day['date'],
            'sessions': day['sessions'],
            'messages': day['messages'],
            'functionCalls': day.get('function_calls', 0),
            'inputTokens': day.get('input_tokens', 0),
            'outputTokens': day.get('output_tokens', 0),
        }
        for day in daily_stats
    ]

    session_lengths = defaultdict(int)
    for session in sessions:
        count = session.get('message_count', 0)
        if count <= 5:
            session_lengths['1-5'] += 1
        elif count <= 10:
            session_lengths['6-10'] += 1
        elif count <= 20:
            session_lengths['11-20'] += 1
        elif count <= 50:
            session_lengths['21-50'] += 1
        elif count <= 100:
            session_lengths['51-100'] += 1
        else:
            session_lengths['100+'] += 1

    session_length_data = [
        {'range': r, 'count': session_lengths.get(r, 0)}
        for r in ['1-5', '6-10', '11-20', '21-50', '51-100', '100+']
    ]

    hourly_activity = command_history.get('commands_by_hour', {})
    hourly_data = [{'hour': h, 'count': hourly_activity.get(str(h), 0)} for h in range(24)]

    tool_usage = sorted(global_tools.items(), key=lambda x: -x[1])[:15]
    tool_usage_data = [{'name': t, 'count': c} for t, c in tool_usage]

    model_data = []
    for model, usage in model_totals.items():
        model_data.append({
            'name': model,
            'sessions': usage['sessions'],
            'messages': usage['messages'],
            'inputTokens': usage['input_tokens'],
            'outputTokens': usage['output_tokens'],
            'reasoningTokens': usage.get('reasoning_tokens', 0),
        })
    model_data.sort(key=lambda x: -x['sessions'])

    project_activity = defaultdict(lambda: {'sessions': 0, 'messages': 0})
    for session in sessions:
        cwd = session.get('cwd', '')
        if cwd:
            proj_name = Path(cwd).name
            project_activity[proj_name]['sessions'] += 1
            project_activity[proj_name]['messages'] += session.get('message_count', 0)

    project_data = [
        {'name': name, 'sessions': data['sessions'], 'messages': data['messages']}
        for name, data in project_activity.items()
    ]
    project_data.sort(key=lambda x: -x['sessions'])
    project_data = project_data[:15]

    return {
        'dailyActivity': daily_activity,
        'sessionLengths': session_length_data,
        'hourlyActivity': hourly_data,
        'toolUsage': tool_usage_data,
        'modelData': model_data,
        'projectData': project_data,
    }


def generate_html(history, processed):
    """Generate the HTML dashboard from template"""
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        sys.exit(1)

    summary = history.get('summary', {})
    totals = summary.get('totals', {})
    config = history.get('config', {})
    command_history = history.get('command_history', {})
    date_range = summary.get('date_range', {})

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    replacements = {
        '{{TIMESTAMP}}': timestamp,
        '{{TOTAL_SESSIONS}}': str(summary.get('total_sessions', 0)),
        '{{DAYS_WITH_ACTIVITY}}': str(summary.get('days_with_activity', 0)),
        '{{TOTAL_COMMANDS}}': str(command_history.get('total_commands', 0)),
        '{{AVG_PROMPT_LENGTH}}': str(int(command_history.get('avg_prompt_length', 0))),
        '{{TOTAL_MESSAGES}}': f"{totals.get('messages', 0):,}",
        '{{USER_MESSAGES}}': f"{totals.get('user_messages', 0):,}",
        '{{ASSISTANT_MESSAGES}}': f"{totals.get('assistant_messages', 0):,}",
        '{{FUNCTION_CALLS}}': f"{totals.get('function_calls', 0):,}",
        '{{REASONING_COUNT}}': f"{totals.get('reasoning_count', 0):,}",
        '{{INPUT_TOKENS}}': format_number(totals.get('input_tokens', 0)),
        '{{OUTPUT_TOKENS}}': format_number(totals.get('output_tokens', 0)),
        '{{CACHED_TOKENS}}': format_number(totals.get('cached_tokens', 0)),
        '{{REASONING_TOKENS}}': format_number(totals.get('reasoning_tokens', 0)),
        '{{CURRENT_MODEL}}': config.get('model', 'unknown'),
        '{{REASONING_EFFORT}}': config.get('model_reasoning_effort', 'default'),
        '{{TRUSTED_PROJECTS}}': str(config.get('trusted_projects', 0)),
        '{{FIRST_DATE}}': date_range.get('first', 'N/A'),
        '{{LAST_DATE}}': date_range.get('last', 'N/A'),
        '{{DAILY_ACTIVITY}}': json.dumps(processed['dailyActivity']),
        '{{SESSION_LENGTHS}}': json.dumps(processed['sessionLengths']),
        '{{HOURLY_ACTIVITY}}': json.dumps(processed['hourlyActivity']),
        '{{TOOL_USAGE}}': json.dumps(processed['toolUsage']),
        '{{MODEL_DATA}}': json.dumps(processed['modelData']),
        '{{PROJECT_DATA}}': json.dumps(processed['projectData']),
    }

    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, value)

    return html_content


def main():
    """Main function to generate the dashboard"""
    print("=" * 60)
    print("🎨 Codex Dashboard Generator")
    print("=" * 60)
    print()

    print(f"📖 Loading aggregated history from {HISTORY_FILE}...")
    history = load_history_data()

    print("📊 Processing data for visualization...")
    processed = process_data(history)

    print(f"🎨 Generating HTML dashboard...")
    html = generate_html(history, processed)

    print(f"💾 Writing dashboard to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    summary = history.get('summary', {})
    totals = summary.get('totals', {})

    print(f"\n✅ Dashboard generated successfully!")
    print(f"📊 Location: {OUTPUT_FILE}")

    print(f"\n📈 Quick Stats:")
    print(f"   Sessions: {summary.get('total_sessions', 0)}")
    print(f"   Messages: {totals.get('messages', 0):,}")
    print(f"   Function calls: {totals.get('function_calls', 0):,}")
    print(f"   Days active: {summary.get('days_with_activity', 0)}")

    print(f"\n🌐 Open in browser: file://{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
