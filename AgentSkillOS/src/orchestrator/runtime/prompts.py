"""Prompts for direct (non-DAG) execution."""

DIRECT_EXECUTOR_PROMPT = """You are completing a task directly using available tools.

## Instructions
1. Analyze the task requirements carefully
2. Use available tools to complete the task
3. Save all outputs to the specified output directory
4. Use absolute paths when referencing files
"""


def build_working_dir_section(working_dir: str) -> str:
    """Build the working directory constraint section for prompts."""
    if not working_dir:
        return ""
    return f"""
## Working Directory
Your working directory is: {working_dir}
**IMPORTANT**: All file operations MUST be performed within this directory or its subdirectories.
Do NOT create or modify files outside of this directory.
"""


def build_direct_executor_prompt(task: str, output_dir: str, working_dir: str = "") -> str:
    """Build prompt for direct Claude execution without skills."""
    working_dir_section = build_working_dir_section(working_dir)

    return f"""{DIRECT_EXECUTOR_PROMPT}

## Task
{task}
{working_dir_section}
## Output Directory
Save all generated files to: {output_dir}

After completing the task, provide a summary in this format:
<execution_summary>
STATUS: SUCCESS or FAILURE
1. What was accomplished (or what went wrong if failed)
2. Key output files created
3. Any notes or recommendations
</execution_summary>

**Important**: Set STATUS to FAILURE only if the core task objective could not be achieved despite retries.
"""
