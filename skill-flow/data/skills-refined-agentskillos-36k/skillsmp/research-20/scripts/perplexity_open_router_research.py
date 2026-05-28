#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "openai>=1.51.0",
# ]
# [tool.uv]
# exclude-newer = "2025-11-05T00:00:00Z"
# ///

"""
Usage:
  chmod +x sonar_search
  OPENROUTER_API_KEY=... ./sonar_search "What happened at Web Summit 2025?"
  --model perplexity/sonar-pro
  --json
  --no-sources
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

from openai import OpenAI


def get_api_key_from_filesystem(key_name: str) -> str:
    """Read API key from ~/.config/sops-nix/secrets/ directory."""
    key_file = os.path.expanduser(f"~/.config/sops-nix/secrets/{key_name}")
    try:
        with open(key_file, 'r') as f:
            return f.read().strip()
    except (FileNotFoundError, IOError):
        return None


def resp_to_dict(resp: Any) -> Dict[str, Any]:
    # Normalize the SDK object to a plain dict.
    for attr in ("model_dump_json", "to_json", "json"):
        if hasattr(resp, attr):
            try:
                raw = getattr(resp, attr)()
                return json.loads(raw)
            except Exception:
                pass
    # Fallback: Pydantic-style
    if hasattr(resp, "model_dump"):
        try:
            return resp.model_dump()
        except Exception:
            pass
    # Last resort
    try:
        return json.loads(str(resp))
    except Exception:
        return {}


def extract_text(d: Dict[str, Any]) -> str:
    try:
        return d["choices"][0]["message"]["content"] or ""
    except Exception:
        return ""


def _normalize_citation(c: Any) -> Dict[str, str] | None:
    # Accept str URL, or dict with url/uri and optional title.
    if isinstance(c, str):
        return {"url": c, "title": c}
    if isinstance(c, dict):
        url = c.get("url") or c.get("uri")
        title = c.get("title") or url
        if url:
            return {"url": url, "title": title or url}
    return None


def extract_citations(d: Dict[str, Any]) -> List[Dict[str, str]]:
    # Priority: top-level "citations" → "search_results" → message.metadata.citations
    out: List[Dict[str, str]] = []

    if isinstance(d.get("citations"), list):
        for c in d["citations"]:
            nc = _normalize_citation(c)
            if nc:
                out.append(nc)

    if not out and isinstance(d.get("search_results"), list):
        for r in d["search_results"]:
            nc = _normalize_citation(r)
            if nc:
                out.append(nc)

    if not out:
        try:
            meta = d["choices"][0]["message"].get("metadata") or {}
            if isinstance(meta.get("citations"), list):
                for c in meta["citations"]:
                    nc = _normalize_citation(c)
                    if nc:
                        out.append(nc)
        except Exception:
            pass

    # Deduplicate by URL order-preserving.
    seen = set()
    uniq = []
    for c in out:
        u = c["url"]
        if u not in seen:
            seen.add(u)
            uniq.append(c)
    return uniq


def add_inline_markers(text: str, citations: List[Dict[str, str]]) -> str:
    if not text:
        return ""
    # If model already included [1], keep as-is. Otherwise append simple markers.
    has_any = any(f"[{i}]" in text for i in range(1, min(len(citations), 9) + 1))
    if has_any or not citations:
        return text
    tail = "\n\nSources: " + " ".join(f"[{i+1}]" for i in range(len(citations)))
    return text + tail


def format_sources(citations: List[Dict[str, str]]) -> str:
    if not citations:
        return ""
    lines = []
    for i, c in enumerate(citations, start=1):
        title = c.get("title") or c.get("url") or "source"
        url = c.get("url") or ""
        if url:
            lines.append(f"- [{i}] {title} — {url}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Search using Perplexity models via OpenRouter API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What happened at Web Summit 2025?"
  %(prog)s --flash "Explain quantum computing"
  %(prog)s --deep "Explain quantum computing"
  %(prog)s --deeper "Research the latest AI developments"
  %(prog)s --model perplexity/sonar-pro --json "Search query"

Model options:
  --flash     Uses perplexity/sonar-pro (default)
  --deep      Uses perplexity/sonar-reasoning-pro
  --deeper    Uses perplexity/sonar-deep-research
"""
    )
    ap.add_argument("prompt", nargs="*", help="Query")
    ap.add_argument("--model", default="perplexity/sonar-pro", help="OpenRouter model id (default: perplexity/sonar-pro)")
    ap.add_argument("--deep", action="store_true", help="Use perplexity/sonar-reasoning-pro model")
    ap.add_argument("--deeper", action="store_true", help="Use perplexity/sonar-deep-research model")
    ap.add_argument("--flash", action="store_true", help="Use perplexity/sonar-pro model (default)")
    ap.add_argument("--json", action="store_true", help="Print raw JSON response")
    ap.add_argument("--no-sources", action="store_true", help="Hide the source list")
    args = ap.parse_args()

    prompt = " ".join(args.prompt).strip()
    if not prompt:
        print("Error: provide a prompt.", file=sys.stderr)
        sys.exit(2)

    # Handle model selection
    model = args.model
    if args.deep:
        model = "perplexity/sonar-reasoning-pro"
    elif args.deeper:
        model = "perplexity/sonar-deep-research"
    model = model + ":online"

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Try to read from filesystem
        api_key = get_api_key_from_filesystem("openrouter_api_key")

    if not api_key:
        print("Error: set OPENROUTER_API_KEY, or place key in ~/.config/sops-nix/secrets/openrouter_api_key", file=sys.stderr)
        sys.exit(2)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://example.com/sonar_script",
            "X-Title": "sonar_search_cli",
        },
    )

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    d = resp_to_dict(resp)
    text = extract_text(d)
    cites = extract_citations(d)

    print(add_inline_markers(text.strip(), cites))

    if cites and not args.no_sources:
        print("\nSources:")
        print(format_sources(cites))

    if args.json:
        print("\n--- RAW RESPONSE JSON ---")
        try:
            print(resp.model_dump_json(indent=2))
        except Exception:
            print(json.dumps(d, indent=2))


if __name__ == "__main__":
    main()
