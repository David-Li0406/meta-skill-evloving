#!/usr/bin/env python3
"""
Ralph Fresh Loop via SDK - Spawns fresh Claude instances via API
Bypasses CLI hooks entirely for true fresh context per iteration
"""

import os
import sys
import time
import argparse
import re
from anthropic import Anthropic, RateLimitError

def parse_args():
    parser = argparse.ArgumentParser(description='Ralph Fresh Loop via SDK')
    parser.add_argument('prompt', help='Task prompt')
    parser.add_argument('--task-id', default='sdk-task', help='Unique task identifier')
    parser.add_argument('--max-iterations', type=int, default=50, help='Max iterations')
    parser.add_argument('--completion-promise', default='', help='Promise text to detect completion')
    parser.add_argument('--model', default='claude-sonnet-4-20250514', help='Model to use')
    return parser.parse_args()

def call_claude(client, prompt: str, iteration: int, promise: str, model: str, task_id: str) -> str:
    """Make a single Claude API call with fresh context."""

    system_prompt = f"""You are Ralph (iteration {iteration}), an autonomous coding agent.
You have access to the filesystem and can create/edit files directly.
Work on the task systematically. Make real changes to files.
Be concise but thorough.

AT THE END of this iteration, update .claude/ralph-progress-{task_id}.md with:
- What you completed this iteration
- Files changed
- Next steps
- Any blockers

{"Output <promise>" + promise + "</promise> ONLY when ALL work is genuinely complete." if promise else ""}

IMPORTANT: You are running via API, not CLI. To modify files, output the file content in this format:
===FILE: /path/to/file.py===
<file content here>
===END FILE===

I will parse these blocks and write the files for you."""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except RateLimitError:
        print("⚠️ Rate limited, waiting 30s...")
        time.sleep(30)
        return call_claude(client, prompt, iteration, promise, model)

def extract_and_write_files(output: str) -> list:
    """Extract file blocks from output and write them."""
    pattern = r'===FILE: (.+?)===\n(.*?)===END FILE==='
    files_written = []

    for match in re.finditer(pattern, output, re.DOTALL):
        filepath = match.group(1).strip()
        content = match.group(2)

        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            f.write(content)

        files_written.append(filepath)
        print(f"  📝 Wrote: {filepath}")

    return files_written

def check_promise(output: str, promise: str) -> bool:
    """Check if completion promise is in output."""
    if not promise:
        return False
    pattern = f'<promise>{re.escape(promise)}</promise>'
    return bool(re.search(pattern, output))

def main():
    args = parse_args()

    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = Anthropic()

    print(f"🔄 Starting SDK-based Ralph Loop: {args.task_id}")
    print(f"   Model: {args.model}")
    print(f"   Max iterations: {args.max_iterations}")
    if args.completion_promise:
        print(f"   Promise: {args.completion_promise}")
    print("━" * 60)

    for iteration in range(1, args.max_iterations + 1):
        print(f"\n🚀 ITERATION {iteration} | {args.task_id}")
        print("━" * 60)

        output = call_claude(
            client,
            args.prompt,
            iteration,
            args.completion_promise,
            args.model,
            args.task_id
        )

        # Print output (truncated)
        print(output[:2000] + ("..." if len(output) > 2000 else ""))

        # Extract and write any files
        files = extract_and_write_files(output)
        if files:
            print(f"\n  ✅ Wrote {len(files)} file(s)")

        # Check for completion
        if check_promise(output, args.completion_promise):
            print(f"\n✅ Ralph loop {args.task_id} complete: Detected promise!")
            break

        # Brief pause between iterations
        time.sleep(2)
    else:
        print(f"\n🛑 Max iterations ({args.max_iterations}) reached")

    print("\n✅ SDK loop finished.")

if __name__ == '__main__':
    main()
