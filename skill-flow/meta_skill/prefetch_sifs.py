"""Pre-populate the persistent SIF cache used by ApptainerEnvironment.

Each unique base image across the SkillsBench tasks is pulled from the registry
exactly once into ``APPTAINER_SIF_DIR`` (default /scratch/daweili5/apptainer-sif).
Task sandboxes then build from the local .sif with no registry access, so runs
are immune to Docker Hub's anonymous pull rate limit. Retries each image with
backoff so a temporarily-exhausted limit eventually drains.

    python -m meta_skill.prefetch_sifs                 # all task base images
    python -m meta_skill.prefetch_sifs ubuntu:24.04    # specific images
"""

from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# apptainer 1.4.5 corrupts its OCI cache index once it accumulates blobs across
# pulls, which then fails every later pull with "invalid character 's' after
# top-level value" (even when not rate-limited). A brand-new cache per pull
# avoids it. Each .sif is standalone, so the cache is just throwaway scratch.
_PULL_CACHE_BASE = "/scratch/daweili5/_sifcache"

from benchmark.environments.apptainer import _sif_path
from benchmark.environments.dockerfile_interp import base_image, parse_dockerfile

TASKS = Path("integration/skillsbench/tasks")
RL = "TOOMANYREQUESTS"


def unique_base_images() -> list[str]:
    imgs: dict[str, int] = {}
    for df in glob.glob(str(TASKS / "**" / "Dockerfile"), recursive=True):
        try:
            instr = parse_dockerfile(Path(df).read_text(encoding="utf-8"))
            img = base_image(instr)
        except Exception:  # noqa: BLE001
            continue
        if img:
            imgs[img] = imgs.get(img, 0) + 1
    return [k for k, _ in sorted(imgs.items(), key=lambda kv: -kv[1])]


def pull_one(img: str, max_tries: int = 40) -> bool:
    sif = _sif_path(img)
    if sif.exists() and sif.stat().st_size > 0:
        print(f"  [cached] {img} -> {sif.name}", flush=True)
        return True
    sif.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(sif) + ".tmp")
    backoff = 60
    safe = img.replace("/", "_").replace(":", "_")
    for attempt in range(1, max_tries + 1):
        # fresh, isolated cache for every attempt -> never reuses a corrupted index
        cache = f"{_PULL_CACHE_BASE}_{safe}_{attempt}"
        shutil.rmtree(cache, ignore_errors=True)
        os.makedirs(cache, exist_ok=True)
        env = {**os.environ, "APPTAINER_CACHEDIR": cache}
        proc = subprocess.run(
            ["apptainer", "pull", "--force", str(tmp), f"docker://{img}"],
            capture_output=True, text=True, env=env,
        )
        shutil.rmtree(cache, ignore_errors=True)
        if proc.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.rename(sif)
            print(f"  [ok]     {img} -> {sif.name} ({sif.stat().st_size//(1024*1024)}MB)", flush=True)
            return True
        err = (proc.stderr or "") + (proc.stdout or "")
        # Docker Hub's rate limit surfaces two ways through apptainer: the clean
        # TOOMANYREQUESTS message AND a parse error on the rate-limit HTML page
        # ("invalid character 's' after top-level value" / "conveyor failed to
        # get"). Both are retryable. Only give up on genuine not-found/auth errors.
        retryable = any(s in err for s in (
            RL, "pull rate limit", "invalid character", "conveyor failed to get",
            "i/o timeout", "TLS handshake", "connection reset"))
        fatal = any(s in err for s in (
            "manifest unknown", "name unknown", "not found", "NAME_UNKNOWN",
            "unauthorized", "requested access to the resource is denied"))
        tag = "rate-limited" if retryable else "error"
        print(f"  [{tag}] {img} attempt {attempt}/{max_tries}: {err.strip()[-160:]}", flush=True)
        if fatal or (not retryable and attempt >= 3):  # genuine failure: give up
            return False
        time.sleep(backoff)
        # cap at 5 min: the rolling limit frees gradually, so retry often enough
        # to grab capacity as soon as it returns (rejected 429s don't count).
        backoff = min(backoff * 2, 300)
    return False


def main() -> None:
    images = sys.argv[1:] or unique_base_images()
    print(f"prefetching {len(images)} base image(s):", flush=True)
    for i in images:
        print("   -", i, flush=True)
    ok, fail = [], []
    for img in images:
        # Docker Hub images (no registry host in the first path component) will
        # succeed once the rate limit drains -> retry generously. Non-DH
        # registries (gcr.io, quay.io) trip apptainer 1.4.5's OCI parse bug and
        # never succeed here -> give up fast so they don't block the rest.
        # A registry host is the first slash component only when it looks like a
        # host (contains "." or ":" port, or is localhost). Without a "/", the
        # image is a Docker Hub short ref (e.g. "ubuntu:24.04" — the dot is in
        # the TAG, not a registry).
        first = img.split("/")[0]
        has_registry = "/" in img and ("." in first or ":" in first
                                       or first == "localhost")
        mt = 3 if has_registry else 150  # non-DH registries trip the parse bug
        (ok if pull_one(img, max_tries=mt) else fail).append(img)
    print(f"\nDONE: {len(ok)} cached, {len(fail)} failed", flush=True)
    if fail:
        print("FAILED:", fail, flush=True)


if __name__ == "__main__":
    main()
