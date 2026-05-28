#!/usr/bin/env python3
"""
RepoGPS run/test command extractor (standalone).

Usage:
  python extract_runbook.py --cache .repogps_cache/xai-org__x-algorithm__main
"""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import List

from _github import (
    extract_ci_commands,
    load_downloaded_text,
    load_key_files,
    extract_commands_from_readme,
    extract_from_package_json,
    extract_from_makefile,
    dedupe,
    detect_languages,
)


def main():
    ap = argparse.ArgumentParser(description="RepoGPS - Extract runbook")
    ap.add_argument("--cache", required=True, help="Path to scan_repo output folder")
    args = ap.parse_args()

    cache_dir = pathlib.Path(args.cache)
    key_files = load_key_files(cache_dir)

    confirmed_run: List[str] = []
    confirmed_test: List[str] = []

    # README
    for rp in key_files.get("docs", []):
        text = load_downloaded_text(cache_dir, rp)
        if text:
            r, t = extract_commands_from_readme(text)
            confirmed_run += r
            confirmed_test += t

    # Manifests
    for mp in key_files.get("manifests", []):
        text = load_downloaded_text(cache_dir, mp)
        if not text:
            continue

        if mp.endswith("package.json"):
            r, t = extract_from_package_json(text)
            confirmed_run += r
            confirmed_test += t
        elif mp.endswith("Makefile"):
            r, t = extract_from_makefile(text)
            confirmed_run += r
            confirmed_test += t

    # CI workflows
    for wf in key_files.get("ci", []):
        text = load_downloaded_text(cache_dir, wf)
        if text:
            r, t = extract_ci_commands(text, wf)
            confirmed_run += r
            confirmed_test += t

    confirmed_run = dedupe(confirmed_run)
    confirmed_test = dedupe(confirmed_test)

    # Inference
    inferred_run: List[str] = []
    inferred_test: List[str] = []
    missing: List[str] = []

    manifests = set(key_files.get("manifests", []))
    entrypoints = set(key_files.get("entrypoints", []))
    langs = detect_languages(manifests, entrypoints)

    lang_commands = {
        "python": ("python -m <module>", "pytest -q"),
        "javascript": ("npm run dev", "npm test"),
        "typescript": ("npm run dev", "npm test"),
        "rust": ("cargo run", "cargo test"),
        "go": ("go run .", "go test ./..."),
        "java": ("mvn spring-boot:run", "mvn test"),
        "csharp": ("dotnet run", "dotnet test"),
        "ruby": ("bundle exec rails server", "bundle exec rspec"),
        "php": ("php artisan serve", "./vendor/bin/phpunit"),
    }

    for lang in langs:
        if lang in lang_commands:
            run_cmd, test_cmd = lang_commands[lang]
            if not confirmed_run:
                inferred_run.append(run_cmd)
            if not confirmed_test:
                inferred_test.append(test_cmd)

    if not confirmed_run and not inferred_run:
        missing.append("No run command found. Check README or Makefile.")
    if not confirmed_test and not inferred_test:
        missing.append("No test command found. Check CI workflows.")

    out = {
        "run": {"confirmed": confirmed_run, "inferred": inferred_run},
        "test": {"confirmed": confirmed_test, "inferred": inferred_test},
        "languages_detected": sorted(langs),
        "missing_info": missing,
        "note": "Confirmed commands from docs/manifests/CI. Inferred are best guesses.",
    }

    (cache_dir / "runbook.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[RepoGPS] Wrote: {cache_dir / 'runbook.json'}")

    if out["run"]["confirmed"]:
        print(f"  Confirmed run: {out['run']['confirmed'][0]}")
    elif out["run"]["inferred"]:
        print(f"  Inferred run: {out['run']['inferred'][0]}")

    if out["test"]["confirmed"]:
        print(f"  Confirmed test: {out['test']['confirmed'][0]}")
    elif out["test"]["inferred"]:
        print(f"  Inferred test: {out['test']['inferred'][0]}")

    if langs:
        print(f"  Languages: {', '.join(sorted(langs))}")


if __name__ == "__main__":
    main()
