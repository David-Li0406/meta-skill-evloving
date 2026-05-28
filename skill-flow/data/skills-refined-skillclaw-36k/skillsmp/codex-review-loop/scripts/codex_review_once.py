#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

CODEX_LOGIN = os.environ.get("CODEX_LOGIN", "codex")  # override if your org installs a different bot login
DEFAULT_TIMEOUT_SECS = int(os.environ.get("CODEX_TIMEOUT_SECS", "1800"))
DEFAULT_POLL_SECS = int(os.environ.get("CODEX_POLL_SECS", "20"))

# Accept labels like: [P0], P1:, Severity=P2, severity: P1
SEV_RE = re.compile(r"(?i)\b(?:\[?\s*(P0|P1|P2)\s*\]?|severity\s*[:=]\s*(P0|P1|P2))\b")

def run(cmd: List[str], *, capture: bool = True, check: bool = True) -> str:
    p = subprocess.run(cmd, text=True, capture_output=capture)
    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {' '.join(cmd)}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )
    return (p.stdout or "").strip()

def gh_json(args: List[str]) -> Any:
    out = run(["gh", *args])
    return json.loads(out) if out else None

def parse_mode(argv: List[str]) -> Tuple[str, List[str]]:
    # returns (mode, remaining_argv)
    # mode in {"blockers", "strict"}
    mode = "blockers"
    rem: List[str] = [argv[0]]
    for a in argv[1:]:
        if a in ("--blockers-only", "--blockers"):
            mode = "blockers"
        elif a in ("--strict",):
            mode = "strict"
        else:
            rem.append(a)
    return mode, rem

def detect_pr_ref(argv: List[str]) -> str:
    if len(argv) >= 2 and argv[1].strip():
        return argv[1].strip()
    # default: PR for current branch
    try:
        num = run(["gh", "pr", "view", "--json", "number", "-q", ".number"])
        return num.strip()
    except Exception:
        return ""

def parse_pr_number(pr_ref: str) -> Optional[int]:
    pr_ref = pr_ref.strip()
    if not pr_ref:
        return None
    m = re.search(r"/pull/(\d+)", pr_ref)
    if m:
        return int(m.group(1))
    m = re.match(r"^#?(\d+)$", pr_ref)
    if m:
        return int(m.group(1))
    return None

def repo_name_with_owner() -> str:
    return run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])

def list_pr_reviews(owner_repo: str, pr_number: int) -> List[Dict[str, Any]]:
    return gh_json(["api", "--paginate", f"/repos/{owner_repo}/pulls/{pr_number}/reviews?per_page=100"]) or []

def list_pr_review_comments(owner_repo: str, pr_number: int) -> List[Dict[str, Any]]:
    return gh_json(["api", "--paginate", f"/repos/{owner_repo}/pulls/{pr_number}/comments?per_page=100"]) or []

def list_issue_comments(owner_repo: str, pr_number: int) -> List[Dict[str, Any]]:
    return gh_json(["api", "--paginate", f"/repos/{owner_repo}/issues/{pr_number}/comments?per_page=100"]) or []

def post_codex_trigger_comment(pr_ref: str, run_id: str, extra: str = "") -> None:
    body = "@codex review"
    if extra.strip():
        body += "\n\n" + extra.strip()
    body += f"\n\n<!-- codex-loop:{run_id} -->\n"
    run(["gh", "pr", "comment", pr_ref, "--body", body], capture=True, check=True)

def to_set_int(xs: List[Any]) -> Set[int]:
    out: Set[int] = set()
    for x in xs:
        try:
            out.add(int(x))
        except Exception:
            pass
    return out

def extract_severity(text: str) -> Optional[str]:
    if not text:
        return None
    m = SEV_RE.search(text)
    if not m:
        return None
    return (m.group(1) or m.group(2) or "").upper() or None

def normalize_inline_comments(inline_comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    norm = []
    for c in inline_comments:
        body = (c.get("body") or "").strip()
        sev = extract_severity(body)
        norm.append({
            "id": c.get("id"),
            "path": c.get("path"),
            "line": c.get("line") or c.get("original_line"),
            "side": c.get("side"),
            "start_line": c.get("start_line") or c.get("original_start_line"),
            "body": body,
            "severity": sev,
            "html_url": c.get("html_url"),
        })
    return norm

def split_blockers(inline_norm: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    blockers = []
    nonblockers = []
    unknown = []
    for c in inline_norm:
        sev = c.get("severity")
        if sev in ("P0", "P1"):
            blockers.append(c)
        elif sev == "P2":
            nonblockers.append(c)
        else:
            unknown.append(c)
    return blockers, nonblockers, unknown

def compute_clean(mode: str, review: Dict[str, Any], blockers: List[Dict[str, Any]], nonblockers: List[Dict[str, Any]], unknown: List[Dict[str, Any]]) -> Tuple[bool, str]:
    state = (review.get("state") or "").upper()
    body = (review.get("body") or "").strip().lower()

    if mode == "strict":
        if state == "APPROVED":
            return True, "APPROVED"
        any_inline = bool(blockers or nonblockers or unknown)
        if not any_inline and any(p in body for p in ["no findings", "no issues", "looks good", "nothing to flag"]):
            return True, "Heuristic clean (strict)"
        return False, "Not approved (strict)"

    # blockers-only mode
    if state == "CHANGES_REQUESTED":
        return False, "CHANGES_REQUESTED"
    if unknown:
        return False, "Unknown-severity comments present (treated as blockers). Set CODEX_EXTRA_PROMPT to force P0/P1/P2 labels."
    if blockers:
        return False, "P0/P1 blockers present"
    return True, "No P0/P1 blockers"

def main() -> int:
    mode, argv = parse_mode(sys.argv)

    pr_ref = detect_pr_ref(argv)
    pr_number = parse_pr_number(pr_ref)
    if pr_number is None:
        print(json.dumps({"error": "Could not detect PR. Pass a PR number or PR URL, or run from a branch with an open PR."}, ensure_ascii=False))
        return 1

    owner_repo = repo_name_with_owner()

    # Snapshot existing Codex reviews (avoid picking up an old review)
    reviews_before = list_pr_reviews(owner_repo, pr_number)
    codex_review_ids_before = to_set_int([
        r.get("id") for r in reviews_before
        if (r.get("user") or {}).get("login", "").lower() == CODEX_LOGIN.lower()
    ])

    run_id = str(int(time.time()))
    extra = os.environ.get("CODEX_EXTRA_PROMPT", "").strip()
    if mode == "blockers" and not extra:
        extra = (
            "Please label every finding as P0/P1/P2. "
            "Only leave inline review comments for P0/P1 blockers. "
            "Summarize P2 (non-blocking suggestions) in the review body under a 'Non-blocking suggestions' section."
        )

    post_codex_trigger_comment(pr_ref, run_id, extra=extra)

    deadline = time.time() + DEFAULT_TIMEOUT_SECS
    newest_review: Optional[Dict[str, Any]] = None

    while time.time() < deadline:
        reviews_now = list_pr_reviews(owner_repo, pr_number)
        codex_reviews_now = [
            r for r in reviews_now
            if (r.get("user") or {}).get("login", "").lower() == CODEX_LOGIN.lower()
        ]
        new_candidates = [
            r for r in codex_reviews_now
            if int(r.get("id") or 0) not in codex_review_ids_before
        ]

        if new_candidates:
            def key(r: Dict[str, Any]) -> Tuple[str, int]:
                return (r.get("submitted_at") or "", int(r.get("id") or 0))
            newest_review = sorted(new_candidates, key=key)[-1]
            break

        # fallback: some installations may only post an issue comment
        issue_comments = list_issue_comments(owner_repo, pr_number)
        codex_issue_comments = [
            c for c in issue_comments
            if (c.get("user") or {}).get("login", "").lower() == CODEX_LOGIN.lower()
        ]
        if codex_issue_comments:
            newest_comment = sorted(codex_issue_comments, key=lambda c: (c.get("created_at") or "", int(c.get("id") or 0)))[-1]
            payload = {
                "mode": mode,
                "clean": False,
                "review": None,
                "inline_comments": [],
                "fallback_issue_comment": {
                    "id": newest_comment.get("id"),
                    "created_at": newest_comment.get("created_at"),
                    "body": (newest_comment.get("body") or "").strip(),
                    "html_url": newest_comment.get("html_url"),
                    "user": (newest_comment.get("user") or {}).get("login"),
                },
                "note": "Codex responded with an issue comment but did not post a PR review. Treat as findings and iterate manually.",
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

        time.sleep(DEFAULT_POLL_SECS)

    if newest_review is None:
        print(json.dumps({
            "error": "Timed out waiting for Codex review.",
            "hint": "Verify Codex GitHub code review is enabled for this repo, and that the bot login matches CODEX_LOGIN (default: codex).",
            "pr": pr_number,
            "repo": owner_repo,
            "codex_login": CODEX_LOGIN,
            "mode": mode,
        }, ensure_ascii=False, indent=2))
        return 3

    all_inline = list_pr_review_comments(owner_repo, pr_number)
    review_id = int(newest_review.get("id") or 0)
    inline = [
        c for c in all_inline
        if int(c.get("pull_request_review_id") or 0) == review_id
        and (c.get("user") or {}).get("login", "").lower() == CODEX_LOGIN.lower()
    ]

    review_state = (newest_review.get("state") or "").upper()
    review_body = (newest_review.get("body") or "").strip()

    inline_norm = normalize_inline_comments(inline)
    blockers, nonblockers, unknown = split_blockers(inline_norm)
    clean, clean_reason = compute_clean(mode, newest_review, blockers, nonblockers, unknown)

    payload = {
        "mode": mode,
        "clean": clean,
        "clean_reason": clean_reason,
        "pr": pr_number,
        "repo": owner_repo,
        "codex_login": CODEX_LOGIN,
        "review": {
            "id": newest_review.get("id"),
            "state": review_state or newest_review.get("state"),
            "submitted_at": newest_review.get("submitted_at"),
            "body": review_body,
            "html_url": newest_review.get("html_url"),
            "user": (newest_review.get("user") or {}).get("login"),
        },
        "inline_comments": inline_norm,
        "blockers": blockers,
        "non_blockers": nonblockers,
        "unknown_severity": unknown,
        "counts": {
            "total_inline": len(inline_norm),
            "blockers": len(blockers),
            "non_blockers": len(nonblockers),
            "unknown_severity": len(unknown),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if clean else 2

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
