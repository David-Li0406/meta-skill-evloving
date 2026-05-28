# .agent/skills/start-task/scripts/setup_worktree.py
import argparse
import os
import subprocess
import sys

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        sys.exit(1)

def setup_worktree(task_name):
    # Enforce kebab-case
    if not task_name.replace("-", "").isalnum() or " " in task_name:
        print("Error: Task name must be kebab-case (alphanumeric and hyphens only).")
        sys.exit(1)

    worktree_path = f".worktrees/{task_name}"
    
    if os.path.exists(worktree_path):
        print(f"Error: Worktree '{worktree_path}' already exists.")
        sys.exit(1)

    print(f"Creating worktree for '{task_name}'...")
    
    # Create worktree and branch
    run_command(f"git worktree add -b {task_name} {worktree_path} origin/main")
    
    # Initialize task.md
    task_md_path = os.path.join(worktree_path, "task.md")
    task_template = f"""# Task: {task_name}

- [ ] Status: Initialized
- [ ] Context: {task_name}

## Checklist
- [ ] Analyze Requirements
- [ ] Implementation
- [ ] Verification
"""
    with open(task_md_path, "w") as f:
        f.write(task_template)
        
    print(f"✅ Worktree setup complete: {worktree_path}")
    print(f"✅ Created {task_md_path}")
    print(f"\nNEXT STEP: Switch your focus to the '{worktree_path}' directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup a new task worktree.")
    parser.add_argument("--name", required=True, help="Task name in kebab-case")
    args = parser.parse_args()
    
    setup_worktree(args.name)
