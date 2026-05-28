#!/usr/bin/env python3
"""
manage.py - CLI for skill management.

Commands:
- list: List all skills with status
- learn: Analyze patterns and generate candidates
- candidates: Show pending skill candidates
- approve: Approve a candidate
- reject: Reject a candidate
- history: Show version history for a skill
- rollback: Rollback a skill to a previous version
- stats: Show usage analytics
- improve: Force improvement analysis on a skill
- refine: Interactively improve a skill
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# Determine skills directory
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
CANDIDATES_DIR = SKILLS_DIR / ".skill-system" / "candidates"
CONFIG_FILE = SKILLS_DIR / ".skill-system" / "config.json"
ANALYTICS_FILE = SKILLS_DIR / ".skill-system" / "analytics.json"


def cmd_list(args):
    """List all installed skills."""
    print("Installed Skills")
    print("=" * 60)

    skills = []
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            meta_file = item / "skill.meta.json"
            if meta_file.exists():
                try:
                    with open(meta_file) as f:
                        meta = json.load(f)
                    skills.append({
                        "name": item.name,
                        "version": meta.get("version", "?"),
                        "domain": meta.get("domain", "general"),
                        "auto_generated": meta.get("auto_generated", False),
                        "effectiveness": meta.get("effectiveness", {}),
                    })
                except Exception:
                    skills.append({
                        "name": item.name,
                        "version": "?",
                        "domain": "?",
                        "auto_generated": False,
                        "effectiveness": {},
                    })

    if not skills:
        print("No skills installed.")
        return

    # Sort by name
    skills.sort(key=lambda x: x["name"])

    # Print table
    print(f"{'Name':<30} {'Version':<10} {'Domain':<15} {'Success':<10} {'Type':<10}")
    print("-" * 60)

    for skill in skills:
        eff = skill["effectiveness"]
        success_rate = eff.get("success_rate", 1.0)
        success_str = f"{success_rate:.0%}" if isinstance(success_rate, float) else "?"
        skill_type = "auto" if skill["auto_generated"] else "manual"

        print(f"{skill['name']:<30} {skill['version']:<10} {skill['domain']:<15} {success_str:<10} {skill_type:<10}")

    print(f"\nTotal: {len(skills)} skills")


def cmd_learn(args):
    """Run the learning engine."""
    from learn import run_learning
    run_learning(verbose=not args.quiet)


def cmd_candidates(args):
    """Show pending skill candidates."""
    print("Skill Candidates")
    print("=" * 60)

    if not CANDIDATES_DIR.exists():
        print("No candidates directory found.")
        return

    candidates = []
    for item in CANDIDATES_DIR.iterdir():
        if item.is_dir():
            meta_file = item / "candidate.json"
            if meta_file.exists():
                try:
                    with open(meta_file) as f:
                        candidate = json.load(f)
                    if candidate.get("status") == "pending":
                        candidates.append(candidate)
                except Exception:
                    pass

    if not candidates:
        print("No pending candidates.")
        print("\nRun 'manage.py learn' to analyze patterns and generate candidates.")
        return

    # Sort by score
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)

    print(f"{'ID':<20} {'Name':<25} {'Domain':<12} {'Score':<8} {'Freq':<6}")
    print("-" * 60)

    for c in candidates:
        print(f"{c['candidate_id']:<20} {c['skill_name']:<25} {c.get('domain', '?'):<12} {c.get('score', 0):<8.2f} {c.get('frequency', 0):<6}")

    print(f"\nTotal: {len(candidates)} pending candidates")
    print("\nUse 'manage.py approve <id>' to approve a candidate")
    print("Use 'manage.py reject <id>' to reject a candidate")


def cmd_approve(args):
    """Approve a skill candidate."""
    if not args.candidate_id:
        print("Error: candidate_id required")
        sys.exit(1)

    from generate import generate_skill
    result = generate_skill(args.candidate_id, verbose=not args.quiet)

    if result:
        print(f"\nSkill approved and generated at: {result}")
    else:
        sys.exit(1)


def cmd_reject(args):
    """Reject a skill candidate."""
    if not args.candidate_id:
        print("Error: candidate_id required")
        sys.exit(1)

    from generate import reject_candidate
    result = reject_candidate(args.candidate_id, verbose=not args.quiet)

    if not result:
        sys.exit(1)


def cmd_history(args):
    """Show version history for a skill."""
    if not args.skill_name:
        print("Error: skill_name required")
        sys.exit(1)

    skill_dir = SKILLS_DIR / args.skill_name

    if not skill_dir.exists():
        print(f"Skill not found: {args.skill_name}")
        sys.exit(1)

    print(f"Version History: {args.skill_name}")
    print("=" * 60)

    # Try git log
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--decorate", "-20"],
            cwd=skill_dir,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git history not available.")

    # Show CHANGELOG if exists
    changelog_file = skill_dir / "CHANGELOG.md"
    if changelog_file.exists():
        print("\nCHANGELOG:")
        print("-" * 40)
        with open(changelog_file) as f:
            # Print first 50 lines
            for i, line in enumerate(f):
                if i >= 50:
                    print("... (truncated)")
                    break
                print(line.rstrip())


def cmd_rollback(args):
    """Rollback a skill to a previous version."""
    if not args.skill_name or not args.version:
        print("Error: skill_name and version required")
        sys.exit(1)

    skill_dir = SKILLS_DIR / args.skill_name

    if not skill_dir.exists():
        print(f"Skill not found: {args.skill_name}")
        sys.exit(1)

    version = args.version
    if not version.startswith("v"):
        version = f"v{version}"

    print(f"Rolling back {args.skill_name} to {version}...")

    try:
        # Checkout the version
        subprocess.run(
            ["git", "checkout", version],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )
        print(f"Successfully rolled back to {version}")

        # Update metadata
        meta_file = skill_dir / "skill.meta.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
            meta["version"] = version.lstrip("v")
            meta["updated_at"] = datetime.utcnow().isoformat() + "Z"
            with open(meta_file, "w") as f:
                json.dump(meta, f, indent=2)

    except subprocess.CalledProcessError as e:
        print(f"Rollback failed: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        sys.exit(1)
    except FileNotFoundError:
        print("Git not available")
        sys.exit(1)


def cmd_stats(args):
    """Show usage analytics."""
    print("Skill System Statistics")
    print("=" * 60)

    # Load analytics
    if ANALYTICS_FILE.exists():
        try:
            with open(ANALYTICS_FILE) as f:
                analytics = json.load(f)

            global_stats = analytics.get("global_stats", {})
            print("\nGlobal Statistics:")
            print(f"  Sessions observed: {global_stats.get('total_sessions_observed', 0)}")
            print(f"  Patterns captured: {global_stats.get('total_patterns_captured', 0)}")
            print(f"  Skills generated: {global_stats.get('total_skills_generated', 0)}")
            print(f"  Skills approved: {global_stats.get('total_skills_approved', 0)}")
            print(f"  Auto-improvements: {global_stats.get('total_auto_improvements', 0)}")

            domain_stats = analytics.get("domain_stats", {})
            if domain_stats:
                print("\nDomain Statistics:")
                for domain, stats in sorted(domain_stats.items()):
                    print(f"  {domain}: {stats.get('sessions', 0)} sessions, {stats.get('patterns', 0)} patterns")

        except Exception as e:
            print(f"Error loading analytics: {e}")
    else:
        print("No analytics data yet. Start using Claude Code to collect patterns!")

    # Skill effectiveness
    print("\nSkill Effectiveness:")
    print("-" * 40)

    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            meta_file = item / "skill.meta.json"
            if meta_file.exists():
                try:
                    with open(meta_file) as f:
                        meta = json.load(f)
                    eff = meta.get("effectiveness", {})
                    usage = eff.get("usage_count", 0)
                    success = eff.get("success_rate", 1.0)
                    print(f"  {item.name}: {usage} uses, {success:.0%} success")
                except Exception:
                    pass


def cmd_improve(args):
    """Force improvement analysis on a skill."""
    if not args.skill_name:
        print("Error: skill_name required")
        sys.exit(1)

    from improve import check_skill, apply_improvement

    proposal = check_skill(args.skill_name, verbose=True)

    if proposal:
        if args.force:
            proposal["confidence"] = 1.0
            apply_improvement(args.skill_name, proposal, verbose=True)
        else:
            print("\nUse --force to apply improvements regardless of confidence threshold.")


def cmd_refine(args):
    """Interactively improve a skill."""
    if not args.skill_name:
        print("Error: skill_name required")
        sys.exit(1)

    skill_dir = SKILLS_DIR / args.skill_name

    if not skill_dir.exists():
        print(f"Skill not found: {args.skill_name}")
        sys.exit(1)

    print(f"Refining skill: {args.skill_name}")
    print("=" * 60)

    # Show current SKILL.md
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        print("\nCurrent SKILL.md (first 30 lines):")
        print("-" * 40)
        with open(skill_file) as f:
            for i, line in enumerate(f):
                if i >= 30:
                    print("... (truncated)")
                    break
                print(line.rstrip())

    print("\nTo refine this skill:")
    print(f"1. Edit {skill_file}")
    print(f"2. Run: cd {skill_dir} && git add -A && git commit -m 'Manual refinement'")
    print("3. The skill system will learn from your changes.")


def cmd_scan(args):
    """Scan transcripts for patterns (alternative to hooks)."""
    script_dir = Path(__file__).parent
    parse_script = script_dir / "parse_transcripts.py"

    if not parse_script.exists():
        print(f"Error: {parse_script} not found")
        sys.exit(1)

    cmd = ["python3", str(parse_script)]
    if args.force:
        cmd.append("--all")

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def cmd_analyze(args):
    """Analyze prompt patterns for semantic learning."""
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from prompt_analyzer import run_prompt_analysis
    run_prompt_analysis(verbose=not args.quiet)


def cmd_preferences(args):
    """Learn preferences from user prompts."""
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from preference_learner import run_preference_learning

    do_update = args.force  # --force means update CLAUDE.md
    run_preference_learning(verbose=not args.quiet, update_claude=do_update)


def cmd_prompts(args):
    """View captured user prompts."""
    prompts_file = SKILLS_DIR / ".skill-system" / "patterns" / "user-prompts.jsonl"

    if not prompts_file.exists():
        print("No prompts captured yet. Run 'manage.py scan' first.")
        sys.exit(1)

    print("User Prompts Log")
    print("=" * 60)

    # Get limit from args
    limit = int(args.skill_name) if args.skill_name and args.skill_name.isdigit() else 20

    prompts = []
    with open(prompts_file) as f:
        for line in f:
            try:
                prompts.append(json.loads(line))
            except:
                pass

    # Filter out warmup and shell commands if not verbose
    if not getattr(args, 'force', False):
        prompts = [p for p in prompts if not p['prompt'].startswith('[shell]')
                   and 'warmup' not in p['prompt'].lower()]

    # Show most recent first
    prompts = prompts[-limit:][::-1]

    for p in prompts:
        ts = p.get('timestamp', '')[:16]
        prompt = p.get('prompt', '')[:70]
        print(f"{ts} | {prompt}")

    print(f"\nTotal: {len(prompts)} prompts (use 'prompts 50' for more)")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Skill management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  list                  List all installed skills
  scan                  Scan transcripts for patterns (no hooks needed)
  learn                 Analyze patterns and generate candidates
  preferences           Learn preferences from prompts (--force to update CLAUDE.md)
  candidates            Show pending skill candidates
  approve <id>          Approve a candidate
  reject <id>           Reject a candidate
  prompts [N]           View captured user prompts (default: 20)
  history <skill>       Show version history for a skill
  rollback <skill> <v>  Rollback a skill to version
  stats                 Show usage analytics
  improve <skill>       Force improvement analysis
  refine <skill>        Instructions for manual refinement
        """
    )

    parser.add_argument("command",
                       choices=["list", "learn", "candidates", "approve", "reject",
                               "history", "rollback", "stats", "improve", "refine", "scan", "prompts", "analyze", "preferences"],
                       help="Command to run")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    parser.add_argument("--force", "-f", action="store_true", help="Force action")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Parse positional arguments based on command
    args.candidate_id = args.args[0] if args.args else None
    args.skill_name = args.args[0] if args.args else None
    args.version = args.args[1] if len(args.args) > 1 else None

    # Dispatch to command handler
    commands = {
        "list": cmd_list,
        "learn": cmd_learn,
        "candidates": cmd_candidates,
        "approve": cmd_approve,
        "reject": cmd_reject,
        "history": cmd_history,
        "rollback": cmd_rollback,
        "stats": cmd_stats,
        "improve": cmd_improve,
        "refine": cmd_refine,
        "scan": cmd_scan,
        "prompts": cmd_prompts,
        "analyze": cmd_analyze,
        "preferences": cmd_preferences,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
