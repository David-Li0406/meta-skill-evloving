#!/usr/bin/env python3
"""
Hook Script Template

Description: [What this hook does]
Event: [PreToolUse/PostToolUse/SessionStart/etc]
Matcher: [Tool name if applicable]
Dependencies: [Required packages]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Add configuration here
PROTECTED_FILES = [".env", "secrets.json"]
LOG_FILE = os.path.join(
    os.environ.get("CLAUDE_PROJECT_DIR", "."),
    ".claude/logs/hook.log"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_message(message, level="INFO"):
    """Log message to stderr (visible to user)"""
    timestamp = datetime.now().isoformat()
    print(f"[{level}] {timestamp}: {message}", file=sys.stderr)


def validate_file_path(file_path):
    """Validate file path for security issues"""
    if not file_path:
        return False, "Empty file path"

    # Check for path traversal
    if ".." in file_path:
        return False, "Path traversal detected"

    # Check for system directories
    dangerous_paths = ["/etc", "/usr", "/sys", "/proc"]
    for dangerous in dangerous_paths:
        if file_path.startswith(dangerous):
            return False, f"Access to {dangerous} not allowed"

    return True, "Valid"


def output_json_response(decision="allow", additional_context=None, updated_input=None):
    """Output JSON response for hook control"""
    response = {"decision": decision}

    if additional_context:
        response["additionalContext"] = additional_context

    if updated_input:
        response["updatedInput"] = updated_input

    print(json.dumps(response))


# ============================================================================
# MAIN HOOK LOGIC
# ============================================================================

def process_hook(input_data):
    """
    Main hook processing logic

    Args:
        input_data: Dictionary containing hook input

    Returns:
        int: Exit code (0 = allow, 2 = block, other = non-blocking error)
    """

    # Extract common fields
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    session_id = input_data.get("session_id", "")
    cwd = input_data.get("cwd", "")

    # Debug logging (optional, comment out in production)
    # log_message(f"Hook triggered for tool: {tool_name}")

    # ========================================================================
    # ADD YOUR VALIDATION LOGIC HERE
    # ========================================================================

    # Example: Tool-specific logic
    # if tool_name == "Write":
    #     file_path = tool_input.get("file_path", "")
    #
    #     # Validate path
    #     is_valid, message = validate_file_path(file_path)
    #     if not is_valid:
    #         log_message(f"BLOCKED: {message}", level="ERROR")
    #         return 2  # Block operation
    #
    #     # Check protected files
    #     for protected in PROTECTED_FILES:
    #         if protected in file_path:
    #             log_message(f"WARNING: Writing to protected file: {file_path}", level="WARN")
    #             # Decide: warn and allow (return 0) or block (return 2)

    # ========================================================================
    # ADD YOUR PROCESSING LOGIC HERE
    # ========================================================================

    # Example: Logging
    # try:
    #     with open(LOG_FILE, "a") as f:
    #         log_entry = {
    #             "timestamp": datetime.now().isoformat(),
    #             "tool": tool_name,
    #             "session": session_id
    #         }
    #         f.write(json.dumps(log_entry) + "\n")
    # except Exception as e:
    #     log_message(f"Logging error: {e}", level="ERROR")

    # Example: Modify input (PreToolUse)
    # if tool_name == "Write" and file_path.endswith(".py"):
    #     content = tool_input.get("content", "")
    #     if not content.startswith("#!/usr/bin/env python3"):
    #         # Add shebang
    #         modified_content = "#!/usr/bin/env python3\n\n" + content
    #         updated_input = tool_input.copy()
    #         updated_input["content"] = modified_content
    #
    #         output_json_response(
    #             decision="allow",
    #             additional_context=f"Added shebang to {file_path}",
    #             updated_input=updated_input
    #         )
    #         return 0

    # ========================================================================
    # DEFAULT BEHAVIOR
    # ========================================================================

    # Allow operation by default
    return 0


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for hook script"""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Process the hook
        exit_code = process_hook(input_data)

        # Exit with appropriate code
        sys.exit(exit_code)

    except json.JSONDecodeError as e:
        log_message(f"JSON parsing error: {e}", level="ERROR")
        sys.exit(0)  # Fail safely, don't block

    except Exception as e:
        log_message(f"Hook error: {e}", level="ERROR")
        sys.exit(0)  # Fail safely, don't block


if __name__ == "__main__":
    main()


# ============================================================================
# NOTES
# ============================================================================
# Exit Codes:
#   0: Allow operation (success)
#   2: Block operation (PreToolUse only)
#   Other: Non-blocking error
#
# Output:
#   - Use sys.stderr for user-visible messages
#   - Use sys.stdout for JSON control responses
#   - JSON format: {"decision": "allow|block", "additionalContext": "...", "updatedInput": {...}}
#
# Environment Variables:
#   - CLAUDE_PROJECT_DIR: Project root directory
#   - CLAUDE_ENV_FILE: Environment persistence file (SessionStart only)
#   - CLAUDE_CODE_REMOTE: Remote execution indicator
#
# Testing:
#   echo '{"tool_name":"Write","tool_input":{"file_path":"/test.txt"}}' | python3 hook-script.py
#   echo "Exit code: $?"
#
# Make Executable:
#   chmod +x hook-script.py
#
# Security:
#   - Always validate inputs
#   - Quote file paths
#   - Check for path traversal
#   - Never expose sensitive data in logs
#   - Use absolute paths or validated relative paths
