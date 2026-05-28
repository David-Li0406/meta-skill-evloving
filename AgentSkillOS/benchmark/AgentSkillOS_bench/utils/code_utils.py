"""
Code execution utilities.
These functions only execute code and return results, they do NOT perform evaluation.
"""
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


def run_subprocess(workspace: Path, cmd: List[str], timeout: int = 60,
                   env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Execute a subprocess command.

    Args:
        workspace: Working directory for the command
        cmd: Command and arguments as list
        timeout: Timeout in seconds
        env: Optional environment variables

    Returns:
        Dict with keys: returncode, stdout, stderr, success, timeout
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
            "timeout": False
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "success": False,
            "timeout": True
        }
    except Exception as e:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
            "timeout": False
        }


def run_python_script(workspace: Path, script: str, args: List[str] = None,
                      timeout: int = 60) -> Dict[str, Any]:
    """
    Execute a Python script.

    Args:
        workspace: Working directory
        script: Relative path to Python script
        args: Optional command line arguments
        timeout: Timeout in seconds

    Returns:
        Dict with execution results
    """
    cmd = [sys.executable, script]
    if args:
        cmd.extend(args)
    return run_subprocess(workspace, cmd, timeout)


def run_pytest(workspace: Path, test_file: str, timeout: int = 120,
               coverage: bool = False, coverage_source: str = None) -> Dict[str, Any]:
    """
    Run pytest on a test file.

    Args:
        workspace: Working directory
        test_file: Relative path to test file
        timeout: Timeout in seconds
        coverage: Whether to measure code coverage
        coverage_source: Source file/dir for coverage measurement

    Returns:
        Dict with test results including tests_passed, tests_failed, coverage_percent
    """
    cmd = [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"]

    if coverage and coverage_source:
        cmd.extend([f"--cov={coverage_source}", "--cov-report=term"])

    result = run_subprocess(workspace, cmd, timeout)

    # Parse test results from output
    output = result["stdout"] + result["stderr"]

    # Count passed/failed tests
    passed_match = re.search(r'(\d+)\s+passed', output)
    failed_match = re.search(r'(\d+)\s+failed', output)
    error_match = re.search(r'(\d+)\s+error', output)

    result["tests_passed"] = int(passed_match.group(1)) if passed_match else 0
    result["tests_failed"] = int(failed_match.group(1)) if failed_match else 0
    result["tests_error"] = int(error_match.group(1)) if error_match else 0

    # Parse coverage if requested
    if coverage:
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
        if coverage_match:
            result["coverage_percent"] = int(coverage_match.group(1))
        else:
            # Try alternative pattern
            alt_match = re.search(r'(\d+)%\s*$', output, re.MULTILINE)
            result["coverage_percent"] = int(alt_match.group(1)) if alt_match else 0

    return result


def run_python_code(workspace: Path, code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute Python code string directly.

    Args:
        workspace: Working directory
        code: Python code to execute
        timeout: Timeout in seconds

    Returns:
        Dict with execution results
    """
    cmd = [sys.executable, "-c", code]
    return run_subprocess(workspace, cmd, timeout)
