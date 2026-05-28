#!/usr/bin/env python3
"""
push_notify.py - Send push notifications via ntfy.sh when Claude Code needs attention.

Usage:
    python3 push_notify.py <event_type>

Event types:
    ask_question - Claude is asking a question via AskUserQuestion tool
    permission   - Claude needs permission for a dangerous action
    stop         - Claude session has ended

Hook data is read from stdin as JSON.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Configuration - try environment first, then config file
def load_config():
    """Load ntfy config from environment or config file."""
    # First try environment variables
    enabled = os.environ.get('NTFY_ENABLED', '').lower() == 'true'
    topic = os.environ.get('NTFY_TOPIC', '')
    server = os.environ.get('NTFY_SERVER', 'https://ntfy.sh')
    rate_limit = os.environ.get('NTFY_RATE_LIMIT', '15')

    # If not in env, try config file
    if not topic:
        config_file = Path.home() / ".claude" / "ntfy.conf"
        if config_file.exists():
            try:
                for line in config_file.read_text().splitlines():
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip("'\"")
                        if key == 'NTFY_ENABLED':
                            enabled = value.lower() == 'true'
                        elif key == 'NTFY_TOPIC':
                            topic = value
                        elif key == 'NTFY_SERVER':
                            server = value
                        elif key == 'NTFY_RATE_LIMIT':
                            rate_limit = value
            except Exception:
                pass

    return enabled, topic, server, int(rate_limit)

NTFY_ENABLED, NTFY_TOPIC, NTFY_SERVER, NTFY_RATE_LIMIT = load_config()

# Rate limiting state file
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
RATE_LIMIT_FILE = SKILLS_DIR / ".skill-system" / "ntfy-ratelimit.json"


def is_rate_limited():
    """Check if notifications are rate-limited."""
    try:
        if RATE_LIMIT_FILE.exists():
            data = json.loads(RATE_LIMIT_FILE.read_text())
            last_sent = data.get('last_sent', 0)
            if time.time() - last_sent < NTFY_RATE_LIMIT:
                return True
    except Exception:
        pass
    return False


def update_rate_limit():
    """Update rate limit timestamp."""
    try:
        RATE_LIMIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        RATE_LIMIT_FILE.write_text(json.dumps({
            'last_sent': time.time(),
            'last_sent_iso': datetime.utcnow().isoformat() + 'Z'
        }))
    except Exception:
        pass


def send_notification(message, title=None, priority='default', tags=None):
    """
    Send a push notification via ntfy.sh.

    Args:
        message: Notification body text
        title: Optional notification title
        priority: 'min', 'low', 'default', 'high', 'urgent'
        tags: List of emoji tags (e.g., ['robot', 'question'])

    Returns:
        True if sent successfully, False otherwise
    """
    if not NTFY_ENABLED or not NTFY_TOPIC:
        return False

    if is_rate_limited():
        return False

    try:
        url = f"{NTFY_SERVER.rstrip('/')}/{NTFY_TOPIC}"

        headers = {
            'Content-Type': 'text/plain; charset=utf-8'
        }

        if title:
            headers['Title'] = title
        if priority and priority != 'default':
            headers['Priority'] = priority
        if tags:
            headers['Tags'] = ','.join(tags)

        req = urllib.request.Request(
            url,
            data=message.encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                update_rate_limit()
                return True
    except urllib.error.URLError:
        pass  # Network error - fail silently
    except Exception:
        pass  # Any other error - fail silently

    return False


def get_session_context(hook_data):
    """Extract session context (project/directory) from hook data."""
    try:
        # Try session_cwd first (most reliable for identifying which session)
        cwd = hook_data.get('session_cwd', '')
        if cwd:
            # Return last directory component
            return Path(cwd).name

        # Fall back to transcript path
        transcript_path = hook_data.get('transcript_path', '')
        if transcript_path:
            # Transcript path like: ~/.claude/projects/<encoded-path>/transcripts/<id>.jsonl
            # Extract project directory from path
            parts = Path(transcript_path).parts
            if 'projects' in parts:
                idx = parts.index('projects')
                if idx + 1 < len(parts):
                    # Decode the project path (it's usually URL-encoded)
                    project = parts[idx + 1]
                    # Return last meaningful segment
                    return project.split('%2F')[-1] if '%2F' in project else project
    except:
        pass
    return None


def get_last_user_prompt(transcript_path):
    """Read transcript to find the last user prompt for context."""
    try:
        if not transcript_path:
            return None
        path = Path(transcript_path)
        if not path.exists():
            return None

        lines = path.read_text().strip().split('\n')
        for line in reversed(lines):
            try:
                entry = json.loads(line)
                if entry.get('type') == 'user':
                    message = entry.get('message', {})
                    content = message.get('content', '')
                    if isinstance(content, str) and content.strip():
                        # Return first ~15 chars of prompt
                        prompt = content.strip()[:15]
                        if len(content.strip()) > 15:
                            prompt += '...'
                        return prompt
            except:
                continue
    except:
        pass
    return None


def get_pending_tool_from_transcript(transcript_path):
    """Read transcript to find the pending tool call for more context."""
    try:
        if not transcript_path:
            return None, None
        path = Path(transcript_path)
        if not path.exists():
            return None, None

        # Read last few lines to find the pending tool call
        lines = path.read_text().strip().split('\n')
        for line in reversed(lines[-10:]):  # Check last 10 entries
            try:
                entry = json.loads(line)
                # Look for assistant message with tool_use
                if entry.get('type') == 'assistant':
                    message = entry.get('message', {})
                    content = message.get('content', [])
                    for block in content:
                        if block.get('type') == 'tool_use':
                            return block.get('name'), block.get('input', {})
            except:
                continue
    except:
        pass
    return None, None


def handle_ask_question(hook_data):
    """Handle AskUserQuestion tool notification with question and options."""
    tool_input = hook_data.get('tool_input', {})
    questions = tool_input.get('questions', [])

    # Get session and prompt context for title
    session = get_session_context(hook_data)
    transcript_path = hook_data.get('transcript_path')
    prompt_context = get_last_user_prompt(transcript_path)

    # Build title with available context
    if session and prompt_context:
        base_title = f'[{session}] {prompt_context}'
    elif session:
        base_title = f'[{session}] Question'
    elif prompt_context:
        base_title = f'Q: {prompt_context}'
    else:
        base_title = 'Question'

    if not questions:
        send_notification(
            message='Claude needs your input',
            title=base_title,
            priority='high',
            tags=['question']
        )
        return

    # Get the first question
    q = questions[0]
    question_text = q.get('question', 'Claude needs your input')
    options = q.get('options', [])

    # Build message with options if available
    if options:
        option_labels = [opt.get('label', '') for opt in options[:4]]  # Max 4 options
        options_str = ' | '.join(option_labels)
        message = f"{question_text}\n→ {options_str}"
    else:
        message = question_text

    send_notification(
        message=message[:250],
        title=base_title,
        priority='high',
        tags=['question']
    )


def handle_permission(hook_data):
    """Handle permission_prompt notification with detailed context."""
    base_message = hook_data.get('message', 'Permission required')
    transcript_path = hook_data.get('transcript_path')

    # Get session and prompt context for title
    session = get_session_context(hook_data)
    prompt_context = get_last_user_prompt(transcript_path)

    # Build title with available context
    if session and prompt_context:
        title = f'[{session}] {prompt_context}'
    elif session:
        title = f'[{session}] Permission'
    elif prompt_context:
        title = f'Permission: {prompt_context}'
    else:
        title = 'Permission needed'

    # Try to get more details from transcript
    tool_name, tool_input = get_pending_tool_from_transcript(transcript_path)

    if tool_name == 'Bash' and tool_input:
        cmd = tool_input.get('command', '')[:150]
        message = f"$ {cmd}"
    elif tool_name in ['Write', 'Edit'] and tool_input:
        file_path = tool_input.get('file_path', 'unknown')
        message = f"{tool_name}: {file_path}"
    elif tool_name:
        message = f"{tool_name}: {base_message}"
    else:
        message = base_message

    send_notification(
        message=message[:200],
        title=title,
        priority='high',
        tags=['warning', 'lock']
    )


def handle_permission_request(hook_data):
    """Handle PermissionRequest hook - fires when permission dialog shown."""
    tool_name = hook_data.get('tool_name', 'Unknown tool')
    tool_input = hook_data.get('tool_input', {})

    # Get session context for title
    session = get_session_context(hook_data)
    title = f'[{session}] Permission' if session else 'Claude needs permission'

    # Build a descriptive message
    if tool_name == 'Bash':
        cmd = tool_input.get('command', '')[:100]
        message = f"Run: {cmd}"
    elif tool_name in ['Write', 'Edit']:
        path = tool_input.get('file_path', 'unknown file')
        message = f"{tool_name}: {path}"
    else:
        message = f"Use {tool_name} tool"

    send_notification(
        message=message,
        title=title,
        priority='high',
        tags=['warning', 'lock']
    )


def handle_stop(hook_data):
    """Handle session stop notification."""
    session = get_session_context(hook_data)
    transcript_path = hook_data.get('transcript_path')
    prompt_context = get_last_user_prompt(transcript_path)

    # Build title with available context
    if session and prompt_context:
        title = f'[{session}] {prompt_context}'
    elif session:
        title = f'[{session}] Complete'
    elif prompt_context:
        title = f'Done: {prompt_context}'
    else:
        title = 'Session complete'

    send_notification(
        message='Claude session has ended',
        title=title,
        priority='default',
        tags=['white_check_mark']
    )


def main():
    # Debug logging
    debug_file = SKILLS_DIR / ".skill-system" / "patterns" / "push-notify-debug.log"
    try:
        debug_file.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_file, "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} - Called with args: {sys.argv}\n")
    except:
        pass

    if len(sys.argv) < 2:
        sys.exit(0)

    event_type = sys.argv[1]

    # Read hook data from stdin
    try:
        hook_data = json.load(sys.stdin)
        # Log what we received
        try:
            with open(debug_file, "a") as f:
                f.write(f"  Data: {json.dumps(hook_data)[:500]}\n")
        except:
            pass
    except Exception:
        hook_data = {}

    # Handle based on event type
    if event_type == 'ask_question':
        handle_ask_question(hook_data)
    elif event_type == 'permission':
        handle_permission(hook_data)
    elif event_type == 'permission_request':
        handle_permission_request(hook_data)
    elif event_type == 'pretool':
        handle_permission_request(hook_data)  # Same handler - fires before tool execution
    elif event_type == 'stop':
        handle_stop(hook_data)
    elif event_type == 'notification_debug':
        # Debug: send notification for ANY notification event
        notif_type = hook_data.get('notification_type', 'unknown')
        message = hook_data.get('message', 'No message')[:150]
        send_notification(
            message=f"[{notif_type}] {message}",
            title='Debug: Notification',
            priority='high',
            tags=['bell']
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
