#!/usr/bin/env python3
"""
Smoke test for Agent Studio's backend game API.

Usage examples:
  python smoke_game_api.py --env-id CartPole-v1 --steps 5
  python smoke_game_api.py --env-id Snake --steps 10 --actions "0,1,2,3"
  python smoke_game_api.py --env-id MountainCar-v0 --steps 10 --random-max 3
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


def http_json(method: str, url: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[int, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            body = raw.decode("utf-8", errors="replace") if raw else ""
            return resp.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {method} {url}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error {method} {url}: {e}") from e


def parse_actions(raw: Optional[str], steps: int, random_max: Optional[int]) -> List[int]:
    if raw:
        actions = [int(x.strip()) for x in raw.split(",") if x.strip()]
        if not actions:
            raise ValueError("--actions was provided but parsed to an empty list")
        # Repeat/trim to match steps
        out = []
        for i in range(steps):
            out.append(actions[i % len(actions)])
        return out

    if random_max is not None:
        if random_max <= 0:
            raise ValueError("--random-max must be > 0")
        return [random.randrange(0, random_max) for _ in range(steps)]

    return [0 for _ in range(steps)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test Agent Studio backend game API.")
    parser.add_argument("--backend-url", default="http://localhost:8000", help="Base URL, default: http://localhost:8000")
    parser.add_argument("--env-id", default="CartPole-v1", help="Game env_id, e.g. CartPole-v1, Snake, Tetris")
    parser.add_argument("--steps", type=int, default=5, help="Number of step calls to make")
    parser.add_argument("--actions", default=None, help='Comma-separated actions, e.g. "0,1,0,1"')
    parser.add_argument("--random-max", type=int, default=None, help="If set, pick random actions in [0, random_max)")
    parser.add_argument("--config", default="{}", help='JSON string for start config, e.g. \'{"grid_w":15,"grid_h":15}\'')
    parser.add_argument("--no-delete", action="store_true", help="Do not DELETE the session at the end")
    args = parser.parse_args()

    if args.steps < 0:
        print("[ERROR] --steps must be >= 0", file=sys.stderr)
        return 2

    backend = args.backend_url.rstrip("/")
    try:
        config = json.loads(args.config)
    except json.JSONDecodeError as e:
        print(f"[ERROR] --config is not valid JSON: {e}", file=sys.stderr)
        return 2

    if config is None:
        config = {}
    if not isinstance(config, dict):
        print("[ERROR] --config must be a JSON object", file=sys.stderr)
        return 2

    # Health
    status, health = http_json("GET", f"{backend}/health")
    print(f"[OK] GET /health -> {status} {health}")

    # Start
    status, start = http_json("POST", f"{backend}/api/game/start", {"env_id": args.env_id, "config": config})
    if status != 200 or not isinstance(start, dict) or "session_id" not in start:
        raise RuntimeError(f"Unexpected start response: {start}")
    session_id = start["session_id"]
    print(f"[OK] POST /api/game/start -> {status} session_id={session_id}")

    # Step
    actions = parse_actions(args.actions, args.steps, args.random_max)
    for i, action in enumerate(actions, start=1):
        status, step = http_json("POST", f"{backend}/api/game/{session_id}/step", {"action": action})
        if status != 200 or not isinstance(step, dict):
            raise RuntimeError(f"Unexpected step response: {step}")
        reward = step.get("reward")
        done = step.get("done")
        truncated = step.get("truncated")
        render = step.get("render") if isinstance(step.get("render"), dict) else None
        render_mode = render.get("mode") if render else None
        print(f"[OK] step {i}/{args.steps}: action={action} reward={reward} done={done} truncated={truncated} render.mode={render_mode}")
        if done or truncated:
            break

    if not args.no_delete:
        status, body = http_json("DELETE", f"{backend}/api/game/{session_id}")
        print(f"[OK] DELETE /api/game/{{session_id}} -> {status} {body}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

