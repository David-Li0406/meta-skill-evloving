#!/usr/bin/env python3
"""
Execute shell commands safely
"""
import argparse
import json
import os
import subprocess
import sys
import time


def execute_command(
    project_root: str,
    command: str,
    timeout: int = 30,
    capture_output: bool = True,
    env: dict | None = None
):
    """Execute a shell command"""
    
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"Project root does not exist: {project_root}")
    
    # Prepare environment
    exec_env = os.environ.copy()
    if env:
        exec_env.update(env)
    
    # Execute command
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=project_root,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            env=exec_env
        )
        
        duration = time.time() - start_time
        
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout if capture_output else "",
            "stderr": result.stderr if capture_output else "",
            "duration": round(duration, 2),
            "timed_out": False
        }
    
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return {
            "exit_code": 124,  # Standard timeout exit code
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "duration": round(duration, 2),
            "timed_out": True
        }
    
    except Exception as e:
        duration = time.time() - start_time
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(duration, 2),
            "timed_out": False
        }


def main():
    parser = argparse.ArgumentParser(description="Execute shell command")
    parser.add_argument("--project-root", required=True, help="Working directory")
    parser.add_argument("--command", required=True, help="Command to execute")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--no-capture", action="store_true", help="Don't capture output")
    parser.add_argument("--env", help="Environment variables (JSON)")
    
    args = parser.parse_args()
    
    # Parse environment variables
    env = None
    if args.env:
        try:
            env = json.loads(args.env)
        except json.JSONDecodeError:
            print("Error: Invalid JSON for --env", file=sys.stderr)
            sys.exit(1)
    
    try:
        result = execute_command(
            args.project_root,
            args.command,
            args.timeout,
            not args.no_capture,
            env
        )
        
        # Print result as JSON
        print(json.dumps(result, indent=2))
        
        # Exit with command's exit code
        sys.exit(result["exit_code"])
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
