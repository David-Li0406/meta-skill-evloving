#!/usr/bin/env python3
"""
analyze-errors.py

Analyzes error logs from Google Cloud Logging, groups similar errors,
identifies patterns, and provides root cause insights.

Usage:
    python3 analyze-errors.py /tmp/gcp-errors.json [--format=text|json]

No external dependencies required - uses Python standard library only.
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any


# Common error patterns and their root causes
ERROR_PATTERNS = {
    r"permission denied|403|forbidden": {
        "type": "Authorization Error",
        "cause": "IAM permissions missing or insufficient",
        "actions": [
            "Check service account permissions",
            "Verify IAM roles are correctly assigned",
            "Ensure API is enabled for the project",
        ],
    },
    r"unauthenticated|401|unauthorized": {
        "type": "Authentication Error",
        "cause": "Missing or invalid authentication credentials",
        "actions": [
            "Check if auth token is being sent",
            "Verify token is not expired",
            "Ensure correct authentication flow",
        ],
    },
    r"memory limit|out of memory|container killed|oom": {
        "type": "Memory Limit Exceeded",
        "cause": "Function using more memory than allocated",
        "actions": [
            "Increase memory allocation in function config",
            "Optimize code to reduce memory usage",
            "Check for memory leaks",
        ],
    },
    r"timeout|execution.*timeout|deadline exceeded": {
        "type": "Timeout Error",
        "cause": "Function execution exceeded timeout limit",
        "actions": [
            "Increase timeout setting",
            "Optimize slow operations",
            "Consider breaking into smaller functions",
        ],
    },
    r"quota exceeded|rate limit|too many requests|429": {
        "type": "Quota/Rate Limit Error",
        "cause": "API quota or rate limit reached",
        "actions": [
            "Request quota increase in GCP console",
            "Implement exponential backoff",
            "Add rate limiting to your code",
        ],
    },
    r"connection refused|econnrefused|connect failed": {
        "type": "Connection Refused",
        "cause": "Unable to connect to external service",
        "actions": [
            "Check if target service is running",
            "Verify VPC connector configuration",
            "Check firewall rules",
        ],
    },
    r"dns.*failed|enotfound|getaddrinfo": {
        "type": "DNS Resolution Error",
        "cause": "Cannot resolve hostname",
        "actions": [
            "Verify hostname spelling",
            "Check DNS configuration",
            "Consider using IP address directly",
        ],
    },
    r"ssl|certificate|tls|x509": {
        "type": "SSL/TLS Error",
        "cause": "Certificate validation failed",
        "actions": [
            "Check certificate validity and expiration",
            "Verify certificate chain is complete",
            "Update CA certificates if needed",
        ],
    },
    r"typeerror|cannot read property|undefined is not": {
        "type": "JavaScript TypeError",
        "cause": "Accessing property of undefined/null",
        "actions": [
            "Add null checks or optional chaining (?.)",
            "Verify data structure before access",
            "Check function arguments",
        ],
    },
    r"referenceerror|is not defined": {
        "type": "JavaScript ReferenceError",
        "cause": "Variable not declared or out of scope",
        "actions": [
            "Check variable spelling",
            "Verify import statements",
            "Check variable scope",
        ],
    },
    r"syntaxerror|unexpected token|parsing error": {
        "type": "Syntax Error",
        "cause": "Invalid code syntax or malformed data",
        "actions": [
            "Check for syntax errors in code",
            "Validate JSON/YAML data",
            "Look for missing brackets/quotes",
        ],
    },
    r"modulenotfounderror|cannot find module|no module named": {
        "type": "Module Not Found",
        "cause": "Missing dependency",
        "actions": [
            "Check package.json/requirements.txt",
            "Verify dependency is installed",
            "Redeploy the function",
        ],
    },
    r"cold start|initialization|init timeout": {
        "type": "Cold Start Issue",
        "cause": "Function initialization taking too long",
        "actions": [
            "Reduce global scope initialization",
            "Use lazy loading for dependencies",
            "Consider minimum instances setting",
        ],
    },
    r"environment variable|env.*not set|missing.*config": {
        "type": "Configuration Error",
        "cause": "Missing environment variable or config",
        "actions": [
            "Check function environment variables",
            "Verify all required config is set",
            "Review deployment configuration",
        ],
    },
}


def load_logs(file_path: str) -> list[dict[str, Any]]:
    """Load logs from JSON file."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return [data]
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def extract_message(log_entry: dict[str, Any]) -> str:
    """Extract error message from log entry."""
    # Try different fields where message might be stored
    if "textPayload" in log_entry:
        return log_entry["textPayload"]

    if "jsonPayload" in log_entry:
        payload = log_entry["jsonPayload"]
        if isinstance(payload, dict):
            # Common fields for error messages
            for field in ["message", "error", "msg", "errorMessage", "stack"]:
                if field in payload:
                    val = payload[field]
                    if isinstance(val, str):
                        return val
                    return str(val)
            # Return JSON representation if no known field
            return json.dumps(payload)
        return str(payload)

    if "protoPayload" in log_entry:
        payload = log_entry["protoPayload"]
        if isinstance(payload, dict):
            if "status" in payload:
                status = payload["status"]
                if isinstance(status, dict) and "message" in status:
                    return status["message"]
            return json.dumps(payload)

    return "Unknown error (no message found)"


def normalize_message(message: str) -> str:
    """Normalize error message for grouping similar errors."""
    normalized = message

    # Replace specific values with placeholders
    # UUIDs
    normalized = re.sub(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "<UUID>",
        normalized,
        flags=re.IGNORECASE,
    )
    # Timestamps
    normalized = re.sub(
        r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.\d]*Z?", "<TIMESTAMP>", normalized
    )
    # Numbers (but preserve error codes like 404, 500)
    normalized = re.sub(r"(?<![0-9])\d{5,}(?![0-9])", "<NUMBER>", normalized)
    # IP addresses
    normalized = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "<IP>", normalized)
    # File paths with line numbers
    normalized = re.sub(r":\d+:\d+", ":<LINE>", normalized)
    # Hex addresses
    normalized = re.sub(r"0x[0-9a-f]+", "<HEX>", normalized, flags=re.IGNORECASE)
    # Email addresses
    normalized = re.sub(r"[\w.-]+@[\w.-]+\.\w+", "<EMAIL>", normalized)

    return normalized.strip()


def extract_timestamp(log_entry: dict[str, Any]) -> datetime | None:
    """Extract timestamp from log entry."""
    ts = log_entry.get("timestamp") or log_entry.get("receiveTimestamp")
    if ts:
        try:
            # Handle various timestamp formats
            ts = ts.replace("Z", "+00:00")
            if "." in ts:
                # Truncate microseconds if too long
                parts = ts.split(".")
                if len(parts) == 2:
                    frac = parts[1].split("+")[0].split("-")[0]
                    tz = "+" + parts[1].split("+")[1] if "+" in parts[1] else ""
                    ts = f"{parts[0]}.{frac[:6]}{tz}"
            return datetime.fromisoformat(ts)
        except (ValueError, IndexError):
            pass
    return None


def extract_function_name(log_entry: dict[str, Any]) -> str:
    """Extract Cloud Function name from log entry."""
    resource = log_entry.get("resource", {})
    labels = resource.get("labels", {})
    return labels.get("function_name", "unknown")


def extract_severity(log_entry: dict[str, Any]) -> str:
    """Extract severity from log entry."""
    return log_entry.get("severity", "UNKNOWN")


def identify_error_type(message: str) -> dict[str, Any] | None:
    """Identify error type based on message patterns."""
    message_lower = message.lower()
    for pattern, info in ERROR_PATTERNS.items():
        if re.search(pattern, message_lower):
            return info
    return None


def group_errors(logs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group errors by normalized message."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for log in logs:
        message = extract_message(log)
        normalized = normalize_message(message)
        groups[normalized].append(
            {
                "original_message": message,
                "timestamp": extract_timestamp(log),
                "function_name": extract_function_name(log),
                "severity": extract_severity(log),
                "raw": log,
            }
        )

    return dict(groups)


def calculate_time_distribution(
    errors: list[dict[str, Any]]
) -> dict[str, int]:
    """Calculate error distribution by hour."""
    distribution: dict[str, int] = defaultdict(int)

    for error in errors:
        ts = error.get("timestamp")
        if ts:
            hour_key = ts.strftime("%Y-%m-%d %H:00")
            distribution[hour_key] += 1

    return dict(sorted(distribution.items()))


def analyze_errors(logs: list[dict[str, Any]]) -> dict[str, Any]:
    """Perform full error analysis."""
    if not logs:
        return {
            "total_errors": 0,
            "unique_patterns": 0,
            "error_groups": [],
            "time_distribution": {},
            "summary": "No errors found in the provided logs.",
        }

    groups = group_errors(logs)

    # Get time range
    all_timestamps = [
        extract_timestamp(log) for log in logs if extract_timestamp(log)
    ]
    time_range = {}
    if all_timestamps:
        time_range = {
            "start": min(all_timestamps).isoformat(),
            "end": max(all_timestamps).isoformat(),
        }

    # Process each group
    error_groups = []
    all_errors_flat = []

    for normalized_msg, errors in groups.items():
        all_errors_flat.extend(errors)

        # Get unique functions affected
        functions = list(set(e["function_name"] for e in errors))

        # Get timestamps
        timestamps = [e["timestamp"] for e in errors if e["timestamp"]]

        # Identify error type
        sample_message = errors[0]["original_message"]
        error_info = identify_error_type(sample_message)

        group_data = {
            "pattern": normalized_msg[:200],  # Truncate long patterns
            "count": len(errors),
            "percentage": round(len(errors) / len(logs) * 100, 1),
            "first_seen": min(timestamps).isoformat() if timestamps else None,
            "last_seen": max(timestamps).isoformat() if timestamps else None,
            "affected_functions": functions,
            "sample_message": sample_message[:500],  # Truncate long messages
            "severity": errors[0]["severity"],
        }

        if error_info:
            group_data["error_type"] = error_info["type"]
            group_data["root_cause"] = error_info["cause"]
            group_data["recommended_actions"] = error_info["actions"]
        else:
            group_data["error_type"] = "Unclassified Error"
            group_data["root_cause"] = "Unable to automatically determine root cause"
            group_data["recommended_actions"] = [
                "Review the error message and stack trace",
                "Search for the error message in documentation",
                "Add logging around the failure point",
                "Check recent code changes",
            ]

        error_groups.append(group_data)

    # Sort by count (most frequent first)
    error_groups.sort(key=lambda x: x["count"], reverse=True)

    # Calculate time distribution
    time_dist = calculate_time_distribution(all_errors_flat)

    # Determine trend
    trend = "stable"
    if len(time_dist) >= 2:
        values = list(time_dist.values())
        first_half_avg = sum(values[: len(values) // 2]) / max(1, len(values) // 2)
        second_half_avg = sum(values[len(values) // 2 :]) / max(
            1, len(values) - len(values) // 2
        )
        if second_half_avg > first_half_avg * 1.5:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.5:
            trend = "decreasing"

    return {
        "total_errors": len(logs),
        "unique_patterns": len(groups),
        "time_range": time_range,
        "error_groups": error_groups,
        "time_distribution": time_dist,
        "trend": trend,
        "top_error_type": error_groups[0]["error_type"] if error_groups else None,
        "most_affected_function": (
            error_groups[0]["affected_functions"][0] if error_groups else None
        ),
    }


def format_text_output(analysis: dict[str, Any]) -> str:
    """Format analysis as readable text."""
    lines = []

    lines.append("=" * 60)
    lines.append("GCP ERROR ANALYSIS RESULTS")
    lines.append("=" * 60)
    lines.append("")

    # Summary
    lines.append(f"Total Errors:     {analysis['total_errors']}")
    lines.append(f"Unique Patterns:  {analysis['unique_patterns']}")

    if analysis.get("time_range"):
        lines.append(f"Time Range:       {analysis['time_range'].get('start', 'N/A')}")
        lines.append(f"                  to {analysis['time_range'].get('end', 'N/A')}")

    lines.append(f"Trend:            {analysis.get('trend', 'N/A')}")
    lines.append("")

    if not analysis["error_groups"]:
        lines.append("No errors found.")
        return "\n".join(lines)

    # Error groups
    lines.append("-" * 60)
    lines.append("ERROR PATTERNS (sorted by frequency)")
    lines.append("-" * 60)
    lines.append("")

    for i, group in enumerate(analysis["error_groups"][:10], 1):  # Top 10
        lines.append(f"### {i}. {group['error_type']}")
        lines.append(f"    Occurrences: {group['count']} ({group['percentage']}%)")
        lines.append(f"    Severity:    {group['severity']}")
        lines.append(f"    First Seen:  {group.get('first_seen', 'N/A')}")
        lines.append(f"    Last Seen:   {group.get('last_seen', 'N/A')}")
        lines.append(f"    Functions:   {', '.join(group['affected_functions'])}")
        lines.append("")
        lines.append(f"    Pattern: {group['pattern'][:100]}...")
        lines.append("")
        lines.append(f"    Root Cause: {group['root_cause']}")
        lines.append("")
        lines.append("    Recommended Actions:")
        for action in group.get("recommended_actions", []):
            lines.append(f"      - {action}")
        lines.append("")
        lines.append("-" * 40)
        lines.append("")

    # Time distribution
    if analysis.get("time_distribution"):
        lines.append("-" * 60)
        lines.append("TIME DISTRIBUTION")
        lines.append("-" * 60)
        lines.append("")

        max_count = max(analysis["time_distribution"].values())
        for hour, count in list(analysis["time_distribution"].items())[-24:]:
            bar_length = int((count / max_count) * 30) if max_count > 0 else 0
            bar = "#" * bar_length
            lines.append(f"  {hour}: {bar} ({count})")
        lines.append("")

    lines.append("=" * 60)
    lines.append("END OF ANALYSIS")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 analyze-errors.py <log-file.json> [--format=text|json]")
        print("")
        print("Arguments:")
        print("  log-file.json    JSON file from fetch-errors.sh")
        print("  --format=text    Human-readable output (default)")
        print("  --format=json    JSON output for programmatic use")
        sys.exit(1)

    file_path = sys.argv[1]
    output_format = "text"

    for arg in sys.argv[2:]:
        if arg.startswith("--format="):
            output_format = arg.split("=")[1]

    # Load and analyze
    logs = load_logs(file_path)
    analysis = analyze_errors(logs)

    # Output
    if output_format == "json":
        print(json.dumps(analysis, indent=2, default=str))
    else:
        print(format_text_output(analysis))


if __name__ == "__main__":
    main()
