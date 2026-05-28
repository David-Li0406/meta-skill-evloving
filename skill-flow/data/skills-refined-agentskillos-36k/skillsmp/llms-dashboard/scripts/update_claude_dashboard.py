#!/usr/bin/env python3
"""
Claude Dashboard Generator - Comprehensive Edition

Reads aggregated history data and ~/.claude.json to generate a comprehensive
HTML dashboard with all available metrics.

Data Sources (via aggregated history):
- stats-cache.json: Authoritative session/message counts, hour-of-day activity
- ~/.claude.json: User info, feature usage, project costs
- history.jsonl: Command patterns, slash command usage
- projects/*.jsonl: Detailed session transcripts, tool usage

Never modifies source files - read-only operation.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Constants
SOURCE_FILE = Path.home() / ".claude.json"
HISTORY_FILE = Path(__file__).parent.parent / "data" / "claude_history.json"
TEMPLATE_FILE = Path(__file__).parent.parent / "templates" / "claude_template.html"
OUTPUT_FILE = Path(__file__).parent.parent / "claude_dashboard.html"


def load_claude_data():
    """Load data from ~/.claude.json (read-only)"""
    try:
        with open(SOURCE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {SOURCE_FILE}: {e}")
        sys.exit(1)


def format_duration(ms):
    """Format milliseconds to human readable duration"""
    if not ms or ms == 0:
        return 'N/A'
    seconds = int(ms / 1000)
    minutes = seconds // 60
    hours = minutes // 60
    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"


def process_data(data):
    """Process and extract comprehensive statistics from ~/.claude.json"""
    stats = {
        'numStartups': data.get('numStartups', 0),
        'installMethod': data.get('installMethod', 'unknown'),
        'autoUpdates': data.get('autoUpdates', False),
        'tipsHistory': data.get('tipsHistory', {}),
        'promptQueueUseCount': data.get('promptQueueUseCount', 0),
        'userID': data.get('userID', 'N/A'),
        'firstStartTime': data.get('firstStartTime', 'N/A'),
        'hasCompletedOnboarding': data.get('hasCompletedOnboarding', False),
        'projects': {},
        'oauthAccount': data.get('oauthAccount', {}),
        'githubRepoPaths': data.get('githubRepoPaths', {}),
        'lastReleaseNotesSeen': data.get('lastReleaseNotesSeen', 'N/A'),
    }

    # Calculate days since first start
    first_start = data.get('firstStartTime', '')
    if first_start:
        try:
            first_date = datetime.fromisoformat(first_start.replace('Z', '+00:00'))
            days_using = (datetime.now(first_date.tzinfo) - first_date).days
            stats['daysUsing'] = days_using
            stats['firstStartDate'] = first_date.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            stats['daysUsing'] = 0
            stats['firstStartDate'] = 'N/A'
    else:
        stats['daysUsing'] = 0
        stats['firstStartDate'] = 'N/A'

    # Process projects
    projects = data.get('projects', {})
    total_cost = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_reads = 0
    total_cache_created = 0
    total_lines_added = 0
    total_lines_removed = 0
    total_duration = 0
    total_api_duration = 0
    total_web_searches = 0
    project_count_with_duration = 0

    model_usage = {
        'haiku': {'cost': 0, 'input': 0, 'output': 0, 'cache_read': 0, 'cache_create': 0},
        'sonnet': {'cost': 0, 'input': 0, 'output': 0, 'cache_read': 0, 'cache_create': 0},
        'opus': {'cost': 0, 'input': 0, 'output': 0, 'cache_read': 0, 'cache_create': 0},
    }

    for proj_path, proj_data in projects.items():
        cost = proj_data.get('lastCost', 0)
        total_cost += cost

        input_tokens = proj_data.get('lastTotalInputTokens', 0)
        output_tokens = proj_data.get('lastTotalOutputTokens', 0)
        cache_reads = proj_data.get('lastTotalCacheReadInputTokens', 0)
        cache_created = proj_data.get('lastTotalCacheCreationInputTokens', 0)
        lines_added = proj_data.get('lastLinesAdded', 0)
        lines_removed = proj_data.get('lastLinesRemoved', 0)
        duration = proj_data.get('lastDuration', 0)
        api_duration = proj_data.get('lastAPIDuration', 0)
        web_searches = proj_data.get('lastTotalWebSearchRequests', 0)

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cache_reads += cache_reads
        total_cache_created += cache_created
        total_lines_added += lines_added
        total_lines_removed += lines_removed
        total_web_searches += web_searches

        if duration > 0:
            total_duration += duration
            project_count_with_duration += 1
        if api_duration > 0:
            total_api_duration += api_duration

        last_model_usage = proj_data.get('lastModelUsage', {})
        for model_name, model_data in last_model_usage.items():
            model_cost = model_data.get('costUSD', 0)
            model_input = model_data.get('inputTokens', 0)
            model_output = model_data.get('outputTokens', 0)
            model_cache_read = model_data.get('cacheReadInputTokens', 0)
            model_cache_create = model_data.get('cacheCreationInputTokens', 0)

            if 'haiku' in model_name.lower():
                model_usage['haiku']['cost'] += model_cost
                model_usage['haiku']['input'] += model_input
                model_usage['haiku']['output'] += model_output
                model_usage['haiku']['cache_read'] += model_cache_read
                model_usage['haiku']['cache_create'] += model_cache_create
            elif 'sonnet' in model_name.lower():
                model_usage['sonnet']['cost'] += model_cost
                model_usage['sonnet']['input'] += model_input
                model_usage['sonnet']['output'] += model_output
                model_usage['sonnet']['cache_read'] += model_cache_read
                model_usage['sonnet']['cache_create'] += model_cache_create
            elif 'opus' in model_name.lower():
                model_usage['opus']['cost'] += model_cost
                model_usage['opus']['input'] += model_input
                model_usage['opus']['output'] += model_output
                model_usage['opus']['cache_read'] += model_cache_read
                model_usage['opus']['cache_create'] += model_cache_create

        stats['projects'][proj_path] = {
            'name': Path(proj_path).name,
            'cost': cost,
            'inputTokens': input_tokens,
            'outputTokens': output_tokens,
            'cacheReads': cache_reads,
            'cacheCreated': cache_created,
            'linesAdded': lines_added,
            'linesRemoved': lines_removed,
            'duration': duration,
            'apiDuration': api_duration,
            'webSearches': web_searches,
            'trusted': proj_data.get('hasTrustDialogAccepted', False),
            'modelUsage': last_model_usage,
        }

    stats['totalCost'] = total_cost
    stats['totalInputTokens'] = total_input_tokens
    stats['totalOutputTokens'] = total_output_tokens
    stats['totalCacheReads'] = total_cache_reads
    stats['totalCacheCreated'] = total_cache_created
    stats['totalLinesAdded'] = total_lines_added
    stats['totalLinesRemoved'] = total_lines_removed
    stats['totalWebSearches'] = total_web_searches
    stats['modelUsage'] = model_usage

    if project_count_with_duration > 0:
        stats['avgDuration'] = total_duration / project_count_with_duration
        stats['avgApiDuration'] = total_api_duration / project_count_with_duration
    else:
        stats['avgDuration'] = 0
        stats['avgApiDuration'] = 0

    total_cache = total_cache_reads + total_cache_created
    if total_cache > 0:
        stats['cacheHitRatio'] = round((total_cache_reads / total_cache) * 100, 1)
    else:
        stats['cacheHitRatio'] = 0

    return stats


def load_history_data():
    """Load aggregated history data"""
    if not HISTORY_FILE.exists():
        print(f"  ⚠️  History file not found: {HISTORY_FILE}")
        print("     Run aggregate_claude_history.py first")
        return None

    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠️  Error loading history: {e}")
        return None


def process_history_data(history):
    """Process comprehensive history data for dashboard"""
    if not history:
        return {
            'dailyStats': [],
            'sessionLengths': [],
            'hourlyRolling': [],
            'weekdayRolling': [],
            'modelOverTime': [],
            'projectComparison': [],
            'toolUsage': [],
            'slashCommands': [],
            'authoritativeHourCounts': {},
            'longestSession': {},
            'commandHistory': {},
            'sessionBreakdown': {'main': 0, 'agent': 0},
        }

    daily_stats = history.get('daily_stats', [])
    sessions = history.get('sessions', [])
    project_stats = history.get('project_stats', {})
    authoritative = history.get('authoritative_stats', {})
    command_history = history.get('command_history', {})
    global_tools = history.get('global_tools_used', {})
    summary = history.get('summary', {})

    # 1. Daily Activity
    daily_activity = [
        {
            'date': day['date'],
            'sessions': day['sessions'],
            'mainSessions': day.get('main_sessions', 0),
            'agentSessions': day.get('agent_sessions', 0),
            'messages': day['messages'],
            'toolCalls': day['tool_calls']
        }
        for day in daily_stats
    ]

    # 2. Session Length Distribution
    session_lengths = []
    ranges = [(1, 5, '1-5'), (6, 20, '6-20'), (21, 50, '21-50'), (51, 100, '51-100'),
              (101, 200, '101-200'), (201, 500, '201-500'), (501, 2000, '500+')]
    lengths = [s['message_count'] for s in sessions]
    for low, high, label in ranges:
        count = len([l for l in lengths if low <= l <= high])
        session_lengths.append({'range': label, 'count': count})

    # 3. Hourly Activity with Rolling 7-day average
    hourly_by_date = defaultdict(lambda: defaultdict(int))
    for s in sessions:
        if s.get('start_time'):
            try:
                date = s['start_time'][:10]
                hour = int(s['start_time'][11:13])
                hourly_by_date[date][hour] += 1
            except (KeyError, TypeError, ValueError, IndexError):
                pass

    dates = sorted(hourly_by_date.keys())
    hourly_rolling = []
    for i, date in enumerate(dates):
        window_dates = dates[max(0, i-6):i+1]
        hour_avgs = {}
        for hour in range(24):
            total = sum(hourly_by_date[d].get(hour, 0) for d in window_dates)
            hour_avgs[hour] = round(total / len(window_dates), 2)
        hourly_rolling.append({'date': date, 'hours': hour_avgs})

    # 4. Weekday Activity
    weekday_by_date = defaultdict(lambda: {'sessions': 0, 'messages': 0})
    for day in daily_stats:
        try:
            dt = datetime.strptime(day['date'], '%Y-%m-%d')
            weekday = dt.strftime('%A')
            weekday_by_date[day['date']] = {
                'weekday': weekday,
                'sessions': day['sessions'],
                'messages': day['messages']
            }
        except (KeyError, ValueError):
            pass

    weekday_rolling = []
    for i, date in enumerate(sorted(weekday_by_date.keys())):
        window_dates = sorted(weekday_by_date.keys())[max(0, i-6):i+1]
        weekday_totals = defaultdict(lambda: {'sessions': 0, 'messages': 0, 'count': 0})
        for d in window_dates:
            wd = weekday_by_date[d]['weekday']
            weekday_totals[wd]['sessions'] += weekday_by_date[d]['sessions']
            weekday_totals[wd]['messages'] += weekday_by_date[d]['messages']
            weekday_totals[wd]['count'] += 1

        weekday_avgs = {}
        for wd in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            if weekday_totals[wd]['count'] > 0:
                weekday_avgs[wd] = round(weekday_totals[wd]['messages'] / weekday_totals[wd]['count'], 1)
            else:
                weekday_avgs[wd] = 0

        weekday_rolling.append({'date': date, 'weekdays': weekday_avgs})

    # 5. Model Usage Over Time
    model_over_time = []
    for day in daily_stats:
        models = day.get('models', {})
        haiku_tokens = sonnet_tokens = opus_tokens = 0
        for model, usage in models.items():
            tokens = usage.get('tokens', 0)
            if 'haiku' in model.lower():
                haiku_tokens += tokens
            elif 'sonnet' in model.lower():
                sonnet_tokens += tokens
            elif 'opus' in model.lower():
                opus_tokens += tokens
        model_over_time.append({
            'date': day['date'],
            'haiku': haiku_tokens,
            'sonnet': sonnet_tokens,
            'opus': opus_tokens
        })

    # 6. Project Comparison
    project_comparison = []
    for proj_path, stats in project_stats.items():
        proj_name = proj_path.split('-')[-1][:20]
        project_comparison.append({
            'name': proj_name,
            'path': proj_path,
            'sessions': stats['sessions'],
            'mainSessions': stats.get('main_sessions', 0),
            'agentSessions': stats.get('agent_sessions', 0),
            'messages': stats['messages'],
            'tokens': stats['input_tokens'] + stats['output_tokens']
        })
    project_comparison.sort(key=lambda x: -x['messages'])

    # 7. Tool Usage (top 15)
    tool_usage = sorted(global_tools.items(), key=lambda x: -x[1])[:15]
    tool_usage = [{'name': t, 'count': c} for t, c in tool_usage]

    # 8. Slash Commands from command history
    slash_commands = command_history.get('slash_commands', {})
    slash_cmd_list = sorted(slash_commands.items(), key=lambda x: -x[1])[:10]
    slash_cmd_list = [{'name': c, 'count': n} for c, n in slash_cmd_list]

    # 9. Authoritative hour counts
    auth_hour_counts = authoritative.get('hour_counts', {})

    # 10. Longest session info
    longest_session = authoritative.get('longest_session', {})

    # 11. Session breakdown
    session_breakdown = {
        'main': summary.get('main_sessions', 0),
        'agent': summary.get('agent_sessions', 0),
        'authoritative': summary.get('authoritative_sessions', 0),
    }

    return {
        'dailyStats': daily_activity,
        'sessionLengths': session_lengths,
        'hourlyRolling': hourly_rolling[-7:] if hourly_rolling else [],
        'weekdayRolling': weekday_rolling[-7:] if weekday_rolling else [],
        'modelOverTime': model_over_time,
        'projectComparison': project_comparison[:10],
        'toolUsage': tool_usage,
        'slashCommands': slash_cmd_list,
        'authoritativeHourCounts': auth_hour_counts,
        'longestSession': longest_session,
        'commandHistory': command_history,
        'sessionBreakdown': session_breakdown,
    }


def generate_html(stats, history_stats):
    """Generate the HTML dashboard from template"""

    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        sys.exit(1)

    # Prepare JSON data for JavaScript
    tips_data = json.dumps(stats['tipsHistory'])
    projects_data = json.dumps(stats['projects'])
    github_repos = json.dumps(stats['githubRepoPaths'])
    model_usage_js = json.dumps({
        'haiku': {'cost': stats['modelUsage']['haiku']['cost'], 'input': stats['modelUsage']['haiku']['input'], 'output': stats['modelUsage']['haiku']['output']},
        'sonnet': {'cost': stats['modelUsage']['sonnet']['cost'], 'input': stats['modelUsage']['sonnet']['input'], 'output': stats['modelUsage']['sonnet']['output']},
        'opus': {'cost': stats['modelUsage']['opus']['cost'], 'input': stats['modelUsage']['opus']['input'], 'output': stats['modelUsage']['opus']['output']},
    })

    # History data
    daily_stats_js = json.dumps(history_stats['dailyStats'])
    session_lengths_js = json.dumps(history_stats['sessionLengths'])
    hourly_rolling_js = json.dumps(history_stats['hourlyRolling'])
    weekday_rolling_js = json.dumps(history_stats['weekdayRolling'])
    model_over_time_js = json.dumps(history_stats['modelOverTime'])
    project_comparison_js = json.dumps(history_stats['projectComparison'])

    # New comprehensive data
    tool_usage_js = json.dumps(history_stats['toolUsage'])
    slash_commands_js = json.dumps(history_stats['slashCommands'])
    auth_hour_counts_js = json.dumps(history_stats['authoritativeHourCounts'])
    longest_session_js = json.dumps(history_stats['longestSession'])
    command_history_js = json.dumps(history_stats['commandHistory'])
    session_breakdown_js = json.dumps(history_stats['sessionBreakdown'])

    # User info
    user_name = stats['oauthAccount'].get('displayName', 'User')
    user_email = stats['oauthAccount'].get('emailAddress', 'N/A')
    org_role = stats['oauthAccount'].get('organizationRole', 'user').title()
    billing_type = stats['oauthAccount'].get('organizationBillingType', 'N/A').replace('_', ' ').title()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    net_lines = stats['totalLinesAdded'] - stats['totalLinesRemoved']
    net_lines_str = f"+{net_lines}" if net_lines >= 0 else str(net_lines)
    net_lines_color = 'text-green-400' if net_lines >= 0 else 'text-red-400'

    max_cache = max(stats['totalCacheReads'], stats['totalCacheCreated'], 1)
    cache_read_pct = min(100, (stats['totalCacheReads'] / max_cache) * 100) if max_cache > 0 else 0
    cache_create_pct = min(100, (stats['totalCacheCreated'] / max_cache) * 100) if max_cache > 0 else 0

    # Session breakdown for display
    main_sessions = history_stats['sessionBreakdown'].get('main', 0)
    agent_sessions = history_stats['sessionBreakdown'].get('agent', 0)
    auth_sessions = history_stats['sessionBreakdown'].get('authoritative', 0)

    # Longest session info
    longest = history_stats['longestSession']
    longest_msgs = longest.get('messageCount', 0)
    longest_duration = format_duration(longest.get('duration', 0))

    # Command history stats
    cmd_hist = history_stats['commandHistory']
    total_commands = cmd_hist.get('total_commands', 0)
    avg_prompt_len = cmd_hist.get('avg_prompt_length', 0)

    # All replacements
    replacements = {
        '{{USER_NAME}}': user_name,
        '{{USER_EMAIL}}': user_email,
        '{{ORG_ROLE}}': org_role,
        '{{BILLING_TYPE}}': billing_type,
        '{{LAST_VERSION}}': stats['lastReleaseNotesSeen'],
        '{{TIMESTAMP}}': timestamp,
        '{{FIRST_START_DATE}}': stats['firstStartDate'],
        '{{DAYS_USING}}': str(stats['daysUsing']),
        '{{NUM_STARTUPS}}': str(stats['numStartups']),
        '{{NUM_PROJECTS}}': str(len(stats['projects'])),
        '{{TOTAL_COST}}': f"${stats['totalCost']:.2f}",
        '{{TOTAL_LINES_ADDED}}': f"{stats['totalLinesAdded']:,}",
        '{{TOTAL_LINES_REMOVED}}': f"{stats['totalLinesRemoved']:,}",
        '{{NET_LINES}}': net_lines_str,
        '{{NET_LINES_COLOR}}': net_lines_color,
        '{{HAIKU_COST}}': f"${stats['modelUsage']['haiku']['cost']:.4f}",
        '{{HAIKU_INPUT}}': f"{stats['modelUsage']['haiku']['input']:,}",
        '{{HAIKU_OUTPUT}}': f"{stats['modelUsage']['haiku']['output']:,}",
        '{{SONNET_COST}}': f"${stats['modelUsage']['sonnet']['cost']:.4f}",
        '{{SONNET_INPUT}}': f"{stats['modelUsage']['sonnet']['input']:,}",
        '{{SONNET_OUTPUT}}': f"{stats['modelUsage']['sonnet']['output']:,}",
        '{{OPUS_COST}}': f"${stats['modelUsage']['opus']['cost']:.4f}",
        '{{OPUS_INPUT}}': f"{stats['modelUsage']['opus']['input']:,}",
        '{{OPUS_OUTPUT}}': f"{stats['modelUsage']['opus']['output']:,}",
        '{{TOTAL_CACHE_READS}}': f"{stats['totalCacheReads']:,}",
        '{{TOTAL_CACHE_CREATED}}': f"{stats['totalCacheCreated']:,}",
        '{{CACHE_READ_PCT}}': f"{cache_read_pct:.0f}",
        '{{CACHE_CREATE_PCT}}': f"{cache_create_pct:.0f}",
        '{{CACHE_HIT_RATIO}}': f"{stats['cacheHitRatio']:.1f}",
        '{{AVG_DURATION}}': format_duration(stats['avgDuration']),
        '{{AVG_API_DURATION}}': format_duration(stats['avgApiDuration']),
        '{{PROMPT_QUEUE_COUNT}}': str(stats['promptQueueUseCount']),
        '{{TOTAL_WEB_SEARCHES}}': str(stats['totalWebSearches']),
        # New comprehensive stats
        '{{MAIN_SESSIONS}}': str(main_sessions),
        '{{AGENT_SESSIONS}}': str(agent_sessions),
        '{{AUTH_SESSIONS}}': str(auth_sessions),
        '{{LONGEST_SESSION_MSGS}}': str(longest_msgs),
        '{{LONGEST_SESSION_DURATION}}': longest_duration,
        '{{TOTAL_COMMANDS}}': str(total_commands),
        '{{AVG_PROMPT_LENGTH}}': str(int(avg_prompt_len)),
        # JSON data
        '{{TIPS_DATA}}': tips_data,
        '{{PROJECTS_DATA}}': projects_data,
        '{{GITHUB_REPOS}}': github_repos,
        '{{MODEL_USAGE}}': model_usage_js,
        '{{DAILY_STATS}}': daily_stats_js,
        '{{SESSION_LENGTHS}}': session_lengths_js,
        '{{HOURLY_ROLLING}}': hourly_rolling_js,
        '{{WEEKDAY_ROLLING}}': weekday_rolling_js,
        '{{MODEL_OVER_TIME}}': model_over_time_js,
        '{{PROJECT_COMPARISON}}': project_comparison_js,
        '{{TOOL_USAGE}}': tool_usage_js,
        '{{SLASH_COMMANDS}}': slash_commands_js,
        '{{AUTH_HOUR_COUNTS}}': auth_hour_counts_js,
        '{{LONGEST_SESSION}}': longest_session_js,
        '{{COMMAND_HISTORY}}': command_history_js,
        '{{SESSION_BREAKDOWN}}': session_breakdown_js,
    }

    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, value)

    return html_content


def main():
    """Main function to generate the dashboard"""
    print("=" * 60)
    print("🎨 Claude Dashboard Generator - Comprehensive Edition")
    print("=" * 60)
    print()

    print(f"📖 Reading Claude data from {SOURCE_FILE}...")
    data = load_claude_data()

    print("📊 Processing project statistics...")
    stats = process_data(data)

    print("📈 Loading comprehensive history data...")
    history = load_history_data()
    history_stats = process_history_data(history)

    print(f"🎨 Generating HTML dashboard...")
    html = generate_html(stats, history_stats)

    print(f"💾 Writing dashboard to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Dashboard generated successfully!")
    print(f"📊 Location: {OUTPUT_FILE}")

    print(f"\n📈 Comprehensive Stats Summary:")
    print(f"   👤 User: {stats['oauthAccount'].get('displayName', 'N/A')}")
    print(f"   📅 Using Claude since: {stats['firstStartDate']} ({stats['daysUsing']} days)")
    print(f"   🚀 Total startups: {stats['numStartups']}")
    print(f"   📁 Total projects: {len(stats['projects'])}")
    print(f"   💰 Total cost: ${stats['totalCost']:.4f}")

    print(f"\n   📊 Session Breakdown:")
    print(f"      Main sessions: {history_stats['sessionBreakdown'].get('main', 0)}")
    print(f"      Agent sessions: {history_stats['sessionBreakdown'].get('agent', 0)}")
    print(f"      Authoritative count: {history_stats['sessionBreakdown'].get('authoritative', 0)}")

    longest = history_stats['longestSession']
    if longest:
        print(f"\n   🏆 Longest Session:")
        print(f"      Messages: {longest.get('messageCount', 0)}")
        print(f"      Duration: {format_duration(longest.get('duration', 0))}")

    cmd_hist = history_stats['commandHistory']
    if cmd_hist:
        print(f"\n   💬 Command History:")
        print(f"      Total commands: {cmd_hist.get('total_commands', 0)}")
        print(f"      Avg prompt length: {cmd_hist.get('avg_prompt_length', 0):.0f} chars")

    print(f"\n🌐 Open in browser: file://{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
