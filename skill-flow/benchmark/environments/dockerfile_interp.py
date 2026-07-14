"""Minimal Dockerfile interpreter for the Apptainer environment.

Parses the subset of Dockerfile syntax used by SkillsBench tasks
(FROM / RUN / COPY / ADD / ENV / WORKDIR / ARG) into an ordered list of
instructions. CMD / ENTRYPOINT / EXPOSE / LABEL / USER are ignored because
harbor drives execution explicitly.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass


@dataclass
class Instruction:
    op: str  # FROM | RUN | COPY | ADD | ENV | WORKDIR | ARG
    value: str  # raw argument text (already line-continuation-joined)


def _join_continuations(text: str) -> list[str]:
    """Collapse backslash line-continuations; drop comments/blank lines."""
    lines: list[str] = []
    buf = ""
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not buf and (not stripped or stripped.startswith("#")):
            continue
        if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1] + " "
            continue
        buf += line
        lines.append(buf)
        buf = ""
    if buf:
        lines.append(buf)
    return lines


def parse_dockerfile(text: str) -> list[Instruction]:
    """Return the ordered instructions relevant to building a sandbox."""
    keep = {"FROM", "RUN", "COPY", "ADD", "ENV", "WORKDIR", "ARG"}
    out: list[Instruction] = []
    for line in _join_continuations(text):
        parts = line.strip().split(None, 1)
        if not parts:
            continue
        op = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""
        if op in keep:
            out.append(Instruction(op=op, value=arg))
    return out


def base_image(instructions: list[Instruction]) -> str:
    """Return the base image from the (first) FROM, stripping ``AS <stage>``."""
    for ins in instructions:
        if ins.op == "FROM":
            tokens = ins.value.split()
            # FROM [--platform=..] <image> [AS <name>]
            tokens = [t for t in tokens if not t.startswith("--platform")]
            return tokens[0]
    raise ValueError("Dockerfile has no FROM instruction")


def parse_env(value: str) -> list[tuple[str, str]]:
    """Parse an ENV instruction body into (key, value) pairs.

    Handles both ``ENV k=v k2=v2`` and the legacy ``ENV k the rest`` form.
    """
    toks0 = value.split()
    is_kv_form = bool(toks0) and "=" in toks0[0]
    if is_kv_form:
        pairs: list[tuple[str, str]] = []
        for tok in shlex.split(value):
            if "=" in tok:
                k, v = tok.split("=", 1)
                pairs.append((k, v))
        return pairs
    # legacy: ENV KEY rest of line
    toks = value.split(None, 1)
    if len(toks) == 2:
        return [(toks[0], toks[1].strip())]
    if len(toks) == 1:
        return [(toks[0], "")]
    return []


def parse_copy(value: str) -> tuple[list[str], str]:
    """Parse ``COPY``/``ADD`` into (sources, dest), dropping flags like --chown."""
    toks = [t for t in shlex.split(value) if not t.startswith("--")]
    if len(toks) < 2:
        raise ValueError(f"COPY/ADD needs >=2 args: {value!r}")
    return toks[:-1], toks[-1]
