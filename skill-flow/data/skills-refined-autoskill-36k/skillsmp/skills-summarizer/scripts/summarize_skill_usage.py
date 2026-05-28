import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize skill usage logs.")
    parser.add_argument("--logs-root", default="logs/skills", help="Logs root dir.")
    parser.add_argument(
        "--output-root",
        default="docs/skill-upkeep",
        help="Output root dir for summaries.",
    )
    parser.add_argument(
        "--skills-root",
        default=".",
        help="Repo root to scan for SKILL.md files.",
    )
    parser.add_argument("--days", type=int, default=7, help="Days to include.")
    parser.add_argument(
        "--as-of",
        default="",
        help="UTC date (YYYY-MM-DD) for summary end date. Defaults to today.",
    )
    return parser.parse_args()


def utc_today():
    return datetime.now(timezone.utc).date()


def iter_log_files(logs_root, start_date, end_date):
    current = start_date
    while current <= end_date:
        month_dir = current.strftime("%Y-%m")
        day_file = current.strftime("skill-usage-%Y-%m-%d.jsonl")
        path = Path(logs_root) / month_dir / day_file
        if path.exists():
            yield path
        current += timedelta(days=1)


def load_entries(paths):
    entries = []
    errors = 0
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    entries.append(data)
                except json.JSONDecodeError:
                    errors += 1
    return entries, errors


def load_skill_catalog(skills_root):
    skills_root = Path(skills_root)
    catalog = {}

    for skill_file in skills_root.rglob("SKILL.md"):
        skill_name = skill_file.parent.name
        description = ""
        try:
            with skill_file.open("r", encoding="utf-8") as handle:
                lines = [next(handle) for _ in range(20)]
        except (StopIteration, OSError):
            lines = []

        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if line.lower().startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"')
                    break

        catalog[skill_name] = {
            "skill_name": skill_name,
            "description": description,
            "path": str(skill_file.parent),
        }

    return catalog


def derive_family(skill_name, description):
    if "-" in skill_name:
        return skill_name.split("-", 1)[0]
    if description:
        return description.split(" ", 1)[0].lower()
    return skill_name


def filter_entries(entries):
    session_entries = [e for e in entries if e.get("source") == "codex_session_log"]
    if session_entries:
        return session_entries, "codex_session_log"
    return entries, "mixed"


def summarize(entries, start_date, end_date, catalog):
    total = len(entries)
    status_counts = Counter()
    skill_counts = Counter()
    skill_status = defaultdict(Counter)
    projects = Counter()
    skill_notes = defaultdict(Counter)
    last_used = {}

    for entry in entries:
        status = entry.get("status", "unknown")
        skill = entry.get("skill_name", "unknown")
        repo_root = entry.get("project_repo_root") or "unknown"
        note = entry.get("notes", "")
        status_counts[status] += 1
        skill_counts[skill] += 1
        skill_status[skill][status] += 1
        projects[repo_root] += 1
        if note:
            skill_notes[skill][note] += 1
        if entry.get("timestamp"):
            last_used[skill] = max(last_used.get(skill, ""), entry["timestamp"])

    top_skills = skill_counts.most_common(10)
    top_projects = projects.most_common(5)

    all_skills = sorted(catalog.keys())
    used_skills = set(skill_counts.keys())
    unused_skills = [s for s in all_skills if s not in used_skills]

    family_counts = Counter()
    family_used = Counter()
    for skill_name in all_skills:
        family = derive_family(skill_name, catalog[skill_name]["description"])
        family_counts[family] += 1
        if skill_name in used_skills:
            family_used[family] += 1

    unused_details = []
    for skill_name in unused_skills:
        family = derive_family(skill_name, catalog[skill_name]["description"])
        family_usage_rate = 0.0
        if family_counts[family]:
            family_usage_rate = family_used[family] / family_counts[family]
        displacement_probability = min(0.95, 0.2 + 0.6 + 0.2 * (1 - family_usage_rate))
        rationale = f"unused in window; family usage rate {family_usage_rate:.0%}"
        unused_details.append(
            {
                "skill_name": skill_name,
                "family": family,
                "days_since_last_use": None,
                "displacement_probability": round(displacement_probability, 2),
                "rationale": rationale,
            }
        )

    review_prompts = [
        "Which top-used skills feel essential vs. replaceable?",
        "Do any unused skills cover workflows you still expect to need?",
        "Are there missing skills implied by repeated work patterns?",
        "Which families should be merged or pruned next?",
    ]

    by_repo = {}
    for entry in entries:
        repo_root = entry.get("project_repo_root") or "unknown"
        skill = entry.get("skill_name", "unknown")
        by_repo.setdefault(repo_root, Counter())[skill] += 1

    return {
        "summary_date": end_date.isoformat(),
        "range": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": (end_date - start_date).days + 1,
        },
        "window_days": (end_date - start_date).days + 1,
        "totals": {
            "invocations": total,
            "status_counts": dict(status_counts),
            "unique_skills": len(skill_counts),
            "unique_projects": len(projects),
        },
        "by_skill": [
            {
                "skill_name": name,
                "count": count,
                "success_rate": round(
                    skill_status[name].get("success", 0) / max(count, 1), 2
                ),
                "top_notes": [note for note, _ in skill_notes[name].most_common(3)],
            }
            for name, count in skill_counts.most_common()
        ],
        "by_repo": [
            {
                "project_repo_root": name,
                "skill_counts": dict(by_repo[name]),
                "notes": [],
            }
            for name, _ in projects.most_common()
        ],
        "top_skills": [
            {
                "skill_name": name,
                "count": count,
                "status_counts": dict(skill_status[name]),
            }
            for name, count in top_skills
        ],
        "top_projects": [
            {"project_repo_root": name, "count": count}
            for name, count in top_projects
        ],
        "catalog": {
            "total_skills": len(all_skills),
            "used_skills": len(used_skills),
            "unused_skills": len(unused_skills),
        },
        "unused_skills": unused_details,
        "review_prompts": review_prompts,
        "candidate_actions": [],
    }


def render_html(summary, errors):
    totals = summary["totals"]
    top_skills = summary["top_skills"]
    top_projects = summary["top_projects"]
    unused_skills = summary.get("unused_skills", [])
    range_info = summary["range"]
    status_counts = totals.get("status_counts", {})

    def render_list(items, formatter):
        if not items:
            return "<p>No data.</p>"
        return "<ul>" + "".join(formatter(item) for item in items) + "</ul>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Skill Usage Summary</title>
  <style>
    :root {{
      --bg: #f6f2ea;
      --card: #fffdf8;
      --ink: #1b1b1b;
      --accent: #2f6f3f;
      --muted: #6b6b6b;
      --border: #e4d9c8;
    }}
    body {{
      margin: 0;
      font-family: "Georgia", "Times New Roman", serif;
      background: radial-gradient(circle at 10% 10%, #efe6d7, var(--bg));
      color: var(--ink);
    }}
    main {{
      max-width: 980px;
      margin: 32px auto;
      padding: 0 20px 40px;
    }}
    h1 {{
      font-size: 2.2rem;
      margin-bottom: 8px;
    }}
    .subtitle {{
      color: var(--muted);
      margin-bottom: 24px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.06);
    }}
    .card h2 {{
      font-size: 1.1rem;
      margin: 0 0 8px;
    }}
    .stat {{
      font-size: 1.8rem;
      color: var(--accent);
      font-weight: bold;
    }}
    ul {{
      margin: 8px 0 0;
      padding-left: 18px;
    }}
    li {{
      margin-bottom: 4px;
    }}
    .footer {{
      margin-top: 24px;
      color: var(--muted);
      font-size: 0.9rem;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Skill Usage Summary</h1>
    <div class="subtitle">Range: {range_info["start_date"]} to {range_info["end_date"]} ({range_info["days"]} days)</div>
    <div class="grid">
      <div class="card">
        <h2>Total Invocations</h2>
        <div class="stat">{totals["invocations"]}</div>
      </div>
      <div class="card">
        <h2>Unique Skills</h2>
        <div class="stat">{totals["unique_skills"]}</div>
      </div>
      <div class="card">
        <h2>Unique Projects</h2>
        <div class="stat">{totals["unique_projects"]}</div>
      </div>
      <div class="card">
        <h2>Status Breakdown</h2>
        {render_list(status_counts.items(), lambda i: f"<li>{i[0]}: {i[1]}</li>")}
      </div>
    </div>
    <div class="grid" style="margin-top: 18px;">
      <div class="card">
        <h2>Top Skills</h2>
        {render_list(top_skills, lambda i: f"<li>{i['skill_name']}: {i['count']}</li>")}
      </div>
      <div class="card">
        <h2>Top Projects</h2>
        {render_list(top_projects, lambda i: f"<li>{i['project_repo_root']}: {i['count']}</li>")}
      </div>
      <div class="card">
        <h2>Parsing Notes</h2>
        <p>Invalid log lines skipped: {errors}</p>
      </div>
    </div>
    <div class="grid" style="margin-top: 18px;">
      <div class="card">
        <h2>Unused Skills (Displacement Candidates)</h2>
        {render_list(unused_skills[:12], lambda i: f"<li>{i['skill_name']} ({i['family']}): {int(i['displacement_probability']*100)}%</li>")}
      </div>
    </div>
    <div class="footer">Metadata only. No prompts or user content captured.</div>
  </main>
</body>
</html>
"""


def main():
    args = parse_args()
    as_of = utc_today() if not args.as_of else datetime.strptime(args.as_of, "%Y-%m-%d").date()
    days = max(args.days, 1)
    end_date = as_of
    start_date = end_date - timedelta(days=days - 1)

    log_paths = list(iter_log_files(args.logs_root, start_date, end_date))
    entries, errors = load_entries(log_paths)
    entries, _ = filter_entries(entries)
    catalog = load_skill_catalog(args.skills_root)
    summary = summarize(entries, start_date, end_date, catalog)

    output_month = end_date.strftime("%Y-%m")
    output_dir = Path(args.output_root) / output_month
    output_dir.mkdir(parents=True, exist_ok=True)

    output_date = end_date.strftime("%Y-%m-%d")
    json_path = output_dir / f"summary-{output_date}.json"
    html_path = output_dir / f"summary-{output_date}.html"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

    html = render_html(summary, errors)
    with html_path.open("w", encoding="utf-8") as handle:
        handle.write(html)

    print(json_path)
    print(html_path)


if __name__ == "__main__":
    main()
