#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_agent_browser(args: list[str]) -> str:
    result = subprocess.run(
        ["agent-browser", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Export agent-browser cookies to a skill asset file.")
    parser.add_argument("--session", required=True, help="Session name to export from.")
    parser.add_argument(
        "--name",
        required=True,
        help="Output file name (without extension). '.local.json' is appended automatically.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parent.parent / "assets" / "cookies"),
        help="Output directory for cookie files.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = run_agent_browser(["cookies", "get", "--json", "--session", args.session])
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse agent-browser output: {exc}", file=sys.stderr)
        return 1

    payload = {
        "exportedAt": datetime.utcnow().isoformat() + "Z",
        "session": args.session,
        "data": data.get("data", {}),
    }

    out_path = out_dir / f"{args.name}.local.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
