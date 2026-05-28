from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    items: list[dict] = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    return items


def norm(u: object) -> str:
    return (u or "").__str__().strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Summarize Moodle Mirror index status.")
    ap.add_argument("--index", required=True, help="Path to _index.jsonl")
    ap.add_argument("--out", required=True, help="Output markdown path (e.g. _status.md)")
    args = ap.parse_args(argv)

    index_path = Path(args.index).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    items = load_jsonl(index_path)

    # Determine latest entry per URL based on timestamp strings (ISO-ish).
    per_url: list[tuple[str, str, dict]] = []
    for it in items:
        url = norm(it.get("url"))
        if not url:
            continue
        t = norm(it.get("time_utc") or it.get("fetched_at_utc"))
        per_url.append((url, t, it))
    per_url.sort(key=lambda x: (x[0], x[1]))
    latest: dict[str, dict] = {}
    for url, _t, it in per_url:
        latest[url] = it

    counts = Counter()
    errors: list[tuple[str, dict]] = []
    blocked: list[tuple[str, dict]] = []

    for url, it in latest.items():
        kind = it.get("kind")
        if kind is None and it.get("md"):
            counts["page"] += 1
        elif kind == "download":
            counts["download"] += 1
        elif kind == "error":
            counts["error"] += 1
            errors.append((url, it))
        elif kind == "blocked":
            counts["blocked"] += 1
            blocked.append((url, it))
        else:
            counts[str(kind)] += 1

    def sort_key(pair: tuple[str, dict]) -> tuple[str, str]:
        url, it = pair
        t = norm(it.get("time_utc") or it.get("fetched_at_utc"))
        return (t, url)

    errors.sort(key=sort_key)
    blocked.sort(key=sort_key)

    lines: list[str] = []
    lines.append("# Moodle Mirror Status")
    lines.append("")
    lines.append(f"- Index: `{index_path}`")
    lines.append(f"- Total URLs (latest status): `{len(latest)}`")
    lines.append("")
    lines.append("## Counts (Latest Status)")
    lines.append("")
    for k in ["page", "download", "blocked", "error"]:
        if k in counts:
            lines.append(f"- {k}: `{counts[k]}`")
    for k, v in sorted(counts.items()):
        if k in {"page", "download", "blocked", "error"}:
            continue
        lines.append(f"- {k}: `{v}`")

    if errors:
        lines.append("")
        lines.append("## Errors (Most Recent First)")
        lines.append("")
        for url, it in reversed(errors[-50:]):
            t = norm(it.get("time_utc") or it.get("fetched_at_utc"))
            err = norm(it.get("error"))
            lines.append(f"- `{t}` `{url}` — {err}")

    if blocked:
        lines.append("")
        lines.append("## Blocked (Most Recent First)")
        lines.append("")
        for url, it in reversed(blocked[-50:]):
            t = norm(it.get("time_utc") or it.get("fetched_at_utc"))
            reason = norm(it.get("reason"))
            final_url = norm(it.get("final_url"))
            extra = f" (final: `{final_url}`)" if final_url else ""
            lines.append(f"- `{t}` `{url}` — {reason}{extra}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

