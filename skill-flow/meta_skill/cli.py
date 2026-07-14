"""CLI for the meta-skill evolving system.

    python -m meta_skill.cli loop    --config meta_skill/config/smoke_skillx.json
    python -m meta_skill.cli manage  --config ...   # one management pass
    python -m meta_skill.cli compare --config ...   # evolved vs seed on held-out
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(prog="meta_skill")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("loop", "manage", "compare"):
        p = sub.add_parser(name)
        p.add_argument("--config", required=True)

    args = ap.parse_args()
    cfg = _load(args.config)

    if args.cmd == "loop":
        from meta_skill.loop import run_loop
        res = run_loop(cfg)
        print(json.dumps({"history": res["history"], "best": res["best"],
                          "compare": res.get("compare")}, indent=2))
    elif args.cmd == "manage":
        from meta_skill.loop import _load_dataset
        from meta_skill.manage import manage
        from meta_skill.metaskill import load_meta_skill
        ds = _load_dataset(cfg["train"])
        meta = load_meta_skill(cfg["seed_meta_skill"])
        wd = Path(cfg["output_dir"]) / "manage_only"
        refined, log = manage(meta, ds.pool, wd)
        print(json.dumps({"input": len(ds.pool), "output": len(refined),
                          "summary": log["summary"]}, indent=2))
    elif args.cmd == "compare":
        from skill_flow.index.encoder import Encoder
        from meta_skill.loop import compare
        from meta_skill.metaskill import load_meta_skill
        # use the best meta-skill recorded by a prior loop run
        result_path = Path(cfg["output_dir"]) / "result.json"
        best = _load(str(result_path))["best"] if result_path.is_file() else {
            "meta_path": cfg["seed_meta_skill"]}
        seed = load_meta_skill(cfg["seed_meta_skill"])
        print(json.dumps(compare(cfg, best, seed, Encoder()), indent=2))


if __name__ == "__main__":
    main()
