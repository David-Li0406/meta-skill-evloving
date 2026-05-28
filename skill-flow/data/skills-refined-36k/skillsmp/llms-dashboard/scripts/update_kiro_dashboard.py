#!/usr/bin/env python3
"""
Kiro Dashboard Generator

Reads aggregated history data and generates a full HTML dashboard
with all available Kiro metrics.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Constants
HISTORY_FILE = Path(__file__).parent.parent / "data" / "kiro_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "kiro_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "kiro_dashboard.html"


def load_history():
    """Load aggregated history data"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {HISTORY_FILE} not found. Run aggregate_kiro_history.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {HISTORY_FILE}: {e}")
        sys.exit(1)


def format_duration(ms):
    """Format milliseconds to human readable duration"""
    if not ms:
        return '0s'
    seconds = int(ms / 1000)
    minutes = seconds // 60
    hours = minutes // 60
    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"


def generate_dashboard():
    print("=" * 60)
    print("🎨 Kiro Dashboard Generator")
    print("=" * 60)
    print()

    data = load_history()
    sessions = data.get('sessions', [])
    summary = data.get('summary', {})
    settings = data.get('settings', {})
    powers = data.get('powers', {})
    workflows = data.get('workflows', {})
    actions = data.get('actions', {})
    models = data.get('models', {})
    context_types = data.get('context_types', {})
    workspaces = data.get('workspaces', {})
    daily_stats = data.get('daily_stats', [])
    cli_history = data.get('cli_history', {})
    cli_sqlite = data.get('cli_sqlite', {})
    log_sessions = data.get('log_sessions', [])

    # Summary stats
    total_sessions = summary.get('total_sessions', 0)
    total_duration_hours = summary.get('total_duration_hours', 0)
    total_messages = summary.get('total_messages', 0)
    total_human = summary.get('total_human_messages', 0)
    total_bot = summary.get('total_bot_messages', 0)
    total_tool = summary.get('total_tool_messages', 0)
    total_tokens = summary.get('total_estimated_tokens', 0)
    unique_workspaces = summary.get('unique_workspaces', 0)

    # Settings info
    thinking_enabled = settings.get('chat.enableThinking', False)
    todo_enabled = settings.get('chat.enableTodoList', False)
    tangent_enabled = settings.get('chat.enableTangentMode', False)
    knowledge_enabled = settings.get('chat.enableKnowledge', False)

    # Powers info
    powers_installed = powers.get('installedCount', 0)
    powers_available = powers.get('availableCount', 0)

    # Prepare chart data
    chart_dates = [d['date'] for d in daily_stats]
    chart_sessions = [d['sessions'] for d in daily_stats]
    chart_messages = [d['messages'] for d in daily_stats]
    chart_human = [d['humanMessages'] for d in daily_stats]
    chart_bot = [d['botMessages'] for d in daily_stats]
    chart_tool = [d['toolMessages'] for d in daily_stats]
    chart_tokens = [d['tokens'] for d in daily_stats]

    # Model data for charts
    model_data = [{'name': k, 'count': v} for k, v in sorted(models.items(), key=lambda x: -x[1])]
    
    # Prepare daily model breakdown (stacked bar chart data)
    all_models = sorted(models.keys())
    daily_models_data = {model: [] for model in all_models}
    for d in daily_stats:
        day_models = d.get('models', {})
        for model in all_models:
            daily_models_data[model].append(day_models.get(model, 0))

    # Prepare CLI SQLite data for charts
    cli_daily_stats = cli_sqlite.get('daily_stats', [])
    cli_dates = [d['date'] for d in cli_daily_stats]
    cli_all_models = sorted(cli_sqlite.get('models', {}).keys())
    cli_models_data = {model: [] for model in cli_all_models}
    for d in cli_daily_stats:
        day_models = d.get('models', {})
        for model in cli_all_models:
            cli_models_data[model].append(day_models.get(model, 0))

    # Workflow data
    workflow_data = [{'name': k, 'count': v} for k, v in sorted(workflows.items(), key=lambda x: -x[1])]

    # Action data
    action_data = [{'name': k, 'count': v} for k, v in sorted(actions.items(), key=lambda x: -x[1])]

    # Context types data
    context_data = [{'name': k, 'count': v} for k, v in sorted(context_types.items(), key=lambda x: -x[1])[:10]]

    # Workspace data (top 10)
    workspace_data = [
        {'hash': k[:12] + '...', 'fullHash': k, 'sessions': v['sessions'], 'messages': v['messages'], 'duration': v['duration']}
        for k, v in sorted(workspaces.items(), key=lambda x: -x[1]['sessions'])[:10]
    ]

    # Generate recent sessions rows
    recent_rows = ""
    for s in sessions[:30]:
        date_str = s.get('startTime', '')[:10] if s.get('startTime') else 'N/A'
        duration = format_duration(s.get('durationMs', 0))
        msgs = s.get('totalMessages', 0)
        workflow = s.get('workflow', 'unknown')
        action = s.get('actionId', 'unknown')
        tokens = s.get('estimatedTokens', 0)

        workflow_badge = "badge-blue" if workflow == "act" else "badge-purple" if workflow == "plan" else "badge-gray"

        recent_rows += f"""
        <tr class="border-b border-gray-700 hover:bg-gray-800 transition-colors">
            <td class="p-3"><span class="badge {workflow_badge}">{workflow}</span></td>
            <td class="p-3 text-gray-300">{date_str}</td>
            <td class="p-3 text-gray-400">{duration}</td>
            <td class="p-3 text-blue-400 font-mono">{msgs}</td>
            <td class="p-3 text-gray-400">{tokens:,}</td>
            <td class="p-3 text-gray-500 text-xs">{action}</td>
        </tr>
        """

    # Read template
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: {TEMPLATE_FILE} not found")
        sys.exit(1)

    # Replace placeholders
    replacements = {
        '{{TIMESTAMP}}': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '{{TOTAL_SESSIONS}}': str(total_sessions),
        '{{TOTAL_DURATION}}': f"{total_duration_hours:.1f}h",
        '{{TOTAL_MESSAGES}}': f"{total_messages:,}",
        '{{TOTAL_HUMAN}}': f"{total_human:,}",
        '{{TOTAL_BOT}}': f"{total_bot:,}",
        '{{TOTAL_TOOL}}': f"{total_tool:,}",
        '{{TOTAL_TOKENS}}': f"{total_tokens:,}",
        '{{UNIQUE_WORKSPACES}}': str(unique_workspaces),
        '{{THINKING_ENABLED}}': 'Yes' if thinking_enabled else 'No',
        '{{TODO_ENABLED}}': 'Yes' if todo_enabled else 'No',
        '{{TANGENT_ENABLED}}': 'Yes' if tangent_enabled else 'No',
        '{{KNOWLEDGE_ENABLED}}': 'Yes' if knowledge_enabled else 'No',
        '{{POWERS_INSTALLED}}': str(powers_installed),
        '{{POWERS_AVAILABLE}}': str(powers_available),
        '{{CLI_COMMANDS}}': str(cli_history.get('total', 0)),
        '{{LOG_SESSIONS}}': str(len(log_sessions)),
        '{{CHART_DATES}}': json.dumps(chart_dates),
        '{{CHART_SESSIONS}}': json.dumps(chart_sessions),
        '{{CHART_MESSAGES}}': json.dumps(chart_messages),
        '{{CHART_HUMAN}}': json.dumps(chart_human),
        '{{CHART_BOT}}': json.dumps(chart_bot),
        '{{CHART_TOOL}}': json.dumps(chart_tool),
        '{{CHART_TOKENS}}': json.dumps(chart_tokens),
        '{{WORKFLOW_DATA}}': json.dumps(workflow_data),
        '{{ACTION_DATA}}': json.dumps(action_data),
        '{{CONTEXT_DATA}}': json.dumps(context_data),
        '{{WORKSPACE_DATA}}': json.dumps(workspace_data),
        '{{MODEL_DATA}}': json.dumps(model_data),
        '{{DAILY_MODELS_DATA}}': json.dumps(daily_models_data),
        '{{ALL_MODELS}}': json.dumps(all_models),
        '{{CLI_DATES}}': json.dumps(cli_dates),
        '{{CLI_MODELS_DATA}}': json.dumps(cli_models_data),
        '{{CLI_ALL_MODELS}}': json.dumps(cli_all_models),
        '{{RECENT_SESSIONS_ROWS}}': recent_rows,
    }

    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # Write output
    with open(OUTPUT_FILE, 'w') as f:
        f.write(html)

    print(f"📊 Dashboard generated at {OUTPUT_FILE}")
    print()
    print("📈 Summary:")
    print(f"   Total sessions: {total_sessions}")
    print(f"   Total duration: {total_duration_hours:.1f} hours")
    print(f"   Total messages: {total_messages:,}")
    print(f"   Estimated tokens: {total_tokens:,}")
    print(f"   Unique workspaces: {unique_workspaces}")
    print(f"   Powers: {powers_installed} installed / {powers_available} available")
    print()
    print(f"🌐 Open in browser: file://{OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dashboard()
