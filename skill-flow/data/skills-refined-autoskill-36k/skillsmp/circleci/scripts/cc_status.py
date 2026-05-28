#!/usr/bin/env python3
"""
Minimal CircleCI API v2 status helper.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request


def _api_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url)
    req.add_header("Circle-Token", token)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def _print_json(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def _token(args: argparse.Namespace) -> str:
    token = args.token or os.environ.get("CIRCLECI_CLI_TOKEN") or os.environ.get(
        "CIRCLECI_TOKEN"
    )
    if not token:
        token = _token_from_cli_config()
    if not token:
        raise SystemExit(
            "Missing token. Set CIRCLECI_CLI_TOKEN, run `circleci setup`, or pass --token."
        )
    return token


def _host(args: argparse.Namespace) -> str:
    return args.host.rstrip("/")


def _quote_slug(slug: str) -> str:
    return urllib.parse.quote(slug, safe="/")


def _token_from_cli_config() -> str | None:
    path = os.path.expanduser("~/.circleci/cli.yml")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.split("#", 1)[0].strip()
                if not line:
                    continue
                match = re.match(r"^token\s*:\s*(.+)$", line)
                if match:
                    token = match.group(1).strip()
                    if token and token[0] in "\"'" and token[-1] == token[0]:
                        token = token[1:-1]
                    return token or None
    except FileNotFoundError:
        return None
    return None


def cmd_pipelines(args: argparse.Namespace) -> None:
    token = _token(args)
    host = _host(args)
    slug = _quote_slug(args.project_slug)
    params = {}
    if args.branch:
        params["branch"] = args.branch
    if args.limit:
        params["limit"] = str(args.limit)
    query = f"?{urllib.parse.urlencode(params)}" if params else ""
    url = f"{host}/api/v2/project/{slug}/pipeline{query}"
    payload = _api_get(url, token)
    if args.json:
        _print_json(payload)
        return
    for item in payload.get("items", []):
        vcs = item.get("vcs", {})
        branch = vcs.get("branch", "")
        revision = vcs.get("revision", "")
        if revision:
            revision = revision[:7]
        print(
            f"{item.get('id','')}\t{item.get('state','')}\t"
            f"{item.get('created_at','')}\t{branch}\t{revision}"
        )


def cmd_workflows(args: argparse.Namespace) -> None:
    token = _token(args)
    host = _host(args)
    url = f"{host}/api/v2/pipeline/{args.pipeline_id}/workflow"
    payload = _api_get(url, token)
    if args.json:
        _print_json(payload)
        return
    for item in payload.get("items", []):
        print(f"{item.get('id','')}\t{item.get('name','')}\t{item.get('status','')}")


def cmd_jobs(args: argparse.Namespace) -> None:
    token = _token(args)
    host = _host(args)
    url = f"{host}/api/v2/workflow/{args.workflow_id}/job"
    payload = _api_get(url, token)
    if args.json:
        _print_json(payload)
        return
    for item in payload.get("items", []):
        print(
            f"{item.get('job_number','')}\t{item.get('name','')}\t{item.get('status','')}"
        )


def cmd_job(args: argparse.Namespace) -> None:
    token = _token(args)
    host = _host(args)
    slug = _quote_slug(args.project_slug)
    url = f"{host}/api/v2/project/{slug}/job/{args.job_number}"
    payload = _api_get(url, token)
    if args.json:
        _print_json(payload)
        return
    print(
        f"{payload.get('job_number','')}\t{payload.get('job_name','')}\t"
        f"{payload.get('status','')}\t{payload.get('started_at','')}\t"
        f"{payload.get('stopped_at','')}"
    )
    if not args.steps:
        return
    steps = payload.get("steps", [])
    for step in steps:
        step_name = step.get("name", "")
        for action in step.get("actions", []):
            action_name = action.get("name", "")
            status = action.get("status", "")
            output_url = action.get("output_url", "")
            print(f"{step_name}\t{action_name}\t{status}\t{output_url}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CircleCI API v2 status helper."
    )
    parser.add_argument(
        "--host",
        default="https://circleci.com",
        help="CircleCI host (default: https://circleci.com)",
    )
    parser.add_argument(
        "--token",
        help="CircleCI token (default: CIRCLECI_CLI_TOKEN env var)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON payload instead of tabular text",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pipelines = sub.add_parser("pipelines", help="List pipelines for a project.")
    pipelines.add_argument("project_slug", help="Project slug, e.g. gh/org/repo")
    pipelines.add_argument("--branch", help="Filter by VCS branch")
    pipelines.add_argument("--limit", type=int, help="Limit number of items")
    pipelines.set_defaults(func=cmd_pipelines)

    workflows = sub.add_parser("workflows", help="List workflows for a pipeline.")
    workflows.add_argument("pipeline_id", help="Pipeline ID")
    workflows.set_defaults(func=cmd_workflows)

    jobs = sub.add_parser("jobs", help="List jobs for a workflow.")
    jobs.add_argument("workflow_id", help="Workflow ID")
    jobs.set_defaults(func=cmd_jobs)

    job = sub.add_parser("job", help="Show job details (optionally steps).")
    job.add_argument("project_slug", help="Project slug, e.g. gh/org/repo")
    job.add_argument("job_number", help="Job number")
    job.add_argument(
        "--steps",
        action="store_true",
        help="Include steps/actions in output",
    )
    job.set_defaults(func=cmd_job)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
