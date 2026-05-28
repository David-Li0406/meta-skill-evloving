#!/usr/bin/env python3
"""
Copy logs from Kubernetes pods into per-pod folders.

Examples:
  python3 copy_logs_from_k8s.py
  python3 copy_logs_from_k8s.py --sources tikv
  python3 copy_logs_from_k8s.py --sources tikv,tiflash
"""
import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Callable, Optional


def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout


TIKV_LOG_DIR = "/var/lib/tikv/log"
TIFLASH_LOG_DIR = "/data0/logs"
S3CLEAN_LOG = "/tmp/s3clean.log"
# Extend by adding a new LogSource in main() and listing its name here.
AVAILABLE_SOURCES = ("tikv", "tiflash", "s3clean")


def list_log_files(pod_name, log_dir, container=None):
    cmd = ["kubectl", "exec", pod_name]
    if container:
        cmd += ["-c", container]
    cmd += ["--", "find", log_dir, "-type", "f", "-print"]
    output = run(cmd)
    return [line.strip() for line in output.splitlines() if line.strip()]


def list_pods():
    pods_json = run(["kubectl", "get", "pods", "-o", "json"])
    data = json.loads(pods_json)
    return [item.get("metadata", {}).get("name", "") for item in data.get("items", [])]


def copy_file_from_pod_exec(pod_name, remote_path, local_path, container=None):
    # kubectl cp treats ':' as a separator and fails on filenames containing it.
    # Stream the file via exec/cat instead for those cases (e.g. tiflash log names).
    cmd = ["kubectl", "exec", pod_name]
    if container:
        cmd += ["-c", container]
    cmd += ["--", "cat", remote_path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    assert proc.stderr is not None
    with open(local_path, "wb") as handle:
        shutil.copyfileobj(proc.stdout, handle)
    proc.stdout.close()
    stderr = proc.stderr.read()
    returncode = proc.wait()
    if returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\n{stderr.decode().strip()}"
        )


def copy_file_from_pod(pod_name, remote_path, local_path, container=None, use_exec=False):
    # Force exec-based copy when requested or when filenames include ':'.
    if use_exec or ":" in remote_path:
        copy_file_from_pod_exec(pod_name, remote_path, local_path, container=container)
        return
    cmd = ["kubectl", "cp"]
    if container:
        cmd += ["-c", container]
    cmd += [f"{pod_name}:{remote_path}", str(local_path)]
    run(cmd)


def copy_log_dir_from_pod(pod_name, log_dir, dest_dir, container=None, use_exec=False):
    files = list_log_files(pod_name, log_dir, container)
    if not files:
        print(f"no log files found in {log_dir} for {pod_name}")
        return 0
    for file_path in files:
        rel_path = Path(file_path).relative_to(log_dir)
        target_dir = dest_dir / rel_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / rel_path.name
        copy_file_from_pod(
            pod_name, file_path, target_file, container=container, use_exec=use_exec
        )
    return len(files)


def copy_single_file_from_pod(
    pod_name, remote_path, dest_dir, container=None, dest_name=None, use_exec=False
):
    dest_name = dest_name or Path(remote_path).name
    dest_path = dest_dir / dest_name
    copy_file_from_pod(
        pod_name, remote_path, dest_path, container=container, use_exec=use_exec
    )
    return dest_path


@dataclass
class LogSource:
    name: str
    pod_predicate: Callable[[str], bool]
    log_dir: Optional[str] = None
    single_file: Optional[str] = None
    container: Optional[str] = None
    dest_name: Optional[str] = None
    # Some logs need exec-based copy because kubectl cp can't handle ':' in filenames.
    use_exec_copy: bool = False


def process_source(source, pod_names_all, base_dir):
    pods = [name for name in pod_names_all if source.pod_predicate(name)]
    if not pods:
        print(f"no {source.name} pods found")
        return

    for pod_name in pods:
        dest_dir = base_dir / pod_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        if source.log_dir:
            count = copy_log_dir_from_pod(
                pod_name,
                source.log_dir,
                dest_dir,
                container=source.container,
                use_exec=source.use_exec_copy,
            )
            if count:
                print(f"copied {count} log file(s) from {pod_name} -> {dest_dir}")
        if source.single_file:
            dest_path = copy_single_file_from_pod(
                pod_name,
                source.single_file,
                dest_dir,
                container=source.container,
                dest_name=source.dest_name,
                use_exec=source.use_exec_copy,
            )
            print(f"copied {source.single_file} from {pod_name} -> {dest_path}")


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--sources",
        default=",".join(AVAILABLE_SOURCES),
        help="Comma-separated list of sources to download: tikv,tiflash,s3clean",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    selected_sources = {name.strip() for name in args.sources.split(",") if name.strip()}
    unknown_sources = sorted(selected_sources.difference(AVAILABLE_SOURCES))
    if unknown_sources:
        print(f"unknown sources: {', '.join(unknown_sources)}", file=sys.stderr)
        return 2
    if not selected_sources:
        print("no sources selected", file=sys.stderr)
        return 2

    try:
        pod_names_all = list_pods()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    base_dir = Path.cwd()
    # To add new pod types, append a LogSource here and add its name to AVAILABLE_SOURCES.
    sources = [
        LogSource(
            name="tikv",
            pod_predicate=lambda name: "tikv" in name and "tikv-worker" not in name,
            log_dir=TIKV_LOG_DIR,
        ),
        LogSource(
            name="tiflash",
            pod_predicate=lambda name: "tiflash" in name and "tiflash-minio" not in name,
            log_dir=TIFLASH_LOG_DIR,
            container="serverlog",
            # Tiflash logs include ':' in filenames, which breaks kubectl cp.
            use_exec_copy=True,
        ),
        LogSource(
            name="s3clean",
            pod_predicate=lambda name: "s3clean" in name,
            single_file=S3CLEAN_LOG,
        ),
    ]

    try:
        for source in sources:
            if source.name in selected_sources:
                process_source(source, pod_names_all, base_dir)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
