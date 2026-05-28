#!/usr/bin/env python3
import argparse
import os
import shlex
import shutil
import subprocess
import sys

# 颜色代码
GREEN = "\033[92m"
CYAN = "\033[96m"
DARK_GRAY = "\033[90m"
RED = "\033[91m"
RESET = "\033[0m"


def print_colored(text, color):
    print(f"{color}{text}{RESET}")
    sys.stdout.flush()


def ensure_tool(name):
    if shutil.which(name) is None:
        print_colored(f"Error: 未找到必需的 CLI：{name}", RED)
        sys.exit(1)


def invoke_agent_command(exe, args, work_dir, prompt, dry_run):
    # 构建展示用的命令字符串，隐藏 prompt 细节以防太长
    safe_args = []
    for arg in args:
        if arg == prompt:
            safe_args.append("<PROMPT>")
        else:
            safe_args.append(shlex.quote(arg))

    action = f"{exe} {' '.join(safe_args)}"
    print_colored(f"[RUN] {action}", CYAN)
    print_colored(f"[PromptChars] {len(prompt)}", DARK_GRAY)

    if dry_run:
        return

    try:
        # 确保目录存在
        if not os.path.exists(work_dir):
            print_colored(f"Error: 工作目录不存在: {work_dir}", RED)
            sys.exit(1)

        # 切换目录执行
        # subprocess.run 的 cwd 参数更安全
        print_colored(f"Executing in {work_dir}...", DARK_GRAY)

        result = subprocess.run([exe] + args, cwd=work_dir)

        if result.returncode != 0:
            print_colored(f"命令执行失败，exit code={result.returncode}：{exe}", RED)
            sys.exit(result.returncode)

    except Exception as e:
        print_colored(f"执行出错: {str(e)}", RED)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Coding Agent Runner")

    # 必需参数
    parser.add_argument("--agent", "-a", required=True, choices=["codex", "claude", "opencode"], help="Agent to invoke")
    parser.add_argument("--prompt", "-p", required=True, help="Task prompt")

    # 可选参数
    parser.add_argument("--work-dir", "-w", default=os.getcwd(), help="Working directory (default: current dir)")
    parser.add_argument("--model", "-m", help="Model to use (e.g., gpt-4o, claude-3-5-sonnet)")
    parser.add_argument("--full-auto", action="store_true", help="Enable full auto mode (codex only)")
    parser.add_argument("--json", action="store_true", help="Enable JSON output")
    parser.add_argument("--dry-run", "--what-if", action="store_true", dest="dry_run", help="Dry run mode (WhatIf)")

    # 额外参数，接受剩余的所有参数
    # 使用 nargs='*' 可以接受列表，但必须小心位置。
    # 建议放在最后，或者使用 --extra-args "arg1" "arg2"
    parser.add_argument("--extra-args", nargs="*", default=[], help="Extra arguments for the agent CLI")

    # 解析参数
    # 使用 parse_known_args 以允许用户直接传递 agent 的 flag
    args, unknown = parser.parse_known_args()

    # 合并显式的 extra_args 和未知的参数
    # 注意：如果 unknown 中的参数与脚本参数同名但位置不对，可能会有问题，但通常是可以的
    all_extra_args = args.extra_args + unknown

    print_colored(f"[Agent] {args.agent}", GREEN)
    print_colored(f"[WorkDir] {args.work_dir}", DARK_GRAY)
    if args.model:
        print_colored(f"[Model] {args.model}", DARK_GRAY)

    ensure_tool(args.agent)

    cmd_args = []

    if args.agent == "codex":
        cmd_args.append("exec")
        if args.model:
            cmd_args.extend(["--model", args.model])
        if args.full_auto:
            cmd_args.append("--full-auto")
        if args.json:
            cmd_args.append("--json")

        # 添加额外参数
        if all_extra_args:
            cmd_args.extend(all_extra_args)

        # Codex 的 -C 和 prompt 必须放在最后
        cmd_args.extend(["-C", args.work_dir, args.prompt])

        invoke_agent_command("codex", cmd_args, args.work_dir, args.prompt, args.dry_run)

    elif args.agent == "claude":
        # claude -p "prompt" --setting-sources user,project,local
        cmd_args.extend(["-p", args.prompt, "--setting-sources", "user,project,local"])
        if args.model:
            cmd_args.extend(["--model", args.model])
        if args.json:
            cmd_args.extend(["--output-format", "json"])

        if all_extra_args:
            cmd_args.extend(all_extra_args)

        invoke_agent_command("claude", cmd_args, args.work_dir, args.prompt, args.dry_run)

    elif args.agent == "opencode":
        if args.json:
            print_colored("Error: 当前封装未映射 opencode 的 -Json 输出；如需要请用 --extra-args 透传参数。", RED)
            sys.exit(1)

        cmd_args.extend(["run", args.prompt])

        if args.model:
            cmd_args.extend(["--model", args.model])

        if all_extra_args:
            cmd_args.extend(all_extra_args)

        invoke_agent_command("opencode", cmd_args, args.work_dir, args.prompt, args.dry_run)

    print_colored("[DONE] Agent execution completed.", GREEN)


if __name__ == "__main__":
    main()
